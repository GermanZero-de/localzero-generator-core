# pyright: strict

from dataclasses import dataclass

from ...refdata import Assumptions
from ...common.g import G, GConsult


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(
    assumptions: Assumptions,
    duration_until_target_year: int,
    population_commune_2018: int,
) -> General:
    ass = assumptions.ass

    invest_pa = ass("Ass_I_G_advice_invest_pa_per_capita") * population_commune_2018

    ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")

    g_consult = GConsult.calc_from_invest_pa(
        assumptions, duration_until_target_year, invest_pa, ratio_wage_to_emplo
    )

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
