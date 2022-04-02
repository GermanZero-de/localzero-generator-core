# pyright: strict
from dataclasses import dataclass
from .co2e import CO2e
from ..inputs import Inputs
from .co2e_per_t import CO2e_per_t
from .co2e_basic import CO2e_basic
from .co2e_per_mwh import CO2e_per_MWh
from .co2e_with_pct_energy import CO2e_with_pct_energy


@dataclass(kw_only=True)
class Production:
    p: CO2e

    p_miner: CO2e
    p_miner_cement: CO2e_per_t
    p_miner_chalk: CO2e_per_t
    p_miner_glas: CO2e_per_t
    p_miner_ceram: CO2e_per_t

    p_chem: CO2e
    p_chem_basic: CO2e_per_t
    p_chem_ammonia: CO2e_per_t
    p_chem_other: CO2e_per_t

    p_metal: CO2e
    p_metal_steel: CO2e_with_pct_energy
    p_metal_steel_primary: CO2e_per_t
    p_metal_steel_secondary: CO2e_per_t
    p_metal_nonfe: CO2e_per_t

    p_other: CO2e
    p_other_paper: CO2e_per_t
    p_other_food: CO2e_per_t
    p_other_further: CO2e_per_MWh
    p_other_2efgh: CO2e_basic


def calc_energy_demand(inputs: Inputs) -> Production:
    fact = inputs.fact
    entries = inputs.entries

    p_miner_energy = entries.i_fec_pct_of_miner * entries.i_energy_total
    p_miner_cement = CO2e_per_t.calc_p_miner_cement(inputs, p_miner_energy)
    p_miner_chalk = CO2e_per_t.calc_p_miner_chalk(inputs, p_miner_energy)
    p_miner_glas = CO2e_per_t.calc_p_miner_glas(inputs, p_miner_energy)
    p_miner_ceram = CO2e_per_t.calc_p_miner_ceram(inputs, p_miner_energy)
    p_miner = p_miner_cement + p_miner_chalk + p_miner_glas + p_miner_ceram

    p_chem_energy = entries.i_fec_pct_of_chem * entries.i_energy_total
    p_chem_basic = CO2e_per_t.calc_p_chem_basic(inputs, p_chem_energy)
    p_chem_ammonia = CO2e_per_t.calc_p_chem_ammonia(inputs, p_chem_energy)
    p_chem_other = CO2e_per_t.calc_p_chem_other(inputs, p_chem_energy)
    p_chem = p_chem_basic + p_chem_ammonia + p_chem_other

    p_metal_energy = entries.i_fec_pct_of_metal * entries.i_energy_total
    p_metal_steel_pct_energy = fact("Fact_I_P_metal_fec_pct_of_steel_2018")
    p_metal_steel_energy = p_metal_energy * p_metal_steel_pct_energy
    p_metal_steel_primary = CO2e_per_t.calc_p_metal_steel_primary_route(
        inputs, p_metal_steel_energy
    )
    p_metal_steel_secondary = CO2e_per_t.calc_p_metal_steel_secondary_route(
        inputs, p_metal_steel_energy
    )
    p_metal_steel = CO2e_with_pct_energy.calc_p_metal_steel(
        inputs,
        p_metal_steel_pct_energy,
        p_metal_steel_energy,
        p_metal_steel_primary,
        p_metal_steel_secondary,
    )
    p_metal_nonfe = CO2e_per_t.calc_p_metal_non_fe(inputs, p_metal_energy)
    p_metal = p_metal_steel + p_metal_nonfe
    p_metal.energy = p_metal_energy

    p_other_energy = entries.i_fec_pct_of_other * entries.i_energy_total
    p_other_paper = CO2e_per_t.calc_p_other_paper(inputs, p_other_energy)
    p_other_food = CO2e_per_t.calc_p_other_food(inputs, p_other_energy)
    p_other_further = CO2e_per_MWh.calc_p_other_further(inputs, p_other_energy)
    p_other_2efgh = CO2e_basic.calc_p_other_2efgh(inputs, p_other_further.energy)
    p_other = p_other_paper + p_other_food
    p_other.energy = p_other_energy

    p_other.CO2e_combustion_based += +p_other_further.CO2e_combustion_based
    p_other.CO2e_production_based += (
        +p_other_further.CO2e_production_based + p_other_2efgh.CO2e_production_based
    )
    p_other.CO2e_total += +p_other_further.CO2e_total + p_other_2efgh.CO2e_total

    p = p_miner + p_chem + p_metal + p_other
    p.energy = entries.i_energy_total

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
