# pyright: strict

from typing import Any

from commands.cmd_test_end_to_end import (
    cmd_test_end_to_end_update_expectations,
    cmd_test_end_to_end_create_expectation,
    cmd_test_end_to_end_run_all_ags,
)


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
    cmd_test_end_to_end_create_expectation_parser.add_argument(
        "-ags", default="03159016"
    )
    cmd_test_end_to_end_create_expectation_parser.add_argument("-year", default=2035)
    cmd_test_end_to_end_create_expectation_parser.set_defaults(
        func=cmd_test_end_to_end_create_expectation
    )

    cmd_test_end_to_end_run_all_ags_parser = subcmd_test_end_to_end.add_parser(
        "run_all_ags",
        help="Runs the generator for all ags.",
    )
    cmd_test_end_to_end_run_all_ags_parser.add_argument("-year", default=2035)
    cmd_test_end_to_end_run_all_ags_parser.add_argument("-year_ref", default=2018)
    cmd_test_end_to_end_run_all_ags_parser.set_defaults(
        func=cmd_test_end_to_end_run_all_ags
    )
