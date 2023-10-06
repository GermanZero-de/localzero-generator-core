import openpyxl
import sys


PRELUDE = """from . import refdata
def calculate_derived_facts(rd: refdata.RefData):
    f = rd.facts()
"""


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
            formula = data["Formula"]
            del data["Formula"]
            del data["label"]
            del data["update 2022"]
            del data["value"]
            print(f"""    f.add_derived_fact({label}, {formula}, {data})""")


main()
