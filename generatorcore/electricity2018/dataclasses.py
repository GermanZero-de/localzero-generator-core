# pyright: strict
from dataclasses import dataclass


@dataclass(kw_only=True)
class Vars0:
    # Used by e
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars2:
    # Used by d
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars3:
    # Used by d_r, d_b, d_i, d_t
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4:
    # Used by d_a, d_h, d_f_hydrogen_reconv, p_renew_reverse
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_certificate: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6:
    # Used by p_fossil
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_certificate: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class FossilFuelsProduction:
    # Used by p_fossil_nuclear, p_fossil_coal_brown, p_fossil_coal_black, p_fossil_gas, p_fossil_ofossil
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_certificate: float = None  # type: ignore
    cost_certificate_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8:
    # Used by p_fossil_coal_brown_cogen, p_fossil_coal_black_cogen, p_fossil_gas_cogen, p_fossil_ofossil_cogen, p_renew_biomass_cogen, p_local_biomass_cogen
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9:
    # Used by p_renew
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars10:
    # Used by p_renew_pv, p_renew_wind
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars11:
    # Used by p_renew_pv_roof, p_renew_pv_facade, p_renew_pv_park, p_renew_pv_agri, p_renew_wind_onshore, p_renew_wind_offshore, p_renew_geoth, p_renew_hydro
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars12:
    # Used by p_renew_biomass
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars13:
    # Used by p_renew_biomass_waste, p_renew_biomass_solid, p_renew_biomass_gaseous, p_fossil_and_renew
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars14:
    # Used by p_local_pv_roof, p_local_pv_facade, p_local_pv_park, p_local_pv_agri
    cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars15:
    # Used by p_local_pv
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars16:
    # Used by p_local_wind_onshore, p_local_hydro
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars17:
    # Used by p_local_biomass
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars18:
    # Used by p_local
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
