# pyright: strict
import dataclasses
from typing import Any
import json
import sys
import os
import os.path
import re
from generatorcore.generator import calculate_with_default_inputs
from generatorcore import refdata
from generatorcore.makeentries import make_entries
from typing import Iterator

test_dir = os.path.join("tests", "end_to_end_expected")


def json_to_output_file(json_object: Any, file_path: str):
    """Write json_object to a file"""
    if file_path is not None:
        with open(file_path, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
        print("Wrote " + file_path)
    else:
        print("No file specified!", file=sys.stderr)


def update_expectation(ags: str, year: int, file_path: str):
    g = calculate_with_default_inputs(ags=ags, year=year)
    json_to_output_file(g.result_dict(), file_path)


def update_entries(ags: str, year: int, file_path: str):
    rd = refdata.RefData.load()
    entries = make_entries(rd, ags=ags, year=year)
    json_to_output_file(dataclasses.asdict(entries), file_path)


def expectation_files(pattern: str) -> Iterator[tuple[str, str, int]]:
    for filename in os.listdir(test_dir):
        m = re.match(pattern, filename)
        if m is not None:
            ags = m.group(1)
            year = int(m.group(4))
            file_path = os.path.join(test_dir, filename)
            yield (file_path, ags, year)


def cmd_test_end_to_end_update_expectations(args: Any):
    expect_entries_pattern = r"entries_((\d+)|(DG000000))_(20\d\d)\.json"
    expect_file_pattern = r"production_((\d+)|(DG000000))_(20\d\d)\.json"

    for (file_path, ags, year) in expectation_files(expect_entries_pattern):
        update_entries(ags=ags, year=year, file_path=file_path)

    for (file_path, ags, year) in expectation_files(expect_file_pattern):
        update_expectation(ags=ags, year=year, file_path=file_path)


def cmd_test_end_to_end_create_expectation(args: Any):
    filename = "production_" + args.ags + "_" + str(args.year) + ".json"
    filepath = os.path.join(test_dir, filename)
    update_expectation(args.ags, int(args.year), filepath)


def cmd_test_end_to_end_run_all_ags(args: Any):
    data = refdata.RefData.load()
    good = 0
    errors = 0
    with open("test_errors.txt", "w") as error_file:
        for ags in list(data.ags_master().keys()):
            try:
                calculate_with_default_inputs(ags=ags, year=int(args.year))
                good = good + 1
            except Exception as e:
                errors = errors + 1
                print(ags, repr(e), sep="\t", file=error_file)
                sys.stdout.write(ags + ": " + repr(e) + "\n")

            sys.stdout.write(f"OK {good:>5}    ERROR {errors:>5}\n\n")
