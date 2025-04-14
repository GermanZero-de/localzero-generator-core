# pyright: strict

from dataclasses import asdict, dataclass

from ...common.invest import InvestCommune
from ...refdata import Assumptions, Facts
from ...transport2018.t18 import T18
from ...utils import div
from .investmentaction import InvestmentAction, RoadInvestmentAction
from .transport import Transport


@dataclass(kw_only=True)
class TransportInvestments:
    """For every mechanism of transport, we compute some basic investment
    costs.
    """

    base_unit: float

    invest: float
    invest_pa: float
    invest_per_x: float


@dataclass(kw_only=True)
class Road:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    mileage: float

    @classmethod
    def calc_goods_lightduty_it_ot(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        *,
        t18: T18,
    ) -> "Road":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_tkm = (
            ass("Ass_T_D_trnsprt_gds_Rd_2050")
            / fact("Fact_T_D_trnsprt_gds_Rd_2018")
            * t18.road_gds_ldt_it_ot.transport_capacity_tkm
        )
        mileage = transport_capacity_tkm / ass("Ass_T_D_lf_gds_LDT_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_LDT_frac_bev_mlg_2050")
            * ass("Ass_T_S_LDT_SEC_elec_it_ot_2030")
        )
        demand_ediesel = (
            mileage
            * ass("Ass_T_S_LDT_frac_diesel_mlg_2050")
            * ass("Ass_T_S_LDT_SEC_diesel_it_ot_2030")
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        demand_hydrogen = (
            mileage
            * ass("Ass_T_S_LDT_frac_fcev_mlg_2050")
            * ass("Ass_T_S_LDT_SEC_fcev_2030")
        )

        CO2e_total_2021_estimated = t18.road_gds_ldt_it_ot.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                demand_ediesel=demand_ediesel,
                demand_hydrogen=demand_hydrogen,
                demand_epetrol=0,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=t18.road_gds_ldt_it_ot,
            ),
        )

    @classmethod
    def calc_goods_lightduty_ab(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        *,
        t18: T18,
    ) -> "Road":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_tkm = (
            ass("Ass_T_D_trnsprt_gds_Rd_2050")
            / fact("Fact_T_D_trnsprt_gds_Rd_2018")
            * t18.road_gds_ldt_ab.transport_capacity_tkm
        )
        mileage = transport_capacity_tkm / ass("Ass_T_D_lf_gds_LDT_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_LDT_frac_bev_mlg_2050")
            * ass("Ass_T_S_LDT_SEC_elec_ab_2030")
        )
        demand_hydrogen = (
            mileage
            * ass("Ass_T_S_LDT_frac_fcev_mlg_2050")
            * ass("Ass_T_S_LDT_SEC_fcev_2030")
        )
        demand_ediesel = (
            mileage
            * ass("Ass_T_S_LDT_frac_diesel_mlg_2050")
            * ass("Ass_T_S_LDT_SEC_diesel_ab_2030")
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        CO2e_total_2021_estimated = t18.road_gds_ldt_ab.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                demand_ediesel=demand_ediesel,
                demand_hydrogen=demand_hydrogen,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=(t18.road_gds_ldt_ab),
            ),
        )

    @classmethod
    def calc_goods_medium_and_heavy_duty_ab(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        *,
        t18: T18,
    ) -> "Road":
        fact = facts.fact
        ass = assumptions.ass

        CO2e_total_2021_estimated = t18.road_gds_mhd_ab.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        transport_capacity_tkm = (
            ass("Ass_T_D_trnsprt_gds_Rd_2050")
            / fact("Fact_T_D_trnsprt_gds_Rd_2018")
            * t18.road_gds_mhd_ab.transport_capacity_tkm
        )
        mileage = transport_capacity_tkm / ass("Ass_T_D_lf_gds_MHD_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_MHD_frac_bev_mlg_2050")
            * ass("Ass_T_S_MHD_SEC_elec_ab_2030")
        )
        demand_ediesel = (
            mileage
            * ass("Ass_T_S_MHD_frac_diesel_mlg_2050")
            * ass("Ass_T_S_MHD_SEC_diesel_ab_2030")
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        demand_hydrogen = (
            mileage
            * ass("Ass_T_S_MHD_frac_fcev_mlg_2050")
            * ass("Ass_T_S_MHD_SEC_fcev_2030")
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                demand_ediesel=demand_ediesel,
                demand_hydrogen=demand_hydrogen,
                demand_epetrol=0,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=(t18.road_gds_mhd_ab),
            ),
        )

    @classmethod
    def calc_goods_medium_and_heavy_duty_it_ot(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        *,
        t18: T18,
    ) -> "Road":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_tkm = (
            ass("Ass_T_D_trnsprt_gds_Rd_2050")
            / fact("Fact_T_D_trnsprt_gds_Rd_2018")
            * t18.road_gds_mhd_it_ot.transport_capacity_tkm
        )
        mileage = transport_capacity_tkm / ass("Ass_T_D_lf_gds_MHD_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_MHD_frac_bev_mlg_2050")
            * ass("Ass_T_S_MHD_SEC_elec_it_ot_2030")
        )
        demand_ediesel = (
            mileage
            * ass("Ass_T_S_MHD_frac_diesel_mlg_2050")
            * ass("Ass_T_S_MHD_SEC_diesel_it_ot_2030")
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        demand_hydrogen = (
            mileage
            * ass("Ass_T_S_MHD_frac_fcev_mlg_2050")
            * ass("Ass_T_S_MHD_SEC_fcev_2030")
        )

        CO2e_total_2021_estimated = t18.road_gds_mhd_it_ot.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                demand_ediesel=demand_ediesel,
                demand_hydrogen=demand_hydrogen,
                demand_epetrol=0,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=(t18.road_gds_mhd_it_ot),
            ),
        )

    @classmethod
    def calc_car_it_ot(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        *,
        t18: T18,
        required_domestic_transport_capacity_pkm: float,
    ) -> "Road":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_pkm = (
            required_domestic_transport_capacity_pkm
            * div(
                t18.road_car_it_ot.mileage,
                t18.road_car_it_ot.mileage + t18.road_car_ab.mileage,
            )
            * (
                (
                    ass("Ass_T_D_trnsprt_ppl_city_car1_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_city_car2_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_city_car3_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_city_car4_frac_2050")
                    if area_kind == "city"
                    else (
                        ass("Ass_T_D_trnsprt_ppl_smcty_car1_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_smcty_car2_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_smcty_car3_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_smcty_car4_frac_2050")
                        if area_kind == "smcty"
                        else (
                            ass("Ass_T_D_trnsprt_ppl_rural_car1_frac_2050")
                            + ass("Ass_T_D_trnsprt_ppl_rural_car2_frac_2050")
                            + ass("Ass_T_D_trnsprt_ppl_rural_car3_frac_2050")
                            + ass("Ass_T_D_trnsprt_ppl_rural_car4_frac_2050")
                            if area_kind == "rural"
                            else ass("Ass_T_D_trnsprt_ppl_nat_car1_frac_2050")
                            + ass("Ass_T_D_trnsprt_ppl_nat_car2_frac_2050")
                            + ass("Ass_T_D_trnsprt_ppl_nat_car3_frac_2050")
                            + ass("Ass_T_D_trnsprt_ppl_nat_car4_frac_2050")
                        )
                    )
                )
            )
        )
        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_ppl_Car_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_Car_frac_bev_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_elec_it_ot_2030")
        )
        demand_epetrol = (
            mileage
            * ass("Ass_T_S_Car_frac_petrol_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_petrol_it_ot_2050")
        )
        CO2e_combustion_based = demand_epetrol * ass(
            "Ass_T_S_petrol_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        CO2e_total_2021_estimated = t18.road_car_it_ot.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                demand_epetrol=demand_epetrol,
                demand_hydrogen=0,
                demand_ediesel=0,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=t18.road_car_it_ot,
            ),
        )

    @classmethod
    def calc_car_ab(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        *,
        t18: T18,
        required_domestic_transport_capacity_pkm: float,
    ) -> "Road":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_pkm = (
            required_domestic_transport_capacity_pkm
            * div(
                t18.road_car_ab.mileage,
                (t18.road_car_it_ot.mileage + t18.road_car_ab.mileage),
            )
            * (
                ass("Ass_T_D_trnsprt_ppl_city_car1_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_city_car2_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_city_car3_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_city_car4_frac_2050")
                if area_kind == "city"
                else (
                    ass("Ass_T_D_trnsprt_ppl_smcty_car1_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_smcty_car2_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_smcty_car3_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_smcty_car4_frac_2050")
                    if area_kind == "smcty"
                    else (
                        ass("Ass_T_D_trnsprt_ppl_rural_car1_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_rural_car2_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_rural_car3_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_rural_car4_frac_2050")
                        if area_kind == "rural"
                        else ass("Ass_T_D_trnsprt_ppl_nat_car1_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_nat_car2_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_nat_car3_frac_2050")
                        + ass("Ass_T_D_trnsprt_ppl_nat_car4_frac_2050")
                    )
                )
            )
        )
        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_ppl_Car_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_Car_frac_bev_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_elec_ab_2030")
        )
        demand_epetrol = (
            mileage
            * ass("Ass_T_S_Car_frac_petrol_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_petrol_ab_2050")
        )
        CO2e_combustion_based = demand_epetrol * ass(
            "Ass_T_S_petrol_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        CO2e_total_2021_estimated = t18.road_car_ab.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                demand_epetrol=demand_epetrol,
                demand_hydrogen=0,
                demand_ediesel=0,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=(t18.road_car_ab),
            ),
        )


