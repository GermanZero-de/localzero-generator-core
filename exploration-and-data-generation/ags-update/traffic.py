import sys
import typing
import csv
import agshistory
from agshistory import AgsOrNameChange, Dissolution, PartialSpinOff
import datetime


def read_traffic(filename: str) -> typing.Tuple[list[str], dict[str, list[float]]]:
    """Read the traffic data.  Returns a tuple of the header and a dict
    mapping the AGS (first column of the file) to the remaining data.
    """
    with open(filename, encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=",")
        header = next(csv_reader)
        result = {}
        for row in csv_reader:
            ags = row[0]
            data = [float(x) for x in row[1:]]
            result[ags] = data
        return header, result


def write_traffic(date: datetime.date, header: list[str], data: dict[str, list[float]]):
    with open(
        f"../../data/proprietary/traffic/{date.isoformat()}.csv", "w", encoding="utf-8"
    ) as f:
        csv_writer = csv.writer(f, delimiter=",", lineterminator="\n")
        csv_writer.writerow(header)
        for ags, row in data.items():
            csv_writer.writerow([ags] + row)


FIRST_DATE_OF_INTEREST = datetime.date(2019, 1, 1)


def distribute_traffic_by_parts(
    label: str,
    traffic_data: dict[str, list[float]],
    change: PartialSpinOff | Dissolution,
) -> bool:
    """Distribute traffic from the ags of the change to the ags's mentioned in parts of the change,
    proportional to the area of the parts.

    NOTE: A good argument can be made that there are cases where proportional to the
    population is sometimes "more right".  And potentially we should invest more
    time here, but this seems like a reasonable first attempt.

    Return's false if the ags of the change is not in the traffic data.
    """
    if change.ags not in traffic_data:
        print(
            f"WARNING (during  {label}): {change.ags} ({change.name}) not found.",
            file=sys.stderr,
        )
        return False
    source = traffic_data[change.ags]
    for part, ratio in change.parts_with_ratios_by_area():
        if part.ags in traffic_data:
            traffic_data[part.ags] = [
                s * ratio + o for s, o in zip(source, traffic_data[part.ags])
            ]
        else:
            traffic_data[part.ags] = [s * ratio for s in source]

    return True


def transplant(last_date: datetime.date):
    changes = agshistory.load()
    traffic_header, traffic_data = read_traffic(
        "../../data/proprietary/traffic/2018.csv"
    )
    for ch in changes:
        if ch.effective_date < FIRST_DATE_OF_INTEREST:
            continue
        if ch.effective_date > last_date:
            break
        match ch:
            case PartialSpinOff():
                distribute_traffic_by_parts("spin off", traffic_data, ch)
            case Dissolution(ags=ags):
                if distribute_traffic_by_parts("dissolution", traffic_data, ch):
                    del traffic_data[ags]
            case AgsOrNameChange(
                ags=ags, new_ags=new_ags, name=name, new_name=new_name
            ):
                if ags not in traffic_data:
                    print(
                        f"WARNING (during change to {new_ags} ({new_name})): {ags} ({name}) not found.",
                        file=sys.stderr,
                    )
                    continue
                data = traffic_data[ags]
                del traffic_data[ags]
                assert new_ags not in traffic_data
                traffic_data[new_ags] = data
            case _:
                continue
    write_traffic(last_date, traffic_header, traffic_data)


def compare(file1: str, file2: str):
    """Compare two traffic files."""
    (header1, data1) = read_traffic(file1)
    (header2, data2) = read_traffic(file2)
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
