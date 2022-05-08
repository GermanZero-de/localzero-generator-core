from collections import defaultdict
import csv
from functools import reduce
from itertools import groupby
import json
import sqlite3
from disjoint_set import DisjointSet

# Diese AGS werden ignoriert, weil wir zurzeit für gemeindefreie Gebiete keine Daten aufbereiten.
IGNORE = {
    "01053105": "Sachsenwald ist ein gemeindefreies Gebiet",
    "01060014": "BuchholzerForstist ist ein gemeindefreies Gebiet",
    "03153504": "Harz (Landkreis Goslar), gemfr. Gebiet ist ein gemeindefreies Gebiet",
    "03155501": "Solling (Landkreis Northeim) ist ein gemeindefreies Gebiet",
    "06435200": "Gutsbezirk Spessart ist ist ein gemeindefreies Gebiet",
    "09478444": "Neuensorger Forst ist ein gemeindefreies gebiet",
    "09478451": "Breitengüßbacher Forst ist ein gemeindefreies Gebiet",
    "09478453": "Neuensorger Forst ist ein gemeindefreies Gebiet",
    "09572444": "Gdefr. Geb. (Lkr Erlangen-Höchstadt) ist ein gemeindefreies Gebiet",
    "09572451": "Birkach ist ein gemeindefreies Gebiet",
    "09572452": "Buckenhofer Forst",
    "09572453": "Dormitzer Forst",
    "09572454": "Erlenstegener Forst",
    "09572455": "Forst Tennenlohe",
    "09572456": "Geschaidt",
    "09572457": "Kalchreuther Forst",
    "09572458": "Kraftshofer Forst",
    "09572459": "Mark",
    "09572460": "Neunhofer Forst",
}


def power_per_component(
    ags_history, unit_power
) -> tuple[dict[str, set[str]], defaultdict[str, float]]:
    """
    Accumulates power of active units per connected component of AGS.

    A connected component of AGS is the maximum set of AGS that are connected
    through predecessor or successor relationships as detailed in the AGS
    history.

    >>> ags_history = [("01051001", "01057777")]
    >>> unit_power = [
    ...     ("01051001", 1.0),
    ...     ("01057777", 2.0),
    ...     ("07232249", 4.0)
    ... ]
    >>> cmpnt_ags, cmpnt_power = power_per_component(ags_history, unit_power)
    >>> cmpnt_ags == {"01057777": {"01051001", "01057777"}, "07232249": {"07232249"}}
    True
    >>> cmpnt_power == {"01057777": 3.0, "07232249": 4.0}
    True
    """
    cmpnts = DisjointSet()
    for ags1, ags2 in ags_history:
        cmpnts.union(ags1, ags2)

    cmpnt_power = defaultdict(float)
    for ags, power in unit_power:
        cmpnt_power[cmpnts.find(ags)] += power

    return dict(cmpnts.itersets(with_canonical_elements=True)), cmpnt_power


def power_per_ags(
    cmpnt_ags, cmpnt_power, population
) -> tuple[float, defaultdict[str, float]]:
    """
    Distributes power of AGS cmpnts over AGS by population.

    >>> cmpnt_ags = {"01057777": {"01051001", "01057777"}, "07232249": {"07232249"}}
    >>> cmpnt_power = {"01057777": 3.0, "07232249": 4.0}
    >>> population = {"01051001": 1000, "01057777": 2000, "07232249": 3000}
    >>> power_lost, ags_power = power_per_ags(cmpnt_ags, cmpnt_power, population)
    >>> power_lost
    0
    >>> ags_power["01051001"]
    1.0
    >>> ags_power["01057777"]
    2.0
    >>> ags_power["07232249"]
    4.0

    (Aggregation is tested separately, see the 'aggregate' function.)
    """
    # ags_power will map each AGS to an approximation of the amount of power produced there.
    ags_power = defaultdict(float)
    power_lost = 0

    for cmpnt_id, total_power in cmpnt_power.items():
        # Ignore AGS with zero inhabitants. This also makes sure that we only distribute power to the ags keys we use with local zero!
        populated = [ags for ags in cmpnt_ags[cmpnt_id] if ags in population.keys() and population[ags] > 0]
        if len(populated) == 0:
            if set(cmpnt_ags[cmpnt_id]).issubset(IGNORE):
                power_lost += total_power
                continue
            else:
                raise Exception(f"Component {cmpnt_id} is empty!")
        total_population = sum(population[ags] for ags in populated)
        power_per_person = total_power / total_population
        ags_power.update((ags, power_per_person * population[ags]) for ags in populated)

    return power_lost, aggregate(ags_power)


