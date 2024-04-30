# pyright: strict

from typing import Any

from commands.cmd_explorer import cmd_explorer
from . import arguments


def add_cmd_explorer_parser(subcmd_parsers: Any):
    cmd_explorer_parser = subcmd_parsers.add_parser(
        "explorer", help="Start the LocalZero Explorer"
    )

    arguments.add_year_ref_argument(cmd_explorer_parser)
    arguments.add_trace_argument(cmd_explorer_parser)

    cmd_explorer_parser.set_defaults(func=cmd_explorer)
