from . import refdata

# FIXME: This block should die

# test_ags = "03159016"
# ags = 'DG000000'
# test_year = 2035

# This is the list of entries we expect the user to be able to
# override on the website before we e.g. generate the report.
# DO NOT MAKE CHANGES TO THIS LIST WITHOUT MAKING SURE THAT
# THE NECESSARY CHANGES TO THE WEB FORM (in site-templates)
# ARE DONE AND THE ROLLOUT OF BOTH CHANGES IS COORDINATED.
USER_OVERRIDABLE_ENTRIES = [
    "In_M_population_com_2018",
    "In_M_population_com_203X",
    "In_R_buildings_2011_today",
    "In_R_coal_fec",
    "In_R_petrol_fec",
    "In_R_fueloil_fec",
    "In_R_lpg_fec",
    "In_R_gas_fec",
    "In_R_biomass_fec",
    "In_R_orenew_fec",
    "In_R_elec_fec",
    "In_R_heatnet_fec",
    "In_B_coal_fec",
    "In_B_petrol_fec",
    "In_B_jetfuel_fec",
    "In_B_diesel_fec",
    "In_B_fueloil_fec",
    "In_B_lpg_fec",
    "In_B_gas_fec",
    "In_B_biomass_fec",
    "In_B_orenew_fec",
    "In_B_elec_fec",
    "In_B_heatnet_fec",
    "In_I_coal_fec",
    "In_I_diesel_fec",
    "In_I_fueloil_fec",
    "In_I_lpg_fec",
    "In_I_gas_fec",
    "In_I_opetpro_fec",
    "In_I_biomass_fec",
    "In_I_orenew_fec",
    "In_I_ofossil_fec",
    "In_I_elec_fec",
    "In_I_heatnet_fec",
    "In_I_fec_pct_of_miner",
    "In_I_fec_pct_of_chem",
    "In_I_fec_pct_of_metal",
    "In_I_fec_pct_of_other",
    "In_A_petrol_fec",
    "In_A_diesel_fec",
    "In_A_fueloil_fec",
    "In_A_lpg_fec",
    "In_A_gas_fec",
    "In_A_biomass_fec",
    "In_A_elec_fec",
]


