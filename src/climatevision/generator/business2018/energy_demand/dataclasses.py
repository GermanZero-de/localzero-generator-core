# pyright: strict

from dataclasses import dataclass

from ...common.energy import EnergyPerM2


@dataclass(kw_only=True)
class EnergyPerM2WithBuildings(EnergyPerM2):
    number_of_buildings: float


@dataclass(kw_only=True)
class Vars4(EnergyPerM2):
    pct_x: float
