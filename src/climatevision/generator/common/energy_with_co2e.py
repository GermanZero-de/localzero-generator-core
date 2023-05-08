# pyright: strict

from dataclasses import dataclass

from .energy import Energy
from .co2_equivalent_emission import CO2eEmission


@dataclass(kw_only=True)
class EnergyWithCO2e(Energy, CO2eEmission):
    @classmethod
    def sum(  # type: ignore[override]
        cls, *childs: "EnergyWithCO2e"
    ) -> "EnergyWithCO2e":
        return cls(
            CO2e_combustion_based=sum(child.CO2e_combustion_based for child in childs),
            CO2e_production_based=sum(child.CO2e_production_based for child in childs),
            CO2e_total=sum(child.CO2e_total for child in childs),
            energy=sum(child.energy for child in childs),
        )
