# pyright: strict

from dataclasses import dataclass
from typing import Any

from ...utils import div


@dataclass(kw_only=True)
class TotalHeatProduction:
    CO2e_combustion_based: float
    CO2e_combustion_based_per_MWh: float
    CO2e_production_based: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(self, energy: float, *childs: Any):
        self.energy = energy
        self.pct_energy = sum(child.pct_energy for child in childs)

        self.CO2e_production_based = sum(
            child.CO2e_production_based for child in childs
        )
        self.CO2e_combustion_based = sum(
            child.CO2e_combustion_based for child in childs
        )

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based

        self.CO2e_combustion_based_per_MWh = div(self.CO2e_combustion_based, energy)


@dataclass(kw_only=True)
class HeatProduction:
    CO2e_combustion_based: float
    CO2e_combustion_based_per_MWh: float
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        energy: float,
        total_energy: float,
        CO2e_production_based_per_MWh: float = 0,
        CO2e_combustion_based_per_MWh: float = 0,
    ):
        self.energy = energy
        self.pct_energy = div(energy, total_energy)

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_combustion_based_per_MWh = CO2e_combustion_based_per_MWh

        self.CO2e_production_based = energy * CO2e_production_based_per_MWh
        self.CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based


@dataclass(kw_only=True)
class Vars6:
    CO2e_production_based: float = 0
    CO2e_combustion_based: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        energy: float,
        total_energy: float,
        CO2e_combustion_based: float,
    ):
        self.energy = energy
        self.pct_energy = div(energy, total_energy)

        self.CO2e_combustion_based = CO2e_combustion_based
        self.CO2e_total = CO2e_combustion_based


@dataclass(kw_only=True)
class Vars8FromEnergySum:
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_combustion_based: float = 0
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        energy: float,
        total_energy: float,
        CO2e_production_based_per_MWh: float,
        CO2e_production_based: float,
    ):
        self.energy = energy
        self.pct_energy = div(energy, total_energy)

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_production_based = CO2e_production_based
        self.CO2e_total = self.CO2e_production_based


@dataclass(kw_only=True)
class Vars8FromEnergyPct:
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        pct_energy: float,
        total_energy: float,
        CO2e_production_based_per_MWh: float,
    ):
        self.pct_energy = pct_energy
        self.energy = total_energy * pct_energy

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_production_based = self.energy * self.CO2e_production_based_per_MWh
        self.CO2e_total = self.CO2e_production_based