# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts, Assumptions
from ...utils import div
from ...common.invest import Invest, InvestCommune
from ...transport2018.t18 import T18

from .transport import Transport
from .investmentaction import InvestmentAction


@dataclass(kw_only=True)
class RailPeople(Invest):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    emplo_existing: float
    invest_per_x: float
    mileage: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc_metro(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        *,
        t18: T18,
        total_transport_capacity_pkm: float,
    ) -> "RailPeople":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_pkm = div(
            total_transport_capacity_pkm * t18.rail_ppl_metro.transport_capacity_pkm,
            (
                t18.road_bus.transport_capacity_pkm
                + t18.rail_ppl_distance.transport_capacity_pkm
                + t18.rail_ppl_metro.transport_capacity_pkm
            ),
        ) * (
            ass("Ass_T_D_trnsprt_ppl_city_pt_frac_2050")
            if area_kind == "city"
            else ass("Ass_T_D_trnsprt_ppl_smcty_pt_frac_2050")
            if area_kind == "smcty"
            else ass("Ass_T_D_trnsprt_ppl_rural_pt_frac_2050")
            if area_kind == "rural"
            else ass("Ass_T_D_trnsprt_ppl_nat_pt_frac_2050")
        )
        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_Rl_Metro_2050")
        demand_electricity = mileage * ass("Ass_T_S_Rl_Metro_SEC_fzkm_2050")
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        base_unit = (mileage - t18.rail_ppl_metro.mileage) / fact(
            "Fact_T_D_rail_metro_ratio_mlg_to_vehicle"
        )
        invest_per_x = fact("Fact_T_D_rail_metro_vehicle_invest")
        ratio_wage_to_emplo = ass("Ass_T_D_bus_metro_wage_driver")
        demand_emplo = mileage / fact("Fact_T_D_metro_ratio_mlg_to_driver")
        emplo_existing = t18.rail_ppl_metro.mileage / fact(
            "Fact_T_D_metro_ratio_mlg_to_driver"
        )
        demand_emplo_new = demand_emplo - emplo_existing
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest = base_unit * invest_per_x + cost_wage * duration_until_target_year
        CO2e_total_2021_estimated = t18.rail_ppl_metro.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_pa = invest / duration_until_target_year
        pct_of_wage = div(cost_wage, invest_pa)
        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            invest=invest,
            mileage=mileage,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=t18.rail_ppl_metro,
            ),
        )

    @classmethod
    def calc_distance(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        *,
        t18: T18,
        total_transport_capacity_pkm: float,
    ) -> "RailPeople":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_pkm = div(
            total_transport_capacity_pkm * t18.rail_ppl_distance.transport_capacity_pkm,
            t18.road_bus.transport_capacity_pkm
            + t18.rail_ppl_distance.transport_capacity_pkm
            + t18.rail_ppl_metro.transport_capacity_pkm,
        ) * (
            ass("Ass_T_D_trnsprt_ppl_city_pt_frac_2050")
            if area_kind == "city"
            else ass("Ass_T_D_trnsprt_ppl_smcty_pt_frac_2050")
            if area_kind == "smcty"
            else ass("Ass_T_D_trnsprt_ppl_rural_pt_frac_2050")
            if area_kind == "rural"
            else ass("Ass_T_D_trnsprt_ppl_nat_pt_frac_2050")
        )
        demand_electricity = transport_capacity_pkm * ass(
            "Ass_T_S_Rl_Train_ppl_long_elec_SEC_2050"
        )
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        mileage = transport_capacity_pkm / fact(
            "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        )
        base_unit = (mileage - t18.rail_ppl_distance.mileage) / fact(
            "Fact_T_D_rail_ppl_ratio_mlg_to_vehicle"
        )
        demand_emplo = mileage / fact("Fact_T_D_rail_ratio_mlg_to_driver")

        emplo_existing = t18.rail_ppl_distance.mileage / fact(
            "Fact_T_D_rail_ratio_mlg_to_driver"
        )
        demand_emplo_new = demand_emplo - emplo_existing
        ratio_wage_to_emplo = ass("Ass_T_D_rail_wage_driver")
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest_per_x = fact("Fact_T_D_rail_ppl_vehicle_invest")
        CO2e_total_2021_estimated = t18.rail_ppl_distance.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest = base_unit * invest_per_x + cost_wage * duration_until_target_year
        invest_pa = invest / duration_until_target_year
        pct_of_wage = div(cost_wage, invest_pa)
        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            invest=invest,
            mileage=mileage,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=t18.rail_ppl_distance,
            ),
        )


