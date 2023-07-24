# pyright: strict

from dataclasses import dataclass

from .e_col_vars_2030 import EColVars2030


@dataclass(kw_only=True)
class G:
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_pa: float = 0
    invest_outside: float = 0
    invest_pa_outside: float = 0

    @classmethod
    def calc_g(
        cls,
        g_grid_offshore: EColVars2030,
        g_grid_onshore: EColVars2030,
        g_grid_pv: EColVars2030,
    ) -> "G":
        invest_outside = g_grid_offshore.invest_outside
        invest_pa_outside = g_grid_offshore.invest_pa_outside
        invest = g_grid_offshore.invest + g_grid_onshore.invest + g_grid_pv.invest
        invest_pa = (
            g_grid_offshore.invest_pa + g_grid_onshore.invest_pa + g_grid_pv.invest_pa
        )
        cost_wage = (
            g_grid_offshore.cost_wage + g_grid_onshore.cost_wage + g_grid_pv.cost_wage
        )
        demand_emplo = (
            g_grid_offshore.demand_emplo
            + g_grid_onshore.demand_emplo
            + g_grid_pv.demand_emplo
        )
        demand_emplo_new = (
            g_grid_offshore.demand_emplo_new
            + g_grid_onshore.demand_emplo_new
            + g_grid_pv.demand_emplo_new
        )
        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_pa=invest_pa,
            invest_outside=invest_outside,
            invest_pa_outside=invest_pa_outside,
        )
