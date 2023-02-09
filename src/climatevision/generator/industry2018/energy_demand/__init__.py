# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

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

    total: ProductionSum

    miner: ProductionBranch
    miner_cement: ProductionSubBranch
    miner_chalk: ProductionSubBranch
    miner_glas: ProductionSubBranch
    miner_ceram: ProductionSubBranch

    chem: ProductionBranch
    chem_basic: ProductionSubBranch
    chem_ammonia: ProductionSubBranch
    chem_other: ProductionSubBranch

    metal: ProductionBranch
    metal_steel: ProductionSubSum
    metal_steel_primary: ProductionSubBranch
    metal_steel_secondary: ProductionSubBranch
    metal_nonfe: ProductionSubBranch

    other: ProductionBranch
    other_paper: ProductionSubBranch
    other_food: ProductionSubBranch
    other_further: ProductionSubBranchCO2viaFEC
    other_2efgh: ExtraEmission


def calc_production(inputs: Inputs) -> Production:
    fact = inputs.fact
    entries = inputs.entries

    energy_consumption_industry = entries.i_energy_total

    energy_consumption_miner = energy_consumption_industry * entries.i_fec_pct_of_miner
    miner_cement = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="cement",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner_chalk = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="chalk",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner_glas = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="glas",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner_ceram = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="miner",
        sub_branch="ceram",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner = ProductionBranch.calc_production_sum(
        sub_branch_list=[miner_cement, miner_chalk, miner_glas, miner_ceram]
    )

    energy_consumption_chemistry = (
        energy_consumption_industry * entries.i_fec_pct_of_chem
    )
    chem_basic = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="chem",
        sub_branch="basic",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    chem_ammonia = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="chem",
        sub_branch="ammonia",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    chem_other = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="chem",
        sub_branch="other",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    chem = ProductionBranch.calc_production_sum(
        sub_branch_list=[chem_basic, chem_ammonia, chem_other]
    )

    energy_consumption_metal = energy_consumption_industry * entries.i_fec_pct_of_metal
    energy_consumption_metal_steel = energy_consumption_metal * fact(
        "Fact_I_P_metal_fec_pct_of_steel"
    )
    metal_steel_primary = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_primary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_secondary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    metal_steel = ProductionSubSum.calc_production_sub_sum(
        energy_consumption_branch=energy_consumption_metal,
        sub_branch_list=[metal_steel_primary, metal_steel_secondary],
    )
    metal_nonfe = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="metal",
        sub_branch="nonfe",
        energy_consumption_branch=energy_consumption_metal,
    )
    metal = ProductionBranch.calc_production_sum(
        sub_branch_list=[metal_steel, metal_nonfe]
    )

    energy_consumption_other = energy_consumption_industry * entries.i_fec_pct_of_other
    other_paper = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="paper",
        energy_consumption_branch=energy_consumption_other,
    )
    other_food = ProductionSubBranch.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="food",
        energy_consumption_branch=energy_consumption_other,
    )
    other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="further",
        energy_consumption_branch=energy_consumption_other,
    )
    other_2efgh = ExtraEmission.calc_extra_emission(
        inputs=inputs,
        branch="other",
        sub_branch="2efgh",
        energy_consumption=other_further.energy,
    )
    other = ProductionBranch.calc_production_sum(
        sub_branch_list=[other_paper, other_food],
        sub_branch_via_FEC_list=[other_further],
        extra_emission_list=[other_2efgh],
    )

    total = ProductionSum.calc_production_sum(
        branch_list=[miner, chem, metal, other]
    )

    return Production(
        total=total,
        miner=miner,
        miner_cement=miner_cement,
        miner_chalk=miner_chalk,
        miner_glas=miner_glas,
        miner_ceram=miner_ceram,
        chem=chem,
        chem_basic=chem_basic,
        chem_ammonia=chem_ammonia,
        chem_other=chem_other,
        metal=metal,
        metal_steel=metal_steel,
        metal_steel_primary=metal_steel_primary,
        metal_steel_secondary=metal_steel_secondary,
        metal_nonfe=metal_nonfe,
        other=other,
        other_paper=other_paper,
        other_food=other_food,
        other_further=other_further,
        other_2efgh=other_2efgh,
    )
