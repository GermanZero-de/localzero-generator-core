# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class LColVars2030:
    area_ha: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    pct_x: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    invest: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    area_ha_change: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    area_ha_available_pct_of_action: float = None  # type: ignore
    area_ha_available: float = None  # type: ignore
    change_within_category: float = None  # type: ignore
    change_wet_org_low: float = None  # type: ignore
    change_wet_org_high: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
