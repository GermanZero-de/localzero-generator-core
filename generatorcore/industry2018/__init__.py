# pyright: strict
from ..inputs import Inputs
from .i18 import I18
from .energy_demand import calc_production
from .energy_source import calc_energy_sources


# for mineral industry the energy_use_factor still needs to be added to facts
def calc(inputs: Inputs) -> I18:

    production = calc_production(inputs)
    energy_source = calc_energy_sources(inputs)

    i = production.p

    return I18(
        i=i,
        p=production.p,
        p_miner=production.p_miner,
        p_miner_cement=production.p_miner_cement,
        p_miner_chalk=production.p_miner_chalk,
        p_miner_glas=production.p_miner_glas,
        p_miner_ceram=production.p_miner_ceram,
        p_chem=production.p_chem,
        p_chem_basic=production.p_chem_basic,
        p_chem_ammonia=production.p_chem_ammonia,
        p_chem_other=production.p_chem_other,
        p_metal=production.p_metal,
        p_metal_steel=production.p_metal_steel,
        p_metal_steel_primary=production.p_metal_steel_primary,
        p_metal_steel_secondary=production.p_metal_steel_secondary,
        p_metal_nonfe=production.p_metal_nonfe,
        p_other=production.p_other,
        p_other_paper=production.p_other_paper,
        p_other_food=production.p_other_food,
        p_other_further=production.p_other_further,
        p_other_2efgh=production.p_other_2efgh,
        s=energy_source.s,
        s_fossil=energy_source.s_fossil,
        s_fossil_gas=energy_source.s_fossil_gas,
        s_fossil_coal=energy_source.s_fossil_coal,
        s_fossil_diesel=energy_source.s_fossil_diesel,
        s_fossil_fueloil=energy_source.s_fossil_fueloil,
        s_fossil_lpg=energy_source.s_fossil_lpg,
        s_fossil_opetpro=energy_source.s_fossil_opetpro,
        s_fossil_ofossil=energy_source.s_fossil_ofossil,
        s_renew=energy_source.s_renew,
        s_renew_biomass=energy_source.s_renew_biomass,
        s_renew_heatnet=energy_source.s_renew_heatnet,
        s_renew_heatpump=energy_source.s_renew_heatpump,
        s_renew_solarth=energy_source.s_renew_solarth,
        s_renew_elec=energy_source.s_renew_elec,
    )
