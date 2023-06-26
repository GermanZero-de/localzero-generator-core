# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Assumptions
from ...common.g import G, GConsult


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(entries: Entries, assumptions: Assumptions) -> General:
    ass = assumptions.ass

    invest_pa = (
        ass("Ass_I_G_advice_invest_pa_per_capita") * entries.m_population_com_2018
    )

    ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")

    g_consult = GConsult.calc_from_invest_pa(
        entries, assumptions, invest_pa, ratio_wage_to_emplo
    )

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
