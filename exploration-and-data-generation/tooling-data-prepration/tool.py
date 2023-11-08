import csv


def interested(row: list[str]) -> bool:
    ags = row[0]
    num = row[1]
    if num == "-":
        return False
    # Allgemeine Regierungsbezirke (aggregation von landkreisen -- modellen wir nicht)
    if ags.endswith("00000") and ags[2] != "0":
        return False
    # Berliner Bezirke (untereinheiten von Berlin -- modellen wir nicht)
    if ags != "11000000" and ags[-6:-3] == ags[-3:] and ags[0:2] == "11":
        return False
    if ags == "10042999":  # Deutsch Luxemburgische Hoheitsgebiet.
        return False
    return True


def read_and_filter_destatis():
    with open("destatis_2023_Bevölkerung_2021.csv", encoding="latin1") as f:
        csvdata = csv.reader(f, delimiter=";")
        data = [c for c in csvdata]
    newdata = [[d[0].ljust(8, "0"), d[2]] for d in data[8:-6]]
    newdata = [nd for nd in newdata if interested(nd)]
    return newdata


def read_new_ags_master() -> set[str]:
    with open("../../data/public/ags/2021.csv", encoding="utf-8") as f:
        csvdata = csv.reader(f, delimiter=",")
        newmaster = [c for c in csvdata]

    return set(d[0] for d in newmaster[1:])


def compare_with_master(destatis):
    newmasterags = read_new_ags_master()

    pop_ags = set(d[0] for d in destatis)

    print("In pop but not in master: ", len(pop_ags - newmasterags))
    for ags in pop_ags - newmasterags:
        print("", ags)
    print("In master but not in pop: ", len(newmasterags - pop_ags))
    for ags in newmasterags - pop_ags:
        print("", ags)


def main():
    destatis = read_and_filter_destatis()
    compare_with_master(destatis)

    # Unsorted but afterwards we ran normalize from devtool data on it
    with open("../../data/public/population/2021.csv", "w", encoding="utf-8") as f:
        csvdata = csv.writer(f, delimiter=",")
        csvdata.writerow(["ags", "total"])
        csvdata.writerows(destatis)


main()
