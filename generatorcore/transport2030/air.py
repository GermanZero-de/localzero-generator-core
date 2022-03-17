# pyright: strict

from dataclasses import dataclass, asdict
from ..inputs import Inputs
from ..utils import div
from ..transport2018 import T18
from .transport import Transport


@dataclass
class AirDomestic(Transport):
    # Used by air_dmstc
    @classmethod
    def calc(cls, inputs: Inputs, t18: T18) -> "AirDomestic":
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
        change_energy_MWh = -t18.air_dmstc.energy
        change_energy_pct = div(change_energy_MWh, t18.air_dmstc.energy)
        change_CO2e_t = -t18.air_dmstc.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.air_dmstc.CO2e_combustion_based)
        return cls(
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            # We need no energy to transport nothing
            energy=0,
            transport_capacity_tkm=0,
            transport_capacity_pkm=0,
            # And not doing anything causes no CO2e
            CO2e_combustion_based=0,
            CO2e_total=0,
        )


@dataclass
class AirInternational(Transport):
    # Used by air_inter
    demand_ejetfuel: float

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
        energy = demand_ejetfuel
        CO2e_total = CO2e_combustion_based
        change_energy_MWh = energy - t18.air_inter.energy
        change_energy_pct = div(change_energy_MWh, t18.air_inter.energy)
        change_CO2e_t = CO2e_combustion_based - t18.air_inter.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.air_inter.CO2e_combustion_based)
        return cls(
            CO2e_total=CO2e_total,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=transport_capacity_pkm,
            change_energy_pct=change_energy_pct,
            change_energy_MWh=change_energy_MWh,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            demand_ejetfuel=demand_ejetfuel,
            energy=energy,
        )


@dataclass
class Air(Transport):
    # Used by air
    demand_ejetfuel: float
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
        domestic: AirDomestic,
        international: AirInternational,
    ) -> "Air":
        sum = Transport.sum(
            domestic,
            international,
            energy_2018=t18.air.energy,
            co2e_2018=t18.air.CO2e_combustion_based,
        )
        demand_ejetfuel = (
            international.demand_ejetfuel  # SUM(air_inter.demand_ejetfuel:BD236)
        )
        return cls(
            demand_ejetfuel=demand_ejetfuel,
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
