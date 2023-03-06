# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from .co2e_change_agri import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeOther(CO2eChangeAgri):
    CO2e_production_based_per_t: float = 0
    demand_change: float = 0
    prod_volume: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    ass_demand_change: InitVar[str]
    fact_production_based_per_t: InitVar[str]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        ass_demand_change: str,
        fact_production_based_per_t: str,
    ):

        self.CO2e_combustion_based = 0

        self.demand_change = inputs.ass(ass_demand_change)
        self.prod_volume = getattr(a18, what).prod_volume * (1 + self.demand_change)

        self.CO2e_production_based_per_t = inputs.fact(fact_production_based_per_t)
        self.CO2e_production_based = self.prod_volume * self.CO2e_production_based_per_t

        CO2eChangeAgri.__post_init__(self, inputs=inputs, what=what, a18=a18)
