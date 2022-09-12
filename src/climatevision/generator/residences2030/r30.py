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
    Vars16,
    Vars17,
    Vars18,
)


@dataclass(kw_only=True)
class R30:
    g: Vars0
    g_consult: Vars1
    p: Vars2
    p_buildings_total: Vars3
    p_buildings_until_1919: Vars4
    p_buildings_1919_1948: Vars4
    p_buildings_1949_1978: Vars4
    p_buildings_1979_1995: Vars4
    p_buildings_1996_2004: Vars4
    p_buildings_2005_2011: Vars5
    p_buildings_2011_today: Vars5
    p_buildings_new: Vars6
    p_buildings_area_m2_com: Vars7
    r: Vars8
    s: Vars9
    s_fueloil: Vars10
    s_lpg: Vars10
    s_biomass: Vars10
    s_coal: Vars10
    s_petrol: Vars10
    s_heatnet: Vars10
    s_solarth: Vars11
    s_heatpump: Vars12
    s_gas: Vars13
    s_elec_heating: Vars14
    s_emethan: Vars15
    s_elec: Vars14
    p_elec_elcon: Vars16
    p_elec_heatpump: Vars16
    p_other: Vars17
    p_vehicles: Vars18
