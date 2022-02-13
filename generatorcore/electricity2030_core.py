from dataclasses import dataclass, asdict

# Definition der relevanten Spaltennamen für den Sektor E
@dataclass
class EColVars2030:
    action: float = None
    energy: float = None
    pet_sites: float = None
    energy_installable: float = None
    cost_fuel_per_MWh: float = None
    cost_fuel: float = None
    pct_energy: float = None
    mro_per_MWh: float = None
    mro: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_cb: float = None
    cost_certificate_per_MWh: float = None
    cost_certificate: float = None
    cost_climate_saved: float = None
    cost_mro: float = None
    cost_mro_pa_com: float = None
    CO2e_total: float = None
    CO2e_total_2021_estimated: float = None
    demand_electricity: float = None
    demand_emplo: float = None
    demand_emplo_com: float = None
    power_installed: float = None
    power_to_be_installed_pct: float = None
    power_to_be_installed: float = None
    power_installable: float = None
    area_ha_available: float = None
    area_ha_available_pct_of_action: float = None
    ratio_power_to_area_ha: float = None
    cost_mro_pa: float = None
    change_energy_MWh: float = None
    change_energy_pct: float = None
    change_CO2e_t: float = None
    change_CO2e_pct: float = None
    change_cost_energy: float = None
    change_cost_mro: float = None
    invest: float = None
    invest_pa: float = None
    invest_com: float = None
    invest_pa_com: float = None
    invest_outside: float = None
    invest_pa_outside: float = None
    invest_per_x: float = None
    pct_of_wage: float = None
    pct_x: float = None
    ratio_wage_to_emplo: float = None
    cost_wage: float = None
    cost_mro_per_MWh: float = None
    demand_emplo: float = None
    emplo_existing: float = None
    demand_emplo_new: float = None
    full_load_hour: float = None
    lifecycle: float = None


# Definition der Zeilennamen für den Sektor E
@dataclass
class E30:
    # Klassenvariablen für E
    e: EColVars2030 = EColVars2030()
    g: EColVars2030 = EColVars2030()
    g_grid_offshore: EColVars2030 = EColVars2030()
    g_grid_onshore: EColVars2030 = EColVars2030()
    g_grid_pv: EColVars2030 = EColVars2030()
    d: EColVars2030 = EColVars2030()
    d_r: EColVars2030 = EColVars2030()
    d_b: EColVars2030 = EColVars2030()
    d_h: EColVars2030 = EColVars2030()
    d_i: EColVars2030 = EColVars2030()
    d_t: EColVars2030 = EColVars2030()
    d_a: EColVars2030 = EColVars2030()
    d_f_hydrogen_reconv: EColVars2030 = EColVars2030()
    d_e_hydrogen: EColVars2030 = EColVars2030()
    d_e_hydrogen_local: EColVars2030 = EColVars2030()
    d_f_wo_hydrogen: EColVars2030 = EColVars2030()
    p: EColVars2030 = EColVars2030()
    p_fossil_and_renew: EColVars2030 = EColVars2030()
    p_fossil: EColVars2030 = EColVars2030()
    p_fossil_nuclear: EColVars2030 = EColVars2030()
    p_fossil_coal_brown: EColVars2030 = EColVars2030()
    p_fossil_coal_brown_cogen: EColVars2030 = EColVars2030()
    p_fossil_coal_black: EColVars2030 = EColVars2030()
    p_fossil_coal_black_cogen: EColVars2030 = EColVars2030()
    p_fossil_gas: EColVars2030 = EColVars2030()
    p_fossil_gas_cogen: EColVars2030 = EColVars2030()
    p_fossil_ofossil: EColVars2030 = EColVars2030()
    p_fossil_ofossil_cogen: EColVars2030 = EColVars2030()
    p_renew: EColVars2030 = EColVars2030()
    p_renew_pv: EColVars2030 = EColVars2030()
    p_renew_pv_roof: EColVars2030 = EColVars2030()
    p_renew_pv_facade: EColVars2030 = EColVars2030()
    p_renew_pv_park: EColVars2030 = EColVars2030()
    p_renew_pv_agri: EColVars2030 = EColVars2030()
    p_renew_wind: EColVars2030 = EColVars2030()
    p_renew_wind_onshore: EColVars2030 = EColVars2030()
    p_renew_wind_offshore: EColVars2030 = EColVars2030()
    p_renew_biomass: EColVars2030 = EColVars2030()
    p_renew_biomass_waste: EColVars2030 = EColVars2030()
    p_renew_biomass_solid: EColVars2030 = EColVars2030()
    p_renew_biomass_gaseous: EColVars2030 = EColVars2030()
    p_renew_biomass_cogen: EColVars2030 = EColVars2030()
    p_renew_geoth: EColVars2030 = EColVars2030()
    p_renew_hydro: EColVars2030 = EColVars2030()
    p_renew_geoth_local: EColVars2030 = EColVars2030()
    p_renew_hydro_local: EColVars2030 = EColVars2030()
    p_renew_reverse: EColVars2030 = EColVars2030()

    p_local: EColVars2030 = EColVars2030()
    p_local_pv: EColVars2030 = EColVars2030()
    p_local_pv_roof: EColVars2030 = EColVars2030()
    p_local_pv_facade: EColVars2030 = EColVars2030()
    p_local_pv_park: EColVars2030 = EColVars2030()
    p_local_pv_agri: EColVars2030 = EColVars2030()
    p_local_wind_onshore: EColVars2030 = EColVars2030()
    p_local_biomass: EColVars2030 = EColVars2030()
    p_local_biomass_solid: EColVars2030 = EColVars2030()
    p_local_biomass_gaseous: EColVars2030 = EColVars2030()
    p_local_biomass_cogen: EColVars2030 = EColVars2030()
    p_local_hydro: EColVars2030 = EColVars2030()
    p_local_surplus: EColVars2030 = EColVars2030()

    # erzeuge dictionry
    def dict(self):
        return asdict(self)

    def convergence_check(self):
        edict = self.dict().copy()
        return edict
