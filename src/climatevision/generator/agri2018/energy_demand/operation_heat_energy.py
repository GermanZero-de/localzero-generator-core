# pyright: strict

from dataclasses import dataclass, InitVar

from ...common.energy import EnergyWithPercentage, EnergyPerM2


@dataclass(kw_only=True)
class OperationHeatEnergy(EnergyWithPercentage, EnergyPerM2):
    total_energy: InitVar[float]

    def __post_init__(self, total_energy: float):  # type: ignore
        EnergyWithPercentage.__post_init__(self, total_energy=total_energy)
        EnergyPerM2.__post_init__(self)