@dataclass(kw_only=True)
class RailPeopleMetroActionInfra(InvestCommune):
    base_unit: float
    emplo_existing: float
    invest_per_x: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        *,
        metro_transport_capacity_pkm: float,
    ) -> "RailPeopleMetroActionInfra":
        fact = facts.fact
        ass = assumptions.ass

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_ppl_metro")
        invest = metro_transport_capacity_pkm * invest_per_x
        base_unit = 0
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa = invest / duration_until_target_year
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        invest_pa_com = invest_com / duration_until_target_year
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        emplo_existing = 0  # nicht existent oder ausgelastet

        demand_emplo = cost_wage / ratio_wage_to_emplo
        demand_emplo_new = demand_emplo

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass(kw_only=True)
class RailPeopleSum(InvestCommune):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    emplo_existing: float
    mileage: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        rail_ppl_metro: RailPeople,
        rail_ppl_distance: RailPeople,
        rail_ppl_metro_action_infra: RailPeopleMetroActionInfra,
    ) -> "RailPeopleSum":
        base_unit = rail_ppl_distance.base_unit + rail_ppl_metro.base_unit
        invest_com = rail_ppl_metro_action_infra.invest_com
        mileage = rail_ppl_distance.mileage + rail_ppl_metro.mileage
        invest = (
            rail_ppl_distance.invest
            + rail_ppl_metro.invest
            + rail_ppl_metro_action_infra.invest
        )
        emplo_existing = (
            rail_ppl_distance.emplo_existing
            + rail_ppl_metro.emplo_existing
            + rail_ppl_metro_action_infra.emplo_existing
        )
        invest_pa = (
            rail_ppl_distance.invest_pa
            + rail_ppl_metro.invest_pa
            + rail_ppl_metro_action_infra.invest_pa
        )
        invest_pa_com = rail_ppl_metro_action_infra.invest_pa_com
        cost_wage = (
            rail_ppl_distance.cost_wage
            + rail_ppl_metro.cost_wage
            + rail_ppl_metro_action_infra.cost_wage
        )
        demand_emplo_new = (
            rail_ppl_distance.demand_emplo_new
            + rail_ppl_metro.demand_emplo_new
            + rail_ppl_metro_action_infra.demand_emplo_new
        )
        demand_emplo = (
            rail_ppl_distance.demand_emplo
            + rail_ppl_metro.demand_emplo
            + rail_ppl_metro_action_infra.demand_emplo
        )

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            invest=invest,
            invest_com=invest_com,
            invest_pa_com=invest_pa_com,
            invest_pa=invest_pa,
            mileage=mileage,
            transport=Transport.sum(
                rail_ppl_metro.transport,
                rail_ppl_distance.transport,
                transport2018=t18.rail_ppl,
            ),
        )


@dataclass(kw_only=True)
class RailGoods(Invest):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    emplo_existing: float
    invest_per_x: float
    pct_of_wage: float
    mileage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        *,
        t18: T18,
    ) -> "RailGoods":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_tkm = t18.rail_gds.transport_capacity_tkm * (
            ass("Ass_T_D_trnsprt_gds_Rl_2050")
            / fact("Fact_T_D_Rl_train_nat_trnsprt_gds_2018")
        )
        demand_electricity = transport_capacity_tkm * ass(
            "Ass_T_S_Rl_Train_gds_elec_SEC_2050"
        )
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        mileage = transport_capacity_tkm / fact(
            "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
        )
        CO2e_total_2021_estimated = t18.rail_gds.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        ratio_wage_to_emplo = ass("Ass_T_D_rail_wage_driver")
        demand_emplo = mileage / fact("Fact_T_D_rail_ratio_mlg_to_driver")
        emplo_existing = t18.rail_gds.mileage / fact(
            "Fact_T_D_rail_ratio_mlg_to_driver"
        )
        demand_emplo_new = demand_emplo - emplo_existing

        change_km = transport_capacity_tkm - t18.rail_gds.transport_capacity_tkm
        base_unit = change_km / fact("Fact_T_D_rail_gds_ratio_mlg_to_vehicle")
        invest_per_x = fact("Fact_T_D_rail_gds_vehicle_invest")
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest = base_unit * invest_per_x + cost_wage * duration_until_target_year
        invest_pa = invest / duration_until_target_year
        pct_of_wage = div(cost_wage, invest_pa)

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            mileage=mileage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=t18.rail_gds,
            ),
        )


@dataclass(kw_only=True)
class Rail(InvestCommune):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    mileage: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        rail_ppl: RailPeopleSum,
        rail_gds: RailGoods,
        rail_action_invest_infra: InvestmentAction,
        rail_action_invest_station: InvestmentAction,
    ) -> "Rail":
        invest_com = (
            rail_action_invest_infra.invest_com
            + rail_action_invest_station.invest_com
            + rail_ppl.invest_com
        )
        demand_emplo_new = (
            rail_action_invest_infra.demand_emplo_new
            + rail_action_invest_station.demand_emplo_new
            + rail_ppl.demand_emplo_new
            + rail_gds.demand_emplo_new
        )
        invest_pa_com = (
            rail_action_invest_infra.invest_pa_com
            + rail_action_invest_station.invest_pa_com
            + rail_ppl.invest_pa_com
        )
        mileage = rail_ppl.mileage + rail_gds.mileage
        base_unit = rail_ppl.base_unit + rail_gds.base_unit
        invest_pa = (
            rail_action_invest_infra.invest_pa
            + rail_action_invest_station.invest_pa
            + rail_ppl.invest_pa
            + rail_gds.invest_pa
        )
        demand_emplo = (
            rail_action_invest_infra.demand_emplo
            + rail_action_invest_station.demand_emplo
            + rail_ppl.demand_emplo
            + rail_gds.demand_emplo
        )
        cost_wage = (
            rail_action_invest_infra.cost_wage
            + rail_action_invest_station.cost_wage
            + rail_ppl.cost_wage
            + rail_gds.cost_wage
        )
        invest = (
            rail_action_invest_infra.invest
            + rail_action_invest_station.invest
            + rail_ppl.invest
            + rail_gds.invest
        )

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            mileage=mileage,
            transport=Transport.sum(
                rail_ppl.transport, rail_gds.transport, transport2018=t18.rail
            ),
        )
