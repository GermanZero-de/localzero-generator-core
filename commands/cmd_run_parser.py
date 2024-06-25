# pyright: strict

from typing import Any

from commands.cmd_run import cmd_run, cmd_make_entries
from . import arguments


def add_cmd_run_parser(subcmd_parsers: Any):
    cmd_run_parser = subcmd_parsers.add_parser("run", help="Run the generator")

    arguments.add_ags_argument(cmd_run_parser)
    arguments.add_year_ref_argument(cmd_run_parser)
    arguments.add_year_baseline_argument(cmd_run_parser)
    arguments.add_year_target_argument(cmd_run_parser)
    arguments.add_output_argument(cmd_run_parser)
    arguments.add_trace_argument(cmd_run_parser)

    cmd_run_parser.set_defaults(func=cmd_run)


def add_cmd_make_entries_parser(subcmd_parsers: Any):
    cmd_make_entries_parser = subcmd_parsers.add_parser("make", help="Run make entries")

    arguments.add_ags_argument(cmd_make_entries_parser)
    arguments.add_year_ref_argument(cmd_make_entries_parser)
    arguments.add_year_baseline_argument(cmd_make_entries_parser)
    arguments.add_year_target_argument(cmd_make_entries_parser)
    arguments.add_output_argument(cmd_make_entries_parser)
    arguments.add_trace_argument(cmd_make_entries_parser)

    cmd_make_entries_parser.set_defaults(func=cmd_make_entries)
