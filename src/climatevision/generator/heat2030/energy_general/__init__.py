# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .g import G, GStorage, GPlanning


@dataclass(kw_only=True)
class General:
    g: G
    g_storage: GStorage
    g_planning: GPlanning


def calc_general(inputs: Inputs, p_heatnet_energy: float) -> General:

    g_planning = GPlanning.calc(inputs=inputs)
    g_storage = GStorage.calc(inputs=inputs, p_heatnet_energy=p_heatnet_energy)

    g = G(
        invest_com=g_storage.invest_com + g_planning.invest_com,
        invest_pa_com=g_storage.invest_pa_com + g_planning.invest_pa_com,
        invest_pa=g_storage.invest_pa + g_planning.invest_pa,
        invest=g_storage.invest + g_planning.invest,
        cost_wage=g_storage.cost_wage + g_planning.cost_wage,
        demand_emplo=g_storage.demand_emplo + g_planning.demand_emplo,
        demand_emplo_new=g_storage.demand_emplo_new + g_planning.demand_emplo_new,
        demand_emplo_com=g_planning.demand_emplo_com,
    )

    return General(g=g, g_planning=g_planning, g_storage=g_storage)
