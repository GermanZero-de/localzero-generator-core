# pyright: strict

from dataclasses import dataclass

from .energy import Energy
from .co2_equivalent_emission import CO2eEmission


@dataclass(kw_only=True)
class EnergyWithCO2e(Energy, CO2eEmission):
    @classmethod
    def sum(  # type: ignore[override]
        cls, *CO2es: "EnergyWithCO2e"
    ) -> "EnergyWithCO2e":
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in CO2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in CO2es),
            CO2e_total=sum(c.CO2e_total for c in CO2es),
            energy=sum(c.energy for c in CO2es),
        )
