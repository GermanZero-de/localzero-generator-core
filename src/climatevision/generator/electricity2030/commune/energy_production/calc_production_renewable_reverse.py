# pyright: strict

from ....refdata import Facts, Assumptions

from ...core.e_col_vars_2030 import EColVars2030


def calc_production_renewable_reverse(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    *,
    d_energy: float,
):
    fact = facts.fact
    ass = assumptions.ass

    p_renew_reverse = EColVars2030()

    p_renew_reverse.CO2e_total = 0
    p_renew_reverse.invest = 0
    p_renew_reverse.demand_emplo = 0
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
    p_renew_reverse.invest_pa = p_renew_reverse.invest / duration_until_target_year
    p_renew_reverse.demand_emplo_new = p_renew_reverse.demand_emplo
    p_renew_reverse.power_to_be_installed = max(
        0,
        ass("Ass_E_P_renew_reverse_addon_to_demand_2035")
        * ass("Ass_E_P_renew_nep_total_2035")
        / ass("Ass_E_P_renew_reverse_full_load_hours")
        - p_renew_reverse.power_installed,
    )
    p_renew_reverse.cost_wage = p_renew_reverse.invest_pa * p_renew_reverse.pct_of_wage
    p_renew_reverse.invest_pa_outside = (
        p_renew_reverse.power_to_be_installed
        * p_renew_reverse.invest_per_x
        / duration_until_target_year
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    p_renew_reverse.invest_outside = (
        p_renew_reverse.invest * d_energy / ass("Ass_E_P_renew_nep_total_2035")
    )

    return p_renew_reverse