def unit_query(column_name):
    """
    Creates a query for units in the given column that were active at a specific cut-off date.

    This cut-off date must be provided as a query parameter called "cutoff_date".
    The query works for unit tables in the Marktstammdatenregister.dev SQLite export, which can be
    downloaded and extracted as follows:

    curl https://s3.eu-central-1.wasabisys.com/mastr-backup/Marktstammdatenregister.db.gz | gunzip - >Marktstammdatenregister.db
    """
    return f"""
        select
            Gemeindeschluessel,
            Bruttoleistung
        from
            {column_name}
        where
            Gemeindeschluessel is not null
            and Inbetriebnahmedatum <= :cutoff_date -- Vor/am Stichtag in Betrieb genommen ...
            and (
                -- ... und nie oder nach Stichtag stillgelegt ...
                DatumEndgueltigeStilllegung is null
                or DatumEndgueltigeStilllegung > :cutoff_date
            )
            and (
                -- ... und nie voruebergehend stillgelegt oder vor/am Stichtag wieder in Betrieb genommen.
                DatumBeginnVoruebergehendeStilllegung is null
                or DatumWiederaufnahmeBetrieb <= :cutoff_date
        )
        """


def read_population_csv(filename) -> dict[str, int]:
    """
    Reads a CSV file containing population data.

    The expected format is <AGS as string>, <population as integer>.
    """
    with open(filename, "r") as f:
        r = csv.reader(f)
        next(r)  # Skip header.
        return dict(((ags, int(pop)) for (ags, pop) in r))


def read_ags_master_csv(filename) -> frozenset[str]:
    """
    Reads the "master.csv" file containing all AGS.

    The expected format is <AGS as string>, <name as string>
    """
    with open(filename, "r") as f:
        r = csv.reader(f)
        next(r)  # Skip header.
        return frozenset(ags for [ags, _name] in r)


def read_ags_history_json(filename) -> tuple[tuple[str, str]]:
    """
    Reads the "AGS Historie" JSON file from Destatis.

    See https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
    """
    with open(filename, "r",encoding="utf-8") as f:
        return tuple(
            (AGS, NachfolgerAGS)
            for [
                _Code,
                AGS,
                _GemeindenameMitZusatz,
                _gueltigAb,
                _Aenderungsart,
                _gueltigBis,
                NachfolgerAGS,
                _NachfolgerName,
                _NachfolgerGueltigAb,
                _Hinweis,
            ] in json.load(f)["daten"]
            if AGS is not None and NachfolgerAGS is not None
        )


def aggregate(ags_power: defaultdict[str, float]) -> defaultdict[str, float]:
    """
    Aggregates nationwide, per-state, and per-district power.

    Modifies the argument and returns it for convenience.

    >>> original = {"01051001": 1.0, "01057777": 2.0}
    >>> result = aggregate(dict(original))
    >>> sorted(list(result.keys()))
    ['01000000', '01051000', '01051001', '01057000', '01057777', 'DG000000']
    >>> set(original.items()).issubset(set(result.items()))
    True
    >>> result["01000000"]
    3.0
    >>> result["01051000"]
    1.0
    >>> result["01057000"]
    2.0
    >>> result["DG000000"]
    3.0
    """
    state_prefix = lambda ags: ags[:2]
    district_prefix = lambda ags: ags[:5]
    ags_sorted = sorted(list(ags_power.keys()))

    # Do this first so we don't include state and district aggregates.
    ags_power["DG000000"] = sum(ags_power.values())

    # Use keys from ags_sorted to avoid including previous aggregates.
    for state, ags in groupby(ags_sorted, state_prefix):
        ags_power[state + "000000"] = sum(ags_power[x] for x in ags)
    for district, ags in groupby(ags_sorted, district_prefix):
        ags_power[district + "000"] = sum(ags_power[x] for x in ags)

    return ags_power


if __name__ == "__main__":
    import sys

    cutoff_date = "2021-12-31"

    population = read_population_csv(sys.argv[1])
    ags_history = read_ags_history_json(sys.argv[2])

    dicts = ()
    with sqlite3.connect(f"file:{sys.argv[3]}?mode=ro", uri=True) as mastr_con:

        def power(column):
            unit_power = mastr_con.execute(
                unit_query(column), {"cutoff_date": cutoff_date}
            )
            cmpnt_ags, cmpnt_power = power_per_component(ags_history, unit_power)
            return power_per_ags(cmpnt_ags, cmpnt_power, population)

        pv_lost, pv = power("EinheitSolar")
        wind_lost, wind = power("EinheitWind")
        biomass_lost, biomass = power("EinheitBiomasse")
        water_lost, water = power("EinheitWasser")

        dicts = (pv, wind, biomass, water)

        total_lost = pv_lost + wind_lost + biomass_lost + water_lost
        print(f"Total power lost: {total_lost} kW")

    def rows():
        for ags in sorted(population.keys()):
            yield [ags] + [f"{d[ags]:.3f}" if d[ags] != 0 else "0" for d in dicts]
            # yield [ags] + [str(d[ags]) for d in dicts]

    with open("out3.csv", "w", newline="") as f:
        writer = csv.writer(f)

        #write header
        writer.writerow(["ags", "pv", "wind", "biomass", "water"])
        writer.writerows(rows())
