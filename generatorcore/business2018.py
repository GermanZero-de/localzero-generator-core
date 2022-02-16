from dataclasses import dataclass, asdict, field
from .inputs import Inputs
from .utils import div
from . import residences2018

# Definition der relevanten Spaltennamen für den Sektor E


@dataclass
class BColVars:
    energy: float = None
    pct_x: float = None
    pct_energy: float = None
    area_m2: float = None
    factor_adapted_to_fec: float = None
    cost_fuel: float = None
    cost_fuel_per_MWh: float = None
    CO2e_cb: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_pb: float = None
    CO2e_total: float = None
    number_of_buildings: float = None


@dataclass
class B18:
    b_energy: float
    b_pct_x: float
    b_pct_energy: float
    b_area_m2: float
    b_factor_adapted_to_fec: float
    b_cost_fuel: float
    b_cost_fuel_per_MWh: float
    b_CO2e_cb: float
    b_CO2e_cb_per_MWh: float
    b_CO2e_pb: float
    b_CO2e_total: float
    b_number_of_buildings: float
    g_energy: float
    g_pct_x: float
    g_pct_energy: float
    g_area_m2: float
    g_factor_adapted_to_fec: float
    g_cost_fuel: float
    g_cost_fuel_per_MWh: float
    g_CO2e_cb: float
    g_CO2e_cb_per_MWh: float
    g_CO2e_pb: float
    g_CO2e_total: float
    g_number_of_buildings: float
    g_consult_energy: float
    g_consult_pct_x: float
    g_consult_pct_energy: float
    g_consult_area_m2: float
    g_consult_factor_adapted_to_fec: float
    g_consult_cost_fuel: float
    g_consult_cost_fuel_per_MWh: float
    g_consult_CO2e_cb: float
    g_consult_CO2e_cb_per_MWh: float
    g_consult_CO2e_pb: float
    g_consult_CO2e_total: float
    g_consult_number_of_buildings: float
    p_energy: float
    p_pct_x: float
    p_pct_energy: float
    p_area_m2: float
    p_factor_adapted_to_fec: float
    p_cost_fuel: float
    p_cost_fuel_per_MWh: float
    p_CO2e_cb: float
    p_CO2e_cb_per_MWh: float
    p_CO2e_pb: float
    p_CO2e_total: float
    p_number_of_buildings: float
    p_nonresi_energy: float
    p_nonresi_pct_x: float
    p_nonresi_pct_energy: float
    p_nonresi_area_m2: float
    p_nonresi_factor_adapted_to_fec: float
    p_nonresi_cost_fuel: float
    p_nonresi_cost_fuel_per_MWh: float
    p_nonresi_CO2e_cb: float
    p_nonresi_CO2e_cb_per_MWh: float
    p_nonresi_CO2e_pb: float
    p_nonresi_CO2e_total: float
    p_nonresi_number_of_buildings: float
    p_nonresi_com_energy: float
    p_nonresi_com_pct_x: float
    p_nonresi_com_pct_energy: float
    p_nonresi_com_area_m2: float
    p_nonresi_com_factor_adapted_to_fec: float
    p_nonresi_com_cost_fuel: float
    p_nonresi_com_cost_fuel_per_MWh: float
    p_nonresi_com_CO2e_cb: float
    p_nonresi_com_CO2e_cb_per_MWh: float
    p_nonresi_com_CO2e_pb: float
    p_nonresi_com_CO2e_total: float
    p_nonresi_com_number_of_buildings: float
    p_elec_elcon_energy: float
    p_elec_elcon_pct_x: float
    p_elec_elcon_pct_energy: float
    p_elec_elcon_area_m2: float
    p_elec_elcon_factor_adapted_to_fec: float
    p_elec_elcon_cost_fuel: float
    p_elec_elcon_cost_fuel_per_MWh: float
    p_elec_elcon_CO2e_cb: float
    p_elec_elcon_CO2e_cb_per_MWh: float
    p_elec_elcon_CO2e_pb: float
    p_elec_elcon_CO2e_total: float
    p_elec_elcon_number_of_buildings: float
    p_elec_heatpump_energy: float
    p_elec_heatpump_pct_x: float
    p_elec_heatpump_pct_energy: float
    p_elec_heatpump_area_m2: float
    p_elec_heatpump_factor_adapted_to_fec: float
    p_elec_heatpump_cost_fuel: float
    p_elec_heatpump_cost_fuel_per_MWh: float
    p_elec_heatpump_CO2e_cb: float
    p_elec_heatpump_CO2e_cb_per_MWh: float
    p_elec_heatpump_CO2e_pb: float
    p_elec_heatpump_CO2e_total: float
    p_elec_heatpump_number_of_buildings: float
    p_vehicles_energy: float
    p_vehicles_pct_x: float
    p_vehicles_pct_energy: float
    p_vehicles_area_m2: float
    p_vehicles_factor_adapted_to_fec: float
    p_vehicles_cost_fuel: float
    p_vehicles_cost_fuel_per_MWh: float
    p_vehicles_CO2e_cb: float
    p_vehicles_CO2e_cb_per_MWh: float
    p_vehicles_CO2e_pb: float
    p_vehicles_CO2e_total: float
    p_vehicles_number_of_buildings: float
    p_other_energy: float
    p_other_pct_x: float
    p_other_pct_energy: float
    p_other_area_m2: float
    p_other_factor_adapted_to_fec: float
    p_other_cost_fuel: float
    p_other_cost_fuel_per_MWh: float
    p_other_CO2e_cb: float
    p_other_CO2e_cb_per_MWh: float
    p_other_CO2e_pb: float
    p_other_CO2e_total: float
    p_other_number_of_buildings: float
    s_energy: float
    s_pct_x: float
    s_pct_energy: float
    s_area_m2: float
    s_factor_adapted_to_fec: float
    s_cost_fuel: float
    s_cost_fuel_per_MWh: float
    s_CO2e_cb: float
    s_CO2e_cb_per_MWh: float
    s_CO2e_pb: float
    s_CO2e_total: float
    s_number_of_buildings: float
    s_gas_energy: float
    s_gas_pct_x: float
    s_gas_pct_energy: float
    s_gas_area_m2: float
    s_gas_factor_adapted_to_fec: float
    s_gas_cost_fuel: float
    s_gas_cost_fuel_per_MWh: float
    s_gas_CO2e_cb: float
    s_gas_CO2e_cb_per_MWh: float
    s_gas_CO2e_pb: float
    s_gas_CO2e_total: float
    s_gas_number_of_buildings: float
    s_emethan_energy: float
    s_emethan_pct_x: float
    s_emethan_pct_energy: float
    s_emethan_area_m2: float
    s_emethan_factor_adapted_to_fec: float
    s_emethan_cost_fuel: float
    s_emethan_cost_fuel_per_MWh: float
    s_emethan_CO2e_cb: float
    s_emethan_CO2e_cb_per_MWh: float
    s_emethan_CO2e_pb: float
    s_emethan_CO2e_total: float
    s_emethan_number_of_buildings: float
    s_lpg_energy: float
    s_lpg_pct_x: float
    s_lpg_pct_energy: float
    s_lpg_area_m2: float
    s_lpg_factor_adapted_to_fec: float
    s_lpg_cost_fuel: float
    s_lpg_cost_fuel_per_MWh: float
    s_lpg_CO2e_cb: float
    s_lpg_CO2e_cb_per_MWh: float
    s_lpg_CO2e_pb: float
    s_lpg_CO2e_total: float
    s_lpg_number_of_buildings: float
    s_petrol_energy: float
    s_petrol_pct_x: float
    s_petrol_pct_energy: float
    s_petrol_area_m2: float
    s_petrol_factor_adapted_to_fec: float
    s_petrol_cost_fuel: float
    s_petrol_cost_fuel_per_MWh: float
    s_petrol_CO2e_cb: float
    s_petrol_CO2e_cb_per_MWh: float
    s_petrol_CO2e_pb: float
    s_petrol_CO2e_total: float
    s_petrol_number_of_buildings: float
    s_jetfuel_energy: float
    s_jetfuel_pct_x: float
    s_jetfuel_pct_energy: float
    s_jetfuel_area_m2: float
    s_jetfuel_factor_adapted_to_fec: float
    s_jetfuel_cost_fuel: float
    s_jetfuel_cost_fuel_per_MWh: float
    s_jetfuel_CO2e_cb: float
    s_jetfuel_CO2e_cb_per_MWh: float
    s_jetfuel_CO2e_pb: float
    s_jetfuel_CO2e_total: float
    s_jetfuel_number_of_buildings: float
    s_diesel_energy: float
    s_diesel_pct_x: float
    s_diesel_pct_energy: float
    s_diesel_area_m2: float
    s_diesel_factor_adapted_to_fec: float
    s_diesel_cost_fuel: float
    s_diesel_cost_fuel_per_MWh: float
    s_diesel_CO2e_cb: float
    s_diesel_CO2e_cb_per_MWh: float
    s_diesel_CO2e_pb: float
    s_diesel_CO2e_total: float
    s_diesel_number_of_buildings: float
    s_fueloil_energy: float
    s_fueloil_pct_x: float
    s_fueloil_pct_energy: float
    s_fueloil_area_m2: float
    s_fueloil_factor_adapted_to_fec: float
    s_fueloil_cost_fuel: float
    s_fueloil_cost_fuel_per_MWh: float
    s_fueloil_CO2e_cb: float
    s_fueloil_CO2e_cb_per_MWh: float
    s_fueloil_CO2e_pb: float
    s_fueloil_CO2e_total: float
    s_fueloil_number_of_buildings: float
    s_biomass_energy: float
    s_biomass_pct_x: float
    s_biomass_pct_energy: float
    s_biomass_area_m2: float
    s_biomass_factor_adapted_to_fec: float
    s_biomass_cost_fuel: float
    s_biomass_cost_fuel_per_MWh: float
    s_biomass_CO2e_cb: float
    s_biomass_CO2e_cb_per_MWh: float
    s_biomass_CO2e_pb: float
    s_biomass_CO2e_total: float
    s_biomass_number_of_buildings: float
    s_coal_energy: float
    s_coal_pct_x: float
    s_coal_pct_energy: float
    s_coal_area_m2: float
    s_coal_factor_adapted_to_fec: float
    s_coal_cost_fuel: float
    s_coal_cost_fuel_per_MWh: float
    s_coal_CO2e_cb: float
    s_coal_CO2e_cb_per_MWh: float
    s_coal_CO2e_pb: float
    s_coal_CO2e_total: float
    s_coal_number_of_buildings: float
    s_heatnet_energy: float
    s_heatnet_pct_x: float
    s_heatnet_pct_energy: float
    s_heatnet_area_m2: float
    s_heatnet_factor_adapted_to_fec: float
    s_heatnet_cost_fuel: float
    s_heatnet_cost_fuel_per_MWh: float
    s_heatnet_CO2e_cb: float
    s_heatnet_CO2e_cb_per_MWh: float
    s_heatnet_CO2e_pb: float
    s_heatnet_CO2e_total: float
    s_heatnet_number_of_buildings: float
    s_elec_heating_energy: float
    s_elec_heating_pct_x: float
    s_elec_heating_pct_energy: float
    s_elec_heating_area_m2: float
    s_elec_heating_factor_adapted_to_fec: float
    s_elec_heating_cost_fuel: float
    s_elec_heating_cost_fuel_per_MWh: float
    s_elec_heating_CO2e_cb: float
    s_elec_heating_CO2e_cb_per_MWh: float
    s_elec_heating_CO2e_pb: float
    s_elec_heating_CO2e_total: float
    s_elec_heating_number_of_buildings: float
    s_heatpump_energy: float
    s_heatpump_pct_x: float
    s_heatpump_pct_energy: float
    s_heatpump_area_m2: float
    s_heatpump_factor_adapted_to_fec: float
    s_heatpump_cost_fuel: float
    s_heatpump_cost_fuel_per_MWh: float
    s_heatpump_CO2e_cb: float
    s_heatpump_CO2e_cb_per_MWh: float
    s_heatpump_CO2e_pb: float
    s_heatpump_CO2e_total: float
    s_heatpump_number_of_buildings: float
    s_solarth_energy: float
    s_solarth_pct_x: float
    s_solarth_pct_energy: float
    s_solarth_area_m2: float
    s_solarth_factor_adapted_to_fec: float
    s_solarth_cost_fuel: float
    s_solarth_cost_fuel_per_MWh: float
    s_solarth_CO2e_cb: float
    s_solarth_CO2e_cb_per_MWh: float
    s_solarth_CO2e_pb: float
    s_solarth_CO2e_total: float
    s_solarth_number_of_buildings: float
    s_elec_energy: float
    s_elec_pct_x: float
    s_elec_pct_energy: float
    s_elec_area_m2: float
    s_elec_factor_adapted_to_fec: float
    s_elec_cost_fuel: float
    s_elec_cost_fuel_per_MWh: float
    s_elec_CO2e_cb: float
    s_elec_CO2e_cb_per_MWh: float
    s_elec_CO2e_pb: float
    s_elec_CO2e_total: float
    s_elec_number_of_buildings: float
    rb_energy: float
    rb_pct_x: float
    rb_pct_energy: float
    rb_area_m2: float
    rb_factor_adapted_to_fec: float
    rb_cost_fuel: float
    rb_cost_fuel_per_MWh: float
    rb_CO2e_cb: float
    rb_CO2e_cb_per_MWh: float
    rb_CO2e_pb: float
    rb_CO2e_total: float
    rb_number_of_buildings: float
    rp_p_energy: float
    rp_p_pct_x: float
    rp_p_pct_energy: float
    rp_p_area_m2: float
    rp_p_factor_adapted_to_fec: float
    rp_p_cost_fuel: float
    rp_p_cost_fuel_per_MWh: float
    rp_p_CO2e_cb: float
    rp_p_CO2e_cb_per_MWh: float
    rp_p_CO2e_pb: float
    rp_p_CO2e_total: float
    rp_p_number_of_buildings: float

    def dict(self):
        return asdict(self)


