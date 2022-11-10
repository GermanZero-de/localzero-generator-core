# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div

from ..dataclasses import Vars1, Vars2, Vars3


@dataclass(kw_only=True)
class General:
    g: Vars1
    g_storage: Vars2
    g_planning: Vars3


def calc_general(inputs: Inputs, p_heatnet_energy: float) -> General:

    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    g_planning = Vars3()
    g_planning.invest = (
        fact("Fact_H_P_planning_cost_basis")
        + fact("Fact_H_P_planning_cost_per_capita") * entries.m_population_com_2018
    )
    g_planning.invest_pa = g_planning.invest / entries.m_duration_target

    g_planning.invest_com = g_planning.invest
    g_planning.invest_pa_com = g_planning.invest_pa

    g_planning.pct_of_wage = ass("Ass_H_G_planning_cost_pct_of_wage")
    g_planning.cost_wage = g_planning.invest / fact("Fact_H_P_planning_duration")

    g_planning.ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
    g_planning.demand_emplo = div(g_planning.cost_wage, g_planning.ratio_wage_to_emplo)
    g_planning.demand_emplo_new = g_planning.demand_emplo
    g_planning.demand_emplo_com = g_planning.demand_emplo_new

    g_storage = Vars2()
    g_storage.energy = p_heatnet_energy
    g_storage.pct_energy = fact("Fact_H_P_storage_specific_volume")

    g_storage.invest_per_x = fact("Fact_H_P_storage_specific_cost")
    g_storage.power_to_be_installed = g_storage.energy * g_storage.pct_energy
    g_storage.invest = g_storage.invest_per_x * g_storage.power_to_be_installed
    g_storage.invest_pa = g_storage.invest / entries.m_duration_target

    g_storage.invest_com = g_storage.invest
    g_storage.invest_pa_com = g_storage.invest_pa

    g_storage.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_storage.cost_wage = g_storage.pct_of_wage * g_storage.invest_pa

    g_storage.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    g_storage.demand_emplo = div(g_storage.cost_wage, g_storage.ratio_wage_to_emplo)
    g_storage.demand_emplo_new = g_storage.demand_emplo

    g = Vars1()
    g.invest_com = g_storage.invest_com + g_planning.invest_com
    g.invest_pa_com = g_storage.invest_pa_com + g_planning.invest_pa_com
    g.invest_pa = g_storage.invest_pa + g_planning.invest_pa
    g.invest = g_storage.invest + g_planning.invest
    g.cost_wage = g_storage.cost_wage + g_planning.cost_wage
    g.demand_emplo = g_storage.demand_emplo + g_planning.demand_emplo
    g.demand_emplo_new = g_storage.demand_emplo_new + g_planning.demand_emplo_new
    g.demand_emplo_com = g_planning.demand_emplo_com

    return General(g=g, g_planning=g_planning, g_storage=g_storage)
