# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18

from .co2eChangePOperation import CO2eChangePOperation


@dataclass(kw_only=True)
class CO2eChangeP:
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    cost_climate_saved: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    energy: float = 0
    invest: float = 0
    invest_pa: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    p_operation: InitVar[CO2eChangePOperation]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation: CO2eChangePOperation,
    ):

        a18_CO2e_total = getattr(a18, what).CO2e_total

        self.CO2e_total_2021_estimated = a18_CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        self.change_CO2e_t = self.CO2e_total - a18_CO2e_total
        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )
        self.change_CO2e_pct = div(self.change_CO2e_t, a18_CO2e_total)
        self.demand_emplo = p_operation.demand_emplo

        self.invest = p_operation.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.demand_emplo_new = p_operation.demand_emplo_new
        self.energy = p_operation.energy
        self.cost_wage = p_operation.cost_wage
