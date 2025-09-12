# pyright: strict

from ....makeentries import Entries
from ....refdata import Facts, Assumptions
from ....utils import MILLION, div
from ....electricity2018.e18 import E18

from ..e_col_vars_2030 import EColVars2030


def calc_production_local_wind_onshore(
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    *,
    e18: E18,
):
    fact = facts.fact
    ass = assumptions.ass

    duration_until_target_year = entries.m_duration_target

    population_commune_2018 = entries.m_population_com_2018
    population_germany_2018 = entries.m_population_nat

    power_installed = entries.e_PV_power_inst_wind_on
    full_load_hour = fact("Fact_E_P_wind_onshore_full_load_hours")
    cost_mro_per_MWh = (
        ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_wind_onshore_mro_per_year")
        / fact("Fact_E_P_wind_onshore_full_load_hours")
        * 1000
    )
    CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    invest_per_x = ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2030") * 1000
    pct_of_wage = ass("Ass_E_P_constr_plant_invest_pct_of_wage_2017")
    ratio_wage_to_emplo = ass("Ass_E_P_constr_elec_ratio_wage_to_emplo_2017")
    emplo_existing = (
        fact("Fact_E_P_wind_onshore_emplo_2018")
        * population_commune_2018
        / population_germany_2018
    )
    power_to_be_installed_pct = entries.e_PV_power_to_be_inst_local_wind_onshore
    ratio_power_to_area_ha = entries.e_local_wind_onshore_ratio_power_to_area_sta
    area_ha_available = entries.m_area_agri_com + entries.m_area_wood_com
    area_ha_available_pct_of_action = ass("Ass_E_P_local_wind_onshore_pct_action")
    power_installable = (
        ratio_power_to_area_ha * area_ha_available * area_ha_available_pct_of_action
    )
    power_to_be_installed = max(
        0,
        power_installable * power_to_be_installed_pct - power_installed,
    )
    energy_installable = (
        full_load_hour
        * power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    energy = (
        (power_to_be_installed + power_installed)
        * full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    invest = power_to_be_installed * invest_per_x
    cost_mro = energy * cost_mro_per_MWh / MILLION
    CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
    CO2e_total = CO2e_combustion_based
    change_cost_mro = cost_mro - e18.p_local_wind_onshore.cost_mro
    invest_pa = invest / duration_until_target_year
    cost_wage = invest_pa * pct_of_wage
    CO2e_total = 0
    change_CO2e_pct = 0
    cost_climate_saved = 0
    change_CO2e_t = 0

    cost_fuel_per_MWh = None
    cost_fuel = None
    pet_sites = None
    CO2e_total_year_before_baseline_estimated = None
    demand_electricity = None
    demand_emplo = None
    demand_emplo_com = None
    change_cost_energy = None
    invest_com = None
    invest_pa_com = None
    invest_outside = None
    invest_pa_outside = None
    pct_x = None
    demand_emplo_new = None

    p_local_wind_onshore = EColVars2030(
        cost_fuel_per_MWh=cost_fuel_per_MWh,  # type: ignore
        cost_fuel=cost_fuel,  # type: ignore
        pet_sites=pet_sites,  # type: ignore
        energy_installable=energy_installable,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
        CO2e_combustion_based=CO2e_combustion_based,
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        CO2e_total_year_before_baseline_estimated=CO2e_total_year_before_baseline_estimated,  # type: ignore
        demand_electricity=demand_electricity,  # type: ignore
        demand_emplo=demand_emplo,  # type: ignore
        demand_emplo_com=demand_emplo_com,  # type: ignore
        power_installed=power_installed,
        power_to_be_installed_pct=power_to_be_installed_pct,
        power_to_be_installed=power_to_be_installed,
        power_installable=power_installable,
        area_ha_available=area_ha_available,
        area_ha_available_pct_of_action=area_ha_available_pct_of_action,
        ratio_power_to_area_ha=ratio_power_to_area_ha,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_energy=change_cost_energy,  # type: ignore
        change_cost_mro=change_cost_mro,
        invest=invest,
        invest_pa=invest_pa,
        invest_com=invest_com,  # type: ignore
        invest_pa_com=invest_pa_com,  # type: ignore
        invest_outside=invest_outside,  # type: ignore
        invest_pa_outside=invest_pa_outside,  # type: ignore
        invest_per_x=invest_per_x,
        pct_of_wage=pct_of_wage,
        pct_x=pct_x,  # type: ignore
        ratio_wage_to_emplo=ratio_wage_to_emplo,
        cost_wage=cost_wage,
        cost_mro_per_MWh=cost_mro_per_MWh,
        emplo_existing=emplo_existing,
        demand_emplo_new=demand_emplo_new,  # type: ignore
        full_load_hour=full_load_hour,
    )

    p_local_wind_onshore.change_energy_MWh = energy - e18.p_local_wind_onshore.energy

    p_local_wind_onshore.change_energy_pct = div(
        p_local_wind_onshore.change_energy_MWh, e18.p_local_wind_onshore.energy
    )

    p_local_wind_onshore.energy = energy

    return p_local_wind_onshore
