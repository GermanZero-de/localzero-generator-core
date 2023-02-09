# pyright: strict

from dataclasses import dataclass, InitVar

from .co2e_change_g_consult import CO2eChangeGConsult
from .co2e_change_g_organic import CO2eChangeGOrganic


@dataclass(kw_only=True)
class CO2eChangeG:
    CO2e_total: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_com: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_outside: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0
    invest_pa_outside: float = 0

    g_consult: InitVar[CO2eChangeGConsult]
    g_organic: InitVar[CO2eChangeGOrganic]

    def __post_init__(
        self, g_consult: CO2eChangeGConsult, g_organic: CO2eChangeGOrganic
    ):

        self.CO2e_total = 0
        self.cost_wage = g_consult.cost_wage + g_organic.cost_wage

        self.demand_emplo = g_consult.demand_emplo + g_organic.demand_emplo
        self.demand_emplo_new = g_consult.demand_emplo_new + g_organic.demand_emplo_new
        self.demand_emplo_com = g_consult.demand_emplo_com

        self.invest = g_consult.invest + g_organic.invest
        self.invest_com = g_consult.invest_com
        self.invest_outside = 0

        self.invest_pa = g_consult.invest_pa + g_organic.invest_pa
        self.invest_pa_com = g_consult.invest_pa_com
        self.invest_pa_outside = 0
