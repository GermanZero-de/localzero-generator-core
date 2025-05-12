# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class Entries:
    a_area_agri_com_pct_of_organic: float
    a_biomass_fec: float
    a_diesel_fec: float
    a_elec_fec: float
    a_farm_amount: float
    a_fermen_dairycow_amount: float
    a_fermen_nondairy_amount: float
    a_fermen_oanimal_amount: float
    a_fermen_pig_amount: float
    a_fermen_poultry_amount: float
    a_fueloil_fec: float
    a_gas_fec: float
    a_lpg_fec: float
    a_manure_dairycow_ratio_CO2e_to_amount: float
    a_manure_deposition_ratio_CO2e_to_amount: float
    a_manure_nondairy_ratio_CO2e_to_amount: float
    a_manure_oanimal_ratio_CO2e_to_amount: float
    a_manure_poultry_ratio_CO2e_to_amount: float
    a_manure_swine_ratio_CO2e_to_amount: float
    a_other_ecrop_prod_volume: float
    a_other_kas_prod_volume: float
    a_other_liming_calcit_prod_volume: float
    a_other_liming_dolomite_prod_volume: float
    a_other_urea_prod_volume: float
    a_petrol_fec: float
    a_soil_crazing_ratio_CO2e_to_ha: float
    a_soil_deposition_ratio_CO2e_to_ha: float
    a_soil_ecrop_ratio_CO2e_to_ha: float
    a_soil_fertilizer_ratio_CO2e_to_ha: float
    a_soil_leaching_ratio_CO2e_to_ha: float
    a_soil_manure_ratio_CO2e_to_ha: float
    a_soil_orgfarm_ratio_CO2e_to_ha: float
    a_soil_orgloss_ratio_CO2e_to_ha: float
    a_soil_residue_ratio_CO2e_to_ha: float
    a_soil_sludge_ratio_CO2e_to_ha: float
    b_biomass_fec: float
    b_coal_fec: float
    b_diesel_fec: float
    b_elec_fec: float
    b_fueloil_fec: float
    b_gas_fec: float
    b_heatnet_fec: float
    b_jetfuel_fec: float
    b_lpg_fec: float
    b_orenew_fec: float
    b_petrol_fec: float
    e_local_wind_onshore_ratio_power_to_area_sta: float
    e_biomass_local_power_installable_sta: float
    e_PV_power_inst_agripv: float
    e_PV_power_inst_biomass: float
    e_PV_power_inst_facade: float
    e_PV_power_inst_park: float
    e_PV_power_inst_roof: float
    e_PV_power_inst_water: float
    e_PV_power_inst_wind_on: float
    e_PV_power_to_be_inst_agri: float
    e_PV_power_to_be_inst_facade: float
    e_PV_power_to_be_inst_local_biomass: float
    e_PV_power_to_be_inst_local_wind_onshore: float
    e_PV_power_to_be_inst_park: float
    e_PV_power_to_be_inst_roof: float
    e_pv_full_load_hours_sta: float
    h_solartherm_to_be_inst: float
    i_dehst_miner_cement: float
    i_dehst_miner_chalk: float
    i_dehst_miner_glas: float
    i_dehst_miner_ceram: float
    i_dehst_chem_basic: float
    i_dehst_chem_ammonia: float
    i_dehst_chem_other: float
    i_dehst_metal_steel_primary: float
    i_dehst_metal_steel_secondary: float
    i_dehst_metal_nonfe: float
    i_dehst_other_paper: float
    i_dehst_other_food: float
    i_dehst_other_further: float
    m_AGS_com: str
    m_AGS_dis: str
    m_AGS_sta: str
    m_GHG_budget_2016_to_year_target: float
    m_area_agri_com: int
    m_area_agri_nat: int
    m_area_agri_sta: int
    m_area_industry_com: float
    m_area_industry_nat: float
    m_area_settlement_com: float
    m_area_total_com: int
    m_area_total_dis: int
    m_area_total_nat: int
    m_area_total_sta: int
    m_area_transport_com: float
    m_area_veg_grove_com: float
    m_area_veg_heath_com: float
    m_area_veg_marsh_com: float
    m_area_veg_moor_com: float
    m_area_veg_plant_uncover_com: float
    m_area_veg_wood_com: float
    m_area_water_com: float
    m_area_wood_com: float
    m_duration_neutral: float  # duration of CO2 neutrality in years until 2050
    m_duration_target: int  # duration from baseline until target year
    m_nonCO2_budget_2016_to_year_target: float
    m_population_com_2018: int  # population of commune in 2018
    m_population_com_203X: int
    m_population_dis: int  # population of district in 2018
    m_population_nat: int  # population of germany in 2018
    m_population_sta: int  # population of state in 2018
    m_year_target: int  # see years.py
    m_year_baseline: int  # see years.py
    m_year_ref: int  # see years.py (i.e RefData.year_ref() )
    r_area_m2: float
    r_area_m2_1flat: float
    r_area_m2_2flat: float
    r_area_m2_3flat: float
    r_area_m2_dorm: float
    r_biomass_fec: float
    r_buildings_1919_1948: float
    r_buildings_1949_1978: float
    r_buildings_1979_1986: float
    r_buildings_1987_1990: float
    r_buildings_1991_1995: float
    r_buildings_1996_2000: float
    r_buildings_2001_2004: float
    r_buildings_2005_2008: float
    r_buildings_2009_2011: float
    r_buildings_2011_today: float
    r_buildings_com: float
    r_buildings_ge_3_apts: float
    r_buildings_le_2_apts: float
    r_buildings_nat: float
    r_buildings_until_1919: float
    r_coal_fec: float
    r_elec_fec: float
    r_energy_total: float
    r_flats_com: float
    r_flats_w_heatnet: float
    r_flats_wo_heatnet: float
    r_fueloil_fec: float
    r_gas_fec: float
    r_heatnet_fec: float
    r_heatnet_ratio_year_target: float
    r_lpg_fec: float
    r_orenew_fec: float
    r_pct_of_area_m2_com: float
    r_petrol_fec: float
    r_rehab_rate_pa: float
    t_bus_mega_km_dis: float
    t_ec_rail_gds_diesel: float
    t_ec_rail_gds_elec: float
    t_ec_rail_ppl_diesel: float
    t_ec_rail_ppl_elec: float
    t_metro_mega_km_dis: float
    t_mil_car_ab: float
    t_mil_car_it_ot: float
    t_mil_ldt_ab: float
    t_mil_ldt_it_ot: float
    t_mil_mhd_ab: float
    t_mil_mhd_it_ot: float
    t_rt3: str
    t_rt7: str
    t_a_eev_kerosene_overseas_total: float
    t_a_conveyance_capa_inland_pkm_com: float
    t_a_transport_capa_inland_tkm_com: float
    t_a_flight_kilometer_inland_km_com: float
    t_a_eev_kerosene_inland_com: float
    t_a_eev_petrol_inland_com: float
    t_a_ghg_inland_com: float
    t_a_conveyance_capa_overseas_pkm_com: float
    t_a_transport_capa_overseas_tkm_com: float
    t_a_flight_kilometer_overseas_km_com: float
    t_a_eev_kerosene_overseas_com: float
    t_a_ghg_overseas_com: float
    t_a_sum_ghg_com: float
    t_s_eev_diesel_inland_mwh_total: float
    t_s_eev_fuel_overseas_mwh_total: float
    t_s_eev_diesel_inland_mwh_com: float
    t_s_eev_fuel_overseas_mwh_com: float
    t_s_ghg_inland_com: float
    t_s_ghg_overseas_com: float
    t_s_ghg_sum_com: float
    w_elec_fec: float
    ags: str

    def assert_is_valid(self):
        """Checks that the numeric values are not negative"""

        assert (
            self.a_area_agri_com_pct_of_organic >= 0
        ), "Entry a_area_agri_com_pct_of_organic should be 0 or positive"
        assert self.a_biomass_fec >= 0, "Entry a_biomass_fec should be 0 or positive"
        assert self.a_diesel_fec >= 0, "Entry a_diesel_fec should be 0 or positive"
        assert self.a_elec_fec >= 0, "Entry a_elec_fec should be 0 or positive"
        assert self.a_farm_amount >= 0, "Entry a_farm_amount should be 0 or positive"
        assert (
            self.a_fermen_dairycow_amount >= 0
        ), "Entry a_fermen_dairycow_amount should be 0 or positive"
        assert (
            self.a_fermen_nondairy_amount >= 0
        ), "Entry a_fermen_nondairy_amount should be 0 or positive"
        assert (
            self.a_fermen_oanimal_amount >= 0
        ), "Entry a_fermen_oanimal_amount should be 0 or positive"
        assert (
            self.a_fermen_pig_amount >= 0
        ), "Entry a_fermen_pig_amount should be 0 or positive"
        assert (
            self.a_fermen_poultry_amount >= 0
        ), "Entry a_fermen_poultry_amount should be 0 or positive"
        assert self.a_fueloil_fec >= 0, "Entry a_fueloil_fec should be 0 or positive"
        assert self.a_gas_fec >= 0, "Entry a_gas_fec should be 0 or positive"
        assert self.a_lpg_fec >= 0, "Entry a_lpg_fec should be 0 or positive"
        assert (
            self.a_manure_dairycow_ratio_CO2e_to_amount >= 0
        ), "Entry a_manure_dairycow_ratio_CO2e_to_amount should be 0 or positive"
        assert (
            self.a_manure_deposition_ratio_CO2e_to_amount >= 0
        ), "Entry a_manure_deposition_ratio_CO2e_to_amount should be 0 or positive"
        assert (
            self.a_manure_nondairy_ratio_CO2e_to_amount >= 0
        ), "Entry a_manure_nondairy_ratio_CO2e_to_amount should be 0 or positive"
        assert (
            self.a_manure_oanimal_ratio_CO2e_to_amount >= 0
        ), "Entry a_manure_oanimal_ratio_CO2e_to_amount should be 0 or positive"
        assert (
            self.a_manure_poultry_ratio_CO2e_to_amount >= 0
        ), "Entry a_manure_poultry_ratio_CO2e_to_amount should be 0 or positive"
        assert (
            self.a_manure_swine_ratio_CO2e_to_amount >= 0
        ), "Entry a_manure_swine_ratio_CO2e_to_amount should be 0 or positive"
        assert (
            self.a_other_ecrop_prod_volume >= 0
        ), "Entry a_other_ecrop_prod_volume should be 0 or positive"
        assert (
            self.a_other_kas_prod_volume >= 0
        ), "Entry a_other_kas_prod_volume should be 0 or positive"
        assert (
            self.a_other_liming_calcit_prod_volume >= 0
        ), "Entry a_other_liming_calcit_prod_volume should be 0 or positive"
        assert (
            self.a_other_liming_dolomite_prod_volume >= 0
        ), "Entry a_other_liming_dolomite_prod_volume should be 0 or positive"
        assert (
            self.a_other_urea_prod_volume >= 0
        ), "Entry a_other_urea_prod_volume should be 0 or positive"
        assert self.a_petrol_fec >= 0, "Entry a_petrol_fec should be 0 or positive"
        assert (
            self.a_soil_crazing_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_crazing_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_deposition_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_deposition_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_ecrop_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_ecrop_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_fertilizer_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_fertilizer_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_leaching_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_leaching_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_manure_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_manure_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_orgfarm_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_orgfarm_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_orgloss_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_orgloss_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_residue_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_residue_ratio_CO2e_to_ha should be 0 or positive"
        assert (
            self.a_soil_sludge_ratio_CO2e_to_ha >= 0
        ), "Entry a_soil_sludge_ratio_CO2e_to_ha should be 0 or positive"
        assert self.b_biomass_fec >= 0, "Entry b_biomass_fec should be 0 or positive"
        assert self.b_coal_fec >= 0, "Entry b_coal_fec should be 0 or positive"
        assert self.b_diesel_fec >= 0, "Entry b_diesel_fec should be 0 or positive"
        assert self.b_elec_fec >= 0, "Entry b_elec_fec should be 0 or positive"
        assert self.b_fueloil_fec >= 0, "Entry b_fueloil_fec should be 0 or positive"
        assert self.b_gas_fec >= 0, "Entry b_gas_fec should be 0 or positive"
        assert self.b_heatnet_fec >= 0, "Entry b_heatnet_fec should be 0 or positive"
        assert self.b_jetfuel_fec >= 0, "Entry b_jetfuel_fec should be 0 or positive"
        assert self.b_lpg_fec >= 0, "Entry b_lpg_fec should be 0 or positive"
        assert self.b_orenew_fec >= 0, "Entry b_orenew_fec should be 0 or positive"
        assert self.b_petrol_fec >= 0, "Entry b_petrol_fec should be 0 or positive"
        assert (
            self.e_local_wind_onshore_ratio_power_to_area_sta >= 0
        ), "Entry e_local_wind_onshore_ratio_power_to_area_sta should be 0 or positive"
        assert (
            self.e_biomass_local_power_installable_sta >= 0
        ), "Entry e_biomass_local_power_installable_sta should be 0 or positive"
        assert (
            self.e_PV_power_inst_agripv >= 0
        ), "Entry e_PV_power_inst_agripv should be 0 or positive"
        assert (
            self.e_PV_power_inst_biomass >= 0
        ), "Entry e_PV_power_inst_biomass should be 0 or positive"
        assert (
            self.e_PV_power_inst_facade >= 0
        ), "Entry e_PV_power_inst_facade should be 0 or positive"
        assert (
            self.e_PV_power_inst_park >= 0
        ), "Entry e_PV_power_inst_park should be 0 or positive"
        assert (
            self.e_PV_power_inst_roof >= 0
        ), "Entry e_PV_power_inst_roof should be 0 or positive"
        assert (
            self.e_PV_power_inst_water >= 0
        ), "Entry e_PV_power_inst_water should be 0 or positive"
        assert (
            self.e_PV_power_inst_wind_on >= 0
        ), "Entry e_PV_power_inst_wind_on should be 0 or positive"
        assert (
            self.e_PV_power_to_be_inst_agri >= 0
        ), "Entry e_PV_power_to_be_inst_agri should be 0 or positive"
        assert (
            self.e_PV_power_to_be_inst_facade >= 0
        ), "Entry e_PV_power_to_be_inst_facade should be 0 or positive"
        assert (
            self.e_PV_power_to_be_inst_local_biomass >= 0
        ), "Entry e_PV_power_to_be_inst_local_biomass should be 0 or positive"
        assert (
            self.e_PV_power_to_be_inst_local_wind_onshore >= 0
        ), "Entry e_PV_power_to_be_inst_local_wind_onshore should be 0 or positive"
        assert (
            self.e_PV_power_to_be_inst_park >= 0
        ), "Entry e_PV_power_to_be_inst_park should be 0 or positive"
        assert (
            self.e_PV_power_to_be_inst_roof >= 0
        ), "Entry e_PV_power_to_be_inst_roof should be 0 or positive"
        assert (
            self.e_pv_full_load_hours_sta >= 0
        ), "Entry e_pv_full_load_hours_sta should be 0 or positive"
        assert (
            self.h_solartherm_to_be_inst >= 0
        ), "Entry h_solartherm_to_be_inst should be 0 or positive"
        assert (
            self.i_dehst_miner_cement >= 0
        ), "Entry i_dehst_miner_cement should be 0 or positive"
        assert (
            self.i_dehst_miner_chalk >= 0
        ), "Entry i_dehst_miner_chalk should be 0 or positive"
        assert (
            self.i_dehst_miner_glas >= 0
        ), "Entry i_dehst_miner_glas should be 0 or positive"
        assert (
            self.i_dehst_miner_ceram >= 0
        ), "Entry i_dehst_miner_ceram should be 0 or positive"
        assert (
            self.i_dehst_chem_basic >= 0
        ), "Entry i_dehst_chem_basic should be 0 or positive"
        assert (
            self.i_dehst_chem_ammonia >= 0
        ), "Entry i_dehst_chem_ammonia should be 0 or positive"
        assert (
            self.i_dehst_chem_other >= 0
        ), "Entry i_dehst_chem_other should be 0 or positive"
        assert (
            self.i_dehst_metal_steel_primary >= 0
        ), "Entry i_dehst_metal_steel_primary should be 0 or positive"
        assert (
            self.i_dehst_metal_steel_secondary >= 0
        ), "Entry i_dehst_metal_steel_secondary should be 0 or positive"
        assert (
            self.i_dehst_metal_nonfe >= 0
        ), "Entry i_dehst_metal_nonfe should be 0 or positive"
        assert (
            self.i_dehst_other_paper >= 0
        ), "Entry i_dehst_other_paper should be 0 or positive"
        assert (
            self.i_dehst_other_food >= 0
        ), "Entry i_dehst_other_food should be 0 or positive"
        assert (
            self.i_dehst_other_further >= 0
        ), "Entry i_dehst_other_further should be 0 or positive"
        assert (
            self.m_GHG_budget_2016_to_year_target >= 0
        ), "Entry m_GHG_budget_2016_to_year_target should be 0 or positive"
        assert (
            self.m_area_agri_com >= 0
        ), "Entry m_area_agri_com should be 0 or positive"
        assert (
            self.m_area_agri_nat >= 0
        ), "Entry m_area_agri_nat should be 0 or positive"
        assert (
            self.m_area_agri_sta >= 0
        ), "Entry m_area_agri_sta should be 0 or positive"
        assert (
            self.m_area_industry_com >= 0
        ), "Entry m_area_industry_com should be 0 or positive"
        assert (
            self.m_area_industry_nat >= 0
        ), "Entry m_area_industry_nat should be 0 or positive"
        assert (
            self.m_area_settlement_com >= 0
        ), "Entry m_area_settlement_com should be 0 or positive"
        assert (
            self.m_area_total_com >= 0
        ), "Entry m_area_total_com should be 0 or positive"
        assert (
            self.m_area_total_dis >= 0
        ), "Entry m_area_total_dis should be 0 or positive"
        assert (
            self.m_area_total_nat >= 0
        ), "Entry m_area_total_nat should be 0 or positive"
        assert (
            self.m_area_total_sta >= 0
        ), "Entry m_area_total_sta should be 0 or positive"
        assert (
            self.m_area_transport_com >= 0
        ), "Entry m_area_transport_com should be 0 or positive"
        assert (
            self.m_area_veg_grove_com >= 0
        ), "Entry m_area_veg_grove_com should be 0 or positive"
        assert (
            self.m_area_veg_heath_com >= 0
        ), "Entry m_area_veg_heath_com should be 0 or positive"
        assert (
            self.m_area_veg_marsh_com >= 0
        ), "Entry m_area_veg_marsh_com should be 0 or positive"
        assert (
            self.m_area_veg_moor_com >= 0
        ), "Entry m_area_veg_moor_com should be 0 or positive"
        assert (
            self.m_area_veg_plant_uncover_com >= 0
        ), "Entry m_area_veg_plant_uncover_com should be 0 or positive"
        assert (
            self.m_area_veg_wood_com >= 0
        ), "Entry m_area_veg_wood_com should be 0 or positive"
        assert (
            self.m_area_water_com >= 0
        ), "Entry m_area_water_com should be 0 or positive"
        assert (
            self.m_area_wood_com >= 0
        ), "Entry m_area_wood_com should be 0 or positive"
        assert (
            self.m_duration_neutral >= 0
        ), "Entry m_duration_neutral should be 0 or positive"
        assert (
            self.m_duration_target >= 0
        ), "Entry m_duration_target should be 0 or positive"
        assert (
            self.m_nonCO2_budget_2016_to_year_target >= 0
        ), "Entry m_nonCO2_budget_2016_to_year_target should be 0 or positive"
        assert (
            self.m_population_com_2018 >= 0
        ), "Entry m_population_com_2018 should be 0 or positive"
        assert (
            self.m_population_com_203X >= 0
        ), "Entry m_population_com_203X should be 0 or positive"
        assert (
            self.m_population_dis >= 0
        ), "Entry m_population_dis should be 0 or positive"
        assert (
            self.m_population_nat >= 0
        ), "Entry m_population_nat should be 0 or positive"
        assert (
            self.m_population_sta >= 0
        ), "Entry m_population_sta should be 0 or positive"
        assert self.m_year_target >= 0, "Entry m_year_target should be 0 or positive"
        assert (
            self.m_year_baseline >= 0
        ), "Entry m_year_baseline should be 0 or positive"
        assert self.m_year_ref >= 0, "Entry m_year_ref should be 0 or positive"
        assert self.r_area_m2 >= 0, "Entry r_area_m2 should be 0 or positive"
        assert (
            self.r_area_m2_1flat >= 0
        ), "Entry r_area_m2_1flat should be 0 or positive"
        assert (
            self.r_area_m2_2flat >= 0
        ), "Entry r_area_m2_2flat should be 0 or positive"
        assert (
            self.r_area_m2_3flat >= 0
        ), "Entry r_area_m2_3flat should be 0 or positive"
        assert self.r_area_m2_dorm >= 0, "Entry r_area_m2_dorm should be 0 or positive"
        assert self.r_biomass_fec >= 0, "Entry r_biomass_fec should be 0 or positive"
        assert (
            self.r_buildings_1919_1948 >= 0
        ), "Entry r_buildings_1919_1948 should be 0 or positive"
        assert (
            self.r_buildings_1949_1978 >= 0
        ), "Entry r_buildings_1949_1978 should be 0 or positive"
        assert (
            self.r_buildings_1979_1986 >= 0
        ), "Entry r_buildings_1979_1986 should be 0 or positive"
        assert (
            self.r_buildings_1987_1990 >= 0
        ), "Entry r_buildings_1987_1990 should be 0 or positive"
        assert (
            self.r_buildings_1991_1995 >= 0
        ), "Entry r_buildings_1991_1995 should be 0 or positive"
        assert (
            self.r_buildings_1996_2000 >= 0
        ), "Entry r_buildings_1996_2000 should be 0 or positive"
        assert (
            self.r_buildings_2001_2004 >= 0
        ), "Entry r_buildings_2001_2004 should be 0 or positive"
        assert (
            self.r_buildings_2005_2008 >= 0
        ), "Entry r_buildings_2005_2008 should be 0 or positive"
        assert (
            self.r_buildings_2009_2011 >= 0
        ), "Entry r_buildings_2009_2011 should be 0 or positive"
        assert (
            self.r_buildings_2011_today >= 0
        ), "Entry r_buildings_2011_today should be 0 or positive"
        assert (
            self.r_buildings_com >= 0
        ), "Entry r_buildings_com should be 0 or positive"
        assert (
            self.r_buildings_ge_3_apts >= 0
        ), "Entry r_buildings_ge_3_apts should be 0 or positive"
        assert (
            self.r_buildings_le_2_apts >= 0
        ), "Entry r_buildings_le_2_apts should be 0 or positive"
        assert (
            self.r_buildings_nat >= 0
        ), "Entry r_buildings_nat should be 0 or positive"
        assert (
            self.r_buildings_until_1919 >= 0
        ), "Entry r_buildings_until_1919 should be 0 or positive"
        assert self.r_coal_fec >= 0, "Entry r_coal_fec should be 0 or positive"
        assert self.r_elec_fec >= 0, "Entry r_elec_fec should be 0 or positive"
        assert self.r_energy_total >= 0, "Entry r_energy_total should be 0 or positive"
        assert self.r_flats_com >= 0, "Entry r_flats_com should be 0 or positive"
        assert (
            self.r_flats_w_heatnet >= 0
        ), "Entry r_flats_w_heatnet should be 0 or positive"
        assert (
            self.r_flats_wo_heatnet >= 0
        ), "Entry r_flats_wo_heatnet should be 0 or positive"
        assert self.r_fueloil_fec >= 0, "Entry r_fueloil_fec should be 0 or positive"
        assert self.r_gas_fec >= 0, "Entry r_gas_fec should be 0 or positive"
        assert self.r_heatnet_fec >= 0, "Entry r_heatnet_fec should be 0 or positive"
        assert (
            self.r_heatnet_ratio_year_target >= 0
        ), "Entry r_heatnet_ratio_year_target should be 0 or positive"
        assert self.r_lpg_fec >= 0, "Entry r_lpg_fec should be 0 or positive"
        assert self.r_orenew_fec >= 0, "Entry r_orenew_fec should be 0 or positive"
        assert (
            self.r_pct_of_area_m2_com >= 0
        ), "Entry r_pct_of_area_m2_com should be 0 or positive"
        assert self.r_petrol_fec >= 0, "Entry r_petrol_fec should be 0 or positive"
        assert (
            self.r_rehab_rate_pa >= 0
        ), "Entry r_rehab_rate_pa should be 0 or positive"
        assert (
            self.t_bus_mega_km_dis >= 0
        ), "Entry t_bus_mega_km_dis should be 0 or positive"
        assert (
            self.t_ec_rail_gds_diesel >= 0
        ), "Entry t_ec_rail_gds_diesel should be 0 or positive"
        assert (
            self.t_ec_rail_gds_elec >= 0
        ), "Entry t_ec_rail_gds_elec should be 0 or positive"
        assert (
            self.t_ec_rail_ppl_diesel >= 0
        ), "Entry t_ec_rail_ppl_diesel should be 0 or positive"
        assert (
            self.t_ec_rail_ppl_elec >= 0
        ), "Entry t_ec_rail_ppl_elec should be 0 or positive"
        assert (
            self.t_metro_mega_km_dis >= 0
        ), "Entry t_metro_mega_km_dis should be 0 or positive"
        assert self.t_mil_car_ab >= 0, "Entry t_mil_car_ab should be 0 or positive"
        assert (
            self.t_mil_car_it_ot >= 0
        ), "Entry t_mil_car_it_ot should be 0 or positive"
        assert self.t_mil_ldt_ab >= 0, "Entry t_mil_ldt_ab should be 0 or positive"
        assert (
            self.t_mil_ldt_it_ot >= 0
        ), "Entry t_mil_ldt_it_ot should be 0 or positive"
        assert self.t_mil_mhd_ab >= 0, "Entry t_mil_mhd_ab should be 0 or positive"
        assert (
            self.t_mil_mhd_it_ot >= 0
        ), "Entry t_mil_mhd_it_ot should be 0 or positive"
        assert (
            self.t_a_eev_kerosene_overseas_total >= 0
        ), "Entry t_a_eev_kerosene_overseas_total should be 0 or positive"
        assert (
            self.t_a_conveyance_capa_inland_pkm_com >= 0
        ), "Entry t_a_conveyance_capa_inland_pkm_com should be 0 or positive"
        assert (
            self.t_a_transport_capa_inland_tkm_com >= 0
        ), "Entry t_a_transport_capa_inland_tkm_com should be 0 or positive"
        assert (
            self.t_a_flight_kilometer_inland_km_com >= 0
        ), "Entry t_a_flight_kilometer_inland_km_com should be 0 or positive"
        assert (
            self.t_a_eev_kerosene_inland_com >= 0
        ), "Entry t_a_eev_kerosene_inland_com should be 0 or positive"
        assert (
            self.t_a_eev_petrol_inland_com >= 0
        ), "Entry t_a_eev_petrol_inland_com should be 0 or positive"
        assert (
            self.t_a_ghg_inland_com >= 0
        ), "Entry t_a_ghg_inland_com should be 0 or positive"
        assert (
            self.t_a_conveyance_capa_overseas_pkm_com >= 0
        ), "Entry t_a_conveyance_capa_overseas_pkm_com should be 0 or positive"
        assert (
            self.t_a_transport_capa_overseas_tkm_com >= 0
        ), "Entry t_a_transport_capa_overseas_tkm_com should be 0 or positive"
        assert (
            self.t_a_flight_kilometer_overseas_km_com >= 0
        ), "Entry t_a_flight_kilometer_overseas_km_com should be 0 or positive"
        assert (
            self.t_a_eev_kerosene_overseas_com >= 0
        ), "Entry t_a_eev_kerosene_overseas_com should be 0 or positive"
        assert (
            self.t_a_ghg_overseas_com >= 0
        ), "Entry t_a_ghg_overseas_com should be 0 or positive"
        assert (
            self.t_a_sum_ghg_com >= 0
        ), "Entry t_a_sum_ghg_com should be 0 or positive"
        assert (
            self.t_s_eev_diesel_inland_mwh_total >= 0
        ), "Entry t_s_eev_diesel_inland_mwh_total should be 0 or positive"
        assert (
            self.t_s_eev_fuel_overseas_mwh_total >= 0
        ), "Entry t_s_eev_fuel_overseas_mwh_total should be 0 or positive"
        assert (
            self.t_s_eev_diesel_inland_mwh_com >= 0
        ), "Entry t_s_eev_diesel_inland_mwh_com should be 0 or positive"
        assert (
            self.t_s_eev_fuel_overseas_mwh_com >= 0
        ), "Entry t_s_eev_fuel_overseas_mwh_com should be 0 or positive"
        assert (
            self.t_s_ghg_inland_com >= 0
        ), "Entry t_s_ghg_inland_com should be 0 or positive"
        assert (
            self.t_s_ghg_overseas_com >= 0
        ), "Entry t_s_ghg_overseas_com should be 0 or positive"
        assert (
            self.t_s_ghg_sum_com >= 0
        ), "Entry t_s_ghg_sum_com should be 0 or positive"
        assert self.w_elec_fec >= 0, "Entry w_elec_fec should be 0 or positive"
