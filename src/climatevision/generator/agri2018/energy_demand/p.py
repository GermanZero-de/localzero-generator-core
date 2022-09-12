# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class P:
    # TODO: What is a good name for this?
    # Used by p
    CO2e_production_based: float
    CO2e_total: float
    energy: float
