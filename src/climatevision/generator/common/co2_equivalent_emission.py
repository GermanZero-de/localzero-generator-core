# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class CO2eEmission:
    CO2e_combustion_based: float = 0
    CO2e_production_based: float = 0
    CO2e_total: float = 0

    def __post_init__(self):
        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based

    @classmethod
    def sum(cls, *CO2es: "CO2eEmission") -> "CO2eEmission":
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in CO2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in CO2es),
            CO2e_total=sum(c.CO2e_total for c in CO2es),
        )
