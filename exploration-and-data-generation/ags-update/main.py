import sys
import datetime
from loadexcel import load, RawRecord, ChangeKind
from agshistory import (
    Change,
    PartialSpinOff,
    Part,
    AgsOrNameChange,
    Dissolution,
    JsonEncoder,
    show,
)
import agshistory
import traffic
import json


def create_partial_spin_off(
    left_over: RawRecord, parts: list[RawRecord]
) -> PartialSpinOff:
    assert left_over.area_in_sqm is not None
    assert all(p.area_in_sqm is not None for p in parts)
    assert left_over.population is not None
    assert all(p.population is not None for p in parts)
    assert all(p.ags == left_over.ags for p in parts)
    assert all(p.effective_date == left_over.effective_date for p in parts)
    assert left_over.new_ags == left_over.ags
    return PartialSpinOff(
        ags=left_over.ags,
        name=left_over.name,
        effective_date=left_over.effective_date,
        remaining_area=left_over.area_in_sqm,
        remaining_population=left_over.population,
        parts=[
            # the 'or 0' just to make the typechecker happy
            Part(p.new_ags, p.new_name, p.area_in_sqm or 0, p.population or 0)
            for p in parts
        ],
    )


def create_dissolution(parts: list[RawRecord]) -> Dissolution:
    assert all(p.area_in_sqm is not None for p in parts)
    assert all(p.population is not None for p in parts)
    assert all(parts[0].ags == p.ags for p in parts)
    assert all(parts[0].effective_date == p.effective_date for p in parts)
    return Dissolution(
        ags=parts[0].ags,
        name=parts[0].name,
        effective_date=parts[0].effective_date,
        parts=[
            # the 'or 0' just to make the typechecker happy
            Part(p.new_ags, p.new_name, p.area_in_sqm or 0, p.population or 0)
            for p in parts
        ],
    )


def convert_representation(changes: list[RawRecord]) -> list[Change]:
    """Given a list of RawRecords, convert them into the highlevel representation.
    In particular consecutive spin offs are turned into a single record of type
    PartialSpinOff, for easier post processing.
    Similarly a dissolution might actually be done giving the area away to multiple
    communes, so we combine them into a single record of type Dissolution."""
    # See the notes at the docstring of loadexcel.load for the format of the records.
    # And in particular the assumptions on the order of the records
    result: list[Change] = []

    not_yet_combined_partial_spin_offs: list[RawRecord] = []
    not_yet_combined_dissolutions = []

    def combine_dissolutions_if_any():
        if len(not_yet_combined_dissolutions) > 0:
            result.append(create_dissolution(not_yet_combined_dissolutions))
            not_yet_combined_dissolutions.clear()

    for ch in changes:
        match ch.change_kind:
            case ChangeKind.DISSOLUTION:
                assert len(not_yet_combined_partial_spin_offs) == 0
                # If this is a dissolution of a different commune than the
                # previous dissolution, then we need to combine the previous
                # first
                if len(not_yet_combined_dissolutions) > 0 and (
                    not_yet_combined_dissolutions[0].ags != ch.ags
                ):
                    combine_dissolutions_if_any()
                not_yet_combined_dissolutions.append(ch)

            case ChangeKind.CHANGE:
                assert len(not_yet_combined_partial_spin_offs) == 0
                combine_dissolutions_if_any()
                # Sometimes the file seems to contain changes that did NOT
                # change anything.  We are ignoring them.
                if ch.new_ags != ch.ags or ch.new_name != ch.name:
                    result.append(
                        AgsOrNameChange(
                            ags=ch.ags,
                            name=ch.name,
                            effective_date=ch.effective_date,
                            new_ags=ch.new_ags,
                            new_name=ch.new_name,
                        )
                    )
            case ChangeKind.PARTIAL_SPIN_OFF:
                combine_dissolutions_if_any()
                if ch.new_ags != ch.ags:
                    not_yet_combined_partial_spin_offs.append(ch)
                else:
                    result.append(
                        create_partial_spin_off(ch, not_yet_combined_partial_spin_offs)
                    )
                    not_yet_combined_partial_spin_offs = []

    combine_dissolutions_if_any()
    assert len(not_yet_combined_partial_spin_offs) == 0

    return result


def convert():
    raw_records = load()
    changes = convert_representation(raw_records)
    json.dump(changes, sys.stdout, indent=2, cls=JsonEncoder)


def changed_urban_area():
    changes = agshistory.load()
    for ch in changes:
        excluding_commune = ch.ags[:-3]
        if any(excluding_commune != a[:-3] for a in ch.all_new_ags()):
            print(ch)


def main():
    match sys.argv:
        case [_, "convert"]:
            convert()
        case [_, "show", ags]:
            show(False, ags)
        case [_, "show", "-p", ags]:
            show(True, ags)
        case [_, "transplant-traffic", target_date]:
            target_date = datetime.date.fromisoformat(target_date)
            traffic.transplant(target_date)
        case [_, "compare-traffic", file1, file2]:
            traffic.compare(file1, file2)
        case [_, "changed-urban-area"]:
            changed_urban_area()

        case _:
            print(
                """Usage: python agshistory.py CMD...
Where CMD is
    convert                           -- Convert excel to json
    show <ags>                        -- Show history of one AGS from the json
    transplant-traffic <target-date>] -- Transplant traffic data from 2018 to the given date"
    compare-traffic <file1> <file2>   -- Compare two traffic files
    changed-urban-area                -- List all AGS changes that changed urban area
"""
            )
            sys.exit(1)


main()
