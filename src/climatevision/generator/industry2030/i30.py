# pyright: strict

from dataclasses import dataclass

from ..common.g import G

from .dataclasses import (
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
)


@dataclass(kw_only=True)
class I30:
    g: G
    g_consult: Vars1
    i: Vars2
    p: Vars3
    p_miner: Vars4
    p_miner_cement: Vars5
    p_miner_chalk: Vars5
    p_miner_glas: Vars6
    p_miner_ceram: Vars7
    p_chem: Vars8
    p_chem_basic: Vars5
    p_chem_ammonia: Vars6
    p_chem_other: Vars5
    p_metal: Vars9
    p_metal_steel: Vars10
    p_metal_steel_primary: Vars11
    p_metal_steel_secondary: Vars6
    p_metal_nonfe: Vars7
    p_other: Vars12
    p_other_paper: Vars13
    p_other_food: Vars13
    p_other_further: Vars14
    p_other_2efgh: Vars15
    s: Vars16
    s_fossil_gas: Vars16
    s_fossil_coal: Vars16
    s_fossil_diesel: Vars16
    s_fossil_fueloil: Vars16
    s_fossil_lpg: Vars16
    s_fossil_opetpro: Vars16
    s_fossil_ofossil: Vars16
    s_renew: Vars16
    s_renew_hydrogen: Vars16
    s_renew_emethan: Vars16
    s_renew_biomass: Vars16
    s_renew_heatnet: Vars16
    s_renew_heatpump: Vars16
    s_renew_solarth: Vars16
    s_renew_elec: Vars16
