# pyright: strict

from dataclasses import dataclass

from ..utils import div


@dataclass(kw_only=True)
class Energy:
    energy: float


@dataclass(kw_only=True)
class EnergyWithPercentage(Energy):
    pct_energy: float

    @classmethod
    def calc(cls, energy: float, total_energy: float) -> "EnergyWithPercentage":
        return cls(energy=energy, pct_energy=div(energy, total_energy))
