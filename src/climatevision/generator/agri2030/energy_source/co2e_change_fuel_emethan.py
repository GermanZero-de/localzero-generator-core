# pyright: strict
from dataclasses import InitVar, dataclass

from ...agri2018.a18 import A18
from ...refdata import Facts
from ..energy_demand import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeFuelEmethan(CO2eChangeAgri):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    demand_emethan: float = 0

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
        fact = facts.fact

        what = ""

        self.CO2e_production_based = 0
        self.CO2e_combustion_based = 0
        self.CO2e_combustion_based_per_MWh = fact(
            "Fact_T_S_methan_EmFa_tank_wheel_2018"
        )

        self.change_energy_MWh = self.energy
        self.demand_emethan = self.energy

        CO2eChangeAgri.__post_init__(
            self,
            facts=facts,
            year_baseline=year_baseline,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
        )
