# pyright: strict
from dataclasses import dataclass, field

from .dataclasses import (
    Vars0,
    Vars2,
    Vars3,
    Vars4,
    Vars5,
    Vars6,
    Vars7,
    Vars8,
    Vars9,
    Vars10,
)


@dataclass
class B18:
    b: Vars0 = field(default_factory=Vars0)
    p: Vars2 = field(default_factory=Vars2)
    p_nonresi: Vars3 = field(default_factory=Vars3)
    p_nonresi_com: Vars4 = field(default_factory=Vars4)
    p_elec_elcon: Vars2 = field(default_factory=Vars2)
    p_elec_heatpump: Vars2 = field(default_factory=Vars2)
    p_vehicles: Vars2 = field(default_factory=Vars2)
    p_other: Vars2 = field(default_factory=Vars2)
    s: Vars5 = field(default_factory=Vars5)
    s_gas: Vars6 = field(default_factory=Vars6)
    s_lpg: Vars6 = field(default_factory=Vars6)
    s_petrol: Vars6 = field(default_factory=Vars6)
    s_jetfuel: Vars6 = field(default_factory=Vars6)
    s_diesel: Vars6 = field(default_factory=Vars6)
    s_fueloil: Vars6 = field(default_factory=Vars6)
    s_biomass: Vars7 = field(default_factory=Vars7)
    s_coal: Vars6 = field(default_factory=Vars6)
    s_heatnet: Vars6 = field(default_factory=Vars6)
    s_elec_heating: Vars8 = field(default_factory=Vars8)
    s_heatpump: Vars6 = field(default_factory=Vars6)
    s_solarth: Vars6 = field(default_factory=Vars6)
    s_elec: Vars8 = field(default_factory=Vars8)
    rb: Vars9 = field(default_factory=Vars9)
    rp_p: Vars10 = field(default_factory=Vars10)
