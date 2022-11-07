# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from ..investmentaction import InvestmentAction, RoadInvestmentAction
from ..rail import RailPeopleMetroActionInfra
from ..other import OtherCycle
from ..dataclasses import GPlanning, G


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

    # --- Planning and other aggregates ---
    g_planning = GPlanning.calc(
        inputs,
        road_bus_action_infra=road_bus_action_infra,
        road_gds_mhd_action_wire=road_gds_mhd_action_wire,
        road_action_charger=road_action_charger,
        rail_ppl_metro_action_infra=rail_ppl_metro_action_infra,
        rail_action_invest_infra=rail_action_invest_infra,
        other_cycl=other_cycl,
    )
    # TODO: This Seems to be a pointless rename?
    g = G(
        invest_com=g_planning.invest_com,
        invest_pa_com=g_planning.invest_pa_com,
        demand_emplo=g_planning.demand_emplo,
        cost_wage=g_planning.cost_wage,
        invest_pa=g_planning.invest_pa,
        invest=g_planning.invest,
        demand_emplo_new=g_planning.demand_emplo_new,
        demand_emplo_com=g_planning.demand_emplo_new,
    )

    return General(g=g, g_planning=g_planning)
