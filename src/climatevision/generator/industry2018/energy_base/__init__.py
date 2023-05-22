# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy

from ..energy_demand import Production


@dataclass(kw_only=True)
class Energies:
    miner_cement: Energy
    miner_chalk: Energy
    miner_glas: Energy
    miner_ceram: Energy
    chem_basic: Energy
    chem_ammonia: Energy
    chem_other: Energy
    metal_steel_primary: Energy
    metal_steel_secondary: Energy
    metal_nonfe: Energy
    other_paper: Energy
    other_food: Energy
    other_further: Energy


def calc(production: Production) -> Energies:

    miner_cement = Energy(energy=production.miner_cement.energy)
    miner_chalk = Energy(energy=production.miner_chalk.energy)
    miner_glas = Energy(energy=production.miner_glas.energy)
    miner_ceram = Energy(energy=production.miner_ceram.energy)
    chem_basic = Energy(energy=production.chem_basic.energy)
    chem_ammonia = Energy(energy=production.chem_ammonia.energy)
    chem_other = Energy(energy=production.chem_other.energy)
    metal_steel_primary = Energy(energy=production.metal_steel_primary.energy)
    metal_steel_secondary = Energy(energy=production.metal_steel_secondary.energy)
    metal_nonfe = Energy(energy=production.metal_nonfe.energy)
    other_paper = Energy(energy=production.other_paper.energy)
    other_food = Energy(energy=production.other_food.energy)
    other_further = Energy(energy=production.other_further.energy)

    return Energies(
        miner_cement=miner_cement,
        miner_chalk=miner_chalk,
        miner_glas=miner_glas,
        miner_ceram=miner_ceram,
        chem_basic=chem_basic,
        chem_ammonia=chem_ammonia,
        chem_other=chem_other,
        metal_steel_primary=metal_steel_primary,
        metal_steel_secondary=metal_steel_secondary,
        metal_nonfe=metal_nonfe,
        other_paper=other_paper,
        other_food=other_food,
        other_further=other_further,
    )
