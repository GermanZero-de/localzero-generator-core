#!/usr/bin/env python

"""Run make and run for the AGSs in ags_list.txt and export selected values."""

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from functools import partial
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


def process_ags(
    item: tuple[int, dict[str, Any]],
    *,
    temp_path: Path,
    usage: dict[str, Any],
    descriptions: dict[str, tuple[str, str]],
) -> tuple[str, str, list[list[Any]]]:
    row_number, ags_row = item
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

    rows = []
    for variable in usage["entries"]:
        unit, description = descriptions.get(variable, ("", ""))
        rows.append(
            [
                ags,
                year_target,
                variable,
                unit,
                description,
                entries.get(variable, ""),
            ]
        )
    for variable in usage["generator"]:
        unit, description = descriptions.get(variable, ("", ""))
        rows.append(
            [
                ags,
                year_target,
                variable,
                unit,
                description,
                value_at_path(result, variable),
            ]
        )

    return ags, year_target, rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=RESULT_DIR,
        help="directory for per-AGS CSV files (default: regression/results)",
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
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="number of AGSs to process in parallel (default: 4)",
    )
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be at least 1")

    with args.usage_list.open(encoding="utf-8") as usage_file:
        usage = json.load(usage_file)

    with (REGRESSION_DIR / "description.csv").open(
        newline="", encoding="utf-8"
    ) as description_file:
        descriptions = {
            row["variable"]: (row["unit"], row["description"])
            for row in csv.DictReader(description_file, delimiter=";")
        }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with args.ags_list.open(newline="", encoding="utf-8") as ags_file:
        ags_rows = list(csv.DictReader(ags_file, skipinitialspace=True))

    header = ["ags", "year_target", "variable", "unit", "description", "value"]
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        process = partial(
            process_ags,
            temp_path=temp_path,
            usage=usage,
            descriptions=descriptions,
        )
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            for ags, year_target, rows in executor.map(
                process, enumerate(ags_rows, start=2)
            ):
                ags_output = args.output_dir / f"{ags}_{year_target}.csv"
                with ags_output.open("w", newline="", encoding="utf-8") as ags_file:
                    ags_writer = csv.writer(ags_file)
                    ags_writer.writerow(header)
                    ags_writer.writerows(rows)


if __name__ == "__main__":
    main()