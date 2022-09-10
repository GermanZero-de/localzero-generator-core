#!/usr/bin/env python

"""
This is a simple wrapper around the generator to

    - Make sure we eat our own dog food(TM) and try the API.

    - Give us a quick way to run the generator as
      just running Generator.py as a script runs into the
      scripts and packages / modules shall not be mixed rule.
      See https://mail.python.org/pipermail/python-3000/2007-April/006793.html
"""

# pyright: strict

from typing import Any
import argparse
import sys

from commands.cmd_run_parser import add_cmd_make_entries_parser, add_cmd_run_parser
from commands.cmd_explorer_parser import add_cmd_explorer_parser
from commands.cmd_ready_to_rock_parser import add_cmd_ready_to_rock_parser
from commands.cmd_data_parser import add_cmd_data_parser
from commands.cmd_test_end_to_end_parser import add_cmd_test_end_to_end_parser


class Devtool:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def parse_args(self, args: Any):
        self.parser.set_defaults()
        subcmd_parsers = self.parser.add_subparsers(dest="subcmd", title="Commands")

        add_cmd_run_parser(subcmd_parsers)
        add_cmd_make_entries_parser(subcmd_parsers)
        add_cmd_explorer_parser(subcmd_parsers)
        add_cmd_ready_to_rock_parser(subcmd_parsers)
        add_cmd_data_parser(subcmd_parsers)
        add_cmd_test_end_to_end_parser(subcmd_parsers)

        return self.parser.parse_args(args)


def main():
    devtool = Devtool()
    args = devtool.parse_args(sys.argv[1:])

    if args.subcmd is None:
        devtool.parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
