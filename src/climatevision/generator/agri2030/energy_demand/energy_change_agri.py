# pyright: strict

from dataclasses import dataclass, InitVar

from ...utils import div
from ...common.energy import Energy, EnergyChange
from ...agri2018.a18 import A18


@dataclass(kw_only=True)
class EnergyChangeAgri(Energy, EnergyChange):
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, what: str, a18: A18):

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)
