# pyright: strict

from dataclasses import dataclass

from ...common.co2_equivalent_emission import CO2eEmission


@dataclass(kw_only=True)
class CO2eFromEnergyUse(CO2eEmission):
    # Used by s
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float
    energy: float

    @classmethod
    def sum(cls, *CO2es: "CO2eFromEnergyUse") -> "CO2eFromEnergyUse":  # type: ignore
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in CO2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in CO2es),
            CO2e_total=sum(c.CO2e_total for c in CO2es),
            energy=sum(c.energy for c in CO2es),
        )
