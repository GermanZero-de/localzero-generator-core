# pyright: strict

from dataclasses import dataclass

from ...common.invest import InvestCommune
from ...entries import Entries
from ...refdata import Assumptions, Facts
from ...transport2018.t18 import T18
from ...utils import div
from .investmentaction import InvestmentAction
from .transport import Transport


@dataclass(kw_only=True)
class ZeroEnergyAndCO2e:
    transport_capacity_pkm: float
    transport_capacity_tkm: float
    energy: float = 0
    CO2e_combustion_based: float = 0


@dataclass(kw_only=True)
class OtherFoot:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        entries: Entries,
        assumptions: Assumptions,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        *,
        t18: T18,
        total_transport_capacity_pkm: float,
    ) -> "OtherFoot":
        """Everybody should walk more it's healthy and has no negative effects
        on the climate. But of course how much we can walk depends on the
        kind of area we are in."""
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_pkm = total_transport_capacity_pkm * (
            ass("Ass_T_D_trnsprt_ppl_city_foot_frac_2050")
            if area_kind == "city"
            else (
                ass("Ass_T_D_trnsprt_ppl_smcty_foot_frac_2050")
                if area_kind == "smcty"
                else (
                    ass("Ass_T_D_trnsprt_ppl_rural_foot_frac_2050")
                    if area_kind == "rural"
                    else ass("Ass_T_D_trnsprt_ppl_nat_foot_frac_2050")
                )
            )
        )

        CO2e_total_2021_estimated = t18.other_foot.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        res = cls(
            invest=0,
            invest_com=0,
            invest_pa=0,
            invest_pa_com=0,
            transport=Transport(
                CO2e_combustion_based=0,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=ZeroEnergyAndCO2e(
                    transport_capacity_pkm=t18.other_foot.transport_capacity_pkm,
                    transport_capacity_tkm=0,
                ),
            ),
        )
        return res


@dataclass(kw_only=True)
class OtherCycle:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    invest_per_x: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        entries: Entries,
        assumptions: Assumptions,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        t18: T18,
        total_transport_capacity_pkm: float,
    ) -> "OtherCycle":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_pkm = total_transport_capacity_pkm * (
            ass("Ass_T_D_trnsprt_ppl_city_cycl_frac_2050")
            if area_kind == "city"
            else (
                ass("Ass_T_D_trnsprt_ppl_smcty_cycl_frac_2050")
                if area_kind == "smcty"
                else (
                    ass("Ass_T_D_trnsprt_ppl_rural_cycl_frac_2050")
                    if area_kind == "rural"
                    else ass("Ass_T_D_trnsprt_ppl_nat_cycl_frac_2050")
                )
            )
        )

        invest_per_x = fact("Fact_T_D_cycl_vehicle_invest_hannah")
        base_unit = (
            transport_capacity_pkm
            * ass("Ass_T_D_cycl_ratio_cargo_to_bikes")
            / ass("Ass_T_D_cycl_cargo_mlg")
        )
        invest = base_unit * invest_per_x
        CO2e_total_2021_estimated = t18.other_cycl.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_com = 0
        invest_pa = invest / duration_until_target_year
        invest_pa_com = invest_com / duration_until_target_year

        return cls(
            base_unit=base_unit,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            transport=Transport(
                CO2e_combustion_based=0,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=ZeroEnergyAndCO2e(
                    transport_capacity_pkm=t18.other_cycl.transport_capacity_pkm,
                    transport_capacity_tkm=0,
                ),
            ),
        )


@dataclass(kw_only=True)
class Other(InvestCommune):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float

    @classmethod
    def calc(
        cls,
        duration_until_target_year: int,
        *,
        t18: T18,
        other_foot: OtherFoot,
        other_cycl: OtherCycle,
        other_foot_action_infra: InvestmentAction,
        other_cycl_action_infra: InvestmentAction,
    ) -> "Other":
        sum = Transport.sum(
            other_foot.transport,
            other_cycl.transport,
            transport2018=ZeroEnergyAndCO2e(
                transport_capacity_pkm=t18.other.transport_capacity_pkm,
                transport_capacity_tkm=0,
            ),
        )

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
            other_cycl_action_infra.invest / duration_until_target_year
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
            transport=sum,
        )
