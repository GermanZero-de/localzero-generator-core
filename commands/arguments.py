from typing import Any


def add_year_ref_argument(parser: Any):
    parser.add_argument("-year_ref", type=int, default=2018)
