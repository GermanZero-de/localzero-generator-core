from .inputs import Inputs
from dataclasses import dataclass, asdict


@dataclass
class AColVars2030:
    area_m2: float = -1
    CO2e_cb: float = -1
    CO2e_cb_per_MWh: float = -1
    CO2e_pb: float = -1
    CO2e_pb_per_t: float = -1
    CO2e_total: float = -1
    energy: float = -1
    demand_ediesel: float = -1
    demand_heatpump: float = -1
    demand_biomass: float = -1
    demand_epetrol: float = -1
    demand_electricity: float = -1
    demand_emethan: float = -1
    factor_adapted_to_fec: float = -1
    pct_energy: float = -1
    prod_volume: float = -1
    change_energy_MWh: float = -1
    change_energy_pct: float = -1
    change_CO2e_t: float = -1
    change_CO2e_pct: float = -1
    CO2e_total_2021_estimated: float = -1
    cost_climate_saved: float = -1
    invest_pa: float = -1
    invest_pa_com: float = -1
    invest_pa_outside: float = -1
    invest: float = -1
    invest_com: float = -1
    invest_outside: float = -1
    invest_per_x: float = -1
    area_ha_available: float = -1
    demand_change: float = -1
    action: float = -1
    area_ha_change: float = -1
    area_ha: float = -1
    pct_nonrehab: float = -1
    pct_rehab: float = -1
    area_m2_nonrehab: float = -1
    area_m2_rehab: float = -1
    demand_heat_nonrehab: float = -1
    demand_heat_rehab: float = -1
    rate_rehab_pa: float = -1
    fec_factor_averaged: float = -1
    pct_of_wage: float = -1
    cost_wage: float = -1
    ratio_wage_to_emplo: float = -1
    demand_emplo: float = -1
    emplo_existing: float = -1
    demand_emplo_new: float = -1
    cost_fuel: float = -1
    cost_fuel_per_MWh: float = -1
    power_to_be_installed: float = -1
    power_installed: float = -1
    full_load_hour: float = -1
    power_to_be_installed_pct: float = -1
    pet_sites: float = -1


@dataclass
class A30:
    # Klassenvariablen für A18
    a: AColVars2030 = AColVars2030()
    p: AColVars2030 = AColVars2030()
    g: AColVars2030 = AColVars2030()
    g_consult: AColVars2030 = AColVars2030()
    g_organic: AColVars2030 = AColVars2030()
    g_conversion: AColVars2030 = AColVars2030()
    p_fermen: AColVars2030 = AColVars2030()
    p_fermen_dairycow: AColVars2030 = AColVars2030()
    p_fermen_nondairy: AColVars2030 = AColVars2030()
    p_fermen_swine: AColVars2030 = AColVars2030()
    p_fermen_poultry: AColVars2030 = AColVars2030()
    p_fermen_oanimal: AColVars2030 = AColVars2030()
    p_manure: AColVars2030 = AColVars2030()
    p_manure_dairycow: AColVars2030 = AColVars2030()
    p_manure_nondairy: AColVars2030 = AColVars2030()
    p_manure_swine: AColVars2030 = AColVars2030()
    p_manure_poultry: AColVars2030 = AColVars2030()
    p_manure_oanimal: AColVars2030 = AColVars2030()
    p_manure_deposition: AColVars2030 = AColVars2030()
    p_soil: AColVars2030 = AColVars2030()
    p_soil_fertilizer: AColVars2030 = AColVars2030()
    p_soil_manure: AColVars2030 = AColVars2030()
    p_soil_sludge: AColVars2030 = AColVars2030()
    p_soil_ecrop: AColVars2030 = AColVars2030()
    p_soil_grazing: AColVars2030 = AColVars2030()
    p_soil_residue: AColVars2030 = AColVars2030()
    p_soil_orgfarm: AColVars2030 = AColVars2030()
    p_soil_orgloss: AColVars2030 = AColVars2030()
    p_soil_leaching: AColVars2030 = AColVars2030()
    p_soil_deposition: AColVars2030 = AColVars2030()
    p_other: AColVars2030 = AColVars2030()
    p_elec_heatpump: AColVars2030 = AColVars2030()
    p_other_liming: AColVars2030 = AColVars2030()
    p_other_liming_calcit: AColVars2030 = AColVars2030()
    p_other_liming_dolomite: AColVars2030 = AColVars2030()
    p_other_urea: AColVars2030 = AColVars2030()
    p_other_kas: AColVars2030 = AColVars2030()
    p_other_ecrop: AColVars2030 = AColVars2030()
    p_other_energy: AColVars2030 = AColVars2030()
    p_operation: AColVars2030 = AColVars2030()
    p_operation_heat: AColVars2030 = AColVars2030()
    p_operation_elec_elcon: AColVars2030 = AColVars2030()
    p_operation_elec_heatpump: AColVars2030 = AColVars2030()
    p_operation_vehicles: AColVars2030 = AColVars2030()
    p_operation: AColVars2030 = AColVars2030()
    p_operation_heat: AColVars2030 = AColVars2030()
    s: AColVars2030 = AColVars2030()
    s_petrol: AColVars2030 = AColVars2030()
    s_diesel: AColVars2030 = AColVars2030()
    s_fueloil: AColVars2030 = AColVars2030()
    s_lpg: AColVars2030 = AColVars2030()
    s_gas: AColVars2030 = AColVars2030()
    s_biomass: AColVars2030 = AColVars2030()
    s_elec: AColVars2030 = AColVars2030()
    s_heatpump: AColVars2030 = AColVars2030()
    s_emethan: AColVars2030 = AColVars2030()

    # erzeuge dictionry

    def dict(self):
        return asdict(self)


