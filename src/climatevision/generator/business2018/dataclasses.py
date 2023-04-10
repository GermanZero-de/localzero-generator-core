# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class Vars10:
    # Used by rp_p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
