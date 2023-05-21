# pyright: strict

from dataclasses import dataclass

from ...utils import MILLION
from ...common.energy_with_co2e_per_mwh import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class Vars5:
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyWithCO2ePerMWhAndCostFuel(EnergyWithCO2ePerMWh):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float

    def __post_init__(self):
        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION

        EnergyWithCO2ePerMWh.__post_init__(self)


@dataclass(kw_only=True)
class EnergyWithCO2ePerMWhAndCostFuelAndBuildings(EnergyWithCO2ePerMWhAndCostFuel):
    number_of_buildings: float = None  # type: ignore
