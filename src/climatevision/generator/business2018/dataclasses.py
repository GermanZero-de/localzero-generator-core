# pyright: strict

from dataclasses import dataclass

from ..common.energy import EnergyWithPercentage


@dataclass(kw_only=True)
class Vars0:
    # Used by b
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6(EnergyWithPercentage):
    # Used by s_gas, s_lpg, s_petrol, s_jetfuel, s_diesel, s_fueloil, s_coal, s_heatnet, s_heatpump, s_solarth
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7(EnergyWithPercentage):
    # Used by s_biomass
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8(EnergyWithPercentage):
    # Used by s_elec_heating, s_elec
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9:
    # Used by rb
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars10:
    # Used by rp_p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
