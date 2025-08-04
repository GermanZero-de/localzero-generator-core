# pyright: strict

from dataclasses import dataclass

from ...common.invest import Invest, InvestCommune
from ...entries import Entries
from ...refdata import Assumptions, Facts
from ...transport2018.t18 import T18
from ...utils import div
from .transport import Transport


@dataclass(kw_only=True)
class ShipDomestic(Invest):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

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
        entries: Entries,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        population_commune_203X: int,
        population_germany_203X: int,
        *,
        t18: T18,
    ) -> "ShipDomestic":
        fact = facts.fact
        ass = assumptions.ass

        transport_capacity_tkm = (
            ass("Ass_T_D_trnsprt_gds_ship_2050")
            * entries.t_s_eev_fuel_overseas_mwh_com
            / entries.t_s_eev_fuel_overseas_mwh_total
        )
        demand_ediesel = (
            ass("Ass_T_D_Shp_dmstc_nat_EB_2050")
            * entries.t_s_eev_diesel_inland_mwh_com
            / entries.t_s_eev_diesel_inland_mwh_total
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        )
        CO2e_total_2021_estimated = t18.ship_dmstc.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        ratio_wage_to_emplo = ass("Ass_T_D_shp_wage_driver")
        demand_emplo = transport_capacity_tkm / fact("Fact_T_D_shp_ratio_mlg_to_driver")
        emplo_existing = t18.ship_dmstc.transport_capacity_tkm / fact(
            "Fact_T_D_shp_ratio_mlg_to_driver"
        )
        demand_emplo_new = demand_emplo - emplo_existing
        change_km = transport_capacity_tkm - t18.ship_dmstc.transport_capacity_tkm
        base_unit = change_km / fact("Fact_T_D_Shp_dmstc_nat_ratio_mlg_to_vehicle")
        invest_per_x = fact("Fact_T_D_Shp_dmstc_vehicle_invest")
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
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
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_ediesel=demand_ediesel,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=t18.ship_dmstc,
            ),
        )


@dataclass(kw_only=True)
class ShipDomesticActionInfra(InvestCommune):
    CO2e_total_2021_estimated: float
    cost_climate_saved: float
    demand_ediesel: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        duration_until_target_year: int,
        population_commune_203X: int,
        population_germany_203X: int,
    ) -> "ShipDomesticActionInfra":
        fact = facts.fact
        ass = assumptions.ass

        invest = (
            ass("Ass_T_C_invest_water_ways")
            * population_commune_203X
            / population_germany_203X
        )
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        demand_ediesel = 0
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        invest_pa = invest / duration_until_target_year
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        invest_pa_com = invest_com / duration_until_target_year
        demand_emplo = div(
            cost_wage,
            ratio_wage_to_emplo,
        )
        demand_emplo_new = demand_emplo
        CO2e_total_2021_estimated = 0
        cost_climate_saved = 0

        return cls(
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_ediesel=demand_ediesel,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass(kw_only=True)
class ShipInternational:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        entries: Entries,
        duration_CO2e_neutral_years: float,
        population_commune_203X: int,
        population_germany_203X: int,
        *,
        t18: T18,
    ) -> "ShipInternational":
        fact = facts.fact
        ass = assumptions.ass

        CO2e_total_2021_estimated = t18.ship_inter.CO2e_combustion_based * fact(
            f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
        )
        demand_ediesel = (
            ass("Ass_T_D_Shp_sea_nat_EB_2050")
            * entries.t_s_eev_fuel_overseas_mwh_com
            / entries.t_s_eev_fuel_overseas_mwh_total
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        transport_capacity_tkm = t18.ship_inter.transport_capacity_tkm * div(
            demand_ediesel, t18.ship_inter.energy
        )

        return cls(
            transport=Transport(
                CO2e_combustion_based=CO2e_combustion_based,
                CO2e_total_2021_estimated=CO2e_total_2021_estimated,
                cost_climate_saved=cost_climate_saved,
                demand_ediesel=demand_ediesel,
                transport_capacity_tkm=transport_capacity_tkm,
                transport_capacity_pkm=0,
                transport2018=t18.ship_inter,
            )
        )


@dataclass(kw_only=True)
class Ship(InvestCommune):
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    emplo_existing: float
    dmstc_action_infra: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        ship_inter: ShipInternational,
        ship_dmstc: ShipDomestic,
        ship_dmstc_action_infra: ShipDomesticActionInfra,
    ) -> "Ship":
        sum = Transport.sum(
            ship_inter.transport, ship_dmstc.transport, transport2018=t18.ship
        )
        # This additional values are all 0 anyway, so the computation below
        # that were in the original excel were not needed. For now I'm leaving
        # them in here until I have either convinced myself that the corresponding
        # variables should just completely disappear from ShipDomesticActionInfra
        # or I have some better plan.
        # demand_ediesel = sum + ship_dmstc_action_infra.demand_ediesel
        # CO2e_total_2021_estimated = (
        #     sum.CO2e_total_2021_estimated
        #     + ship_dmstc_action_infra.CO2e_total_2021_estimated
        # )
        # cost_climate_saved = (
        #     sum.cost_climate_saved + ship_dmstc_action_infra.cost_climate_saved
        # )

        invest = ship_dmstc_action_infra.invest + ship_dmstc.invest
        invest_com = ship_dmstc_action_infra.invest_com
        emplo_existing = ship_dmstc.emplo_existing
        base_unit = ship_dmstc.base_unit
        invest_pa = ship_dmstc_action_infra.invest_pa + ship_dmstc.invest_pa
        invest_pa_com = ship_dmstc_action_infra.invest_pa_com
        cost_wage = ship_dmstc.cost_wage + ship_dmstc_action_infra.cost_wage
        demand_emplo_new = (
            ship_dmstc.demand_emplo_new + ship_dmstc_action_infra.demand_emplo_new
        )
        demand_emplo = ship_dmstc.demand_emplo + ship_dmstc_action_infra.demand_emplo
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
            transport=sum,
            dmstc_action_infra=ship_dmstc_action_infra.invest_com,
        )
