# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class CO2eEmissions:
    CO2e_combustion_based: float = 0
    CO2e_production_based: float = 0
    CO2e_total: float = 0

    @classmethod
    def sum(cls, *co2es: "CO2eEmissions") -> "CO2eEmissions":
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in co2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in co2es),
            CO2e_total=sum(c.CO2e_total for c in co2es),
        )
