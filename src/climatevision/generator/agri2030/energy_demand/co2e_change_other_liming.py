# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from .co2e_change_agri import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeOtherLiming(CO2eChangeAgri):
    prod_volume: float

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):

        self.CO2e_combustion_based = 0

        CO2eChangeAgri.__post_init__(self, inputs=inputs, what=what, a18=a18)
