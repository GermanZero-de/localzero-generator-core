# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class F:
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float