# Berechnungsfunktion im Sektor GHD für 2018


def calc(inputs: Inputs, *, r18: residences2018.R18) -> B18:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    Million = 1000000.0

    b18_s_gas_energy = entry("In_B_gas_fec")  # 98.602.500 MWh

    b18_s_lpg_energy = entry("In_B_lpg_fec")  # 3.007.222 MWh

    b18_s_petrol_energy = entry("In_B_petrol_fec")  # 1.667.778 MWh

    b18_s_jetfuel_energy = entry("In_B_jetfuel_fec")  # 284.722 MWh

    b18_s_diesel_energy = entry("In_B_diesel_fec")  # 9.033.056 MWh

    b18_s_fueloil_energy = entry("In_B_fueloil_fec")  # 33.370.278 MWh

    b18_s_biomass_energy = entry("In_B_biomass_fec")  # 20.860.278 MWh

    b18_s_coal_energy = entry("In_B_coal_fec")  # 232.778 MWh

    b18_s_heatnet_energy = entry("In_B_heatnet_fec")  # 6.521.944 MWh

    b18_s_elec_heating_energy = (
        fact("Fact_B_S_elec_heating_fec_2018")
        * entry("In_R_flats_wo_heatnet")
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )  # 13.027.778 MWh

    b18_s_heatpump_energy = entry("In_B_orenew_fec") * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )  # 1.262.040 MWh

    b18_s_solarth_energy = entry("In_B_orenew_fec") * (
        1 - fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    )  # 1.262.040 MWh

    b18_s_elec_energy = entry("In_B_elec_fec")
    # 856.293 MWh

    b18_s_energy = (
        b18_s_gas_energy
        + b18_s_lpg_energy
        + b18_s_petrol_energy
        + b18_s_jetfuel_energy
        + b18_s_diesel_energy
        + b18_s_fueloil_energy
        + b18_s_biomass_energy
        + b18_s_coal_energy
        + b18_s_heatnet_energy
        + b18_s_heatpump_energy
        + b18_s_solarth_energy
        + b18_s_elec_energy
    )  # 187.870.374 MWh

    b18_s_gas_pct_energy = div(b18_s_gas_energy, b18_s_energy)  # 52,5%

    b18_s_lpg_pct_energy = div(b18_s_lpg_energy, b18_s_energy)  # 1,6%

    b18_s_petrol_pct_energy = div(b18_s_petrol_energy, b18_s_energy)  # 0,9%

    b18_s_jetfuel_pct_energy = div(b18_s_jetfuel_energy, b18_s_energy)  # 0,2%

    b18_s_diesel_pct_energy = div(b18_s_diesel_energy, b18_s_energy)  # 4,8%

    b18_s_fueloil_pct_energy = div(b18_s_fueloil_energy, b18_s_energy)  # 17,8%

    b18_s_biomass_pct_energy = div(b18_s_biomass_energy, b18_s_energy)  # 11,1%

    b18_s_coal_pct_energy = div(b18_s_coal_energy, b18_s_energy)  # 0,1%

    b18_s_heatnet_pct_energy = div(b18_s_heatnet_energy, b18_s_energy)  # 3,5%

    b18_s_elec_heating_pct_energy = div(
        b18_s_elec_heating_energy, b18_s_elec_energy
    )  # 6,9%

    b18_s_heatpump_pct_energy = div(b18_s_heatpump_energy, b18_s_energy)  # 0,7%

    b18_s_solarth_pct_energy = div(b18_s_solarth_energy, b18_s_energy)  # 0,5%

    b18_s_elec_pct_energy = div(b18_s_elec_energy, b18_s_energy)

    b18_s_pct_energy = (
        b18_s_gas_pct_energy
        + b18_s_lpg_pct_energy
        + b18_s_petrol_pct_energy
        + b18_s_jetfuel_pct_energy
        + b18_s_diesel_pct_energy
        + b18_s_fueloil_pct_energy
        + b18_s_biomass_pct_energy
        + b18_s_coal_pct_energy
        + b18_s_heatnet_pct_energy
        + b18_s_heatpump_pct_energy
        + b18_s_solarth_pct_energy
        + b18_s_elec_pct_energy
    )

    # NACHFRAGE:
    b18_p_nonresi_area_m2 = (
        entry("In_R_area_m2")
        * fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016")
        / (1 - fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016"))
        * (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
    )

    b18_p_nonresi_com_pct_x = ass(
        "Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050"
    )
    b18_p_nonresi_com_area_m2 = b18_p_nonresi_area_m2 * b18_p_nonresi_com_pct_x
    b18_p_nonresi_energy = (
        b18_s_gas_energy
        + b18_s_lpg_energy
        + b18_s_fueloil_energy
        + b18_s_biomass_energy
        + b18_s_coal_energy
        + b18_s_heatnet_energy
        + b18_s_heatpump_energy
        + b18_s_solarth_energy
        + b18_s_elec_heating_energy
    )
    # 187.870.374 MWh

    b18_p_nonresi_com_energy = b18_p_nonresi_energy * b18_p_nonresi_com_pct_x
    # 38.712.683 MWh

    b18_p_nonresi_number_of_buildings = (
        fact("Fact_B_P_number_business_buildings_2016")
        * entry("In_M_population_com_2018")
        / entry("In_M_population_nat")
    )

    b18_p_nonresi_com_factor_adapted_to_fec = div(
        b18_p_nonresi_com_energy, b18_p_nonresi_com_area_m2
    )

    # Elektrische Energie / Bisherige elektrische Verbraucher

    # Wärmepumpen
    b18_p_elec_heatpump_energy = b18_s_heatpump_energy / fact(
        "Fact_R_S_heatpump_mean_annual_performance_factor_all"
    )

    b18_p_elec_elcon_energy = b18_p_elec_elcon_energy = (
        b18_s_elec_energy - b18_p_elec_heatpump_energy - b18_s_elec_heating_energy
    )
    b18_p_vehicles_energy = (
        b18_s_petrol_energy + b18_s_jetfuel_energy + b18_s_diesel_energy
    )
    b18_p_other_energy = (
        b18_p_elec_elcon_energy + b18_p_elec_heatpump_energy + b18_p_vehicles_energy
    )  # SUM(p_elec_elcon.energy:p_vehicles.energy)
    b18_p_energy = b18_p_nonresi_energy + b18_p_other_energy
    b18_p_nonresi_factor_adapted_to_fec = div(
        b18_p_nonresi_energy, b18_p_nonresi_area_m2
    )

    b18_p_elec_elcon_demand_change = ass("Ass_R_D_fec_elec_elcon_change")

    b18_p_vehicles_demand_change = ass("Ass_B_D_fec_vehicles_change")

    b18_p_vehicles_demand_ediesel = b18_p_vehicles_energy * (
        1 + b18_p_vehicles_demand_change
    )

    # Primärenergiekosten
    b18_s_gas_cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")
    b18_s_lpg_cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    b18_s_petrol_cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    b18_s_jetfuel_cost_fuel_per_MWh = fact("Fact_R_S_kerosine_energy_cost_factor_2018")
    b18_s_diesel_cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    b18_s_fueloil_cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    b18_s_biomass_cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    b18_s_coal_cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    b18_s_heatnet_cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    b18_s_heatpump_cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )

    b18_s_solarth_cost_fuel_per_MWh = 0

    b18_s_gas_cost_fuel = b18_s_gas_energy * b18_s_gas_cost_fuel_per_MWh / Million

    b18_s_lpg_cost_fuel = b18_s_lpg_energy * b18_s_lpg_cost_fuel_per_MWh / Million
    b18_s_petrol_cost_fuel = (
        b18_s_petrol_energy * b18_s_petrol_cost_fuel_per_MWh / Million
    )
    b18_s_jetfuel_cost_fuel = (
        b18_s_jetfuel_energy * b18_s_jetfuel_cost_fuel_per_MWh / Million
    )
    b18_s_diesel_cost_fuel = (
        b18_s_diesel_energy * b18_s_diesel_cost_fuel_per_MWh / Million
    )
    b18_s_fueloil_cost_fuel = (
        b18_s_fueloil_energy * b18_s_fueloil_cost_fuel_per_MWh / Million
    )
    b18_s_biomass_cost_fuel = (
        b18_s_biomass_energy * b18_s_biomass_cost_fuel_per_MWh / Million
    )
    b18_s_coal_cost_fuel = b18_s_coal_energy * b18_s_coal_cost_fuel_per_MWh / Million
    b18_s_heatnet_cost_fuel = (
        b18_s_heatnet_energy * b18_s_heatnet_cost_fuel_per_MWh / Million
    )
    b18_s_heatpump_cost_fuel = (
        b18_s_heatpump_energy * b18_s_heatpump_cost_fuel_per_MWh / Million
    )
    b18_s_solarth_cost_fuel = 0

    b18_s_cost_fuel = (
        b18_s_gas_cost_fuel
        + b18_s_lpg_cost_fuel
        + b18_s_petrol_cost_fuel
        + b18_s_jetfuel_cost_fuel
        + b18_s_diesel_cost_fuel
        + b18_s_fueloil_cost_fuel
        + b18_s_biomass_cost_fuel
        + b18_s_coal_cost_fuel
        + b18_s_heatnet_cost_fuel
        + b18_s_heatpump_cost_fuel
        + b18_s_solarth_cost_fuel
    )

    # Energiebedingte THG-Emissionen
    b18_s_gas_CO2e_cb_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    b18_s_lpg_CO2e_cb_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    b18_s_petrol_CO2e_cb_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    b18_s_jetfuel_CO2e_cb_per_MWh = fact("Fact_H_P_kerosene_cb_EF")
    b18_s_diesel_CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    b18_s_fueloil_CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    b18_s_biomass_CO2e_cb_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    b18_s_coal_CO2e_cb_per_MWh = fact("Fact_R_S_coal_CO2e_EF")

    b18_s_gas_CO2e_cb = b18_s_gas_energy * b18_s_gas_CO2e_cb_per_MWh
    b18_s_lpg_CO2e_cb = b18_s_lpg_energy * b18_s_lpg_CO2e_cb_per_MWh
    b18_s_petrol_CO2e_cb = b18_s_petrol_energy * b18_s_petrol_CO2e_cb_per_MWh
    b18_s_jetfuel_CO2e_cb = b18_s_jetfuel_energy * b18_s_jetfuel_CO2e_cb_per_MWh
    b18_s_diesel_CO2e_cb = b18_s_diesel_energy * b18_s_diesel_CO2e_cb_per_MWh
    b18_s_fueloil_CO2e_cb = b18_s_fueloil_energy * b18_s_fueloil_CO2e_cb_per_MWh
    b18_s_biomass_CO2e_cb = b18_s_biomass_energy * b18_s_biomass_CO2e_cb_per_MWh
    b18_s_coal_CO2e_cb = b18_s_coal_energy * b18_s_coal_CO2e_cb_per_MWh

    b18_s_CO2e_cb = (
        b18_s_gas_CO2e_cb
        + b18_s_lpg_CO2e_cb
        + b18_s_petrol_CO2e_cb
        + b18_s_jetfuel_CO2e_cb
        + b18_s_diesel_CO2e_cb
        + b18_s_fueloil_CO2e_cb
        + b18_s_biomass_CO2e_cb
        + b18_s_coal_CO2e_cb
    )
    b18_s_CO2e_total = b18_s_CO2e_cb

    b18_p_elec_elcon_demand_electricity = (
        b18_p_elec_elcon_energy
        * (entry("In_M_population_com_203X") / entry("In_M_population_com_2018"))
        * (1 + b18_p_elec_elcon_demand_change)
    )

    b18_CO2e_cb_ = b18_s_CO2e_cb
    b18_CO2e_total_ = b18_s_CO2e_total
    b18_s_gas_CO2e_total = b18_s_gas_CO2e_cb
    b18_s_lpg_CO2e_total = b18_s_lpg_CO2e_cb
    b18_s_petrol_CO2e_total = b18_s_petrol_CO2e_cb
    b18_s_jetfuel_CO2e_total = b18_s_jetfuel_CO2e_cb
    b18_s_diesel_CO2e_total = b18_s_diesel_CO2e_cb
    b18_s_fueloil_CO2e_total = b18_s_fueloil_CO2e_cb
    b18_s_biomass_CO2e_total = b18_s_biomass_CO2e_cb
    b18_s_coal_CO2e_total = b18_s_coal_CO2e_cb
    b18_s_biomass_number_of_buildings = (
        b18_s_biomass_energy
        * b18_p_nonresi_number_of_buildings
        / (b18_p_nonresi_factor_adapted_to_fec * b18_p_nonresi_area_m2)
    )
    b18_rp_p_CO2e_cb = (
        r18.s.CO2e_cb
        - r18.s_petrol.CO2e_cb
        + b18_s_CO2e_cb
        - b18_s_petrol_CO2e_cb
        - b18_s_jetfuel_CO2e_cb
        - b18_s_diesel_CO2e_cb
    )
    b18_rp_p_CO2e_total = r18.s.CO2e_cb + b18_s_CO2e_cb
    b18_rb_energy = r18.p.energy + b18_p_energy
    b18_b_CO2e_cb = b18_s_CO2e_cb
    b18_rb_CO2e_cb = r18.r.CO2e_cb + b18_b_CO2e_cb
    b18_rb_CO2e_total = b18_rb_CO2e_cb
    b18_b_CO2e_total = b18_s_CO2e_total

    b18_b_CO2e_pb = 0
    b18_s_heatnet_CO2e_cb = 0
    b18_s_heatnet_CO2e_cb_per_MWh = 0
    b18_s_heatnet_CO2e_total = 0
    b18_s_heatpump_CO2e_cb = 0
    b18_s_heatpump_CO2e_cb_per_MWh = 0
    b18_s_heatpump_CO2e_total = 0
    b18_s_solarth_CO2e_cb = 0
    b18_s_solarth_CO2e_cb_per_MWh = 0
    b18_s_solarth_CO2e_total = 0
    b18_s_elec_CO2e_cb = 0
    b18_s_elec_CO2e_cb_per_MWh = 0
    b18_s_elec_CO2e_total = 0
    b18_s_elec_heating_CO2e_cb = 0
    b18_s_elec_heating_CO2e_cb_per_MWh = 0
    b18_s_elec_heating_CO2e_total = 0

    return B18(
        b_energy=b18_b_energy,
        b_pct_x=b18_b_pct_x,
        b_pct_energy=b18_b_pct_energy,
        b_area_m2=b18_b_area_m2,
        b_factor_adapted_to_fec=b18_b_factor_adapted_to_fec,
        b_cost_fuel=b18_b_cost_fuel,
        b_cost_fuel_per_MWh=b18_b_cost_fuel_per_MWh,
        b_CO2e_cb=b18_b_CO2e_cb,
        b_CO2e_cb_per_MWh=b18_b_CO2e_cb_per_MWh,
        b_CO2e_pb=b18_b_CO2e_pb,
        b_CO2e_total=b18_b_CO2e_total,
        b_number_of_buildings=b18_b_number_of_buildings,
        g_energy=b18_g_energy,
        g_pct_x=b18_g_pct_x,
        g_pct_energy=b18_g_pct_energy,
        g_area_m2=b18_g_area_m2,
        g_factor_adapted_to_fec=b18_g_factor_adapted_to_fec,
        g_cost_fuel=b18_g_cost_fuel,
        g_cost_fuel_per_MWh=b18_g_cost_fuel_per_MWh,
        g_CO2e_cb=b18_g_CO2e_cb,
        g_CO2e_cb_per_MWh=b18_g_CO2e_cb_per_MWh,
        g_CO2e_pb=b18_g_CO2e_pb,
        g_CO2e_total=b18_g_CO2e_total,
        g_number_of_buildings=b18_g_number_of_buildings,
        g_consult_energy=b18_g_consult_energy,
        g_consult_pct_x=b18_g_consult_pct_x,
        g_consult_pct_energy=b18_g_consult_pct_energy,
        g_consult_area_m2=b18_g_consult_area_m2,
        g_consult_factor_adapted_to_fec=b18_g_consult_factor_adapted_to_fec,
        g_consult_cost_fuel=b18_g_consult_cost_fuel,
        g_consult_cost_fuel_per_MWh=b18_g_consult_cost_fuel_per_MWh,
        g_consult_CO2e_cb=b18_g_consult_CO2e_cb,
        g_consult_CO2e_cb_per_MWh=b18_g_consult_CO2e_cb_per_MWh,
        g_consult_CO2e_pb=b18_g_consult_CO2e_pb,
        g_consult_CO2e_total=b18_g_consult_CO2e_total,
        g_consult_number_of_buildings=b18_g_consult_number_of_buildings,
        p_energy=b18_p_energy,
        p_pct_x=b18_p_pct_x,
        p_pct_energy=b18_p_pct_energy,
        p_area_m2=b18_p_area_m2,
        p_factor_adapted_to_fec=b18_p_factor_adapted_to_fec,
        p_cost_fuel=b18_p_cost_fuel,
        p_cost_fuel_per_MWh=b18_p_cost_fuel_per_MWh,
        p_CO2e_cb=b18_p_CO2e_cb,
        p_CO2e_cb_per_MWh=b18_p_CO2e_cb_per_MWh,
        p_CO2e_pb=b18_p_CO2e_pb,
        p_CO2e_total=b18_p_CO2e_total,
        p_number_of_buildings=b18_p_number_of_buildings,
        p_nonresi_energy=b18_p_nonresi_energy,
        p_nonresi_pct_x=b18_p_nonresi_pct_x,
        p_nonresi_pct_energy=b18_p_nonresi_pct_energy,
        p_nonresi_area_m2=b18_p_nonresi_area_m2,
        p_nonresi_factor_adapted_to_fec=b18_p_nonresi_factor_adapted_to_fec,
        p_nonresi_cost_fuel=b18_p_nonresi_cost_fuel,
        p_nonresi_cost_fuel_per_MWh=b18_p_nonresi_cost_fuel_per_MWh,
        p_nonresi_CO2e_cb=b18_p_nonresi_CO2e_cb,
        p_nonresi_CO2e_cb_per_MWh=b18_p_nonresi_CO2e_cb_per_MWh,
        p_nonresi_CO2e_pb=b18_p_nonresi_CO2e_pb,
        p_nonresi_CO2e_total=b18_p_nonresi_CO2e_total,
        p_nonresi_number_of_buildings=b18_p_nonresi_number_of_buildings,
        p_nonresi_com_energy=b18_p_nonresi_com_energy,
        p_nonresi_com_pct_x=b18_p_nonresi_com_pct_x,
        p_nonresi_com_pct_energy=b18_p_nonresi_com_pct_energy,
        p_nonresi_com_area_m2=b18_p_nonresi_com_area_m2,
        p_nonresi_com_factor_adapted_to_fec=b18_p_nonresi_com_factor_adapted_to_fec,
        p_nonresi_com_cost_fuel=b18_p_nonresi_com_cost_fuel,
        p_nonresi_com_cost_fuel_per_MWh=b18_p_nonresi_com_cost_fuel_per_MWh,
        p_nonresi_com_CO2e_cb=b18_p_nonresi_com_CO2e_cb,
        p_nonresi_com_CO2e_cb_per_MWh=b18_p_nonresi_com_CO2e_cb_per_MWh,
        p_nonresi_com_CO2e_pb=b18_p_nonresi_com_CO2e_pb,
        p_nonresi_com_CO2e_total=b18_p_nonresi_com_CO2e_total,
        p_nonresi_com_number_of_buildings=b18_p_nonresi_com_number_of_buildings,
        p_elec_elcon_energy=b18_p_elec_elcon_energy,
        p_elec_elcon_pct_x=b18_p_elec_elcon_pct_x,
        p_elec_elcon_pct_energy=b18_p_elec_elcon_pct_energy,
        p_elec_elcon_area_m2=b18_p_elec_elcon_area_m2,
        p_elec_elcon_factor_adapted_to_fec=b18_p_elec_elcon_factor_adapted_to_fec,
        p_elec_elcon_cost_fuel=b18_p_elec_elcon_cost_fuel,
        p_elec_elcon_cost_fuel_per_MWh=b18_p_elec_elcon_cost_fuel_per_MWh,
        p_elec_elcon_CO2e_cb=b18_p_elec_elcon_CO2e_cb,
        p_elec_elcon_CO2e_cb_per_MWh=b18_p_elec_elcon_CO2e_cb_per_MWh,
        p_elec_elcon_CO2e_pb=b18_p_elec_elcon_CO2e_pb,
        p_elec_elcon_CO2e_total=b18_p_elec_elcon_CO2e_total,
        p_elec_elcon_number_of_buildings=b18_p_elec_elcon_number_of_buildings,
        p_elec_heatpump_energy=b18_p_elec_heatpump_energy,
        p_elec_heatpump_pct_x=b18_p_elec_heatpump_pct_x,
        p_elec_heatpump_pct_energy=b18_p_elec_heatpump_pct_energy,
        p_elec_heatpump_area_m2=b18_p_elec_heatpump_area_m2,
        p_elec_heatpump_factor_adapted_to_fec=b18_p_elec_heatpump_factor_adapted_to_fec,
        p_elec_heatpump_cost_fuel=b18_p_elec_heatpump_cost_fuel,
        p_elec_heatpump_cost_fuel_per_MWh=b18_p_elec_heatpump_cost_fuel_per_MWh,
        p_elec_heatpump_CO2e_cb=b18_p_elec_heatpump_CO2e_cb,
        p_elec_heatpump_CO2e_cb_per_MWh=b18_p_elec_heatpump_CO2e_cb_per_MWh,
        p_elec_heatpump_CO2e_pb=b18_p_elec_heatpump_CO2e_pb,
        p_elec_heatpump_CO2e_total=b18_p_elec_heatpump_CO2e_total,
        p_elec_heatpump_number_of_buildings=b18_p_elec_heatpump_number_of_buildings,
        p_vehicles_energy=b18_p_vehicles_energy,
        p_vehicles_pct_x=b18_p_vehicles_pct_x,
        p_vehicles_pct_energy=b18_p_vehicles_pct_energy,
        p_vehicles_area_m2=b18_p_vehicles_area_m2,
        p_vehicles_factor_adapted_to_fec=b18_p_vehicles_factor_adapted_to_fec,
        p_vehicles_cost_fuel=b18_p_vehicles_cost_fuel,
        p_vehicles_cost_fuel_per_MWh=b18_p_vehicles_cost_fuel_per_MWh,
        p_vehicles_CO2e_cb=b18_p_vehicles_CO2e_cb,
        p_vehicles_CO2e_cb_per_MWh=b18_p_vehicles_CO2e_cb_per_MWh,
        p_vehicles_CO2e_pb=b18_p_vehicles_CO2e_pb,
        p_vehicles_CO2e_total=b18_p_vehicles_CO2e_total,
        p_vehicles_number_of_buildings=b18_p_vehicles_number_of_buildings,
        p_other_energy=b18_p_other_energy,
        p_other_pct_x=b18_p_other_pct_x,
        p_other_pct_energy=b18_p_other_pct_energy,
        p_other_area_m2=b18_p_other_area_m2,
        p_other_factor_adapted_to_fec=b18_p_other_factor_adapted_to_fec,
        p_other_cost_fuel=b18_p_other_cost_fuel,
        p_other_cost_fuel_per_MWh=b18_p_other_cost_fuel_per_MWh,
        p_other_CO2e_cb=b18_p_other_CO2e_cb,
        p_other_CO2e_cb_per_MWh=b18_p_other_CO2e_cb_per_MWh,
        p_other_CO2e_pb=b18_p_other_CO2e_pb,
        p_other_CO2e_total=b18_p_other_CO2e_total,
        p_other_number_of_buildings=b18_p_other_number_of_buildings,
        s_energy=b18_s_energy,
        s_pct_x=b18_s_pct_x,
        s_pct_energy=b18_s_pct_energy,
        s_area_m2=b18_s_area_m2,
        s_factor_adapted_to_fec=b18_s_factor_adapted_to_fec,
        s_cost_fuel=b18_s_cost_fuel,
        s_cost_fuel_per_MWh=b18_s_cost_fuel_per_MWh,
        s_CO2e_cb=b18_s_CO2e_cb,
        s_CO2e_cb_per_MWh=b18_s_CO2e_cb_per_MWh,
        s_CO2e_pb=b18_s_CO2e_pb,
        s_CO2e_total=b18_s_CO2e_total,
        s_number_of_buildings=b18_s_number_of_buildings,
        s_gas_energy=b18_s_gas_energy,
        s_gas_pct_x=b18_s_gas_pct_x,
        s_gas_pct_energy=b18_s_gas_pct_energy,
        s_gas_area_m2=b18_s_gas_area_m2,
        s_gas_factor_adapted_to_fec=b18_s_gas_factor_adapted_to_fec,
        s_gas_cost_fuel=b18_s_gas_cost_fuel,
        s_gas_cost_fuel_per_MWh=b18_s_gas_cost_fuel_per_MWh,
        s_gas_CO2e_cb=b18_s_gas_CO2e_cb,
        s_gas_CO2e_cb_per_MWh=b18_s_gas_CO2e_cb_per_MWh,
        s_gas_CO2e_pb=b18_s_gas_CO2e_pb,
        s_gas_CO2e_total=b18_s_gas_CO2e_total,
        s_gas_number_of_buildings=b18_s_gas_number_of_buildings,
        s_emethan_energy=b18_s_emethan_energy,
        s_emethan_pct_x=b18_s_emethan_pct_x,
        s_emethan_pct_energy=b18_s_emethan_pct_energy,
        s_emethan_area_m2=b18_s_emethan_area_m2,
        s_emethan_factor_adapted_to_fec=b18_s_emethan_factor_adapted_to_fec,
        s_emethan_cost_fuel=b18_s_emethan_cost_fuel,
        s_emethan_cost_fuel_per_MWh=b18_s_emethan_cost_fuel_per_MWh,
        s_emethan_CO2e_cb=b18_s_emethan_CO2e_cb,
        s_emethan_CO2e_cb_per_MWh=b18_s_emethan_CO2e_cb_per_MWh,
        s_emethan_CO2e_pb=b18_s_emethan_CO2e_pb,
        s_emethan_CO2e_total=b18_s_emethan_CO2e_total,
        s_emethan_number_of_buildings=b18_s_emethan_number_of_buildings,
        s_lpg_energy=b18_s_lpg_energy,
        s_lpg_pct_x=b18_s_lpg_pct_x,
        s_lpg_pct_energy=b18_s_lpg_pct_energy,
        s_lpg_area_m2=b18_s_lpg_area_m2,
        s_lpg_factor_adapted_to_fec=b18_s_lpg_factor_adapted_to_fec,
        s_lpg_cost_fuel=b18_s_lpg_cost_fuel,
        s_lpg_cost_fuel_per_MWh=b18_s_lpg_cost_fuel_per_MWh,
        s_lpg_CO2e_cb=b18_s_lpg_CO2e_cb,
        s_lpg_CO2e_cb_per_MWh=b18_s_lpg_CO2e_cb_per_MWh,
        s_lpg_CO2e_pb=b18_s_lpg_CO2e_pb,
        s_lpg_CO2e_total=b18_s_lpg_CO2e_total,
        s_lpg_number_of_buildings=b18_s_lpg_number_of_buildings,
        s_petrol_energy=b18_s_petrol_energy,
        s_petrol_pct_x=b18_s_petrol_pct_x,
        s_petrol_pct_energy=b18_s_petrol_pct_energy,
        s_petrol_area_m2=b18_s_petrol_area_m2,
        s_petrol_factor_adapted_to_fec=b18_s_petrol_factor_adapted_to_fec,
        s_petrol_cost_fuel=b18_s_petrol_cost_fuel,
        s_petrol_cost_fuel_per_MWh=b18_s_petrol_cost_fuel_per_MWh,
        s_petrol_CO2e_cb=b18_s_petrol_CO2e_cb,
        s_petrol_CO2e_cb_per_MWh=b18_s_petrol_CO2e_cb_per_MWh,
        s_petrol_CO2e_pb=b18_s_petrol_CO2e_pb,
        s_petrol_CO2e_total=b18_s_petrol_CO2e_total,
        s_petrol_number_of_buildings=b18_s_petrol_number_of_buildings,
        s_jetfuel_energy=b18_s_jetfuel_energy,
        s_jetfuel_pct_x=b18_s_jetfuel_pct_x,
        s_jetfuel_pct_energy=b18_s_jetfuel_pct_energy,
        s_jetfuel_area_m2=b18_s_jetfuel_area_m2,
        s_jetfuel_factor_adapted_to_fec=b18_s_jetfuel_factor_adapted_to_fec,
        s_jetfuel_cost_fuel=b18_s_jetfuel_cost_fuel,
        s_jetfuel_cost_fuel_per_MWh=b18_s_jetfuel_cost_fuel_per_MWh,
        s_jetfuel_CO2e_cb=b18_s_jetfuel_CO2e_cb,
        s_jetfuel_CO2e_cb_per_MWh=b18_s_jetfuel_CO2e_cb_per_MWh,
        s_jetfuel_CO2e_pb=b18_s_jetfuel_CO2e_pb,
        s_jetfuel_CO2e_total=b18_s_jetfuel_CO2e_total,
        s_jetfuel_number_of_buildings=b18_s_jetfuel_number_of_buildings,
        s_diesel_energy=b18_s_diesel_energy,
        s_diesel_pct_x=b18_s_diesel_pct_x,
        s_diesel_pct_energy=b18_s_diesel_pct_energy,
        s_diesel_area_m2=b18_s_diesel_area_m2,
        s_diesel_factor_adapted_to_fec=b18_s_diesel_factor_adapted_to_fec,
        s_diesel_cost_fuel=b18_s_diesel_cost_fuel,
        s_diesel_cost_fuel_per_MWh=b18_s_diesel_cost_fuel_per_MWh,
        s_diesel_CO2e_cb=b18_s_diesel_CO2e_cb,
        s_diesel_CO2e_cb_per_MWh=b18_s_diesel_CO2e_cb_per_MWh,
        s_diesel_CO2e_pb=b18_s_diesel_CO2e_pb,
        s_diesel_CO2e_total=b18_s_diesel_CO2e_total,
        s_diesel_number_of_buildings=b18_s_diesel_number_of_buildings,
        s_fueloil_energy=b18_s_fueloil_energy,
        s_fueloil_pct_x=b18_s_fueloil_pct_x,
        s_fueloil_pct_energy=b18_s_fueloil_pct_energy,
        s_fueloil_area_m2=b18_s_fueloil_area_m2,
        s_fueloil_factor_adapted_to_fec=b18_s_fueloil_factor_adapted_to_fec,
        s_fueloil_cost_fuel=b18_s_fueloil_cost_fuel,
        s_fueloil_cost_fuel_per_MWh=b18_s_fueloil_cost_fuel_per_MWh,
        s_fueloil_CO2e_cb=b18_s_fueloil_CO2e_cb,
        s_fueloil_CO2e_cb_per_MWh=b18_s_fueloil_CO2e_cb_per_MWh,
        s_fueloil_CO2e_pb=b18_s_fueloil_CO2e_pb,
        s_fueloil_CO2e_total=b18_s_fueloil_CO2e_total,
        s_fueloil_number_of_buildings=b18_s_fueloil_number_of_buildings,
        s_biomass_energy=b18_s_biomass_energy,
        s_biomass_pct_x=b18_s_biomass_pct_x,
        s_biomass_pct_energy=b18_s_biomass_pct_energy,
        s_biomass_area_m2=b18_s_biomass_area_m2,
        s_biomass_factor_adapted_to_fec=b18_s_biomass_factor_adapted_to_fec,
        s_biomass_cost_fuel=b18_s_biomass_cost_fuel,
        s_biomass_cost_fuel_per_MWh=b18_s_biomass_cost_fuel_per_MWh,
        s_biomass_CO2e_cb=b18_s_biomass_CO2e_cb,
        s_biomass_CO2e_cb_per_MWh=b18_s_biomass_CO2e_cb_per_MWh,
        s_biomass_CO2e_pb=b18_s_biomass_CO2e_pb,
        s_biomass_CO2e_total=b18_s_biomass_CO2e_total,
        s_biomass_number_of_buildings=b18_s_biomass_number_of_buildings,
        s_coal_energy=b18_s_coal_energy,
        s_coal_pct_x=b18_s_coal_pct_x,
        s_coal_pct_energy=b18_s_coal_pct_energy,
        s_coal_area_m2=b18_s_coal_area_m2,
        s_coal_factor_adapted_to_fec=b18_s_coal_factor_adapted_to_fec,
        s_coal_cost_fuel=b18_s_coal_cost_fuel,
        s_coal_cost_fuel_per_MWh=b18_s_coal_cost_fuel_per_MWh,
        s_coal_CO2e_cb=b18_s_coal_CO2e_cb,
        s_coal_CO2e_cb_per_MWh=b18_s_coal_CO2e_cb_per_MWh,
        s_coal_CO2e_pb=b18_s_coal_CO2e_pb,
        s_coal_CO2e_total=b18_s_coal_CO2e_total,
        s_coal_number_of_buildings=b18_s_coal_number_of_buildings,
        s_heatnet_energy=b18_s_heatnet_energy,
        s_heatnet_pct_x=b18_s_heatnet_pct_x,
        s_heatnet_pct_energy=b18_s_heatnet_pct_energy,
        s_heatnet_area_m2=b18_s_heatnet_area_m2,
        s_heatnet_factor_adapted_to_fec=b18_s_heatnet_factor_adapted_to_fec,
        s_heatnet_cost_fuel=b18_s_heatnet_cost_fuel,
        s_heatnet_cost_fuel_per_MWh=b18_s_heatnet_cost_fuel_per_MWh,
        s_heatnet_CO2e_cb=b18_s_heatnet_CO2e_cb,
        s_heatnet_CO2e_cb_per_MWh=b18_s_heatnet_CO2e_cb_per_MWh,
        s_heatnet_CO2e_pb=b18_s_heatnet_CO2e_pb,
        s_heatnet_CO2e_total=b18_s_heatnet_CO2e_total,
        s_heatnet_number_of_buildings=b18_s_heatnet_number_of_buildings,
        s_elec_heating_energy=b18_s_elec_heating_energy,
        s_elec_heating_pct_x=b18_s_elec_heating_pct_x,
        s_elec_heating_pct_energy=b18_s_elec_heating_pct_energy,
        s_elec_heating_area_m2=b18_s_elec_heating_area_m2,
        s_elec_heating_factor_adapted_to_fec=b18_s_elec_heating_factor_adapted_to_fec,
        s_elec_heating_cost_fuel=b18_s_elec_heating_cost_fuel,
        s_elec_heating_cost_fuel_per_MWh=b18_s_elec_heating_cost_fuel_per_MWh,
        s_elec_heating_CO2e_cb=b18_s_elec_heating_CO2e_cb,
        s_elec_heating_CO2e_cb_per_MWh=b18_s_elec_heating_CO2e_cb_per_MWh,
        s_elec_heating_CO2e_pb=b18_s_elec_heating_CO2e_pb,
        s_elec_heating_CO2e_total=b18_s_elec_heating_CO2e_total,
        s_elec_heating_number_of_buildings=b18_s_elec_heating_number_of_buildings,
        s_heatpump_energy=b18_s_heatpump_energy,
        s_heatpump_pct_x=b18_s_heatpump_pct_x,
        s_heatpump_pct_energy=b18_s_heatpump_pct_energy,
        s_heatpump_area_m2=b18_s_heatpump_area_m2,
        s_heatpump_factor_adapted_to_fec=b18_s_heatpump_factor_adapted_to_fec,
        s_heatpump_cost_fuel=b18_s_heatpump_cost_fuel,
        s_heatpump_cost_fuel_per_MWh=b18_s_heatpump_cost_fuel_per_MWh,
        s_heatpump_CO2e_cb=b18_s_heatpump_CO2e_cb,
        s_heatpump_CO2e_cb_per_MWh=b18_s_heatpump_CO2e_cb_per_MWh,
        s_heatpump_CO2e_pb=b18_s_heatpump_CO2e_pb,
        s_heatpump_CO2e_total=b18_s_heatpump_CO2e_total,
        s_heatpump_number_of_buildings=b18_s_heatpump_number_of_buildings,
        s_solarth_energy=b18_s_solarth_energy,
        s_solarth_pct_x=b18_s_solarth_pct_x,
        s_solarth_pct_energy=b18_s_solarth_pct_energy,
        s_solarth_area_m2=b18_s_solarth_area_m2,
        s_solarth_factor_adapted_to_fec=b18_s_solarth_factor_adapted_to_fec,
        s_solarth_cost_fuel=b18_s_solarth_cost_fuel,
        s_solarth_cost_fuel_per_MWh=b18_s_solarth_cost_fuel_per_MWh,
        s_solarth_CO2e_cb=b18_s_solarth_CO2e_cb,
        s_solarth_CO2e_cb_per_MWh=b18_s_solarth_CO2e_cb_per_MWh,
        s_solarth_CO2e_pb=b18_s_solarth_CO2e_pb,
        s_solarth_CO2e_total=b18_s_solarth_CO2e_total,
        s_solarth_number_of_buildings=b18_s_solarth_number_of_buildings,
        s_elec_energy=b18_s_elec_energy,
        s_elec_pct_x=b18_s_elec_pct_x,
        s_elec_pct_energy=b18_s_elec_pct_energy,
        s_elec_area_m2=b18_s_elec_area_m2,
        s_elec_factor_adapted_to_fec=b18_s_elec_factor_adapted_to_fec,
        s_elec_cost_fuel=b18_s_elec_cost_fuel,
        s_elec_cost_fuel_per_MWh=b18_s_elec_cost_fuel_per_MWh,
        s_elec_CO2e_cb=b18_s_elec_CO2e_cb,
        s_elec_CO2e_cb_per_MWh=b18_s_elec_CO2e_cb_per_MWh,
        s_elec_CO2e_pb=b18_s_elec_CO2e_pb,
        s_elec_CO2e_total=b18_s_elec_CO2e_total,
        s_elec_number_of_buildings=b18_s_elec_number_of_buildings,
        rb_energy=b18_rb_energy,
        rb_pct_x=b18_rb_pct_x,
        rb_pct_energy=b18_rb_pct_energy,
        rb_area_m2=b18_rb_area_m2,
        rb_factor_adapted_to_fec=b18_rb_factor_adapted_to_fec,
        rb_cost_fuel=b18_rb_cost_fuel,
        rb_cost_fuel_per_MWh=b18_rb_cost_fuel_per_MWh,
        rb_CO2e_cb=b18_rb_CO2e_cb,
        rb_CO2e_cb_per_MWh=b18_rb_CO2e_cb_per_MWh,
        rb_CO2e_pb=b18_rb_CO2e_pb,
        rb_CO2e_total=b18_rb_CO2e_total,
        rb_number_of_buildings=b18_rb_number_of_buildings,
        rp_p_energy=b18_rp_p_energy,
        rp_p_pct_x=b18_rp_p_pct_x,
        rp_p_pct_energy=b18_rp_p_pct_energy,
        rp_p_area_m2=b18_rp_p_area_m2,
        rp_p_factor_adapted_to_fec=b18_rp_p_factor_adapted_to_fec,
        rp_p_cost_fuel=b18_rp_p_cost_fuel,
        rp_p_cost_fuel_per_MWh=b18_rp_p_cost_fuel_per_MWh,
        rp_p_CO2e_cb=b18_rp_p_CO2e_cb,
        rp_p_CO2e_cb_per_MWh=b18_rp_p_CO2e_cb_per_MWh,
        rp_p_CO2e_pb=b18_rp_p_CO2e_pb,
        rp_p_CO2e_total=b18_rp_p_CO2e_total,
        rp_p_number_of_buildings=b18_rp_p_number_of_buildings,
    )