@dataclass(kw_only=True)
class RoadCar(Road):
    LIFT_INTO_RESULT_DICT = ["transport", "fleet_modernisation_cost"]
    fleet_modernisation_cost: TransportInvestments

    @staticmethod
    def calc_cost_modernisation_of_fleet(
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        *,
        sum_it_ot_ab: Transport,
    ) -> TransportInvestments:
        """Many cars will have to be replaced."""
        fact = facts.fact
        ass = assumptions.ass

        base_unit = sum_it_ot_ab.transport_capacity_pkm / fact(
            "Fact_T_S_Car_ratio_mlg_to_stock_2018"
        )
        invest_per_x = ass("Ass_T_S_car_average_price_2050")
        invest = base_unit * invest_per_x
        invest_pa = invest / duration_until_target_year

        return TransportInvestments(
            base_unit=base_unit,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
        )

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        *,
        t18: T18,
        it_ot: Road,
        ab: Road,
    ) -> "RoadCar":
        sum = Transport.sum(it_ot.transport, ab.transport, transport2018=t18.road_car)
        return cls(
            mileage=it_ot.mileage + ab.mileage,
            transport=sum,
            fleet_modernisation_cost=cls.calc_cost_modernisation_of_fleet(
                facts, assumptions, duration_until_target_year, sum_it_ot_ab=sum
            ),
        )


