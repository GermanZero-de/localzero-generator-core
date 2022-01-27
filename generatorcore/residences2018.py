from dataclasses import dataclass, asdict
from .inputs import Inputs


# Definition der relevanten Spaltennamen für den Sektor R18
@dataclass
class RColVars:
    energy: float = None
    number_of_buildings: float = None
    relative_building_ratio: float = None
    area_m2: float = None
    area_m2_relative_heat_ratio: float = None
    relative_building_ratio: float = None
    fec_after_BMWi: float = None
    fec_factor_BMWi: float = None
    factor_adapted_to_fec: float = None
    relative_heat_ratio_buildings_until_2004: float = None
    relative_heat_ratio_BMWi: float = None
    demand_change: float = None
    demand_change_pa: float = None
    demand_electricity: float = None
    cost_fuel: float = None
    cost_fuel_per_MWh: float = None
    CO2e_cb: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_total: float = None
    pct_x: float = None
    pct_energy: float = None


@dataclass
class R18:
    # Klassenvariablen für Residences
    g: RColVars = RColVars()
    r: RColVars = RColVars()
    g_consult: RColVars = RColVars()

    p: RColVars = RColVars()
    p_buildings_total: RColVars = RColVars()
    p_buildings_until_1919: RColVars = RColVars()
    p_buildings_1919_1948: RColVars = RColVars()
    p_buildings_1949_1978: RColVars = RColVars()
    p_buildings_1979_1995: RColVars = RColVars()
    p_buildings_1996_2004: RColVars = RColVars()
    p_buildings_2005_2011: RColVars = RColVars()
    p_buildings_2011_today: RColVars = RColVars()
    p_buildings_new: RColVars = RColVars()
    p_buildings_area_m2_com: RColVars = RColVars()
    p_elec_elcon: RColVars = RColVars()
    p_elec_heatpump: RColVars = RColVars()
    p_vehicles: RColVars = RColVars()
    p_other: RColVars = RColVars()
    r: RColVars = RColVars()
    s: RColVars = RColVars()
    s_fueloil: RColVars = RColVars()
    s_lpg: RColVars = RColVars()
    s_biomass: RColVars = RColVars()
    s_coal: RColVars = RColVars()
    s_petrol: RColVars = RColVars()
    s_heatnet: RColVars = RColVars()
    s_solarth: RColVars = RColVars()
    s_heatpump: RColVars = RColVars()
    s_emethan: RColVars = RColVars()
    s_elec_heating: RColVars = RColVars()
    s_gas: RColVars = RColVars()
    s_elec: RColVars = RColVars()

    # erzeuge dictionry

    def dict(self):
        return asdict(self)


class Generator:
    pass


