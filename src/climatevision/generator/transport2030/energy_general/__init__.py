# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.g import G, GPlanning

from ..energy_demand import (
    InvestmentAction,
    RoadInvestmentAction,
    RailPeopleMetroActionInfra,
    OtherCycle,
)


@dataclass(kw_only=True)
class General:
    g: G
    g_planning: GPlanning


def calc_general(
    inputs: Inputs,
    road_bus_action_infra: InvestmentAction,
    road_gds_mhd_action_wire: InvestmentAction,
    road_action_charger: RoadInvestmentAction,
    rail_ppl_metro_action_infra: RailPeopleMetroActionInfra,
    rail_action_invest_infra: InvestmentAction,
    other_cycl: OtherCycle,
) -> General:

    ass = inputs.ass

    invest = ass("Ass_T_C_planer_cost_per_invest_cost") * (
        road_bus_action_infra.invest
        + road_gds_mhd_action_wire.invest
        + road_action_charger.invest
        + rail_ppl_metro_action_infra.invest
        + rail_action_invest_infra.invest
        + other_cycl.invest
    )

    g_planning = GPlanning.calc(inputs, invest)

    # TODO: This Seems to be a pointless rename?
    g = G.sum(g_planning)

    return General(g=g, g_planning=g_planning)
