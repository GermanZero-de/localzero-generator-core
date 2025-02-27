# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts
from ...common.energy import Energy

from ..energy_base import Energies

from .supply_branches import EnergySupplySubBranch, EnergySupplySum


@dataclass(kw_only=True)
class EnergySupply:
    total: Energy
    fossil: Energy
    fossil_gas: Energy
    fossil_coal: Energy
    fossil_diesel: Energy
    fossil_fueloil: Energy
    fossil_lpg: Energy
    fossil_opetpro: Energy
    fossil_ofossil: Energy
    renew: Energy
    renew_biomass: Energy
    renew_heatnet: Energy
    renew_elec: Energy
    renew_orenew: Energy


def calc_supply(facts: Facts, energies: Energies) -> EnergySupply:

    # do for all subbranches + copy structure for branches from production_branches
    miner_cement = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.miner_cement.energy,
        sub_branch="cement",
        branch="miner",
    )
    miner_chalk = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.miner_chalk.energy,
        sub_branch="chalk",
        branch="miner",
    )
    miner_glas = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.miner_glas.energy,
        sub_branch="glas",
        branch="miner",
    )
    miner_ceram = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.miner_ceram.energy,
        sub_branch="ceram",
        branch="miner",
    )
    miner = EnergySupplySum.sum(miner_cement, miner_chalk, miner_glas, miner_ceram)

    chem_basic = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.chem_basic.energy,
        sub_branch="basic",
        branch="chem",
    )
    chem_ammonia = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.chem_ammonia.energy,
        sub_branch="basic",  # assumtion same as chem basic (TODO Find specific factors for ammonia production) -> Erwartung wäre, dass sub_branch amonia oder so wäre
        branch="chem",
    )
    chem_other = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.chem_other.energy,
        sub_branch="other",
        branch="chem",
    )
    chem = EnergySupplySum.sum(chem_basic, chem_ammonia, chem_other)

    metal_steel_primary = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.metal_steel_primary.energy,
        sub_branch="steel_primary",
        branch="metal",
    )
    metal_steel_secondary = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.metal_steel_secondary.energy,
        sub_branch="steel_secondary",
        branch="metal",
    )
    metal_nonfe = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.metal_nonfe.energy,
        sub_branch="nonfe",
        branch="metal",
    )
    metal = EnergySupplySum.sum(metal_steel_primary, metal_steel_secondary, metal_nonfe)

    other_paper = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.other_paper.energy,
        sub_branch="paper",
        branch="other",
    )
    other_food = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.other_food.energy,
        sub_branch="food",
        branch="other",
    )
    other_further = EnergySupplySubBranch.calc_sub_branch(
        facts=facts,
        energy_demand=energies.other_further.energy,
        sub_branch="further",
        branch="other",
    )
    other = EnergySupplySum.sum(other_paper, other_food, other_further)

    total = EnergySupplySum.sum(miner, metal, chem, other)

    return EnergySupply(
        total=total.total,
        fossil=total.fossil,
        fossil_gas=total.fossil_gas,
        fossil_coal=total.fossil_coal,
        fossil_diesel=total.fossil_diesel,
        fossil_fueloil=total.fossil_fueloil,
        fossil_lpg=total.fossil_lpg,
        fossil_opetpro=total.fossil_opetpro,
        fossil_ofossil=total.fossil_ofossil,
        renew=total.renew,
        renew_biomass=total.renew_biomass,
        renew_heatnet=total.renew_heatnet,
        renew_elec=total.renew_elec,
        renew_orenew=total.renew_orenew,
    )
