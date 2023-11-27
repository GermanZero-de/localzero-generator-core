# pyright: strict

from dataclasses import dataclass

from .energy_demand import Vars1


@dataclass(kw_only=True)
class R18New:
    dummy: float = None  # type: ignore
    r: float = None  # type: ignore
    p: float = None  # type: ignore
    p_heating: float = None  # type: ignore
    p_heating_fossil: float = None  # type: ignore
    p_heating_fossil_gas: Vars1
    p_heating_fossil_lpg: Vars1
    p_heating_fossil_fueloil: Vars1
    p_heating_fossil_coal: Vars1
    p_heating_renew: float = None  # type: ignore
    p_heating_renew_heatnet: Vars1
    p_heating_renew_biomass: Vars1
    p_heating_renew_elec_heating: Vars1
    p_heating_renew_elec_heatpump: Vars1
    p_heating_renew_without_heating: Vars1
    s: float = None  # type: ignore
    s_dummy: float = None  # type: ignore
