# pyright: strict
import openpyxl
import sys
import re
import typing
import datetime

PRELUDE = """\"\"\"
This module was auto generated from an annotated version of the 2018 facts file, which
contained explicit formulas for every derived fact. This way we could simplify updating
the facts, without changing a lot of the actual code.
\"\"\"

from . import refdata

def calculate_derived_facts(rd: refdata.RefData):
    f = rd.facts()
"""
ROWS: typing.TypeAlias = list[dict[str, str | float | datetime.datetime | None]]

FACT_REGEX = re.compile(r"(Fact_[A-Za-z0-9_]+)")

"""Renames old name -> new name"""
RENAMES: typing.TypeAlias = dict[str, str]

haukes_typos = {"Fact_F_P_opetpro_prodvol_2018": "Fact_H_P_opetpro_prodvol_2018"}


def replace_fact_name_by_fact_lookup(fact_name: str, renames: RENAMES) -> str:
    if fact_name in haukes_typos:
        fact_name = haukes_typos[fact_name]

    return f'f.fact("{fact_name}")'


def rows_with_header(w: openpyxl.Workbook) -> ROWS:
    header: tuple[str | float | datetime.datetime | None] | None = None
    sheet = w["2018"]
    for header_row in sheet.iter_rows(
        min_row=1, max_row=1, max_col=11, values_only=True
    ):
        header = header_row  # type: ignore
    if header is None:
        raise Exception("Could not find header row")
    rows: ROWS = []
    for r in sheet.iter_rows(min_row=2, max_col=11, max_row=2000, values_only=True):
        rows.append(
            dict(
                [
                    (h, x)
                    for (h, x) in zip(header, r)
                    if h is not None and type(h) is str
                ]
            )
        )
    return rows


def gather_renames(rows: ROWS) -> RENAMES:
    renames: RENAMES = {}
    for row in rows:
        note = row["note HS"]
        if type(note) is not str:
            continue
        if row["update 2022"] not in ["F", "x"]:
            continue
        old_name = row["label"]
        if type(old_name) is not str:
            continue
        if not note.startswith("umbenennen zu "):
            continue
        new_name = note[len("umbenennen zu ") :]
        if new_name == "I_S":
            new_name = old_name.replace("_I_P_", "_I_S_")
        elif new_name == "cb statt eb":
            new_name = old_name.replace("_eb_", "_cb_")
        elif " " in new_name:
            assert (
                False
            ), "{new_name} is not a valid fact name, maybe unknown Hauke replacement strategy?"
        elif len(new_name) <= 8:
            assert (
                False
            ), "{new_name} is suspiciously short, maybe unknown Hauke replacement strategy?"
        assert old_name not in renames
        renames[old_name] = new_name

    return renames


def main():
    renames = {}
    if len(sys.argv) != 2:
        print(
            "Usage: python gen_calculate_derived_facts.py <path-to-2018_facts_edit_2022.xlsx>"
        )
        sys.exit(1)
    w = openpyxl.load_workbook(sys.argv[1])
    rows = rows_with_header(w)
    renames = gather_renames(rows)
    print(f"Found {len(renames)} renames", file=sys.stderr)
    for old_name, new_name in renames.items():
        print(f"    {old_name} -> {new_name}", file=sys.stderr)
    print(file=sys.stderr)

    print(PRELUDE)
    for data in rows:
        if (
            data["update 2022"] == "F"
            and data["Formula"] is not None
            and data["Formula"] != "noch nicht existent"
        ):
            label = data["label"]
            formula: str = data["Formula"]  # type: ignore
            formula = FACT_REGEX.sub(
                lambda m: replace_fact_name_by_fact_lookup(m.group(1), renames), formula
            )
            del data["Formula"]
            del data["label"]
            del data["update 2022"]
            del data["value"]
            data = {k: ("" if v is None else v) for k, v in data.items()}
            print(f"""    f.add_derived_fact("{label}", {formula}, {data})""")


main()
