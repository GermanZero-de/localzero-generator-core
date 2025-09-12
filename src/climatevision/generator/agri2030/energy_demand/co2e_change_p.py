# pyright: strict

from dataclasses import InitVar, dataclass

from ...agri2018.a18 import A18
from ...common.invest import Invest
from ...refdata import Facts
from ...utils import div
from .energy_change_p_operation import EnergyChangePOperation


@dataclass(kw_only=True)
class CO2eChangeP(Invest):
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    CO2e_total_year_before_baseline_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    cost_climate_saved: float = 0
    energy: float = 0

    facts: InitVar[Facts]
    year_baseline: InitVar[int]
    duration_until_target_year: InitVar[int]
    duration_CO2e_neutral_years: InitVar[float]
    what: InitVar[str]
    a18: InitVar[A18]
    operation: InitVar[EnergyChangePOperation]

    def __post_init__(
        self,
        facts: Facts,
        year_baseline: int,
        duration_until_target_year: int,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
        operation: EnergyChangePOperation,
    ):
        fact = facts.fact

        a18_CO2e_total = getattr(a18, what).CO2e_total

        self.CO2e_total_year_before_baseline_estimated = a18_CO2e_total * fact(
            f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref"
        )

        self.change_CO2e_t = self.CO2e_total - a18_CO2e_total
        self.cost_climate_saved = (
            (self.CO2e_total_year_before_baseline_estimated - self.CO2e_total)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        self.change_CO2e_pct = div(self.change_CO2e_t, a18_CO2e_total)
        self.demand_emplo = operation.demand_emplo

        self.invest = operation.invest
        self.invest_pa = self.invest / duration_until_target_year

        self.demand_emplo_new = operation.demand_emplo_new
        self.energy = operation.energy
        self.cost_wage = operation.cost_wage
