# pyright: strict

from dataclasses import dataclass, asdict
from ..inputs import Inputs
from ..utils import div
from ..transport2018 import T18
from .transport import Transport


def calc_air_domestic(inputs: Inputs, t18: T18) -> "Transport":
    """We assume that no domestic flights are allowed when Germany is carbon neutral as trains
    are a good and cheap alternative (or should be).

    So this just computes the reduction to 0.
    """
    CO2e_total_2021_estimated = t18.air_dmstc.CO2e_combustion_based * inputs.fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    cost_climate_saved = (
        (CO2e_total_2021_estimated)
        * inputs.entries.m_duration_neutral
        * inputs.fact("Fact_M_cost_per_CO2e_2020")
    )
    change_km = -t18.air_dmstc.transport_capacity_pkm
    t = Transport(
        CO2e_total_2021_estimated=CO2e_total_2021_estimated,
        change_km=change_km,
        cost_climate_saved=cost_climate_saved,
        # We need no energy to transport nothing
        transport_capacity_tkm=0,
        transport_capacity_pkm=0,
        # And not doing anything causes no CO2e
        CO2e_combustion_based=0,
        CO2e_total=0,
        transport2018=t18.air_dmstc,
    )
    return t


@dataclass(kw_only=True)
class AirInternational(Transport):
    @classmethod
    def calc(cls, inputs: Inputs, t18: T18) -> "AirInternational":
        """However for many international flights there are no good alternatives.
        So we will need ejetfuels.
        """
        demand_ejetfuel = (
            inputs.ass("Ass_T_D_Air_nat_EB_2050")
            * inputs.entries.m_population_com_203X
            / inputs.entries.m_population_nat
        )
        transport_capacity_tkm = t18.air_inter.transport_capacity_tkm * div(
            demand_ejetfuel, t18.air_inter.demand_jetfuel
        )
        CO2e_combustion_based = demand_ejetfuel * inputs.ass(
            "Ass_T_S_jetfuel_EmFa_tank_wheel_2050"
        )
        CO2e_total_2021_estimated = t18.air_inter.CO2e_combustion_based * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )
        transport_capacity_pkm = t18.air_inter.transport_capacity_pkm * div(
            demand_ejetfuel, t18.air_inter.demand_jetfuel
        )
        change_km = transport_capacity_pkm - t18.air_inter.transport_capacity_pkm
        CO2e_total = CO2e_combustion_based
        res = cls(
            CO2e_total=CO2e_total,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=transport_capacity_pkm,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            demand_ejetfuel=demand_ejetfuel,
            transport2018=t18.air_inter,
        )
        return res


@dataclass
class Air(Transport):
    # Used by air
    demand_emplo: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def calc(
        cls,
        t18: T18,
        domestic: Transport,
        international: AirInternational,
    ) -> "Air":
        sum = Transport.sum(domestic, international, transport2018=t18.air)
        res = cls(
            # Our simplified assumption here is that the only costs to get clean international flight is
            # using efuels. Therefore no costs show up here and all in the fuels2030 section.
            invest_pa_com=0,
            invest_com=0,
            invest_pa=0,
            invest=0,
            demand_emplo=0,
            demand_emplo_new=0,
            **asdict(sum),
        )
        return res
