import json
import sys
from generatorcore.generator import calculate_with_default_inputs


def json_to_output(json_object, args):
    """Write json_object to stdout or a file depending on args"""
    if args.o is not None:
        with open(args.o, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
    else:
        json.dump(json_object, indent=4, fp=sys.stdout)


def cmd_run(args):
    # TODO: pass ags in here
    g = calculate_with_default_inputs(ags=args.ags, year=args.year)
    json_to_output(g.result_dict(), args)
