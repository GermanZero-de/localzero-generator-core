import sys
import typing
import csv
import agshistory
from agshistory import AgsOrNameChange, Dissolution, PartialSpinOff
import datetime


def read_traffic() -> typing.Tuple[list[str], dict[str, list[float]]]:
    """Read the traffic data.  Returns a tuple of the header and a dict
    mapping the AGS (first column of the file) to the remaining data.
    """
    with open("../../data/proprietary/traffic/2018.csv", encoding="utf-8") as f:
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


def transplant(last_date: datetime.date):
    changes = agshistory.load()
    traffic_header, traffic_data = read_traffic()
    for ch in changes:
        if ch.effective_date < FIRST_DATE_OF_INTEREST:
            continue
        if ch.effective_date > last_date:
            break
        match ch:
            case PartialSpinOff(ags=ags, name=name, parts=parts):
                if ags not in traffic_data:
                    print(
                        f"WARNING (during spin off): {ags} ({name}) not found.",
                        file=sys.stderr,
                    )
                    continue
                old = traffic_data[ags]
                for p in parts:
                    if p.ags in traffic_data:
                        traffic_data[p.ags] = [
                            x + y for x, y in zip(traffic_data[p.ags], p.data)
                        ]
                    else:
                        traffic_data[p.ags] = p.data
                if ags in traffic_data:
                    traffic_data[ags] = [x - y for x, y in zip(traffic_data[ags], old)]
                # todo adjust old numbers of old
            case Dissolution(ags=ags, name=name, new_ags=new_ags, new_name=new_name):
                # Dissolution is relatively simple, all old traffic moves
                # to the new ags.
                if ags not in traffic_data:
                    print(
                        f"WARNING (during dissolution): {ags} ({name}) not found.",
                        file=sys.stderr,
                    )
                    continue
                old = traffic_data[ags]
                del traffic_data[ags]
                if new_ags in traffic_data:
                    traffic_data[new_ags] = [
                        x + y for x, y in zip(traffic_data[new_ags], old)
                    ]
                else:
                    traffic_data[new_ags] = old
            case AgsOrNameChange(
                ags=ags, new_ags=new_ags, name=name, new_name=new_name
            ):
                data = traffic_data[ags]
                del traffic_data[ags]
                assert new_ags not in traffic_data
                traffic_data[new_ags] = data
            case _:
                continue
    write_traffic(last_date, traffic_header, traffic_data)
