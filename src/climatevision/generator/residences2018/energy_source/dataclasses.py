# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class Vars6:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7:
    # Used by s_fueloil, s_lpg, s_coal, s_petrol, s_heatnet, s_solarth, s_heatpump, s_elec_heating, s_gas
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


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


@dataclass(kw_only=True)
class Vars9:
    # Used by s_elec
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
