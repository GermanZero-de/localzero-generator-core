# pyright: strict

import json
import os
import os.path
import re
import sys
from dataclasses import asdict
from typing import Any, Iterator

from climatevision.generator import RefData, calculate_with_default_inputs, make_entries

test_dir = os.path.join("tests", "end_to_end_expected")


def json_to_output_file(json_object: object, file_path: str):
    """Write json_object to a file"""
    if file_path != "":
        with open(file_path, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
        print("Wrote " + file_path)
    else:
        print("No file specified!", file=sys.stderr)


def update_expectation(
    year_ref: int, ags: str, year_baseline: int, year_target: int, file_path: str
):
    g = calculate_with_default_inputs(
        year_ref=year_ref, ags=ags, year_baseline=year_baseline, year_target=year_target
    )
    json_to_output_file(g.result_dict(), file_path)


def update_entries(
    year_ref: int, ags: str, year_baseline: int, year_target: int, file_path: str
):
    rd = RefData.load(year_ref=year_ref)
    entries = make_entries(
        data=rd, ags=ags, year_baseline=year_baseline, year_target=year_target
    )
    json_to_output_file(asdict(entries), file_path)


def expectation_files(
    year_baseline: int, year_ref: int, pattern: str
) -> Iterator[tuple[str, str, int, int]]:
    dir = os.path.join(test_dir, f"{year_ref}")
    for filename in os.listdir(dir):
        m = re.match(pattern, filename)
        if m is not None:
            ags = m.group(1)
            year_baseline = int(m.group(4))
            year_target = int(m.group(5))
            file_path = os.path.join(dir, filename)
            yield (file_path, ags, year_baseline, year_target)


def cmd_test_end_to_end_update_expectations(args: Any):
    expect_entries_pattern = r"entries_((\d+)|(DG000000))_(20\d\d)_(20\d\d)\.json"
    expect_file_pattern = r"production_((\d+)|(DG000000))_(20\d\d)_(20\d\d)\.json"

    year_baseline = 2025

    for year_ref in [2018, 2021]:
        for file_path, ags, year_baseline, year_target in expectation_files(
            year_baseline, year_ref, expect_entries_pattern
        ):
            update_entries(
                year_ref=year_ref,
                ags=ags,
                year_baseline=year_baseline,
                year_target=year_target,
                file_path=file_path,
            )

        for file_path, ags, year_baseline, year_target in expectation_files(
            year_baseline, year_ref, expect_file_pattern
        ):
            update_expectation(
                year_ref=year_ref,
                ags=ags,
                year_baseline=year_baseline,
                year_target=year_target,
                file_path=file_path,
            )


def cmd_test_end_to_end_create_expectation(args: Any):
    filename = (
        "production_"
        + args.ags
        + "_"
        + str(args.year_baseline)
        + "_"
        + str(args.year_target)
        + ".json"
    )
    for year_ref in [2018, 2021]:
        filepath = os.path.join(test_dir, f"{year_ref}", filename)
        update_expectation(
            year_ref=year_ref,
            ags=args.ags,
            year_baseline=args.year_baseline,
            year_target=args.year_target,
            file_path=filepath,
        )


def cmd_test_end_to_end_run_all_ags(args: Any):
    data = RefData.load(args.year_ref)
    good = 0
    errors = 0
    with open("test_errors.txt", "w") as error_file:
        for ags in list(data.ags_master().keys()):
            try:
                calculate_with_default_inputs(
                    year_ref=args.year_ref,
                    ags=ags,
                    year_baseline=args.year_baseline,
                    year_target=args.year_target,
                )
                good = good + 1
            except Exception as e:
                errors = errors + 1
                print(ags, repr(e), sep="\t", file=error_file)
                sys.stdout.write(ags + ": " + repr(e) + "\n")

            sys.stdout.write(f"OK {good:>5}    ERROR {errors:>5}\n\n")
