# pyright: strict
from dataclasses import dataclass, field

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


@dataclass
class H30:
    h: Vars0 = field(default_factory=Vars0)
    g: Vars1 = field(default_factory=Vars1)
    g_storage: Vars2 = field(default_factory=Vars2)
    g_planning: Vars3 = field(default_factory=Vars3)
    d: Vars4 = field(default_factory=Vars4)
    d_r: Vars4 = field(default_factory=Vars4)
    d_b: Vars4 = field(default_factory=Vars4)
    d_i: Vars4 = field(default_factory=Vars4)
    d_t: Vars4 = field(default_factory=Vars4)
    a_t: Vars4 = field(default_factory=Vars4)
    p: Vars5 = field(default_factory=Vars5)
    p_gas: Vars6 = field(default_factory=Vars6)
    p_lpg: Vars7 = field(default_factory=Vars7)
    p_fueloil: Vars8 = field(default_factory=Vars8)
    p_opetpro: Vars9 = field(default_factory=Vars9)
    p_coal: Vars6 = field(default_factory=Vars6)
    p_heatnet: Vars10 = field(default_factory=Vars10)
    p_heatnet_cogen: Vars9 = field(default_factory=Vars9)
    p_heatnet_plant: Vars11 = field(default_factory=Vars11)
    p_heatnet_lheatpump: Vars12 = field(default_factory=Vars12)
    p_heatnet_geoth: Vars13 = field(default_factory=Vars13)
    p_biomass: Vars14 = field(default_factory=Vars14)
    p_ofossil: Vars15 = field(default_factory=Vars15)
    p_orenew: Vars15 = field(default_factory=Vars15)
    p_solarth: Vars15 = field(default_factory=Vars15)
    p_heatpump: Vars15 = field(default_factory=Vars15)

    # for pdf
    p_fossil_change_CO2e_t: float = None  # type: ignore
