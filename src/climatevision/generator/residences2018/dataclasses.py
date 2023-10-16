# pyright: strict

from dataclasses import dataclass

from ..common.energy import EnergyPerM2WithBuildings


@dataclass(kw_only=True)
class Vars1:
    # Used by r
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars2:
    # Used by p, p_elec_elcon, p_elec_heatpump, p_vehicles, p_other
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars3(EnergyPerM2WithBuildings):
    # Used by p_buildings_total, p_buildings_until_1919, p_buildings_1919_1948, p_buildings_1949_1978, p_buildings_1979_1995, p_buildings_1996_2004
    area_m2_relative_heat_ratio: float = None  # type: ignore
    fec_after_BMWi: float = None  # type: ignore
    fec_factor_BMWi: float = None  # type: ignore
    relative_building_ratio: float = None  # type: ignore
    relative_heat_ratio_BMWi: float = None  # type: ignore
    relative_heat_ratio_buildings_until_2004: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4(EnergyPerM2WithBuildings):
    # Used by p_buildings_2005_2011, p_buildings_2011_today
    fec_after_BMWi: float = None  # type: ignore
    fec_factor_BMWi: float = None  # type: ignore
    relative_building_ratio: float = None  # type: ignore
    relative_heat_ratio_BMWi: float = None  # type: ignore
