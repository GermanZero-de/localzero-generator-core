# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import div
from ..business2018.b18 import B18


@dataclass(kw_only=True)
class G:
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def sum(cls, *gs: "G") -> "G":
        return cls(
            cost_wage=sum(g.cost_wage for g in gs),
            demand_emplo=sum(g.demand_emplo for g in gs),
            demand_emplo_com=sum(g.demand_emplo_com for g in gs),
            demand_emplo_new=sum(g.demand_emplo_new for g in gs),
            invest=sum(g.invest for g in gs),
            invest_com=sum(g.invest_com for g in gs),
            invest_pa=sum(g.invest_pa for g in gs),
            invest_pa_com=sum(g.invest_pa_com for g in gs),
        )


@dataclass(kw_only=True)
class GConsult(G):
    emplo_existing: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc_for_business2030(cls, inputs: Inputs, b18: B18) -> "GConsult":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        invest = (
            fact("Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats")
            * b18.p_nonresi.number_of_buildings
        )
        invest_pa = invest / entries.m_duration_target

        invest_com = invest
        invest_pa_com = invest_pa

        cost_wage = invest_pa
        ratio_wage_to_emplo = fact("Fact_R_G_energy_consulting_cost_personel")

        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        emplo_existing = (
            fact("Fact_R_G_energy_consulting_total_personel")
            * ass("Ass_B_D_energy_consulting_emplo_pct_of_B")
            * entries.m_population_com_2018
            / entries.m_population_nat
        )
        demand_emplo_new = max(0, demand_emplo - emplo_existing)
        demand_emplo_com = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            emplo_existing=emplo_existing,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_for_industry2030(cls, inputs: Inputs) -> "GConsult":
        ass = inputs.ass
        entries = inputs.entries

        invest_pa = (
            ass("Ass_I_G_advice_invest_pa_per_capita") * entries.m_population_com_2018
        )
        invest = invest_pa * entries.m_duration_target

        invest_pa_com = invest_pa
        invest_com = invest

        pct_of_wage = ass("Ass_I_G_advice_invest_pct_of_wage")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")

        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        emplo_existing = 0

        demand_emplo_new = demand_emplo - emplo_existing
        demand_emplo_com = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            emplo_existing=emplo_existing,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_for_residences2030(cls, inputs: Inputs) -> "GConsult":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        invest = entries.r_buildings_le_2_apts * fact(
            "Fact_R_G_energy_consulting_cost_detached_house"
        ) + entries.r_buildings_ge_3_apts * fact(
            "Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats"
        )
        invest_pa = invest / entries.m_duration_target

        invest_com = invest
        invest_pa_com = invest_pa

        cost_wage = invest_pa
        ratio_wage_to_emplo = fact("Fact_R_G_energy_consulting_cost_personel")

        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        emplo_existing = (
            fact("Fact_R_G_energy_consulting_total_personel")
            * ass("Ass_B_D_energy_consulting_emplo_pct_of_R")
            * entries.m_population_com_2018
            / entries.m_population_nat
        )
        demand_emplo_new = max(0, demand_emplo - emplo_existing)
        demand_emplo_com = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            emplo_existing=emplo_existing,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
