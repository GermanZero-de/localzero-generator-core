# pyright: strict

from dataclasses import dataclass

from .supply_classes import EnergySum, EnergySource
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

    s: EnergySource
    s_fossil: EnergySum
    s_fossil_gas: EnergySource
    s_fossil_coal: EnergySource
    s_fossil_diesel: EnergySource
    s_fossil_fueloil: EnergySource
    s_fossil_lpg: EnergySource
    s_fossil_opetpro: EnergySource
    s_fossil_ofossil: EnergySource
    s_renew: EnergySum
    s_renew_biomass: EnergySource
    s_renew_heatnet: EnergySource
    s_renew_heatpump: EnergySource
    s_renew_solarth: EnergySource
    s_renew_elec: EnergySource
