from typing import TypedDict, Literal

from .. import generator


def identity(x):
    return x


class Overridable(TypedDict):
    override_name: str
    override_type: Literal["int", "float"]
    override_label: str


class OverridableWithDefault(Overridable):
    override_default: int | float


class Info(TypedDict):
    info_title: str
    info_text: str


class OverridableSection(TypedDict):
    section: str
    elements: list[Overridable | Info]


class OverridableSectionWithDefaults(TypedDict):
    section: str
    elements: list[OverridableWithDefault | Info]


_sections: list[OverridableSection] = [
    {
        "section": r"Basisdaten von '${CITYDESC}'",
        "elements": [
            {
                "override_name": "m_population_com_203X",
                "override_type": "int",
                "override_label": "Prognostizierte Einwohnerzahl im Zieljahr",
            },
            {
                "override_name": "r_buildings_2011_today",
                "override_type": "int",
                "override_label": "Anzahl Gebäude Baujahr 2011 - 2018",
            },
        ],
    },
    {
        "section": "Endenergieverbrauch Private Haushalte (MWh)",
        "elements": [
            {
                "override_name": "r_coal_fec",
                "override_type": "int",
                "override_label": "Kohle",
            },
            {
                "override_name": "r_petrol_fec",
                "override_type": "int",
                "override_label": "Benzin",
            },
            {
                "override_name": "r_fueloil_fec",
                "override_type": "int",
                "override_label": "Heizöl",
            },
            {
                "override_name": "r_lpg_fec",
                "override_type": "int",
                "override_label": "Flüssiggas",
            },
            {
                "override_name": "r_gas_fec",
                "override_type": "int",
                "override_label": "Erdgas",
            },
            {
                "override_name": "r_biomass_fec",
                "override_type": "int",
                "override_label": "Biomasse",
            },
            {
                "override_name": "r_orenew_fec",
                "override_type": "int",
                "override_label": "Solarthermie",
            },
            {
                "override_name": "r_elec_fec",
                "override_type": "int",
                "override_label": "Strom",
            },
            {
                "override_name": "r_heatnet_fec",
                "override_type": "int",
                "override_label": "Fernwärme",
            },
        ],
    },
    {
        "section": "Endenergieverbrauch Gewerbe, Handel, Dienstleistung und Sonstige (MWh)",
        "elements": [
            {
                "override_name": "b_coal_fec",
                "override_type": "int",
                "override_label": "Kohle",
            },
            {
                "override_name": "b_petrol_fec",
                "override_type": "int",
                "override_label": "Benzin",
            },
            {
                "override_name": "b_jetfuel_fec",
                "override_type": "int",
                "override_label": "Kerosin",
            },
            {
                "override_name": "b_diesel_fec",
                "override_type": "int",
                "override_label": "Diesel",
            },
            {
                "override_name": "b_fueloil_fec",
                "override_type": "int",
                "override_label": "Heizöl",
            },
            {
                "override_name": "b_lpg_fec",
                "override_type": "int",
                "override_label": "Flüssiggas",
            },
            {
                "override_name": "b_gas_fec",
                "override_type": "int",
                "override_label": "Erdgas",
            },
            {
                "override_name": "b_biomass_fec",
                "override_type": "int",
                "override_label": "Biomasse",
            },
            {
                "override_name": "b_orenew_fec",
                "override_type": "int",
                "override_label": "Sonstige Erneuerbare Energien",
            },
            {
                "override_name": "b_elec_fec",
                "override_type": "int",
                "override_label": "Strom",
            },
            {
                "override_name": "b_heatnet_fec",
                "override_type": "int",
                "override_label": "Fernwärme",
            },
        ],
    },
    # {
    #     "section": "Endenergieverbrauch Industrie (MWh)",
    #     "elements": [
    #         {
    #             "override_name": "i_coal_fec",
    #             "override_type": "int",
    #             "override_label": "Kohle",
    #         },
    #         {
    #             "override_name": "i_diesel_fec",
    #             "override_type": "int",
    #             "override_label": "Diesel",
    #         },
    #         {
    #             "override_name": "i_fueloil_fec",
    #             "override_type": "int",
    #             "override_label": "Heizöl",
    #         },
    #         {
    #             "override_name": "i_lpg_fec",
    #             "override_type": "int",
    #             "override_label": "Flüssiggas",
    #         },
    #         {
    #             "override_name": "i_gas_fec",
    #             "override_type": "int",
    #             "override_label": "Erdgas",
    #         },
    #         {
    #             "override_name": "i_opetpro_fec",
    #             "override_type": "int",
    #             "override_label": "Sonstige Mineralölprodukte",
    #         },
    #         {
    #             "override_name": "i_biomass_fec",
    #             "override_type": "int",
    #             "override_label": "Biomasse",
    #         },
    #         {
    #             "override_name": "i_orenew_fec",
    #             "override_type": "int",
    #             "override_label": "Sonstige Erneuerbare Energien",
    #         },
    #         {
    #             "override_name": "i_ofossil_fec",
    #             "override_type": "int",
    #             "override_label": "Sonstige Konventionelle",
    #         },
    #         {
    #             "override_name": "i_elec_fec",
    #             "override_type": "int",
    #             "override_label": "Strom",
    #         },
    #         {
    #             "override_name": "i_heatnet_fec",
    #             "override_type": "int",
    #             "override_label": "Fernwärme",
    #         },
    #     ],
    # },
    # {
    #     "section": "Industrieanteile",
    #     "elements": [
    #         {
    #             "info_title": "Erklärung",
    #             "info_text": """Hier kann eine geschätzte Endenergie-Zuteilung der kommunalen Industriestruktur (mineralische, chemische, metallische und sonstige Industrie)
    #             erfolgen. Weißt du bspw., dass es keine Metallische Industrie gibt, setzt du diesen Wert auf 0 und teilst die anderen Subsektoren so auf, dass sie in Summe 1 ergeben.
    #             Zur Orientierung kannst du die größten Emittenten in der
    #             <a href="https://www.dehst.de/DE/Europaeischer-Emissionshandel/Anlagenbetreiber/2013-2020/2013-2020_node.html" target="_blank" rel="noopener nofollow" style="color: #00aed8">Anlagenliste 2018 bei der DEHSt</a> nachschauen.
    #             Eine grobe graphische Übersicht und Einführung in die Industriezweige bietet zudem die Studie
    #             <a href="https://www.agora-energiewende.de/veroeffentlichungen/klimaneutrale-industrie-hauptstudie/" target="_blank" rel="noopener nofollow" style="color: #00aed8">"Klimaneutrale Industrie" von Agora Energiewende</a>""",
    #         },
    #         {
    #             "override_name": "i_fec_pct_of_miner",
    #             "override_type": "float",
    #             "override_label": "Anteil mineralische Industrie",
    #         },
    #         {
    #             "override_name": "i_fec_pct_of_chem",
    #             "override_type": "float",
    #             "override_label": "Anteil chemische Industrie",
    #         },
    #         {
    #             "override_name": "i_fec_pct_of_metal",
    #             "override_type": "float",
    #             "override_label": "Anteil metallische Industrie",
    #         },
    #         {
    #             "override_name": "i_fec_pct_of_other",
    #             "override_type": "float",
    #             "override_label": "Anteil sonstige Industrie",
    #         },
    #     ],
    # },
    {
        "section": "Endenergieverbrauch Landwirtschaft (MWh)",
        "elements": [
            {
                "override_name": "a_petrol_fec",
                "override_type": "int",
                "override_label": "Benzin",
            },
            {
                "override_name": "a_diesel_fec",
                "override_type": "int",
                "override_label": "Diesel",
            },
            {
                "override_name": "a_fueloil_fec",
                "override_type": "int",
                "override_label": "Heizöl",
            },
            {
                "override_name": "a_lpg_fec",
                "override_type": "int",
                "override_label": "Flüssiggas",
            },
            {
                "override_name": "a_gas_fec",
                "override_type": "int",
                "override_label": "Erdgas",
            },
            {
                "override_name": "a_biomass_fec",
                "override_type": "int",
                "override_label": "Biomasse",
            },
            {
                "override_name": "a_elec_fec",
                "override_type": "int",
                "override_label": "Strom",
            },
            {
                "override_name": "a_fermen_dairycow_amount",
                "override_type": "int",
                "override_label": "Anzahl Milchkühe",
            },
            {
                "override_name": "a_fermen_nondairy_amount",
                "override_type": "int",
                "override_label": "Anzahl übrige Rinder",
            },
            {
                "override_name": "a_fermen_pig_amount",
                "override_type": "int",
                "override_label": "Anzahl Schweine",
            },
            {
                "override_name": "a_fermen_poultry_amount",
                "override_type": "int",
                "override_label": "Anzahl Geflügel",
            },
            {
                "override_name": "a_fermen_oanimal_amount",
                "override_type": "int",
                "override_label": "Anzahl andere Tiere",
            },
        ],
    },
    {
        "section": "Verkehr",
        "elements": [
            {
                "info_title": "Hinweis zum Sektor Verkehr",
                "info_text": "Für den Verkehrssektor liegen bereits kommunenfeine Straßenverkehrsdaten des Instituts für Energie- und Umweltforschung (ifeu) vor.",
            }
        ],
    },
]


def overridables_only() -> list[Overridable]:
    """Only the overridables without section data / infos or defaults."""
    res: list[Overridable] = []
    for s in _sections:
        for entry in s["elements"]:
            if "info_title" in entry:
                pass
            else:
                res.append(entry)

    return res


def sections_with_defaults(
    data: generator.RefData, ags: str, year_baseline: int, year_target: int
) -> list[OverridableSectionWithDefaults]:
    """Complete overridable data including section data and info blocks, with defaults
    populated."""
    entries = generator.make_entries(data, ags, year_baseline, year_target)
    res: list[OverridableSectionWithDefaults] = []
    for os in _sections:
        populated_section: OverridableSectionWithDefaults = {
            "section": os["section"],
            "elements": [],
        }
        for oe in os["elements"]:
            if "info_title" in oe:
                populated_section["elements"].append(oe)  # type: ignore oe is of type Info here
            else:
                populated_e: OverridableWithDefault = {
                    "override_name": oe["override_name"],
                    "override_type": oe["override_type"],
                    "override_label": oe["override_label"],
                    "override_default": getattr(entries, oe["override_name"]),
                }
                populated_section["elements"].append(populated_e)

        res.append(populated_section)

    return res
