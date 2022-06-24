from ..inputs import Inputs
from ..utils import div
from . import electricity2030_core
from .. import (
    electricity2018,
    residences2018,
    business2018,
    agri2030,
    business2030,
    fuels2030,
    heat2030,
    industry2030,
    residences2030,
    transport2030,
)

from ..electricity2018.dataclasses import FossilFuelsProduction


def calc_stop_production_by_fossil_fuels(
    inputs: Inputs, *, e18_production: electricity2018.e18.FossilFuelsProduction
) -> electricity2030_core.FossilFuelsProduction:
    """Compute what happens if we stop producing electricity from a fossil fuel."""
    fact = inputs.fact
    entries = inputs.entries

    KlimaneutraleJahre = entries.m_duration_neutral

    energy = 0
    CO2e_total_2021_estimated = e18_production.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    cost_fuel_per_MWh = e18_production.cost_fuel_per_MWh
    cost_mro_per_MWh = e18_production.cost_mro_per_MWh
    CO2e_combustion_based_per_MWh = e18_production.CO2e_combustion_based_per_MWh
    change_energy_MWh = energy - e18_production.energy
    cost_fuel = cost_fuel_per_MWh * energy / 1000000
    cost_mro = cost_mro_per_MWh * energy / 1000000
    CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
    change_energy_pct = div(change_energy_MWh, e18_production.energy)
    change_cost_energy = cost_fuel - e18_production.cost_fuel
    change_cost_mro = cost_mro - e18_production.cost_mro
    CO2e_total = CO2e_combustion_based
    cost_climate_saved = (
        (CO2e_total_2021_estimated - CO2e_combustion_based)
        * KlimaneutraleJahre
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    change_CO2e_t = CO2e_total - e18_production.CO2e_total
    change_CO2e_pct = div(change_CO2e_t, e18_production.CO2e_total)

    return electricity2030_core.FossilFuelsProduction(
        energy=energy,
        cost_fuel_per_MWh=cost_fuel_per_MWh,
        cost_fuel=cost_fuel,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
        CO2e_combustion_based=CO2e_combustion_based,
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        CO2e_total_2021_estimated=CO2e_total_2021_estimated,
        change_energy_MWh=change_energy_MWh,
        change_energy_pct=change_energy_pct,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_energy=change_cost_energy,
        change_cost_mro=change_cost_mro,
        cost_mro_per_MWh=cost_mro_per_MWh,
    )


def calc_production_renewable_geothermal(
    inputs: Inputs,
    *,
    d_energy: float,
) -> electricity2030_core.RenewableGeothermalProduction:
    ass = inputs.ass
    fact = inputs.fact
    entries = inputs.entries

    Kalkulationszeitraum = entries.m_duration_target

    p_renew_geoth = electricity2030_core.RenewableGeothermalProduction()
    p_renew_geoth.pct_energy = ass("Ass_E_P_renew_geoth_pct_of_nep_2035")
    p_renew_geoth.CO2e_total = 0
    p_renew_geoth.invest = 0
    p_renew_geoth.demand_emplo = 0
    p_renew_geoth.cost_mro_per_MWh = ass("Ass_E_P_renew_geoth_mro_per_MWh")
    p_renew_geoth.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_renew_geoth.invest_per_x = ass("Ass_E_P_renew_geoth_invest") * 1000
    p_renew_geoth.pct_of_wage = ass("Ass_E_P_constr_plant_invest_pct_of_wage_2017")
    p_renew_geoth.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_renew_geoth.emplo_existing = 0
    p_renew_geoth.power_installable = ass("Ass_E_P_renew_geoth_power_installable")
    p_renew_geoth.power_to_be_installed_pct = ass(
        "Ass_E_P_renew_geoth_power_to_be_installed_2035"
    )
    p_renew_geoth.power_installed = fact("Fact_E_P_geoth_power_installed_2018")
    p_renew_geoth.full_load_hour = fact("Fact_E_P_geoth_full_load_hours")

    p_renew_geoth.invest_pa = p_renew_geoth.invest / Kalkulationszeitraum
    p_renew_geoth.demand_emplo_new = max(
        0, p_renew_geoth.demand_emplo - p_renew_geoth.emplo_existing
    )
    p_renew_geoth.power_to_be_installed = max(
        0,
        p_renew_geoth.power_installable * p_renew_geoth.power_to_be_installed_pct
        - p_renew_geoth.power_installed,
    )
    p_renew_geoth.energy_installable = (
        p_renew_geoth.full_load_hour
        * p_renew_geoth.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_renew_geoth.invest_outside = (
        p_renew_geoth.invest * d_energy / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew_geoth.cost_wage = p_renew_geoth.invest_pa * p_renew_geoth.pct_of_wage
    p_renew_geoth.invest_pa_outside = (
        p_renew_geoth.power_to_be_installed
        * p_renew_geoth.invest_per_x
        / Kalkulationszeitraum
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew_geoth.change_CO2e_pct = 0
    p_renew_geoth.cost_climate_saved = 0
    return p_renew_geoth


def calc(
    inputs: Inputs,
    *,
    e18: electricity2018.E18,
    r18: residences2018.R18,
    b18: business2018.B18,
    a30: agri2030.A30,
    b30: business2030.B30,
    f30: fuels2030.F30,
    h30: heat2030.H30,
    i30: industry2030.I30,
    r30: residences2030.R30,
    t30: transport2030.T30,
    p_local_biomass_cogen: electricity2030_core.EColVars2030,
    p_local_biomass: electricity2030_core.EColVars2030,
) -> electricity2030_core.E30:
    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    Million = 1000000
    Kalkulationszeitraum = entries.m_duration_target
    KlimaneutraleJahre = entries.m_duration_neutral

    e30 = electricity2030_core.E30()

    e30.p_local_biomass = p_local_biomass
    e30.p_local_biomass_cogen = p_local_biomass_cogen

    e = e30.e
    g = e30.g
    g_grid_offshore = e30.g_grid_offshore
    g_grid_onshore = e30.g_grid_onshore
    g_grid_pv = e30.g_grid_pv
    d = e30.d
    d_r = e30.d_r
    d_b = e30.d_b
    d_h = e30.d_h
    d_i = e30.d_i
    d_t = e30.d_t
    d_a = e30.d_a
    d_f_hydrogen_reconv = e30.d_f_hydrogen_reconv
    d_f_wo_hydrogen = e30.d_f_wo_hydrogen

    p = e30.p
    p_fossil = e30.p_fossil
    p_fossil_gas = e30.p_fossil_gas
    p_fossil_ofossil = e30.p_fossil_ofossil
    p_renew = e30.p_renew
    p_renew_wind = e30.p_renew_wind
    p_renew_hydro = e30.p_renew_hydro
    p_renew_pv = e30.p_renew_pv
    p_renew_pv_roof = e30.p_renew_pv_roof
    p_renew_pv_facade = e30.p_renew_pv_facade
    p_renew_pv_park = e30.p_renew_pv_park
    p_renew_pv_agri = e30.p_renew_pv_agri
    p_renew_wind_onshore = e30.p_renew_wind_onshore
    p_renew_wind_offshore = e30.p_renew_wind_offshore
    p_renew_biomass = e30.p_renew_biomass
    p_renew_reverse = e30.p_renew_reverse

    p_local = e30.p_local
    p_local_pv = e30.p_local_pv
    p_local_pv_roof = e30.p_local_pv_roof
    p_local_pv_facade = e30.p_local_pv_facade
    p_local_pv_park = e30.p_local_pv_park
    p_local_pv_agri = e30.p_local_pv_agri
    p_local_wind_onshore = e30.p_local_wind_onshore

    p_local_hydro = e30.p_local_hydro
    p_local_surplus = e30.p_local_surplus
    p_fossil_and_renew = e30.p_fossil_and_renew

    g_grid_offshore.invest = 0
    g_grid_offshore.invest_per_x = ass("Ass_E_G_grid_offshore_ratio_invest_to_power")
    g_grid_offshore.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_grid_offshore.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )

    g_grid_onshore.invest_per_x = ass("Ass_E_G_grid_onshore_ratio_invest_to_power")
    g_grid_onshore.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_grid_onshore.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )

    g_grid_pv.invest_per_x = ass("Ass_E_G_grid_pv_ratio_invest_to_power")
    g_grid_pv.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_grid_pv.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )

    d_h.energy = h30.p.demand_electricity
    d_r.energy = r30.p.demand_electricity
    d_b.energy = b30.p.demand_electricity
    d_i.energy = i30.p.demand_electricity
    d_t.energy = t30.t.transport.demand_electricity
    d_a.energy = a30.p_operation.demand_electricity
    d_f_wo_hydrogen.energy = (
        f30.p_petrol.demand_electricity
        + f30.p_jetfuel.demand_electricity
        + f30.p_diesel.demand_electricity
        + f30.p_emethan.demand_electricity
        + f30.p_hydrogen.demand_electricity
    )
    d_r.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    d_b.cost_fuel_per_MWh = fact("Fact_E_D_B_cost_fuel_per_MWh_2018")
    d_i.cost_fuel_per_MWh = fact("Fact_E_D_I_cost_fuel_per_MWh_2018")
    d_t.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    d_a.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    d_h.change_energy_MWh = d_h.energy - e18.d_h.energy  #
    d_r.change_energy_MWh = d_r.energy - e18.d_r.energy
    d_b.change_energy_MWh = d_b.energy - e18.d_b.energy
    d_i.change_energy_MWh = d_i.energy - e18.d_i.energy
    d_t.change_energy_MWh = d_t.energy - e18.d_t.energy
    d_a.change_energy_MWh = d_a.energy - e18.d_a.energy
    d_f_wo_hydrogen.change_energy_MWh = d_f_wo_hydrogen.energy - 0
    d_h.change_energy_pct = div(d_h.change_energy_MWh, e18.d_h.energy)
    d_r.change_energy_pct = div(d_r.change_energy_MWh, e18.d_r.energy)
    d_b.change_energy_pct = div(d_b.change_energy_MWh, e18.d_b.energy)
    d_i.change_energy_pct = div(d_i.change_energy_MWh, e18.d_i.energy)
    d_t.change_energy_pct = div(d_t.change_energy_MWh, e18.d_t.energy)
    d_a.change_energy_pct = div(d_a.change_energy_MWh, e18.d_a.energy)
    d_f_hydrogen_reconv.energy = f30.p_hydrogen_reconv.demand_electricity

    d.energy = (
        d_h.energy
        + d_r.energy
        + d_b.energy
        + d_i.energy
        + d_t.energy
        + d_a.energy
        + d_f_wo_hydrogen.energy
        + d_f_hydrogen_reconv.energy
    )  #
    d_f_hydrogen_reconv.change_energy_MWh = (
        d_f_hydrogen_reconv.energy - e18.d_f_hydrogen_reconv.energy
    )

    d.change_energy_MWh = d.energy - e18.d.energy
    d.change_energy_pct = div(d.change_energy_MWh, e18.d.energy)
    d_h.pct_energy = div(d_h.energy, d.energy)
    d_r.pct_energy = div(d_r.energy, d.energy)
    d_b.pct_energy = div(d_b.energy, d.energy)
    d_i.pct_energy = div(d_i.energy, d.energy)
    d_t.pct_energy = div(d_t.energy, d.energy)
    d_a.pct_energy = div(d_a.energy, d.energy)
    d_f_wo_hydrogen.pct_energy = div(d_f_wo_hydrogen.energy, d.energy)
    d_f_hydrogen_reconv.pct_energy = div(d_f_hydrogen_reconv.energy, d.energy)
    d.pct_energy = (
        d_h.pct_energy
        + d_r.pct_energy
        + d_b.pct_energy
        + d_i.pct_energy
        + d_t.pct_energy
        + d_a.pct_energy
        + d_f_wo_hydrogen.pct_energy
        + d_f_hydrogen_reconv.pct_energy
    )

    p_renew.invest_pa_com = 0
    p_renew.invest_com = 0

    p_fossil_nuclear = calc_stop_production_by_fossil_fuels(
        inputs, e18_production=e18.p_fossil_nuclear
    )
    p_fossil_coal_brown = calc_stop_production_by_fossil_fuels(
        inputs, e18_production=e18.p_fossil_coal_brown
    )
    p_fossil_coal_black = calc_stop_production_by_fossil_fuels(
        inputs, e18_production=e18.p_fossil_coal_black
    )
    p_fossil_gas = calc_stop_production_by_fossil_fuels(
        inputs, e18_production=e18.p_fossil_gas
    )
    p_fossil_ofossil = calc_stop_production_by_fossil_fuels(
        inputs, e18_production=e18.p_fossil_ofossil
    )

    e30.p_fossil_nuclear = p_fossil_nuclear
    e30.p_fossil_coal_brown = p_fossil_coal_brown
    e30.p_fossil_coal_black = p_fossil_coal_black
    e30.p_fossil_gas = p_fossil_gas
    e30.p_fossil_ofossil = p_fossil_ofossil

    p_fossil.energy = (
        p_fossil_nuclear.energy
        + p_fossil_coal_brown.energy
        + p_fossil_coal_black.energy
        + p_fossil_gas.energy
        + p_fossil_ofossil.energy
    )

    p_fossil.CO2e_total_2021_estimated = (
        p_fossil_coal_brown.CO2e_total_2021_estimated
        + p_fossil_coal_black.CO2e_total_2021_estimated
        + p_fossil_gas.CO2e_total_2021_estimated
        + p_fossil_ofossil.CO2e_total_2021_estimated
    )

    p_renew_pv.pct_energy = ass("Ass_E_P_renew_pv_pct_of_nep_2035")
    p_renew_pv.CO2e_total = 0
    p_renew_pv.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )

    p_renew_wind.pct_energy = ass("Ass_E_P_renew_wind_onshore_pct_of_nep_2035") + ass(
        "Ass_E_P_renew_wind_offshore_pct_of_nep_2035"
    )
    p_renew_wind.CO2e_total = 0
    p_renew_wind.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )

    p_renew_biomass.pct_energy = ass("Ass_E_P_renew_biomass_pct_of_nep_2035")
    p_renew_biomass.CO2e_total_2021_estimated = (
        e18.p_renew_biomass.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )

    p_renew_geoth = calc_production_renewable_geothermal(inputs, d_energy=d.energy)
    e30.p_renew_geoth = p_renew_geoth

    p_renew_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")
    p_renew_hydro.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_renew_hydro.pct_energy = ass("Ass_E_P_renew_hydro_pct_of_nep_2035")  # energy
    p_renew_hydro.CO2e_total = 0

    p_renew_reverse.pct_energy = ass("Ass_E_P_renew_reverse_pct_of_nep_2035")
    p_renew_reverse.CO2e_total = 0
    p_renew_reverse.invest = 0
    p_renew_reverse.demand_emplo = 0

    p_renew_pv_roof.pct_energy = ass("Ass_E_P_renew_pv_roof_pct_of_nep_2035")

    p_renew_pv_facade.pct_energy = ass("Ass_E_P_renew_pv_facade_pct_of_nep_2035")

    p_local_pv_roof.full_load_hour = entries.e_pv_full_load_hours_sta
    p_local_pv_facade.full_load_hour = ass("Ass_E_P_local_pv_facade_full_load_hours")
    p_renew_pv_park.pct_energy = ass("Ass_E_P_renew_pv_park_pct_of_nep_2035")
    p_renew_pv_agri.pct_energy = ass("Ass_E_P_renew_pv_agri_pct_of_nep_2035")

    p_renew_wind_offshore.invest = 0
    p_renew_wind_offshore.demand_emplo = 0
    p_renew_wind_offshore.emplo_existing = 0
    p_renew_wind_offshore.pct_energy = ass(
        "Ass_E_P_renew_wind_offshore_pct_of_nep_2035"
    )
    p_renew_wind_offshore.cost_mro_per_MWh = (
        ass("Ass_E_P_renew_wind_offshore_ratio_invest_to_power_2030")
        * ass("Ass_E_P_renew_wind_offshore_mro_per_year")
        / fact("Fact_E_P_wind_offshore_full_load_hours")
        * 1000
    )
    p_renew_wind_offshore.invest_per_x = (
        ass("Ass_E_P_renew_wind_offshore_ratio_invest_to_power_2030") * 1000
    )
    p_renew_wind_offshore.pct_of_wage = ass(
        "Ass_E_P_constr_plant_invest_pct_of_wage_2017"
    )
    p_renew_wind_offshore.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_renew_wind_offshore.power_installable = ass(
        "Ass_E_P_renew_wind_offshore_power_installable"
    )
    p_renew_wind_offshore.power_to_be_installed_pct = ass(
        "Ass_E_P_renew_wind_offshore_power_to_be_installed_2035"
    )
    p_renew_wind_offshore.power_installed = fact(
        "Fact_E_P_wind_offshore_power_installed_2018"
    )
    p_renew_wind_offshore.full_load_hour = fact(
        "Fact_E_P_wind_offshore_full_load_hours"
    )
    p_renew_wind_offshore.invest_pa = (
        p_renew_wind_offshore.invest / Kalkulationszeitraum
    )
    p_renew_wind_offshore.demand_emplo_new = max(
        0, p_renew_wind_offshore.demand_emplo - p_renew_wind_offshore.emplo_existing
    )
    p_renew_wind_offshore.power_to_be_installed = max(
        0,
        p_renew_wind_offshore.power_installable
        * p_renew_wind_offshore.power_to_be_installed_pct
        - p_renew_wind_offshore.power_installed,
    )
    p_renew_wind_offshore.energy_installable = (
        p_renew_wind_offshore.full_load_hour
        * p_renew_wind_offshore.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )

    p_renew_wind_onshore.pct_energy = ass("Ass_E_P_renew_wind_onshore_pct_of_nep_2035")
    p_renew_wind_onshore.cost_mro_per_MWh = (
        ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_wind_onshore_mro_per_year")
        / fact("Fact_E_P_wind_onshore_full_load_hours")
        * 1000
    )

    p_renew_biomass.cost_fuel_per_MWh = ass(
        "Ass_E_P_local_biomass_material_costs"
    ) / ass("Ass_E_P_local_biomass_efficiency")
    p_renew_biomass.cost_mro_per_MWh = ass("Ass_E_P_local_biomass_mro_per_MWh")
    p_renew_biomass.CO2e_combustion_based_per_MWh = (
        e18.p_renew_biomass.CO2e_combustion_based_per_MWh
    )

    p_renew_reverse.cost_mro_per_MWh = ass(
        "Ass_E_P_renew_reverse_gud_cost_mro_per_MW"
    ) / ass("Ass_E_P_renew_reverse_full_load_hours")
    p_renew_reverse.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_renew_reverse.invest_per_x = (
        ass("Ass_E_P_renew_reverse_gud_ratio_invest_to_power") * 1000
    )
    p_renew_reverse.pct_of_wage = ass("Ass_E_P_constr_plant_invest_pct_of_wage_2017")
    p_renew_reverse.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_renew_reverse.emplo_existing = 0
    p_renew_reverse.power_installed = fact("Fact_E_P_gas_power_installed_2018")
    p_renew_reverse.full_load_hour = ass("Ass_E_P_renew_reverse_full_load_hours")

    p_local_biomass.CO2e_total_2021_estimated = (
        e18.p_local_biomass.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    p_local_pv.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_local_pv.emplo_existing = (
        fact("Fact_B_P_install_elec_emplo_2017")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )

    p_local_pv_roof.power_installed = entries.e_PV_power_inst_roof
    p_local_pv_roof.invest_per_x = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2030") * 1000
    )
    p_local_pv_roof.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_roof.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_roof.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_roof
    p_local_pv_roof.area_ha_available = (
        (4 / 3)
        * (
            (
                entries.r_area_m2_1flat
                / 100
                * ass("Ass_E_P_local_pv_roof_area_building1")
                + entries.r_area_m2_2flat
                / 100
                * ass("Ass_E_P_local_pv_roof_area_building2")
                + entries.r_area_m2_3flat
                / 100
                * ass("Ass_E_P_local_pv_roof_area_buildingD")
                + entries.r_area_m2_dorm
                / 100
                * ass("Ass_E_P_local_pv_roof_area_buildingD")
            )
        )
        / 10000
    )
    p_local_pv_roof.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_roof_potential"
    )
    p_local_pv_roof.ratio_power_to_area_ha = ass(
        "Ass_E_P_local_pv_roof_ratio_power_to_area_ha"
    )
    p_local_pv_roof.power_installable = (
        p_local_pv_roof.area_ha_available
        * p_local_pv_roof.area_ha_available_pct_of_action
        * p_local_pv_roof.ratio_power_to_area_ha
    )
    p_local_pv_roof.power_to_be_installed = max(
        0,
        p_local_pv_roof.power_installable * p_local_pv_roof.power_to_be_installed_pct
        - p_local_pv_roof.power_installed,
    )
    p_local_pv_roof.energy_installable = (
        p_local_pv_roof.power_installable
        * p_local_pv_roof.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_roof.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / p_local_pv_roof.full_load_hour
        * 1000
    )
    p_local_pv_roof.energy = (
        (p_local_pv_roof.power_to_be_installed + p_local_pv_roof.power_installed)
        * p_local_pv_roof.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_roof.invest = (
        p_local_pv_roof.power_to_be_installed * p_local_pv_roof.invest_per_x
    )

    p_local_pv_facade.power_installed = entries.e_PV_power_inst_facade
    p_local_pv_facade.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / ass("Ass_E_P_local_pv_facade_full_load_hours")
        * 1000
    )
    p_local_pv_facade.invest_per_x = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power") * 1000
    )
    p_local_pv_facade.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_facade.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_facade.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_facade
    p_local_pv_facade.ratio_power_to_area_ha = ass(
        "Ass_E_P_local_pv_facade_ratio_power_to_area_ha"
    )
    p_local_pv_facade.area_ha_available = (
        ass("Ass_E_P_lcoal_pv_facade_potential")
        * entries.r_buildings_com
        / entries.r_buildings_nat
    )
    p_local_pv_facade.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_facade_potential_usable"
    )
    p_local_pv_facade.power_installable = (
        p_local_pv_facade.ratio_power_to_area_ha
        * p_local_pv_facade.area_ha_available
        * p_local_pv_facade.area_ha_available_pct_of_action
    )
    p_local_pv_facade.power_to_be_installed = max(
        0,
        p_local_pv_facade.power_installable
        * p_local_pv_facade.power_to_be_installed_pct
        - p_local_pv_facade.power_installed,
    )
    p_local_pv_facade.energy_installable = (
        p_local_pv_facade.full_load_hour
        * p_local_pv_facade.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )

    p_local_pv_park.power_installed = entries.e_PV_power_inst_park
    p_local_pv_park.invest_per_x = (
        ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2030") * 1000
    )
    p_local_pv_park.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_park.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_park.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_park
    p_local_pv_park.ratio_power_to_area_ha = ass("Ass_E_P_local_pv_park_power_per_ha")
    p_local_pv_park.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_park_area_pct_of_available"
    )
    p_local_pv_park.area_ha_available = entries.m_area_total_com
    p_local_pv_park.power_installable = (
        p_local_pv_park.ratio_power_to_area_ha
        * p_local_pv_park.area_ha_available_pct_of_action
        * p_local_pv_park.area_ha_available
    )
    p_local_pv_park.full_load_hour = p_local_pv_roof.full_load_hour
    p_local_pv_park.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_pv_park_mro_per_year")
        / p_local_pv_park.full_load_hour
        * 1000
    )
    p_local_pv_park.power_to_be_installed = max(
        0,
        p_local_pv_park.power_installable * p_local_pv_park.power_to_be_installed_pct
        - p_local_pv_park.power_installed,
    )
    p_local_pv_park.energy_installable = (
        p_local_pv_park.full_load_hour
        * p_local_pv_park.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_park.energy = (
        (p_local_pv_park.power_to_be_installed + p_local_pv_park.power_installed)
        * p_local_pv_park.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_park.invest = (
        p_local_pv_park.power_to_be_installed * p_local_pv_park.invest_per_x
    )
    p_local_pv_park.cost_mro = (
        p_local_pv_park.energy * p_local_pv_park.cost_mro_per_MWh / Million
    )
    p_local_pv_park.change_energy_MWh = (
        p_local_pv_park.energy - e18.p_local_pv_park.energy
    )
    p_local_pv_park.invest_pa = p_local_pv_park.invest / Kalkulationszeitraum
    p_local_pv_park.change_cost_mro = (
        p_local_pv_park.cost_mro - e18.p_local_pv_park.cost_mro
    )
    p_local_pv_park.change_energy_pct = div(
        p_local_pv_park.change_energy_MWh, e18.p_local_pv_park.energy
    )
    p_local_pv_park.cost_wage = p_local_pv_park.invest_pa * p_local_pv_park.pct_of_wage

    p_local_pv_agri.power_installed = entries.e_PV_power_inst_agripv
    p_local_pv_agri.invest_per_x = (
        ass("Ass_E_P_local_pv_agri_ratio_invest_to_power") * 1000
    )
    p_local_pv_agri.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_agri.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_agri.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_agri
    p_local_pv_agri.ratio_power_to_area_ha = ass("Ass_E_P_local_pv_agri_power_per_ha")
    p_local_pv_agri.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_agri_power_installable"
    ) / (ass("Ass_E_P_local_pv_agri_power_per_ha") * entries.m_area_agri_nat)
    p_local_pv_agri.area_ha_available = entries.m_area_agri_com
    p_local_pv_agri.full_load_hour = p_local_pv_roof.full_load_hour
    p_local_pv_agri.power_installable = (
        p_local_pv_agri.ratio_power_to_area_ha
        * p_local_pv_agri.area_ha_available_pct_of_action
        * p_local_pv_agri.area_ha_available
    )
    p_local_pv_agri.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_agri_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_agri_mro_per_year")
        / p_local_pv_park.full_load_hour
        * 1000
    )
    p_local_pv_agri.power_to_be_installed = max(
        0,
        p_local_pv_agri.power_installable * p_local_pv_agri.power_to_be_installed_pct
        - p_local_pv_agri.power_installed,
    )
    p_local_pv_agri.energy_installable = (
        p_local_pv_agri.full_load_hour
        * p_local_pv_agri.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_agri.energy = (
        (p_local_pv_agri.power_to_be_installed + p_local_pv_agri.power_installed)
        * p_local_pv_agri.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_agri.invest = (
        p_local_pv_agri.power_to_be_installed * p_local_pv_agri.invest_per_x
    )
    p_local_pv_agri.cost_mro = (
        p_local_pv_agri.energy * p_local_pv_agri.cost_mro_per_MWh / Million
    )
    p_local_pv_agri.change_energy_MWh = (
        p_local_pv_agri.energy - e18.p_local_pv_agri.energy
    )
    p_local_pv_agri.invest_pa = p_local_pv_agri.invest / Kalkulationszeitraum
    p_local_pv_agri.change_cost_mro = (
        p_local_pv_agri.cost_mro - e18.p_local_pv_agri.cost_mro
    )
    p_local_pv_agri.change_energy_pct = div(
        p_local_pv_agri.change_energy_MWh, e18.p_local_pv_agri.energy
    )
    p_local_pv_agri.cost_wage = p_local_pv_agri.invest_pa * p_local_pv_agri.pct_of_wage

    p_local_wind_onshore.power_installed = entries.e_PV_power_inst_wind_on
    p_local_wind_onshore.full_load_hour = fact("Fact_E_P_wind_onshore_full_load_hours")
    p_local_wind_onshore.cost_mro_per_MWh = (
        ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_wind_onshore_mro_per_year")
        / fact("Fact_E_P_wind_onshore_full_load_hours")
        * 1000
    )
    p_local_wind_onshore.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_local_wind_onshore.invest_per_x = (
        ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2030") * 1000
    )
    p_local_wind_onshore.pct_of_wage = ass(
        "Ass_E_P_constr_plant_invest_pct_of_wage_2017"
    )
    p_local_wind_onshore.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_wind_onshore.emplo_existing = (
        fact("Fact_E_P_wind_onshore_emplo_2018")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )
    p_local_wind_onshore.power_to_be_installed_pct = (
        entries.e_PV_power_to_be_inst_local_wind_onshore
    )
    p_local_wind_onshore.ratio_power_to_area_ha = (
        entries.e_local_wind_onshore_ratio_power_to_area_sta
    )
    p_local_wind_onshore.area_ha_available = (
        entries.m_area_agri_com + entries.m_area_wood_com
    )
    p_local_wind_onshore.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_wind_onshore_pct_action"
    )

    p_local_biomass.cost_fuel_per_MWh = ass(
        "Ass_E_P_local_biomass_material_costs"
    ) / ass("Ass_E_P_local_biomass_efficiency")
    p_local_biomass.cost_mro_per_MWh = ass("Ass_E_P_local_biomass_mro_per_MWh")
    p_local_biomass.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_biomass_ratio_CO2e_cb_nonCO2_to_gep_2018"
    ) / (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    p_local_biomass.invest_per_x = ass(
        "Ass_E_P_local_biomass_ratio_invest_to_power"
    )  # invest
    p_local_biomass.pct_of_wage = ass(
        "Ass_E_P_constr_plant_invest_pct_of_wage_2017"
    )  # cost_wage
    p_local_biomass.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )  # demand_emplo
    p_local_biomass.emplo_existing = (
        fact("Fact_E_P_biomass_emplo_2018")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )
    p_local_biomass.energy_installable = (
        p_local_biomass.power_installable
        * p_local_biomass.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_biomass.cost_fuel = (
        p_local_biomass.cost_fuel_per_MWh * p_local_biomass.energy / Million
    )
    p_local_biomass.cost_mro = (
        p_local_biomass.energy * p_local_biomass.cost_mro_per_MWh / Million
    )
    p_local_biomass.CO2e_combustion_based = (
        p_local_biomass.energy * p_local_biomass.CO2e_combustion_based_per_MWh
    )
    p_local_biomass.change_energy_MWh = (
        p_local_biomass.energy - e18.p_local_biomass.energy
    )
    p_local_biomass.invest = (
        p_local_biomass.power_to_be_installed * p_local_biomass.invest_per_x
    )
    p_local_biomass.invest_pa = p_local_biomass.invest / Kalkulationszeitraum
    p_local_biomass.change_cost_energy = (
        p_local_biomass.cost_fuel - e18.p_local_biomass.cost_fuel
    )
    p_local_biomass.change_cost_mro = (
        p_local_biomass.cost_mro - e18.p_local_biomass.cost_mro
    )
    p_local_biomass.CO2e_total = p_local_biomass.CO2e_combustion_based
    p_local_biomass.cost_climate_saved = (
        (
            p_local_biomass.CO2e_total_2021_estimated
            - p_local_biomass.CO2e_combustion_based
        )
        * KlimaneutraleJahre
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_local_biomass.cost_wage = (
        p_local_biomass.invest_pa * p_local_biomass.pct_of_wage / Kalkulationszeitraum
    )
    p_local_biomass.change_CO2e_t = p_local_biomass.CO2e_total - 0
    p_local_biomass.demand_emplo = div(
        p_local_biomass.cost_wage, p_local_biomass.ratio_wage_to_emplo
    )

    p_local_hydro.power_installed = entries.e_PV_power_inst_water
    p_local_hydro.full_load_hour = fact("Fact_E_P_hydro_full_load_hours")  # energy
    p_local_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")  # cost_mro
    p_local_hydro.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_local_hydro.energy = (
        p_local_hydro.power_installed
        * p_local_hydro.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_hydro.cost_mro = (
        p_local_hydro.energy * p_local_hydro.cost_mro_per_MWh / Million
    )
    p_local_hydro.CO2e_combustion_based = (
        p_local_hydro.energy * p_local_hydro.CO2e_combustion_based_per_MWh
    )
    p_local_hydro.CO2e_total = p_local_hydro.CO2e_combustion_based
    p_local_hydro.change_energy_MWh = p_local_hydro.energy - e18.p_local_hydro.energy
    p_local_hydro.change_CO2e_t = 0
    p_local_hydro.change_CO2e_pct = 0
    p_local_hydro.cost_climate_saved = 0

    g_grid_offshore.cost_mro = (
        g_grid_offshore.invest * ass("Ass_E_G_grid_offshore_mro") / Million
    )
    g_grid_offshore.invest_pa = g_grid_offshore.invest / entries.m_duration_target
    p_fossil_and_renew.invest_pa_com = p_renew.invest_pa_com
    p_fossil_and_renew.invest_com = p_renew.invest_com
    p_renew.pct_energy = (
        p_renew_pv.pct_energy
        + p_renew_wind.pct_energy
        + p_renew_biomass.pct_energy
        + p_renew_geoth.pct_energy
        + p_renew_hydro.pct_energy
        + p_renew_reverse.pct_energy
    )
    p_renew.CO2e_total_2021_estimated = p_renew_biomass.CO2e_total_2021_estimated
    p_renew_reverse.invest_pa = p_renew_reverse.invest / Kalkulationszeitraum
    p_renew_reverse.demand_emplo_new = p_renew_reverse.demand_emplo
    p_renew_pv_roof.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / p_local_pv_roof.full_load_hour
        * 1000
    )
    p_renew_pv_facade.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / p_local_pv_facade.full_load_hour
        * 1000
    )
    p_renew_wind.invest = p_renew_wind_offshore.invest
    p_renew_wind.demand_emplo = p_renew_wind_offshore.demand_emplo
    p_renew_wind.emplo_existing = p_renew_wind_offshore.emplo_existing
    p_renew_reverse.power_to_be_installed = max(
        0,
        ass("Ass_E_P_renew_reverse_addon_to_demand_2035")
        * ass("Ass_E_P_renew_nep_total_2035")
        / ass("Ass_E_P_renew_reverse_full_load_hours")
        - p_renew_reverse.power_installed,
    )
    p_local.CO2e_total_2021_estimated = p_local_biomass.CO2e_total_2021_estimated
    p_local_pv.power_installed = (
        p_local_pv_roof.power_installed
        + p_local_pv_facade.power_installed
        + p_local_pv_park.power_installed
        + p_local_pv_agri.power_installed
    )  #

    p_local_wind_onshore.power_installable = (
        p_local_wind_onshore.ratio_power_to_area_ha
        * p_local_wind_onshore.area_ha_available
        * p_local_wind_onshore.area_ha_available_pct_of_action
    )

    g_grid_offshore.cost_wage = g_grid_offshore.invest_pa * g_grid_offshore.pct_of_wage

    p_renew_reverse.invest_outside = (
        p_renew_reverse.invest * d.energy / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_fossil.change_energy_MWh = p_fossil.energy - e18.p_fossil.energy

    p_fossil.cost_fuel = (
        p_fossil_nuclear.cost_fuel
        + p_fossil_coal_brown.cost_fuel
        + p_fossil_coal_black.cost_fuel
        + p_fossil_gas.cost_fuel
        + p_fossil_ofossil.cost_fuel
    )
    p_fossil.cost_mro = (
        p_fossil_nuclear.cost_mro
        + p_fossil_coal_brown.cost_mro
        + p_fossil_gas.cost_mro
        + p_fossil_ofossil.cost_mro
    )
    p_fossil.CO2e_combustion_based = (
        p_fossil_nuclear.CO2e_combustion_based
        + p_fossil_coal_brown.CO2e_combustion_based
        + p_fossil_coal_black.CO2e_combustion_based
        + p_fossil_gas.CO2e_combustion_based
        + p_fossil_ofossil.CO2e_combustion_based
    )
    p_fossil_and_renew.CO2e_total_2021_estimated = (
        p_fossil.CO2e_total_2021_estimated + p_renew.CO2e_total_2021_estimated
    )
    p_renew_reverse.cost_wage = p_renew_reverse.invest_pa * p_renew_reverse.pct_of_wage
    p_renew_pv_park.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_pv_park_mro_per_year")
        / p_local_pv_park.full_load_hour
        * 1000
    )
    p_renew_pv_agri.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_agri_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / p_local_pv_agri.full_load_hour
        * 1000
    )
    p_renew.invest = p_renew_wind.invest + p_renew_geoth.invest + p_renew_reverse.invest
    p_renew_wind.invest_pa = p_renew_wind_offshore.invest_pa
    p_renew_wind_offshore.cost_wage = (
        p_renew_wind_offshore.invest_pa
        * p_renew_wind_offshore.pct_of_wage
        / Kalkulationszeitraum
    )
    p_renew_wind_offshore.invest_pa_outside = (
        p_renew_wind_offshore.power_to_be_installed
        * p_renew_wind_offshore.invest_per_x
        / Kalkulationszeitraum
        * d.energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew_wind_offshore.invest_outside = (
        p_renew_wind_offshore.power_to_be_installed
        * p_renew_wind_offshore.invest_per_x
        * d.energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew.demand_emplo = (
        p_renew_wind.demand_emplo
        + p_renew_geoth.demand_emplo
        + p_renew_reverse.demand_emplo
    )
    p_renew_wind.demand_emplo_new = max(
        0, p_renew_wind.demand_emplo - p_renew_wind.emplo_existing
    )
    g_grid_offshore.power_to_be_installed = p_renew_wind_offshore.power_to_be_installed
    p_renew_reverse.invest_pa_outside = (
        p_renew_reverse.power_to_be_installed
        * p_renew_reverse.invest_per_x
        / entries.m_duration_target
        * d.energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )

    p_local_wind_onshore.power_to_be_installed = max(
        0,
        p_local_wind_onshore.power_installable
        * p_local_wind_onshore.power_to_be_installed_pct
        - p_local_wind_onshore.power_installed,
    )
    p_local_wind_onshore.energy_installable = (
        p_local_wind_onshore.full_load_hour
        * p_local_wind_onshore.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )

    p_local_pv.power_installable = (
        p_local_pv_roof.power_installable
        + p_local_pv_facade.power_installable
        + p_local_pv_park.power_installable
        + p_local_pv_agri.power_installable
    )

    g_grid_offshore.demand_emplo = div(
        g_grid_offshore.cost_wage, g_grid_offshore.ratio_wage_to_emplo
    )
    p_fossil.change_energy_pct = div(p_fossil.change_energy_MWh, e18.p_fossil.energy)
    # p_fossil_coal_brown.change_CO2e_t = (
    #    p_fossil_coal_brown.CO2e_total - e18.p_fossil_coal_brown.CO2e_total
    # )
    # p_fossil_coal_brown.change_CO2e_pct = div(
    #    p_fossil_coal_brown.change_CO2e_t, e18.p_fossil_coal_brown.CO2e_total
    # )
    # p_fossil_coal_black.change_CO2e_t = (
    #    p_fossil_coal_black.CO2e_total - e18.p_fossil_coal_black.CO2e_total
    # )
    # p_fossil_coal_black.change_CO2e_pct = div(
    #    p_fossil_coal_black.change_CO2e_t, e18.p_fossil_coal_black.CO2e_total
    # )
    p_fossil.change_cost_energy = (
        p_fossil_nuclear.change_cost_energy
        + p_fossil_coal_brown.change_cost_energy
        + p_fossil_coal_black.change_cost_energy
        + p_fossil_gas.change_cost_energy
        + p_fossil_ofossil.change_cost_energy
    )
    p_fossil.change_cost_mro = (
        p_fossil_nuclear.change_cost_energy
        + p_fossil_coal_brown.change_cost_mro
        + p_fossil_coal_black.change_cost_mro
        + p_fossil_gas.change_cost_mro
        + p_fossil_ofossil.change_cost_mro
    )
    p_fossil.cost_climate_saved = (
        p_fossil_coal_brown.cost_climate_saved
        + p_fossil_coal_black.cost_climate_saved
        + p_fossil_gas.cost_climate_saved
        + p_fossil_ofossil.cost_climate_saved
    )
    p.CO2e_total_2021_estimated = (
        p_fossil_and_renew.CO2e_total_2021_estimated + p_local.CO2e_total_2021_estimated
    )
    p_fossil_and_renew.invest = p_renew.invest
    p_renew.invest_pa = (
        p_renew_wind.invest_pa + p_renew_geoth.invest_pa + p_renew_reverse.invest_pa
    )
    p_renew_wind.cost_wage = p_renew_wind_offshore.cost_wage
    p_fossil_and_renew.demand_emplo = p_renew.demand_emplo
    p_renew.demand_emplo_new = (
        p_renew_wind.demand_emplo_new
        + p_renew_geoth.demand_emplo_new
        + p_renew_reverse.demand_emplo_new
    )
    g_grid_offshore.invest_outside = (
        g_grid_offshore.power_to_be_installed
        * g_grid_offshore.invest_per_x
        * d.energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew_wind.invest_pa_outside = p_renew_wind_offshore.invest_pa_outside
    p_renew_wind.invest_outside = p_renew_wind_offshore.invest_outside
    p_local_pv_facade.energy = (
        (p_local_pv_facade.power_to_be_installed + p_local_pv_facade.power_installed)
        * p_local_pv_facade.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_facade.invest = (
        p_local_pv_facade.power_to_be_installed * p_local_pv_facade.invest_per_x
    )

    p_local_pv.power_to_be_installed = (
        p_local_pv_roof.power_to_be_installed
        + p_local_pv_facade.power_to_be_installed
        + p_local_pv_park.power_to_be_installed
        + p_local_pv_agri.power_to_be_installed
    )
    p_local_pv.energy_installable = (
        p_local_pv_roof.energy_installable
        + p_local_pv_facade.energy_installable
        + p_local_pv_park.energy_installable
        + p_local_pv_agri.energy_installable
    )
    g_grid_onshore.power_to_be_installed = p_local_wind_onshore.power_to_be_installed

    p_local_wind_onshore.energy = (
        (
            p_local_wind_onshore.power_to_be_installed
            + p_local_wind_onshore.power_installed
        )
        * p_local_wind_onshore.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_wind_onshore.invest = (
        p_local_wind_onshore.power_to_be_installed * p_local_wind_onshore.invest_per_x
    )

    g_grid_offshore.demand_emplo_new = g_grid_offshore.demand_emplo
    p_fossil.change_CO2e_t = (
        p_fossil_nuclear.change_CO2e_t
        + p_fossil_coal_brown.change_CO2e_t
        + p_fossil_coal_black.change_CO2e_t
        + p_fossil_gas.change_CO2e_t
        + p_fossil_ofossil.change_CO2e_t
    )
    p_fossil.change_CO2e_pct = div(p_fossil.change_CO2e_t, e18.p_fossil.CO2e_total)
    e.CO2e_total_2021_estimated = p.CO2e_total_2021_estimated
    p_fossil_and_renew.invest_pa = p_renew.invest_pa
    p_renew.cost_wage = (
        p_renew_wind.cost_wage + p_renew_geoth.cost_wage + p_renew_reverse.cost_wage
    )
    p_fossil_and_renew.demand_emplo_new = p_renew.demand_emplo_new
    g.invest_outside = g_grid_offshore.invest_outside
    g_grid_offshore.invest_pa_outside = (
        g_grid_offshore.invest_outside / entries.m_duration_target
    )
    p_renew.invest_pa_outside = (
        p_renew_wind.invest_pa_outside
        + p_renew_geoth.invest_pa_outside
        + p_renew_reverse.invest_pa_outside
    )
    p_renew.invest_outside = (
        p_renew_wind.invest_outside
        + p_renew_geoth.invest_outside
        + p_renew_reverse.invest_outside
    )
    p_local_pv_roof.cost_mro = (
        p_local_pv_roof.energy * p_local_pv_roof.cost_mro_per_MWh / Million
    )
    p_local_pv_roof.change_energy_MWh = (
        p_local_pv_roof.energy - e18.p_local_pv_roof.energy
    )
    p_local_pv_roof.invest_pa = p_local_pv_roof.invest / Kalkulationszeitraum
    p_local_pv_roof.invest_com = div(
        p_local_pv_roof.invest
        * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2),
        b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2,
    )
    p_local_pv_facade.cost_mro = (
        p_local_pv_facade.energy * p_local_pv_facade.cost_mro_per_MWh / Million
    )
    p_local_pv_facade.change_energy_MWh = (
        p_local_pv_facade.energy - e18.p_local_pv_facade.energy
    )
    p_local_pv_facade.invest_pa = p_local_pv_facade.invest / Kalkulationszeitraum
    p_local_pv_facade.invest_com = div(
        p_local_pv_facade.invest
        * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2),
        b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2,
    )
    g_grid_pv.power_to_be_installed = p_local_pv.power_to_be_installed
    p_local_pv.energy = (
        p_local_pv_roof.energy
        + p_local_pv_facade.energy
        + p_local_pv_park.energy
        + p_local_pv_agri.energy
    )  #

    p_local_pv.invest = (
        p_local_pv_roof.invest
        + p_local_pv_facade.invest
        + p_local_pv_park.invest
        + p_local_pv_agri.invest
    )  #
    g_grid_onshore.invest = (
        g_grid_onshore.power_to_be_installed * g_grid_onshore.invest_per_x
    )
    p_local_wind_onshore.cost_mro = (
        p_local_wind_onshore.energy * p_local_wind_onshore.cost_mro_per_MWh / Million
    )
    p_local_wind_onshore.CO2e_combustion_based = (
        p_local_wind_onshore.energy * p_local_wind_onshore.CO2e_combustion_based_per_MWh
    )
    p_local_wind_onshore.CO2e_total = p_local_wind_onshore.CO2e_combustion_based

    p_local_wind_onshore.change_energy_MWh = (
        p_local_wind_onshore.energy - e18.p_local_wind_onshore.energy
    )

    p_local.invest = (
        p_local_pv_roof.invest
        + p_local_pv_facade.invest
        + p_local_pv_park.invest
        + p_local_pv_agri.invest
        + p_local_wind_onshore.invest
        + p_local_biomass.invest
    )
    p_local_wind_onshore.invest_pa = p_local_wind_onshore.invest / Kalkulationszeitraum
    p_local.cost_fuel = p_local_biomass.cost_fuel
    p_fossil_and_renew.cost_wage = p_renew.cost_wage
    g.invest_pa_outside = g_grid_offshore.invest_pa_outside
    p_fossil_and_renew.invest_pa_outside = p_renew.invest_pa_outside
    p_fossil_and_renew.invest_outside = p_renew.invest_outside
    p_local_pv_roof.change_cost_mro = (
        p_local_pv_roof.cost_mro - e18.p_local_pv_roof.cost_mro
    )
    p_local_pv_roof.change_energy_pct = div(
        p_local_pv_roof.change_energy_MWh, e18.p_local_pv_roof.energy
    )
    p_local_pv_roof.cost_wage = p_local_pv_roof.invest_pa * p_local_pv_roof.pct_of_wage
    p_local_pv_roof.invest_pa_com = p_local_pv_roof.invest_com / Kalkulationszeitraum
    p_local_pv_facade.change_cost_mro = (
        p_local_pv_facade.cost_mro - e18.p_local_pv_facade.cost_mro
    )
    p_local_pv_facade.change_energy_pct = div(
        p_local_pv_facade.change_energy_MWh, e18.p_local_pv_facade.energy
    )
    p_local_pv_facade.cost_wage = (
        p_local_pv_facade.invest_pa * p_local_pv_facade.pct_of_wage
    )
    p_local_pv.invest_com = p_local_pv_roof.invest_com + p_local_pv_facade.invest_com
    p_local_pv_facade.invest_pa_com = (
        p_local_pv_facade.invest_com / Kalkulationszeitraum
    )
    g_grid_pv.invest = g_grid_pv.power_to_be_installed * g_grid_pv.invest_per_x
    p_local.energy = (
        p_local_pv.energy
        + p_local_wind_onshore.energy
        + p_local_biomass.energy
        + p_local_hydro.energy
    )
    p_local_pv.CO2e_combustion_based = (
        p_local_pv.energy * p_local_pv.CO2e_combustion_based_per_MWh
    )
    p_local_pv.CO2e_total = p_local_pv.CO2e_combustion_based
    p_local_pv.change_CO2e_t = p_local_pv.CO2e_total - e18.p_local_pv.CO2e_total

    p_local_pv.change_energy_MWh = p_local_pv.energy - e18.p_local_pv.energy
    p_local_pv_roof.pct_energy = div(p_local_pv_roof.energy, p_local_pv.energy)
    p_local_pv_roof.pet_sites = div(p_local_pv_roof.energy, p_local_pv.energy)
    p_local_pv_facade.pct_energy = div(p_local_pv_facade.energy, p_local_pv.energy)
    p_local_pv_facade.pet_sites = div(p_local_pv_facade.energy, p_local_pv.energy)
    p_local_pv_park.pct_energy = div(p_local_pv_park.energy, p_local_pv.energy)
    p_local_pv_park.pet_sites = div(p_local_pv_park.energy, p_local_pv.energy)
    p_local_pv_agri.pct_energy = div(p_local_pv_agri.energy, p_local_pv.energy)
    p_local_pv_agri.pet_sites = div(p_local_pv_agri.energy, p_local_pv.energy)
    p_local_pv.cost_mro = (
        p_local_pv_roof.cost_mro
        + p_local_pv_facade.cost_mro
        + p_local_pv_park.cost_mro
        + p_local_pv_agri.cost_mro
    )  #

    p_local_pv.invest_pa = (
        p_local_pv_roof.invest_pa
        + p_local_pv_facade.invest_pa
        + p_local_pv_park.invest_pa
        + p_local_pv_agri.invest_pa
    )  # (
    g_grid_onshore.cost_mro = (
        g_grid_onshore.invest * ass("Ass_E_G_grid_onshore_mro") / Million
    )
    g_grid_onshore.invest_pa = g_grid_onshore.invest / entries.m_duration_target
    p_local_wind_onshore.change_cost_mro = (
        p_local_wind_onshore.cost_mro - e18.p_local_wind_onshore.cost_mro
    )
    p_local_wind_onshore.change_energy_pct = div(
        p_local_wind_onshore.change_energy_MWh, e18.p_local_wind_onshore.energy
    )
    p.invest = p_fossil_and_renew.invest + p_local.invest
    p_local.invest_pa = (
        p_local_pv_roof.invest_pa
        + p_local_pv_facade.invest_pa
        + p_local_pv_park.invest_pa
        + p_local_pv_agri.invest_pa
        + p_local_wind_onshore.invest_pa
        + p_local_biomass.invest_pa
    )  #
    p_local_wind_onshore.cost_wage = (
        p_local_wind_onshore.invest_pa * p_local_wind_onshore.pct_of_wage
    )
    p_local.change_cost_energy = p_local_biomass.change_cost_energy
    p_local.change_cost_mro = p_local_biomass.change_cost_mro
    p_local.cost_climate_saved = p_local_biomass.cost_climate_saved
    p.invest_pa_outside = p_fossil_and_renew.invest_pa_outside
    p.invest_outside = p_fossil_and_renew.invest_outside
    p_local_pv_roof.demand_emplo = div(
        p_local_pv_roof.cost_wage, p_local_pv_roof.ratio_wage_to_emplo
    )
    p_local_pv_facade.demand_emplo = div(
        p_local_pv_facade.cost_wage, p_local_pv_facade.ratio_wage_to_emplo
    )
    p_local.invest_com = p_local_pv.invest_com
    p_local_pv_agri.invest_pa_com = 0
    p_local.invest_pa_com = (
        p_local_pv_roof.invest_pa_com
        + p_local_pv_facade.invest_pa_com
        + p_local_pv_agri.invest_pa_com
    )  #
    p_local_pv.invest_pa_com = (
        p_local_pv_roof.invest_pa_com
        + p_local_pv_facade.invest_pa_com
        + p_local_pv_agri.invest_pa_com
    )  #
    p_local_pv_park.demand_emplo = div(
        p_local_pv_park.cost_wage, p_local_pv_park.ratio_wage_to_emplo
    )
    g.invest = g_grid_offshore.invest + g_grid_onshore.invest + g_grid_pv.invest
    g_grid_pv.cost_mro = g_grid_pv.invest * ass("Ass_E_G_grid_pv_mro") / Million
    g_grid_pv.invest_pa = g_grid_pv.invest / entries.m_duration_target
    p_local.change_energy_MWh = p_local.energy - e18.p_local.energy
    p_local_pv.pct_energy = div(p_local_pv.energy, p_local.energy)
    p_local_wind_onshore.pct_energy = div(p_local_wind_onshore.energy, p_local.energy)
    p_local_biomass.pct_energy = div(p_local_biomass.energy, p_local.energy)
    p_local_hydro.pct_energy = div(p_local_hydro.energy, p_local.energy)
    p_local_surplus.energy = p_local.energy - d.energy

    p_local.CO2e_combustion_based = (
        p_local_pv.CO2e_combustion_based
        + p_local_wind_onshore.CO2e_combustion_based
        + p_local_biomass.CO2e_combustion_based
        + p_local_hydro.CO2e_combustion_based
    )
    p_local_pv.change_energy_pct = div(
        p_local_pv.change_energy_MWh, e18.p_local_pv.energy
    )
    p_local.cost_mro = (
        p_local_pv.cost_mro
        + p_local_wind_onshore.cost_mro
        + p_local_biomass.cost_mro
        + p_local_hydro.cost_mro
    )
    p_local_pv.change_cost_mro = p_local_pv.cost_mro - e18.p_local_pv.cost_mro
    p_local_pv.cost_wage = (
        p_local_pv_roof.cost_wage
        + p_local_pv_facade.cost_wage
        + p_local_pv_park.cost_wage
        + p_local_pv_agri.cost_wage
    )
    p_local_pv_agri.demand_emplo = div(
        p_local_pv_agri.cost_wage, p_local_pv_agri.ratio_wage_to_emplo
    )
    g_grid_onshore.cost_wage = g_grid_onshore.invest_pa * g_grid_onshore.pct_of_wage
    p.invest_pa = p_fossil_and_renew.invest_pa + p_local.invest_pa
    p_local_wind_onshore.demand_emplo = div(
        p_local_wind_onshore.cost_wage, p_local_wind_onshore.ratio_wage_to_emplo
    )
    p_local.change_CO2e_t = p_local_biomass.change_CO2e_t
    p_local_biomass.demand_emplo_new = max(
        0, p_local_biomass.demand_emplo - p_local_biomass.emplo_existing
    )
    e.invest_pa_outside = g.invest_pa_outside + p.invest_pa_outside
    e.invest_outside = g.invest_outside + p.invest_outside
    p.invest_com = p_fossil_and_renew.invest_com + p_local.invest_com
    p.invest_pa_com = p_fossil_and_renew.invest_pa_com + p_local.invest_pa_com
    e.invest = g.invest + p.invest
    g.invest_pa = (
        g_grid_offshore.invest_pa + g_grid_onshore.invest_pa + g_grid_pv.invest_pa
    )
    g_grid_pv.cost_wage = g_grid_pv.invest_pa * g_grid_pv.pct_of_wage
    p_local.change_energy_pct = div(p_local.change_energy_MWh, e18.p_local.energy)
    p_local.pct_energy = (
        p_local_pv.pct_energy
        + p_local_wind_onshore.pct_energy
        + p_local_biomass.pct_energy
        + p_local_hydro.pct_energy
    )

    p_renew.energy = max(0, -p_local_surplus.energy)

    p_local.CO2e_combustion_based_per_MWh = div(
        p_local.CO2e_combustion_based, p_local.energy
    )
    p_local.CO2e_total = p_local.CO2e_combustion_based  # change_energy_MWh
    p_local.cost_wage = (
        p_local_pv.cost_wage
        + p_local_wind_onshore.cost_wage
        + p_local_biomass.cost_wage
    )
    p_local_pv.demand_emplo = (
        p_local_pv_roof.demand_emplo
        + p_local_pv_facade.demand_emplo
        + p_local_pv_park.demand_emplo
        + p_local_pv_agri.demand_emplo
    )
    g_grid_onshore.demand_emplo = div(
        g_grid_onshore.cost_wage, g_grid_onshore.ratio_wage_to_emplo
    )
    p_local_wind_onshore.demand_emplo_new = max(
        0, p_local_wind_onshore.demand_emplo - p_local_wind_onshore.emplo_existing
    )
    e.invest_com = 0 + p.invest_com
    e.invest_pa_com = 0 + p.invest_pa_com
    e.invest_pa = g.invest_pa + p.invest_pa
    g.cost_wage = (
        g_grid_offshore.cost_wage + g_grid_onshore.cost_wage + g_grid_pv.cost_wage
    )
    g_grid_pv.demand_emplo = div(g_grid_pv.cost_wage, g_grid_pv.ratio_wage_to_emplo)
    p_fossil_and_renew.energy = p_renew.energy
    p_renew.change_energy_MWh = p_renew.energy - e18.p_renew.energy
    p_renew_pv.energy = p_renew.energy * p_renew_pv.pct_energy
    p_renew_wind_onshore.energy = p_renew.energy * p_renew_wind_onshore.pct_energy
    p_renew_wind_offshore.energy = p_renew.energy * p_renew_wind_offshore.pct_energy
    p_renew_biomass.energy = p_renew.energy * p_renew_biomass.pct_energy
    p_renew_geoth.energy = p_renew.energy * p_renew_geoth.pct_energy
    p_renew_hydro.energy = p_renew.energy * p_renew_hydro.pct_energy
    p_renew_reverse.energy = p_renew.energy * p_renew_reverse.pct_energy
    p.cost_wage = p_fossil_and_renew.cost_wage + p_local.cost_wage
    p_local.demand_emplo = (
        p_local_pv.demand_emplo
        + p_local_wind_onshore.demand_emplo
        + p_local_biomass.demand_emplo
    )  # emplo_existing
    p_local_pv.demand_emplo_new = max(
        0, p_local_pv.demand_emplo - p_local_pv.emplo_existing
    )
    g_grid_onshore.demand_emplo_new = g_grid_onshore.demand_emplo
    g.demand_emplo = (
        g_grid_offshore.demand_emplo
        + g_grid_onshore.demand_emplo
        + g_grid_pv.demand_emplo
    )
    g_grid_pv.demand_emplo_new = g_grid_pv.demand_emplo
    p.energy = p_fossil_and_renew.energy + p_local.energy
    p_fossil_and_renew.change_energy_MWh = (
        p_fossil_and_renew.energy - e18.p_fossil_and_renew.energy
    )  # change_energy_pct
    p_renew.change_energy_pct = div(p_renew.change_energy_MWh, e18.p_renew.energy)
    p_renew_pv.CO2e_combustion_based = (
        p_renew_pv.energy * p_renew_pv.CO2e_combustion_based_per_MWh
    )
    p_renew_pv_roof.energy = p_renew_pv.energy * p_renew_pv_roof.pct_energy
    p_renew_pv_facade.energy = p_renew_pv.energy * p_renew_pv_facade.pct_energy
    p_renew_pv_park.energy = p_renew_pv.energy * p_renew_pv_park.pct_energy
    p_renew_pv_agri.energy = p_renew_pv.energy * p_renew_pv_agri.pct_energy
    p_renew_wind_onshore.cost_mro = (
        p_renew_wind_onshore.energy * p_renew_wind_onshore.cost_mro_per_MWh / Million
    )
    p_renew_wind_onshore.change_energy_MWh = (
        p_renew_wind_onshore.energy - e18.p_renew_wind_onshore.energy
    )
    p_renew_wind.energy = p_renew_wind_onshore.energy + p_renew_wind_offshore.energy
    p_renew_wind_offshore.cost_mro = (
        p_renew_wind_offshore.energy * p_renew_wind_offshore.cost_mro_per_MWh / Million
    )
    p_renew_wind_offshore.change_energy_MWh = (
        p_renew_wind_offshore.energy - e18.p_renew_wind_offshore.energy
    )
    p_renew_biomass.cost_fuel = (
        p_renew_biomass.energy * p_renew_biomass.cost_fuel_per_MWh / Million
    )
    p_renew_biomass.cost_mro = (
        p_renew_biomass.energy * p_renew_biomass.cost_mro_per_MWh / Million
    )
    p_renew_biomass.CO2e_combustion_based = (
        p_renew_biomass.energy * p_renew_biomass.CO2e_combustion_based_per_MWh
    )
    p_renew_biomass.change_energy_MWh = (
        p_renew_biomass.energy - e18.p_renew_biomass.energy
    )
    p_renew_geoth.cost_mro = (
        p_renew_geoth.energy * p_renew_geoth.cost_mro_per_MWh / Million
    )
    p_renew_geoth.CO2e_combustion_based = (
        p_renew_geoth.energy * p_renew_geoth.CO2e_combustion_based_per_MWh
    )
    p_renew_geoth.change_energy_MWh = p_renew_geoth.energy - e18.p_renew_geoth.energy
    p_renew_hydro.cost_mro = (
        p_renew_hydro.energy * p_renew_hydro.cost_mro_per_MWh / Million
    )
    p_renew_hydro.CO2e_combustion_based = (
        p_renew_hydro.energy * p_renew_hydro.CO2e_combustion_based_per_MWh
    )
    p_renew_hydro.change_energy_MWh = p_renew_hydro.energy - e18.p_renew_hydro.energy
    p_renew_reverse.cost_mro = (
        p_renew_reverse.energy * p_renew_reverse.cost_mro_per_MWh / Million
    )
    p_renew_reverse.CO2e_combustion_based = (
        p_renew_reverse.energy * p_renew_reverse.CO2e_combustion_based_per_MWh
    )
    p_renew_reverse.change_energy_MWh = p_renew_reverse.energy
    e.cost_wage = g.cost_wage + p.cost_wage
    p.demand_emplo = p_fossil_and_renew.demand_emplo + p_local.demand_emplo
    p_local.demand_emplo_new = (
        p_local_pv.demand_emplo_new
        + p_local_wind_onshore.demand_emplo_new
        + p_local_biomass.demand_emplo_new
    )  # lifecycle
    g.demand_emplo_new = (
        g_grid_offshore.demand_emplo_new
        + g_grid_onshore.demand_emplo_new
        + g_grid_pv.demand_emplo_new
    )
    d_r.cost_fuel = (
        d_r.energy
        * d_r.cost_fuel_per_MWh
        * p_fossil_and_renew.energy
        / p.energy
        / Million
    )
    d_b.cost_fuel = (
        d_b.energy
        * d_b.cost_fuel_per_MWh
        * p_fossil_and_renew.energy
        / p.energy
        / Million
    )
    d_i.cost_fuel = (
        d_i.energy
        * d_i.cost_fuel_per_MWh
        * p_fossil_and_renew.energy
        / p.energy
        / Million
    )
    d_t.cost_fuel = (
        d_t.energy
        * d_t.cost_fuel_per_MWh
        * p_fossil_and_renew.energy
        / p.energy
        / Million
    )
    d_a.cost_fuel = (
        d_a.energy
        * d_a.cost_fuel_per_MWh
        * p_fossil_and_renew.energy
        / p.energy
        / Million
    )
    p.change_energy_MWh = p.energy - e18.p.energy
    p_renew_wind_offshore.pct_x = div(p_renew_wind_offshore.energy, p.energy)
    p_renew_geoth.pct_x = div(p_renew_geoth.energy, p.energy)
    p_renew_reverse.pct_x = div(p_renew_reverse.energy, p.energy)
    p_local_pv.pct_x = div(p_local_pv.energy, p.energy)
    p_local_wind_onshore.pct_x = div(p_local_wind_onshore.energy, p.energy)
    p_local_biomass.pct_x = div(p_local_biomass.energy, p.energy)
    p_local_hydro.pct_x = div(p_local_hydro.energy, p.energy)

    p_local_pv_roof.pct_x = div(p_local_pv_roof.energy, p.energy)

    p_fossil_and_renew.change_energy_pct = div(
        p_fossil_and_renew.change_energy_MWh, e18.p_fossil_and_renew.energy
    )
    p_renew_pv_roof.cost_mro = (
        p_renew_pv_roof.energy * p_renew_pv_roof.cost_mro_per_MWh / Million
    )
    p_renew_pv_roof.change_energy_MWh = (
        p_renew_pv_roof.energy - e18.p_renew_pv_roof.energy
    )
    p_renew_pv_facade.cost_mro = (
        p_renew_pv_facade.energy * p_renew_pv_facade.cost_mro_per_MWh / Million
    )
    p_renew_pv_facade.change_energy_MWh = (
        p_renew_pv_facade.energy - e18.p_renew_pv_facade.energy
    )
    p_renew_pv_park.cost_mro = (
        p_renew_pv_park.energy * p_renew_pv_park.cost_mro_per_MWh / Million
    )
    p_renew_pv_park.change_energy_MWh = (
        p_renew_pv_park.energy - e18.p_renew_pv_park.energy
    )
    p_renew_pv_agri.cost_mro = (
        p_renew_pv_agri.energy * p_renew_pv_agri.cost_mro_per_MWh / Million
    )
    p_renew_pv_agri.change_energy_MWh = (
        p_renew_pv_agri.energy - e18.p_renew_pv_agri.energy
    )
    p_renew_wind_onshore.change_cost_mro = (
        p_renew_wind_onshore.cost_mro - e18.p_renew_wind_onshore.cost_mro
    )
    p_renew_wind_onshore.change_energy_pct = div(
        p_renew_wind_onshore.change_energy_MWh, e18.p_renew_wind_onshore.energy
    )
    p_renew_wind.CO2e_combustion_based = (
        p_renew_wind.energy * p_renew_wind.CO2e_combustion_based_per_MWh
    )
    p_renew_wind.cost_mro = (
        p_renew_wind_onshore.cost_mro + p_renew_wind_offshore.cost_mro
    )
    p_renew_wind_offshore.change_cost_mro = (
        p_renew_wind_offshore.cost_mro - e18.p_renew_wind_offshore.cost_mro
    )
    p_renew_wind.change_energy_MWh = (
        p_renew_wind_onshore.change_energy_MWh + p_renew_wind_offshore.change_energy_MWh
    )
    p_renew_wind_offshore.change_energy_pct = div(
        p_renew_wind_offshore.change_energy_MWh, e18.p_renew_wind_offshore.energy
    )
    p_renew.cost_fuel = p_renew_biomass.cost_fuel
    p_renew_biomass.change_cost_energy = (
        p_renew_biomass.cost_fuel - e18.p_renew_biomass.cost_fuel
    )
    p_renew_biomass.change_cost_mro = (
        p_renew_biomass.cost_mro - e18.p_renew_biomass.cost_mro
    )
    p_renew_biomass.CO2e_total = p_renew_biomass.CO2e_combustion_based
    p_renew_biomass.cost_climate_saved = (
        (
            p_renew_biomass.CO2e_total_2021_estimated
            - p_renew_biomass.CO2e_combustion_based
        )
        * KlimaneutraleJahre
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_renew_biomass.change_energy_pct = div(
        p_renew_biomass.change_energy_MWh, e18.p_renew_biomass.energy
    )
    p_renew_geoth.change_cost_mro = p_renew_geoth.cost_mro - e18.p_renew_geoth.cost_mro
    p_renew_geoth.change_energy_pct = div(
        p_renew_geoth.change_energy_MWh, e18.p_renew_geoth.energy
    )
    p_renew_hydro.change_cost_mro = p_renew_hydro.cost_mro - e18.p_renew_hydro.cost_mro
    p_renew_hydro.change_energy_pct = div(
        p_renew_hydro.change_energy_MWh, e18.p_renew_hydro.energy
    )
    p_renew_reverse.change_cost_mro = p_renew_reverse.cost_mro - 0
    e.demand_emplo = g.demand_emplo + p.demand_emplo
    p.demand_emplo_new = p_fossil_and_renew.demand_emplo_new + p_local.demand_emplo_new
    e.change_energy_MWh = p.change_energy_MWh
    p.change_energy_pct = div(p.change_energy_MWh, e18.p.energy)
    p_renew_pv_roof.change_cost_mro = (
        p_renew_pv_roof.cost_mro - e18.p_renew_pv_roof.cost_mro
    )
    p_renew_pv_roof.change_energy_pct = div(
        p_renew_pv_roof.change_energy_MWh, e18.p_renew_pv_roof.energy
    )
    p_renew_pv_facade.change_cost_mro = (
        p_renew_pv_facade.cost_mro - e18.p_renew_pv_facade.cost_mro
    )
    p_renew_pv_facade.change_energy_pct = div(
        p_renew_pv_facade.change_energy_MWh, e18.p_renew_pv_facade.energy
    )
    p_renew_pv_park.change_cost_mro = (
        p_renew_pv_park.cost_mro - e18.p_renew_pv_park.cost_mro
    )
    p_renew_pv_park.change_energy_pct = div(
        p_renew_pv_park.change_energy_MWh, e18.p_renew_pv_park.energy
    )
    p_renew_pv.cost_mro = (
        p_renew_pv_roof.cost_mro
        + p_renew_pv_facade.cost_mro
        + p_renew_pv_park.cost_mro
        + p_renew_pv_agri.cost_mro
    )  #
    p_renew_pv_agri.change_cost_mro = (
        p_renew_pv_agri.cost_mro - e18.p_renew_pv_agri.cost_mro
    )
    p_renew_pv.change_energy_MWh = (
        p_renew_pv_roof.change_energy_MWh
        + p_renew_pv_facade.change_energy_MWh
        + p_renew_pv_park.change_energy_MWh
        + p_renew_pv_agri.change_energy_MWh
    )
    p_renew_pv_agri.change_energy_pct = div(
        p_renew_pv_agri.change_energy_MWh, e18.p_renew_pv_agri.energy
    )
    p_renew.CO2e_combustion_based = (
        p_renew_pv.CO2e_combustion_based
        + p_renew_wind.CO2e_combustion_based
        + p_renew_biomass.CO2e_combustion_based
        + p_renew_geoth.CO2e_combustion_based
        + p_renew_hydro.CO2e_combustion_based
        + p_renew_reverse.CO2e_combustion_based
    )
    p_renew_wind.change_cost_mro = p_renew_wind.cost_mro - e18.p_renew_wind.cost_mro
    p_renew_wind.change_energy_pct = div(
        p_renew_wind.change_energy_MWh, e18.p_renew_wind.energy
    )
    p_fossil_and_renew.cost_fuel = p_fossil.cost_fuel + p_renew.cost_fuel
    p_renew.change_cost_energy = p_renew_biomass.change_cost_energy
    p_renew.change_cost_mro = p_renew_biomass.change_cost_mro
    p_renew.CO2e_total = (
        p_renew_pv.CO2e_total
        + p_renew_wind.CO2e_total
        + p_renew_biomass.CO2e_total
        + p_renew_geoth.CO2e_total
        + p_renew_hydro.CO2e_total
        + p_renew_reverse.CO2e_total
    )
    p_renew_biomass.change_CO2e_t = (
        p_renew_biomass.CO2e_total - e18.p_renew_biomass.CO2e_total
    )
    p_renew.cost_climate_saved = p_renew_biomass.cost_climate_saved
    e.demand_emplo_new = g.demand_emplo_new + p.demand_emplo_new
    e.change_energy_pct = p.change_energy_pct
    p_renew.cost_mro = (
        p_renew_pv.cost_mro
        + p_renew_wind.cost_mro
        + p_renew_biomass.cost_mro
        + p_renew_geoth.cost_mro
        + p_renew_hydro.cost_mro
        + p_renew_reverse.cost_mro
    )
    p_renew_pv.change_cost_mro = (
        p_renew_pv_roof.change_cost_mro
        + p_renew_pv_facade.change_cost_mro
        + p_renew_pv_park.change_cost_mro
        + p_renew_pv_agri.change_cost_mro
    )
    p_renew_pv.change_energy_pct = div(
        p_renew_pv.change_energy_MWh, e18.p_renew_pv.energy
    )
    p_fossil_and_renew.CO2e_combustion_based = (
        p_fossil.CO2e_combustion_based + p_renew.CO2e_combustion_based
    )
    p_renew.CO2e_combustion_based_per_MWh = div(
        p_renew.CO2e_combustion_based, p_renew.energy
    )
    p.cost_fuel = p_fossil_and_renew.cost_fuel + p_local.cost_fuel
    p_fossil_and_renew.change_cost_energy = (
        p_fossil.change_cost_energy + p_renew.change_cost_energy
    )
    p_fossil_and_renew.change_cost_mro = (
        p_fossil.change_cost_mro + p_renew.change_cost_mro
    )
    p_renew.change_CO2e_t = p_renew_biomass.change_CO2e_t
    p_renew_biomass.change_CO2e_pct = div(
        p_renew_biomass.change_CO2e_t, e18.p_renew_biomass.CO2e_total
    )
    p_fossil_and_renew.cost_climate_saved = (
        p_fossil.cost_climate_saved + p_renew.cost_climate_saved
    )
    p_fossil_and_renew.cost_mro = p_fossil.cost_mro + p_renew.cost_mro
    p.CO2e_combustion_based = (
        p_fossil_and_renew.CO2e_combustion_based + p_local.CO2e_combustion_based
    )
    p_fossil_and_renew.CO2e_combustion_based_per_MWh = div(
        p_fossil_and_renew.CO2e_combustion_based, p_fossil_and_renew.energy
    )
    p_fossil_and_renew.CO2e_total = p_fossil_and_renew.CO2e_combustion_based
    p.change_cost_energy = (
        p_fossil_and_renew.change_cost_energy + p_local.change_cost_energy
    )
    p.change_cost_mro = p_fossil_and_renew.change_cost_mro + p_local.change_cost_mro
    p.change_CO2e_t = (
        p_fossil.change_CO2e_t + p_renew.change_CO2e_t + p_local.change_CO2e_t
    )
    p_fossil_and_renew.change_CO2e_t = p_fossil.change_CO2e_t + p_renew.change_CO2e_t
    p_renew.change_CO2e_pct = div(p_renew.change_CO2e_t, e18.p_renew.CO2e_total)
    p.cost_climate_saved = (
        p_fossil_and_renew.cost_climate_saved + p_local.cost_climate_saved
    )
    p.cost_mro = p_fossil_and_renew.cost_mro + p_local.cost_mro
    e.CO2e_combustion_based = p.CO2e_combustion_based
    p.CO2e_combustion_based_per_MWh = div(p.CO2e_combustion_based, p.energy)
    p.CO2e_total = p.CO2e_combustion_based
    e.change_CO2e_t = p.change_CO2e_t
    p.change_CO2e_pct = div(p.change_CO2e_t, e18.p.CO2e_combustion_based)
    p_fossil_and_renew.change_CO2e_pct = div(
        p_fossil_and_renew.change_CO2e_t, e18.p_fossil_and_renew.CO2e_total
    )
    e.cost_climate_saved = p.cost_climate_saved
    e.CO2e_total = p.CO2e_total
    e.change_CO2e_pct = p.change_CO2e_pct

    p_local.power_installed = (
        p_local_pv.power_installed
        + p_local_wind_onshore.power_installed
        + p_local_biomass.power_installed
        + p_local_hydro.power_installed
    )

    p_local.power_installable = (
        p_local_pv.power_installable
        + p_local_wind_onshore.power_installable
        + p_local_biomass.power_installable
        # p_local_hydro.power_installable
    )

    p_local.power_to_be_installed = (
        p_local_pv.power_to_be_installed
        + p_local_wind_onshore.power_to_be_installed
        + p_local_biomass.power_to_be_installed
        # p_local_hydro.power_to_be_installed
    )

    # TODO: correct excel calculations and reimport these somehow missing variabels to python
    p_local_pv.cost_climate_saved = 0
    p_local_pv_park.change_CO2e_t = 0
    p_local_pv_park.cost_climate_saved = 0
    p_local_pv_facade.change_CO2e_t = 0
    p_local_pv_facade.cost_climate_saved = 0
    p_local_pv_agri.change_CO2e_t = 0
    p_local_pv_agri.cost_climate_saved = 0
    p_local_pv_roof.change_CO2e_t = 0
    p_local_pv_roof.cost_climate_saved = 0

    p_local_wind_onshore.CO2e_total = 0

    p_fossil.CO2e_total = 0

    p_renew_wind.change_CO2e_t = 0
    p_renew_wind.cost_climate_saved = 0

    p_renew_wind_onshore.CO2e_total = 0

    p_renew_wind_onshore.change_CO2e_t = 0
    p_renew_wind_offshore.change_CO2e_t = 0
    p_renew_wind_offshore.CO2e_total = 0

    p_renew_hydro.cost_climate_saved = 0
    p_renew_hydro.change_CO2e_t = 0

    p_renew_reverse.change_CO2e_t = 0
    p_renew_reverse.cost_climate_saved = 0

    p_renew_pv.change_CO2e_t = 0

    p_renew_pv_roof.change_CO2e_t = 0
    p_renew_pv_agri.change_CO2e_t = 0
    p_renew_pv_facade.change_CO2e_t = 0
    p_renew_pv_park.change_CO2e_t = 0

    p_renew_geoth.change_CO2e_t = 0

    p_local_pv_agri.CO2e_total = 0
    p_local_pv_roof.CO2e_total = 0
    p_local_pv_facade.CO2e_total = 0
    p_local_pv_park.CO2e_total = 0

    # ---copy
    p_renew_pv.change_CO2e_pct = 0
    p_renew_pv_roof.change_CO2e_pct = 0
    p_renew_pv_agri.change_CO2e_pct = 0
    p_renew_pv_facade.change_CO2e_pct = 0
    p_renew_pv_park.change_CO2e_pct = 0

    p_renew_wind.change_CO2e_pct = 0
    p_renew_wind_onshore.change_CO2e_pct = 0
    p_renew_wind_offshore.change_CO2e_pct = 0

    p_renew_hydro.change_CO2e_pct = 0

    p_local.change_CO2e_pct = 0
    p_local_pv.change_CO2e_pct = 0
    p_local_pv_roof.change_CO2e_pct = 0
    p_local_pv_agri.change_CO2e_pct = 0
    p_local_pv_facade.change_CO2e_pct = 0
    p_local_pv_park.change_CO2e_pct = 0
    p_local_wind_onshore.change_CO2e_pct = 0
    p_local_biomass.change_CO2e_pct = div(
        p_local_biomass.change_CO2e_t, e18.p_local_biomass.CO2e_total
    )

    p_renew_pv.cost_climate_saved = 0
    p_renew_pv_roof.cost_climate_saved = 0
    p_renew_pv_agri.cost_climate_saved = 0
    p_renew_pv_facade.cost_climate_saved = 0
    p_renew_pv_park.cost_climate_saved = 0

    p_renew_wind.cost_climate_saved = 0
    p_renew_wind_onshore.cost_climate_saved = 0
    p_renew_wind_offshore.cost_climate_saved = 0

    p_renew_hydro.cost_climate_saved = 0

    p_local.cost_climate_saved = 0
    p_local_pv.cost_climate_saved = 0
    p_local_pv_roof.cost_climate_saved = 0
    p_local_pv_agri.cost_climate_saved = 0
    p_local_pv_facade.cost_climate_saved = 0
    p_local_pv_park.cost_climate_saved = 0
    p_local_wind_onshore.cost_climate_saved = 0

    p_renew_reverse.change_CO2e_pct = 0
    p_local_wind_onshore.change_CO2e_t = 0

    return e30
