# pyright: strict

from typing import Any

from commands.cmd_data import (
    cmd_data_normalize,
    cmd_data_checkout,
    cmd_data_lookup,
    cmd_data_is_production,
)


def add_cmd_data_parser(subcmd_parsers: Any):
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
        help="Lookup all the reference data for a given AGS, or lookup a fact or assumption.",
    )
    cmd_data_lookup_parser.add_argument("pattern")
    cmd_data_lookup_parser.add_argument(
        "-no-fixes", action="store_false", dest="fix_missing_entries"
    )
    cmd_data_lookup_parser.set_defaults(func=cmd_data_lookup)
