# pyright: strict

from .e_col_vars_2030 import EColVars2030


def calc_g(
    g_grid_offshore: EColVars2030,
    g_grid_onshore: EColVars2030,
    g_grid_pv: EColVars2030,
) -> EColVars2030:
    g = EColVars2030()
    g.invest_outside = g_grid_offshore.invest_outside
    g.invest_pa_outside = g_grid_offshore.invest_pa_outside
    g.invest = g_grid_offshore.invest + g_grid_onshore.invest + g_grid_pv.invest
    g.invest_pa = (
        g_grid_offshore.invest_pa + g_grid_onshore.invest_pa + g_grid_pv.invest_pa
    )
    g.cost_wage = (
        g_grid_offshore.cost_wage + g_grid_onshore.cost_wage + g_grid_pv.cost_wage
    )
    g.demand_emplo = (
        g_grid_offshore.demand_emplo
        + g_grid_onshore.demand_emplo
        + g_grid_pv.demand_emplo
    )
    g.demand_emplo_new = (
        g_grid_offshore.demand_emplo_new
        + g_grid_onshore.demand_emplo_new
        + g_grid_pv.demand_emplo_new
    )

    return g
