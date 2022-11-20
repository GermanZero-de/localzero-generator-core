# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.g import G, GConsult as GPlanning

from .g_storage import GStorage


@dataclass(kw_only=True)
class General:
    g: G
    g_storage: GStorage
    g_planning: GPlanning


def calc_general(inputs: Inputs, p_heatnet_energy: float) -> General:

    fact = inputs.fact
    entries = inputs.entries

    invest = (
        fact("Fact_H_P_planning_cost_basis")
        + fact("Fact_H_P_planning_cost_per_capita") * entries.m_population_com_2018
    )

    g_planning = GPlanning.calc_from_invest_calc_planning(inputs=inputs, invest=invest)
    g_storage = GStorage.calc(inputs=inputs, p_heatnet_energy=p_heatnet_energy)

    g = G.sum(g_planning, g_storage)

    return General(g=g, g_planning=g_planning, g_storage=g_storage)
