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
    Vars16,
    Vars17,
    Vars18,
)


@dataclass(kw_only=True)
class B30:
    b: Vars0 = field(default_factory=Vars0)
    g: Vars1 = field(default_factory=Vars1)
    g_consult: Vars2 = field(default_factory=Vars2)
    p: Vars3 = field(default_factory=Vars3)
    p_nonresi: Vars4 = field(default_factory=Vars4)
    p_nonresi_com: Vars5 = field(default_factory=Vars5)
    p_elec_elcon: Vars6 = field(default_factory=Vars6)
    p_elec_heatpump: Vars7 = field(default_factory=Vars7)
    p_vehicles: Vars8 = field(default_factory=Vars8)
    p_other: Vars9 = field(default_factory=Vars9)
    s: Vars10 = field(default_factory=Vars10)
    s_gas: Vars11 = field(default_factory=Vars11)
    s_emethan: Vars12 = field(default_factory=Vars12)
    s_lpg: Vars13 = field(default_factory=Vars13)
    s_petrol: Vars13 = field(default_factory=Vars13)
    s_jetfuel: Vars13 = field(default_factory=Vars13)
    s_diesel: Vars13 = field(default_factory=Vars13)
    s_fueloil: Vars14 = field(default_factory=Vars14)
    s_biomass: Vars15 = field(default_factory=Vars15)
    s_coal: Vars14 = field(default_factory=Vars14)
    s_heatnet: Vars15 = field(default_factory=Vars15)
    s_elec_heating: Vars13 = field(default_factory=Vars13)
    s_heatpump: Vars16 = field(default_factory=Vars16)
    s_solarth: Vars17 = field(default_factory=Vars17)
    s_elec: Vars13 = field(default_factory=Vars13)
    rb: Vars18 = field(default_factory=Vars18)
