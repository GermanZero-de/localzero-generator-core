# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...common.invest import Invest
from ...agri2018.a18 import A18

from .energy_change_p_operation import EnergyChangePOperation


@dataclass(kw_only=True)
class CO2eChangeP(Invest):
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    cost_climate_saved: float = 0
    energy: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    operation: InitVar[EnergyChangePOperation]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        operation: EnergyChangePOperation,
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
        self.demand_emplo = operation.demand_emplo

        self.invest = operation.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.demand_emplo_new = operation.demand_emplo_new
        self.energy = operation.energy
        self.cost_wage = operation.cost_wage
