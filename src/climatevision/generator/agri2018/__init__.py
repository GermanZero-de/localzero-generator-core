"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from ..inputs import Inputs
from ..lulucf2018.l18 import L18
from ..business2018.b18 import B18

from .a18 import A18
from .energy_demand import CO2eEmissions
from . import energy_demand, energy_source


def calc(inputs: Inputs, l18: L18, b18: B18) -> A18:
    entries = inputs.entries

    # Energy
    total_energy = (
        entries.a_petrol_fec
        + entries.a_diesel_fec
        + entries.a_fueloil_fec
        + entries.a_lpg_fec
        + entries.a_gas_fec
        + entries.a_biomass_fec
        + entries.a_elec_fec
    )

    supply = energy_source.calc_supply(inputs, total_energy)
    production = energy_demand.calc_production(
        inputs,
        l18,
        b18,
        total_energy,
        supply.s_elec.energy,
        supply.s_petrol.energy,
        supply.s_diesel.energy,
        supply.s_fueloil.energy,
        supply.s_lpg.energy,
        supply.s_gas.energy,
        supply.s_biomass.energy,
    )

    a = CO2eEmissions(
        CO2e_total=production.p.CO2e_total + supply.s.CO2e_total,
        CO2e_production_based=production.p.CO2e_production_based,
        CO2e_combustion_based=supply.s.CO2e_combustion_based,
    )

    return A18(
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
        s=supply.s,
        a=a,
    )