def calc(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    Million = 1000000

    a30 = root.a30
    a18 = root.a18
    l30 = root.l30

    a = root.a30.a
    g = root.a30.g
    g_consult = root.a30.g_consult
    g_conversion = root.a30.g_conversion
    g_organic = root.a30.g_organic
    p = root.a30.p
    p_fermen = root.a30.p_fermen
    p_fermen_dairycow = root.a30.p_fermen_dairycow
    p_fermen_nondairy = root.a30.p_fermen_nondairy
    p_fermen_swine = root.a30.p_fermen_swine
    p_fermen_poultry = root.a30.p_fermen_poultry
    p_fermen_oanimal = root.a30.p_fermen_oanimal
    p_manure = root.a30.p_manure
    p_manure_dairycow = root.a30.p_manure_dairycow
    p_manure_nondairy = root.a30.p_manure_nondairy
    p_manure_swine = root.a30.p_manure_swine
    p_manure_poultry = root.a30.p_manure_poultry
    p_manure_oanimal = root.a30.p_manure_oanimal
    p_manure_deposition = root.a30.p_manure_deposition
    p_soil = root.a30.p_soil
    p_soil_fertilizer = root.a30.p_soil_fertilizer
    p_soil_manure = root.a30.p_soil_manure
    p_soil_sludge = root.a30.p_soil_sludge
    p_soil_ecrop = root.a30.p_soil_ecrop
    p_soil_grazing = root.a30.p_soil_grazing
    p_soil_residue = root.a30.p_soil_residue
    p_soil_orgfarm = root.a30.p_soil_orgfarm
    p_soil_orgloss = root.a30.p_soil_orgloss
    p_soil_leaching = root.a30.p_soil_leaching
    p_soil_deposition = root.a30.p_soil_deposition
    p_other = root.a30.p_other
    p_elec_heatpump = root.a30.p_elec_heatpump
    p_other_liming = root.a30.p_other_liming
    p_other_liming_calcit = root.a30.p_other_liming_calcit
    p_other_liming_dolomite = root.a30.p_other_liming_dolomite
    p_other_urea = root.a30.p_other_urea
    p_other_kas = root.a30.p_other_kas
    p_other_ecrop = root.a30.p_other_ecrop
    p_other_energy = root.a30.p_other_energy
    p_operation = root.a30.p_operation
    p_operation_heat = root.a30.p_operation_heat
    p_operation_elec_elcon = root.a30.p_operation_elec_elcon
    p_operation_vehicles = root.a30.p_operation_vehicles
    p_operation_elec_heatpump = root.a30.p_operation_elec_heatpump
    s = root.a30.s
    s_petrol = root.a30.s_petrol
    s_diesel = root.a30.s_diesel
    s_fueloil = root.a30.s_fueloil
    s_lpg = root.a30.s_lpg
    s_gas = root.a30.s_gas
    s_biomass = root.a30.s_biomass
    s_elec = root.a30.s_elec
    s_heatpump = root.a30.s_heatpump
    s_emethan = root.a30.s_emethan

    g.CO2e_total = 0
    p_other_energy.CO2e_total = 0
    p_fermen.CO2e_cb = 0
    p_fermen_dairycow.CO2e_cb = 0
    p_fermen_nondairy.CO2e_cb = 0
    p_fermen_swine.CO2e_cb = 0
    p_fermen_poultry.CO2e_cb = 0
    p_fermen_oanimal.CO2e_cb = 0
    p_manure.CO2e_cb = 0
    p_manure_dairycow.CO2e_cb = 0
    p_manure_nondairy.CO2e_cb = 0
    p_manure_swine.CO2e_cb = 0
    p_manure_poultry.CO2e_cb = 0
    p_manure_oanimal.CO2e_cb = 0
    p_manure_deposition.CO2e_cb = 0
    p_soil.CO2e_cb = 0
    p_soil_fertilizer.CO2e_cb = 0
    p_soil_manure.CO2e_cb = 0
    p_soil_sludge.CO2e_cb = 0
    p_soil_ecrop.CO2e_cb = 0
    p_soil_grazing.CO2e_cb = 0
    p_soil_residue.CO2e_cb = 0
    p_soil_orgfarm.CO2e_cb = 0
    p_soil_orgloss.CO2e_cb = 0
    p_soil_leaching.CO2e_cb = 0
    p_soil_deposition.CO2e_cb = 0
    p_other.CO2e_cb = 0
    p_other_liming.CO2e_cb = 0
    p_other_liming_calcit.CO2e_cb = 0
    p_other_liming_dolomite.CO2e_cb = 0
    p_other_urea.CO2e_cb = 0
    p_other_kas.CO2e_cb = 0
    p_other_ecrop.CO2e_cb = 0
    s.CO2e_pb = 0
    s_petrol.CO2e_pb = 0
    s_diesel.CO2e_pb = 0
    s_fueloil.area_m2 = 0
    s_fueloil.CO2e_pb = 0
    s_lpg.energy = 0
    s_lpg.CO2e_pb = 0
    s_gas.area_m2 = 0
    s_gas.CO2e_pb = 0
    s_biomass.CO2e_pb = 0
    s_elec.CO2e_pb = 0
    s_heatpump.CO2e_pb = 0
    s_heatpump.energy = 0
    s_heatpump.cost_fuel = 0
    p_operation_elec_elcon.demand_heatpump = (
        p_elec_heatpump.demand_heatpump
    ) = p_operation_vehicles.demand_heatpump = 0
    p_operation_elec_elcon.demand_biomass = (
        p_elec_heatpump.demand_biomass
    ) = p_operation_vehicles.demand_biomass = 0
    p_operation_heat.demand_ediesel = (
        p_operation_elec_elcon.demand_ediesel
    ) = p_elec_heatpump.demand_ediesel = 0
    p_operation_heat.demand_epetrol = (
        p_operation_elec_elcon.demand_epetrol
    ) = p_elec_heatpump.demand_epetrol = 0
    p_operation_heat.demand_electricity = p_operation_vehicles.demand_electricity = 0
    p_operation_elec_elcon.demand_emethan = (
        p_elec_heatpump.demand_emethan
    ) = p_operation_vehicles.demand_emethan = 0
    s_emethan.CO2e_cb = 0

    a30_dict = {}
    for i in range(20):
        if a30_dict == a30.dict():
            break
        a30_dict = a30.dict()
        p_operation_vehicles.demand_change = ass("Ass_B_D_fec_vehicles_change")
        p_fermen_dairycow.CO2e_pb_per_t = a18.p_fermen_dairycow.CO2e_pb_per_t
        g_consult.invest_per_x = ass("Ass_A_G_consult_invest_per_farm")
        g_consult.area_ha_available = entry("In_A_farm_amount")
        g_consult.invest = g_consult.area_ha_available * g_consult.invest_per_x
        g_consult.invest_com = g_consult.invest * ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )
        g_consult.pct_of_wage = ass("Ass_A_G_consult_invest_pct_of_wage")
        g_consult.invest_pa = g_consult.invest / entry("In_M_duration_target")
        g_consult.ratio_wage_to_emplo = ass("Ass_A_G_consult_ratio_wage_to_emplo")
        g_consult.cost_wage = g_consult.invest_pa * g_consult.pct_of_wage
        g_consult.demand_emplo = g_consult.cost_wage / g_consult.ratio_wage_to_emplo
        g_consult.invest_pa_com = g_consult.invest_pa * ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )
        g_conversion.invest_per_x = ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
        g_conversion.power_installed = entry("In_A_area_agri_com_pct_of_organic")
        g_conversion.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        g_conversion.power_to_be_installed_pct = ass(
            "Ass_A_G_area_agri_pct_of_organic_2050"
        )
        g_conversion.ratio_wage_to_emplo = fact(
            "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
        )
        g_conversion.area_ha_available = entry("In_M_area_agri_com")
        g_conversion.power_to_be_installed = g_conversion.area_ha_available * (
            g_conversion.power_to_be_installed_pct - g_conversion.power_installed
        )
        g_conversion.invest = (
            g_conversion.power_to_be_installed * g_conversion.invest_per_x
        )
        g_conversion.invest_pa = g_conversion.invest / entry("In_M_duration_target")
        g_conversion.cost_wage = g_conversion.invest_pa * g_conversion.pct_of_wage
        g_conversion.demand_emplo = (
            g_conversion.cost_wage / g_conversion.ratio_wage_to_emplo
        )
        g_organic.demand_emplo_new = g_organic.demand_emplo
        g_consult.demand_emplo_new = g_consult.demand_emplo
        g.demand_emplo_new = g_consult.demand_emplo_new + g_organic.demand_emplo_new
        g.demand_emplo = g_consult.demand_emplo + g_organic.demand_emplo
        s_petrol.CO2e_cb_per_MWh = a18.s_petrol.CO2e_cb_per_MWh
        p_fermen_dairycow.pet_sites = a18.p_fermen_dairycow.amount * (
            1 + p_fermen_dairycow.demand_change
        )
        p_fermen_dairycow.CO2e_pb = (
            p_fermen_dairycow.pet_sites * p_fermen_dairycow.CO2e_pb_per_t
        )
        p.CO2e_total_2021_estimated = a18.p.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_fermen_nondairy.pet_sites = a18.p_fermen_nondairy.amount * (
            1 + p_fermen_nondairy.demand_change
        )
        p_fermen_nondairy.CO2e_pb_per_t = a18.p_fermen_nondairy.CO2e_pb_per_t
        p_manure_dairycow.demand_change = ass(
            "Ass_A_P_manure_ratio_CO2e_to_amount_change"
        )
        p_fermen_nondairy.CO2e_pb = (
            p_fermen_nondairy.pet_sites * p_fermen_nondairy.CO2e_pb_per_t
        )
        p_fermen_swine.pet_sites = a18.p_fermen_swine.amount * (
            1 + p_fermen_swine.demand_change
        )
        p_fermen.CO2e_total_2021_estimated = a18.p_fermen.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_fermen_swine.CO2e_pb_per_t = a18.p_fermen_swine.CO2e_pb_per_t
        p_fermen_dairycow.demand_change = ass("Ass_A_P_fermen_dairycow_change")
        p_fermen_swine.CO2e_pb = p_fermen_swine.pet_sites * p_fermen_swine.CO2e_pb_per_t
        p_fermen_poultry.pet_sites = a18.p_fermen_poultry.amount * (
            1 + p_fermen_poultry.demand_change
        )
        p_fermen_poultry.CO2e_pb_per_t = a18.p_fermen_poultry.CO2e_pb_per_t
        p_fermen_dairycow.CO2e_total = (
            p_fermen_dairycow.CO2e_pb + p_fermen_dairycow.CO2e_cb
        )
        p_fermen_dairycow.change_CO2e_t = (
            p_fermen_dairycow.CO2e_total - a18.p_fermen_dairycow.CO2e_total
        )
        p_fermen_dairycow.change_CO2e_pct = (
            p_fermen_dairycow.change_CO2e_t / a18.p_fermen_dairycow.CO2e_total
        )
        p_fermen_dairycow.CO2e_total_2021_estimated = (
            a18.p_fermen_dairycow.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fermen_dairycow.cost_climate_saved = (
            (p_fermen_dairycow.CO2e_total_2021_estimated - p_fermen_dairycow.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fermen_nondairy.demand_change = ass("Ass_A_P_fermen_nondairy_change")
        p_fermen_poultry.CO2e_pb = (
            p_fermen_poultry.pet_sites * p_fermen_poultry.CO2e_pb_per_t
        )
        p_fermen_oanimal.pet_sites = a18.p_fermen_oanimal.amount * (
            1 + p_fermen_oanimal.demand_change
        )
        p_fermen_oanimal.CO2e_pb_per_t = a18.p_fermen_oanimal.CO2e_pb_per_t
        p_fermen_nondairy.CO2e_total = (
            p_fermen_nondairy.CO2e_pb + p_fermen_nondairy.CO2e_cb
        )
        p_fermen_nondairy.change_CO2e_t = (
            p_fermen_nondairy.CO2e_total - a18.p_fermen_nondairy.CO2e_total
        )
        p_fermen_nondairy.change_CO2e_pct = (
            p_fermen_nondairy.change_CO2e_t / a18.p_fermen_nondairy.CO2e_total
        )
        p_fermen_nondairy.CO2e_total_2021_estimated = (
            a18.p_fermen_nondairy.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fermen_nondairy.cost_climate_saved = (
            (p_fermen_nondairy.CO2e_total_2021_estimated - p_fermen_nondairy.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fermen_swine.demand_change = ass("Ass_A_P_fermen_swine_change")
        p_fermen_oanimal.CO2e_pb = (
            p_fermen_oanimal.pet_sites * p_fermen_oanimal.CO2e_pb_per_t
        )
        p_fermen.CO2e_pb = (
            p_fermen_dairycow.CO2e_pb
            + p_fermen_nondairy.CO2e_pb
            + p_fermen_swine.CO2e_pb
            + p_fermen_poultry.CO2e_pb
            + p_fermen_oanimal.CO2e_pb
        )
        p_fermen.CO2e_total = p_fermen.CO2e_pb + p_fermen.CO2e_cb
        p_fermen_swine.CO2e_total = p_fermen_swine.CO2e_pb + p_fermen_swine.CO2e_cb
        p_fermen_swine.change_CO2e_t = (
            p_fermen_swine.CO2e_total - a18.p_fermen_swine.CO2e_total
        )
        p_fermen_swine.change_CO2e_pct = (
            p_fermen_swine.change_CO2e_t / a18.p_fermen_swine.CO2e_total
        )
        p_fermen_swine.CO2e_total_2021_estimated = a18.p_fermen_swine.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_fermen_swine.cost_climate_saved = (
            (p_fermen_swine.CO2e_total_2021_estimated - p_fermen_swine.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fermen_poultry.demand_change = ass("Ass_A_P_fermen_poultry_change")
        p_fermen.cost_climate_saved = (
            (p_fermen.CO2e_total_2021_estimated - p_fermen.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fermen.change_CO2e_t = p_fermen.CO2e_total - a18.p_fermen.CO2e_total
        p_fermen.change_CO2e_pct = p_fermen.change_CO2e_t / a18.p_fermen.CO2e_total
        p_fermen_poultry.CO2e_total = (
            p_fermen_poultry.CO2e_pb + p_fermen_poultry.CO2e_cb
        )
        p_fermen_poultry.change_CO2e_t = (
            p_fermen_poultry.CO2e_total - a18.p_fermen_poultry.CO2e_total
        )
        # p_fermen_poultry.change_CO2e_pct = (p_fermen_poultry.change_CO2e_t /a18.p_fermen_poultry.CO2e_total) #Todo not calculted div 0
        p_fermen_poultry.CO2e_total_2021_estimated = (
            a18.p_fermen_poultry.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fermen_poultry.cost_climate_saved = (
            (p_fermen_poultry.CO2e_total_2021_estimated - p_fermen_poultry.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fermen_oanimal.demand_change = ass("Ass_A_P_fermen_oanimal_change")
        p_manure_dairycow.pet_sites = p_fermen_dairycow.pet_sites
        p_manure_dairycow.CO2e_pb_per_t = a18.p_manure_dairycow.CO2e_pb_per_t * (
            1 + p_manure_dairycow.demand_change
        )
        p_manure_dairycow.CO2e_pb = (
            p_manure_dairycow.pet_sites * p_manure_dairycow.CO2e_pb_per_t
        )
        p_fermen_oanimal.CO2e_total = (
            p_fermen_oanimal.CO2e_pb + p_fermen_oanimal.CO2e_cb
        )
        p_fermen_oanimal.change_CO2e_t = (
            p_fermen_oanimal.CO2e_total - a18.p_fermen_oanimal.CO2e_total
        )
        p_fermen_oanimal.change_CO2e_pct = (
            p_fermen_oanimal.change_CO2e_t / a18.p_fermen_oanimal.CO2e_total
        )
        p_fermen_oanimal.CO2e_total_2021_estimated = (
            a18.p_fermen_oanimal.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fermen_oanimal.cost_climate_saved = (
            (p_fermen_oanimal.CO2e_total_2021_estimated - p_fermen_oanimal.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure_nondairy.pet_sites = p_fermen_nondairy.pet_sites
        p_soil_fertilizer.demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        p_manure_nondairy.demand_change = ass(
            "Ass_A_P_manure_ratio_CO2e_to_amount_change"
        )
        p_manure_nondairy.CO2e_pb_per_t = a18.p_manure_nondairy.CO2e_pb_per_t * (
            1 + p_manure_nondairy.demand_change
        )
        p_manure.CO2e_total_2021_estimated = a18.p_manure.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_manure_nondairy.CO2e_pb = (
            p_manure_nondairy.pet_sites * p_manure_nondairy.CO2e_pb_per_t
        )
        p_manure_swine.pet_sites = p_fermen_swine.pet_sites
        p_manure_swine.demand_change = ass("Ass_A_P_manure_ratio_CO2e_to_amount_change")
        p_manure_swine.CO2e_pb_per_t = a18.p_manure_swine.CO2e_pb_per_t * (
            1 + p_manure_swine.demand_change
        )
        p_manure_swine.CO2e_pb = p_manure_swine.pet_sites * p_manure_swine.CO2e_pb_per_t
        p_manure_dairycow.CO2e_total = (
            p_manure_dairycow.CO2e_pb + p_manure_dairycow.CO2e_cb
        )
        p_manure_dairycow.change_CO2e_t = (
            p_manure_dairycow.CO2e_total - a18.p_manure_dairycow.CO2e_total
        )
        p_manure_dairycow.change_CO2e_pct = (
            p_manure_dairycow.change_CO2e_t / a18.p_manure_dairycow.CO2e_total
        )
        p_manure_dairycow.CO2e_total_2021_estimated = (
            a18.p_manure_dairycow.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_manure_dairycow.cost_climate_saved = (
            (p_manure_dairycow.CO2e_total_2021_estimated - p_manure_dairycow.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure_poultry.pet_sites = p_fermen_poultry.pet_sites
        p_manure_poultry.demand_change = ass(
            "Ass_A_P_manure_ratio_CO2e_to_amount_change"
        )
        p_manure_poultry.CO2e_pb_per_t = a18.p_manure_poultry.CO2e_pb_per_t * (
            1 + p_manure_poultry.demand_change
        )
        p_manure_poultry.CO2e_pb = (
            p_manure_poultry.pet_sites * p_manure_poultry.CO2e_pb_per_t
        )
        p_manure_nondairy.CO2e_total = (
            p_manure_nondairy.CO2e_pb + p_manure_nondairy.CO2e_cb
        )
        p_manure_nondairy.change_CO2e_t = (
            p_manure_nondairy.CO2e_total - a18.p_manure_nondairy.CO2e_total
        )
        p_manure_nondairy.change_CO2e_pct = (
            p_manure_nondairy.change_CO2e_t / a18.p_manure_nondairy.CO2e_total
        )
        p_manure_nondairy.CO2e_total_2021_estimated = (
            a18.p_manure_nondairy.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_manure_nondairy.cost_climate_saved = (
            (p_manure_nondairy.CO2e_total_2021_estimated - p_manure_nondairy.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure_oanimal.pet_sites = p_fermen_oanimal.pet_sites
        p_manure_oanimal.demand_change = ass(
            "Ass_A_P_manure_ratio_CO2e_to_amount_change"
        )
        p_manure_oanimal.CO2e_pb_per_t = a18.p_manure_oanimal.CO2e_pb_per_t * (
            1 + p_manure_oanimal.demand_change
        )
        p_manure_oanimal.CO2e_pb = (
            p_manure_oanimal.pet_sites * p_manure_oanimal.CO2e_pb_per_t
        )
        p_manure_swine.CO2e_total = p_manure_swine.CO2e_pb + p_manure_swine.CO2e_cb
        p_manure_swine.change_CO2e_t = (
            p_manure_swine.CO2e_total - a18.p_manure_swine.CO2e_total
        )
        p_manure_swine.change_CO2e_pct = (
            p_manure_swine.change_CO2e_t / a18.p_manure_swine.CO2e_total
        )
        p_manure_swine.CO2e_total_2021_estimated = a18.p_manure_swine.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_manure_swine.cost_climate_saved = (
            (p_manure_swine.CO2e_total_2021_estimated - p_manure_swine.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure_deposition.pet_sites = (
            p_fermen_dairycow.pet_sites
            + p_fermen_nondairy.pet_sites
            + p_fermen_swine.pet_sites
            + p_fermen_oanimal.pet_sites
        )
        p_manure_deposition.demand_change = ass(
            "Ass_A_P_manure_ratio_CO2e_to_amount_change"
        )
        p_manure_deposition.CO2e_pb_per_t = a18.p_manure_deposition.CO2e_pb_per_t * (
            1 + p_manure_deposition.demand_change
        )
        p_manure_deposition.CO2e_pb = (
            p_manure_deposition.pet_sites * p_manure_deposition.CO2e_pb_per_t
        )
        p_manure_poultry.CO2e_total = (
            p_manure_poultry.CO2e_pb + p_manure_poultry.CO2e_cb
        )
        p_manure_poultry.change_CO2e_t = (
            p_manure_poultry.CO2e_total - a18.p_manure_poultry.CO2e_total
        )
        p_manure_poultry.change_CO2e_pct = (
            p_manure_poultry.change_CO2e_t / a18.p_manure_poultry.CO2e_total
        )
        p_manure_poultry.CO2e_total_2021_estimated = (
            a18.p_manure_poultry.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_manure_poultry.cost_climate_saved = (
            (p_manure_poultry.CO2e_total_2021_estimated - p_manure_poultry.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure.CO2e_pb = (
            p_manure_dairycow.CO2e_pb
            + p_manure_nondairy.CO2e_pb
            + p_manure_swine.CO2e_pb
            + p_manure_poultry.CO2e_pb
            + p_manure_oanimal.CO2e_pb
            + p_manure_deposition.CO2e_pb
        )
        p_manure.CO2e_total = p_manure.CO2e_pb + p_manure.CO2e_cb
        p_manure.cost_climate_saved = (
            (p_manure.CO2e_total_2021_estimated - p_manure.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure.change_CO2e_t = p_manure.CO2e_total - a18.p_manure.CO2e_total
        p_manure_oanimal.CO2e_total = (
            p_manure_oanimal.CO2e_pb + p_manure_oanimal.CO2e_cb
        )
        p_manure_oanimal.change_CO2e_t = (
            p_manure_oanimal.CO2e_total - a18.p_manure_oanimal.CO2e_total
        )
        p_manure_oanimal.change_CO2e_pct = (
            p_manure_oanimal.change_CO2e_t / a18.p_manure_oanimal.CO2e_total
        )
        p_manure_oanimal.CO2e_total_2021_estimated = (
            a18.p_manure_oanimal.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_manure_oanimal.cost_climate_saved = (
            (p_manure_oanimal.CO2e_total_2021_estimated - p_manure_oanimal.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_manure.change_CO2e_pct = p_manure.change_CO2e_t / a18.p_manure.CO2e_total
        p_soil_fertilizer.area_ha = l30.g_crop.area_ha
        p_soil_fertilizer.CO2e_pb_per_t = a18.p_soil_fertilizer.CO2e_pb_per_t * (
            1 + p_soil_fertilizer.demand_change
        )
        p_soil_fertilizer.CO2e_pb = (
            p_soil_fertilizer.area_ha * p_soil_fertilizer.CO2e_pb_per_t
        )
        p_manure_deposition.CO2e_total = (
            p_manure_deposition.CO2e_pb + p_manure_deposition.CO2e_cb
        )
        p_manure_deposition.change_CO2e_t = (
            p_manure_deposition.CO2e_total - a18.p_manure_deposition.CO2e_total
        )
        p_manure_deposition.change_CO2e_pct = (
            p_manure_deposition.change_CO2e_t / a18.p_manure_deposition.CO2e_total
        )
        p_manure_deposition.CO2e_total_2021_estimated = (
            a18.p_manure_deposition.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_manure_deposition.cost_climate_saved = (
            (
                p_manure_deposition.CO2e_total_2021_estimated
                - p_manure_deposition.CO2e_total
            )
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_manure.area_ha = l30.g_crop.area_ha
        p_other_liming_calcit.CO2e_pb_per_t = fact(
            "Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018"
        )
        p_soil_manure.demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        p_soil_manure.CO2e_pb_per_t = a18.p_soil_manure.CO2e_pb_per_t * (
            1 + p_soil_manure.demand_change
        )
        p_soil.CO2e_total_2021_estimated = a18.p_soil.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_manure.CO2e_pb = p_soil_manure.area_ha * p_soil_manure.CO2e_pb_per_t
        p_soil_sludge.area_ha = l30.g_crop.area_ha
        p_soil_sludge.demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        p_soil_fertilizer.area_ha_change = -(
            a18.p_soil_fertilizer.area_ha - p_soil_fertilizer.area_ha
        )
        p_soil_sludge.CO2e_pb_per_t = a18.p_soil_sludge.CO2e_pb_per_t * (
            1 + p_soil_sludge.demand_change
        )
        p_soil_sludge.CO2e_pb = p_soil_sludge.area_ha * p_soil_sludge.CO2e_pb_per_t
        p_soil_fertilizer.CO2e_total = (
            p_soil_fertilizer.CO2e_pb + p_soil_fertilizer.CO2e_cb
        )
        p_soil_fertilizer.change_CO2e_t = (
            p_soil_fertilizer.CO2e_total - a18.p_soil_fertilizer.CO2e_total
        )
        p_soil_fertilizer.change_CO2e_pct = (
            p_soil_fertilizer.change_CO2e_t / a18.p_soil_fertilizer.CO2e_total
        )
        p_soil_fertilizer.CO2e_total_2021_estimated = (
            a18.p_soil_fertilizer.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_soil_fertilizer.cost_climate_saved = (
            (p_soil_fertilizer.CO2e_total_2021_estimated - p_soil_fertilizer.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_ecrop.area_ha = l30.g_crop.area_ha
        p_soil_ecrop.demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        p_soil_manure.area_ha_change = -(
            a18.p_soil_manure.area_ha - p_soil_manure.area_ha
        )
        p_soil_ecrop.CO2e_pb_per_t = a18.p_soil_ecrop.CO2e_pb_per_t * (
            1 + p_soil_ecrop.demand_change
        )
        p_soil_ecrop.CO2e_pb = p_soil_ecrop.area_ha * p_soil_ecrop.CO2e_pb_per_t
        p_soil_manure.CO2e_total = p_soil_manure.CO2e_pb + p_soil_manure.CO2e_cb
        p_soil_manure.change_CO2e_t = (
            p_soil_manure.CO2e_total - a18.p_soil_manure.CO2e_total
        )
        p_soil_manure.change_CO2e_pct = (
            p_soil_manure.change_CO2e_t / a18.p_soil_manure.CO2e_total
        )
        p_soil_manure.CO2e_total_2021_estimated = a18.p_soil_manure.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_manure.cost_climate_saved = (
            (p_soil_manure.CO2e_total_2021_estimated - p_soil_manure.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_grazing.area_ha = l30.g_grass.area_ha
        p_fermen_dairycow.pet_sites = a18.p_fermen_dairycow.amount * (
            1 + p_fermen_dairycow.demand_change
        )
        p_fermen_nondairy.pet_sites = a18.p_fermen_nondairy.amount * (
            1 + p_fermen_nondairy.demand_change
        )
        p_fermen_oanimal.pet_sites = a18.p_fermen_oanimal.amount * (
            1 + p_fermen_oanimal.demand_change
        )
        p_soil_grazing.CO2e_pb_per_t = (
            a18.p_soil_grazing.CO2e_pb_per_t
            * (
                p_fermen_dairycow.pet_sites
                + p_fermen_nondairy.pet_sites
                + p_fermen_oanimal.pet_sites
            )
            / (
                a18.p_fermen_dairycow.amount
                + a18.p_fermen_nondairy.amount
                + a18.p_fermen_oanimal.amount
            )
        )
        p_soil_sludge.area_ha_change = -(
            a18.p_soil_sludge.area_ha - p_soil_sludge.area_ha
        )
        p_soil_grazing.CO2e_pb = p_soil_grazing.area_ha * p_soil_grazing.CO2e_pb_per_t
        p_soil_residue.area_ha = l30.g_crop.area_ha
        p_soil_sludge.CO2e_total = p_soil_sludge.CO2e_pb + p_soil_sludge.CO2e_cb
        p_soil_sludge.change_CO2e_t = (
            p_soil_sludge.CO2e_total - a18.p_soil_sludge.CO2e_total
        )
        p_soil_sludge.change_CO2e_pct = (
            p_soil_sludge.change_CO2e_t / a18.p_soil_sludge.CO2e_total
        )
        p_soil_sludge.CO2e_total_2021_estimated = a18.p_soil_sludge.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_sludge.cost_climate_saved = (
            (p_soil_sludge.CO2e_total_2021_estimated - p_soil_sludge.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_residue.CO2e_pb_per_t = a18.p_soil_residue.CO2e_pb_per_t
        p_soil_residue.CO2e_pb = p_soil_residue.area_ha * p_soil_residue.CO2e_pb_per_t
        p_soil_ecrop.area_ha_change = -(a18.p_soil_ecrop.area_ha - p_soil_ecrop.area_ha)
        p_soil_orgfarm.area_ha = (
            l30.g_crop_org_low.area_ha
            + l30.g_crop_org_high.area_ha
            + l30.g_grass_org_low.area_ha
            + l30.g_grass_org_high.area_ha
        )
        p_soil_orgfarm.CO2e_pb_per_t = a18.p_soil_orgfarm.CO2e_pb_per_t
        p_soil_ecrop.CO2e_total = p_soil_ecrop.CO2e_pb + p_soil_ecrop.CO2e_cb
        p_soil_ecrop.change_CO2e_t = (
            p_soil_ecrop.CO2e_total - a18.p_soil_ecrop.CO2e_total
        )
        p_soil_ecrop.change_CO2e_pct = (
            p_soil_ecrop.change_CO2e_t / a18.p_soil_ecrop.CO2e_total
        )
        p_soil_ecrop.CO2e_total_2021_estimated = a18.p_soil_ecrop.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_ecrop.cost_climate_saved = (
            (p_soil_ecrop.CO2e_total_2021_estimated - p_soil_ecrop.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_grazing.demand_change = (
            p_soil_grazing.CO2e_pb_per_t / a18.p_soil_grazing.CO2e_pb_per_t - 1
        )
        p_soil_orgfarm.CO2e_pb = p_soil_orgfarm.area_ha * p_soil_orgfarm.CO2e_pb_per_t
        p_soil_grazing.area_ha_change = -(
            a18.p_soil_grazing.area_ha - p_soil_grazing.area_ha
        )
        p_soil_orgloss.area_ha = (
            l30.g_crop_org_low.area_ha + l30.g_crop_org_high.area_ha
        )
        p_soil_orgloss.CO2e_pb_per_t = a18.p_soil_orgloss.CO2e_pb_per_t
        p_soil_grazing.CO2e_total = p_soil_grazing.CO2e_pb + p_soil_grazing.CO2e_cb
        p_soil_grazing.change_CO2e_t = (
            p_soil_grazing.CO2e_total - a18.p_soil_grazing.CO2e_total
        )
        p_soil_grazing.change_CO2e_pct = (
            p_soil_grazing.change_CO2e_t / a18.p_soil_grazing.CO2e_total
        )
        p_soil_grazing.CO2e_total_2021_estimated = a18.p_soil_grazing.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_grazing.cost_climate_saved = (
            (p_soil_grazing.CO2e_total_2021_estimated - p_soil_grazing.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_residue.demand_change = (
            p_soil_residue.CO2e_pb_per_t / a18.p_soil_residue.CO2e_pb_per_t - 1
        )
        p_soil_orgloss.CO2e_pb = p_soil_orgloss.area_ha * p_soil_orgloss.CO2e_pb_per_t
        p_soil_residue.area_ha_change = -(
            a18.p_soil_residue.area_ha - p_soil_residue.area_ha
        )
        p_soil_leaching.area_ha = l30.g_crop.area_ha + l30.g_grass.area_ha
        p_soil_leaching.demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        p_soil_residue.CO2e_total = p_soil_residue.CO2e_pb + p_soil_residue.CO2e_cb
        p_soil_residue.change_CO2e_t = (
            p_soil_residue.CO2e_total - a18.p_soil_residue.CO2e_total
        )
        p_soil_residue.change_CO2e_pct = (
            p_soil_residue.change_CO2e_t / a18.p_soil_residue.CO2e_total
        )
        p_soil_residue.CO2e_total_2021_estimated = a18.p_soil_residue.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_residue.cost_climate_saved = (
            (p_soil_residue.CO2e_total_2021_estimated - p_soil_residue.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_orgfarm.demand_change = (
            p_soil_orgfarm.CO2e_pb_per_t / a18.p_soil_orgfarm.CO2e_pb_per_t - 1
        )
        p_soil_leaching.CO2e_pb_per_t = a18.p_soil_leaching.CO2e_pb_per_t * (
            1 + p_soil_leaching.demand_change
        )
        p_soil_orgfarm.area_ha_change = -(
            a18.p_soil_orgfarm.area_ha - p_soil_orgfarm.area_ha
        )
        p_soil_leaching.CO2e_pb = (
            p_soil_leaching.area_ha * p_soil_leaching.CO2e_pb_per_t
        )
        p_soil_deposition.area_ha = l30.g_crop.area_ha + l30.g_grass.area_ha
        p_soil_orgfarm.CO2e_total = p_soil_orgfarm.CO2e_pb + p_soil_orgfarm.CO2e_cb
        p_soil_orgfarm.change_CO2e_t = (
            p_soil_orgfarm.CO2e_total - a18.p_soil_orgfarm.CO2e_total
        )
        p_soil_orgfarm.change_CO2e_pct = (
            p_soil_orgfarm.change_CO2e_t / a18.p_soil_orgfarm.CO2e_total
        )
        p_soil_orgfarm.CO2e_total_2021_estimated = a18.p_soil_orgfarm.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_orgfarm.cost_climate_saved = (
            (p_soil_orgfarm.CO2e_total_2021_estimated - p_soil_orgfarm.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil_orgloss.demand_change = (
            p_soil_orgloss.CO2e_pb_per_t / a18.p_soil_orgloss.CO2e_pb_per_t - 1
        )
        p_soil_deposition.demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        p_soil_orgloss.area_ha_change = -(
            a18.p_soil_orgloss.area_ha - p_soil_orgloss.area_ha
        )
        p_soil_deposition.CO2e_pb_per_t = a18.p_soil_deposition.CO2e_pb_per_t * (
            1 + p_soil_deposition.demand_change
        )
        p_soil_deposition.CO2e_pb = (
            p_soil_deposition.area_ha * p_soil_deposition.CO2e_pb_per_t
        )
        p_soil_orgloss.CO2e_total = p_soil_orgloss.CO2e_pb + p_soil_orgloss.CO2e_cb
        p_soil_orgloss.change_CO2e_t = (
            p_soil_orgloss.CO2e_total - a18.p_soil_orgloss.CO2e_total
        )
        p_soil_orgloss.change_CO2e_pct = (
            p_soil_orgloss.change_CO2e_t / a18.p_soil_orgloss.CO2e_total
        )
        p_soil_orgloss.CO2e_total_2021_estimated = a18.p_soil_orgloss.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_soil_orgloss.cost_climate_saved = (
            (p_soil_orgloss.CO2e_total_2021_estimated - p_soil_orgloss.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil.CO2e_pb = (
            p_soil_fertilizer.CO2e_pb
            + p_soil_manure.CO2e_pb
            + p_soil_sludge.CO2e_pb
            + p_soil_ecrop.CO2e_pb
            + p_soil_grazing.CO2e_pb
            + p_soil_residue.CO2e_pb
            + p_soil_orgfarm.CO2e_pb
            + p_soil_orgloss.CO2e_pb
            + p_soil_leaching.CO2e_pb
            + p_soil_deposition.CO2e_pb
        )
        p_soil.CO2e_total = p_soil.CO2e_pb + p_soil.CO2e_cb
        p_soil_leaching.area_ha_change = -(
            a18.p_soil_leaching.area_ha - p_soil_leaching.area_ha
        )
        p_soil.cost_climate_saved = (
            (p_soil.CO2e_total_2021_estimated - p_soil.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil.change_CO2e_t = p_soil.CO2e_total - a18.p_soil.CO2e_total
        p_soil_leaching.CO2e_total = p_soil_leaching.CO2e_pb + p_soil_leaching.CO2e_cb
        p_soil_leaching.change_CO2e_t = (
            p_soil_leaching.CO2e_total - a18.p_soil_leaching.CO2e_total
        )
        p_soil_leaching.change_CO2e_pct = (
            p_soil_leaching.change_CO2e_t / a18.p_soil_leaching.CO2e_total
        )
        p_soil_leaching.CO2e_total_2021_estimated = (
            a18.p_soil_leaching.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_soil_leaching.cost_climate_saved = (
            (p_soil_leaching.CO2e_total_2021_estimated - p_soil_leaching.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_soil.change_CO2e_pct = p_soil.change_CO2e_t / a18.p_soil.CO2e_total
        p_other_urea.demand_change = ass("Ass_A_P_other_urea_amount_change")
        p_soil_deposition.area_ha_change = -(
            a18.p_soil_deposition.area_ha - p_soil_deposition.area_ha
        )
        p_other_urea.prod_volume = a18.p_other_urea.prod_volume * (
            1 + p_other_urea.demand_change
        )
        p_other_urea.CO2e_pb_per_t = fact("Fact_A_P_other_urea_CO2e_pb_to_amount_2018")
        p_soil_deposition.CO2e_total = (
            p_soil_deposition.CO2e_pb + p_soil_deposition.CO2e_cb
        )
        p_soil_deposition.change_CO2e_t = (
            p_soil_deposition.CO2e_total - a18.p_soil_deposition.CO2e_total
        )
        p_soil_deposition.change_CO2e_pct = (
            p_soil_deposition.change_CO2e_t / a18.p_soil_deposition.CO2e_total
        )
        p_soil_deposition.CO2e_total_2021_estimated = (
            a18.p_soil_deposition.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_soil_deposition.cost_climate_saved = (
            (p_soil_deposition.CO2e_total_2021_estimated - p_soil_deposition.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other_liming_calcit.demand_change = ass(
            "Ass_A_P_other_liming_calcit_amount_change"
        )
        p_other_urea.CO2e_pb = p_other_urea.prod_volume * p_other_urea.CO2e_pb_per_t
        p_other_liming_calcit.prod_volume = a18.p_other_liming_calcit.prod_volume * (
            1 + p_other_liming_calcit.demand_change
        )
        p_other_liming_calcit.CO2e_pb = (
            p_other_liming_calcit.prod_volume * p_other_liming_calcit.CO2e_pb_per_t
        )
        p_other.CO2e_total_2021_estimated = a18.p_other.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_other_liming_dolomite.demand_change = ass(
            "Ass_A_P_other_liming_dolomit_amount_change"
        )
        p_other_liming_dolomite.prod_volume = (
            a18.p_other_liming_dolomite.prod_volume
            * (1 + p_other_liming_dolomite.demand_change)
        )
        p_other_liming_dolomite.CO2e_pb_per_t = fact(
            "Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018"
        )
        p_other_liming_dolomite.CO2e_pb = (
            p_other_liming_dolomite.prod_volume * p_other_liming_dolomite.CO2e_pb_per_t
        )
        p_other_liming.CO2e_pb = (
            p_other_liming_calcit.CO2e_pb + p_other_liming_dolomite.CO2e_pb
        )
        p_other_kas.demand_change = ass("Ass_A_P_other_kas_amount_change")
        p_other_liming.CO2e_total_2021_estimated = a18.p_other_liming.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_other_kas.prod_volume = a18.p_other_kas.prod_volume * (
            1 + p_other_kas.demand_change
        )
        p_other_kas.CO2e_pb_per_t = fact(
            "Fact_A_P_other_kas_ratio_CO2e_pb_to_amount_2018"
        )
        p_other_kas.CO2e_pb = p_other_kas.prod_volume * p_other_kas.CO2e_pb_per_t
        p_other_liming.CO2e_total = p_other_liming.CO2e_pb + p_other_liming.CO2e_cb
        p_other_liming.cost_climate_saved = (
            (p_other_liming.CO2e_total_2021_estimated - p_other_liming.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other_liming_calcit.CO2e_total = (
            p_other_liming_calcit.CO2e_pb + p_other_liming_calcit.CO2e_cb
        )
        p_other_liming_calcit.change_CO2e_t = (
            p_other_liming_calcit.CO2e_total - a18.p_other_liming_calcit.CO2e_total
        )
        p_other_liming_calcit.change_CO2e_pct = (
            p_other_liming_calcit.change_CO2e_t / a18.p_other_liming_calcit.CO2e_total
        )
        p_other_liming_calcit.CO2e_total_2021_estimated = (
            a18.p_other_liming_calcit.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_other_liming_calcit.cost_climate_saved = (
            (
                p_other_liming_calcit.CO2e_total_2021_estimated
                - p_other_liming_calcit.CO2e_total
            )
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other_liming.change_CO2e_t = (
            p_other_liming.CO2e_total - a18.p_other_liming.CO2e_total
        )
        p_other_liming.prod_volume = (
            p_other_liming_calcit.prod_volume + p_other_liming_dolomite.prod_volume
        )
        p_other_ecrop.demand_change = ass("Ass_A_P_other_ecrop_amount_change")
        p_other_liming.change_CO2e_pct = (
            p_other_liming.change_CO2e_t / a18.p_other_liming.CO2e_total
        )
        p_other_liming_dolomite.CO2e_total = (
            p_other_liming_dolomite.CO2e_pb + p_other_liming_dolomite.CO2e_cb
        )
        p_other_liming_dolomite.change_CO2e_t = (
            p_other_liming_dolomite.CO2e_total - a18.p_other_liming_dolomite.CO2e_total
        )
        p_other_liming_dolomite.change_CO2e_pct = (
            p_other_liming_dolomite.change_CO2e_t
            / a18.p_other_liming_dolomite.CO2e_total
        )
        p_other_liming_dolomite.CO2e_total_2021_estimated = (
            a18.p_other_liming_dolomite.CO2e_total
            * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_other_liming_dolomite.cost_climate_saved = (
            (
                p_other_liming_dolomite.CO2e_total_2021_estimated
                - p_other_liming_dolomite.CO2e_total
            )
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other_ecrop.prod_volume = a18.p_other_ecrop.prod_volume * (
            1 + p_other_ecrop.demand_change
        )
        p_other_ecrop.CO2e_pb_per_t = fact(
            "Fact_A_P_other_ecrop_ratio_CO2e_pb_to_amount_2018"
        )
        p_other_ecrop.CO2e_pb = p_other_ecrop.prod_volume * p_other_ecrop.CO2e_pb_per_t
        p_other.CO2e_pb = (
            p_other_liming.CO2e_pb
            + p_other_urea.CO2e_pb
            + p_other_kas.CO2e_pb
            + p_other_ecrop.CO2e_pb
        )
        p_other_urea.CO2e_total = p_other_urea.CO2e_pb + p_other_urea.CO2e_cb
        p_other_urea.change_CO2e_t = (
            p_other_urea.CO2e_total - a18.p_other_urea.CO2e_total
        )
        p_other_urea.change_CO2e_pct = (
            p_other_urea.change_CO2e_t / a18.p_other_urea.CO2e_total
        )
        p_other_urea.CO2e_total_2021_estimated = a18.p_other_urea.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_other_urea.cost_climate_saved = (
            (p_other_urea.CO2e_total_2021_estimated - p_other_urea.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other.CO2e_total = p_other.CO2e_pb + p_other.CO2e_cb
        p_other.cost_climate_saved = (
            (p_other.CO2e_total_2021_estimated - p_other.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other.change_CO2e_t = p_other.CO2e_total - a18.p_other.CO2e_total
        p_other.change_CO2e_pct = p_other.change_CO2e_t / a18.p_other.CO2e_total
        p_other_kas.CO2e_total = p_other_kas.CO2e_pb + p_other_kas.CO2e_cb
        p_other_kas.change_CO2e_t = p_other_kas.CO2e_total - a18.p_other.CO2e_total
        p_other_kas.change_CO2e_pct = (
            p_other_kas.change_CO2e_t / 1
        )  # a18.p_other_kas.CO2e_total)
        p_other_kas.CO2e_total_2021_estimated = a18.p_other_kas.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_other_kas.cost_climate_saved = (
            (p_other_kas.CO2e_total_2021_estimated - p_other_kas.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p.CO2e_total = (
            p_fermen.CO2e_total
            + p_manure.CO2e_total
            + p_soil.CO2e_total
            + p_other.CO2e_total
            + p_other_energy.CO2e_total
        )
        p.change_CO2e_t = p.CO2e_total - a18.p.CO2e_total
        p.change_CO2e_pct = p.change_CO2e_t / a18.p.CO2e_total
        p.cost_climate_saved = (
            (p.CO2e_total_2021_estimated - p.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_other_ecrop.CO2e_total = p_other_ecrop.CO2e_pb + p_other_ecrop.CO2e_cb
        p_other_ecrop.change_CO2e_t = (
            p_other_ecrop.CO2e_total - a18.p_other_ecrop.CO2e_total
        )
        p_other_ecrop.change_CO2e_pct = (
            p_other_ecrop.change_CO2e_t / a18.p_other_ecrop.CO2e_total
        )
        p_other_ecrop.CO2e_total_2021_estimated = a18.p_other_ecrop.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_other_ecrop.cost_climate_saved = (
            (p_other_ecrop.CO2e_total_2021_estimated - p_other_ecrop.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_operation_elec_elcon.demand_change = ass("Ass_B_D_fec_elec_elcon_change")
        p_operation_heat.rate_rehab_pa = entry("In_R_rehab_rate_pa")
        p_operation_heat.pct_rehab = fact(
            "Fact_B_P_ratio_renovated_to_not_renovated_2021"
        ) + p_operation_heat.rate_rehab_pa * entry("In_M_duration_target")
        p_operation_vehicles.energy = a18.p_operation_vehicles.energy * (
            1 + p_operation_vehicles.demand_change
        )
        p_operation_vehicles.demand_ediesel = (
            p_operation_vehicles.energy
            * a18.s_diesel.energy
            / (a18.s_petrol.energy + a18.s_diesel.energy)
        )
        p_operation_heat.pct_nonrehab = 1 - p_operation_heat.pct_rehab
        p_operation_heat.area_m2_rehab = (
            p_operation_heat.pct_rehab * a18.p_operation_heat.area_m2
        )
        p_operation_heat.demand_heat_rehab = p_operation_heat.area_m2_rehab * ass(
            "Ass_B_D_ratio_fec_to_area_2050"
        )
        p_operation_heat.demand_heatpump = p_operation_heat.demand_heat_rehab
        p_operation_heat.area_m2_nonrehab = (
            p_operation_heat.pct_nonrehab * a18.p_operation_heat.area_m2
        )
        p_other_energy.demand_heatpump = (
            p_operation_heat.demand_heatpump
            + p_operation_elec_elcon.demand_heatpump
            + p_elec_heatpump.demand_heatpump
            + p_operation_vehicles.demand_heatpump
        )
        p_operation_heat.area_m2 = a18.p_operation_heat.area_m2
        p_operation_heat.demand_heat_nonrehab = (
            p_operation_heat.area_m2_nonrehab
            * (
                a18.p_operation_heat.factor_adapted_to_fec
                - fact("Fact_B_P_ratio_renovated_to_not_renovated_2021")
                * ass("Ass_B_D_ratio_fec_to_area_2050")
            )
            / (1 - fact("Fact_B_P_ratio_renovated_to_not_renovated_2021"))
        )
        s_heatpump.energy = p_other_energy.demand_heatpump
        p_operation_heat.energy = (
            p_operation_heat.demand_heat_nonrehab + p_operation_heat.demand_heat_rehab
        )
        p_operation_heat.demand_biomass = min(
            a18.s_biomass.energy, p_operation_heat.energy - s_heatpump.energy
        )
        p_other_energy.demand_biomass = (
            p_operation_heat.demand_biomass
            + p_operation_elec_elcon.demand_biomass
            + p_elec_heatpump.demand_biomass
            + p_operation_vehicles.demand_biomass
        )
        s_biomass.energy = p_other_energy.demand_biomass
        p_operation_heat.demand_emethan = (
            p_operation_heat.energy - s_biomass.energy - s_heatpump.energy
        )
        p_operation_heat.fec_factor_averaged = (
            p_operation_heat.energy / a18.p_operation_heat.area_m2
        )
        p_operation_heat.change_energy_MWh = (
            p_operation_heat.energy - a18.p_operation_heat.energy
        )
        p_operation_heat.change_energy_pct = (
            p_operation_heat.change_energy_MWh / a18.p_operation_heat.energy
        )
        p_operation_heat.invest_per_x = fact(
            "Fact_R_P_energetical_renovation_cost_business"
        )
        p_operation_heat.invest = (
            p_operation_heat.area_m2_rehab
            * (1 - fact("Fact_B_P_ratio_renovated_to_not_renovated_2021"))
            * p_operation_heat.invest_per_x
        )
        p_operation_heat.pct_of_wage = fact(
            "Fact_B_P_renovations_ratio_wage_to_main_revenue_2017"
        )
        p_operation_heat.cost_wage = (
            p_operation_heat.invest
            / entry("In_M_duration_target")
            * p_operation_heat.pct_of_wage
        )
        p_operation_heat.ratio_wage_to_emplo = fact(
            "Fact_B_P_renovations_wage_per_person_per_year_2017"
        )
        p_operation_heat.demand_emplo = (
            p_operation_heat.cost_wage / p_operation_heat.ratio_wage_to_emplo
        )
        p_operation_heat.emplo_existing = (
            fact("Fact_B_P_renovation_emplo_2017")
            * ass("Ass_B_D_renovation_emplo_pct_of_A")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        p_operation_heat.demand_emplo_new = max(
            0, p_operation_heat.demand_emplo - p_operation_heat.emplo_existing
        )
        p_operation_heat.invest_pa = p_operation_heat.invest / entry(
            "In_M_duration_target"
        )
        p_elec_heatpump.energy = s_heatpump.energy / fact(
            "Fact_R_S_heatpump_mean_annual_performance_factor_all"
        )
        p_operation_elec_elcon.energy = a18.p_operation_elec_elcon.energy * (
            1 + p_operation_elec_elcon.demand_change
        )
        p_operation_elec_elcon.demand_electricity = p_operation_elec_elcon.energy
        p_elec_heatpump.demand_electricity = p_elec_heatpump.energy
        p_other_energy.energy = (
            p_operation_heat.energy
            + p_operation_elec_elcon.energy
            + p_elec_heatpump.energy
            + p_operation_vehicles.energy
        )
        p_operation_vehicles.demand_epetrol = (
            p_operation_vehicles.energy
            * a18.s_petrol.energy
            / (a18.s_petrol.energy + a18.s_diesel.energy)
        )
        p_other_energy.demand_ediesel = (
            p_operation_heat.demand_ediesel
            + p_operation_elec_elcon.demand_ediesel
            + p_elec_heatpump.demand_ediesel
            + p_operation_vehicles.demand_ediesel
        )
        s_diesel.energy = p_operation_vehicles.demand_ediesel
        p_other_energy.demand_epetrol = (
            p_operation_heat.demand_epetrol
            + p_operation_elec_elcon.demand_epetrol
            + p_elec_heatpump.demand_epetrol
            + p_operation_vehicles.demand_epetrol
        )
        p.demand_emplo_new = p_operation.demand_emplo_new
        p_operation.demand_emplo = p_operation_heat.demand_emplo
        p_operation.demand_emplo_new = p_operation_heat.demand_emplo_new
        p_operation.demand_emethan = p_operation_heat.demand_emethan
        p_operation.demand_ediesel = p_operation_vehicles.demand_ediesel
        p_operation.demand_epetrol = p_operation_vehicles.demand_epetrol
        p_operation.demand_electricity = (
            p_operation_elec_elcon.demand_electricity
            + p_operation_elec_heatpump.demand_electricity
        )
        p.demand_emplo = p_operation.demand_emplo
        s_petrol.energy = p_operation_vehicles.demand_epetrol
        s_fueloil.energy = 0
        s_petrol.CO2e_cb = s_petrol.energy * s_petrol.CO2e_cb_per_MWh
        s_diesel.CO2e_cb_per_MWh = a18.s_diesel.CO2e_cb_per_MWh
        s_diesel.CO2e_cb = s_diesel.energy * s_diesel.CO2e_cb_per_MWh
        s_fueloil.CO2e_cb_per_MWh = a18.s_fueloil.CO2e_cb_per_MWh
        s.CO2e_total_2021_estimated = a18.s.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_fueloil.CO2e_cb = s_fueloil.energy * s_fueloil.CO2e_cb_per_MWh
        s_petrol.demand_epetrol = s_petrol.energy
        s_gas.energy = 0
        s_emethan.energy = (
            p_operation_heat.energy - s_biomass.energy - s_heatpump.energy
        )
        s_lpg.CO2e_cb_per_MWh = a18.s_lpg.CO2e_cb_per_MWh
        s_lpg.CO2e_cb = s_lpg.energy * s_lpg.CO2e_cb_per_MWh
        s_petrol.CO2e_total = s_petrol.CO2e_pb + s_petrol.CO2e_cb
        s_petrol.change_CO2e_t = s_petrol.CO2e_total - a18.s_petrol.CO2e_total
        s_petrol.change_CO2e_pct = s_petrol.change_CO2e_t / a18.s_petrol.CO2e_total
        s_petrol.CO2e_total_2021_estimated = a18.s_petrol.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_petrol.cost_climate_saved = (
            (s_petrol.CO2e_total_2021_estimated - s_petrol.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_diesel.demand_ediesel = s_diesel.energy
        a.demand_ediesel = s_diesel.demand_ediesel

        s_heatpump.emplo_existing = (
            fact("Fact_B_P_install_heating_emplo_2017")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
            * ass("Ass_B_D_install_heating_emplo_pct_of_A_heatpump")
        )
        s_heatpump.demand_emplo_new = max(
            0, s_heatpump.demand_emplo - s_heatpump.emplo_existing
        )
        s.demand_emplo_new = s_heatpump.demand_emplo_new
        a.demand_emplo_new = (
            g.demand_emplo_new + p.demand_emplo_new + s.demand_emplo_new
        )
        a.demand_emplo = g.demand_emplo + p.demand_emplo + s.demand_emplo
        p_other_energy.demand_electricity = (
            p_operation_heat.demand_electricity
            + p_operation_elec_elcon.demand_electricity
            + p_elec_heatpump.demand_electricity
            + p_operation_vehicles.demand_electricity
        )
        s_gas.CO2e_cb_per_MWh = a18.s_gas.CO2e_cb_per_MWh
        s_gas.CO2e_cb = s_gas.energy * s_gas.CO2e_cb_per_MWh
        s_diesel.CO2e_total = s_diesel.CO2e_pb + s_diesel.CO2e_cb
        s_diesel.change_CO2e_t = s_diesel.CO2e_total - a18.s_diesel.CO2e_total
        s_diesel.change_CO2e_pct = s_diesel.change_CO2e_t / a18.s_diesel.CO2e_total
        s_diesel.CO2e_total_2021_estimated = a18.s_diesel.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_diesel.cost_climate_saved = (
            (s_diesel.CO2e_total_2021_estimated - s_diesel.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_elec.energy = p_other_energy.demand_electricity
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
        s_biomass.CO2e_cb_per_MWh = a18.s_biomass.CO2e_cb_per_MWh
        s_biomass.CO2e_cb = s_biomass.energy * s_biomass.CO2e_cb_per_MWh
        s_fueloil.CO2e_total = s_fueloil.CO2e_pb + s_fueloil.CO2e_cb
        s_fueloil.change_CO2e_t = s_fueloil.CO2e_total - a18.s_fueloil.CO2e_total
        s_fueloil.change_CO2e_pct = s_fueloil.change_CO2e_t / a18.s_fueloil.CO2e_total
        s_fueloil.CO2e_total_2021_estimated = a18.s_fueloil.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_fueloil.cost_climate_saved = (
            (s_fueloil.CO2e_total_2021_estimated - s_fueloil.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_gas.pct_energy = s_gas.energy / s.energy
        s_elec.CO2e_cb_per_MWh = a18.s_elec.CO2e_cb_per_MWh
        s_elec.CO2e_cb = s_elec.energy * s_elec.CO2e_cb_per_MWh
        s_lpg.CO2e_total = s_lpg.CO2e_pb + s_lpg.CO2e_cb
        s_lpg.change_CO2e_t = s_lpg.CO2e_total - a18.s_lpg.CO2e_total
        s_lpg.change_CO2e_pct = s_lpg.change_CO2e_t / a18.s_lpg.CO2e_total
        s_lpg.CO2e_total_2021_estimated = a18.s_lpg.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_lpg.cost_climate_saved = (
            (s_lpg.CO2e_total_2021_estimated - s_lpg.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_lpg.pct_energy = s_lpg.energy / s.energy
        s_emethan.pct_energy = s_gas.energy / s.energy
        s_heatpump.CO2e_cb_per_MWh = a18.s_heatpump.CO2e_cb_per_MWh
        s_heatpump.CO2e_cb = s_heatpump.energy * s_heatpump.CO2e_cb_per_MWh
        s_gas.CO2e_total = s_gas.CO2e_pb + s_gas.CO2e_cb
        s_gas.change_CO2e_t = s_gas.CO2e_total - a18.s_gas.CO2e_total
        s_gas.change_CO2e_pct = s_gas.change_CO2e_t / a18.s_gas.CO2e_total
        s_gas.CO2e_total_2021_estimated = a18.s_gas.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_gas.cost_climate_saved = (
            (s_gas.CO2e_total_2021_estimated - s_gas.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_emethan.demand_emethan = s_emethan.energy
        s_diesel.pct_energy = s_diesel.energy / s.energy
        s_biomass.pct_energy = s_biomass.energy / s.energy
        s_biomass.demand_biomass = s_biomass.energy
        p_other_energy.demand_emethan = (
            p_operation_heat.demand_emethan
            + p_operation_elec_elcon.demand_emethan
            + p_elec_heatpump.demand_emethan
            + p_operation_vehicles.demand_emethan
        )
        s_elec.pct_energy = s_elec.energy / s.energy
        s.CO2e_cb = (
            s_petrol.CO2e_cb
            + s_diesel.CO2e_cb
            + s_fueloil.CO2e_cb
            + s_lpg.CO2e_cb
            + s_gas.CO2e_cb
            + s_emethan.CO2e_cb
            + s_biomass.CO2e_cb
            + s_elec.CO2e_cb
            + s_heatpump.CO2e_cb
        )
        s.CO2e_total = s.CO2e_pb + s.CO2e_cb
        s_biomass.CO2e_total = s_biomass.CO2e_pb + s_biomass.CO2e_cb
        s_biomass.change_CO2e_t = s_biomass.CO2e_total - a18.s_biomass.CO2e_total
        s_biomass.change_CO2e_pct = s_biomass.change_CO2e_t / a18.s_biomass.CO2e_total
        s_biomass.CO2e_total_2021_estimated = a18.s_biomass.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_biomass.cost_climate_saved = (
            (s_biomass.CO2e_total_2021_estimated - s_biomass.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_elec.demand_electricity = s_elec.energy
        s_petrol.pct_energy = s_petrol.energy / s.energy
        s_heatpump.pct_energy = s_heatpump.energy / s.energy
        s.cost_climate_saved = (
            (s.CO2e_total_2021_estimated - s.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s.change_CO2e_t = s.CO2e_total - a18.s.CO2e_total
        s_elec.CO2e_total = s_elec.CO2e_pb + s_elec.CO2e_cb
        s_elec.change_CO2e_t = s_elec.CO2e_total - a18.s_elec.CO2e_total
        s_elec.change_CO2e_pct = s_elec.change_CO2e_t / 1  # a18.s_elec.CO2e_total)
        s_elec.CO2e_total_2021_estimated = a18.s_elec.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_elec.cost_climate_saved = (
            (s_elec.CO2e_total_2021_estimated - s_elec.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_heatpump.demand_heatpump = s_heatpump.energy
        s_fueloil.pct_energy = s_fueloil.energy / s.energy
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
        s_heatpump.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")
        s_heatpump.cost_fuel = (
            s_heatpump.energy * s_heatpump.cost_fuel_per_MWh / Million
        )
        a.CO2e_total = g.CO2e_total + p.CO2e_total + s.CO2e_total
        s.change_CO2e_pct = s.change_CO2e_t / a18.s.CO2e_total
        s_heatpump.CO2e_total = s_heatpump.CO2e_pb + s_heatpump.CO2e_cb
        s_heatpump.change_energy_MWh = s_heatpump.energy - a18.s_heatpump.energy
        s_heatpump.change_CO2e_t = s_heatpump.CO2e_total - a18.s_heatpump.CO2e_total
        s_heatpump.change_CO2e_pct = (
            s_heatpump.change_CO2e_t / 1.0
        )  # a18.s_heatpump.CO2e_total)
        s_heatpump.CO2e_total_2021_estimated = a18.s_heatpump.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_heatpump.cost_climate_saved = (
            (s_heatpump.CO2e_total_2021_estimated - s_heatpump.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_heatpump.change_cost_energy = s_heatpump.cost_fuel - s_heatpump.cost_fuel
        s_heatpump.invest_per_x = fact("Fact_R_S_heatpump_cost")
        s_heatpump.full_load_hour = fact("Fact_B_S_full_usage_hours_buildings")
        s_heatpump.pct_of_wage = fact(
            "Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017"
        )
        s_heatpump.power_installed = a18.s_heatpump.energy / s_heatpump.full_load_hour
        s_heatpump.ratio_wage_to_emplo = fact(
            "Fact_B_P_heating_wage_per_person_per_year"
        )
        s_heatpump.power_to_be_installed = max(
            s_heatpump.energy / s_heatpump.full_load_hour - s_heatpump.power_installed,
            0,
        )
        s_heatpump.invest = (
            s_heatpump.invest_per_x * s_heatpump.power_to_be_installed * 1000
        )
        s_heatpump.invest_pa = s_heatpump.invest / entry("In_M_duration_target")
        s_heatpump.cost_wage = s_heatpump.invest_pa * s_heatpump.pct_of_wage
        s_heatpump.demand_emplo = s_heatpump.cost_wage / s_heatpump.ratio_wage_to_emplo

        a.CO2e_pb = p.CO2e_pb
        a.CO2e_cb = s.CO2e_cb
        a.change_energy_MWh = p_operation.change_energy_MWh
        a.change_energy_pct = p_operation.change_energy_pct
        a.change_CO2e_t = a.CO2e_total - a18.a.CO2e_total
        a.change_CO2e_pct = a.change_CO2e_t / a18.a.CO2e_total
        a.CO2e_total_2021_estimated = a18.a.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        a.cost_climate_saved = (
            (a.CO2e_total_2021_estimated - a.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        a.invest_pa = g.invest_pa
        a.invest_pa_com = g.invest_pa_com
        a.invest = g.invest
        a.invest_com = g.invest_com
        g.invest_pa = g_consult.invest_pa + g_organic.invest_pa
        g.invest_pa_com = g_consult.invest_pa_com
        g.invest = g_consult.invest + g_organic.invest
        g.invest_com = g_consult.invest_com
        g_organic.invest_pa = g_organic.invest / entry("In_M_duration_target")
        g_organic.invest = g_organic.power_to_be_installed * g_organic.invest_per_x
        g_organic.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        g_organic.cost_wage = g_organic.invest_pa * g_organic.pct_of_wage
        g_organic.ratio_wage_to_emplo = fact(
            "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
        )
        g_organic.demand_emplo = g_organic.cost_wage / g_organic.ratio_wage_to_emplo
        g_organic.invest_per_x = ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
        g_organic.power_to_be_installed = g_organic.area_ha_available * (
            g_organic.power_to_be_installed_pct - g_organic.power_installed
        )
        g_organic.power_installed = entry("In_A_area_agri_com_pct_of_organic")
        g_organic.power_to_be_installed_pct = ass(
            "Ass_A_G_area_agri_pct_of_organic_2050"
        )
        g_organic.area_ha_available = entry("In_M_area_agri_com")
        p.energy = p_operation.energy
        p.CO2e_pb = (
            p_fermen.CO2e_pb + p_manure.CO2e_pb + p_soil.CO2e_pb + p_other.CO2e_pb
        )
        p_operation.demand_biomass = p_operation_heat.demand_biomass
        p_operation.demand_heatpump = p_operation_heat.demand_heatpump
        p_operation.energy = (
            p_operation_heat.energy
            + p_operation_elec_elcon.energy
            + p_operation_elec_heatpump.energy
            + p_operation_vehicles.energy
        )
        p_operation.change_energy_MWh = p_operation.energy - a18.p_operation.energy
        p_operation.change_energy_pct = (
            p_operation.change_energy_MWh / a18.p_operation.energy
        )
        p_operation_elec_elcon.change_energy_MWh = (
            p_operation_elec_elcon.energy - a18.p_operation_elec_elcon.energy
        )
        p_operation_elec_elcon.change_energy_pct = (
            p_operation_elec_elcon.change_energy_MWh / a18.p_operation_elec_elcon.energy
        )
        p_operation_elec_heatpump.demand_electricity = p_operation_elec_heatpump.energy
        p_operation_elec_heatpump.energy = s_heatpump.energy / fact(
            "Fact_R_S_heatpump_mean_annual_performance_factor_all"
        )
        a18.p_operation_elec_heatpump.energy = 0
        p_operation_elec_heatpump.change_energy_MWh = (
            p_operation_elec_heatpump.energy - a18.p_operation_elec_heatpump.energy
        )
        p_operation_vehicles.change_energy_MWh = (
            p_operation_vehicles.energy - a18.p_operation_vehicles.energy
        )
        p_operation_vehicles.change_energy_pct = (
            p_operation_vehicles.change_energy_MWh / a18.p_operation_vehicles.energy
        )
        s.change_energy_MWh = s.energy - a18.s.energy
        s.change_energy_pct = s.change_energy_MWh / a18.s.energy
        s_petrol.change_energy_MWh = s_petrol.energy - a18.s_petrol.energy
        s_petrol.change_energy_pct = s_petrol.change_energy_MWh / a18.s_petrol.energy
        s_diesel.change_energy_MWh = s_diesel.energy - a18.s_diesel.energy
        s_diesel.change_energy_pct = s_diesel.change_energy_MWh / a18.s_diesel.energy
        s_fueloil.change_energy_MWh = s_fueloil.energy - a18.s_fueloil.energy
        s_lpg.change_energy_MWh = s_lpg.energy - a18.s_lpg.energy
        s_gas.change_energy_MWh = s_gas.energy - a18.s_gas.energy
        s_emethan.CO2e_cb_per_MWh = fact("Fact_T_S_methan_EmFa_tank_wheel_2018")
        s_biomass.change_energy_MWh = s_biomass.energy - a18.s_biomass.energy
        s_biomass.change_energy_pct = s_biomass.change_energy_MWh / a18.s_biomass.energy
        s_elec.change_energy_MWh = s_elec.energy - a18.s_elec.energy
        s_elec.change_energy_pct = s_elec.change_energy_MWh / a18.s_elec.energy
        s.demand_emplo = s_heatpump.demand_emplo
