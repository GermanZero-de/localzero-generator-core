# pyright: strict

from dataclasses import InitVar, dataclass

from ...agri2018.a18 import A18
from ...common.co2_equivalent_emission import CO2eEmission
from ...common.co2e_change import CO2eChange
from ...entries import Entries
from ...refdata import Facts
from ...utils import div


@dataclass(kw_only=True)
class CO2eChangeAgri(CO2eEmission, CO2eChange):
    facts: InitVar[Facts]
    entries: Entries
    duration_CO2e_neutral_years: InitVar[float]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(  # type: ignore[override]
        self,
        facts: Facts,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
    ):
        fact = facts.fact

        if not what:
            a18_CO2e_total = 0
        else:
            a18_CO2e_total = getattr(a18, what).CO2e_total

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based
        self.change_CO2e_t = self.CO2e_total - a18_CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, a18_CO2e_total)

        self.CO2e_total_2021_estimated = a18_CO2e_total * fact(
            f"Fact_M_CO2e_wo_lulucf_{self.entries.m_year_baseline - 1}_vs_year_ref"
        )
        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * duration_CO2e_neutral_years
            * fact("Fact_M_cost_per_CO2e_2020")
        )
