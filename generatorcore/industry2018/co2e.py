# pyright: strict
from dataclasses import dataclass


@dataclass
class CO2e:
    # Used by i, p, p_miner, p_chem, p_metal, p_other
    CO2e_combustion_based: float = 0
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    energy: float = 0
    prod_volume: float = 0

    def __add__(self: "CO2e", other: "CO2e") -> "CO2e":
        return CO2e(
            CO2e_combustion_based=self.CO2e_combustion_based
            + other.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based
            + other.CO2e_production_based,
            CO2e_total=self.CO2e_total + other.CO2e_total,
            energy=self.energy + other.energy,
            prod_volume=self.prod_volume + other.prod_volume,
        )
