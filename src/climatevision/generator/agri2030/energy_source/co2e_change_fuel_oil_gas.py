# pyright: strict
from dataclasses import dataclass, InitVar

from ...makeentries import Entries
from ...refdata import Facts
from ...agri2018.a18 import A18

from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh


@dataclass(kw_only=True)
class CO2eChangeFuelOilGas(CO2eChangeEnergyPerMWh):
    area_m2: float = 0

    entries: InitVar[Entries]
    facts: InitVar[Facts]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, entries: Entries, facts: Facts, what: str, a18: A18):

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0
        self.area_m2 = 0

        CO2eChangeEnergyPerMWh.__post_init__(
            self, entries=entries, facts=facts, what=what, a18=a18
        )
