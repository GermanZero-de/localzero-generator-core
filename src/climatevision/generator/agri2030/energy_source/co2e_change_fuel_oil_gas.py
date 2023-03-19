# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh


@dataclass(kw_only=True)
class CO2eChangeFuelOilGas(CO2eChangeEnergyPerMWh):
    area_m2: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0
        self.area_m2 = 0

        CO2eChangeEnergyPerMWh.__post_init__(self, inputs=inputs, what=what, a18=a18)
