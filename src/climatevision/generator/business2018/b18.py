# pyright: strict

from dataclasses import dataclass

from .energy_demand import (
    Vars2,
    Vars3,
    Vars4,
)
from .dataclasses import (
    Vars0,
    Vars5,
    Vars6,
    Vars7,
    Vars8,
    Vars9,
    Vars10,
)


@dataclass(kw_only=True)
class B18:
    b: Vars0
    p: Vars2
    p_nonresi: Vars3
    p_nonresi_com: Vars4
    p_elec_elcon: Vars2
    p_elec_heatpump: Vars2
    p_vehicles: Vars2
    p_other: Vars2
    s: Vars5
    s_gas: Vars6
    s_lpg: Vars6
    s_petrol: Vars6
    s_jetfuel: Vars6
    s_diesel: Vars6
    s_fueloil: Vars6
    s_biomass: Vars7
    s_coal: Vars6
    s_heatnet: Vars6
    s_elec_heating: Vars8
    s_heatpump: Vars6
    s_solarth: Vars6
    s_elec: Vars8
    rb: Vars9
    rp_p: Vars10
