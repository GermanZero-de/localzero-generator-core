# pyright: strict
from dataclasses import dataclass

from .dataclasses import (
    Vars0,
    Vars1,
    Vars2,
    Vars3,
    Vars4,
    Vars5,
    Vars6,
    Vars7,
    Vars8,
    Vars9,
    Vars10,
    Vars11,
    Vars12,
    Vars13,
    Vars14,
    Vars15,
)


@dataclass(kw_only=True)
class H30:
    h: Vars0
    g: Vars1
    g_storage: Vars2
    g_planning: Vars3
    d: Vars4
    d_r: Vars4
    d_b: Vars4
    d_i: Vars4
    d_t: Vars4
    d_a: Vars4
    p: Vars5
    p_gas: Vars6
    p_lpg: Vars7
    p_fueloil: Vars8
    p_opetpro: Vars9
    p_coal: Vars6
    p_heatnet: Vars10
    p_heatnet_cogen: Vars9
    p_heatnet_plant: Vars11
    p_heatnet_lheatpump: Vars12
    p_heatnet_geoth: Vars13
    p_biomass: Vars14
    p_ofossil: Vars15
    p_orenew: Vars15
    p_solarth: Vars15
    p_heatpump: Vars15

    # for pdf
    p_fossil_change_CO2e_t: float = None  # type: ignore
