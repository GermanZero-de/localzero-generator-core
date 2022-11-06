# pyright: strict

from typing import Any
import json
import sys

from climatevision.generator.generator import calculate_indicators_with_default_inputs


def json_to_output(json_object: Any, args: Any):
    """Write json_object to stdout or a file depending on args"""
    if args.o is not None:
        with open(args.o, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
    else:
        json.dump(json_object, indent=4, fp=sys.stdout)


def cmd_indicators(args: Any):
    ind = calculate_indicators_with_default_inputs(ags=args.ags, year=int(args.year)
        )
    print("")
    print("Um den Bedarf an Elektrizität lokal zu decken, müssen:")
    print("- " + str(ind.pv_pa) + " PV-Module auf die Dächer geschraubt werden oder")
    print("- " + str(ind.wpp_pa) + " mit einer Leistung von 3,2 MW gebaut werden")


