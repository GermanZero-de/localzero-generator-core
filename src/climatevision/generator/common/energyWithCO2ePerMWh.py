# pyright: strict

from dataclasses import dataclass

from ..utils import div


@dataclass(kw_only=True)
class EnergyWithCO2ePerMWh:
    CO2e_combustion_based: float = 0
    CO2e_combustion_based_per_MWh: float
    CO2e_production_based: float = 0
    CO2e_production_based_per_MWh: float
    CO2e_total: float = 0
    energy: float

    @classmethod
    def calcFromEnergyAndCO2eBasedPerMWh(
        cls,
        energy: float,
        CO2e_production_based_per_MWh: float = 0,
        CO2e_combustion_based_per_MWh: float = 0,
    ) -> "EnergyWithCO2ePerMWh":
        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        return cls(
            energy=energy,
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
        CO2e_production_based: float = 0,
        CO2e_combustion_based: float = 0,
    ) -> "EnergyWithCO2ePerMWh":
        CO2e_production_based_per_MWh = div(CO2e_production_based, energy)
        CO2e_combustion_based_per_MWh = div(CO2e_combustion_based, energy)

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        return cls(
            energy=energy,
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
    ) -> "EnergyWithCO2ePerMWh":
        energy = total_energy * pct_energy

        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        return cls(
            energy=energy,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )

    @classmethod
    def calcSum(cls, *childs: "EnergyWithCO2ePerMWh") -> "EnergyWithCO2ePerMWh":
        energy = sum(child.energy for child in childs)

        CO2e_combustion_based = sum(child.CO2e_combustion_based for child in childs)
        CO2e_production_based = sum(child.CO2e_production_based for child in childs)

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        CO2e_combustion_based_per_MWh = div(CO2e_combustion_based, energy)
        CO2e_production_based_per_MWh = div(CO2e_production_based, energy)

        return cls(
            energy=energy,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )
