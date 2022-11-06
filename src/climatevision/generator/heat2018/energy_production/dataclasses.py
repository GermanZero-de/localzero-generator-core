# pyright: strict

from dataclasses import dataclass
from typing import Any

from ...utils import div


@dataclass(kw_only=True)
class HeatProduction:
    CO2e_combustion_based: float
    CO2e_combustion_based_per_MWh: float
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    @classmethod
    def calcFromEnergyAndCO2eBasedPerMWh(
        cls,
        energy: float,
        total_energy: float,
        CO2e_production_based_per_MWh: float = 0,
        CO2e_combustion_based_per_MWh: float = 0,
    ) -> "HeatProduction":
        pct_energy = div(energy, total_energy)

        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        return cls(
            energy=energy,
            pct_energy=pct_energy,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )

    @classmethod
    def calcFromEnergyAndCO2e(
        cls,
        energy: float,
        total_energy: float,
        CO2e_production_based: float = 0,
        CO2e_combustion_based: float = 0,
    ) -> "HeatProduction":
        pct_energy = div(energy, total_energy)

        CO2e_production_based_per_MWh = div(CO2e_production_based, energy)
        CO2e_combustion_based_per_MWh = div(CO2e_combustion_based, energy)

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        return cls(
            energy=energy,
            pct_energy=pct_energy,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )

    @classmethod
    def calcFromPctEnergyAndCO2eBasedPerMWh(
        cls,
        pct_energy: float,
        total_energy: float,
        CO2e_production_based_per_MWh: float = 0,
        CO2e_combustion_based_per_MWh: float = 0,
    ) -> "HeatProduction":
        energy = total_energy * pct_energy

        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        return cls(
            energy=energy,
            pct_energy=pct_energy,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )

    @classmethod
    def calcSum(cls, energy: float, *childs: Any) -> "HeatProduction":
        pct_energy = sum(child.pct_energy for child in childs)

        CO2e_combustion_based = sum(child.CO2e_combustion_based for child in childs)
        CO2e_production_based = sum(child.CO2e_production_based for child in childs)

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        CO2e_combustion_based_per_MWh = div(CO2e_combustion_based, energy)
        CO2e_production_based_per_MWh = div(CO2e_production_based, energy)

        return cls(
            energy=energy,
            pct_energy=pct_energy,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )


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
