# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div
from ...transport2018.t18 import T18

from .transport import Transport


@dataclass(kw_only=True)
class ShipDomestic:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    base_unit: float
    cost_wage: float
    demand_emplo_new: float
    demand_emplo: float
    emplo_existing: float
    invest_pa: float
    invest_per_x: float
    invest: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(cls, inputs: Inputs, *, t18: T18) -> "ShipDomestic":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        transport_capacity_tkm = (
            ass("Ass_T_D_trnsprt_gds_ship_2050")
            * entries.m_population_com_203X
            / entries.m_population_nat
        )
        demand_ediesel = (
            ass("Ass_T_D_Shp_dmstc_nat_EB_2050")
            * entries.m_population_com_203X
            / entries.m_population_nat
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        )
        CO2e_total_2021_estimated = t18.ship_dmstc.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
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
        invest = base_unit * invest_per_x + cost_wage * entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
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
class ShipDomesticActionInfra:
    CO2e_total_2021_estimated: float
    cost_climate_saved: float
    cost_wage: float
    demand_ediesel: float
    demand_emplo: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(cls, inputs: Inputs) -> "ShipDomesticActionInfra":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        invest = (
            ass("Ass_T_C_invest_water_ways")
            * entries.m_population_com_203X
            / entries.m_population_nat
        )
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        demand_ediesel = 0
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        invest_pa = invest / entries.m_duration_target
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        invest_pa_com = invest_com / entries.m_duration_target
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
    def calc(cls, inputs: Inputs, *, t18: T18) -> "ShipInternational":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        CO2e_total_2021_estimated = t18.ship_inter.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        demand_ediesel = (
            ass("Ass_T_D_Shp_sea_nat_EB_2050")
            * entries.m_population_com_203X
            / entries.m_population_nat
        )
        CO2e_combustion_based = demand_ediesel * ass(
            "Ass_T_S_diesel_EmFa_tank_wheel_2050"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
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
class Ship:
    LIFT_INTO_RESULT_DICT = ["transport"]
    transport: Transport

    demand_emplo_new: float
    demand_emplo: float
    base_unit: float
    cost_wage: float
    emplo_existing: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

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
        )
