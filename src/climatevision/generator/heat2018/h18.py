# pyright: strict

from dataclasses import dataclass

from .dataclasses import Vars2, Vars3, Vars4, Vars5, Vars6, Vars7, Vars8
from .energy_demand import Vars1


@dataclass(kw_only=True)
class H18:
    d: Vars1
    d_r: Vars1
    d_b: Vars1
    d_i: Vars1
    d_t: Vars1
    d_a: Vars1
    h: Vars2
    p: Vars3
    p_gas: Vars4
    p_lpg: Vars5
    p_fueloil: Vars5
    p_opetpro: Vars4
    p_coal: Vars4
    p_heatnet: Vars6
    p_heatnet_cogen: Vars5
    p_heatnet_plant: Vars5
    p_heatnet_geoth: Vars7
    p_heatnet_lheatpump: Vars7
    p_biomass: Vars8
    p_ofossil: Vars8
    p_orenew: Vars8
    p_solarth: Vars8
    p_heatpump: Vars8
