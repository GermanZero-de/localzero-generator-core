# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...common.g import G, GConsult as GPlanning, GConsult as GStorage


@dataclass(kw_only=True)
class General:
    g: G
    g_storage: GStorage
    g_planning: GPlanning


def calc_general(
    entries: Entries, facts: Facts, assumptions: Assumptions, p_heatnet_energy: float
) -> General:

    fact = facts.fact

    invest = (
        fact("Fact_H_P_planning_cost_basis")
        + fact("Fact_H_P_planning_cost_per_capita") * entries.m_population_com_2018
    )

    g_planning = GPlanning.calc_from_invest_calc_planning(
        entries=entries, facts=facts, assumptions=assumptions, invest=invest
    )
    g_storage = GStorage.calc_storage(
        entries=entries, facts=facts, energy=p_heatnet_energy
    )

    g = G.sum(g_planning, g_storage)

    return General(g=g, g_planning=g_planning, g_storage=g_storage)
