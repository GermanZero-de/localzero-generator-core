# pyright: strict

from dataclasses import dataclass

from .dataclasses import Vars1, Vars2, Vars3, Vars4, Vars5, Vars6, Vars7, Vars8, Vars9


@dataclass(kw_only=True)
class R18:
    r: Vars1
    p: Vars2
    p_buildings_total: Vars3
    p_buildings_until_1919: Vars3
    p_buildings_1919_1948: Vars3
    p_buildings_1949_1978: Vars3
    p_buildings_1979_1995: Vars3
    p_buildings_1996_2004: Vars3
    p_buildings_2005_2011: Vars4
    p_buildings_2011_today: Vars4
    p_buildings_area_m2_com: Vars5
    p_elec_elcon: Vars2
    p_elec_heatpump: Vars2
    p_vehicles: Vars2
    p_other: Vars2
    s: Vars6
    s_fueloil: Vars7
    s_lpg: Vars7
    s_biomass: Vars8
    s_coal: Vars7
    s_petrol: Vars7
    s_heatnet: Vars7
    s_solarth: Vars7
    s_heatpump: Vars7
    s_elec_heating: Vars7
    s_gas: Vars7
    s_elec: Vars9