@dataclass(kw_only=True)
class BusInvestments(TransportInvestments):
    cost_wage: float
    demand_emplo_new: float
    demand_emplo: float
    emplo_existing: float
    invest_com: float
    invest_pa_com: float
    pct_of_wage: float
    ratio_wage_to_emplo: float


@dataclass(kw_only=True)
class RoadBus(Road, BusInvestments):
    @staticmethod
    def calc_action_infra(
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        *,
        bus_transport_capacity_pkm: float,
    ) -> InvestmentAction:
        """Costs of bus stations and similar."""
        fact = facts.fact
        ass = assumptions.ass

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_ppl_bus_infrstrctr")
        invest = bus_transport_capacity_pkm * invest_per_x
        invest_pa = invest / duration_until_target_year
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_com = invest_com / duration_until_target_year
        return InvestmentAction(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @staticmethod
    def calc_bus_investments(
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        *,
        t18: T18,
        mileage: float,
    ) -> BusInvestments:
        """Cost of buses and bus drivers"""
        fact = facts.fact
        ass = assumptions.ass

        base_unit = mileage / fact("Fact_T_S_Bus_ratio_mlg_to_stock_2018")
        invest_per_x = ass("Ass_T_S_bus_average_price_2050")
        ratio_wage_to_emplo = ass("Ass_T_D_bus_metro_wage_driver")
        demand_emplo = mileage / fact("Fact_T_S_bus_ratio_mlg_to_driver_2018")
        emplo_existing = div(t18.road_bus.mileage, mileage) * demand_emplo
        demand_emplo_new = demand_emplo - emplo_existing
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest = base_unit * invest_per_x + cost_wage * duration_until_target_year
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa = invest / duration_until_target_year
        pct_of_wage = div(cost_wage, invest_pa)
        invest_pa_com = invest_com / duration_until_target_year
        return BusInvestments(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            invest_com=invest_com,
            invest=invest,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        year_baseline: int,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        area_kind: str,
        *,
        t18: T18,
        total_transport_capacity_pkm: float,
    ) -> "RoadBus":
        fact = facts.fact
        ass = assumptions.ass

        t18_public_transport_capacity_pkm = (
            t18.road_bus.transport_capacity_pkm
            + t18.rail_ppl_distance.transport_capacity_pkm
            + t18.rail_ppl_metro.transport_capacity_pkm
        )
        public_transport_ppl_frac_2050 = (
            ass("Ass_T_D_trnsprt_ppl_city_pt_frac_2050")
            if area_kind == "city"
            else (
                ass("Ass_T_D_trnsprt_ppl_smcty_pt_frac_2050")
                if area_kind == "smcty"
                else (
                    ass("Ass_T_D_trnsprt_ppl_rural_pt_frac_2050")
                    if area_kind == "rural"
                    else ass("Ass_T_D_trnsprt_ppl_nat_pt_frac_2050")
                )
            )
        )

        import math

        if not math.isclose(t18_public_transport_capacity_pkm, 0):
            transport_capacity_pkm = (
                div(
                    total_transport_capacity_pkm * t18.road_bus.transport_capacity_pkm,
                    t18_public_transport_capacity_pkm,
                )
                * public_transport_ppl_frac_2050
            )
        else:
            transport_capacity_pkm = (
                total_transport_capacity_pkm * public_transport_ppl_frac_2050
            )

        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_ppl_Bus_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_bus_frac_bev_mlg_2050")
            * ass("Ass_T_S_Bus_SEC_elec_2030")
        )
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )

        CO2e_total_2021_estimated = t18.road_bus.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            mileage=mileage,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_electricity=demand_electricity,
                transport_capacity_pkm=transport_capacity_pkm,
                transport_capacity_tkm=0,
                transport2018=t18.road_bus,
            ),
            **asdict(
                cls.calc_bus_investments(
                    facts,
                    assumptions,
                    duration_until_target_year,
                    t18=t18,
                    mileage=mileage,
                )
            ),
        )


