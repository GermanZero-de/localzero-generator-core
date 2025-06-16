# pyright: strict

from dataclasses import dataclass

from ..common.invest import InvestCommune
from ..transport2018.t18 import T18
from .energy_demand import Air, Other, Rail, RoadSum, Ship, Transport
from .energy_general import G


@dataclass(kw_only=True)
class T(InvestCommune):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    demand_emplo_com: float

    invest_com_state: float
    invest_com_pa_state: float
    invest_com_wo_state: float
    invest_com_pa_wo_state: float

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
        invest_com_state = (
            road.gds_mhd_action_wire
            + rail.action_invest_infra
            + rail.action_invest_station
            + ship.dmstc_action_infra
        )
        invest_com_pa_state = (
            invest_com_state / g.duration_until_target_year
        )  # FIXME: This is a guess, please verify
        invest_com_wo_state = invest_com - invest_com_state
        invest_com_pa_wo_state = (
            invest_com_wo_state / g.duration_until_target_year
        )  # FIXME: This is a guess, please verify

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
            invest_com_state=invest_com_state,
            invest_com_pa_state=invest_com_pa_state,
            invest_com_wo_state=invest_com_wo_state,
            invest_com_pa_wo_state=invest_com_pa_wo_state,
        )
        return res
