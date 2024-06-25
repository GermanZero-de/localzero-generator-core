# pyright: strict

from typing import Any

from commands.cmd_test_end_to_end import (
    cmd_test_end_to_end_update_expectations,
    cmd_test_end_to_end_create_expectation,
    cmd_test_end_to_end_run_all_ags,
)
from . import arguments


def add_cmd_test_end_to_end_parser(subcmd_parsers: Any):
    cmd_test_end_to_end_parser = subcmd_parsers.add_parser(
        name="test_end_to_end", help="Test tools for end to end tests"
    )
    subcmd_test_end_to_end = cmd_test_end_to_end_parser.add_subparsers(
        title="Test tools", dest="subcmd"
    )

    cmd_test_end_to_end_update_expectations_parser = subcmd_test_end_to_end.add_parser(
        "update_expectations",
        help="Update the expectations for the end to end tests.",
    )
    cmd_test_end_to_end_update_expectations_parser.set_defaults(
        func=cmd_test_end_to_end_update_expectations
    )

    cmd_test_end_to_end_create_expectation_parser = subcmd_test_end_to_end.add_parser(
        "create_expectation",
        help="Create an expectation for the end to end tests.",
    )
    arguments.add_ags_argument(cmd_test_end_to_end_create_expectation_parser)
    arguments.add_year_baseline_argument(cmd_test_end_to_end_create_expectation_parser)
    arguments.add_year_target_argument(cmd_test_end_to_end_create_expectation_parser)
    cmd_test_end_to_end_create_expectation_parser.set_defaults(
        func=cmd_test_end_to_end_create_expectation
    )

    cmd_test_end_to_end_run_all_ags_parser = subcmd_test_end_to_end.add_parser(
        "run_all_ags",
        help="Runs the generator for all ags.",
    )
    arguments.add_year_ref_argument(cmd_test_end_to_end_run_all_ags_parser)
    arguments.add_year_baseline_argument(cmd_test_end_to_end_run_all_ags_parser)
    arguments.add_year_target_argument(cmd_test_end_to_end_run_all_ags_parser)
    cmd_test_end_to_end_run_all_ags_parser.set_defaults(
        func=cmd_test_end_to_end_run_all_ags
    )
