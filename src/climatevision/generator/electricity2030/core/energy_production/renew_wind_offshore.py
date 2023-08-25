# pyright: strict

from ....refdata import Facts, Assumptions

from ..e_col_vars_2030 import EColVars2030


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
