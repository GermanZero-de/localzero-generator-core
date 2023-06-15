# pyright: strict

from dataclasses import dataclass, InitVar

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...utils import div
from ...common.invest import Invest


@dataclass(kw_only=True)
class CO2eChangeGOrganic(Invest):
    area_ha_available: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    power_installed: float = 0
    power_to_be_installed: float = 0
    power_to_be_installed_pct: float = 0
    ratio_wage_to_emplo: float = 0

    entries: InitVar[Entries]
    facts: InitVar[Facts]
    assumptions: InitVar[Assumptions]

    def __post_init__(self, entries: Entries, facts: Facts, assumptions: Assumptions):
        fact = facts.fact
        ass = assumptions.ass

        self.area_ha_available = entries.m_area_agri_com

        self.power_installed = entries.a_area_agri_com_pct_of_organic
        self.power_to_be_installed_pct = ass("Ass_A_G_area_agri_pct_of_organic_2050")
        self.power_to_be_installed = self.area_ha_available * (
            self.power_to_be_installed_pct - self.power_installed
        )

        self.invest_per_x = ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
        self.invest = self.power_to_be_installed * self.invest_per_x
        self.invest_pa = self.invest / entries.m_duration_target

        self.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        self.cost_wage = self.invest_pa * self.pct_of_wage

        self.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo
