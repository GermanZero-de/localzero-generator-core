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
    emplo_existing: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc_from_invest(
        cls, inputs: Inputs, invest: float, emplo_existing: float
    ) -> "GConsult":
        fact = inputs.fact
        entries = inputs.entries

        invest_pa = invest / entries.m_duration_target

        invest_com = invest
        invest_pa_com = invest_pa

        cost_wage = invest_pa

        ratio_wage_to_emplo = fact("Fact_R_G_energy_consulting_cost_personel")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

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
    def calc_from_invest_pa(
        cls, inputs: Inputs, invest_pa: float, ratio_wage_to_emplo: float
    ) -> "GConsult":
        ass = inputs.ass
        entries = inputs.entries

        invest = invest_pa * entries.m_duration_target

        invest_pa_com = invest_pa
        invest_com = invest

        pct_of_wage = ass("Ass_I_G_advice_invest_pct_of_wage")
        cost_wage = invest_pa * pct_of_wage

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