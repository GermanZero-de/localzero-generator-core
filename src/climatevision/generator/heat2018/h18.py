# pyright: strict

from dataclasses import dataclass

from .energy_demand import EnergyDemand
from .dataclasses import Vars2, Vars3, Vars4, Vars5, Vars6, Vars7, Vars8


@dataclass(kw_only=True)
class H18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
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
