import json
import sys
import os
import os.path
import re
from generatorcore.generator import calculate_with_default_inputs

test_dir = os.path.join("tests", "end_to_end_expected")


def json_to_output_file(json_object, file_path):
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


def cmd_test_end_to_end_update_expectations(args):
    year = 2035
    expect_file_pattern = r"production_((\d+)|(DG000000))\.json"

    for filename in os.listdir(test_dir):
        m = re.match(expect_file_pattern, filename)
        if m is not None:
            ags = m.group(1)
            file_path = os.path.join(test_dir, filename)
            update_expectation(ags=ags, year=year, file_path=file_path)


def cmd_test_end_to_end_create_expectation(args):
    year = 2035
    filename = "production_" + args.ags + ".json"
    filepath = os.path.join(test_dir, filename)
    update_expectation(args.ags, year, filepath)
