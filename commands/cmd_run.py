# pyright: strict

from dataclasses import asdict
from typing import Any
import json
import sys

from climatevision.generator import calculate_with_default_inputs, RefData, make_entries
from . import monkeypatch


def json_to_output(json_object: Any, args: Any):
    """Write json_object to stdout or a file depending on args"""
    if args.o is not None:
        with open(args.o, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
    else:
        json.dump(json_object, indent=4, fp=sys.stdout)


def cmd_run(args: Any):
    finalize_traces_if_enabled = monkeypatch.maybe_enable_tracing(args)
    g = calculate_with_default_inputs(ags=args.ags, year=int(args.year))
    d = finalize_traces_if_enabled(g.result_dict())
    json_to_output(d, args)


def cmd_make_entries(args: Any):
    finalize_traces_if_enabled = monkeypatch.maybe_enable_tracing(args)
    rd = RefData.load()
    e = make_entries(rd, args.ags, int(args.year))
    json_to_output(finalize_traces_if_enabled(asdict(e)), args)
