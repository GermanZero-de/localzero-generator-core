# pyright: strict

from dataclasses import dataclass

from .energy_source import Energy
from .energy_demand import (
    ExtraEmission,
    ProductionSubBranch,
    ProductionSubBranchCO2viaFEC,
    ProductionSubSum,
    ProductionBranch,
    ProductionSum,
)


@dataclass(kw_only=True)
class I18:
    i: ProductionSum
    p: ProductionSum
    p_germany: ProductionSum

    p_miner: ProductionBranch
    p_miner_cement: ProductionSubBranch
    p_miner_chalk: ProductionSubBranch
    p_miner_glas: ProductionSubBranch
    p_miner_ceram: ProductionSubBranch

    p_chem: ProductionBranch
    p_chem_basic: ProductionSubBranch
    p_chem_ammonia: ProductionSubBranch
    p_chem_other: ProductionSubBranch

    p_metal: ProductionBranch
    p_metal_steel: ProductionSubSum
    p_metal_steel_primary: ProductionSubBranch
    p_metal_steel_secondary: ProductionSubBranch
    p_metal_nonfe: ProductionSubBranch

    p_other: ProductionBranch
    p_other_paper: ProductionSubBranch
    p_other_food: ProductionSubBranch

    p_other_further: ProductionSubBranchCO2viaFEC
    p_other_2efgh: ExtraEmission

    s: Energy
    s_fossil: Energy
    s_fossil_gas: Energy
    s_fossil_coal: Energy
    s_fossil_diesel: Energy
    s_fossil_fueloil: Energy
    s_fossil_lpg: Energy
    s_fossil_opetpro: Energy
    s_fossil_ofossil: Energy
    s_renew: Energy
    s_renew_biomass: Energy
    s_renew_heatnet: Energy
    s_renew_elec: Energy
    s_renew_orenew: Energy
