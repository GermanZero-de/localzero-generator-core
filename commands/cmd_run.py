# pyright: strict

from dataclasses import asdict
from typing import Any
import json
import sys

from climatevision.generator import calculate_with_default_inputs, RefData, make_entries
from climatevision.tracing import with_tracing


def json_to_output(json_object: object, args: Any):
    """Write json_object to stdout or a file depending on args"""
    if args.o is not None:
        with open(args.o, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
    else:
        json.dump(json_object, indent=4, fp=sys.stdout)


def cmd_run(args: Any):
    d = with_tracing(
        enabled=args.trace,
        f=lambda: calculate_with_default_inputs(
            year_ref=args.year_ref,
            ags=args.ags,
            year_baseline=args.year_baseline,
            year_target=args.year_target,
        ).result_dict(),
    )
    json_to_output(d, args)


def cmd_make_entries(args: Any):
    rd = RefData.load(args.year_ref)
    e = with_tracing(
        enabled=args.trace,
        f=lambda: asdict(
            make_entries(
                data=rd,
                ags=args.ags,
                year_baseline=args.year_baseline,
                year_target=args.year_target,
            )
        ),
    )
    json_to_output(e, args)
