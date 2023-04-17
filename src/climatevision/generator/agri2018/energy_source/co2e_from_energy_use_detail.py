# pyright: strict

from dataclasses import dataclass

from .co2e_from_energy_use import CO2eFromEnergyUse


@dataclass(kw_only=True)
class CO2eFromEnergyUseDetail(CO2eFromEnergyUse):
    CO2e_combustion_based_per_MWh: float

    @classmethod
    def calc(
        cls, energy: float, CO2e_combustion_based_per_MWh: float
    ) -> "CO2eFromEnergyUseDetail":
        CO2e_production_based = 0.0
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
            energy=energy,
        )
