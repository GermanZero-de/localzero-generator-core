from dataclasses import dataclass


@dataclass
class Vars0:
    # Used by b
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars2:
    # Used by p, p_elec_elcon, p_elec_heatpump, p_vehicles, p_other
    energy: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by p_nonresi
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by p_nonresi_com
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass
class Vars5:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by s_gas, s_lpg, s_petrol, s_jetfuel, s_diesel, s_fueloil, s_coal, s_heatnet, s_heatpump, s_solarth
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by s_biomass
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by s_elec_heating, s_elec
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars9:
    # Used by rb
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars10:
    # Used by rp_p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
