# pyright: strict

from dataclasses import dataclass

from .energy_branches import (
    EnergySourceSubBranch,
    EnergySourceBranch,
    EnergySourceSubSum,
    EnergySourceSum,
)
from .production_branches import (
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

    s: EnergySourceSum

    s_miner: EnergySourceBranch
    s_miner_cement: EnergySourceSubBranch
    s_miner_chalk: EnergySourceSubBranch
    s_miner_glas: EnergySourceSubBranch
    s_miner_ceram: EnergySourceSubBranch

    s_chem: EnergySourceBranch
    s_chem_basic: EnergySourceSubBranch
    s_chem_ammonia: EnergySourceSubBranch
    s_chem_other: EnergySourceSubBranch

    s_metal: EnergySourceBranch
    s_metal_steel: EnergySourceSubSum
    s_metal_steel_primary: EnergySourceSubBranch
    s_metal_steel_secondary: EnergySourceSubBranch
    s_metal_nonfe: EnergySourceSubBranch

    s_other: EnergySourceBranch
    s_other_paper: EnergySourceSubBranch
    s_other_food: EnergySourceSubBranch
    s_other_further: EnergySourceSubBranch
