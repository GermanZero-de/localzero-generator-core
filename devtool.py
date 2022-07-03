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
import argparse
from commands.cmd_run_parser import add_cmd_make_entries_parser, add_cmd_run_parser
from commands.cmd_explorer_parser import add_cmd_explorer_parser
from commands.cmd_ready_to_rock_parser import add_cmd_ready_to_rock_parser
from commands.cmd_compare_to_excel_parser import add_cmd_compare_to_excel_parser
from commands.cmd_data_parser import add_cmd_data_parser
from commands.cmd_test_end_to_end_parser import add_cmd_test_end_to_end_parser


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults()
    subcmd_parsers = parser.add_subparsers(dest="subcmd", title="Commands")

    add_cmd_run_parser(subcmd_parsers)
    add_cmd_make_entries_parser(subcmd_parsers)
    add_cmd_explorer_parser(subcmd_parsers)
    add_cmd_ready_to_rock_parser(subcmd_parsers)
    add_cmd_compare_to_excel_parser(subcmd_parsers)
    add_cmd_data_parser(subcmd_parsers)
    add_cmd_test_end_to_end_parser(subcmd_parsers)

    args = parser.parse_args()
    if args.subcmd is None:
        parser.print_help()
    else:
        args.func(args)


main()
