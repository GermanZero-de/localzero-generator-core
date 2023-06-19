# pyright: strict
from dataclasses import dataclass, InitVar

from ...makeentries import Entries
from ...refdata import Facts
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeFuelEmethan(CO2eChangeAgri):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    demand_emethan: float = 0

    entries: InitVar[Entries]
    facts: InitVar[Facts]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, entries: Entries, facts: Facts, what: str, a18: A18):
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
            self, entries=entries, facts=facts, what=what, a18=a18
        )
