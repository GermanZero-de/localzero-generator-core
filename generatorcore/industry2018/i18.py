# pyright: strict
from dataclasses import dataclass
from .energy_sum import EnergySum, Energy_pct
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

    s: Energy_pct
    s_fossil: EnergySum
    s_fossil_gas: Energy_pct
    s_fossil_coal: Energy_pct
    s_fossil_diesel: Energy_pct
    s_fossil_fueloil: Energy_pct
    s_fossil_lpg: Energy_pct
    s_fossil_opetpro: Energy_pct
    s_fossil_ofossil: Energy_pct
    s_renew: EnergySum
    s_renew_biomass: Energy_pct
    s_renew_heatnet: Energy_pct
    s_renew_heatpump: Energy_pct
    s_renew_solarth: Energy_pct
    s_renew_elec: Energy_pct
