from typing import Any

from climatevision.generator.years import (
    YEAR_REF_DEFAULT,
    YEAR_REF_CHOICES,
    YEAR_REF_HELP,
    YEAR_BASELINE_DEFAULT,
    YEAR_BASELINE_CHOICES,
    YEAR_BASELINE_HELP,
    YEAR_TARGET_DEFAULT,
    YEAR_TARGET_CHOICES,
    YEAR_TARGET_HELP,
)


def add_ags_argument(parser: Any):
    parser.add_argument("-ags", default="03159016")


def add_year_ref_argument(parser: Any):
    parser.add_argument(
        "-year_ref",
        type=int,
        default=YEAR_REF_DEFAULT,
        choices=YEAR_REF_CHOICES,
        help=YEAR_REF_HELP,
    )


def add_year_baseline_argument(parser: Any):
    parser.add_argument(
        "-year_baseline",
        type=int,
        default=YEAR_BASELINE_DEFAULT,
        choices=YEAR_BASELINE_CHOICES,
        help=YEAR_BASELINE_HELP,
    )


def add_year_target_argument(parser: Any):
    parser.add_argument(
        "-year_target",
        type=int,
        default=YEAR_TARGET_DEFAULT,
        choices=YEAR_TARGET_CHOICES,
        help=YEAR_TARGET_HELP,
    )


def add_output_argument(parser: Any):
    parser.add_argument("-o", default=None, help="output file path")


def add_trace_argument(parser: Any):
    parser.add_argument("-trace", action="store_true")
