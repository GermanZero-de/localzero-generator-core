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
    parts = [Part(p.new_ags, p.new_name, p.area_in_sqm, p.population) for p in parts]
    return PartialSpinOff(
        ags=left_over.ags,
        name=left_over.name,
        effective_date=left_over.effective_date,
        remaining_area=left_over.area_in_sqm,
        remaining_population=left_over.population,
        parts=parts,
    )


def convert_representation(changes: list[RawRecord]) -> list[Change]:
    """Given a list of RawRecords, convert them into the highlevel representation.
    In particular consecutive spin offs are turned into a single record of type
    PartialSpinOff, for easier post processing."""
    # See the notes at the docstring of loadexcel.load for the format of the records.
    # And in particular the assumptions on the order of the records
    result: list[Change] = []
    not_yet_combined_partial_spin_offs: list[RawRecord] = []
    for ch in changes:
        match ch.change_kind:
            case ChangeKind.DISSOLUTION:
                assert len(not_yet_combined_partial_spin_offs) == 0
                result.append(
                    Dissolution(
                        ags=ch.ags,
                        name=ch.name,
                        effective_date=ch.effective_date,
                        new_ags=ch.new_ags,
                        new_name=ch.new_name,
                    )
                )
            case ChangeKind.CHANGE:
                assert len(not_yet_combined_partial_spin_offs) == 0
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
                if ch.new_ags != ch.ags:
                    not_yet_combined_partial_spin_offs.append(ch)
                else:
                    result.append(
                        create_partial_spin_off(ch, not_yet_combined_partial_spin_offs)
                    )
                    not_yet_combined_partial_spin_offs = []

    assert len(not_yet_combined_partial_spin_offs) == 0

    return result


def convert():
    raw_records = load()
    changes = convert_representation(raw_records)
    json.dump(changes, sys.stdout, indent=2, cls=JsonEncoder)


def main():
    match sys.argv:
        case [_, "convert"]:
            convert()
        case [_, "show", ags]:
            show(ags)
        case [_, "transplant-traffic", target_date]:
            target_date = datetime.date.fromisoformat(target_date)
            traffic.transplant(target_date)

        case _:
            print(
                "Usage: python agshistory.py [convert|show <ags>|transplant-traffic <target-date>]"
            )
            sys.exit(1)


main()