@dataclass(kw_only=True)
class RoadPeople(Road, InvestCommune):
    base_unit: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        car: RoadCar,
        bus: RoadBus,
        road_bus_action_infra: InvestmentAction,
    ) -> "RoadPeople":

        sum = Transport.sum(car.transport, bus.transport, transport2018=t18.road_ppl)

        demand_emplo_new = bus.demand_emplo_new + road_bus_action_infra.demand_emplo_new
        invest = (
            car.fleet_modernisation_cost.invest
            + bus.invest
            + road_bus_action_infra.invest
        )
        invest_com = bus.invest_com + road_bus_action_infra.invest_com
        base_unit = car.fleet_modernisation_cost.base_unit + bus.base_unit
        invest_pa = (
            car.fleet_modernisation_cost.invest_pa
            + bus.invest_pa
            + road_bus_action_infra.invest_pa
        )
        invest_pa_com = bus.invest_pa_com + road_bus_action_infra.invest_pa_com
        cost_wage = bus.cost_wage + road_bus_action_infra.cost_wage
        demand_emplo = bus.demand_emplo + road_bus_action_infra.demand_emplo

        return cls(
            mileage=car.mileage + bus.mileage,
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest_com=invest_com,
            invest=invest,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            transport=sum,
        )


@dataclass(kw_only=True)
class RoadGoodsMediumAndHeavyDuty(Road):
    base_unit: float
    demand_emplo_new: float
    demand_emplo: float
    emplo_existing: float
    invest_pa: float
    invest_per_x: float
    invest: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        t18: T18,
        it_ot: Road,
        ab: Road,
    ) -> "RoadGoodsMediumAndHeavyDuty":
        fact = facts.fact
        ass = assumptions.ass

        sum = Transport.sum(
            it_ot.transport, ab.transport, transport2018=t18.road_gds_mhd
        )
        mileage = it_ot.mileage + ab.mileage

        demand_emplo = mileage / fact("Fact_T_D_MHD_ratio_mlg_to_driver")
        emplo_existing = (
            t18.road_gds_mhd_it_ot.mileage + t18.road_gds_mhd_ab.mileage
        ) / fact("Fact_T_D_MHD_ratio_mlg_to_driver")
        demand_emplo_new = demand_emplo - emplo_existing
        base_unit = (sum.transport_capacity_tkm) / fact(
            "Fact_T_S_MHD_ratio_mlg_to_stock_2018"
        )
        invest_per_x = ass("Ass_T_S_MHCV_BEV_FCEV_average_price_2050")
        invest = base_unit * invest_per_x
        invest_pa = invest / duration_until_target_year
        return cls(
            mileage=it_ot.mileage + ab.mileage,
            base_unit=base_unit,
            emplo_existing=emplo_existing,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            transport=sum,
        )

    @staticmethod
    def calc_action_wire(
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        population_commune_203X: int,
    ) -> InvestmentAction:
        fact = facts.fact
        ass = assumptions.ass

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_gds_truck_infrstrctr")
        invest = population_commune_203X * invest_per_x
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa = invest / duration_until_target_year
        invest_pa_com = invest_com / duration_until_target_year
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
        return InvestmentAction(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass(kw_only=True)
class RoadGoodsLightDuty(Road):
    base_unit: float

    invest_pa: float
    invest_per_x: float
    invest: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        *,
        t18: T18,
        it_ot: Road,
        ab: Road,
    ) -> "RoadGoodsLightDuty":
        fact = facts.fact
        ass = assumptions.ass

        sum = Transport.sum(
            ab.transport, it_ot.transport, transport2018=t18.road_gds_ldt
        )

        base_unit = (sum.transport_capacity_tkm) / fact(
            "Fact_T_S_LDT_ratio_mlg_to_stock_2018"
        )
        invest_per_x = ass("Ass_T_S_LCV_average_price_2050")
        invest = base_unit * invest_per_x
        invest_pa = invest / duration_until_target_year
        return cls(
            base_unit=base_unit,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            mileage=ab.mileage + it_ot.mileage,
            transport=sum,
        )


