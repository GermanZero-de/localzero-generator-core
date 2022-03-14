from dataclasses import dataclass


@dataclass
class CO2e_basic:
    # Used by p_other_2efgh
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
