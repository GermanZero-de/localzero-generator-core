# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...common.invest import InvestCom


@dataclass(kw_only=True)
class CO2eChangeGConsult(InvestCom):
    area_ha_available: float = 0
    demand_emplo_com: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]

    def __post_init__(self, inputs: Inputs):

        self.area_ha_available = inputs.entries.a_farm_amount

        self.invest_per_x = inputs.ass("Ass_A_G_consult_invest_per_farm")
        self.invest = self.area_ha_available * self.invest_per_x
        self.invest_com = self.invest * inputs.ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )
        self.invest_pa = self.invest / inputs.entries.m_duration_target
        self.invest_pa_com = self.invest_pa * inputs.ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )

        self.pct_of_wage = inputs.ass("Ass_A_G_consult_invest_pct_of_wage")
        self.cost_wage = self.invest_pa * self.pct_of_wage

        self.ratio_wage_to_emplo = inputs.ass("Ass_A_G_consult_ratio_wage_to_emplo")
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo
        self.demand_emplo_com = self.demand_emplo_new
