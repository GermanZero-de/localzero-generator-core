from dataclasses import dataclass, field

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


@dataclass
class E18:
    e: Vars0 = field(default_factory=Vars0)
    d: Vars2 = field(default_factory=Vars2)
    d_r: Vars3 = field(default_factory=Vars3)
    d_b: Vars3 = field(default_factory=Vars3)
    d_i: Vars3 = field(default_factory=Vars3)
    d_t: Vars3 = field(default_factory=Vars3)
    d_a: Vars4 = field(default_factory=Vars4)
    d_h: Vars4 = field(default_factory=Vars4)
    d_f_hydrogen_reconv: Vars4 = field(default_factory=Vars4)
    p: Vars5 = field(default_factory=Vars5)
    p_fossil: Vars6 = field(default_factory=Vars6)
    p_fossil_nuclear: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_coal_brown: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_coal_brown_cogen: Vars8 = field(default_factory=Vars8)
    p_fossil_coal_black: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_coal_black_cogen: Vars8 = field(default_factory=Vars8)
    p_fossil_gas: FossilFuelsProduction = field(default_factory=FossilFuelsProduction)
    p_fossil_gas_cogen: Vars8 = field(default_factory=Vars8)
    p_fossil_ofossil: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_ofossil_cogen: Vars8 = field(default_factory=Vars8)
    p_renew: Vars9 = field(default_factory=Vars9)
    p_renew_pv: Vars10 = field(default_factory=Vars10)
    p_renew_pv_roof: Vars11 = field(default_factory=Vars11)
    p_renew_pv_facade: Vars11 = field(default_factory=Vars11)
    p_renew_pv_park: Vars11 = field(default_factory=Vars11)
    p_renew_pv_agri: Vars11 = field(default_factory=Vars11)
    p_renew_wind: Vars10 = field(default_factory=Vars10)
    p_renew_wind_onshore: Vars11 = field(default_factory=Vars11)
    p_renew_wind_offshore: Vars11 = field(default_factory=Vars11)
    p_renew_biomass: Vars12 = field(default_factory=Vars12)
    p_renew_biomass_waste: Vars13 = field(default_factory=Vars13)
    p_renew_biomass_solid: Vars13 = field(default_factory=Vars13)
    p_renew_biomass_gaseous: Vars13 = field(default_factory=Vars13)
    p_renew_biomass_cogen: Vars8 = field(default_factory=Vars8)
    p_renew_geoth: Vars11 = field(default_factory=Vars11)
    p_renew_hydro: Vars11 = field(default_factory=Vars11)
    p_renew_reverse: Vars4 = field(default_factory=Vars4)
    p_fossil_and_renew: Vars13 = field(default_factory=Vars13)
    p_local_pv_roof: Vars14 = field(default_factory=Vars14)
    p_local_pv_facade: Vars14 = field(default_factory=Vars14)
    p_local_pv_park: Vars14 = field(default_factory=Vars14)
    p_local_pv_agri: Vars14 = field(default_factory=Vars14)
    p_local_pv: Vars15 = field(default_factory=Vars15)
    p_local_wind_onshore: Vars16 = field(default_factory=Vars16)
    p_local_biomass: Vars17 = field(default_factory=Vars17)
    p_local_biomass_cogen: Vars8 = field(default_factory=Vars8)
    p_local_hydro: Vars16 = field(default_factory=Vars16)
    p_local: Vars18 = field(default_factory=Vars18)
