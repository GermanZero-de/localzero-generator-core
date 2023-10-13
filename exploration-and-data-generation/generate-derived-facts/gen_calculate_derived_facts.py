import openpyxl
import sys
import re

PRELUDE = """\"\"\"
This module was auto generated from an annotated version of the 2018 facts file, which
contained explicit formulas for every derived fact. This way we could simplify updating
the facts, without changing a lot of the actual code.
\"\"\"

from . import refdata

def calculate_derived_facts(rd: refdata.RefData):
    f = rd.facts()
"""

FACT_REGEX = re.compile(r"(Fact_[A-Za-z0-9_]+)")


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python gen_calculate_derived_facts.py <path-to-2018_facts_edit_2022.xlsx>"
        )
        sys.exit(1)
    w = openpyxl.load_workbook(sys.argv[1])
    s = w["2018"]
    header = []
    for header_row in s.iter_rows(min_row=1, max_row=1, max_col=11, values_only=True):
        header = header_row
    print(PRELUDE)
    for r in s.iter_rows(min_row=2, max_col=11, max_row=1100, values_only=True):
        data = dict([(h, x) for (h, x) in zip(header, r) if h is not None])
        if (
            data["update 2022"] == "F"
            and data["Formula"] is not None
            and data["Formula"] != "noch nicht existent"
        ):
            label = data["label"]
            formula: str = data["Formula"]  # type: ignore
            formula = FACT_REGEX.sub(r'f.fact("\1")', formula)
            del data["Formula"]
            del data["label"]
            del data["update 2022"]
            del data["value"]
            data = {k: ("" if v is None else v) for k, v in data.items()}
            print(f"""    f.add_derived_fact("{label}", {formula}, {data})""")


main()