def make_entries(data: refdata.RefData, ags: str, year: int):
    # ags identifies the community (Kommune)
    ags_dis = ags[:5]  # This identifies the administrative district (Landkreis)
    ags_sta = ags[:2]  # This identifies the federal state (Bundesland)

    ags_dis_padded = ags_dis + "000"
    ags_sta_padded = ags_sta + "000000"
    ags_germany = "DG000000"

    entry = {}

    entry["ags"] = ags

    entry[
        "In_M_year_today"
    ] = 2022  # int(date.strftime("%Y")) # TODO update accordingly

    entry["In_M_AGS_com"] = ags
    entry["In_M_AGS_dis"] = ags_dis
    entry["In_M_AGS_sta"] = ags_sta

    entry["In_M_year_target"] = year

    entry["In_M_duration_target"] = entry["In_M_year_target"] - entry["In_M_year_today"]
    entry["In_M_duration_target_until_2050"] = 2050 - entry["In_M_year_target"]
    entry["In_M_duration_neutral"] = float(
        entry["In_M_duration_target_until_2050"] + entry["In_M_duration_target"] / 2
    )

    entry["In_M_population_com_2018"] = data.population(ags).int("total")
    entry["In_M_population_com_203X"] = entry["In_M_population_com_2018"]
    entry["In_M_population_dis"] = data.population(ags_dis_padded).int("total")
    entry["In_M_population_sta"] = data.population(ags_sta_padded).int("total")
    entry["In_M_population_nat"] = data.population(ags_germany).int("total")

    data_area_com = data.area(ags)
    data_area_dis = data.area(ags_dis_padded)
    data_area_sta = data.area(ags_sta_padded)
    data_area_nat = data.area(ags_germany)
    entry["In_M_area_total_com"] = data_area_com.int("land_total")
    entry["In_M_area_total_dis"] = data_area_dis.int("land_total")
    entry["In_M_area_total_sta"] = data_area_sta.int("land_total")
    entry["In_M_area_total_nat"] = data_area_nat.int("land_total")

    entry["In_M_area_wood_com"] = data_area_com.int("veg_forrest")
    entry["In_M_area_agri_com"] = data_area_com.int("veg_agri")
    entry["In_M_area_agri_sta"] = data_area_sta.int("veg_agri")
    entry["In_M_area_agri_nat"] = data_area_nat.int("veg_agri")

    entry["In_M_area_veg_grove_com"] = data_area_com.float(
        "veg_wood"
    )  # TODO double check this
    entry["In_M_area_transport_com"] = data_area_com.float("land_traffic")
    entry["In_M_area_settlement_com"] = data_area_com.float("land_settlement")
    entry["In_M_area_veg_heath_com"] = data_area_com.float("veg_heath")
    entry["In_M_area_veg_moor_com"] = data_area_com.float("veg_moor")
    entry["In_M_area_veg_marsh_com"] = data_area_com.float("veg_marsh")
    entry["In_M_area_veg_plant_uncover_com"] = data_area_com.float(
        "veg_plant_uncover_com"
    )
    entry["In_M_area_veg_wood_com"] = data_area_com.float("veg_wood")

    entry["In_M_area_water_com"] = data_area_com.float("water_total")
    entry["In_M_area_industry_com"] = data_area_com.float("settlement_ghd")
    entry["In_M_area_industry_nat"] = data_area_nat.float("settlement_ghd")

    data_flats_com = data.flats(ags)
    entry["In_R_buildings_le_2_apts"] = data_flats_com.float(
        "buildings_2flats"
    ) + data_flats_com.float("buildings_1flat")
    entry["In_R_buildings_ge_3_apts"] = data_flats_com.float(
        "buildings_3flats"
    ) + data_flats_com.float("buildings_dorms")

    data_buildings_com = data.buildings(ags)
    entry["In_R_buildings_until_1919"] = data_buildings_com.float(
        "buildings_until_1919"
    )
    entry["In_R_buildings_1919_1948"] = data_buildings_com.float("buildings_1919_1948")
    entry["In_R_buildings_1949_1978"] = data_buildings_com.float("buildings_1949_1978")
    entry["In_R_buildings_1979_1986"] = data_buildings_com.float("buildings_1979_1986")
    entry["In_R_buildings_1987_1990"] = data_buildings_com.float("buildings_1987_1990")
    entry["In_R_buildings_1991_1995"] = data_buildings_com.float("buildings_1991_1995")
    entry["In_R_buildings_1996_2000"] = data_buildings_com.float("buildings_1996_2000")
    entry["In_R_buildings_2001_2004"] = data_buildings_com.float("buildings_2001_2004")
    entry["In_R_buildings_2005_2008"] = data_buildings_com.float("buildings_2005_2008")
    entry["In_R_buildings_2009_2011"] = data_buildings_com.float("buildings_2009_2011")
    entry["In_R_buildings_2011_today"] = (
        data.fact("Fact_R_P_newbuilt_2011_2018")
        * entry["In_M_population_com_2018"]
        / entry["In_M_population_nat"]
    )
    entry["In_R_buildings_com"] = (
        entry["In_R_buildings_until_1919"]
        + entry["In_R_buildings_1919_1948"]
        + entry["In_R_buildings_1949_1978"]
        + entry["In_R_buildings_1979_1986"]
        + entry["In_R_buildings_1987_1990"]
        + entry["In_R_buildings_1991_1995"]
        + entry["In_R_buildings_1996_2000"]
        + entry["In_R_buildings_2001_2004"]
        + entry["In_R_buildings_2005_2008"]
        + entry["In_R_buildings_2009_2011"]
        + entry["In_R_buildings_2011_today"]
    )
    entry["In_R_buildings_nat"] = data.buildings(ags_germany).float(
        "buildings_total"
    ) + data.fact("Fact_R_P_newbuilt_2011_2018")

    entry["In_R_flats_com"] = data_buildings_com.float("flats_total")
    entry["In_R_flats_w_heatnet"] = data_buildings_com.float("flats_heatnet")
    entry["In_R_flats_wo_heatnet"] = (
        entry["In_R_flats_com"] - entry["In_R_flats_w_heatnet"]
    )
    entry["In_R_area_m2"] = (
        data_flats_com.float("residential_buildings_area_total") * 1000.0
    )
    entry["In_R_area_m2_1flat"] = data_flats_com.float("buildings_1flat") * data.fact(
        "Fact_R_buildings_livingspace_oneflat"
    )
    entry["In_R_area_m2_2flat"] = data_flats_com.float("buildings_2flats") * data.fact(
        "Fact_R_buildings_livingspace_twoflat"
    )
    entry["In_R_area_m2_3flat"] = data_flats_com.float("buildings_3flats") * data.fact(
        "Fact_R_buildings_livingspace_moreflat"
    )
    entry["In_R_area_m2_dorm"] = data_flats_com.float("buildings_dorms") * data.fact(
        "Fact_R_buildings_livingspace_dorm"
    )
    entry["In_R_pct_of_area_m2_com"] = data.nat_res_buildings(ags_sta_padded).float(
        "communal"
    )
    entry["In_R_rehab_rate_pa"] = data.ass("Ass_R_B_P_renovation_rate")
    entry["In_R_heatnet_ratio_year_target"] = (
        entry["In_R_flats_w_heatnet"] / entry["In_R_flats_com"]
    )

    if ags == ags_germany:
        entry["In_T_rt7"] = "nd"
        entry["In_T_rt3"] = "nd"
    else:
        # entry['In_T_rt7'] = list(raumtypen[raumtypen['ags'] == entry['In_M_AGS_com']]['RegioStaR7'])[0]
        # entry['In_T_rt3'] = list(raumtypen[raumtypen['ags'] == entry['In_M_AGS_com']]['Raumtyp3'])[0]
        entry["In_T_rt7"] = data.area_kinds(ags).int("rt7")
        entry["In_T_rt3"] = data.area_kinds(ags).str("rt3")

    data_renewable_energy_com = data.renewable_energy(ags)
    data_nat_energy_sta = data.nat_energy(ags_sta_padded)
    entry["In_E_PV_power_inst_roof"] = (
        data_renewable_energy_com.float("pv")
        / 1000.0
        * data_nat_energy_sta.float("PV_roof_2017")
    )
    entry["In_E_PV_power_inst_facade"] = (
        data_renewable_energy_com.float("pv")
        / 1000.0
        * data_nat_energy_sta.float("PV_others")
        / 2.0
    )
    entry["In_E_PV_power_inst_park"] = (
        data_renewable_energy_com.float("pv")
        / 1000.0
        * data_nat_energy_sta.float("PV_land_2017")
    )
    entry["In_E_PV_power_inst_agripv"] = (
        data_renewable_energy_com.float("pv")
        / 1000.0
        * data_nat_energy_sta.float("PV_others")
        / 2.0
    )
    entry["In_E_PV_power_inst_wind_on"] = (
        data_renewable_energy_com.float("wind_on") / 1000.0
    )
    entry["In_E_PV_power_inst_biomass"] = (
        data_renewable_energy_com.float("biomass") / 1000.0
    )
    entry["In_E_PV_power_inst_water"] = (
        data_renewable_energy_com.float("water") / 1000.0
    )

    entry["In_E_PV_power_to_be_inst_roof"] = data.ass(
        "Ass_E_P_local_pv_roof_power_to_be_installed_2035"
    )
    entry["In_H_solartherm_to_be_inst"] = data.ass(
        "Ass_R_B_P_roof_area_fraction_solar_thermal"
    )
    entry["In_E_PV_power_to_be_inst_facade"] = data.ass(
        "Ass_E_P_local_pv_roof_facade_to_be_installed_2035"
    )
    entry["In_E_PV_power_to_be_inst_park"] = data.ass(
        "Ass_E_P_local_pv_park_power_to_be_installed_2035"
    )
    entry["In_E_PV_power_to_be_inst_agri"] = data.ass(
        "Ass_E_P_local_pv_agri_power_to_be_installed_2035"
    )
    entry["In_E_PV_power_to_be_inst_local_wind_onshore"] = data.ass(
        "Ass_E_P_local_wind_onshore_power_to_be_installed_2035"
    )
    entry["In_E_PV_power_to_be_inst_local_biomass"] = data.ass(
        "Ass_E_P_local_biomass_power_to_be_installed_2035"
    )

    entry["In_E_pv_full_load_hours_sta"] = data_nat_energy_sta.float("PV_average_flh")
    entry[
        "In_E_local_wind_onshore_ratio_power_to_area_sta"
    ] = data_nat_energy_sta.float("demand_2018")
    potential_electricity_from_bioenergy_sta = (
        data_nat_energy_sta.float("bioenergy_potential")
        * 1000.0
        / 3.6
        * data.ass("Ass_E_P_BHKW_efficiency_electric")
    )
    bioenergy_installable_capacity_sta = (
        potential_electricity_from_bioenergy_sta
        / data.fact("Fact_E_P_biomass_full_load_hours")
    )
    entry[
        "In_E_biomass_local_power_installable_sta"
    ] = bioenergy_installable_capacity_sta * (
        entry["In_M_area_agri_com"] / entry["In_M_area_agri_sta"]
    )

    entry["In_R_coal_fec"] = (
        data.fact("Fact_R_S_coal_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_petrol_fec"] = (
        data.fact("Fact_R_S_petrol_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_fueloil_fec"] = (
        data.fact("Fact_R_S_fueloil_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_lpg_fec"] = (
        data.fact("Fact_R_S_lpg_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_gas_fec"] = (
        data.fact("Fact_R_S_gas_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_biomass_fec"] = (
        data.fact("Fact_R_S_biomass_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_orenew_fec"] = (
        data.fact("Fact_R_S_orenew_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_R_elec_fec"] = (
        data.fact("Fact_R_S_elec_fec_2018")
        * entry["In_M_population_com_2018"]
        / entry["In_M_population_nat"]
    )
    entry["In_R_heatnet_fec"] = (
        data.fact("Fact_R_S_heatnet_fec_2018")
        * entry["In_R_flats_w_heatnet"]
        / data.fact("Fact_R_P_flats_w_heatnet_2011")
    )
    entry["In_R_energy_total"] = (
        entry["In_R_coal_fec"]
        + entry["In_R_petrol_fec"]
        + entry["In_R_fueloil_fec"]
        + entry["In_R_lpg_fec"]
        + entry["In_R_gas_fec"]
        + entry["In_R_biomass_fec"]
        + entry["In_R_orenew_fec"]
        + entry["In_R_elec_fec"]
        + entry["In_R_heatnet_fec"]
    )

    entry["In_B_coal_fec"] = (
        data.fact("Fact_B_S_coal_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_B_petrol_fec"] = (
        data.fact("Fact_B_S_petrol_fec_2018")
        * entry["In_M_population_com_2018"]
        / entry["In_M_population_nat"]
    )
    entry["In_B_jetfuel_fec"] = (
        data.fact("Fact_B_S_jetfuel_fec_2018")
        * entry["In_M_population_com_2018"]
        / entry["In_M_population_nat"]
    )
    entry["In_B_diesel_fec"] = (
        data.fact("Fact_B_S_diesel_fec_2018")
        * entry["In_M_population_com_2018"]
        / entry["In_M_population_nat"]
    )
    entry["In_B_fueloil_fec"] = (
        data.fact("Fact_B_S_fueloil_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_B_lpg_fec"] = (
        data.fact("Fact_B_S_lpg_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_B_gas_fec"] = (
        data.fact("Fact_B_S_gas_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_B_biomass_fec"] = (
        data.fact("Fact_B_S_biomass_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_B_orenew_fec"] = (
        data.fact("Fact_B_S_orenew_fec_2018")
        * entry["In_R_flats_wo_heatnet"]
        / data.fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    entry["In_B_elec_fec"] = (
        data.fact("Fact_B_S_elec_fec_2018")
        * entry["In_M_population_com_2018"]
        / entry["In_M_population_nat"]
    )
    entry["In_B_heatnet_fec"] = (
        data.fact("Fact_B_S_heatnet_fec_2018")
        * entry["In_R_flats_w_heatnet"]
        / data.fact("Fact_R_P_flats_w_heatnet_2011")
    )

    entry["In_I_coal_fec"] = (
        data.fact("Fact_I_S_coal_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_diesel_fec"] = (
        data.fact("Fact_I_S_diesel_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_fueloil_fec"] = (
        data.fact("Fact_I_S_fueloil_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_lpg_fec"] = (
        data.fact("Fact_I_S_lpg_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_gas_fec"] = (
        data.fact("Fact_I_S_gas_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_opetpro_fec"] = (
        data.fact("Fact_I_S_opetpro_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_biomass_fec"] = (
        data.fact("Fact_I_S_biomass_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_orenew_fec"] = (
        data.fact("Fact_I_S_orenew_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_ofossil_fec"] = (
        data.fact("Fact_I_S_ofossil_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_elec_fec"] = (
        data.fact("Fact_I_S_elec_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )
    entry["In_I_heatnet_fec"] = (
        data.fact("Fact_I_S_heatnet_fec_2018")
        * entry["In_M_area_industry_com"]
        / entry["In_M_area_industry_nat"]
    )

    entry["In_I_energy_total"] = (
        entry["In_I_coal_fec"]
        + entry["In_I_diesel_fec"]
        + entry["In_I_fueloil_fec"]
        + entry["In_I_lpg_fec"]
        + entry["In_I_gas_fec"]
        + entry["In_I_opetpro_fec"]
        + entry["In_I_biomass_fec"]
        + entry["In_I_orenew_fec"]
        + entry["In_I_ofossil_fec"]
        + entry["In_I_elec_fec"]
        + entry["In_I_heatnet_fec"]
    )

    entry["In_I_fec_pct_of_miner"] = data.fact(
        "Fact_I_P_miner_ratio_fec_to_industry_2018"
    )
    entry["In_I_fec_pct_of_chem"] = data.fact(
        "Fact_I_S_chem_fec_ratio_to_industrie_2018"
    )
    entry["In_I_fec_pct_of_metal"] = data.fact("Fact_I_P_fec_pct_of_metal_2018")
    entry["In_I_fec_pct_of_other"] = data.fact(
        "Fact_I_P_other_ratio_fec_to_industry_2018"
    )

    data_traffic_com = data.traffic(ags)
    entry["In_T_ec_rail_ppl_elec"] = data_traffic_com.float("rail_ppl_elec")
    entry["In_T_ec_rail_ppl_diesel"] = data_traffic_com.float("rail_ppl_diesel")
    entry["In_T_ec_rail_gds_elec"] = data_traffic_com.float("gds_elec")
    entry["In_T_ec_rail_gds_diesel"] = data_traffic_com.float("gds_diesel")

    entry["In_T_mil_car_it_at"] = data_traffic_com.float("car_it_at")
    entry["In_T_mil_car_ab"] = data_traffic_com.float("car_ab")
    entry["In_T_mil_ldt_it_at"] = data_traffic_com.float("ldt_it_at")
    entry["In_T_mil_ldt_ab"] = data_traffic_com.float("ldt_ab")
    entry["In_T_mil_mhd_it_at"] = data_traffic_com.float("mhd_it_at")
    entry["In_T_mil_mhd_ab"] = data_traffic_com.float("mhd_ab")

    data_destatis_com = data.destatis(ags_dis_padded)
    entry["In_T_metro_mega_km_dis"] = data_destatis_com.float("metro_mega_km")
    entry["In_T_bus_mega_km_dis"] = data_destatis_com.float("bus_mega_km")

    entry["In_A_petrol_fec"] = (
        data.fact("Fact_A_S_petrol_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )
    entry["In_A_diesel_fec"] = (
        data.fact("Fact_A_S_diesel_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )
    entry["In_A_fueloil_fec"] = (
        data.fact("Fact_A_S_fueloil_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )
    entry["In_A_lpg_fec"] = (
        data.fact("Fact_A_S_lpg_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )
    entry["In_A_gas_fec"] = (
        data.fact("Fact_A_S_gas_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )
    entry["In_A_biomass_fec"] = (
        data.fact("Fact_A_S_biomass_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )
    entry["In_A_elec_fec"] = (
        data.fact("Fact_A_S_elec_fec_2018")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_nat"]
    )

    data_nat_agri_sta = data.nat_agri(ags_sta_padded)
    entry["In_A_other_liming_calcit_prod_volume"] = (
        data_nat_agri_sta.float("amount_sale_calcit")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_sta"]
    )
    entry["In_A_other_liming_dolomite_prod_volume"] = (
        data_nat_agri_sta.float("amount_sale_dolomite")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_sta"]
    )
    entry["In_A_other_kas_prod_volume"] = (
        data_nat_agri_sta.float("amount_sale_kas")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_sta"]
    )
    entry["In_A_other_urea_prod_volume"] = (
        data_nat_agri_sta.float("amount_sale_urea")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_sta"]
    )
    entry["In_A_other_ecrop_prod_volume"] = (
        data_nat_agri_sta.float("drymass_ecrop")
        * entry["In_M_area_agri_com"]
        / entry["In_M_area_agri_sta"]
    )

    cows_density_sta = data_nat_agri_sta.float("cows") / entry["In_M_area_agri_sta"]
    entry["In_A_fermen_dairycow_amount"] = (
        cows_density_sta * entry["In_M_area_agri_com"]
    )

    cattle_density_sta = data_nat_agri_sta.float("cattle") / entry["In_M_area_agri_sta"]
    entry["In_A_fermen_nondairy_amount"] = (
        cattle_density_sta * entry["In_M_area_agri_com"]
    )

    pig_density_sta = data_nat_agri_sta.float("pigs") / entry["In_M_area_agri_sta"]
    entry["In_A_fermen_pig_amount"] = pig_density_sta * entry["In_M_area_agri_com"]

    poultry_density_sta = (
        data_nat_agri_sta.float("poultry") / entry["In_M_area_agri_sta"]
    )
    entry["In_A_fermen_poultry_amount"] = (
        poultry_density_sta * entry["In_M_area_agri_com"]
    )

    other_animals_density_sta = (
        data_nat_agri_sta.float("other_animals") / entry["In_M_area_agri_sta"]
    )
    entry["In_A_fermen_oanimal_amount"] = (
        other_animals_density_sta * entry["In_M_area_agri_com"]
    )

    def compute_animal_efactor(what: str):
        ch4e = data_nat_agri_sta.float(what + "_ch4e")
        n2oe = data_nat_agri_sta.float(what + "_n2oe")
        co2e = (ch4e * 25.0 + n2oe * 298.0) * 1000.0
        count = data_nat_agri_sta.float(what)
        if count > 0:
            return co2e / count
        else:
            # TODO: compute national equivalent
            assert False, "Here we should return the national efactor instead"

    entry["In_A_manure_dairycow_ratio_CO2e_to_amount"] = compute_animal_efactor("cows")
    entry["In_A_manure_nondairy_ratio_CO2e_to_amount"] = compute_animal_efactor(
        "cattle"
    )
    entry["In_A_manure_swine_ratio_CO2e_to_amount"] = compute_animal_efactor("pigs")
    entry["In_A_manure_poultry_ratio_CO2e_to_amount"] = compute_animal_efactor(
        "poultry"
    )
    entry["In_A_manure_oanimal_ratio_CO2e_to_amount"] = compute_animal_efactor(
        "other_animals"
    )
    animal_wo_poultry_deposition_sta = (
        data_nat_agri_sta.float("cows")
        + data_nat_agri_sta.float("cattle")
        + data_nat_agri_sta.float("pigs")
        + data_nat_agri_sta.float("other_animals")
    )
    if animal_wo_poultry_deposition_sta > 0:
        entry["In_A_manure_deposition_ratio_CO2e_to_amount"] = (
            data_nat_agri_sta.float("animal_wo_poultry_deposition_co2e")
            / animal_wo_poultry_deposition_sta
        )
    else:
        assert False, "TODO here we should compute the natoional factor instead"

    def compute_efactor_from_n2o(
        what: str, area: float, data_nat_agri: refdata.Row = data_nat_agri_sta
    ):
        n2o = data_nat_agri.float(what + "_n2o")
        co2e = n2o * 298.0
        return co2e / area

    farmland_area_total_sta = entry["In_M_area_agri_sta"] * data.fact(
        "Fact_L_G_factor_crop"
    )
    entry["In_A_soil_fertilizer_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "fertilizer_mineral", farmland_area_total_sta
    )
    entry["In_A_soil_manure_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "fertilizer_economy", farmland_area_total_sta
    )
    entry["In_A_soil_sludge_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "sewage_sludge", farmland_area_total_sta
    )
    entry["In_A_soil_ecrop_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "fermentation_ecrop", farmland_area_total_sta
    )
    greenland_area_total_sta = (
        entry["In_M_area_agri_sta"] * data.fact("Fact_L_G_factor_crop_to_grass")
        + data_area_sta.float("veg_heath")
        + data_area_sta.float("veg_marsh")
        + data_area_sta.float("veg_plant_uncover_com")
        * data.fact("Fact_L_G_factor_grass_strict")
    )
    entry["In_A_soil_crazing_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "pasturage", greenland_area_total_sta
    )
    entry["In_A_soil_residue_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "crop_residues", farmland_area_total_sta
    )
    farmland_area_organic_sta = farmland_area_total_sta * (
        data.fact("Fact_L_G_fraction_org_soil_fen_crop")
        + data.fact("Fact_L_G_fraction_org_soil_bog_crop")
    )
    farmland_area_organic_germany = (
        entry["In_M_area_agri_nat"]
        * data.fact("Fact_L_G_factor_crop")
        * (
            data.fact("Fact_L_G_fraction_org_soil_fen_crop")
            + data.fact("Fact_L_G_fraction_org_soil_bog_crop")
        )
    )
    greenland_area_organic_sta = greenland_area_total_sta * (
        data.fact("Fact_L_G_fraction_org_soil_fen_grass_strict")
        + data.fact("Fact_L_G_fraction_org_soil_bog_grass_strict")
    )
    entry["In_A_soil_orgfarm_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "farmed_soil", farmland_area_organic_sta + greenland_area_organic_sta
    )
    # unlike the other factors we don't have the n2o levels below the national level available :-(
    data_nat_agri_germany = data.nat_agri(ags_germany)
    entry["In_A_soil_orgloss_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "farmed_soil_loss_organic",
        area=farmland_area_organic_germany,
        data_nat_agri=data_nat_agri_germany,
    )
    entry["In_A_soil_leaching_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "diffuse_nitrate_emissions",
        area=farmland_area_total_sta + greenland_area_total_sta,
    )
    entry["In_A_soil_deposition_ratio_CO2e_to_ha"] = compute_efactor_from_n2o(
        "diffuse_emissions", area=farmland_area_total_sta + greenland_area_total_sta
    )

    farming_density_sta = data_nat_agri_sta.float("farms") / entry["In_M_area_agri_sta"]
    # We would like 2018 data here but we only have 2016, so we assume the ratio stayed constant
    data_nat_organic_agri_sta = data.nat_organic_agri(ags_sta_padded)

    entry["In_A_farm_amount"] = farming_density_sta * entry["In_M_area_agri_com"]
    entry["In_A_area_agri_com_pct_of_organic"] = (
        data_nat_organic_agri_sta.float("organic_farms_area")
        / entry["In_M_area_agri_sta"]
    )

    entry["In_M_GHG_budget_2016_to_year_target"] = data.co2path(year).float(
        "GHG_budget_2016_to_year"
    )
    entry["In_M_nonCO2_budget_2016_to_year_target"] = data.co2path(year).float(
        "nonCO2_budget_2016_to_year"
    )

    return entry
