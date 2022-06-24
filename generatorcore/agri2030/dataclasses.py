from dataclasses import dataclass


@dataclass
class Vars0:
    # Used by a
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore


@dataclass
class Vars1:
    # Used by p
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore


@dataclass
class Vars2:
    # Used by g
    CO2e_total: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by g_consult
    area_ha_available: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by g_organic
    area_ha_available: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    power_to_be_installed_pct: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars5:
    # Used by p_fermen, p_manure, p_soil, p_other
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by p_fermen_dairycow, p_fermen_nondairy, p_fermen_swine, p_fermen_poultry, p_fermen_oanimal, p_manure_dairycow, p_manure_nondairy, p_manure_swine, p_manure_poultry, p_manure_oanimal, p_manure_deposition
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    amount: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_change: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by p_soil_fertilizer, p_soil_manure, p_soil_sludge, p_soil_ecrop, p_soil_grazing, p_soil_residue, p_soil_orgfarm, p_soil_orgloss, p_soil_leaching, p_soil_deposition
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    area_ha: float = None  # type: ignore
    area_ha_change: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_change: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by p_other_liming
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars9:
    # Used by p_other_liming_calcit, p_other_liming_dolomite, p_other_urea, p_other_kas, p_other_ecrop
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars10:
    # Used by p_operation
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore


@dataclass
class Vars11:
    # Used by p_operation_heat
    area_m2: float = None  # type: ignore
    area_m2_nonrehab: float = None  # type: ignore
    area_m2_rehab: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_heat_nonrehab: float = None  # type: ignore
    demand_heat_rehab: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    fec_factor_averaged: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_nonrehab: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    pct_rehab: float = None  # type: ignore
    rate_rehab_pa: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars12:
    # Used by p_operation_elec_elcon
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars13:
    # Used by p_operation_elec_heatpump
    change_energy_MWh: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars14:
    # Used by p_operation_vehicles
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars15:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars16:
    # Used by s_petrol, s_diesel, s_lpg, s_biomass, s_elec
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars17:
    # Used by s_fueloil, s_gas
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    area_m2: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars18:
    # Used by s_heatpump
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars19:
    # Used by s_emethan
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
