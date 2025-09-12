# pyright: strict

from dataclasses import dataclass

from ..common.invest import InvestCommune


@dataclass(kw_only=True)
class Vars0(InvestCommune):
    # Used by b
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars3(InvestCommune):
    # Used by p
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_heatnet: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    demand_solarth: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4(InvestCommune):
    # Used by p_nonresi
    area_m2: float = None  # type: ignore
    area_m2_nonrehab: float = None  # type: ignore
    area_m2_rehab: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_heat_nonrehab: float = None  # type: ignore
    demand_heat_rehab: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    fec_factor_averaged: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_nonrehab: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    pct_rehab: float = None  # type: ignore
    rate_rehab_pa: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by p_nonresi_com
    area_m2: float = None  # type: ignore
    area_m2_rehab: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    energy: float = None  # type: ignore
    fec_factor_averaged: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6:
    # Used by p_elec_elcon
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7:
    # Used by p_elec_heatpump
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8:
    # Used by p_vehicles
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9:
    # Used by p_other
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars10(InvestCommune):
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars11:
    # Used by s_gas
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars12:
    # Used by s_emethan
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars13:
    # Used by s_lpg, s_petrol, s_jetfuel, s_diesel, s_elec_heating, s_elec
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars14:
    # Used by s_fueloil, s_coal
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars15:
    # Used by s_biomass, s_heatnet
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars16(InvestCommune):
    # Used by s_heatpump
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars17(InvestCommune):
    # Used by s_solarth
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    area_ha_available: float = None  # type: ignore
    area_ha_available_pct_of_action: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    energy_installable: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_to_be_installed_pct: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars18(InvestCommune):
    # Used by rb
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_year_before_baseline_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    energy: float = None  # type: ignore
