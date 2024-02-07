# pyright: strict

from typing import TextIO, Any, Callable
import csv
import sys
import os.path

from climatevision.generator import ags, refdatatools, refdata


def cmd_data_normalize(args: Any):
    def sortby_and_check_ags_column(rows: list[list[str]]) -> list[list[str]]:
        header = rows[0]
        if header[0] != "ags":
            # All files that have an AGS have it in the first column.
            return rows
        rows_with_invalid_ags = list(filter(lambda r: not ags.is_valid(r[0]), rows))
        if len(rows_with_invalid_ags) > 0:
            print(f"Found {len(rows_with_invalid_ags)} rows with invalid ags:\n")
            for r in rows_with_invalid_ags:
                print("\t", *r)
            exit(1)
        return sorted(rows, key=lambda r: r[0])

    def find_duplicate_ags_in_sorted(rows: list[list[str]]) -> list[list[str]]:
        dups = []
        current = []
        for r in rows:
            if len(current) > 0 and r[0] == current[0][0]:  # type: ignore
                current.append(r)  # type: ignore
            else:
                if len(current) > 1:  # type: ignore
                    dups.append(current)  # type: ignore
                current = [r]
        return dups  # type: ignore

    with open(args.file, "r", newline="", encoding="utf-8") as fp:
        rows_with_header = list(csv.reader(fp))

    sorted_rows = sortby_and_check_ags_column(rows_with_header[1:])
    dups = find_duplicate_ags_in_sorted(sorted_rows)
    if len(dups) > 0:
        print(f"Found {len(dups)} AGS that had more dataset\n")
        for d in dups:
            print("\t", d[0][0])
            for r in d:
                print("\t\t", *(r[1:]))
    with open(args.file, "w", encoding="utf-8") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        writer.writerow(rows_with_header[0])
        for row in sorted_rows:
            data = [x.replace("\n", " ") if type(x) == str else x for x in row]
            writer.writerow(data)


def cmd_data_is_production(args: Any):
    ds = refdatatools.DataDirStatus.get(refdatatools.datadir())
    # TODO: Add a verbose option that prints a json of DataDirStatus
    if not ds.is_good():
        exit(1)


def bold(s, end=None, file: TextIO = sys.stdout):  # type: ignore
    print(f"\033[1m{s}\033[0m", end=end, file=file)  # type: ignore


def faint(s, end=None, file: TextIO = sys.stdout):  # type: ignore
    print(f"\033[2m{s}\033[0m", end=end, file=file)  # type: ignore


def lookup_by_ags(data: refdata.RefData, ags: str):
    ags_dis = ags[:5] + "000"  # This identifies the administrative district (Landkreis)
    ags_sta = ags[:2] + "000000"  # This identifies the federal state (Bundesland)

    def print_lookup(name: str, lookup_fn: Callable[[str], refdata.Row[str]], key: str):
        bold(name)
        try:
            record: object = lookup_fn(key)
        except Exception:
            record = None

        if record is None:
            print("", "MISSING", sep="\t")
        else:
            print(record)
        print()

    by_ags = [
        ("area", data.area),
        ("area_kinds", data.area_kinds),
        ("buildings", data.buildings),
        ("population", data.population),
        ("renewable_energy", data.renewable_energy),
        ("flats", data.flats),
        ("traffic", data.traffic),
    ]

    by_dis = [
        ("destatis", data.destatis),
    ]

    by_sta = [
        ("nat_agri", data.nat_agri),
        ("nat_organic_agri", data.nat_organic_agri),
        ("nat_energy", data.nat_energy),
        ("nat_res_buildings", data.nat_res_buildings),
    ]

    description = data.ags_master().get(ags, "MISSING IN MASTER")

    bold(f"{ags} {description} (commune level data)")
    bold("---------------------------------------------------------------")
    print()
    for name, lookup_fn in by_ags:
        print_lookup(name, lookup_fn, key=ags)

    bold(f"{ags_dis} (administrative district level data)")
    bold("--------------------------------------------------")
    print()
    for name, lookup_fn in by_dis:
        print_lookup(name, lookup_fn, key=ags_dis)

    bold(f"{ags_sta} (federal state level data)")
    bold("--------------------------------------------------")
    print()
    for name, lookup_fn in by_sta:
        print_lookup(name, lookup_fn, key=ags_sta)


