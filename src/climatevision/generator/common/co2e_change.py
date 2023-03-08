# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class CO2eChange:
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    cost_climate_saved: float = 0


@dataclass(kw_only=True)
class CO2eChangeEnergy:
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
