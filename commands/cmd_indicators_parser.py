# pyright: strict

from typing import Any

from commands.cmd_indicators import cmd_indicators


def add_cmd_indicators_parser(subcmd_parsers: Any):
    cmd_run_parser = subcmd_parsers.add_parser(
        "indicators", help="Run the generator and publish indicators"
    )
    cmd_run_parser.add_argument("-ags", default="03159016")
    cmd_run_parser.add_argument("-year", default=2035)
    cmd_run_parser.add_argument("-o", default=None)
    cmd_run_parser.add_argument("-trace", action="store_true")
    cmd_run_parser.set_defaults(func=cmd_indicators)
