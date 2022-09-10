# pyright: strict

from dataclasses import asdict
from typing import Callable, Literal, TextIO, Any
import csv
import sys
import os.path
import json

from generatorcore import ags, refdatatools, refdata, makeentries


def cmd_data_normalize(args: Any):
    def sortby_and_check_ags_column(rows: Any):
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

    def find_duplicate_ags_in_sorted(rows: Any) -> Any:
        dups = []
        current = []
        for r in rows:
            if len(current) > 0 and r[0] == current[0][0]:
                current.append(r)
            else:
                if len(current) > 1:
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
            writer.writerow(row)


def cmd_data_is_production(args: Any):
    ds = refdatatools.DataDirStatus.get(refdatatools.datadir())
    # TODO: Add a verbose option that prints a json of DataDirStatus
    if not ds.is_good():
        exit(1)


def bold(s, end=None, file: TextIO = sys.stdout):  # type: ignore
    print(f"\033[1m{s}\033[0m", end=end, file=file)  # type: ignore


def faint(s, end=None, file: TextIO = sys.stdout):  # type: ignore
    print(f"\033[2m{s}\033[0m", end=end, file=file)  # type: ignore


def lookup_by_ags(ags: Any, *, fix_missing_entries: bool):
    ags_dis = ags[:5] + "000"  # This identifies the administrative district (Landkreis)
    ags_sta = ags[:2] + "000000"  # This identifies the federal state (Bundesland)

    def print_lookup(name: Any, lookup_fn: Any, key: Any):
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

    data = refdata.RefData.load(fix_missing_entries=fix_missing_entries)

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
    for (name, lookup_fn) in by_ags:
        print_lookup(name, lookup_fn, key=ags)

    bold(f"{ags_dis} (administrative district level data)")
    bold("--------------------------------------------------")
    print()
    for (name, lookup_fn) in by_dis:
        print_lookup(name, lookup_fn, key=ags_dis)

    bold(f"{ags_sta} (federal state level data)")
    bold("--------------------------------------------------")
    print()
    for (name, lookup_fn) in by_sta:
        print_lookup(name, lookup_fn, key=ags_sta)


def lookup_fact_or_ass(
    pattern: str,
    what: Literal["fact", "assumption"],
    lookup: Callable[
        [refdata.FactsAndAssumptions, str], refdata.FactOrAssumptionCompleteRow
    ],
):

    data = refdata.RefData.load()
    try:
        res = lookup(data.facts_and_assumptions(), pattern)
        bold(pattern)
        print(res.value, end="")
        if res.unit != "":
            print(f" {res.unit}\t({res.description})")
        else:
            print(f"\t({res.description})")
        print("")
        if res.rationale:
            print(res.rationale)
        if res.reference or res.link:
            bold("reference")
            print(res.reference)
            print(res.link)
        else:
            bold("reference")
            faint("no reference provided")
    except:
        bold(f"No {what} called {pattern} found!", file=sys.stderr)
        exit(1)


def cmd_data_lookup(args: Any):
    pattern: str = args.pattern
    if ags.is_valid(pattern):
        lookup_by_ags(pattern, fix_missing_entries=args.fix_missing_entries)
    elif pattern.startswith("Ass_"):
        lookup_fact_or_ass(
            pattern, "assumption", refdata.FactsAndAssumptions.complete_ass
        )
    elif pattern.startswith("Fact_"):
        lookup_fact_or_ass(pattern, "fact", refdata.FactsAndAssumptions.complete_fact)
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


def cmd_data_entries_user_overrides_generate_defaults(args: Any):
    data = refdata.RefData.load()
    result = []
    good = 0
    errors = 0
    crazy_errors = 0
    with open("errors.txt", "w") as error_file, open(
        "crazy-errors.txt", "w"
    ) as crazy_error_file:

        for (ags, description) in list(data.ags_master().items()):
            try:
                entries = makeentries.make_entries(data, ags, 2035)
                default_values: dict[str, str] = {
                    k: v
                    for (k, v) in asdict(entries).items()
                    if k in makeentries.USER_OVERRIDABLE_ENTRIES
                }
                default_values["city"] = description
                result.append(default_values)  # type: ignore
                good = good + 1
            except refdata.LookupFailure as e:
                errors = errors + 1
                print(ags, repr(e), sep="\t", file=error_file)
            except Exception as e:
                crazy_errors = crazy_errors + 1
                print(ags, repr(e), sep="\t", file=crazy_error_file)

            sys.stdout.write(
                f"\rOK {good:>5}    BAD {errors:>5}  CRAZY {crazy_errors:>5}"
            )
    with open("output.json", "w") as output_file:
        json.dump(result, indent=4, fp=output_file)
