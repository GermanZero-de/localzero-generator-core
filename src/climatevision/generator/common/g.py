# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import div


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
    ratio_wage_to_emplo: float

    @classmethod
    def calc_from_invest(
        cls, inputs: Inputs, invest: float, emplo_existing: float
    ) -> "GConsult":
        fact = inputs.fact
        entries = inputs.entries

        invest_pa = invest / entries.m_duration_target

        invest_commune = invest
        invest_pa_commune = invest_pa

        cost_wage = invest_pa

        ratio_wage_to_emplo = fact("Fact_R_G_energy_consulting_cost_personel")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        demand_emplo_new = max(0, demand_emplo - emplo_existing)
        demand_emplo_commune = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_commune,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_commune,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_commune,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_from_invest_calc_planning(
        cls, inputs: Inputs, invest: float
    ) -> "GConsult":
        entries = inputs.entries
        ass = inputs.ass
        fact = inputs.fact

        invest_pa = invest / entries.m_duration_target

        invest_commune = invest
        invest_pa_commune = invest_pa

        cost_wage = invest / fact("Fact_H_P_planning_duration")

        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        demand_emplo_new = demand_emplo
        demand_emplo_commune = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_commune,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_commune,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_commune,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_from_invest_calc_planning_with_invest_commune(
        cls, inputs: Inputs, invest: float
    ) -> "GConsult":
        ass = inputs.ass
        entries = inputs.entries

        invest_pa = invest / entries.m_duration_target

        invest_commune = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_commune = invest_commune / entries.m_duration_target

        cost_wage = invest_pa

        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        demand_emplo_new = demand_emplo
        demand_emplo_commune = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_commune,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_commune,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_commune,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_from_invest_pa(
        cls, inputs: Inputs, invest_pa: float, ratio_wage_to_emplo: float
    ) -> "GConsult":
        ass = inputs.ass
        entries = inputs.entries

        invest = invest_pa * entries.m_duration_target

        invest_pa_commune = invest_pa
        invest_commune = invest

        pct_of_wage = ass("Ass_I_G_advice_invest_pct_of_wage")
        cost_wage = invest_pa * pct_of_wage

        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        demand_emplo_new = demand_emplo
        demand_emplo_commune = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_commune,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_commune,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_commune,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_storage(cls, inputs: Inputs, energy: float) -> "GConsult":
        entries = inputs.entries
        fact = inputs.fact

        pct_energy = fact("Fact_H_P_storage_specific_volume")
        power_to_be_installed = energy * pct_energy

        invest_per_x = fact("Fact_H_P_storage_specific_cost")
        invest = invest_per_x * power_to_be_installed
        invest_pa = invest / entries.m_duration_target

        invest_commune = invest
        invest_pa_commune = invest_pa

        pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        cost_wage = pct_of_wage * invest_pa

        ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        demand_emplo_commune = 0

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_commune,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_commune,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_commune,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
