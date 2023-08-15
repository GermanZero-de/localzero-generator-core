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

    # TODO: Change the below
    p_local_wind_onshore = EColVars2030()

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
        * population_commune_2018
        / population_germany_2018
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
    p_local_wind_onshore.power_installable = (
        p_local_wind_onshore.ratio_power_to_area_ha
        * p_local_wind_onshore.area_ha_available
        * p_local_wind_onshore.area_ha_available_pct_of_action
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
    p_local_wind_onshore.cost_mro = (
        p_local_wind_onshore.energy * p_local_wind_onshore.cost_mro_per_MWh / MILLION
    )
    p_local_wind_onshore.CO2e_combustion_based = (
        p_local_wind_onshore.energy * p_local_wind_onshore.CO2e_combustion_based_per_MWh
    )
    p_local_wind_onshore.CO2e_total = p_local_wind_onshore.CO2e_combustion_based
    p_local_wind_onshore.change_energy_MWh = (
        p_local_wind_onshore.energy - e18.p_local_wind_onshore.energy
    )
    p_local_wind_onshore.change_cost_mro = (
        p_local_wind_onshore.cost_mro - e18.p_local_wind_onshore.cost_mro
    )
    p_local_wind_onshore.change_energy_pct = div(
        p_local_wind_onshore.change_energy_MWh, e18.p_local_wind_onshore.energy
    )
    p_local_wind_onshore.invest_pa = (
        p_local_wind_onshore.invest / duration_until_target_year
    )
    p_local_wind_onshore.cost_wage = (
        p_local_wind_onshore.invest_pa * p_local_wind_onshore.pct_of_wage
    )
    p_local_wind_onshore.CO2e_total = 0
    p_local_wind_onshore.change_CO2e_pct = 0
    p_local_wind_onshore.cost_climate_saved = 0
    p_local_wind_onshore.change_CO2e_t = 0
    return p_local_wind_onshore


def calc_renew_wind_offshore(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    *,
    d_energy: float,
):
    fact = facts.fact
    ass = assumptions.ass

    p_renew_wind_offshore = EColVars2030()
    p_renew_wind_offshore.invest = 0
    p_renew_wind_offshore.demand_emplo = 0
    p_renew_wind_offshore.emplo_existing = 0
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
        p_renew_wind_offshore.invest / duration_until_target_year
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
    p_renew_wind_offshore.cost_wage = (
        p_renew_wind_offshore.invest_pa
        * p_renew_wind_offshore.pct_of_wage
        / duration_until_target_year
    )
    p_renew_wind_offshore.invest_pa_outside = (
        p_renew_wind_offshore.power_to_be_installed
        * p_renew_wind_offshore.invest_per_x
        / duration_until_target_year
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew_wind_offshore.invest_outside = (
        p_renew_wind_offshore.power_to_be_installed
        * p_renew_wind_offshore.invest_per_x
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    return p_renew_wind_offshore
