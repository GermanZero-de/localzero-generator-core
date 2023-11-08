import csv

#      1	ags
#      2	land_total
#      3	land_settlement
#      4	land_traffic
#      5	veg_agri
#      6	veg_forrest
#      7	veg_wood
#      8	veg_heath
#      9	veg_moor
#     10	veg_marsh
#     11	veg_plant_uncover_com
#     12	water_total


def read_and_filter_destatis_settlement():
    with open("destatis_2023_Siedlungsflächen_2021.csv", encoding="latin1") as f:
        csvdata = csv.reader(f, delimiter=";")
        dataonly = list(csvdata)[9:-4]
        ags_to_settlement_ghd = {d[1].ljust(8, "0"): d[7] for d in dataonly}
        return ags_to_settlement_ghd


def read_and_filter_destatis_area():
    with open("destatis_2023_Bodenflächen_2021.csv", encoding="latin1") as f:
        csvdata = csv.reader(f, delimiter=";")
        dataonly = list(csvdata)[10:-4]
        interesting_columns = [
            [d[1].ljust(8, "0")] + d[3:6] + d[7:15] for d in dataonly
        ]
        excluding_rows_with_no_total_area = [
            d for d in interesting_columns if d[1] != "-"
        ]
        replace_minus_with_zero = [
            ["0" if c == "-" else c for c in r]
            for r in excluding_rows_with_no_total_area
        ]

        return replace_minus_with_zero


def read_new_ags_master() -> set[str]:
    with open("../../data/public/ags/2021.csv", encoding="utf-8") as f:
        csvdata = csv.reader(f, delimiter=",")
        newmaster = [c for c in csvdata]

    return set(d[0] for d in newmaster[1:])


def compare_with_master(destatis):
    newmasterags = read_new_ags_master()

    ags_in_destatis = set(d[0] for d in destatis)

    print("In destatis but not in master: ", len(ags_in_destatis - newmasterags))
    for ags in sorted(list(ags_in_destatis - newmasterags)):
        print("", ags)
    print("In master but not in destatis: ", len(newmasterags - ags_in_destatis))
    for ags in newmasterags - ags_in_destatis:
        print("", ags)


def main():
    ags_to_settlement_ghd = read_and_filter_destatis_settlement()
    destatis_area = read_and_filter_destatis_area()
    print(len(destatis_area))
    compare_with_master(destatis_area)

    for rows in destatis_area:
        ags = rows[0]
        if ags not in ags_to_settlement_ghd:
            assert False, f"Missing ags {ags}"


main()
