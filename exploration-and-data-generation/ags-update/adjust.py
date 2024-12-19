from enum import Enum
import sys
import typing
import csv
import agshistory
from agshistory import AgsOrNameChange, Dissolution, PartialSpinOff
import datetime
from typing import Literal


STR_COLS = 0


def read_data(
    filename: str, *, remove_empty_rows: bool
) -> typing.Tuple[list[str], dict[str, tuple[list[str], list[float]]]]:
    """Read the original data.  Returns a tuple of the header and a dict
    mapping the AGS (first column of the file) to the remaining data.
    """
    with open(filename, encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=",")
        header = next(csv_reader)
        result = {}
        for row in csv_reader:
            ags = row[0]
            str_data = row[1 : STR_COLS + 1]
            data = row[STR_COLS + 1 :]
            if remove_empty_rows and all((x == "" for x in data)):
                continue
            data = [float(x) if x != "" else 0.0 for x in data]
            result[ags] = (str_data, data)
        return header, result


def write_data(
    filename: str, header: list[str], data: dict[str, tuple[list[str], list[float]]]
):
    with open(filename, "w", encoding="utf-8") as f:
        csv_writer = csv.writer(f, delimiter=",", lineterminator="\n")
        csv_writer.writerow(header)
        for ags, row in data.items():
            csv_writer.writerow([ags] + row[0] + row[1])


FIRST_DATE_OF_INTEREST = datetime.date(2019, 1, 1)


def distribute_by_area(
    label: str,
    original_data: dict[str, tuple[list[str], list[float]]],
    change: PartialSpinOff | Dissolution,
) -> bool:
    """Distribute data from the ags of the change to the ags's mentioned in parts of the change,
    proportional to the area of the parts.

    NOTE: A good argument can be made that there are cases where proportional to the
    population is sometimes "more right".

    Return's false if the ags of the change is not in the traffic data.
    """
    if change.ags not in original_data:
        print(
            f"WARNING (during  {label}): {change.ags} ({change.name}) not found.",
        )
        return False
    if len(change.parts) > 1:
        print("MANY", change)
    (source_str, source) = original_data[change.ags]
    for part, ratio in change.parts_with_ratios_by_area():
        if part.ags in original_data:
            original_data[part.ags] = (
                source_str,
                [s * ratio + o for s, o in zip(source, original_data[part.ags][1])],
            )
        else:
            original_data[part.ags] = ([""] * STR_COLS, [s * ratio for s in source])

    return True


class Mode(Enum):
    BY_AREA = 1
    IGNORE_SPIN_OFFS = 2


def transplant(
    mode: Mode,
    source_filename: str,
    target_filename: str,
    last_date: datetime.date,
    remove_empty_rows: bool,
):
    changes = agshistory.load()
    traffic_header, original_data = read_data(
        source_filename, remove_empty_rows=remove_empty_rows
    )
    for ch in changes:
        if ch.effective_date < FIRST_DATE_OF_INTEREST:
            continue
        if ch.effective_date > last_date:
            break
        match ch:
            case PartialSpinOff(ags=ags):
                if mode != Mode.IGNORE_SPIN_OFFS:
                    if distribute_by_area("spin off", original_data, ch):
                        ratio = (
                            1 - ch.total_area_of_parts_in_sqm() / ch.total_area_in_sqm()
                        )
                        assert False
                        # This is dead code we no longer run with mode != IGNORE_SPIN_OFFS
                        # original_data[ags] = [o * ratio for o in original_data[ags]]
                else:
                    print("ignoring", ch)
            case Dissolution(ags=ags):
                if len(ch.parts) > 1:
                    print("ignoring dissolution into multiple parts", ch)
                    if ags in original_data:
                        del original_data[ags]
                    continue
                if distribute_by_area("dissolution", original_data, ch):
                    del original_data[ags]
            case AgsOrNameChange(
                ags=ags, new_ags=new_ags, name=name, new_name=new_name
            ):
                if ags not in original_data:
                    print(
                        f"WARNING (during change to {new_ags} ({new_name})): {ags} ({name}) not found.",
                        file=sys.stderr,
                    )
                    continue
                data = original_data[ags]
                del original_data[ags]
                assert new_ags not in original_data
                original_data[new_ags] = data
            case _:
                continue
    write_data(target_filename, traffic_header, original_data)


def compare(file1: str, file2: str, *, remove_empty_rows: bool):
    """Compare two traffic files."""
    (header1, data1) = read_data(file1, remove_empty_rows=remove_empty_rows)
    (header2, data2) = read_data(file2, remove_empty_rows=remove_empty_rows)
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
