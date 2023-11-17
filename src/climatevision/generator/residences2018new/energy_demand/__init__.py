# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions


@dataclass(kw_only=True)
class Production:
    total: float = None  # type: ignore
    dummy: float = None  # type: ignore


def calc_production(
    entries: Entries, facts: Facts, assumptions: Assumptions
) -> Production:

    return Production(dummy=0)
