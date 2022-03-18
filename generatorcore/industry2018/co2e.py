from dataclasses import dataclass
from ..utils import element_wise_plus


@dataclass
class CO2e:
    # Used by i, p, p_miner, p_chem, p_metal, p_other
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore

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
