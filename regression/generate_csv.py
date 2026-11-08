#!/usr/bin/env python

"""Run make and run for the AGSs in ags_list.txt and export selected values."""

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGRESSION_DIR = Path(__file__).resolve().parent
RESULT_DIR = REGRESSION_DIR / "results"

def value_at_path(data: dict[str, Any], path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        value = value[part]
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REGRESSION_DIR / "results.csv",
        help="CSV output path (default: regression/results.csv)",
    )
    parser.add_argument(
        "--ags-list",
        type=Path,
        default=REGRESSION_DIR / "ags_list.txt",
        help="CSV input with ags and year_target columns",
    )
    parser.add_argument(
        "--usage-list",
        type=Path,
        default=REGRESSION_DIR / "usage.txt",
        help="JSON file listing selected entries and generator variables",
    )
    args = parser.parse_args()

    with args.usage_list.open(encoding="utf-8") as usage_file:
        usage = json.load(usage_file)

    with (REGRESSION_DIR / "description.csv").open(
        newline="", encoding="utf-8"
    ) as description_file:
        descriptions = {
            row["variable"]: (row["unit"], row["description"])
            for row in csv.DictReader(description_file, delimiter=";")
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.ags_list.open(newline="", encoding="utf-8") as ags_file:
        ags_rows = list(csv.DictReader(ags_file, skipinitialspace=True))

    with args.output.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        header = ["ags", "year_target", "variable", "unit", "description", "value"]
        writer.writerow(header)

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            for row_number, ags_row in enumerate(ags_rows, start=2):
                ags = ags_row["ags"].strip()
                year_target = ags_row["year_target"].strip()
                make_output = temp_path / f"entries_{row_number}.json"
                run_output = temp_path / f"result_{row_number}.json"

                common_args = ["-ags", ags, "-year_target", year_target]
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "devtool.py"),
                        "make",
                        *common_args,
                        "-o",
                        str(make_output),
                    ],
                    cwd=ROOT,
                    check=True,
                )
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "devtool.py"),
                        "run",
                        *common_args,
                        "-o",
                        str(run_output),
                    ],
                    cwd=ROOT,
                    check=True,
                )

                with make_output.open(encoding="utf-8") as entries_file:
                    entries = json.load(entries_file)
                with run_output.open(encoding="utf-8") as result_file:
                    result = json.load(result_file)

                ags_output = args.output.parent / f"{ags}_{year_target}.csv"
                with ags_output.open("w", newline="", encoding="utf-8") as ags_file:
                    ags_writer = csv.writer(ags_file)
                    ags_writer.writerow(header)

                    for variable in usage["entries"]:
                        unit, description = descriptions.get(variable, ("", ""))
                        row = [
                            ags,
                            year_target,
                            variable,
                            unit,
                            description,
                            entries.get(variable, ""),
                        ]
                        writer.writerow(row)
                        ags_writer.writerow(row)
                    for variable in usage["generator"]:
                        unit, description = descriptions.get(variable, ("", ""))
                        row = [
                            ags,
                            year_target,
                            variable,
                            unit,
                            description,
                            value_at_path(result, variable),
                        ]
                        writer.writerow(row)
                        ags_writer.writerow(row)


if __name__ == "__main__":
    main()