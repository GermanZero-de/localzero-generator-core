# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18


@dataclass(kw_only=True)
class CO2eChangeEnergy:
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    energy: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)
