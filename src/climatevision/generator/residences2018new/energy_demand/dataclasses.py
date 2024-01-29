# pyright: strict

from dataclasses import dataclass

@dataclass(kw_only=True)
class Vars1:
    number_of_buildings: float
    number_of_flats: float
    ratio_flats_to_buildings: float = 0
    ratio_area_m2_to_flat: float
    area_m2: float = 0
    factor_adapted_to_fec: float
    energy: float = 0

    def __post_init__(
        self,
    ):
        self.ratio_flats_to_buildings = self.number_of_flats / self.number_of_buildings
        self.area_m2 = self.number_of_flats * self.ratio_area_m2_to_flat
        self.energy = self.area_m2 * self.factor_adapted_to_fec