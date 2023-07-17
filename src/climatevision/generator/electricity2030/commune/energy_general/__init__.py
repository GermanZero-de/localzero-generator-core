# pyright: strict

from dataclasses import dataclass

from ....refdata import Facts, Assumptions
from ....utils import div, MILLION

from ...core.e_col_vars_2030 import EColVars2030
from ...core.g_grid_onshore import calc_g_grid_onshore
from ...core.g_grid_pv import calc_g_grid_pv
from ...core.g import calc_g


@dataclass(kw_only=True)
class General:
    g: EColVars2030
    g_grid_offshore: EColVars2030
    g_grid_onshore: EColVars2030
    g_grid_pv: EColVars2030


def calc_general(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    p_renew_wind_offshore_power_to_be_installed: float,
    p_local_wind_onshore_power_to_be_installed: float,
    p_local_pv_power_to_be_installed: float,
    d_energy: float,
) -> General:
    fact = facts.fact
    ass = assumptions.ass

    g_grid_onshore = calc_g_grid_onshore(
        facts,
        assumptions,
        duration_until_target_year,
        p_local_wind_onshore_power_to_be_installed,
    )

    g_grid_pv = calc_g_grid_pv(
        facts, assumptions, duration_until_target_year, p_local_pv_power_to_be_installed
    )

    g_grid_offshore = EColVars2030()
    g_grid_offshore.invest = 0
    g_grid_offshore.invest_per_x = ass("Ass_E_G_grid_offshore_ratio_invest_to_power")
    g_grid_offshore.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_grid_offshore.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    g_grid_offshore.cost_mro = (
        g_grid_offshore.invest * ass("Ass_E_G_grid_offshore_mro") / MILLION
    )
    g_grid_offshore.invest_pa = g_grid_offshore.invest / duration_until_target_year
    g_grid_offshore.cost_wage = g_grid_offshore.invest_pa * g_grid_offshore.pct_of_wage
    g_grid_offshore.power_to_be_installed = p_renew_wind_offshore_power_to_be_installed
    g_grid_offshore.demand_emplo = div(
        g_grid_offshore.cost_wage, g_grid_offshore.ratio_wage_to_emplo
    )
    g_grid_offshore.invest_outside = (
        g_grid_offshore.power_to_be_installed
        * g_grid_offshore.invest_per_x
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    g_grid_offshore.demand_emplo_new = g_grid_offshore.demand_emplo
    g_grid_offshore.invest_pa_outside = (
        g_grid_offshore.invest_outside / duration_until_target_year
    )

    g = calc_g(g_grid_offshore, g_grid_onshore, g_grid_pv)

    return General(
        g=g,
        g_grid_offshore=g_grid_offshore,
        g_grid_onshore=g_grid_onshore,
        g_grid_pv=g_grid_pv,
    )
