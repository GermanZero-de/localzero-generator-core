# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div


@dataclass(kw_only=True)
class GStorage:
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    invest_per_x: float
    pct_energy: float
    pct_of_wage: float
    power_to_be_installed: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(cls, inputs: Inputs, p_heatnet_energy: float) -> "GStorage":
        entries = inputs.entries
        fact = inputs.fact

        energy = p_heatnet_energy
        pct_energy = fact("Fact_H_P_storage_specific_volume")
        power_to_be_installed = energy * pct_energy

        invest_per_x = fact("Fact_H_P_storage_specific_cost")
        invest = invest_per_x * power_to_be_installed
        invest_pa = invest / entries.m_duration_target

        invest_com = invest
        invest_pa_com = invest_pa

        pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        cost_wage = pct_of_wage * invest_pa

        ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_energy=pct_energy,
            pct_of_wage=pct_of_wage,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass(kw_only=True)
class GPlanning:
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(cls, inputs: Inputs) -> "GPlanning":
        entries = inputs.entries
        ass = inputs.ass
        fact = inputs.fact

        invest = (
            fact("Fact_H_P_planning_cost_basis")
            + fact("Fact_H_P_planning_cost_per_capita") * entries.m_population_com_2018
        )
        invest_pa = invest / entries.m_duration_target

        invest_com = invest
        invest_pa_com = invest_pa

        pct_of_wage = ass("Ass_H_G_planning_cost_pct_of_wage")
        cost_wage = invest / fact("Fact_H_P_planning_duration")

        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
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
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
