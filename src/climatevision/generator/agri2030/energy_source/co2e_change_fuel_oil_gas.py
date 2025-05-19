# pyright: strict
from dataclasses import InitVar, dataclass

from ...agri2018.a18 import A18
from ...refdata import Facts
from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh


@dataclass(kw_only=True)
class CO2eChangeFuelOilGas(CO2eChangeEnergyPerMWh):
    area_m2: float = 0

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
        self.CO2e_production_based = 0
        self.area_m2 = 0

        CO2eChangeEnergyPerMWh.__post_init__(
            self,
            facts=facts,
            year_baseline=year_baseline,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
        )
