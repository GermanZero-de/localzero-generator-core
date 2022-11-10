# pyright: strict

from dataclasses import dataclass

from ..transport2018.t18 import T18

from .energy_demand import (
    Air,
    RoadSum,
    Rail,
    Ship,
    Other,
    Transport,
)
from .energy_general import G


@dataclass(kw_only=True)
class T:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

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
