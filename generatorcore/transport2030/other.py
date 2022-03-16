# pyright: strict

from dataclasses import dataclass, asdict
from ..inputs import Inputs
from ..utils import div
from ..transport2018 import T18

from .transport import Transport
from .investmentaction import InvestmentAction


@dataclass
class OtherFoot(Transport):
    # Used by other_foot
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def calc(
        cls, inputs: Inputs, *, t18: T18, total_transport_capacity_pkm: float
    ) -> "OtherFoot":
        """Everybody should walk more it's healthy and has no negative effects
        on the climate. But of course how much we can walk depends on the
        kind of area we are in."""
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        transport_capacity_pkm = total_transport_capacity_pkm * (
            ass("Ass_T_D_trnsprt_ppl_city_foot_frac_2050")
            if entries.t_rt3 == "city"
            else ass("Ass_T_D_trnsprt_ppl_smcty_foot_frac_2050")
            if entries.t_rt3 == "smcty"
            else ass("Ass_T_D_trnsprt_ppl_rural_foot_frac_2050")
            if entries.t_rt3 == "rural"
            else ass("Ass_T_D_trnsprt_ppl_nat_foot_frac_2050")
        )
        change_km = transport_capacity_pkm - t18.other_foot.transport_capacity_pkm

        CO2e_total_2021_estimated = t18.other_foot.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            CO2e_combustion_based=0,
            CO2e_total=0,
            change_CO2e_t=0,
            change_CO2e_pct=0,
            energy=0,
            change_energy_MWh=0,
            change_energy_pct=0,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            invest=0,
            invest_com=0,
            invest_pa=0,
            invest_pa_com=0,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
        )


@dataclass
class OtherCycle(Transport):
    # Used by other_cycl

    base_unit: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    invest_per_x: float

    @classmethod
    def calc(
        cls, inputs: Inputs, t18: T18, total_transport_capacity_pkm: float
    ) -> "OtherCycle":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        transport_capacity_pkm = total_transport_capacity_pkm * (
            ass("Ass_T_D_trnsprt_ppl_city_cycl_frac_2050")
            if entries.t_rt3 == "city"
            else ass("Ass_T_D_trnsprt_ppl_smcty_cycl_frac_2050")
            if entries.t_rt3 == "smcty"
            else ass("Ass_T_D_trnsprt_ppl_rural_cycl_frac_2050")
            if entries.t_rt3 == "rural"
            else ass("Ass_T_D_trnsprt_ppl_nat_cycl_frac_2050")
        )

        invest_per_x = fact("Fact_T_D_cycl_vehicle_invest_hannah")
        base_unit = (
            transport_capacity_pkm
            * ass("Ass_T_D_cycl_ratio_cargo_to_bikes")
            / ass("Ass_T_D_cycl_cargo_mlg")
        )
        invest = base_unit * invest_per_x
        CO2e_total_2021_estimated = t18.other_cycl.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_com = 0
        invest_pa = invest / entries.m_duration_target
        change_km = transport_capacity_pkm - t18.other_cycl.transport_capacity_pkm
        invest_pa_com = invest_com / entries.m_duration_target
        CO2e_total = 0

        return cls(
            CO2e_combustion_based=0,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_t=0,
            change_CO2e_pct=0,
            energy=0,
            change_energy_MWh=0,
            change_energy_pct=0,
            base_unit=base_unit,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
        )


@dataclass
class Other(Transport):
    # Used by other

    base_unit: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        *,
        other_foot: OtherFoot,
        other_cycl: OtherCycle,
        other_foot_action_infra: InvestmentAction,
        other_cycl_action_infra: InvestmentAction,
    ) -> "Other":
        sum = Transport.sum(other_foot, other_cycl, energy_2018=0, co2e_2018=0)
        invest_com = (
            other_foot.invest_com
            + other_cycl.invest_com
            + other_foot_action_infra.invest_com
            + other_cycl_action_infra.invest_com
        )
        invest = (
            other_foot.invest
            + other_cycl.invest
            + other_foot_action_infra.invest
            + other_cycl_action_infra.invest
        )
        invest_pa_com = (
            other_foot.invest_pa_com
            + other_cycl.invest_pa_com
            + other_foot_action_infra.invest_pa_com
            + other_cycl_action_infra.invest_pa_com
        )
        demand_emplo_new = (
            other_foot_action_infra.demand_emplo_new
            + other_cycl_action_infra.demand_emplo_new
        )
        cost_wage = (
            other_foot_action_infra.cost_wage + other_cycl_action_infra.cost_wage
        )
        other_cycl_action_infra.invest_pa = (
            other_cycl_action_infra.invest / inputs.entries.m_duration_target
        )
        other_cycl_action_infra.demand_emplo = div(
            other_cycl_action_infra.cost_wage,
            other_cycl_action_infra.ratio_wage_to_emplo,
        )
        demand_emplo = (
            other_foot_action_infra.demand_emplo + other_cycl_action_infra.demand_emplo
        )
        invest_pa = (
            other_foot.invest_pa
            + other_cycl.invest_pa
            + other_foot_action_infra.invest_pa
            + other_cycl_action_infra.invest_pa
        )
        base_unit = other_cycl.base_unit

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            **asdict(sum),
        )
