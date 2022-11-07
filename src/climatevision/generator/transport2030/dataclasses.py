# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import div
from ..transport2018.t18 import T18

from .investmentaction import InvestmentAction
from .air import Air
from .road import RoadSum
from .rail import Rail, RailPeopleMetroActionInfra
from .ship import Ship
from .other import Other, OtherCycle
from .transport import Transport


@dataclass(kw_only=True)
class GPlanning:
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        road_bus_action_infra: InvestmentAction,
        road_gds_mhd_action_wire: InvestmentAction,
        road_action_charger: InvestmentAction,
        rail_ppl_metro_action_infra: RailPeopleMetroActionInfra,
        rail_action_invest_infra: InvestmentAction,
        other_cycl: OtherCycle,
    ) -> "GPlanning":
        ass = inputs.ass
        entries = inputs.entries

        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
        invest = ass("Ass_T_C_planer_cost_per_invest_cost") * (
            road_bus_action_infra.invest
            + road_gds_mhd_action_wire.invest
            + road_action_charger.invest
            + rail_ppl_metro_action_infra.invest
            + rail_action_invest_infra.invest
            + other_cycl.invest
        )
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_com = invest_com / entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        cost_wage = invest_pa
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
        demand_emplo_com = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass(kw_only=True)
class G:
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float


@dataclass(kw_only=True)
class T:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport
    # Used by t
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        required_domestic_transport_capacity_pkm: float,
        air: Air,
        rail: Rail,
        road: RoadSum,
        ship: Ship,
        other: Other,
        g: G,
    ) -> "T":
        invest_com = (
            g.invest_com
            + road.invest_com
            + rail.invest_com
            + ship.invest_com
            + other.invest_com
            + air.invest_com
        )
        invest_pa_com = (
            g.invest_pa_com
            + road.invest_pa_com
            + rail.invest_pa_com
            + ship.invest_pa_com
            + other.invest_pa_com
            + air.invest_pa_com
        )
        invest = (
            road.invest
            + rail.invest
            + ship.invest
            + other.invest
            + air.invest
            + g.invest
        )
        cost_wage = (
            g.cost_wage
            + road.cost_wage
            + rail.cost_wage
            + ship.cost_wage
            + other.cost_wage
        )
        demand_emplo = (
            g.demand_emplo
            + air.demand_emplo
            + road.demand_emplo
            + rail.demand_emplo
            + ship.demand_emplo
            + other.demand_emplo
        )
        demand_emplo_new = (
            g.demand_emplo_new
            + air.demand_emplo_new
            + road.demand_emplo_new
            + rail.demand_emplo_new
            + ship.demand_emplo_new
            + other.demand_emplo_new
        )
        invest_pa = (
            road.invest_pa
            + rail.invest_pa
            + ship.invest_pa
            + other.invest_pa
            + air.invest_pa
            + g.invest_pa
        )
        demand_emplo_com = g.demand_emplo_com

        res = cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            transport=Transport.sum(
                air.transport,
                rail.transport,
                road.transport,
                ship.transport,
                other.transport,
                transport2018=t18.t,
            ),
        )
        assert (
            required_domestic_transport_capacity_pkm
            <= res.transport.transport_capacity_pkm
        ), "We should know have at least as much provided transport capacity as we required initially"
        # Also shouldn't we store the computed transport capacity here?
        # And not what we claimed we need but what we are providing?
        return res
