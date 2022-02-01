import json
import sys
import os.path
import re
from generatorcore.generator import calculate_with_default_inputs

test_dir = "tests\end_to_end_expected"


def json_to_output_file(json_object, filePath):
    """Write json_object to a file"""
    if filePath is not None:
        with open(filePath, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
        print("Wrote " + filePath)
    else:
        print("No file specified!", file=sys.stderr)


def update_expectation(ags: str, year: int, filePath: str):
    g = calculate_with_default_inputs(ags=ags, year=year)
    json_to_output_file(g.result_dict(), filePath)


def cmd_test_end_to_end_update_expectations(args):
    year = 2035
    regEx_expected_files = "production_((\d+)|(DG000000))\.json"

    for fileName in os.listdir(test_dir):
        if os.path.isfile(os.path.join(test_dir, fileName)):
            if re.match(regEx_expected_files, fileName):
                ags = re.match(regEx_expected_files, fileName).group(1)
                filePath = os.path.join(test_dir, fileName)

                print("\nFound " + filePath)
                update_expectation(ags=ags, year=year, filePath=filePath)


def cmd_test_end_to_end_create_expectation(args):
    year = 2035
    fileName = "production_" + args.ags + ".json"
    filePath = os.path.join(test_dir, fileName)
    update_expectation(args.ags, year, filePath)
