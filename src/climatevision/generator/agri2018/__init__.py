"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts
from ..lulucf2018.l18 import L18
from ..business2018.b18 import B18

from .a18 import A18
from .energy_demand import CO2eEmission
from . import energy_base, energy_demand, energy_source


def calc(entries: Entries, facts: Facts, l18: L18, b18: B18) -> A18:
    energies = energy_base.calc(entries=entries)

    supply = energy_source.calc_supply(facts, energies)
    production = energy_demand.calc_production(entries, facts, l18, b18, energies)

    a = CO2eEmission(
        CO2e_production_based=production.total.CO2e_production_based,
        CO2e_combustion_based=supply.total.CO2e_combustion_based,
    )

    return A18(
        p_fermen_dairycow=production.fermen_dairycow,
        p_fermen_nondairy=production.fermen_nondairy,
        p_fermen_swine=production.fermen_swine,
        p_fermen_poultry=production.fermen_poultry,
        p_fermen_oanimal=production.fermen_oanimal,
        p_fermen=production.fermen,
        p_manure_dairycow=production.manure_dairycow,
        p_manure_nondairy=production.manure_nondairy,
        p_manure_swine=production.manure_swine,
        p_manure_poultry=production.manure_poultry,
        p_manure_oanimal=production.manure_oanimal,
        p_manure_deposition=production.manure_deposition,
        p_manure=production.manure,
        p_soil_fertilizer=production.soil_fertilizer,
        p_soil_manure=production.soil_manure,
        p_soil_sludge=production.soil_sludge,
        p_soil_ecrop=production.soil_ecrop,
        p_soil_residue=production.soil_residue,
        p_soil_grazing=production.soil_grazing,
        p_soil_orgfarm=production.soil_orgfarm,
        p_soil_orgloss=production.soil_orgloss,
        p_soil_leaching=production.soil_leaching,
        p_soil_deposition=production.soil_deposition,
        p_soil=production.soil,
        p_other_liming_calcit=production.other_liming_calcit,
        p_other_liming_dolomite=production.other_liming_dolomite,
        p_other_liming=production.other_liming,
        p_other_urea=production.other_urea,
        p_other_ecrop=production.other_ecrop,
        p_other_kas=production.other_kas,
        p_other=production.other,
        p_operation_elec_heatpump=production.operation_elec_heatpump,
        p_operation=production.operation,
        p_operation_elec_elcon=production.operation_elec_elcon,
        p_operation_vehicles=production.operation_vehicles,
        p_operation_heat=production.operation_heat,
        p=production.total,
        s_petrol=supply.petrol,
        s_diesel=supply.diesel,
        s_fueloil=supply.fueloil,
        s_lpg=supply.lpg,
        s_gas=supply.gas,
        s_biomass=supply.biomass,
        s_elec=supply.elec,
        s_heatpump=supply.heatpump,
        s=supply.total,
        a=a,
    )
