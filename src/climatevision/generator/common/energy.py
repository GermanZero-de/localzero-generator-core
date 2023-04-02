# pyright: strict

from dataclasses import dataclass, InitVar

from ..utils import div


@dataclass(kw_only=True)
class Energy:
    energy: float = 0


@dataclass(kw_only=True)
class EnergyWithPercentage(Energy):
    pct_energy: float = 0
    total_energy: InitVar[float]

    def __post_init__(self, total_energy: float):
        self.pct_energy = div(self.energy, total_energy)


@dataclass(kw_only=True)
class EnergyChange:
    change_energy_MWh: float = 0
    change_energy_pct: float = 0


@dataclass(kw_only=True)
class EnergyPerM2(Energy):
    area_m2: float = 0
    ratio_energy_to_m2: float = 0

    def __post_init__(
        self,
    ):
        self.ratio_energy_to_m2 = div(self.energy, self.area_m2)


@dataclass(kw_only=True)
class EnergyPerM2PctCommune(EnergyPerM2):
    pct_x: float

    total: InitVar[EnergyPerM2]

    def __post_init__(self, total: EnergyPerM2):  # type: ignore
        self.area_m2 = total.area_m2 * self.pct_x
        self.energy = total.energy * self.pct_x

        EnergyPerM2.__post_init__(self)
