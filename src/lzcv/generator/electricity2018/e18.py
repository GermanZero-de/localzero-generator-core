# pyright: strict
from dataclasses import dataclass

from .dataclasses import (
    Vars0,
    Vars2,
    Vars3,
    Vars4,
    Vars5,
    Vars6,
    Vars8,
    Vars9,
    Vars10,
    Vars11,
    Vars12,
    Vars13,
    Vars14,
    Vars15,
    Vars16,
    Vars17,
    Vars18,
    FossilFuelsProduction,
)


@dataclass(kw_only=True)
class E18:
    e: Vars0
    d: Vars2
    d_r: Vars3
    d_b: Vars3
    d_i: Vars3
    d_t: Vars3
    d_a: Vars4
    d_h: Vars4
    d_f_hydrogen_reconv: Vars4
    p: Vars5
    p_fossil: Vars6
    p_fossil_nuclear: FossilFuelsProduction
    p_fossil_coal_brown: FossilFuelsProduction
    p_fossil_coal_brown_cogen: Vars8
    p_fossil_coal_black: FossilFuelsProduction
    p_fossil_coal_black_cogen: Vars8
    p_fossil_gas: FossilFuelsProduction
    p_fossil_gas_cogen: Vars8
    p_fossil_ofossil: FossilFuelsProduction
    p_fossil_ofossil_cogen: Vars8
    p_renew: Vars9
    p_renew_pv: Vars10
    p_renew_pv_roof: Vars11
    p_renew_pv_facade: Vars11
    p_renew_pv_park: Vars11
    p_renew_pv_agri: Vars11
    p_renew_wind: Vars10
    p_renew_wind_onshore: Vars11
    p_renew_wind_offshore: Vars11
    p_renew_biomass: Vars12
    p_renew_biomass_waste: Vars13
    p_renew_biomass_solid: Vars13
    p_renew_biomass_gaseous: Vars13
    p_renew_biomass_cogen: Vars8
    p_renew_geoth: Vars11
    p_renew_hydro: Vars11
    p_renew_reverse: Vars4
    p_fossil_and_renew: Vars13
    p_local_pv_roof: Vars14
    p_local_pv_facade: Vars14
    p_local_pv_park: Vars14
    p_local_pv_agri: Vars14
    p_local_pv: Vars15
    p_local_wind_onshore: Vars16
    p_local_biomass: Vars17
    p_local_biomass_cogen: Vars8
    p_local_hydro: Vars16
    p_local: Vars18
