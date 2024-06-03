from typing import Any


def add_ags_argument(parser: Any):
    parser.add_argument("-ags", default="03159016")


def add_year_ref_argument(parser: Any):
    parser.add_argument(
        "-year_ref",
        type=int,
        default=2018,
        choices=[2018, 2021],
        help="year of the reference data",
    )


def add_year_baseline_argument(parser: Any):
    parser.add_argument(
        "-year_baseline",
        type=int,
        default=2022,
        choices=[2022],
        help="the baseline year should nearly be the current year - it represents the year which separates the past (based on reference data) and the future (where the path to CO2 neutrality starts)",
    )


def add_year_target_argument(parser: Any):
    parser.add_argument(
        "-year_target",
        type=int,
        default=2035,
        choices=range(2025, 2051),
        help="target year",
    )


def add_output_argument(parser: Any):
    parser.add_argument("-o", default=None, help="output file path")


def add_trace_argument(parser: Any):
    parser.add_argument("-trace", action="store_true")
