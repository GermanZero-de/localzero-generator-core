# pyright: strict

from ...refdata import Facts, Assumptions
from ...utils import div, MILLION

from .e_col_vars_2030 import EColVars2030


def calc_g_grid_onshore(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    p_local_wind_onshore_power_to_be_installed: float,
) -> EColVars2030:
    fact = facts.fact
    ass = assumptions.ass

    g_grid_onshore = EColVars2030()
    g_grid_onshore.invest_per_x = ass("Ass_E_G_grid_onshore_ratio_invest_to_power")
    g_grid_onshore.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_grid_onshore.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    g_grid_onshore.power_to_be_installed = p_local_wind_onshore_power_to_be_installed
    g_grid_onshore.invest = (
        g_grid_onshore.power_to_be_installed * g_grid_onshore.invest_per_x
    )
    g_grid_onshore.cost_mro = (
        g_grid_onshore.invest * ass("Ass_E_G_grid_onshore_mro") / MILLION
    )
    g_grid_onshore.invest_pa = g_grid_onshore.invest / duration_until_target_year
    g_grid_onshore.cost_wage = g_grid_onshore.invest_pa * g_grid_onshore.pct_of_wage
    g_grid_onshore.demand_emplo = div(
        g_grid_onshore.cost_wage, g_grid_onshore.ratio_wage_to_emplo
    )
    g_grid_onshore.demand_emplo_new = g_grid_onshore.demand_emplo

    return g_grid_onshore
