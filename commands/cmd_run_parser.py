# pyright: strict
from typing import Any
from commands.cmd_run import cmd_run, cmd_make_entries


def add_cmd_run_parser(subcmd_parsers: Any):
    cmd_run_parser = subcmd_parsers.add_parser("run", help="Run the generator")
    cmd_run_parser.add_argument("-ags", default="03159016")
    cmd_run_parser.add_argument("-year", default=2035)
    cmd_run_parser.add_argument("-o", default=None)
    cmd_run_parser.add_argument("-trace", action="store_true")
    cmd_run_parser.set_defaults(func=cmd_run)


def add_cmd_make_entries_parser(subcmd_parsers: Any):
    cmd_make_entries_parser = subcmd_parsers.add_parser("make", help="Run make entries")
    cmd_make_entries_parser.add_argument("-ags", default="03159016")
    cmd_make_entries_parser.add_argument("-year", default=2035)
    cmd_make_entries_parser.add_argument("-o", default=None)
    cmd_make_entries_parser.add_argument("-trace", action="store_true")
    cmd_make_entries_parser.set_defaults(func=cmd_make_entries)
