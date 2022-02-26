#!/usr/bin/env python
"""
This is a simple wrapper around the generator to

    - Make sure we eat our own dog food(TM) and try the API.

    - Give us a quick way to run the generator as
      just running Generator.py as a script runs into the
      scripts and packages / modules shall not be mixed rule.
      See https://mail.python.org/pipermail/python-3000/2007-April/006793.html
"""
import argparse
from commands.cmd_ready_to_rock import cmd_ready_to_rock
from commands.cmd_run import cmd_run
from commands.cmd_compare_to_excel import cmd_compare_to_excel
from commands.cmd_data import (
    cmd_data_normalize,
    cmd_data_checkout,
    cmd_data_entries_user_overrides_generate_defaults,
    cmd_data_lookup,
    cmd_data_is_production,
)
from commands.cmd_test_end_to_end import (
    cmd_test_end_to_end_update_expectations,
    cmd_test_end_to_end_create_expectation,
    cmd_test_end_to_end_run_all_ags,
)


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults()
    subcmd_parsers = parser.add_subparsers(dest="subcmd", title="Commands")

    cmd_run_parser = subcmd_parsers.add_parser("run", help="Run the generator")
    cmd_run_parser.add_argument("-ags", default="03159016")
    cmd_run_parser.add_argument("-year", default=2035)
    cmd_run_parser.add_argument("-o", default=None)
    cmd_run_parser.set_defaults(func=cmd_run)

    cmd_ready_to_rock_parser = subcmd_parsers.add_parser(
        "ready_to_rock", help="Check if all is well"
    )
    cmd_ready_to_rock_parser.set_defaults(func=cmd_ready_to_rock)

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

    cmd_data_parser = subcmd_parsers.add_parser(
        name="data", help="Data Repository tools"
    )
    subcmd_data = cmd_data_parser.add_subparsers(
        title="Data Repository tools", dest="subcmd"
    )

    cmd_data_is_production_parser = subcmd_data.add_parser(
        "is-production",
        help="Check that the data dir contains clean checkouts of the production reference data set",
    )
    cmd_data_is_production_parser.set_defaults(func=cmd_data_is_production)

    cmd_data_normalize_parser = subcmd_data.add_parser(
        "normalize",
        help="Normalize csv files",
    )
    cmd_data_normalize_parser.add_argument("file")
    cmd_data_normalize_parser.set_defaults(func=cmd_data_normalize)

    cmd_data_checkout_parser = subcmd_data.add_parser(
        "checkout",
        help="Checkout the production version of the reference data (if necessary clone them first)",
    )
    cmd_data_checkout_parser.add_argument("-pat", action="store", default=None)
    cmd_data_checkout_parser.set_defaults(func=cmd_data_checkout)

    cmd_data_lookup_parser = subcmd_data.add_parser(
        "lookup",
        help="Lookup all the reference data for a given AGS",
    )
    cmd_data_lookup_parser.add_argument("ags")
    cmd_data_lookup_parser.add_argument(
        "-no-fixes", action="store_false", dest="fix_missing_entries"
    )
    cmd_data_lookup_parser.set_defaults(func=cmd_data_lookup)

    cmd_data_entries_user_overrides_generate_defaults_parser = subcmd_data.add_parser(
        "entries-user-overrides-generate-defaults",
        help="Generate a file of default values for user overridable entries as used by the website.",
    )
    cmd_data_entries_user_overrides_generate_defaults_parser.set_defaults(
        func=cmd_data_entries_user_overrides_generate_defaults
    )

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
    cmd_test_end_to_end_run_all_ags_parser.set_defaults(
        func=cmd_test_end_to_end_run_all_ags
    )

    args = parser.parse_args()
    if args.subcmd is None:
        parser.print_help()
    else:
        args.func(args)


main()
