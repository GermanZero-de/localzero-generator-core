from dataclasses import dataclass


@dataclass
class CO2e:
    # Used by i, p, p_miner, p_chem, p_metal, p_other
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
