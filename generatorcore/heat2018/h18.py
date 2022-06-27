from dataclasses import dataclass, field

from .dataclasses import Vars0, Vars1, Vars2, Vars3, Vars4, Vars5, Vars6, Vars7, Vars8


@dataclass
class H18:
    g: Vars0 = field(default_factory=Vars0)
    g_storage: Vars0 = field(default_factory=Vars0)
    g_planning: Vars0 = field(default_factory=Vars0)
    d: Vars1 = field(default_factory=Vars1)
    d_r: Vars1 = field(default_factory=Vars1)
    d_b: Vars1 = field(default_factory=Vars1)
    d_i: Vars1 = field(default_factory=Vars1)
    d_t: Vars1 = field(default_factory=Vars1)
    d_a: Vars1 = field(default_factory=Vars1)
    h: Vars2 = field(default_factory=Vars2)
    p: Vars3 = field(default_factory=Vars3)
    p_gas: Vars4 = field(default_factory=Vars4)
    p_lpg: Vars5 = field(default_factory=Vars5)
    p_fueloil: Vars5 = field(default_factory=Vars5)
    p_opetpro: Vars4 = field(default_factory=Vars4)
    p_coal: Vars4 = field(default_factory=Vars4)
    p_heatnet: Vars6 = field(default_factory=Vars6)
    p_heatnet_cogen: Vars5 = field(default_factory=Vars5)
    p_heatnet_plant: Vars5 = field(default_factory=Vars5)
    p_heatnet_geoth: Vars7 = field(default_factory=Vars7)
    p_heatnet_lheatpump: Vars7 = field(default_factory=Vars7)
    p_biomass: Vars8 = field(default_factory=Vars8)
    p_ofossil: Vars8 = field(default_factory=Vars8)
    p_orenew: Vars8 = field(default_factory=Vars8)
    p_solarth: Vars8 = field(default_factory=Vars8)
    p_heatpump: Vars8 = field(default_factory=Vars8)
