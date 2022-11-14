# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div

from ..energy_demand import (
    InvestmentAction,
    RailPeopleMetroActionInfra,
    OtherCycle,
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
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        road_bus_action_infra: InvestmentAction,
        road_gds_mhd_action_wire: InvestmentAction,
        road_action_charger: InvestmentAction,
        rail_ppl_metro_action_infra: RailPeopleMetroActionInfra,
        rail_action_invest_infra: InvestmentAction,
        other_cycl: OtherCycle,
    ) -> "GPlanning":
        ass = inputs.ass
        entries = inputs.entries

        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
        invest = ass("Ass_T_C_planer_cost_per_invest_cost") * (
            road_bus_action_infra.invest
            + road_gds_mhd_action_wire.invest
            + road_action_charger.invest
            + rail_ppl_metro_action_infra.invest
            + rail_action_invest_infra.invest
            + other_cycl.invest
        )
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_com = invest_com / entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        cost_wage = invest_pa
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
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
