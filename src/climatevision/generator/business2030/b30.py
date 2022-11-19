# pyright: strict

from dataclasses import dataclass

from ..common.g import G

from .dataclasses import (
    Vars0,
    GConsult,
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
    b: Vars0
    g: G
    g_consult: GConsult
    p: Vars3
    p_nonresi: Vars4
    p_nonresi_com: Vars5
    p_elec_elcon: Vars6
    p_elec_heatpump: Vars7
    p_vehicles: Vars8
    p_other: Vars9
    s: Vars10
    s_gas: Vars11
    s_emethan: Vars12
    s_lpg: Vars13
    s_petrol: Vars13
    s_jetfuel: Vars13
    s_diesel: Vars13
    s_fueloil: Vars14
    s_biomass: Vars15
    s_coal: Vars14
    s_heatnet: Vars15
    s_elec_heating: Vars13
    s_heatpump: Vars16
    s_solarth: Vars17
    s_elec: Vars13
    rb: Vars18
