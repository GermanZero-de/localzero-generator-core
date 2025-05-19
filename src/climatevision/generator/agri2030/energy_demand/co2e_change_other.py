# pyright: strict

from dataclasses import InitVar, dataclass

from ...agri2018.a18 import A18
from ...refdata import Assumptions, Facts
from .co2e_change_agri import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeOther(CO2eChangeAgri):
    CO2e_production_based_per_t: float = 0
    demand_change: float = 0
    prod_volume: float = 0

    facts: InitVar[Facts]
    assumptions: InitVar[Assumptions]
    duration_CO2e_neutral_years: InitVar[float]
    what: InitVar[str]
    a18: InitVar[A18]
    ass_demand_change: InitVar[str]
    fact_production_based_per_t: InitVar[str]

    def __post_init__(  # type: ignore[override]
        self,
        facts: Facts,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
        assumptions: Assumptions,
        ass_demand_change: str,
        fact_production_based_per_t: str,
    ):
        fact = facts.fact
        ass = assumptions.ass

        self.CO2e_combustion_based = 0

        self.demand_change = ass(ass_demand_change)
        self.prod_volume = getattr(a18, what).prod_volume * (1 + self.demand_change)

        self.CO2e_production_based_per_t = fact(fact_production_based_per_t)
        self.CO2e_production_based = self.prod_volume * self.CO2e_production_based_per_t

        CO2eChangeAgri.__post_init__(
            self,
            facts=facts,
            year_baseline=year_baseline,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
        )
