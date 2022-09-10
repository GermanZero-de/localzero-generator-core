# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class EnergyDemand:
    energy: float
