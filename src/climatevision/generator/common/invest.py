# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class Invest:
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0
