from dataclasses import dataclass


@dataclass
class CO2e_with_pct_energy:
    # Used by p_metal_steel
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
