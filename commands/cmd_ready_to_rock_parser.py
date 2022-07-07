# pyright: strict
from typing import Any
from commands.cmd_ready_to_rock import cmd_ready_to_rock


def add_cmd_ready_to_rock_parser(subcmd_parsers: Any):
    cmd_ready_to_rock_parser = subcmd_parsers.add_parser(
        "ready_to_rock", help="Check if all is well"
    )
    cmd_ready_to_rock_parser.set_defaults(func=cmd_ready_to_rock)
