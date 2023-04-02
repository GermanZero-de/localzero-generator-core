# pyright: strict

from dataclasses import dataclass, InitVar

from ...common.energy import EnergyPerM2


@dataclass(kw_only=True)
class EnergyPerM2WithBuildings(EnergyPerM2):
    number_of_buildings: float


@dataclass(kw_only=True)
class EnergyPerM2PctCommune(EnergyPerM2):
    pct_x: float

    total: InitVar[EnergyPerM2]

    def __post_init__(self, total: EnergyPerM2):  # type: ignore
        self.area_m2 = total.area_m2 * self.pct_x
        self.energy = total.energy * self.pct_x

        EnergyPerM2.__post_init__(self)
