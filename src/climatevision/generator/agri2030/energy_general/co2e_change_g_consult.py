# pyright: strict

from dataclasses import dataclass, InitVar

from ...refdata import Assumptions
from ...utils import div
from ...common.invest import InvestCommune


@dataclass(kw_only=True)
class CO2eChangeGConsult(InvestCommune):
    area_ha_available: float = 0
    demand_emplo_com: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    ratio_wage_to_emplo: float = 0

    assumptions: InitVar[Assumptions]
    duration_until_target_year: InitVar[int]
    farm_amount: InitVar[float]

    def __post_init__(
        self,
        assumptions: Assumptions,
        duration_until_target_year: int,
        farm_amount: float,
    ):
        ass = assumptions.ass

        self.area_ha_available = farm_amount

        self.invest_per_x = ass("Ass_A_G_consult_invest_per_farm")
        self.invest = self.area_ha_available * self.invest_per_x
        self.invest_com = self.invest * ass("Ass_A_G_consult_invest_pct_of_public")
        self.invest_pa = self.invest / duration_until_target_year
        self.invest_pa_com = self.invest_pa * ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )

        self.pct_of_wage = ass("Ass_A_G_consult_invest_pct_of_wage")
        self.cost_wage = self.invest_pa * self.pct_of_wage

        self.ratio_wage_to_emplo = ass("Ass_A_G_consult_ratio_wage_to_emplo")
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo
        self.demand_emplo_com = self.demand_emplo_new
