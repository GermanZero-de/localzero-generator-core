# pyright: strict
from dataclasses import dataclass, InitVar

from ...refdata import Facts
from ...utils import div
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeEnergyPerMWh(CO2eChangeAgri):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0

    facts: InitVar[Facts]
    duration_CO2e_neutral_years: InitVar[float]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self, facts: Facts, duration_CO2e_neutral_years: float, what: str, a18: A18
    ):

        self.CO2e_production_based = 0
        self.CO2e_combustion_based_per_MWh = getattr(
            a18, what
        ).CO2e_combustion_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        CO2eChangeAgri.__post_init__(
            self,
            facts=facts,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
        )
