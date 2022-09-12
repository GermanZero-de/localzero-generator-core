# pyright: strict

from dataclasses import dataclass

from ...utils import div

from .energy import Energy


@dataclass(kw_only=True)
class EnergyWithPercentage(Energy):
    # Used by p_operation_elec_elcon, p_operation_vehicles
    pct_energy: float

    @classmethod
    def calc(cls, energy: float, total_energy: float) -> "EnergyWithPercentage":
        return cls(energy=energy, pct_energy=div(energy, total_energy))
