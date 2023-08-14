# pyright: strict

from dataclasses import dataclass, InitVar

from ...utils import div


@dataclass(kw_only=True)
class Energy:
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyDemand(Energy):
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyDemandWithCostFuel(EnergyDemand):
    cost_fuel_per_MWh: float
    cost_fuel: float = None  # type: ignore

    energy_18: InitVar[float]

    def __post_init__(self, energy_18: float):
        self.change_energy_MWh = self.energy - energy_18
        self.change_energy_pct = div(self.change_energy_MWh, energy_18)
