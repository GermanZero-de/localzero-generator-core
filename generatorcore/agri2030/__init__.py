"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict
from .dataclasses import Vars6, Vars7
from ..inputs import Inputs
from ..utils import div, MILLION
from .. import agri2018, lulucf2030
from .a30 import A30


def calc(inputs: Inputs, *, a18: agri2018.A18, l30: lulucf2030.L30) -> A30:
    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    a30 = A30()

    a = a30.a
    g = a30.g
    g_consult = a30.g_consult
    g_organic = a30.g_organic
    p = a30.p
    p_fermen = a30.p_fermen
    p_fermen_dairycow = a30.p_fermen_dairycow
    p_fermen_nondairy = a30.p_fermen_nondairy
    p_fermen_swine = a30.p_fermen_swine
    p_fermen_poultry = a30.p_fermen_poultry
    p_fermen_oanimal = a30.p_fermen_oanimal
    p_manure = a30.p_manure
    p_manure_dairycow = a30.p_manure_dairycow
    p_manure_nondairy = a30.p_manure_nondairy
    p_manure_swine = a30.p_manure_swine
    p_manure_poultry = a30.p_manure_poultry
    p_manure_oanimal = a30.p_manure_oanimal
    p_manure_deposition = a30.p_manure_deposition
    p_soil = a30.p_soil
    p_soil_fertilizer = a30.p_soil_fertilizer
    p_soil_manure = a30.p_soil_manure
    p_soil_sludge = a30.p_soil_sludge
    p_soil_ecrop = a30.p_soil_ecrop
    p_soil_grazing = a30.p_soil_grazing
    p_soil_residue = a30.p_soil_residue
    p_soil_orgfarm = a30.p_soil_orgfarm
    p_soil_orgloss = a30.p_soil_orgloss
    p_soil_leaching = a30.p_soil_leaching
    p_soil_deposition = a30.p_soil_deposition
    p_other = a30.p_other
    p_other_liming = a30.p_other_liming
    p_other_liming_calcit = a30.p_other_liming_calcit
    p_other_liming_dolomite = a30.p_other_liming_dolomite
    p_other_urea = a30.p_other_urea
    p_other_kas = a30.p_other_kas
    p_other_ecrop = a30.p_other_ecrop
    p_operation = a30.p_operation
    p_operation_heat = a30.p_operation_heat
    p_operation_elec_elcon = a30.p_operation_elec_elcon
    p_operation_vehicles = a30.p_operation_vehicles
    p_operation_elec_heatpump = a30.p_operation_elec_heatpump
    s = a30.s
    s_petrol = a30.s_petrol
    s_diesel = a30.s_diesel
    s_fueloil = a30.s_fueloil
    s_lpg = a30.s_lpg
    s_gas = a30.s_gas
    s_biomass = a30.s_biomass
    s_elec = a30.s_elec
    s_heatpump = a30.s_heatpump
    s_emethan = a30.s_emethan

    """ S T A R T """
    g_consult.area_ha_available = entries.a_farm_amount
    g_consult.invest_per_x = ass("Ass_A_G_consult_invest_per_farm")
    g_consult.pct_of_wage = ass("Ass_A_G_consult_invest_pct_of_wage")
    g_consult.ratio_wage_to_emplo = ass("Ass_A_G_consult_ratio_wage_to_emplo")
    g_consult.invest = g_consult.area_ha_available * g_consult.invest_per_x
    g_consult.invest_pa = g_consult.invest / entries.m_duration_target
    g_consult.invest_com = g_consult.invest * ass(
        "Ass_A_G_consult_invest_pct_of_public"
    )
    g_consult.invest_pa_com = g_consult.invest_pa * ass(
        "Ass_A_G_consult_invest_pct_of_public"
    )
    g_consult.cost_wage = g_consult.invest_pa * g_consult.pct_of_wage
    g_consult.demand_emplo = div(g_consult.cost_wage, g_consult.ratio_wage_to_emplo)
    g_consult.demand_emplo_new = g_consult.demand_emplo
    g_consult.demand_emplo_com = g_consult.demand_emplo_new

    g_organic.area_ha_available = entries.m_area_agri_com
    g_organic.invest_per_x = ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
    g_organic.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    g_organic.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    g_organic.power_to_be_installed_pct = ass("Ass_A_G_area_agri_pct_of_organic_2050")
    g_organic.power_installed = entries.a_area_agri_com_pct_of_organic
    g_organic.power_to_be_installed = g_organic.area_ha_available * (
        g_organic.power_to_be_installed_pct - g_organic.power_installed
    )
    g_organic.invest = g_organic.power_to_be_installed * g_organic.invest_per_x
    g_organic.invest_pa = g_organic.invest / entries.m_duration_target
    g_organic.cost_wage = g_organic.invest_pa * g_organic.pct_of_wage
    g_organic.demand_emplo = div(g_organic.cost_wage, g_organic.ratio_wage_to_emplo)
    g_organic.demand_emplo_new = g_organic.demand_emplo

    p_fermen_dairycow = Vars6.calc_fermen(
        inputs, "p_fermen_dairycow", "Ass_A_P_fermen_dairycow_change", a18
    )
    p_fermen_nondairy = Vars6.calc_fermen(
        inputs, "p_fermen_nondairy", "Ass_A_P_fermen_nondairy_change", a18
    )
    p_fermen_swine = Vars6.calc_fermen(
        inputs, "p_fermen_swine", "Ass_A_P_fermen_swine_change", a18
    )
    p_fermen_poultry = Vars6.calc_fermen(
        inputs, "p_fermen_poultry", "Ass_A_P_fermen_poultry_change", a18
    )
    p_fermen_oanimal = Vars6.calc_fermen(
        inputs, "p_fermen_oanimal", "Ass_A_P_fermen_oanimal_change", a18
    )
    a30.p_fermen_dairycow = p_fermen_dairycow
    a30.p_fermen_nondairy = p_fermen_nondairy
    a30.p_fermen_swine = p_fermen_swine
    a30.p_fermen_poultry = p_fermen_poultry
    a30.p_fermen_oanimal = p_fermen_oanimal

    p_manure_dairycow = Vars6.calc_manure(
        inputs, "p_manure_dairycow", a18, p_fermen_dairycow.amount
    )
    p_manure_nondairy = Vars6.calc_manure(
        inputs, "p_manure_nondairy", a18, p_fermen_nondairy.amount
    )
    p_manure_swine = Vars6.calc_manure(
        inputs, "p_manure_swine", a18, p_fermen_swine.amount
    )
    p_manure_poultry = Vars6.calc_manure(
        inputs, "p_manure_poultry", a18, p_fermen_poultry.amount
    )
    p_manure_oanimal = Vars6.calc_manure(
        inputs, "p_manure_oanimal", a18, p_fermen_oanimal.amount
    )
    p_manure_deposition = Vars6.calc_manure(
        inputs,
        "p_manure_deposition",
        a18,
        p_fermen_dairycow.amount
        + p_fermen_nondairy.amount
        + p_fermen_swine.amount
        + p_fermen_oanimal.amount,
    )
    a30.p_manure_dairycow = p_manure_dairycow
    a30.p_manure_nondairy = p_manure_nondairy
    a30.p_manure_swine = p_manure_swine
    a30.p_manure_poultry = p_manure_poultry
    a30.p_manure_oanimal = p_manure_oanimal
    a30.p_manure_deposition = p_manure_deposition

    p_soil_fertilizer = Vars7.calc_soil(
        inputs, "p_soil_fertilizer", a18, l30.g_crop.area_ha
    )
    p_soil_manure = Vars7.calc_soil(inputs, "p_soil_manure", a18, l30.g_crop.area_ha)
    p_soil_sludge = Vars7.calc_soil(inputs, "p_soil_sludge", a18, l30.g_crop.area_ha)
    p_soil_ecrop = Vars7.calc_soil(inputs, "p_soil_ecrop", a18, l30.g_crop.area_ha)
    p_soil_grazing = Vars7.calc_soil_grazing(
        inputs,
        "p_soil_grazing",
        a18,
        l30.g_grass.area_ha,
        p_fermen_dairycow,
        p_fermen_nondairy,
        p_fermen_oanimal,
    )
    p_soil_residue = Vars7.calc_soil_residue(
        inputs, "p_soil_residue", a18, l30.g_crop.area_ha
    )
    p_soil_orgfarm = Vars7.calc_soil_residue(
        inputs,
        "p_soil_orgfarm",
        a18,
        l30.g_crop_org_low.area_ha
        + l30.g_crop_org_high.area_ha
        + l30.g_grass_org_low.area_ha
        + l30.g_grass_org_high.area_ha,
    )
    p_soil_orgloss = Vars7.calc_soil_residue(
        inputs,
        "p_soil_orgloss",
        a18,
        l30.g_crop_org_low.area_ha + l30.g_crop_org_high.area_ha,
    )
    p_soil_leaching = Vars7.calc_soil(
        inputs, "p_soil_leaching", a18, l30.g_crop.area_ha + l30.g_grass.area_ha
    )
    p_soil_deposition = Vars7.calc_soil(
        inputs, "p_soil_deposition", a18, l30.g_crop.area_ha + l30.g_grass.area_ha
    )
    a30.p_soil_fertilizer = p_soil_fertilizer
    a30.p_soil_manure = p_soil_manure
    a30.p_soil_sludge = p_soil_sludge
    a30.p_soil_ecrop = p_soil_ecrop
    a30.p_soil_grazing = p_soil_grazing
    a30.p_soil_residue = p_soil_residue
    a30.p_soil_orgfarm = p_soil_orgfarm
    a30.p_soil_orgloss = p_soil_orgloss
    a30.p_soil_leaching = p_soil_leaching
    a30.p_soil_deposition = p_soil_deposition

    # Next

    p_fermen.CO2e_combustion_based = 0
    p_fermen.CO2e_total_2021_estimated = a18.p_fermen.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )

    p_manure.CO2e_combustion_based = 0
    p_manure.CO2e_total_2021_estimated = a18.p_manure.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )

    p.CO2e_total_2021_estimated = a18.p.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )

    g.invest_pa_outside = 0
    g.invest_outside = 0
    a.invest_pa_outside = g.invest_pa_outside
    a.invest_outside = g.invest_outside
    g.CO2e_total = 0
    a.CO2e_total_2021_estimated = a18.a.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )

    p_soil.CO2e_combustion_based = 0
    p_soil.CO2e_total_2021_estimated = a18.p_soil.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_other.CO2e_combustion_based = 0
    p_other.CO2e_total_2021_estimated = a18.p_other.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_other_liming.CO2e_combustion_based = 0
    p_other_liming.CO2e_total_2021_estimated = a18.p_other_liming.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_other_liming_calcit.demand_change = ass(
        "Ass_A_P_other_liming_calcit_amount_change"
    )
    p_other_liming_calcit.CO2e_production_based_per_t = fact(
        "Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_liming_calcit.CO2e_combustion_based = 0
    p_other_liming_calcit.CO2e_total_2021_estimated = (
        a18.p_other_liming_calcit.CO2e_total
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    p_other_liming_dolomite.demand_change = ass(
        "Ass_A_P_other_liming_dolomit_amount_change"
    )
    p_other_liming_dolomite.CO2e_production_based_per_t = fact(
        "Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_liming_dolomite.CO2e_combustion_based = 0
    p_other_liming_dolomite.CO2e_total_2021_estimated = (
        a18.p_other_liming_dolomite.CO2e_total
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    p_other_urea.demand_change = ass("Ass_A_P_other_urea_amount_change")
    p_other_urea.CO2e_production_based_per_t = fact(
        "Fact_A_P_other_urea_CO2e_pb_to_amount_2018"
    )
    p_other_urea.CO2e_combustion_based = 0
    p_other_urea.CO2e_total_2021_estimated = a18.p_other_urea.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_other_kas.demand_change = ass("Ass_A_P_other_kas_amount_change")
    p_other_kas.CO2e_production_based_per_t = fact(
        "Fact_A_P_other_kas_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_kas.CO2e_combustion_based = 0
    p_other_kas.CO2e_total_2021_estimated = a18.p_other_kas.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_other_ecrop.demand_change = ass("Ass_A_P_other_ecrop_amount_change")
    p_other_ecrop.CO2e_production_based_per_t = fact(
        "Fact_A_P_other_ecrop_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_ecrop.CO2e_combustion_based = 0
    p_other_ecrop.CO2e_total_2021_estimated = a18.p_other_ecrop.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_operation_heat.demand_electricity = 0
    p_operation_heat.demand_epetrol = 0
    p_operation_heat.demand_ediesel = 0
    p_operation_heat.area_m2 = a18.p_operation_heat.area_m2
    p_operation_heat.rate_rehab_pa = entries.r_rehab_rate_pa
    p_operation_heat.invest_per_x = fact(
        "Fact_R_P_energetical_renovation_cost_business"
    )
    p_operation_heat.pct_of_wage = fact(
        "Fact_B_P_renovations_ratio_wage_to_main_revenue_2017"
    )
    p_operation_heat.ratio_wage_to_emplo = fact(
        "Fact_B_P_renovations_wage_per_person_per_year_2017"
    )
    p_operation_heat.emplo_existing = (
        fact("Fact_B_P_renovation_emplo_2017")
        * ass("Ass_B_D_renovation_emplo_pct_of_A")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )
    p_operation_elec_elcon.demand_biomass = 0
    p_operation_elec_elcon.demand_heatpump = 0
    p_operation_elec_elcon.demand_ediesel = 0
    p_operation_elec_elcon.demand_emethan = 0
    p_operation_elec_elcon.demand_change = ass("Ass_B_D_fec_elec_elcon_change")
    p_operation_vehicles.demand_electricity = 0
    p_operation_vehicles.demand_biomass = 0
    p_operation_vehicles.demand_heatpump = 0
    p_operation_vehicles.demand_emethan = 0
    p_operation_vehicles.demand_change = ass("Ass_B_D_fec_vehicles_change")
    s_fueloil.energy = 0
    s_lpg.energy = 0
    s_gas.energy = 0
    s.CO2e_production_based = 0
    s_emethan.CO2e_combustion_based = 0
    s_emethan.CO2e_total = s_emethan.CO2e_combustion_based
    s_emethan.change_CO2e_t = s_emethan.CO2e_total
    s_emethan.change_CO2e_pct = div(s_emethan.change_CO2e_t, 0)
    s_emethan.CO2e_total_2021_estimated = 0 * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    s_emethan.cost_climate_saved = (
        (s_emethan.CO2e_total_2021_estimated - s_emethan.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s.CO2e_total_2021_estimated = a18.s.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_petrol.CO2e_production_based = 0
    s_petrol.CO2e_combustion_based_per_MWh = a18.s_petrol.CO2e_combustion_based_per_MWh
    s_petrol.CO2e_total_2021_estimated = a18.s_petrol.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_diesel.CO2e_production_based = 0
    s_diesel.CO2e_combustion_based_per_MWh = a18.s_diesel.CO2e_combustion_based_per_MWh
    s_diesel.CO2e_total_2021_estimated = a18.s_diesel.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_fueloil.area_m2 = 0
    s_fueloil.CO2e_production_based = 0
    s_fueloil.CO2e_combustion_based_per_MWh = (
        a18.s_fueloil.CO2e_combustion_based_per_MWh
    )
    s_fueloil.CO2e_total_2021_estimated = a18.s_fueloil.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_lpg.CO2e_production_based = 0
    s_lpg.CO2e_combustion_based_per_MWh = a18.s_lpg.CO2e_combustion_based_per_MWh
    s_lpg.CO2e_total_2021_estimated = a18.s_lpg.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_gas.area_m2 = 0
    s_gas.CO2e_production_based = 0
    s_gas.CO2e_combustion_based_per_MWh = a18.s_gas.CO2e_combustion_based_per_MWh
    s_gas.CO2e_total_2021_estimated = a18.s_gas.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_emethan.CO2e_combustion_based_per_MWh = fact(
        "Fact_T_S_methan_EmFa_tank_wheel_2018"
    )
    s_biomass.CO2e_production_based = 0
    s_biomass.CO2e_combustion_based_per_MWh = (
        a18.s_biomass.CO2e_combustion_based_per_MWh
    )
    s_biomass.CO2e_total_2021_estimated = a18.s_biomass.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_elec.CO2e_production_based = 0
    s_elec.CO2e_combustion_based_per_MWh = a18.s_elec.CO2e_combustion_based_per_MWh
    s_elec.CO2e_total_2021_estimated = a18.s_elec.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_heatpump.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")
    s_heatpump.CO2e_production_based = 0
    s_heatpump.CO2e_combustion_based_per_MWh = (
        a18.s_heatpump.CO2e_combustion_based_per_MWh
    )
    s_heatpump.CO2e_total_2021_estimated = a18.s_heatpump.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    s_heatpump.invest_per_x = fact("Fact_R_S_heatpump_cost")
    s_heatpump.pct_of_wage = fact("Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017")
    s_heatpump.ratio_wage_to_emplo = fact("Fact_B_P_heating_wage_per_person_per_year")
    s_heatpump.emplo_existing = (
        fact("Fact_B_P_install_heating_emplo_2017")
        * entries.m_population_com_2018
        / entries.m_population_nat
        * ass("Ass_B_D_install_heating_emplo_pct_of_A_heatpump")
    )
    s_heatpump.full_load_hour = fact("Fact_B_S_full_usage_hours_buildings")

    p_other_liming_calcit.prod_volume = a18.p_other_liming_calcit.prod_volume * (
        1 + p_other_liming_calcit.demand_change
    )
    p_other_liming_dolomite.prod_volume = a18.p_other_liming_dolomite.prod_volume * (
        1 + p_other_liming_dolomite.demand_change
    )
    p_other_urea.prod_volume = a18.p_other_urea.prod_volume * (
        1 + p_other_urea.demand_change
    )
    p_other_kas.prod_volume = a18.p_other_kas.prod_volume * (
        1 + p_other_kas.demand_change
    )
    p_other_ecrop.prod_volume = a18.p_other_ecrop.prod_volume * (
        1 + p_other_ecrop.demand_change
    )
    p_operation_heat.pct_rehab = (
        fact("Fact_B_P_ratio_renovated_to_not_renovated_2021")
        + p_operation_heat.rate_rehab_pa * entries.m_duration_target
    )
    p_operation_elec_elcon.energy = a18.p_operation_elec_elcon.energy * (
        1 + p_operation_elec_elcon.demand_change
    )
    p_operation_vehicles.energy = a18.p_operation_vehicles.energy * (
        1 + p_operation_vehicles.demand_change
    )
    s_fueloil.change_energy_MWh = s_fueloil.energy - a18.s_fueloil.energy
    s_fueloil.change_energy_pct = div(s_fueloil.change_energy_MWh, a18.s_fueloil.energy)
    s_lpg.change_energy_MWh = s_lpg.energy - a18.s_lpg.energy
    s_lpg.change_energy_pct = div(s_lpg.change_energy_MWh, a18.s_lpg.energy)
    s_gas.change_energy_MWh = s_gas.energy - a18.s_gas.energy
    s_gas.change_energy_pct = div(s_gas.change_energy_MWh, a18.s_gas.energy)
    s_fueloil.CO2e_combustion_based = (
        s_fueloil.energy * s_fueloil.CO2e_combustion_based_per_MWh
    )
    s_lpg.CO2e_combustion_based = s_lpg.energy * s_lpg.CO2e_combustion_based_per_MWh
    s_gas.CO2e_combustion_based = s_gas.energy * s_gas.CO2e_combustion_based_per_MWh
    s_heatpump.power_installed = div(a18.s_heatpump.energy, s_heatpump.full_load_hour)
    p_other_liming_calcit.CO2e_production_based = (
        p_other_liming_calcit.prod_volume
        * p_other_liming_calcit.CO2e_production_based_per_t
    )
    p_other_liming.prod_volume = (
        p_other_liming_calcit.prod_volume + p_other_liming_dolomite.prod_volume
    )
    p_other_liming_dolomite.CO2e_production_based = (
        p_other_liming_dolomite.prod_volume
        * p_other_liming_dolomite.CO2e_production_based_per_t
    )
    p_other_urea.CO2e_production_based = (
        p_other_urea.prod_volume * p_other_urea.CO2e_production_based_per_t
    )
    p_other_kas.CO2e_production_based = (
        p_other_kas.prod_volume * p_other_kas.CO2e_production_based_per_t
    )
    p_other_ecrop.CO2e_production_based = (
        p_other_ecrop.prod_volume * p_other_ecrop.CO2e_production_based_per_t
    )
    p_operation_heat.pct_nonrehab = 1 - p_operation_heat.pct_rehab
    p_operation_heat.area_m2_rehab = (
        p_operation_heat.pct_rehab * a18.p_operation_heat.area_m2
    )
    p_operation_elec_elcon.demand_electricity = p_operation_elec_elcon.energy
    p_operation_elec_elcon.change_energy_MWh = (
        p_operation_elec_elcon.energy - a18.p_operation_elec_elcon.energy
    )
    p_operation_vehicles.demand_epetrol = div(
        p_operation_vehicles.energy * a18.s_petrol.energy,
        a18.s_petrol.energy + a18.s_diesel.energy,
    )
    p_operation_vehicles.demand_ediesel = div(
        p_operation_vehicles.energy * a18.s_diesel.energy,
        a18.s_petrol.energy + a18.s_diesel.energy,
    )
    p_operation_vehicles.change_energy_MWh = (
        p_operation_vehicles.energy - a18.p_operation_vehicles.energy
    )
    s_fueloil.CO2e_total = (
        s_fueloil.CO2e_production_based + s_fueloil.CO2e_combustion_based
    )
    s_lpg.CO2e_total = s_lpg.CO2e_production_based + s_lpg.CO2e_combustion_based
    s_gas.CO2e_total = s_gas.CO2e_production_based + s_gas.CO2e_combustion_based
    g.invest_com = g_consult.invest_com
    g.invest = g_consult.invest + g_organic.invest
    p_fermen.CO2e_production_based = (
        p_fermen_dairycow.CO2e_production_based
        + p_fermen_nondairy.CO2e_production_based
        + p_fermen_swine.CO2e_production_based
        + p_fermen_poultry.CO2e_production_based
        + p_fermen_oanimal.CO2e_production_based
    )
    p_other_liming_calcit.CO2e_total = (
        p_other_liming_calcit.CO2e_production_based
        + p_other_liming_calcit.CO2e_combustion_based
    )
    p_other_liming.CO2e_production_based = (
        p_other_liming_calcit.CO2e_production_based
        + p_other_liming_dolomite.CO2e_production_based
    )
    p_other_liming_dolomite.CO2e_total = (
        p_other_liming_dolomite.CO2e_production_based
        + p_other_liming_dolomite.CO2e_combustion_based
    )
    p_other_urea.CO2e_total = (
        p_other_urea.CO2e_production_based + p_other_urea.CO2e_combustion_based
    )
    p_other_kas.CO2e_total = (
        p_other_kas.CO2e_production_based + p_other_kas.CO2e_combustion_based
    )
    p_other_ecrop.CO2e_total = (
        p_other_ecrop.CO2e_production_based + p_other_ecrop.CO2e_combustion_based
    )
    p_operation_heat.area_m2_nonrehab = (
        p_operation_heat.pct_nonrehab * a18.p_operation_heat.area_m2
    )
    p_operation_heat.demand_heat_rehab = p_operation_heat.area_m2_rehab * ass(
        "Ass_B_D_ratio_fec_to_area_2050"
    )
    p_operation_heat.invest = (
        p_operation_heat.area_m2_rehab
        * (1 - fact("Fact_B_P_ratio_renovated_to_not_renovated_2021"))
        * p_operation_heat.invest_per_x
    )

    p_operation_elec_elcon.change_energy_pct = div(
        p_operation_elec_elcon.change_energy_MWh, a18.p_operation_elec_elcon.energy
    )
    p_operation.demand_epetrol = p_operation_vehicles.demand_epetrol
    s_petrol.energy = p_operation_vehicles.demand_epetrol
    p_operation.demand_ediesel = p_operation_vehicles.demand_ediesel
    s_diesel.energy = p_operation_vehicles.demand_ediesel
    p_operation_vehicles.change_energy_pct = div(
        p_operation_vehicles.change_energy_MWh, a18.p_operation_vehicles.energy
    )
    s_fueloil.change_CO2e_t = s_fueloil.CO2e_total - a18.s_fueloil.CO2e_total
    s_fueloil.cost_climate_saved = (
        (s_fueloil.CO2e_total_2021_estimated - s_fueloil.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s_lpg.change_CO2e_t = s_lpg.CO2e_total - a18.s_lpg.CO2e_total
    s_lpg.cost_climate_saved = (
        (s_lpg.CO2e_total_2021_estimated - s_lpg.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s_gas.change_CO2e_t = s_gas.CO2e_total - a18.s_gas.CO2e_total
    s_gas.cost_climate_saved = (
        (s_gas.CO2e_total_2021_estimated - s_gas.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g.invest_pa_com = g_consult.invest_pa_com

    g.invest_pa = g_consult.invest_pa + g_organic.invest_pa

    p_fermen.CO2e_total = (
        p_fermen.CO2e_production_based + p_fermen.CO2e_combustion_based
    )
    p_manure.CO2e_production_based = (
        p_manure_dairycow.CO2e_production_based
        + p_manure_nondairy.CO2e_production_based
        + p_manure_swine.CO2e_production_based
        + p_manure_poultry.CO2e_production_based
        + p_manure_oanimal.CO2e_production_based
        + p_manure_deposition.CO2e_production_based
    )
    p_soil.CO2e_production_based = (
        p_soil_fertilizer.CO2e_production_based
        + p_soil_manure.CO2e_production_based
        + p_soil_sludge.CO2e_production_based
        + p_soil_ecrop.CO2e_production_based
        + p_soil_grazing.CO2e_production_based
        + p_soil_residue.CO2e_production_based
        + p_soil_orgfarm.CO2e_production_based
        + p_soil_orgloss.CO2e_production_based
        + p_soil_leaching.CO2e_production_based
        + p_soil_deposition.CO2e_production_based
    )
    p_other_liming_calcit.change_CO2e_t = (
        p_other_liming_calcit.CO2e_total - a18.p_other_liming_calcit.CO2e_total
    )
    p_other_liming_calcit.cost_climate_saved = (
        (
            p_other_liming_calcit.CO2e_total_2021_estimated
            - p_other_liming_calcit.CO2e_total
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other.CO2e_production_based = (
        p_other_liming.CO2e_production_based
        + p_other_urea.CO2e_production_based
        + p_other_kas.CO2e_production_based
        + p_other_ecrop.CO2e_production_based
    )
    p_other_liming.CO2e_total = (
        p_other_liming.CO2e_production_based + p_other_liming.CO2e_combustion_based
    )
    p_other_liming_dolomite.change_CO2e_t = (
        p_other_liming_dolomite.CO2e_total - a18.p_other_liming_dolomite.CO2e_total
    )
    p_other_liming_dolomite.cost_climate_saved = (
        (
            p_other_liming_dolomite.CO2e_total_2021_estimated
            - p_other_liming_dolomite.CO2e_total
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other_urea.change_CO2e_t = p_other_urea.CO2e_total - a18.p_other_urea.CO2e_total
    p_other_urea.cost_climate_saved = (
        (p_other_urea.CO2e_total_2021_estimated - p_other_urea.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other_kas.change_CO2e_t = p_other_kas.CO2e_total - a18.p_other_kas.CO2e_total
    p_other_kas.cost_climate_saved = (
        (p_other_kas.CO2e_total_2021_estimated - p_other_kas.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other_ecrop.change_CO2e_t = (
        p_other_ecrop.CO2e_total - a18.p_other_ecrop.CO2e_total
    )
    p_other_ecrop.cost_climate_saved = (
        (p_other_ecrop.CO2e_total_2021_estimated - p_other_ecrop.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_operation_heat.demand_heat_nonrehab = (
        p_operation_heat.area_m2_nonrehab
        * (
            a18.p_operation_heat.factor_adapted_to_fec
            - fact("Fact_B_P_ratio_renovated_to_not_renovated_2021")
            * ass("Ass_B_D_ratio_fec_to_area_2050")
        )
        / (1 - fact("Fact_B_P_ratio_renovated_to_not_renovated_2021"))
    )
    p_operation_heat.demand_heatpump = p_operation_heat.demand_heat_rehab
    p_operation_heat.invest_pa = p_operation_heat.invest / entries.m_duration_target
    p_operation_heat.cost_wage = (
        p_operation_heat.invest
        / entries.m_duration_target
        * p_operation_heat.pct_of_wage
    )
    s_petrol.CO2e_combustion_based = (
        s_petrol.energy * s_petrol.CO2e_combustion_based_per_MWh
    )
    s_petrol.change_energy_MWh = s_petrol.energy - a18.s_petrol.energy
    s_diesel.CO2e_combustion_based = (
        s_diesel.energy * s_diesel.CO2e_combustion_based_per_MWh
    )
    s_diesel.change_energy_MWh = s_diesel.energy - a18.s_diesel.energy
    s_fueloil.change_CO2e_pct = div(s_fueloil.change_CO2e_t, a18.s_fueloil.CO2e_total)
    s_lpg.change_CO2e_pct = div(s_lpg.change_CO2e_t, a18.s_lpg.CO2e_total)
    s_gas.change_CO2e_pct = div(s_gas.change_CO2e_t, a18.s_gas.CO2e_total)

    p_fermen.change_CO2e_t = p_fermen.CO2e_total - a18.p_fermen.CO2e_total
    p_fermen.cost_climate_saved = (
        (p_fermen.CO2e_total_2021_estimated - p_fermen.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_manure.CO2e_total = (
        p_manure.CO2e_production_based + p_manure.CO2e_combustion_based
    )
    p_soil.CO2e_total = p_soil.CO2e_production_based + p_soil.CO2e_combustion_based
    p_other_liming_calcit.change_CO2e_pct = div(
        p_other_liming_calcit.change_CO2e_t, a18.p_other_liming_calcit.CO2e_total
    )
    p.CO2e_production_based = (
        p_fermen.CO2e_production_based
        + p_manure.CO2e_production_based
        + p_soil.CO2e_production_based
        + p_other.CO2e_production_based
    )
    p_other.CO2e_total = p_other.CO2e_production_based + p_other.CO2e_combustion_based
    p_other_liming.change_CO2e_t = (
        p_other_liming.CO2e_total - a18.p_other_liming.CO2e_total
    )
    p_other_liming.cost_climate_saved = (
        (p_other_liming.CO2e_total_2021_estimated - p_other_liming.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other_liming_dolomite.change_CO2e_pct = div(
        p_other_liming_dolomite.change_CO2e_t, a18.p_other_liming_dolomite.CO2e_total
    )

    p_other_urea.change_CO2e_pct = div(
        p_other_urea.change_CO2e_t, a18.p_other_urea.CO2e_total
    )

    p_other_kas.change_CO2e_pct = div(
        p_other_kas.change_CO2e_t, a18.p_other_kas.CO2e_total
    )

    p_other_ecrop.change_CO2e_pct = div(
        p_other_ecrop.change_CO2e_t, a18.p_other_ecrop.CO2e_total
    )
    p_operation_heat.energy = (
        p_operation_heat.demand_heat_nonrehab + p_operation_heat.demand_heat_rehab
    )
    p_operation.demand_heatpump = p_operation_heat.demand_heatpump
    p_operation_heat.demand_emplo = div(
        p_operation_heat.cost_wage, p_operation_heat.ratio_wage_to_emplo
    )
    s_petrol.CO2e_total = (
        s_petrol.CO2e_production_based + s_petrol.CO2e_combustion_based
    )
    s_petrol.change_energy_pct = div(s_petrol.change_energy_MWh, a18.s_petrol.energy)
    s_diesel.CO2e_total = (
        s_diesel.CO2e_production_based + s_diesel.CO2e_combustion_based
    )
    s_diesel.change_energy_pct = div(s_diesel.change_energy_MWh, a18.s_diesel.energy)
    g.demand_emplo = g_consult.demand_emplo + g_organic.demand_emplo

    p_fermen.change_CO2e_pct = div(p_fermen.change_CO2e_t, a18.p_fermen.CO2e_total)

    p_manure.change_CO2e_t = p_manure.CO2e_total - a18.p_manure.CO2e_total
    p_manure.cost_climate_saved = (
        (p_manure.CO2e_total_2021_estimated - p_manure.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_soil.change_CO2e_t = p_soil.CO2e_total - a18.p_soil.CO2e_total
    p_soil.cost_climate_saved = (
        (p_soil.CO2e_total_2021_estimated - p_soil.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    a.CO2e_production_based = p.CO2e_production_based
    p.CO2e_total = (
        p_fermen.CO2e_total
        + p_manure.CO2e_total
        + p_soil.CO2e_total
        + p_other.CO2e_total
    )
    p_other.change_CO2e_t = p_other.CO2e_total - a18.p_other.CO2e_total
    p_other.cost_climate_saved = (
        (p_other.CO2e_total_2021_estimated - p_other.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other_liming.change_CO2e_pct = div(
        p_other_liming.change_CO2e_t, a18.p_other_liming.CO2e_total
    )
    p_operation_heat.fec_factor_averaged = div(
        p_operation_heat.energy, a18.p_operation_heat.area_m2
    )
    p_operation_heat.change_energy_MWh = (
        p_operation_heat.energy - a18.p_operation_heat.energy
    )
    s_heatpump.energy = 0
    s_heatpump.energy = p_operation.demand_heatpump
    p_operation.demand_emplo = p_operation_heat.demand_emplo
    p_operation_heat.demand_emplo_new = max(
        0, p_operation_heat.demand_emplo - p_operation_heat.emplo_existing
    )
    s_petrol.change_CO2e_t = s_petrol.CO2e_total - a18.s_petrol.CO2e_total
    s_petrol.cost_climate_saved = (
        (s_petrol.CO2e_total_2021_estimated - s_petrol.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s_diesel.change_CO2e_t = s_diesel.CO2e_total - a18.s_diesel.CO2e_total
    s_diesel.cost_climate_saved = (
        (s_diesel.CO2e_total_2021_estimated - s_diesel.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g.demand_emplo_new = g_consult.demand_emplo_new + g_organic.demand_emplo_new
    p_manure.change_CO2e_pct = div(p_manure.change_CO2e_t, a18.p_manure.CO2e_total)
    p_soil.change_CO2e_pct = div(p_soil.change_CO2e_t, a18.p_soil.CO2e_total)
    p.change_CO2e_t = p.CO2e_total - a18.p.CO2e_total
    p.cost_climate_saved = (
        (p.CO2e_total_2021_estimated - p.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_other.change_CO2e_pct = div(p_other.change_CO2e_t, a18.p_other.CO2e_total)
    p_operation_heat.change_energy_pct = div(
        p_operation_heat.change_energy_MWh, a18.p_operation_heat.energy
    )
    p_operation_heat.demand_biomass = min(
        a18.s_biomass.energy, p_operation_heat.energy - s_heatpump.energy
    )
    p_operation_elec_heatpump.energy = s_heatpump.energy / fact(
        "Fact_R_S_heatpump_mean_annual_performance_factor_all"
    )
    s_heatpump.cost_fuel = 0
    s_heatpump.cost_fuel = s_heatpump.energy * s_heatpump.cost_fuel_per_MWh / MILLION
    s_heatpump.CO2e_combustion_based = (
        s_heatpump.energy * s_heatpump.CO2e_combustion_based_per_MWh
    )
    s_heatpump.change_energy_MWh = s_heatpump.energy - a18.s_heatpump.energy
    s_heatpump.power_to_be_installed = max(
        div(s_heatpump.energy, s_heatpump.full_load_hour) - s_heatpump.power_installed,
        0,
    )
    p.demand_emplo = p_operation.demand_emplo
    p_operation.demand_emplo_new = p_operation_heat.demand_emplo_new
    s_petrol.change_CO2e_pct = div(s_petrol.change_CO2e_t, a18.s_petrol.CO2e_total)
    s_diesel.change_CO2e_pct = div(s_diesel.change_CO2e_t, a18.s_diesel.CO2e_total)
    p.change_CO2e_pct = div(p.change_CO2e_t, a18.p.CO2e_total)
    p_operation.demand_biomass = p_operation_heat.demand_biomass
    p_operation.energy = (
        p_operation_heat.energy
        + p_operation_elec_elcon.energy
        + p_operation_elec_heatpump.energy
        + p_operation_vehicles.energy
    )
    p_operation_elec_heatpump.demand_electricity = p_operation_elec_heatpump.energy
    p_operation_elec_heatpump.change_energy_MWh = (
        p_operation_elec_heatpump.energy - a18.p_operation_elec_heatpump.energy
    )

    s_heatpump.CO2e_total = (
        s_heatpump.CO2e_production_based + s_heatpump.CO2e_combustion_based
    )
    s_heatpump.invest = (
        s_heatpump.invest_per_x * s_heatpump.power_to_be_installed * 1000
    )

    p_operation.invest = p_operation_heat.invest
    p_operation.invest_pa = p_operation.invest / entries.m_duration_target

    p.invest = p_operation.invest
    p.invest_pa = p.invest / entries.m_duration_target

    s.invest = s_heatpump.invest
    s.invest_pa = s.invest / entries.m_duration_target

    a.invest_com = g.invest_com
    a.invest = g.invest + s.invest + p.invest

    a.invest_pa_com = g.invest_pa_com
    a.invest_pa = a.invest / entries.m_duration_target

    p.demand_emplo_new = p_operation.demand_emplo_new
    s_biomass.energy = p_operation.demand_biomass
    p.energy = p_operation.energy
    p_operation.change_energy_MWh = p_operation.energy - a18.p_operation.energy
    p_operation.demand_electricity = (
        p_operation_elec_elcon.demand_electricity
        + p_operation_elec_heatpump.demand_electricity
    )
    s_heatpump.change_CO2e_t = s_heatpump.CO2e_total - a18.s_heatpump.CO2e_total
    s_heatpump.cost_climate_saved = (
        (s_heatpump.CO2e_total_2021_estimated - s_heatpump.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s_heatpump.invest_pa = s_heatpump.invest / entries.m_duration_target
    p_operation_heat.demand_emethan = (
        p_operation_heat.energy - s_biomass.energy - s_heatpump.energy
    )
    s_emethan.energy = p_operation_heat.energy - s_biomass.energy - s_heatpump.energy
    s_emethan.change_energy_MWh = s_emethan.energy
    s_biomass.CO2e_combustion_based = (
        s_biomass.energy * s_biomass.CO2e_combustion_based_per_MWh
    )
    s_biomass.change_energy_MWh = s_biomass.energy - a18.s_biomass.energy
    a.change_energy_MWh = p_operation.change_energy_MWh
    p_operation.change_energy_pct = div(
        p_operation.change_energy_MWh, a18.p_operation.energy
    )
    s_elec.energy = p_operation.demand_electricity
    s_heatpump.change_CO2e_pct = div(
        s_heatpump.change_CO2e_t, 1.0
    )  # a18.s_heatpump.CO2e_total)
    s_heatpump.cost_wage = s_heatpump.invest_pa * s_heatpump.pct_of_wage
    p_operation.demand_emethan = p_operation_heat.demand_emethan
    s_emethan.demand_emethan = s_emethan.energy
    s_biomass.CO2e_total = (
        s_biomass.CO2e_production_based + s_biomass.CO2e_combustion_based
    )
    s_biomass.change_energy_pct = div(s_biomass.change_energy_MWh, a18.s_biomass.energy)
    a.change_energy_pct = p_operation.change_energy_pct
    s.energy = (
        s_petrol.energy
        + s_diesel.energy
        + s_fueloil.energy
        + s_lpg.energy
        + s_gas.energy
        + s_emethan.energy
        + s_biomass.energy
        + s_elec.energy
        + s_heatpump.energy
    )
    s_elec.CO2e_combustion_based = s_elec.energy * s_elec.CO2e_combustion_based_per_MWh
    s_elec.change_energy_MWh = s_elec.energy - a18.s_elec.energy
    s_heatpump.demand_emplo = div(s_heatpump.cost_wage, s_heatpump.ratio_wage_to_emplo)
    s_biomass.change_CO2e_t = s_biomass.CO2e_total - a18.s_biomass.CO2e_total
    s_biomass.cost_climate_saved = (
        (s_biomass.CO2e_total_2021_estimated - s_biomass.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s.change_energy_MWh = s.energy - a18.s.energy
    s_petrol.pct_energy = div(s_petrol.energy, s.energy)
    s_diesel.pct_energy = div(s_diesel.energy, s.energy)
    s_fueloil.pct_energy = div(s_fueloil.energy, s.energy)
    s_lpg.pct_energy = div(s_lpg.energy, s.energy)
    s_gas.pct_energy = div(s_gas.energy, s.energy)
    s_emethan.pct_energy = div(s_gas.energy, s.energy)
    s_biomass.pct_energy = div(s_biomass.energy, s.energy)
    s_elec.pct_energy = div(s_elec.energy, s.energy)
    s_heatpump.pct_energy = div(s_heatpump.energy, s.energy)
    s.CO2e_combustion_based = (
        s_petrol.CO2e_combustion_based
        + s_diesel.CO2e_combustion_based
        + s_fueloil.CO2e_combustion_based
        + s_lpg.CO2e_combustion_based
        + s_gas.CO2e_combustion_based
        + s_emethan.CO2e_combustion_based
        + s_biomass.CO2e_combustion_based
        + s_elec.CO2e_combustion_based
        + s_heatpump.CO2e_combustion_based
    )
    s_elec.CO2e_total = s_elec.CO2e_production_based + s_elec.CO2e_combustion_based
    s_elec.change_energy_pct = div(s_elec.change_energy_MWh, a18.s_elec.energy)
    s.demand_emplo = s_heatpump.demand_emplo
    s_heatpump.demand_emplo_new = max(
        0, s_heatpump.demand_emplo - s_heatpump.emplo_existing
    )
    s_biomass.change_CO2e_pct = div(s_biomass.change_CO2e_t, a18.s_biomass.CO2e_total)
    s.change_energy_pct = div(s.change_energy_MWh, a18.s.energy)
    s.pct_energy = (
        s_petrol.pct_energy
        + s_diesel.pct_energy
        + s_fueloil.pct_energy
        + s_lpg.pct_energy
        + s_gas.pct_energy
        + s_emethan.pct_energy
        + s_biomass.pct_energy
        + s_elec.pct_energy
        + s_heatpump.pct_energy
    )
    a.CO2e_combustion_based = s.CO2e_combustion_based
    s.CO2e_total = s.CO2e_production_based + s.CO2e_combustion_based
    s_elec.change_CO2e_t = s_elec.CO2e_total - a18.s_elec.CO2e_total
    s_elec.cost_climate_saved = (
        (s_elec.CO2e_total_2021_estimated - s_elec.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    a.demand_emplo = g.demand_emplo + p.demand_emplo + s.demand_emplo
    s.demand_emplo_new = s_heatpump.demand_emplo_new
    a.CO2e_total = g.CO2e_total + p.CO2e_total + s.CO2e_total
    s.change_CO2e_t = s.CO2e_total - a18.s.CO2e_total
    s.cost_climate_saved = (
        (s.CO2e_total_2021_estimated - s.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    s_elec.change_CO2e_pct = div(s_elec.change_CO2e_t, a18.s_elec.CO2e_total)

    a.demand_emplo_new = g.demand_emplo_new + p.demand_emplo_new + s.demand_emplo_new
    a.change_CO2e_t = a.CO2e_total - a18.a.CO2e_total
    a.cost_climate_saved = (
        (a.CO2e_total_2021_estimated - a.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    s.change_CO2e_pct = div(s.change_CO2e_t, a18.s.CO2e_total)
    a.change_CO2e_pct = div(a.change_CO2e_t, a18.a.CO2e_total)

    g.demand_emplo_com = g_consult.demand_emplo_com
    a.demand_emplo_com = g.demand_emplo_com

    p_operation_heat.cost_wage = (
        div(p_operation_heat.invest, entries.m_duration_target)
        * p_operation_heat.pct_of_wage
    )
    p_operation.cost_wage = p_operation_heat.cost_wage
    p.cost_wage = p_operation.cost_wage

    s_heatpump.cost_wage = s_heatpump.invest_pa * s_heatpump.pct_of_wage
    s.cost_wage = s_heatpump.cost_wage

    g.cost_wage = g_consult.cost_wage + g_organic.cost_wage
    a.cost_wage = g.cost_wage + p.cost_wage + s.cost_wage

    return a30
