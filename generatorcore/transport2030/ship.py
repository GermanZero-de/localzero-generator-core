# pyright: strict

from dataclasses import dataclass
from ..inputs import Inputs
from ..utils import div
from ..transport2018 import T18

from .transport import Transport


@dataclass
class ShipDomestic(Transport):
    # Used by ship_dmstc
    base_unit: float
    cost_wage: float
    demand_ediesel: float
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
        energy = demand_ediesel
        CO2e_total = CO2e_combustion_based
        change_energy_MWh = energy - t18.ship_dmstc.energy
        change_energy_pct = div(change_energy_MWh, t18.ship_dmstc.energy)
        change_CO2e_t = CO2e_combustion_based - t18.ship_dmstc.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.ship_dmstc.CO2e_combustion_based)
        base_unit = change_km / fact("Fact_T_D_Shp_dmstc_nat_ratio_mlg_to_vehicle")
        invest_per_x = fact("Fact_T_D_Shp_dmstc_vehicle_invest")
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest = base_unit * invest_per_x + cost_wage * entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = div(cost_wage, invest_pa)

        return cls(
            base_unit=base_unit,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_total=CO2e_total,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_ediesel=demand_ediesel,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            energy=energy,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            invest=invest,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=0,
        )


@dataclass
class ShipDomesticActionInfra:
    # Used by ship_dmstc_action_infra
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


@dataclass
class ShipInternational(Transport):
    # Used by ship_inter
    demand_ediesel: float

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
        energy = demand_ediesel
        CO2e_total = CO2e_combustion_based
        change_energy_MWh = energy - t18.ship_inter.energy
        change_energy_pct = div(change_energy_MWh, t18.ship_inter.energy)
        change_CO2e_t = CO2e_combustion_based - t18.ship_inter.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.ship_inter.CO2e_combustion_based)
        transport_capacity_tkm = t18.ship_inter.transport_capacity_tkm * div(
            energy, t18.ship_inter.energy
        )
        change_km = transport_capacity_tkm - t18.ship_inter.transport_capacity_tkm

        return cls(
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_total=CO2e_total,
            cost_climate_saved=cost_climate_saved,
            demand_ediesel=demand_ediesel,
            energy=energy,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=0,
        )


@dataclass
class Ship(Transport):
    # Used by ship

    demand_ediesel: float
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
            ship_inter,
            ship_dmstc,
            energy_2018=t18.ship.energy,
            co2e_2018=t18.ship.CO2e_combustion_based,
        )

        invest = ship_dmstc_action_infra.invest + ship_dmstc.invest
        invest_com = ship_dmstc_action_infra.invest_com
        demand_ediesel = (
            ship_dmstc.demand_ediesel
            + ship_dmstc_action_infra.demand_ediesel
            + ship_inter.demand_ediesel
        )
        emplo_existing = ship_dmstc.emplo_existing
        base_unit = ship_dmstc.base_unit
        invest_pa = ship_dmstc_action_infra.invest_pa + ship_dmstc.invest_pa
        invest_pa_com = ship_dmstc_action_infra.invest_pa_com
        cost_wage = ship_dmstc.cost_wage + ship_dmstc_action_infra.cost_wage
        demand_emplo_new = (
            ship_dmstc.demand_emplo_new + ship_dmstc_action_infra.demand_emplo_new
        )
        demand_emplo = ship_dmstc.demand_emplo + ship_dmstc_action_infra.demand_emplo
        CO2e_total_2021_estimated = (
            sum.CO2e_total_2021_estimated
            + ship_dmstc_action_infra.CO2e_total_2021_estimated
        )
        cost_climate_saved = (
            sum.cost_climate_saved + ship_dmstc_action_infra.cost_climate_saved
        )
        return cls(
            CO2e_combustion_based=sum.CO2e_combustion_based,
            CO2e_total=sum.CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            base_unit=base_unit,
            change_km=sum.change_km,
            change_CO2e_pct=sum.change_CO2e_pct,
            change_CO2e_t=sum.change_CO2e_t,
            change_energy_MWh=sum.change_energy_MWh,
            change_energy_pct=sum.change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_ediesel=demand_ediesel,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            energy=sum.energy,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            transport_capacity_tkm=sum.transport_capacity_tkm,
            transport_capacity_pkm=sum.transport_capacity_pkm,
        )
