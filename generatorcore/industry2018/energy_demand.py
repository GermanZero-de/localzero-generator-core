# pyright: strict
from dataclasses import dataclass

from ..inputs import Inputs
from .production_branches import (
    ExtraEmission,
    ProductionSubBranch,
    ProductionSubBranchCO2viaFEC,
    ProductionSubSum,
    ProductionBranch,
    ProductionSum,
)


@dataclass(kw_only=True)
class Production:

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


def calc_production(inputs: Inputs) -> Production:
    fact = inputs.fact
    entries = inputs.entries

    energy_consumption_industry = entries.i_energy_total

    energy_consumption_miner = energy_consumption_industry * entries.i_fec_pct_of_miner
    p_miner_cement = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="cement",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner_chalk = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="chalk",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner_glas = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="glas",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner_ceram = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="ceram",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_miner_cement, p_miner_chalk, p_miner_glas, p_miner_ceram]
    )

    energy_consumption_chemistry = (
        energy_consumption_industry * entries.i_fec_pct_of_chem
    )
    p_chem_basic = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="chem",
        sub_branch="basic",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    p_chem_ammonia = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="chem",
        sub_branch="ammonia",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    p_chem_other = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="chem",
        sub_branch="other",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    p_chem = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_chem_basic, p_chem_ammonia, p_chem_other]
    )

    energy_consumption_metal = energy_consumption_industry * entries.i_fec_pct_of_metal
    energy_consumption_metal_steel = energy_consumption_metal * fact(
        "Fact_I_P_metal_fec_pct_of_steel"
    )
    p_metal_steel_primary = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_primary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    p_metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_secondary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    p_metal_steel = ProductionSubSum.calc_production_sub_sum(
        energy_consumption_branch=energy_consumption_metal,
        sub_branch_list=[p_metal_steel_primary, p_metal_steel_secondary],
    )
    p_metal_nonfe = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="metal",
        sub_branch="nonfe",
        energy_consumption_branch=energy_consumption_metal,
    )
    p_metal = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_metal_steel, p_metal_nonfe]
    )

    energy_consumption_other = energy_consumption_industry * entries.i_fec_pct_of_other
    p_other_paper = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="paper",
        energy_consumption_branch=energy_consumption_other,
    )
    p_other_food = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="food",
        energy_consumption_branch=energy_consumption_other,
    )
    p_other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="further",
        energy_consumption_branch=energy_consumption_other,
    )
    p_other_2efgh = ExtraEmission.calc_extra_emission(
        inputs=inputs,
        branch="other",
        sub_branch="2efgh",
        energy_consumption=p_other_further.energy,
    )
    p_other = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_other_paper, p_other_food],
        sub_branch_via_FEC_list=[p_other_further],
        extra_emission_list=[p_other_2efgh],
    )

    p = ProductionSum.calc_production_sum(
        branch_list=[p_miner, p_chem, p_metal, p_other]
    )

    return Production(
        p=p,
        p_miner=p_miner,
        p_miner_cement=p_miner_cement,
        p_miner_chalk=p_miner_chalk,
        p_miner_glas=p_miner_glas,
        p_miner_ceram=p_miner_ceram,
        p_chem=p_chem,
        p_chem_basic=p_chem_basic,
        p_chem_ammonia=p_chem_ammonia,
        p_chem_other=p_chem_other,
        p_metal=p_metal,
        p_metal_steel=p_metal_steel,
        p_metal_steel_primary=p_metal_steel_primary,
        p_metal_steel_secondary=p_metal_steel_secondary,
        p_metal_nonfe=p_metal_nonfe,
        p_other=p_other,
        p_other_paper=p_other_paper,
        p_other_food=p_other_food,
        p_other_further=p_other_further,
        p_other_2efgh=p_other_2efgh,
    )
