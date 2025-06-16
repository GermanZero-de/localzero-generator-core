# pyright: strict

from dataclasses import InitVar, dataclass

from ...agri2018.a18 import A18
from ...refdata import Facts
from .co2e_change_agri import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeOtherLiming(CO2eChangeAgri):
    prod_volume: float

    facts: InitVar[Facts]
    duration_CO2e_neutral_years: InitVar[float]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        facts: Facts,
        year_baseline: int,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
    ):

        self.CO2e_combustion_based = 0

        CO2eChangeAgri.__post_init__(
            self,
            facts=facts,
            year_baseline=year_baseline,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
        )
