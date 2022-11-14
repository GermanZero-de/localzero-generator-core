# pyright: strict

from dataclasses import dataclass


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
