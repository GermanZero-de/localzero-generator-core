import csv
from area import read_new_ags_master
import openpyxl

header = ["ags", "rt7", "rt3"]

rt3_by_rt7 = {
    71: "city",
    72: "city",
    73: "smcty",
    75: "smcty",
    74: "rural",
    76: "rural",
    77: "rural",
}


def read_and_filter_destatis_area_kinds():
    wb = openpyxl.load_workbook("BMDV_2023_RegioStaR-Referenzdateien_2021.xlsx")
    ws = wb["ReferenzGebietsstand2021"]
    for row in ws.iter_rows(min_row=2, max_row=10995, max_col=12, values_only=True):
        ags = row[0]
        rt7 = row[11]
        rt3 = rt3_by_rt7[rt7]
        yield (str(ags).rjust(8, "0"), rt7, rt3)


def main():
    destatis_area_kinds = list(read_and_filter_destatis_area_kinds())
    for ags, rt7, rt3 in destatis_area_kinds[:3]:
        print(ags, rt7, rt3)
    print()
    for ags, rt7, rt3 in destatis_area_kinds[-3:]:
        print(ags, rt7, rt3)
    ags_in_master = read_new_ags_master()
    with open("../../data/public/area_kinds/2021.csv", "w", encoding="utf-8") as f:
        csvdata = csv.writer(f, delimiter=",")
        csvdata.writerow(header)
        for ags, rt7, rt3 in destatis_area_kinds:
            if ags in ags_in_master:
                csvdata.writerow([ags, rt7, rt3])


if __name__ == "__main__":
    main()
