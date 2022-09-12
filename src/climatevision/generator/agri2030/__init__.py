"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from ..inputs import Inputs
from ..agri2018.a18 import A18
from ..lulucf2030.l30 import L30

from .co2eChangeA import CO2eChangeA
from .a30 import A30
from . import energy_demand, energy_source, energy_general


def calc(inputs: Inputs, a18: A18, l30: L30) -> A30:

    production = energy_demand.calc_production(inputs, a18, l30)
    supply = energy_source.calc_supply(inputs, a18, production)
    general = energy_general.calc_general(inputs=inputs)

    a = CO2eChangeA(
        inputs=inputs,
        what="a",
        a18=a18,
        p_operation=production.p_operation,
        p=production.p,
        g=general.g,
        s=supply.s,
    )

    return A30(
        p_fermen_dairycow=production.p_fermen_dairycow,
        p_fermen_nondairy=production.p_fermen_nondairy,
        p_fermen_swine=production.p_fermen_swine,
        p_fermen_poultry=production.p_fermen_poultry,
        p_fermen_oanimal=production.p_fermen_oanimal,
        p_fermen=production.p_fermen,
        p_manure_dairycow=production.p_manure_dairycow,
        p_manure_nondairy=production.p_manure_nondairy,
        p_manure_swine=production.p_manure_swine,
        p_manure_poultry=production.p_manure_poultry,
        p_manure_oanimal=production.p_manure_oanimal,
        p_manure_deposition=production.p_manure_deposition,
        p_manure=production.p_manure,
        p_soil_fertilizer=production.p_soil_fertilizer,
        p_soil_manure=production.p_soil_manure,
        p_soil_sludge=production.p_soil_sludge,
        p_soil_ecrop=production.p_soil_ecrop,
        p_soil_residue=production.p_soil_residue,
        p_soil_grazing=production.p_soil_grazing,
        p_soil_orgfarm=production.p_soil_orgfarm,
        p_soil_orgloss=production.p_soil_orgloss,
        p_soil_leaching=production.p_soil_leaching,
        p_soil_deposition=production.p_soil_deposition,
        p_soil=production.p_soil,
        p_other_liming_calcit=production.p_other_liming_calcit,
        p_other_liming_dolomite=production.p_other_liming_dolomite,
        p_other_liming=production.p_other_liming,
        p_other_urea=production.p_other_urea,
        p_other_ecrop=production.p_other_ecrop,
        p_other_kas=production.p_other_kas,
        p_other=production.p_other,
        p_operation_elec_heatpump=production.p_operation_elec_heatpump,
        p_operation=production.p_operation,
        p_operation_elec_elcon=production.p_operation_elec_elcon,
        p_operation_vehicles=production.p_operation_vehicles,
        p_operation_heat=production.p_operation_heat,
        p=production.p,
        s_petrol=supply.s_petrol,
        s_diesel=supply.s_diesel,
        s_fueloil=supply.s_fueloil,
        s_lpg=supply.s_lpg,
        s_gas=supply.s_gas,
        s_biomass=supply.s_biomass,
        s_elec=supply.s_elec,
        s_heatpump=supply.s_heatpump,
        s_emethan=supply.s_emethan,
        s=supply.s,
        a=a,
        g=general.g,
        g_consult=general.g_consult,
        g_organic=general.g_organic,
    )
