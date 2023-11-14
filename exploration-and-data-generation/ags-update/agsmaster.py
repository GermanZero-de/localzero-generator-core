# Code to update the ags master list (taking 2018 ags master list and apply ags history
# to get a reasonable 2021 ags master list).
import typing
import datetime
import csv
import agshistory
import sys
from agshistory import PartialSpinOff, AgsOrNameChange, Dissolution


def read(filename: str) -> typing.Tuple[list[str], dict[str, str]]:
    """Read the traffic data.  Returns a tuple of the header and a dict
    mapping the AGS (first column of the file) to the remaining data.
    """
    with open(filename, encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=",")
        header = next(csv_reader)
        result = {}
        for row in csv_reader:
            ags = row[0]
            result[ags] = row[1]
        return header, result


def write(date: datetime.date, header: list[str], data: dict[str, str]):
    with open(
        f"../../data/public/ags/{date.isoformat()}.csv", "w", encoding="utf-8"
    ) as f:
        csv_writer = csv.writer(f, delimiter=",", lineterminator="\n")
        csv_writer.writerow(header)
        for ags, desc in sorted(data.items(), key=lambda x: x[0]):
            csv_writer.writerow([ags, desc])


def compare(file1: str, file2: str):
    """Compare two traffic files."""
    (header1, data1) = read(file1)
    (header2, data2) = read(file2)
    assert header1 == header2
    equals = 0
    only_in_1 = []
    only_in_2 = []
    unequal = []
    all_ags = sorted(list(set(data1.keys()) | set(data2.keys())))
    for ags in all_ags:
        if ags not in data1:
            only_in_2.append(ags)
        elif ags not in data2:
            only_in_1.append(ags)
        else:
            if data1[ags] == data2[ags]:
                equals += 1
            else:
                unequal.append(ags)

    print("SUMMARY")
    print(
        "only in 1:",
        len(only_in_1),
        "only in 2:",
        len(only_in_2),
        "equals:",
        equals,
        "unequal:",
        len(unequal),
    )
    print()

    print("ONLY IN 1")
    for a in only_in_1:
        print(a)
    print()

    print("ONLY IN 2")
    for a in only_in_2:
        print(a, data2[a])
    print()

    print("UNEQUAL")
    for a in unequal:
        print(a)
        print(data1[a])
        print(data2[a])
    print()


def transplant(target_date: datetime.date):
    changes = agshistory.load()
    master_header, master_data = read("../../data/public/ags/master.csv")

    def maybe_create(label: str, change: PartialSpinOff | Dissolution) -> bool:
        if change.ags not in master_data:
            print(
                f"WARNING (during  {label}): {change.ags} ({change.name}) not found.",
                file=sys.stderr,
            )
            return False
        for p in change.parts:
            if p.ags not in master_data:
                master_data[p.ags] = p.name
        return True

    for ch in changes:
        if ch.effective_date < agshistory.FIRST_DATE_OF_INTEREST:
            continue
        if ch.effective_date > target_date:
            break
        match ch:
            case PartialSpinOff():
                maybe_create("spin off", ch)
            case Dissolution(ags=ags):
                if maybe_create("dissolution", ch):
                    del master_data[ags]
            case AgsOrNameChange(
                ags=ags, new_ags=new_ags, name=name, new_name=new_name
            ):
                if ags not in master_data:
                    print(
                        f"WARNING (during change): {ags} ({name}) not found.",
                        file=sys.stderr,
                    )
                    continue
                data = master_data[ags]
                del master_data[ags]
                assert new_ags not in master_data
                master_data[new_ags] = new_name
            case _:
                continue
    write(target_date, master_header, master_data)
