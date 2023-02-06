# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..common.energy import Energy, EnergyWithPercentage
from .energy_demand import Production
from .energy_branches import (
    EnergySourceSubBranch,
    EnergySourceBranch,
    EnergySourceSum,
)


@dataclass(kw_only=True)
class EnergySource:
    s: EnergyWithPercentage
    s_fossil: Energy
    s_fossil_gas: EnergyWithPercentage
    s_fossil_coal: EnergyWithPercentage
    s_fossil_diesel: EnergyWithPercentage
    s_fossil_fueloil: EnergyWithPercentage
    s_fossil_lpg: EnergyWithPercentage
    s_fossil_opetpro: EnergyWithPercentage
    s_fossil_ofossil: EnergyWithPercentage
    s_renew: Energy
    s_renew_biomass: EnergyWithPercentage
    s_renew_heatnet: EnergyWithPercentage
    s_renew_elec: EnergyWithPercentage
    s_renew_orenew: EnergyWithPercentage


# TODO Energy calculation with new facts for each sector
def calc_supply(inputs: Inputs, production: Production) -> EnergySource:

    # do for all subbranches + copy structure for branches from production_branches
    s_miner_cement = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_miner_cement.energy,
        sub_branch="cement",
        branch="miner",
    )
    s_miner_chalk = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_miner_chalk.energy,
        sub_branch="chalk",
        branch="miner",
    )
    s_miner_glas = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_miner_glas.energy,
        sub_branch="glas",
        branch="miner",
    )
    s_miner_ceram = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_miner_ceram.energy,
        sub_branch="ceram",
        branch="miner",
    )
    s_miner = EnergySourceBranch.calc_energy_source_sum(
        sub_branch_list=[s_miner_cement, s_miner_chalk, s_miner_glas, s_miner_ceram]
    )

    s_chem_basic = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_chem_basic.energy,
        sub_branch="basic",
        branch="chem",
    )
    s_chem_ammonia = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_chem_ammonia.energy,
        sub_branch="ammonia",
        branch="chem",
    )
    s_chem_other = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_chem_other.energy,
        sub_branch="other",
        branch="chem",
    )
    s_chem = EnergySourceBranch.calc_energy_source_sum(
        sub_branch_list=[s_chem_basic, s_chem_ammonia, s_chem_other]
    )

    s_metal_steel_primary = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_metal_steel_primary.energy,
        sub_branch="steel_primary",
        branch="metal",
    )

    s_metal_steel_secondary = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_metal_steel_secondary.energy,
        sub_branch="steel_secondary",
        branch="metal",
    )

    s_metal_nonfe = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_metal_nonfe.energy,
        sub_branch="nonfe",
        branch="metal",
    )

    s_metal = EnergySourceBranch.calc_energy_source_sum(
        sub_branch_list=[s_metal_steel_primary, s_metal_steel_secondary, s_metal_nonfe]
    )

    s_other_paper = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_other_paper.energy,
        sub_branch="paper",
        branch="other",
    )
    s_other_food = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_other_food.energy,
        sub_branch="food",
        branch="other",
    )
    s_other_further = EnergySourceSubBranch.calc_energy_source_sub_branch(
        inputs=inputs,
        energy_demand=production.p_other_further.energy,
        sub_branch="further",
        branch="other",
    )

    s_other = EnergySourceBranch.calc_energy_source_sum(
        sub_branch_list=[s_other_paper, s_other_food, s_other_further]
    )

    s = EnergySourceSum.calc_energy_source_sum(
        branch_list=[s_miner, s_metal, s_chem, s_other]
    )

    return EnergySource(
        s=s.s,
        s_fossil=s.s_fossil,
        s_fossil_gas=s.s_fossil_gas,
        s_fossil_coal=s.s_fossil_coal,
        s_fossil_diesel=s.s_fossil_diesel,
        s_fossil_fueloil=s.s_fossil_fueloil,
        s_fossil_lpg=s.s_fossil_lpg,
        s_fossil_opetpro=s.s_fossil_opetpro,
        s_fossil_ofossil=s.s_fossil_ofossil,
        s_renew=s.s_renew,
        s_renew_biomass=s.s_renew_biomass,
        s_renew_heatnet=s.s_renew_heatnet,
        s_renew_elec=s.s_renew_elec,
        s_renew_orenew=s.s_renew_orenew,
    )