@dataclass(kw_only=True)
class RoadGoods(Road, InvestCommune):
    base_unit: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        ldt: RoadGoodsLightDuty,
        mhd: RoadGoodsMediumAndHeavyDuty,
        road_gds_mhd_action_wire: InvestmentAction,
    ) -> "RoadGoods":
        sum = Transport.sum(ldt.transport, mhd.transport, transport2018=t18.road_gds)

        base_unit = ldt.base_unit + mhd.base_unit
        demand_emplo_new = mhd.demand_emplo_new
        demand_emplo = road_gds_mhd_action_wire.demand_emplo + mhd.demand_emplo
        invest_pa = road_gds_mhd_action_wire.invest_pa + ldt.invest_pa + mhd.invest_pa
        invest_com = road_gds_mhd_action_wire.invest_com
        invest_pa_com = road_gds_mhd_action_wire.invest_pa_com
        invest = ldt.invest + mhd.invest

        return cls(
            base_unit=base_unit,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            cost_wage=road_gds_mhd_action_wire.cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            mileage=ldt.mileage + mhd.mileage,
            transport=sum,
        )


@dataclass(kw_only=True)
class RoadSum(Road, InvestCommune):
    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        goods: RoadGoods,
        people: RoadPeople,
        road_action_charger: RoadInvestmentAction,
    ) -> "RoadSum":
        sum = Transport.sum(goods.transport, people.transport, transport2018=t18.road)
        demand_emplo_new = (
            road_action_charger.demand_emplo_new
            + people.demand_emplo_new
            + goods.demand_emplo_new
        )
        cost_wage = road_action_charger.cost_wage + people.cost_wage + goods.cost_wage
        invest_pa_com = (
            road_action_charger.invest_pa_com
            + people.invest_pa_com
            + goods.invest_pa_com
        )
        invest_com = (
            road_action_charger.invest_com + people.invest_com + goods.invest_com
        )

        invest = road_action_charger.invest + people.invest + goods.invest
        invest_pa = road_action_charger.invest_pa + people.invest_pa + goods.invest_pa
        demand_emplo = (
            road_action_charger.demand_emplo + people.demand_emplo + goods.demand_emplo
        )
        return cls(
            invest_com=invest_com,
            invest_pa_com=invest_pa_com,
            invest_pa=invest_pa,
            invest=invest,
            cost_wage=cost_wage,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            mileage=people.mileage + goods.mileage,
            transport=sum,
        )
