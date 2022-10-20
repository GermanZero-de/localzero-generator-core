# pyright: strict

from typing import Any
import json
import sys

from climatevision.tracing import with_tracing
from climatevision.generator import calculate_with_default_inputs

def json_to_output(json_object: Any, args: Any):
    """Write json_object to stdout or a file depending on args"""
    if args.o is not None:
        with open(args.o, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
    else:
        json.dump(json_object, indent=4, fp=sys.stdout)

def cmd_indicators(args: Any):
    d = with_tracing(
        enabled=args.trace,
        f=lambda: calculate_with_default_inputs(
            ags=args.ags, year=int(args.year)
        ).result_dict(),
    )
    json_to_output(d, args)

