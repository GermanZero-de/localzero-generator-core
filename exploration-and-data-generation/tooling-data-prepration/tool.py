import csv


def uninterested(row: list[str]) -> bool:
    ags = row[0]
    num = row[1]
    if num == "-":
        return True
    if ags.endswith("00000") and ags[2] != "0":
        return True
    if ags[-6:-3] == ags[-3:] and ags[0:2] == "11":
        return True
    if ags == "10042999":  # Deutsch Luxemburgische Freunschaftsgebiet
        return True
    return False


def main():
    with open("destatis_2023_Bevölkerung_2021.csv", encoding="latin1") as f:
        csvdata = csv.reader(f, delimiter=";")
        data = [c for c in csvdata]
    newdata = [[d[0].ljust(8, "0"), d[2]] for d in data[8:-6]]
    newdata = [nd for nd in newdata if uninterested(nd)]

    with open("../../data/public/ags/2021.csv", encoding="utf-8") as f:
        csvdata = csv.reader(f, delimiter=",")
        newmaster = [c for c in csvdata]

    newmasterags = set(d[0] for d in newmaster[1:])
    pop_ags = set(d[0] for d in newdata)

    print("In pop but not in master: ", len(pop_ags - newmasterags))
    for ags in pop_ags - newmasterags:
        if not ags.endswith("00000"):
            print("", ags)
    print("In master but not in pop: ", len(newmasterags - pop_ags))


main()
