# pyright: strict

from dataclasses import dataclass

from ...utils import MILLION
from ...common.energy import EnergyWithPercentage


@dataclass(kw_only=True)
class Vars5:
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyWithPercentageWithCO2ePerMWh(EnergyWithPercentage):
    CO2e_combustion_based: float = 0
    CO2e_combustion_based_per_MWh: float
    CO2e_total: float = 0

    def __post_init__(self, total_energy: float):
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh
        self.CO2e_total = self.CO2e_combustion_based

        EnergyWithPercentage.__post_init__(self, total_energy)


@dataclass(kw_only=True)
class Vars6(EnergyWithPercentageWithCO2ePerMWh):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float

    def __post_init__(self, total_energy: float):
        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION

        EnergyWithPercentageWithCO2ePerMWh.__post_init__(self, total_energy)


@dataclass(kw_only=True)
class Vars7(Vars6):
    number_of_buildings: float = None  # type: ignore
