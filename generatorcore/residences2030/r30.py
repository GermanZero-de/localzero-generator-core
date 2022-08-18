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
class R30:
    g: Vars0 = field(default_factory=Vars0)
    g_consult: Vars1 = field(default_factory=Vars1)
    p: Vars2 = field(default_factory=Vars2)
    p_buildings_total: Vars3 = field(default_factory=Vars3)
    p_buildings_until_1919: Vars4 = field(default_factory=Vars4)
    p_buildings_1919_1948: Vars4 = field(default_factory=Vars4)
    p_buildings_1949_1978: Vars4 = field(default_factory=Vars4)
    p_buildings_1979_1995: Vars4 = field(default_factory=Vars4)
    p_buildings_1996_2004: Vars4 = field(default_factory=Vars4)
    p_buildings_2005_2011: Vars5 = field(default_factory=Vars5)
    p_buildings_2011_today: Vars5 = field(default_factory=Vars5)
    p_buildings_new: Vars6 = field(default_factory=Vars6)
    p_buildings_area_m2_com: Vars7 = field(default_factory=Vars7)
    r: Vars8 = field(default_factory=Vars8)
    s: Vars9 = field(default_factory=Vars9)
    s_fueloil: Vars10 = field(default_factory=Vars10)
    s_lpg: Vars10 = field(default_factory=Vars10)
    s_biomass: Vars10 = field(default_factory=Vars10)
    s_coal: Vars10 = field(default_factory=Vars10)
    s_petrol: Vars10 = field(default_factory=Vars10)
    s_heatnet: Vars10 = field(default_factory=Vars10)
    s_solarth: Vars11 = field(default_factory=Vars11)
    s_heatpump: Vars12 = field(default_factory=Vars12)
    s_gas: Vars13 = field(default_factory=Vars13)
    s_elec_heating: Vars14 = field(default_factory=Vars14)
    s_emethan: Vars15 = field(default_factory=Vars15)
    s_elec: Vars14 = field(default_factory=Vars14)
    p_elec_elcon: Vars16 = field(default_factory=Vars16)
    p_elec_heatpump: Vars16 = field(default_factory=Vars16)
    p_other: Vars17 = field(default_factory=Vars17)
    p_vehicles: Vars18 = field(default_factory=Vars18)
