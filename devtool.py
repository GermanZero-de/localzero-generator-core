#!/usr/bin/env python
"""
This is a simple wrapper around the generator to

    - Make sure we eat our own dog food(TM) and try the API.

    - Give us a quick way to run the generator as
      just running Generator.py as a script runs into the
      scripts and packages / modules shall not be mixed rule.
      See https://mail.python.org/pipermail/python-3000/2007-April/006793.html
"""
import argparse

from generatorcore.generator import Generator


def run_cmd(args):
    # TODO: pass ags in here
    Generator()


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults()
    subcmd_parsers = parser.add_subparsers(dest="subcmd")

    cmd_run_parser = subcmd_parsers.add_parser("run", help="Run the generator")
    # TODO: Add the below when the generator can actually use that
    # cmd_run_parser.add_argument('-ags', default='03159016')
    cmd_run_parser.set_defaults(func=run_cmd)

    args = parser.parse_args()
    if args.subcmd is None:
        parser.print_help()
    else:
        args.func(args)


main()