def calc(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    ### P - Section ###
    r18 = root.r18
    p = r18.p
    r = r18.r
    p_buildings_total = r18.p_buildings_total
    p_buildings_until_1919 = r18.p_buildings_until_1919
    p_buildings_1919_1948 = r18.p_buildings_1919_1948
    p_buildings_1949_1978 = r18.p_buildings_1949_1978
    p_buildings_1979_1995 = r18.p_buildings_1979_1995
    p_buildings_1996_2004 = r18.p_buildings_1996_2004
    p_buildings_2005_2011 = r18.p_buildings_2005_2011
    p_buildings_2011_today = r18.p_buildings_2011_today
    p_buildings_new = r18.p_buildings_new
    p_buildings_area_m2_com = r18.p_buildings_area_m2_com
    p_other = r18.p_other
    p_vehicles = r18.p_vehicles

    p_buildings_until_1919.number_of_buildings = entry("In_R_buildings_until_1919")
    p_buildings_1919_1948.number_of_buildings = entry("In_R_buildings_1919_1948")
    p_buildings_1949_1978.number_of_buildings = entry("In_R_buildings_1949_1978")
    p_buildings_1979_1995.number_of_buildings = (
        entry("In_R_buildings_1979_1986")
        + entry("In_R_buildings_1987_1990")
        + entry("In_R_buildings_1991_1995")
    )
    p_buildings_1996_2004.number_of_buildings = entry(
        "In_R_buildings_1996_2000"
    ) + entry("In_R_buildings_2001_2004")
    p_buildings_2005_2011.number_of_buildings = entry(
        "In_R_buildings_2005_2008"
    ) + entry("In_R_buildings_2009_2011")
    p_buildings_2011_today.number_of_buildings = entry("In_R_buildings_2011_today")

    p_buildings_total.number_of_buildings = (
        p_buildings_until_1919.number_of_buildings
        + p_buildings_1919_1948.number_of_buildings
        + p_buildings_1949_1978.number_of_buildings
        + p_buildings_1979_1995.number_of_buildings
        + p_buildings_1996_2004.number_of_buildings
        + p_buildings_2005_2011.number_of_buildings
        + p_buildings_2011_today.number_of_buildings
    )

    p_buildings_until_1919.relative_building_ratio = (
        p_buildings_until_1919.number_of_buildings
        / p_buildings_total.number_of_buildings
    )
    p_buildings_1919_1948.relative_building_ratio = (
        p_buildings_1919_1948.number_of_buildings
        / p_buildings_total.number_of_buildings
    )
    p_buildings_1949_1978.relative_building_ratio = (
        p_buildings_1949_1978.number_of_buildings
        / p_buildings_total.number_of_buildings
    )
    p_buildings_1979_1995.relative_building_ratio = (
        p_buildings_1979_1995.number_of_buildings
        / p_buildings_total.number_of_buildings
    )
    p_buildings_1996_2004.relative_building_ratio = (
        p_buildings_1996_2004.number_of_buildings
        / p_buildings_total.number_of_buildings
    )
    p_buildings_2005_2011.relative_building_ratio = (
        p_buildings_2005_2011.number_of_buildings
        / p_buildings_total.number_of_buildings
    )
    p_buildings_2011_today.relative_building_ratio = (
        p_buildings_2011_today.number_of_buildings
        / p_buildings_total.number_of_buildings
    )

    p_buildings_total.relative_building_ratio = (
        p_buildings_until_1919.relative_building_ratio
        + p_buildings_1919_1948.relative_building_ratio
        + p_buildings_1949_1978.relative_building_ratio
        + p_buildings_1979_1995.relative_building_ratio
        + p_buildings_1996_2004.relative_building_ratio
        + p_buildings_2005_2011.relative_building_ratio
        + p_buildings_2011_today.relative_building_ratio
    )

    p_buildings_total.area_m2 = entry("In_R_area_m2")
    p_buildings_until_1919.area_m2 = (
        p_buildings_until_1919.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1919_1948.area_m2 = (
        p_buildings_1919_1948.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1949_1978.area_m2 = (
        p_buildings_1949_1978.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1979_1995.area_m2 = (
        p_buildings_1979_1995.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1996_2004.area_m2 = (
        p_buildings_1996_2004.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_2005_2011.area_m2 = (
        p_buildings_2005_2011.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_2011_today.area_m2 = (
        p_buildings_2011_today.relative_building_ratio * p_buildings_total.area_m2
    )

    p_buildings_until_1919.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_until_1919_2014"
    )
    p_buildings_1919_1948.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1919_1948_2014"
    )
    p_buildings_1949_1978.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1949_1978_2014"
    )
    p_buildings_1979_1995.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1979_1995_2014"
    )
    p_buildings_1996_2004.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1996_2002_2014"
    )
    p_buildings_2005_2011.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_2003_2009_2014"
    )
    p_buildings_2011_today.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_2010_2014_2014"
    )

    p_buildings_until_1919.fec_after_BMWi = (
        p_buildings_until_1919.fec_factor_BMWi * p_buildings_until_1919.area_m2
    )
    p_buildings_1919_1948.fec_after_BMWi = (
        p_buildings_1919_1948.fec_factor_BMWi * p_buildings_1919_1948.area_m2
    )
    p_buildings_1949_1978.fec_after_BMWi = (
        p_buildings_1949_1978.fec_factor_BMWi * p_buildings_1949_1978.area_m2
    )
    p_buildings_1979_1995.fec_after_BMWi = (
        p_buildings_1979_1995.fec_factor_BMWi * p_buildings_1979_1995.area_m2
    )
    p_buildings_1996_2004.fec_after_BMWi = (
        p_buildings_1996_2004.fec_factor_BMWi * p_buildings_1996_2004.area_m2
    )
    p_buildings_2005_2011.fec_after_BMWi = (
        p_buildings_2005_2011.fec_factor_BMWi * p_buildings_2005_2011.area_m2
    )
    p_buildings_2011_today.fec_after_BMWi = (
        p_buildings_2011_today.fec_factor_BMWi * p_buildings_2011_today.area_m2
    )

    p_buildings_total.fec_after_BMWi = (
        p_buildings_until_1919.fec_after_BMWi
        + p_buildings_1919_1948.fec_after_BMWi
        + p_buildings_1949_1978.fec_after_BMWi
        + p_buildings_1979_1995.fec_after_BMWi
        + p_buildings_1996_2004.fec_after_BMWi
        + p_buildings_2005_2011.fec_after_BMWi
        + p_buildings_2011_today.fec_after_BMWi
    )
    p_buildings_total.fec_factor_BMWi = (
        p_buildings_total.fec_after_BMWi / p_buildings_total.area_m2
    )

    p_buildings_until_1919.relative_heat_ratio_BMWi = (
        p_buildings_until_1919.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )
    p_buildings_1919_1948.relative_heat_ratio_BMWi = (
        p_buildings_1919_1948.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )
    p_buildings_1949_1978.relative_heat_ratio_BMWi = (
        p_buildings_1949_1978.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )
    p_buildings_1979_1995.relative_heat_ratio_BMWi = (
        p_buildings_1979_1995.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )
    p_buildings_1996_2004.relative_heat_ratio_BMWi = (
        p_buildings_1996_2004.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )
    p_buildings_2005_2011.relative_heat_ratio_BMWi = (
        p_buildings_2005_2011.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )
    p_buildings_2011_today.relative_heat_ratio_BMWi = (
        p_buildings_2011_today.fec_after_BMWi / p_buildings_total.fec_after_BMWi
    )

    p_buildings_total.relative_heat_ratio_BMWi = (
        p_buildings_until_1919.relative_heat_ratio_BMWi
        + p_buildings_1919_1948.relative_heat_ratio_BMWi
        + p_buildings_1949_1978.relative_heat_ratio_BMWi
        + p_buildings_1979_1995.relative_heat_ratio_BMWi
        + p_buildings_1996_2004.relative_heat_ratio_BMWi
        + p_buildings_2005_2011.relative_heat_ratio_BMWi
        + p_buildings_2011_today.relative_heat_ratio_BMWi
    )

    p_buildings_area_m2_com.pct_x = entry("In_R_pct_of_area_m2_com")
    p_buildings_area_m2_com.area_m2 = (
        p_buildings_total.area_m2 * p_buildings_area_m2_com.pct_x
    )

    p_buildings_until_1919.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_until_1919.fec_after_BMWi
        / (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        )
    )
    p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_1919_1948.fec_after_BMWi
        / (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        )
    )
    p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_1949_1978.fec_after_BMWi
        / (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        )
    )
    p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_1979_1995.fec_after_BMWi
        / (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        )
    )
    p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_1996_2004.fec_after_BMWi
        / (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        )
    )

    p_buildings_total.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_until_1919.relative_heat_ratio_buildings_until_2004
        + p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004
        + p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004
        + p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004
        + p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_until_1919.area_m2_relative_heat_ratio = (
        p_buildings_until_1919.area_m2
        * p_buildings_until_1919.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1919_1948.area_m2_relative_heat_ratio = (
        p_buildings_1919_1948.area_m2
        * p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1949_1978.area_m2_relative_heat_ratio = (
        p_buildings_1949_1978.area_m2
        * p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1979_1995.area_m2_relative_heat_ratio = (
        p_buildings_1979_1995.area_m2
        * p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1996_2004.area_m2_relative_heat_ratio = (
        p_buildings_1996_2004.area_m2
        * p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004
    )

    p_buildings_total.area_m2_relative_heat_ratio = (
        p_buildings_until_1919.area_m2_relative_heat_ratio
        + p_buildings_1919_1948.area_m2_relative_heat_ratio
        + p_buildings_1949_1978.area_m2_relative_heat_ratio
        + p_buildings_1979_1995.area_m2_relative_heat_ratio
        + p_buildings_1996_2004.area_m2_relative_heat_ratio
    )

    ### S - Section ###

    Million = 1000000

    # Definitions

    s = r18.s

    s_fueloil = root.r18.s_fueloil
    s_lpg = root.r18.s_lpg
    s_biomass = root.r18.s_biomass
    s_coal = root.r18.s_coal
    s_petrol = root.r18.s_petrol
    s_heatnet = root.r18.s_heatnet
    s_solarth = root.r18.s_solarth
    s_heatpump = root.r18.s_heatpump
    s_elec_heating = root.r18.s_elec_heating
    s_gas = root.r18.s_gas
    s_elec = root.r18.s_elec
    s_emethan = root.r18.s_emethan
    p_elec_elcon = root.r18.p_elec_elcon
    p_elec_heatpump = root.r18.p_elec_heatpump

    # Energy
    s_fueloil.energy = entry("In_R_fueloil_fec")
    s_lpg.energy = entry("In_R_lpg_fec")
    s_biomass.energy = entry("In_R_biomass_fec")
    s_coal.energy = entry("In_R_coal_fec")
    s_petrol.energy = entry("In_R_petrol_fec")
    s_heatnet.energy = entry("In_R_heatnet_fec")
    s_solarth.energy = entry("In_R_orenew_fec") * fact(
        "Fact_R_S_ratio_solarth_to_orenew_2018"
    )
    s_heatpump.energy = entry("In_R_orenew_fec") * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    s_gas.energy = entry("In_R_gas_fec")
    s_elec.energy = entry("In_R_elec_fec")
    s_elec_heating.energy = (
        fact("Fact_R_S_elec_heating_fec_2018")
        * entry("In_R_flats_wo_heatnet")
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )

    p_buildings_total.energy = (
        s_fueloil.energy
        + s_lpg.energy
        + s_biomass.energy
        + s_coal.energy
        + s_heatnet.energy
        + s_solarth.energy
        + s_heatpump.energy
        + s_gas.energy
        + s_elec_heating.energy
    )

    p_buildings_until_1919.energy = (
        p_buildings_total.energy * p_buildings_until_1919.relative_heat_ratio_BMWi
    )
    p_buildings_1919_1948.energy = (
        p_buildings_total.energy * p_buildings_1919_1948.relative_heat_ratio_BMWi
    )
    p_buildings_1949_1978.energy = (
        p_buildings_total.energy * p_buildings_1949_1978.relative_heat_ratio_BMWi
    )
    p_buildings_1979_1995.energy = (
        p_buildings_total.energy * p_buildings_1979_1995.relative_heat_ratio_BMWi
    )
    p_buildings_1996_2004.energy = (
        p_buildings_total.energy * p_buildings_1996_2004.relative_heat_ratio_BMWi
    )
    p_buildings_2005_2011.energy = (
        p_buildings_total.energy * p_buildings_2005_2011.relative_heat_ratio_BMWi
    )
    p_buildings_2011_today.energy = (
        p_buildings_total.energy * p_buildings_2011_today.relative_heat_ratio_BMWi
    )

    p_buildings_area_m2_com.energy = (
        p_buildings_total.energy * p_buildings_area_m2_com.pct_x
    )
    p_buildings_total.factor_adapted_to_fec = (
        p_buildings_total.energy / p_buildings_total.area_m2
    )
    p_buildings_until_1919.factor_adapted_to_fec = (
        p_buildings_until_1919.energy / p_buildings_until_1919.area_m2
    )
    p_buildings_1919_1948.factor_adapted_to_fec = (
        p_buildings_1919_1948.energy / p_buildings_1919_1948.area_m2
    )
    p_buildings_1949_1978.factor_adapted_to_fec = (
        p_buildings_1949_1978.energy / p_buildings_1949_1978.area_m2
    )
    p_buildings_1979_1995.factor_adapted_to_fec = (
        p_buildings_1979_1995.energy / p_buildings_1979_1995.area_m2
    )
    p_buildings_1996_2004.factor_adapted_to_fec = (
        p_buildings_1996_2004.energy / p_buildings_1996_2004.area_m2
    )
    p_buildings_2005_2011.factor_adapted_to_fec = (
        p_buildings_2005_2011.energy / p_buildings_2005_2011.area_m2
    )
    p_buildings_2011_today.factor_adapted_to_fec = (
        p_buildings_2011_today.energy / p_buildings_2011_today.area_m2
    )
    p_buildings_area_m2_com.factor_adapted_to_fec = (
        p_buildings_area_m2_com.energy / p_buildings_area_m2_com.area_m2
    )

    s.energy = (
        s_fueloil.energy
        + s_lpg.energy
        + s_biomass.energy
        + s_coal.energy
        + s_petrol.energy
        + s_heatnet.energy
        + s_solarth.energy
        + s_heatpump.energy
        + s_gas.energy
        + s_elec.energy
    )

    # pct_energy
    s_fueloil.pct_energy = s_fueloil.energy / s.energy
    s_lpg.pct_energy = s_lpg.energy / s.energy
    s_biomass.pct_energy = s_biomass.energy / s.energy
    s_coal.pct_energy = s_coal.energy / s.energy
    s_petrol.pct_energy = s_petrol.energy / s.energy
    s_heatnet.pct_energy = s_heatnet.energy / s.energy
    s_solarth.pct_energy = s_solarth.energy / s.energy
    s_heatpump.pct_energy = s_heatpump.energy / s.energy
    s_elec_heating.pct_energy = s_elec_heating.energy / s_elec.energy

    s_gas.pct_energy = s_gas.energy / s.energy
    s_elec.pct_energy = s_elec.energy / s.energy

    s.pct_energy = (
        s_fueloil.pct_energy
        + s_lpg.pct_energy
        + s_biomass.pct_energy
        + s_coal.pct_energy
        + s_petrol.pct_energy
        + s_heatnet.pct_energy
        + s_solarth.pct_energy
        + s_heatpump.pct_energy
        + s_gas.pct_energy
        + s_elec.pct_energy
    )

    # CO2e_cb_per_MWh
    s_lpg.CO2e_cb_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    s_fueloil.CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    s_biomass.CO2e_cb_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    s_coal.CO2e_cb_per_MWh = fact("Fact_R_S_coal_CO2e_EF")
    s_petrol.CO2e_cb_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    s_heatnet.CO2e_cb_per_MWh = fact("Fact_RB_S_heatnet_ratio_CO2e_to_fec")
    s_solarth.CO2e_cb_per_MWh = fact("Fact_RB_S_solarth_ratio_CO2e_to_fec")
    s_heatpump.CO2e_cb_per_MWh = fact("Fact_RB_S_heatpump_ratio_CO2e_to_fec")
    s_gas.CO2e_cb_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    s_elec.CO2e_cb_per_MWh = fact("Fact_RB_S_elec_ratio_CO2e_to_fec")
    s_elec_heating.CO2e_cb_per_MWh = fact("Fact_RB_S_elec_ratio_CO2e_to_fec")

    # CO2e_cb
    s_fueloil.CO2e_cb = s_fueloil.energy * s_fueloil.CO2e_cb_per_MWh
    s_lpg.CO2e_cb = s_lpg.energy * s_lpg.CO2e_cb_per_MWh
    s_biomass.CO2e_cb = s_biomass.energy * s_biomass.CO2e_cb_per_MWh
    s_coal.CO2e_cb = s_coal.energy * s_coal.CO2e_cb_per_MWh
    s_petrol.CO2e_cb = s_petrol.energy * s_petrol.CO2e_cb_per_MWh
    s_heatnet.CO2e_cb = s_heatnet.energy * s_heatnet.CO2e_cb_per_MWh
    s_solarth.CO2e_cb = s_solarth.energy * s_solarth.CO2e_cb_per_MWh
    s_heatpump.CO2e_cb = s_heatpump.energy * s_heatpump.CO2e_cb_per_MWh
    s_gas.CO2e_cb = s_gas.energy * s_gas.CO2e_cb_per_MWh
    s.CO2e_cb = (
        s_fueloil.CO2e_cb
        + s_lpg.CO2e_cb
        + s_biomass.CO2e_cb
        + s_coal.CO2e_cb
        + s_petrol.CO2e_cb
        + s_gas.CO2e_cb
    )

    s_elec.CO2e_cb = s_elec.energy * s_elec.CO2e_cb_per_MWh
    s_elec_heating.CO2e_cb = s_elec_heating.energy * s_elec_heating.CO2e_cb_per_MWh
    r.CO2e_cb = s.CO2e_cb

    # CO2e_total

    s.CO2e_total = s.CO2e_cb
    r.CO2e_total = s.CO2e_total

    s_fueloil.CO2e_total = s_fueloil.CO2e_cb
    s_lpg.CO2e_total = s_lpg.CO2e_cb
    s_biomass.CO2e_total = s_biomass.CO2e_cb
    s_coal.CO2e_total = s_coal.CO2e_cb
    s_petrol.CO2e_total = s_petrol.CO2e_cb
    s_heatnet.CO2e_total = s_heatnet.CO2e_cb
    s_solarth.CO2e_total = s_solarth.CO2e_cb
    s_heatpump.CO2e_total = s_heatpump.CO2e_cb
    s_gas.CO2e_total = s_gas.CO2e_cb
    s_elec.CO2e_total = s_elec.CO2e_cb

    # cost_fuel_per_MW
    s_fueloil.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    s_lpg.cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    s_biomass.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    s_coal.cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    s_petrol.cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    s_heatnet.cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    s_solarth.cost_fuel_per_MWh = 0
    s_heatpump.cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )
    s_elec_heating.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    s_gas.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")

    # cost_fuel
    s_fueloil.cost_fuel = s_fueloil.energy * s_fueloil.cost_fuel_per_MWh / Million
    s_lpg.cost_fuel = s_lpg.energy * s_lpg.cost_fuel_per_MWh / Million
    s_biomass.cost_fuel = s_biomass.energy * s_biomass.cost_fuel_per_MWh / Million
    s_coal.cost_fuel = s_coal.energy * s_coal.cost_fuel_per_MWh / Million
    s_petrol.cost_fuel = s_petrol.energy * s_petrol.cost_fuel_per_MWh / Million
    s_heatnet.cost_fuel = s_heatnet.energy * s_heatnet.cost_fuel_per_MWh / Million
    s_solarth.cost_fuel = s_solarth.energy * s_solarth.cost_fuel_per_MWh / Million
    s_heatpump.cost_fuel = s_heatpump.energy * s_heatpump.cost_fuel_per_MWh / Million
    s_elec_heating.cost_fuel = (
        s_elec_heating.energy * s_elec_heating.cost_fuel_per_MWh / Million
    )
    s_gas.cost_fuel = s_gas.energy * s_gas.cost_fuel_per_MWh / Million

    s.cost_fuel = (
        s_fueloil.cost_fuel
        + s_lpg.cost_fuel
        + s_biomass.cost_fuel
        + s_coal.cost_fuel
        + s_petrol.cost_fuel
        + s_heatnet.cost_fuel
        + s_solarth.cost_fuel
        + s_heatpump.cost_fuel
        + s_gas.cost_fuel
    )

    p_elec_heatpump.energy = s_heatpump.energy / fact(
        "Fact_R_S_heatpump_mean_annual_performance_factor_all"
    )

    p_elec_elcon.energy = s_elec.energy - p_elec_heatpump.energy - s_elec_heating.energy
    p_vehicles.energy = s_petrol.energy
    p_other.energy = p_elec_heatpump.energy + p_elec_elcon.energy + p_vehicles.energy

    p.energy = p_buildings_total.energy + p_other.energy

    s_biomass.number_of_buildings = (
        s_biomass.energy
        * p_buildings_total.number_of_buildings
        / (p_buildings_total.factor_adapted_to_fec * p_buildings_total.area_m2)
    )
