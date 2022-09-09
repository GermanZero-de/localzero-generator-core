# pyright: strict
from typing import Any
from commands.cmd_explorer import cmd_explorer


def add_cmd_explorer_parser(subcmd_parsers: Any):
    cmd_explorer_parser = subcmd_parsers.add_parser(
        "explorer", help="Start the LocalZero Explorer"
    )
    cmd_explorer_parser.add_argument("-trace", action="store_true")
    cmd_explorer_parser.set_defaults(func=cmd_explorer)
