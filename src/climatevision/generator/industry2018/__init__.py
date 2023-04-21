"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/industry.html
"""

# pyright: strict

from ..inputs import Inputs

from .i18 import I18
from . import energy_demand, energy_source


def calc(inputs: Inputs, inputs_germany: Inputs) -> I18:
    production_germany = energy_demand.calc_production_by_energy(inputs_germany)

    production = energy_demand.calc_production_by_co2e(
        inputs, inputs_germany, production_germany
    )
    supply = energy_source.calc_supply(inputs, production)

    i = production.total

    return I18(
        i=i,
        p=production.total,
        p_germany=production_germany.total,
        p_miner=production.miner,
        p_miner_cement=production.miner_cement,
        p_miner_chalk=production.miner_chalk,
        p_miner_glas=production.miner_glas,
        p_miner_ceram=production.miner_ceram,
        p_chem=production.chem,
        p_chem_basic=production.chem_basic,
        p_chem_ammonia=production.chem_ammonia,
        p_chem_other=production.chem_other,
        p_metal=production.metal,
        p_metal_steel=production.metal_steel,
        p_metal_steel_primary=production.metal_steel_primary,
        p_metal_steel_secondary=production.metal_steel_secondary,
        p_metal_nonfe=production.metal_nonfe,
        p_other=production.other,
        p_other_paper=production.other_paper,
        p_other_food=production.other_food,
        p_other_further=production.other_further,
        p_other_2efgh=production.other_2efgh,
        s=supply.s,
        s_fossil=supply.s_fossil,
        s_fossil_gas=supply.s_fossil_gas,
        s_fossil_coal=supply.s_fossil_coal,
        s_fossil_diesel=supply.s_fossil_diesel,
        s_fossil_fueloil=supply.s_fossil_fueloil,
        s_fossil_lpg=supply.s_fossil_lpg,
        s_fossil_opetpro=supply.s_fossil_opetpro,
        s_fossil_ofossil=supply.s_fossil_ofossil,
        s_renew=supply.s_renew,
        s_renew_biomass=supply.s_renew_biomass,
        s_renew_heatnet=supply.s_renew_heatnet,
        s_renew_elec=supply.s_renew_elec,
        s_renew_orenew=supply.s_renew_orenew,
    )
