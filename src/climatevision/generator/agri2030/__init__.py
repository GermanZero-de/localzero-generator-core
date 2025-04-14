"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from ..agri2018.a18 import A18
from ..lulucf2030.l30 import L30
from ..makeentries import Entries
from ..refdata import Assumptions, Facts
from . import energy_demand, energy_general, energy_source
from .a30 import A30
from .co2e_change_a import CO2eChangeA


def calc(
    entries: Entries, facts: Facts, assumptions: Assumptions, a18: A18, l30: L30
) -> A30:

    production = energy_demand.calc_production(
        facts,
        assumptions,
        entries,
        entries.m_duration_neutral,
        entries.m_duration_target,
        entries.m_population_com_2018,
        entries.m_population_nat,
        entries.r_rehab_rate_pa,
        a18,
        l30,
    )
    supply = energy_source.calc_supply(
        facts,
        entries,
        assumptions,
        entries.m_duration_neutral,
        entries.m_duration_target,
        entries.m_population_com_2018,
        entries.m_population_nat,
        a18,
        production,
    )
    general = energy_general.calc_general(
        facts,
        assumptions,
        entries.m_duration_target,
        entries.a_farm_amount,
        entries.m_area_agri_com,
        entries.a_area_agri_com_pct_of_organic,
    )

    a = CO2eChangeA(
        facts=facts,
        entries=entries,
        duration_until_target_year=entries.m_duration_target,
        duration_CO2e_neutral_years=entries.m_duration_neutral,
        what="a",
        a18=a18,
        p_operation=production.operation,
        p=production.total,
        g=general.g,
        s=supply.total,
    )

    return A30(
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
        s_emethan=supply.emethan,
        s=supply.total,
        a=a,
        g=general.g,
        g_consult=general.g_consult,
        g_organic=general.g_organic,
    )
