# pyright: strict

from dataclasses import dataclass

@dataclass(kw_only=True)
class Vars1:
    number_of_buildings: float = None  # type: ignore
    number_of_flats: float = None  # type: ignore
    ratio_flats_to_buildings: float = None  # type: ignore
    ratio_area_m2_to_flat: float = None  # type: ignore
    area_m2: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    energy: float = None  # type: ignore

    def __post_init__(
        self,
    ):
        self.ratio_flats_to_buildings = self.number_of_flats / self.number_of_buildings
        self.area_m2 = self.number_of_flats * self.ratio_area_m2_to_flat
        self.energy = self.area_m2 * self.factor_adapted_to_fec #factor_adapted_to_fec_gas # V neuer Fakt: