# pyright: strict
from dataclasses import dataclass


@dataclass
class EnergySum:
    # Used by s_fossil, s_renew
    energy: float