def print_fact_or_ass(name: str, record: refdata.FactOrAssumptionCompleteRow):
    bold(name)
    print(record.value, end="")
    if record.unit != "":
        print(f" {record.unit}\t({record.description})")
    else:
        print(f"\t({record.description})")
    print("")
    if record.rationale:
        print(record.rationale)
    if record.reference or record.link:
        bold("reference")
        print(record.reference)
        print(record.link)
    else:
        bold("reference")
        faint("no reference provided")


def lookup_fact(data: refdata.RefData, pattern: str):
    try:
        complete_fact = data.facts().complete_fact(pattern)
        print_fact_or_ass(name=pattern, record=complete_fact)
    except:
        bold(f"No fact called {pattern} found!", file=sys.stderr)
        exit(1)


def lookup_ass(data: refdata.RefData, pattern: str):
    try:
        complete_ass = data.assumptions().complete_ass(pattern)
        print_fact_or_ass(name=pattern, record=complete_ass)
    except:
        bold(f"No assumption called {pattern} found!", file=sys.stderr)
        exit(1)


def cmd_data_lookup(args: Any):
    pattern: str = args.pattern
    data: refdata.RefData = refdata.RefData.load(
        year_ref=args.year_ref, fix_missing_entries=args.fix_missing_entries
    )

    if ags.is_valid(pattern):
        lookup_by_ags(data, pattern)
    elif pattern.startswith("Ass_"):
        lookup_ass(data, pattern)
    elif pattern.startswith("Fact_"):
        lookup_fact(data, pattern)
    else:
        print(
            f"This {pattern} does not look like a AGS, fact or pattern... do not know what to do... giving up!",
            file=sys.stderr,
        )


def cmd_data_checkout(args: Any):
    def update_existing(
        repo: refdatatools.PUBLIC_OR_PROPRIETARY, *, current: str, wanted: str
    ):
        if current == wanted:
            if not freshly_cloned:
                print(
                    f"{repo} already contains a checkout of {wanted} -- not touching it",
                    file=sys.stderr,
                )
        else:
            print(f"switching {repo} from {current} to {wanted}")
            # First switch to main before pulling -- this has the least chance of causing
            # trouble as we should merge on github
            refdatatools.checkout(datadir, repo, "main")
            # refdatatools.pull uses --ff-only
            refdatatools.pull(datadir, repo, pa_token=args.pat)
            # Now we should have all changes and can switch to whatever the production file
            # wants
            refdatatools.checkout(datadir, repo, wanted)

    datadir = refdatatools.datadir()
    public_dir = os.path.join(datadir, "public")
    proprietary_dir = os.path.join(datadir, "proprietary")
    freshly_cloned = False

    # Clone the repos if there is nothing at all
    if not os.path.exists(public_dir) and not os.path.exists(proprietary_dir):
        print(
            "Looks like there is no checkout at all yet -- cloning for you",
            file=sys.stderr,
        )
        refdatatools.clone(datadir, "public", pa_token=args.pat)
        refdatatools.clone(datadir, "proprietary", pa_token=args.pat)
        freshly_cloned = True

    # now figure out the current state
    status = refdatatools.DataDirStatus.get(datadir)

    # make sure we are not causing data loss
    if not status.public_status.is_clean or not status.proprietary_status.is_clean:
        print(
            "There uncommitted changes or untracked files in at least one data repository. Fix that first."
        )
        exit(1)

    # Alright now pull and checkout the wanted hashes
    update_existing(
        "public", current=status.public_status.rev, wanted=status.production.public
    )
    update_existing(
        "proprietary",
        current=status.proprietary_status.rev,
        wanted=status.production.proprietary,
    )
