# pyright: strict
from dataclasses import dataclass
from typing import Any

from ..utils import div
from ..agri2018.a18 import A18
from ..inputs import Inputs


@dataclass
class CO2eChangeA:
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation: Any,
        p: Any,
        g: Any,
        s: Any,
    ) -> "CO2eChangeA":

        CO2e_production_based = p.CO2e_production_based
        CO2e_combustion_based = s.CO2e_combustion_based
        CO2e_total = g.CO2e_total + p.CO2e_total + s.CO2e_total

        CO2e_total_2021_estimated = getattr(a18, what).CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        invest_pa_outside = g.invest_pa_outside
        invest_outside = g.invest_outside
        invest_com = g.invest_com
        invest = g.invest + s.invest + p.invest
        invest_pa_com = g.invest_pa_com
        invest_pa = invest / inputs.entries.m_duration_target

        change_CO2e_t = CO2e_total - getattr(a18, what).CO2e_total
        change_CO2e_pct = div(change_CO2e_t, a18.a.CO2e_total)
        change_energy_MWh = p_operation.change_energy_MWh
        change_energy_pct = p_operation.change_energy_pct

        demand_emplo = g.demand_emplo + p.demand_emplo + s.demand_emplo
        demand_emplo_new = g.demand_emplo_new + p.demand_emplo_new + s.demand_emplo_new
        demand_emplo_com = g.demand_emplo_com

        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )

        cost_wage = g.cost_wage + p.cost_wage + s.cost_wage

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_outside=invest_outside,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_pa_outside=invest_pa_outside,
        )


@dataclass
class CO2eChangeG:
    CO2e_total: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore

    @classmethod
    def calc(cls, g_consult: Any, g_organic: Any) -> "CO2eChangeG":
        CO2e_total = 0
        cost_wage = g_consult.cost_wage + g_organic.cost_wage

        demand_emplo = g_consult.demand_emplo + g_organic.demand_emplo
        demand_emplo_new = g_consult.demand_emplo_new + g_organic.demand_emplo_new
        demand_emplo_com = g_consult.demand_emplo_com

        invest = g_consult.invest + g_organic.invest
        invest_com = g_consult.invest_com
        invest_outside = 0

        invest_pa = g_consult.invest_pa + g_organic.invest_pa
        invest_pa_com = g_consult.invest_pa_com
        invest_pa_outside = 0

        return cls(
            CO2e_total=CO2e_total,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_outside=invest_outside,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_pa_outside=invest_pa_outside,
        )


@dataclass
class CO2eChangeGConsult:
    area_ha_available: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore

    @classmethod
    def calc(cls, inputs: Inputs) -> "CO2eChangeGConsult":
        area_ha_available = inputs.entries.a_farm_amount

        invest_per_x = inputs.ass("Ass_A_G_consult_invest_per_farm")
        invest = area_ha_available * invest_per_x
        invest_com = invest * inputs.ass("Ass_A_G_consult_invest_pct_of_public")
        invest_pa = invest / inputs.entries.m_duration_target
        invest_pa_com = invest_pa * inputs.ass("Ass_A_G_consult_invest_pct_of_public")

        pct_of_wage = inputs.ass("Ass_A_G_consult_invest_pct_of_wage")
        cost_wage = invest_pa * pct_of_wage

        ratio_wage_to_emplo = inputs.ass("Ass_A_G_consult_ratio_wage_to_emplo")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
        demand_emplo_com = demand_emplo_new

        return cls(
            area_ha_available=area_ha_available,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class CO2eChangeGOrganic:
    area_ha_available: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    power_to_be_installed_pct: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore

    @classmethod
    def calc(cls, inputs: Inputs) -> "CO2eChangeGOrganic":
        area_ha_available = inputs.entries.m_area_agri_com

        power_installed = inputs.entries.a_area_agri_com_pct_of_organic
        power_to_be_installed_pct = inputs.ass("Ass_A_G_area_agri_pct_of_organic_2050")
        power_to_be_installed = area_ha_available * (
            power_to_be_installed_pct - power_installed
        )

        invest_per_x = inputs.ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
        invest = power_to_be_installed * invest_per_x
        invest_pa = invest / inputs.entries.m_duration_target

        pct_of_wage = inputs.fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        cost_wage = invest_pa * pct_of_wage

        ratio_wage_to_emplo = inputs.fact(
            "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
        )
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        return cls(
            area_ha_available=area_ha_available,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            power_installed=power_installed,
            power_to_be_installed=power_to_be_installed,
            power_to_be_installed_pct=power_to_be_installed_pct,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
