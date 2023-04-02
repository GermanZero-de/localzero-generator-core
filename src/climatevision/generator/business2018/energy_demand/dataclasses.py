# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy
from ...utils import div


@dataclass(kw_only=True)
class Vars3(Energy):
    area_m2: float
    factor_adapted_to_fec: float = 0
    number_of_buildings: float

    def __post_init__(
        self,
    ):
        self.factor_adapted_to_fec = div(self.energy, self.area_m2)


@dataclass(kw_only=True)
class Vars4(Energy):
    area_m2: float
    factor_adapted_to_fec: float = 0
    pct_x: float

    def __post_init__(
        self,
    ):
        self.factor_adapted_to_fec = div(self.energy, self.area_m2)
