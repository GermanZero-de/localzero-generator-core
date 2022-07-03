# pyright: strict
from typing import Any
from commands.cmd_compare_to_excel import cmd_compare_to_excel


def add_cmd_compare_to_excel_parser(subcmd_parsers: Any):
    cmd_compare_to_excel_parser = subcmd_parsers.add_parser(
        "compare_to_excel", help="Compare an end to end test file with an excel file"
    )
    cmd_compare_to_excel_parser.add_argument("result_file")
    cmd_compare_to_excel_parser.add_argument("excel_file")
    cmd_compare_to_excel_parser.add_argument(
        "-show-missing-in-excel", action="store_true"
    )
    cmd_compare_to_excel_parser.add_argument(
        "-relative-tolerance", action="store", default="1e-6"
    )
    cmd_compare_to_excel_parser.set_defaults(func=cmd_compare_to_excel)
