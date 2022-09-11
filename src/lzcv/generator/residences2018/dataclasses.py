# pyright: strict
from dataclasses import dataclass


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
class Vars3:
    # Used by p_buildings_total, p_buildings_until_1919, p_buildings_1919_1948, p_buildings_1949_1978, p_buildings_1979_1995, p_buildings_1996_2004
    area_m2: float = None  # type: ignore
    area_m2_relative_heat_ratio: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    fec_after_BMWi: float = None  # type: ignore
    fec_factor_BMWi: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore
    relative_building_ratio: float = None  # type: ignore
    relative_heat_ratio_BMWi: float = None  # type: ignore
    relative_heat_ratio_buildings_until_2004: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4:
    # Used by p_buildings_2005_2011, p_buildings_2011_today
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    fec_after_BMWi: float = None  # type: ignore
    fec_factor_BMWi: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore
    relative_building_ratio: float = None  # type: ignore
    relative_heat_ratio_BMWi: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by p_buildings_area_m2_com
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7:
    # Used by s_fueloil, s_lpg, s_coal, s_petrol, s_heatnet, s_solarth, s_heatpump, s_elec_heating, s_gas
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8:
    # Used by s_biomass
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9:
    # Used by s_elec
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
