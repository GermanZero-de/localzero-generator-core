# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeFuelEmethan(CO2eChangeAgri):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    demand_emethan: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        what = ""

        self.CO2e_production_based = 0
        self.CO2e_combustion_based = 0
        self.CO2e_combustion_based_per_MWh = inputs.fact(
            "Fact_T_S_methan_EmFa_tank_wheel_2018"
        )

        self.change_energy_MWh = self.energy
        self.demand_emethan = self.energy

        CO2eChangeAgri.__post_init__(self, inputs=inputs, what=what, a18=a18)
