# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class CO2eEmissions:
    # Used by a, p_fermen, p_manure, p_soil, p_other, p_other_liming
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float

    @classmethod
    def sum(cls, *co2es: "CO2eEmissions") -> "CO2eEmissions":
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in co2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in co2es),
            CO2e_total=sum(c.CO2e_total for c in co2es),
        )
