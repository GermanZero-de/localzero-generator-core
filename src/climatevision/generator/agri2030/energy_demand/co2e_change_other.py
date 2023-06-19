# pyright: strict

from dataclasses import dataclass, InitVar

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...agri2018.a18 import A18

from .co2e_change_agri import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeOther(CO2eChangeAgri):
    CO2e_production_based_per_t: float = 0
    demand_change: float = 0
    prod_volume: float = 0

    entries: InitVar[Entries]
    facts: InitVar[Facts]
    assumptions: InitVar[Assumptions]
    what: InitVar[str]
    a18: InitVar[A18]
    ass_demand_change: InitVar[str]
    fact_production_based_per_t: InitVar[str]

    def __post_init__(  # type: ignore[override]
        self,
        entries: Entries,
        facts: Facts,
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
            self, entries=entries, facts=facts, what=what, a18=a18
        )
