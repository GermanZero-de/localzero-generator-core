#!/usr/bin/env python
# coding: utf-8

from .setup import *
from dataclasses import dataclass, asdict


# Definition der relevanten Spaltennamen für den Sektor E
@dataclass
class EColVars2030:
    energy: float = None
    energy_installable: float = None
    cost_fuel_per_MWh: float = None
    cost_fuel: float = None
    pct_energy: float = None
    mro_per_MWh: float = None
    mro: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_cb: float = None
    cost_certificate_per_MWh: float = None
    cost_certificate: float = None
    cost_climate_saved: float = None
    cost_mro: float = None
    cost_mro_pa_com: float = None
    CO2e_total: float = None
    CO2e_total_2021_estimated: float = None
    demand_electricity: float = None
    demand_emplo_com: float = None
    power_installed: float = None
    power_to_be_installed_pct: float = None
    power_to_be_installed: float = None
    power_installable: float = None
    area_ha_available: float = None
    area_ha_available_pct_of_action: float = None
    ratio_power_to_area_ha: float = None
    cost_mro_pa: float = None
    change_energy_MWh: float = None
    change_energy_pct: float = None
    change_CO2e_t: float = None
    change_cost_energy: float = None
    change_cost_mro: float = None
    invest: float = None
    invest_pa: float = None
    invest_com: float = None
    invest_pa_com: float = None
    invest_outside: float = None
    invest_pa_outside: float = None
    invest_per_x: float = None
    pct_of_wage: float = None
    pct_x: float = None
    ratio_wage_to_emplo: float = None
    cost_wage: float = None
    cost_mro_per_MWh: float = None
    demand_emplo: float = None
    emplo_existing: float = None
    demand_emplo_new: float = None
    full_load_hour: float = None
    lifecycle: float = None


# Definition der Zeilennamen für den Sektor E
@dataclass
class E30:
    # Klassenvariablen für E
    e: EColVars2030 = EColVars2030()
    g: EColVars2030 = EColVars2030()
    d: EColVars2030 = EColVars2030()
    d_r: EColVars2030 = EColVars2030()
    d_b: EColVars2030 = EColVars2030()
    d_i: EColVars2030 = EColVars2030()
    d_t: EColVars2030 = EColVars2030()
    d_a: EColVars2030 = EColVars2030()
    d_f_hydrogen: EColVars2030 = EColVars2030()
    d_e_hydrogen: EColVars2030 = EColVars2030()
    d_e_hydrogen_local: EColVars2030 = EColVars2030()
    p: EColVars2030 = EColVars2030()
    p_g: EColVars2030 = EColVars2030()
    p_fossil: EColVars2030 = EColVars2030()
    p_fossil_nuclear: EColVars2030 = EColVars2030()
    p_fossil_coal_brown: EColVars2030 = EColVars2030()
    p_fossil_coal_brown_cogen: EColVars2030 = EColVars2030()
    p_fossil_coal_black: EColVars2030 = EColVars2030()
    p_fossil_coal_black_cogen: EColVars2030 = EColVars2030()
    p_fossil_gas: EColVars2030 = EColVars2030()
    p_fossil_gas_cogen: EColVars2030 = EColVars2030()
    p_fossil_ofossil: EColVars2030 = EColVars2030()
    p_fossil_ofossil_cogen: EColVars2030 = EColVars2030()
    p_renew: EColVars2030 = EColVars2030()
    p_renew_pv: EColVars2030 = EColVars2030()
    p_renew_pv_roof: EColVars2030 = EColVars2030()
    p_renew_pv_facade: EColVars2030 = EColVars2030()
    p_renew_pv_park: EColVars2030 = EColVars2030()
    p_renew_pv_agri: EColVars2030 = EColVars2030()
    p_wind: EColVars2030 = EColVars2030()
    p_renew_wind_onshore: EColVars2030 = EColVars2030()
    p_renew_wind_offshore: EColVars2030 = EColVars2030()
    p_renew_biomass: EColVars2030 = EColVars2030()
    p_renew_biomass_waste: EColVars2030 = EColVars2030()
    p_renew_biomass_solid: EColVars2030 = EColVars2030()
    p_renew_biomass_gaseous: EColVars2030 = EColVars2030()
    p_renew_biomass_cogen: EColVars2030 = EColVars2030()
    p_renew_geoth: EColVars2030 = EColVars2030()
    p_renew_hydro: EColVars2030 = EColVars2030()
    p_renew_geoth_local: EColVars2030 = EColVars2030()
    p_renew_hydro_local: EColVars2030 = EColVars2030()
    p_reverse: EColVars2030 = EColVars2030()

    p_local: EColVars2030 = EColVars2030()
    p_local_pv: EColVars2030 = EColVars2030()
    p_local_pv_roof: EColVars2030 = EColVars2030()
    p_local_pv_facade: EColVars2030 = EColVars2030()
    p_local_pv_park: EColVars2030 = EColVars2030()
    p_local_pv_agri: EColVars2030 = EColVars2030()
    p_local_wind_onshore: EColVars2030 = EColVars2030()
    p_local_biomass: EColVars2030 = EColVars2030()
    p_local_biomass_solid: EColVars2030 = EColVars2030()
    p_local_biomass_gaseous: EColVars2030 = EColVars2030()
    p_local_biomass_cogen: EColVars2030 = EColVars2030()
    p_local_hydro: EColVars2030 = EColVars2030()
    p_local_surplus: EColVars2030 = EColVars2030()

    # erzeuge dictionry
    def dict(self):
        return asdict(self)


# Berechnungsfunktion im Sektor E für 2018
# Parameter root: oberste Generator Instanz
def Electricity2030_calc(root):
    try:

        Million = 1000000
        Kalkulationszeitraum = entry("In_M_duration_target")
        f18 = root.f18
        e18 = root.e18
        r18 = root.r18
        i18 = root.i18
        #        f30 = root.f30
        e30 = root.e30
        b18 = root.b18
        b30 = root.b30
        i30 = root.i30
        t30 = root.t30
        # a30 = root.a30

        e = root.e30.e
        d = root.e30.d
        d_r = root.e30.d_r
        d_b = root.e30.d_b
        d_i = root.e30.d_i
        d_t = root.e30.d_t
        d_a = root.e30.d_a
        d_f_hydrogen = root.e30.d_f_hydrogen
        d_e_hydrogen = root.e30.d_e_hydrogen

        p = e30.p
        p_g = e30.p_g
        p_fossil = e30.p_fossil
        p_fossil_nuclear = e30.p_fossil_nuclear
        p_fossil_coal_brown = e30.p_fossil_coal_brown
        p_fossil_coal_black = e30.p_fossil_coal_black
        p_fossil_gas = e30.p_fossil_gas
        p_fossil_gas_cogen = e30.p_fossil_gas_cogen
        p_fossil_ofossil = e30.p_fossil_ofossil
        p_renew = e30.p_renew
        p_wind = e30.p_wind
        p_renew_wind_onshore = e30.p_renew_wind_onshore
        p_renew_geoth = e30.p_renew_geoth
        p_renew_hydro = e30.p_renew_hydro
        p_renew_pv = e30.p_renew_pv
        p_renew_pv_roof = e30.p_renew_pv_roof
        p_renew_pv_facade = e30.p_renew_pv_facade
        p_renew_pv_park = e30.p_renew_pv_park
        p_renew_pv_agri = e30.p_renew_pv_agri
        p_renew_wind_onshore = e30.p_renew_wind_onshore
        p_renew_wind_offshore = e30.p_renew_wind_offshore
        p_renew_biomass = e30.p_renew_biomass
        p_reverse = e30.p_reverse

        p_local = e30.p_local
        p_local_pv = e30.p_local_pv
        p_local_pv_roof = e30.p_local_pv_roof
        p_local_pv_facade = e30.p_local_pv_facade
        p_local_pv_park = e30.p_local_pv_park
        p_local_pv_agri = e30.p_local_pv_agri
        p_local_wind_onshore = e30.p_local_wind_onshore
        p_local_biomass = e30.p_local_biomass
        p_local_biomass_cogen = e30.p_local_biomass_cogen
        p_local_biomass_gaseous = e30.p_local_biomass_gaseous
        p_local_hydro = e30.p_local_hydro
        p_local_surplus = e30.p_local_surplus
        d_f_hydrogen = root.e30.d_f_hydrogen
        d_e_hydrogen = root.e30.d_e_hydrogen

        # Begin
        d_r.demand_electricity = r18.s_elec.demand_electricity
        d_b.demand_electricity = b30.s_elec.demand_electricity
        d_i.demand_electricity = 149383800  # todo i18.s_renew_elec.demand_electricity
        d_t.demand_electricity = t30.s_elec.demand_electricity
        d_a.demand_electricity = 5250000  # todo a30.s_elec.demand_electricity
        d_r.energy = d_r.demand_electricity
        d_b.energy = d_b.demand_electricity
        d_i.energy = d_i.demand_electricity
        d_t.energy = d_t.demand_electricity
        d_a.energy = d_a.demand_electricity  # Todo
        # todo #f30.p_petrol.demand_electricity + #f30.p_jetfuel.demand_electricty + #f30.p_diesel.demand_electricty + #f30.p_emethan.demand_electricty + #f30.p_hydrogen.demand_electricty )
        d_f_hydrogen.energy = 870533558.11
        d_e_hydrogen.energy = (
            152111037.44  # todo f30.p_hydrogen_reconv.demand_electricity
        )
        d.energy = (
            d_r.energy
            + d_b.energy
            + d_i.energy
            + d_t.energy
            + d_a.energy
            + d_f_hydrogen.energy
            + d_e_hydrogen.energy
        )  # SUM(d_r.energy:d_e_hydrogen.energy) #power_installed
        p_renew_geoth.power_installed = fact(
            "Fact_E_P_geothermal_installed_capacity_2018"
        )
        p_renew_wind_offshore.power_installed = fact(
            "Fact_E_P_wind_offshore_installed_capacity_2018"
        )
        p_renew_geoth.full_load_hour = fact("Fakt_S_Volllaststunden_Geothermie")
        p_reverse.power_installed = (
            fact("Fact_E_P_gas_installed_capacity_2018") * 1
            if (ags == "DG000000")
            else 0
        )
        p_local_pv_roof.power_installed = entry("In_E_PV_power_inst_roof")
        p_local_pv_facade.power_installed = entry("In_E_PV_power_inst_facade")
        p_local_pv_park.power_installed = entry("In_E_PV_power_inst_park")
        p_local_pv_agri.power_installed = entry("In_E_PV_power_inst_agripv")
        p_local_wind_onshore.power_installed = entry("In_E_PV_power_inst_wind_on")
        p_local_biomass.power_installed = entry("In_E_PV_power_inst_biomass")
        p_local_hydro.power_installed = entry("In_E_PV_power_inst_water")
        p_local_pv.power_installed = (
            p_local_pv_roof.power_installed
            + p_local_pv_facade.power_installed
            + p_local_pv_park.power_installed
            + p_local_pv_agri.power_installed
        )  # SUM(p_local_pv_roof.power_installed:p_local_pv_agri.power_installed) # pct_energy
        p_renew_pv.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_S_pv_ratio_2035")
        )
        p_renew_pv_roof.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_S_pv_roof_ratio_2035")
        )
        p_renew_pv_facade.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_S_pv_facade_ratio_2035")
        )
        p_renew_pv_park.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_S_pv_park_ratio_2035")
        )
        p_renew_pv_agri.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_S_pv_agri_ratio_2035")
        )
        p_renew_wind_onshore.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_P_renew_wind_onshore_ratio_2035")
        )
        p_renew_wind_offshore.power_to_be_installed_pct = ass(
            "Ass_E_P_wind_offshore_power_to_be_installed_2035"
        )
        p_renew_biomass.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_P_renew_biomass_ratio_2035")
        )
        p_renew_geoth.pct_energy = ass("Ass_E_P_renew_hydro_ratio_2035")
        p_renew_hydro.pct_energy = (
            0 if (ags == "DG000000") else ass("Ass_E_P_renew_hydro_ratio_2035")
        )  # energy
        p_renew_wind_offshore.power_installable = ass(
            "ASS_E_P_wind_offshore_power_installable"
        )
        p_renew_wind_offshore.power_to_be_installed = max(
            0,
            p_renew_wind_offshore.power_installable
            * p_renew_wind_offshore.power_to_be_installed_pct
            - p_renew_wind_offshore.power_installed,
        )
        p_renew_geoth.power_to_be_installed_pct = ass(
            "ASS_E_P_geoth_power_to_be_installed_2030"
        )
        p_local_pv_roof.power_to_be_installed_pct = entry(
            "In_E_PV_power_to_be_inst_roof"
        )
        p_local_pv_facade.power_to_be_installed_pct = entry(
            "In_E_PV_power_to_be_inst_facade"
        )
        p_local_pv_park.power_to_be_installed_pct = entry(
            "In_E_PV_power_to_be_inst_park"
        )
        p_local_pv_agri.area_ha_available = entry("In_M_area_agri_com")
        p_local_wind_onshore.power_to_be_installed_pct = entry(
            "In_E_PV_power_to_be_inst_local_wind_onshore"
        )
        p_renew_wind_offshore.full_load_hour = fact(
            "Fact_E_P_wind_offshore_full_load_hours"
        )
        p_renew_geoth.power_installable = ass("ASS_E_P_renew_geoth_power_installable")
        p_local_pv_facade.area_ha_available = (
            ass("Ass_E_P_pv_facade_potential")
            * entry("In_R_buildings_com")
            / entry("In_R_buildings_nat")
        )
        p_local_pv_park.area_ha_available = entry("In_M_area_total_com")
        p_local_pv_agri.area_ha_available_pct_of_action = ass(
            "Ass_E_P_pv_agri_area_ha_avail_pct_action"
        ) / (ass("Ass_E_P_pv_agri_power_per_ha") * entry("In_M_area_agri_nat"))
        p_local_wind_onshore.area_ha_available = entry("In_M_area_agri_com") + entry(
            "In_M_area_wood_com"
        )
        p_local_pv_roof.area_ha_available_pct_of_action = ass(
            "Ass_S_Potential_Dachfläche"
        )
        p_local_pv_park.area_ha_available_pct_of_action = fact(
            "Fact_S_B_PV_Freifläche_nutzbarer_Anteil"
        )
        p_local_pv_agri.ratio_power_to_area_ha = ass("Ass_E_P_pv_agri_power_per_ha")
        p_local_wind_onshore.area_ha_available_pct_of_action = ass(
            "Ass_E_P_local_wind_onshore_pct_action"
        )
        p_local_pv_roof.ratio_power_to_area_ha = ass(
            "Ass_E_P_pv_roof_ratio_power_to_area_ha"
        )
        p_local_pv_facade.ratio_power_to_area_ha = ass(
            "Ass_E_P_pv_facade_ratio_power_to_area_ha"
        )
        p_local_pv_park.ratio_power_to_area_ha = ass("Ass_E_P_pv_park_power_per_ha")
        p_local_pv_agri.power_installable = (
            p_local_pv_agri.ratio_power_to_area_ha
            * p_local_pv_agri.area_ha_available_pct_of_action
            * p_local_pv_agri.area_ha_available
        )
        p_local_wind_onshore.ratio_power_to_area_ha = entry(
            "In_E_local_wind_onshore_ratio_power_to_area"
        )
        p_local_pv_facade.area_ha_available_pct_of_action = ass(
            "Ass_E_P_pv_facade_useful_potential"
        )
        p_local_pv_roof.power_installable = (
            p_local_pv_roof.area_ha_available
            * p_local_pv_roof.area_ha_available_pct_of_action
            * p_local_pv_roof.ratio_power_to_area_ha
        )
        p_local_pv_facade.power_installable = (
            p_local_pv_facade.ratio_power_to_area_ha
            * p_local_pv_facade.area_ha_available
            * p_local_pv_facade.area_ha_available_pct_of_action
        )
        p_local_pv_park.power_installable = (
            p_local_pv_park.ratio_power_to_area_ha
            * p_local_pv_park.area_ha_available_pct_of_action
            * p_local_pv_park.area_ha_available
        )
        p_local_pv_roof.full_load_hour = entry("In_E_full_load_h_PV")
        p_local_wind_onshore.power_installable = (
            p_local_wind_onshore.ratio_power_to_area_ha
            * p_local_wind_onshore.area_ha_available
            * p_local_wind_onshore.area_ha_available_pct_of_action
        )
        p_local_biomass.power_installable = entry("In_E_biomass_local_power_inst")
        p_local_wind_onshore.power_to_be_installed = max(
            0,
            p_local_wind_onshore.power_installable
            * p_local_wind_onshore.power_to_be_installed_pct
            - p_local_wind_onshore.power_installed,
        )
        p_reverse.power_to_be_installed = max(
            0,
            ass("Ass_E_P_reverse_ratio_2035")
            * ass("Ass_E_P_total_2035")
            / ass("Ass_E_P_h2_reverse_power")
            - p_reverse.power_installed,
        )
        p_local_pv_roof.power_to_be_installed = max(
            0,
            p_local_pv_roof.power_installable
            * p_local_pv_roof.power_to_be_installed_pct
            - p_local_pv_roof.power_installed,
        )
        p_local_pv_facade.power_to_be_installed = max(
            0,
            p_local_pv_facade.power_installable
            * p_local_pv_facade.power_to_be_installed_pct
            - p_local_pv_facade.power_installed,
        )
        p_local_pv_park.power_to_be_installed = max(
            0,
            p_local_pv_park.power_installable
            * p_local_pv_park.power_to_be_installed_pct
            - p_local_pv_park.power_installed,
        )
        p_local_pv_agri.full_load_hour = p_local_pv_roof.full_load_hour
        p_local_wind_onshore.full_load_hour = fact(
            "Fact_E_P_wind_onshore_full_load_hours"
        )
        p_local_biomass.power_to_be_installed_pct = entry(
            "In_E_PV_power_to_be_inst_local_biomass"
        )
        p_local_biomass.power_to_be_installed = max(
            0,
            p_local_biomass.power_installable
            * p_local_biomass.power_to_be_installed_pct
            - p_local_biomass.power_installed,
        )
        p_local_pv_agri.energy_installable = (
            p_local_pv_agri.full_load_hour * p_local_pv_agri.power_installable
        )
        p_local_wind_onshore.energy = (
            p_local_wind_onshore.power_to_be_installed
            + p_local_wind_onshore.power_installed
        ) * p_local_wind_onshore.full_load_hour
        p_renew_geoth.power_to_be_installed = max(
            0,
            p_renew_geoth.power_installable * p_renew_geoth.power_to_be_installed_pct
            - p_renew_geoth.power_installed,
        )
        p_reverse.full_load_hour = ass("Ass_E_P_h2_reverse_power")
        p_local_biomass.full_load_hour = fact("Fact_E_P_bio_full_load_hours")
        p_local_pv_facade.full_load_hour = ass("Ass_E_P_pv_facade_full_load_hours")
        p_local_pv_park.full_load_hour = p_local_pv_roof.full_load_hour
        p_local_biomass.energy = (
            p_local_biomass.power_to_be_installed + p_local_biomass.power_installed
        ) * p_local_biomass.full_load_hour
        p_local_pv_roof.energy = (
            p_local_pv_roof.power_to_be_installed + p_local_pv_roof.power_installed
        ) * p_local_pv_roof.full_load_hour
        p_local_pv_facade.energy = (
            p_local_pv_facade.power_to_be_installed + p_local_pv_facade.power_installed
        ) * p_local_pv_facade.full_load_hour
        p_local_hydro.full_load_hour = fact("Fact_E_P_hydro_full_load_hours")  # energy
        p_local_pv_park.energy = (
            p_local_pv_park.power_to_be_installed + p_local_pv_park.power_installed
        ) * p_local_pv_park.full_load_hour
        p_local_hydro.energy = (
            p_local_hydro.power_installed * p_local_hydro.full_load_hour
        )
        p_local_biomass_cogen.pct_energy = fact("Fact_E_P_renew_cogen_ratio_2018")
        p_renew_geoth.energy = (
            (p_renew_geoth.power_to_be_installed + p_renew_geoth.power_installed)
            * p_renew_geoth.full_load_hour
            if (ags == "DG000000")
            else p_renew.energy_ * p_renew_geoth.pct_energy_
        )
        p_reverse.energy = (
            (d.energy - d_e_hydrogen.energy) * ass("Ass_E_P_reverse_ratio_2035")
            if (ags == "DG000000")
            else p_renew.energy_ * ass("Ass_E_P_reverse_ratio_2035")
        )
        p_renew_wind_offshore.energy = (
            (
                p_renew_wind_offshore.power_to_be_installed
                + p_renew_wind_offshore.power_installed
            )
            * p_renew_wind_offshore.full_load_hour
            if (ags == "DG000000")
            else p_renew.energy_ * p_renew_wind_offshore.pct_energy_
        )
        p_local_biomass_cogen.energy = (
            p_local_biomass.energy * p_local_biomass_cogen.pct_energy
        )
        p_g.energy = (
            p_renew_wind_offshore.energy + p_renew_geoth.energy + p_reverse.energy
            if (ags == "DG000000")
            else max(0, -p_local_surplus.energy_)
        )
        p_renew.energy = p_g.energy
        p_local_pv_agri.energy = d.energy - (
            p_local_pv_roof.energy
            + p_local_pv_facade.energy
            + p_local_pv_park.energy
            + p_local_wind_onshore.energy
            + p_local_biomass.energy
            + p_local_hydro.energy
            + p_renew.energy
        )
        p_local_pv.energy = (
            p_local_pv_roof.energy
            + p_local_pv_facade.energy
            + p_local_pv_park.energy
            + p_local_pv_agri.energy
        )  # SUM(p_local_pv_roof.energy:p_local_pv_agri.energy)
        # SUM(p_local_pv.energy,p_local_wind_onshore.energy,p_local_biomass.energy,p_local_hydro.energy)
        p_local.energy = (
            p_local_pv.energy
            + p_local_wind_onshore.energy
            + p_local_biomass.energy
            + p_local_hydro.energy
        )
        p_local_surplus.energy = p_local.energy - d.energy
        p_local_pv_agri.power_to_be_installed_pct = (
            p_local_pv_agri.energy / p_local_pv_agri.energy_installable
            if (ags == "DG000000")
            else entry("In_E_PV_power_to_be_inst_agri")
        )
        p_renew_geoth.pct_energy = (
            p_renew_geoth.energy / p_renew.energy
            if (ags == "DG000000")
            else ass("Ass_E_P_renew_geoth_ratio_2035")
        )
        p_renew_pv.energy = (
            0 if (ags == "DG000000") else p_renew.energy * p_renew_pv.pct_energy
        )
        p.energy = p_g.energy + p_local.energy
        p_renew_pv_park.energy = p_renew_pv.energy * p_renew_pv_park.pct_energy
        p_renew_pv_agri.energy = p_renew_pv.energy * p_renew_pv_agri.pct_energy
        p_renew_wind_onshore.energy = (
            0
            if (ags == "DG000000")
            else p_renew.energy * p_renew_wind_onshore.pct_energy
        )
        p_wind.energy = p_renew_wind_onshore.energy + p_renew_wind_offshore.energy
        p_renew_biomass.energy = (
            0 if (ags == "DG000000") else p_renew.energy * p_renew_biomass.pct_energy
        )
        p_renew_pv_facade.energy = p_renew_pv.energy * p_renew_pv_facade.pct_energy
        p_renew_hydro.energy = (
            0 if (ags == "DG000000") else p_renew.energy * p_renew_hydro.pct_energy
        )
        p_renew_pv_roof.energy = p_renew_pv.energy * p_renew_pv_roof.pct_energy
        p_local_pv.power_installable = (
            p_local_pv_roof.power_installable
            + p_local_pv_facade.power_installable
            + p_local_pv_park.power_installable
            + p_local_pv_agri.power_installable
        )
        p_renew_geoth.pct_x = p_renew_geoth.energy / p.energy
        p_renew_wind_offshore.pct_energy = (
            p_renew_wind_offshore.energy / p_renew.energy
            if (ags == "DG000000")
            else ass("Ass_E_P_renew_wind_offshore_ratio_2035")
        )
        p_reverse.pct_energy = 0 if (ags == "DG000000") else p_reverse.energy / p.energy
        p_reverse.pct_x = p_reverse.energy / p.energy
        p_local_pv.pct_energy = p_local_pv.energy / p_local.energy
        p_local_pv_roof.pct_energy = p_local_pv_roof.energy / p_local_pv.energy
        p_local_pv_facade.pct_energy = p_local_pv_facade.energy / p_local_pv.energy
        p_local_pv_park.pct_energy = p_local_pv_park.energy / p_local_pv.energy
        p_local_pv_agri.pct_energy = p_local_pv_agri.energy / p_local_pv.energy
        p_local_wind_onshore.pct_energy = p_local_wind_onshore.energy / p_local.energy
        p_local_biomass.pct_energy = p_local_biomass.energy / p_local.energy
        p_local_hydro.pct_energy = p_local_hydro.energy / p_local.energy
        p_local.pct_energy = (
            p_local_pv.pct_energy
            + p_local_wind_onshore.pct_energy
            + p_local_biomass.pct_energy
            + p_local_hydro.pct_energy
        )
        d_r.pct_energy = d_r.energy / d.energy
        d_b.pct_energy = d_b.energy / d.energy
        d_i.pct_energy = d_i.energy / d.energy
        d_t.pct_energy = d_t.energy / d.energy
        d_a.pct_energy = d_a.energy / d.energy
        d_f_hydrogen.pct_energy = d_f_hydrogen.energy / d.energy
        d_e_hydrogen.pct_energy = d_e_hydrogen.energy / d.energy
        d.pct_energy = (
            d_r.pct_energy
            + d_b.pct_energy
            + d_i.pct_energy
            + d_t.pct_energy
            + d_a.pct_energy
            + d_f_hydrogen.pct_energy
            + d_e_hydrogen.pct_energy
        )
        p_wind.pct_energy = (
            p_renew_wind_onshore.pct_energy + p_renew_wind_offshore.pct_energy
        )  # power_to_be_installed_pct
        p_local_pv_roof.pct_x = p_local_pv_roof.energy / (
            d_r.energy + d_b.energy + d_i.energy + d_t.energy + d_a.energy
        )  # e30.p_local_pv_roof.energy / SUM(e30.d_r.energy:e30.d_a.energy)
        d_r.cost_fuel_per_MWh = fact("Fact_E_S_electricity_costs_household_2018")
        d_b.cost_fuel_per_MWh = fact("Fact_E_S_electricity_costs_GHD_2018")
        d_i.cost_fuel_per_MWh = fact("Fact_E_S_electricity_costs_industrie_2018")
        d_t.cost_fuel_per_MWh = fact("Fact_E_S_electricity_costs_household_2018")
        d_a.cost_fuel_per_MWh = fact("Fact_E_S_electricity_costs_household_2018")
        p_fossil_nuclear.cost_fuel_per_MWh = e18.p_fossil_nuclear.cost_fuel_per_MWh
        p_fossil_coal_brown.cost_fuel_per_MWh = (
            e18.p_fossil_coal_brown.cost_fuel_per_MWh
        )
        p_fossil_coal_black.cost_fuel_per_MWh = (
            e18.p_fossil_coal_black.cost_fuel_per_MWh
        )
        p_fossil_gas.cost_fuel_per_MWh = e18.p_fossil_gas.cost_fuel_per_MWh
        p_fossil_ofossil.cost_fuel_per_MWh = e18.p_fossil_ofossil.cost_fuel_per_MWh
        p_renew_biomass.cost_fuel_per_MWh = ass("Ass_E_S_biomass_material_costs") / ass(
            "Ass_E_S_biomass_efficiency"
        )
        p_local_biomass.cost_fuel_per_MWh = ass("Ass_E_S_biomass_material_costs") / ass(
            "Ass_E_S_biomass_efficiency"
        )
        d_r.cost_fuel = (
            d_r.energy * d_r.cost_fuel_per_MWh * p_g.energy / p.energy / Million
        )
        d_b.cost_fuel = (
            d_b.energy * d_b.cost_fuel_per_MWh * p_g.energy / p.energy / Million
        )
        d_i.cost_fuel = (
            d_i.energy * d_i.cost_fuel_per_MWh * p_g.energy / p.energy / Million
        )
        d_t.cost_fuel = (
            d_t.energy * d_t.cost_fuel_per_MWh * p_g.energy / p.energy / Million
        )
        d_a.cost_fuel = (
            d_a.energy * d_a.cost_fuel_per_MWh * p_g.energy / p.energy / Million
        )
        p_fossil.energy = 0
        p_fossil_nuclear.energy = 0
        p_fossil_coal_brown.energy = 0
        p_fossil_coal_black.energy = 0
        p_fossil_gas.energy = 0
        p_fossil_gas_cogen.energy = 0
        p_fossil_ofossil.energy = 0  # cost_fuel
        p_fossil_nuclear.cost_fuel = (
            p_fossil_nuclear.cost_fuel_per_MWh * p_fossil_nuclear.energy / 1000000
        )
        p_fossil_coal_brown.cost_fuel = (
            p_fossil_coal_brown.cost_fuel_per_MWh * p_fossil_coal_brown.energy / 1000000
        )
        p_fossil_coal_black.cost_fuel = (
            p_fossil_coal_black.cost_fuel_per_MWh * p_fossil_coal_black.energy
        )
        p_fossil_gas.cost_fuel = (
            p_fossil_gas.cost_fuel_per_MWh * p_fossil_gas.energy / 1000000
        )
        p_fossil_ofossil.cost_fuel = (
            p_fossil_ofossil.cost_fuel_per_MWh * p_fossil_ofossil.energy / 1000000
        )
        p_renew_biomass.cost_fuel = (
            p_renew_biomass.energy * p_renew_biomass.cost_fuel_per_MWh / Million
        )
        p_renew.cost_fuel = p_renew_biomass.cost_fuel
        p_local_biomass.cost_fuel = (
            p_local_biomass.cost_fuel_per_MWh * p_local_biomass.energy / Million
        )
        p_local.cost_fuel = p_local_biomass.cost_fuel
        p_fossil.cost_fuel = (
            p_fossil_nuclear.cost_fuel
            + p_fossil_coal_brown.cost_fuel
            + p_fossil_coal_black.cost_fuel
            + p_fossil_gas.cost_fuel
            + p_fossil_ofossil.cost_fuel
        )
        p_g.cost_fuel = p_fossil.cost_fuel + p_renew.cost_fuel
        p.cost_fuel = p_g.cost_fuel + p_local.cost_fuel  # cost_mro_per_MWh
        p_fossil_nuclear.cost_mro_per_MWh = ass("Ass_E_P_nuclear_mro_per_year") / fact(
            "Fact_E_P_full_load_hours_nuclear_plant_2015"
        )
        p_fossil_coal_brown.cost_mro_per_MWh = e18.p_fossil_coal_brown.cost_mro_per_MWh
        p_fossil_coal_black.cost_mro_per_MWh = e18.p_fossil_coal_black.cost_mro_per_MWh
        p_fossil_gas.cost_mro_per_MWh = ass("Ass_E_P_gas_mro_per_year") / fact(
            "Fact_E_P_gas_full_load_hours"
        )
        p_fossil_ofossil.cost_mro_per_MWh = ass(
            "Ass_E_P_MO_costs_brown_coal_plant"
        ) / fact("Fact_E_P_full_load_hours_brown_coal_plant_2015")
        p_renew_pv_roof.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_roof_investcosts")
            * ass("Ass_E_P_pv_roof_mro_per_year")
            / p_local_pv_roof.full_load_hour
            * 1000
        )
        p_renew_pv_facade.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_facade_investcosts")
            * ass("Ass_E_P_pv_roof_mro_per_year")
            / p_local_pv_facade.full_load_hour
            * 1000
        )
        p_renew_pv_park.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_park_investcosts_2020")
            * ass("Ass_E_P_pv_park_mro_per_year")
            / p_local_pv_park.full_load_hour
            * 1000
        )
        p_renew_pv_agri.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_agri_investcosts")
            * ass("Ass_E_P_pv_roof_mro_per_year")
            / p_local_pv_agri.full_load_hour
            * 1000
        )
        p_renew_wind_onshore.cost_mro_per_MWh = (
            ass("Ass_E_S_wind_onshore_investcosts_2020")
            * ass("Ass_E_P_wind_onshore_mro_per_year")
            / fact("Fact_E_P_wind_onshore_full_load_hours")
            * 1000
        )
        p_renew_wind_offshore.cost_mro_per_MWh = (
            ass("Ass_E_S_wind_offshore_investcosts_2030")
            * ass("Ass_E_P_wind_offshore_mro_per_year")
            / fact("Fact_E_P_wind_offshore_full_load_hours")
            * 1000
        )
        p_renew_biomass.cost_mro_per_MWh = ass("Ass_E_P_biomass_mro_per_MWh")
        p_renew_geoth.cost_mro_per_MWh = ass("Ass_E_P_geoth_mro")
        p_renew_hydro.cost_mro_per_MWh = ass("Ass_E_P_hydro_mro_per_MWh")
        p_reverse.cost_mro_per_MWh = ass("Ass_E_P_gas_mro_per_year") / ass(
            "Ass_E_P_h2_reverse_power"
        )
        p_local_pv_roof.cost_mro_per_MWh = (
            ass("Ass_S_A_Investitionskosten_PV_Dach_2030")
            * ass("Ass_E_P_pv_roof_mro_per_year")
            / p_local_pv_roof.full_load_hour
            * 1000
        )
        p_local_pv_facade.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_facade_investcosts")
            * ass("Ass_E_P_pv_roof_mro_per_year")
            / ass("Ass_E_P_pv_facade_full_load_hours")
            * 1000
        )
        p_local_pv_park.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_park_investcosts_2030")
            * ass("Ass_E_P_pv_park_mro_per_year")
            / p_local_pv_park.full_load_hour
            * 1000
        )
        p_local_pv_agri.cost_mro_per_MWh = (
            ass("Ass_E_S_pv_agri_investcosts")
            * ass("Ass_E_P_pv_agri_mro_per_year")
            / p_local_pv_park.full_load_hour
            * 1000
        )
        p_local_wind_onshore.cost_mro_per_MWh = (
            ass("Ass_E_S_wind_onshore_investcosts_2030")
            * ass("Ass_E_P_wind_onshore_mro_per_year")
            / fact("Fact_E_P_wind_onshore_full_load_hours")
            * 1000
        )
        p_local_biomass.cost_mro_per_MWh = ass("Ass_E_P_biomass_mro_per_MWh")
        p_local_hydro.cost_mro_per_MWh = ass("Ass_E_P_hydro_mro_per_MWh")  # cost_mro
        p_fossil_nuclear.cost_mro = (
            p_fossil_nuclear.cost_mro_per_MWh * p_fossil_nuclear.energy / 1000000
        )
        p_fossil_coal_brown.cost_mro = (
            p_fossil_coal_brown.cost_mro_per_MWh * p_fossil_coal_brown.energy / 1000000
        )
        p_fossil_coal_black.cost_mro = (
            p_fossil_coal_black.cost_mro_per_MWh * p_fossil_coal_black.energy / 1000000
        )
        p_fossil_gas.cost_mro = (
            p_fossil_gas.cost_mro_per_MWh * p_fossil_gas.energy / 1000000
        )
        p_fossil_ofossil.cost_mro = (
            p_fossil_ofossil.cost_mro_per_MWh * p_fossil_ofossil.energy / 1000000
        )
        p_fossil.cost_mro = (
            p_fossil_nuclear.cost_mro
            + p_fossil_coal_brown.cost_mro
            + p_fossil_gas.cost_mro
            + p_fossil_ofossil.cost_mro
        )  # SUM(p_fossil_nuclear.cost_mro:CQ72)
        p_renew_pv_roof.cost_mro = (
            p_renew_pv_roof.energy * p_renew_pv_roof.cost_mro_per_MWh / Million
        )
        p_renew_pv_facade.cost_mro = (
            p_renew_pv_facade.energy * p_renew_pv_facade.cost_mro_per_MWh / Million
        )
        p_renew_pv_park.cost_mro = (
            p_renew_pv_park.energy * p_renew_pv_park.cost_mro_per_MWh / Million
        )
        p_renew_pv_agri.cost_mro = (
            p_renew_pv_agri.energy * p_renew_pv_agri.cost_mro_per_MWh / Million
        )
        p_renew_pv.cost_mro = (
            p_renew_pv_roof.cost_mro
            + p_renew_pv_facade.cost_mro
            + p_renew_pv_park.cost_mro
            + p_renew_pv_agri.cost_mro
        )  # SUM(p_renew_pv_roof.cost_mro:p_renew_pv_agri.cost_mro)
        p_renew_wind_onshore.cost_mro = (
            p_renew_wind_onshore.energy
            * p_renew_wind_onshore.cost_mro_per_MWh
            / Million
        )
        p_renew_wind_offshore.cost_mro = (
            p_renew_wind_offshore.energy
            * p_renew_wind_offshore.cost_mro_per_MWh
            / Million
        )
        p_wind.cost_mro = p_renew_wind_onshore.cost_mro + p_renew_wind_offshore.cost_mro
        p_renew_biomass.cost_mro = (
            p_renew_biomass.energy * p_renew_biomass.cost_mro_per_MWh / Million
        )
        p_renew_geoth.cost_mro = (
            p_renew_geoth.energy * p_renew_geoth.cost_mro_per_MWh / Million
        )
        p_renew_hydro.cost_mro = (
            p_renew_hydro.energy * p_renew_hydro.cost_mro_per_MWh / Million
        )
        p_reverse.cost_mro = p_reverse.energy * p_reverse.cost_mro_per_MWh / Million
        p_reverse.cost_mro = p_reverse.energy * p_reverse.cost_mro_per_MWh / Million
        p_local_pv_roof.cost_mro = (
            p_local_pv_roof.energy * p_local_pv_roof.cost_mro_per_MWh / Million
        )
        p_local_pv_facade.cost_mro = (
            p_local_pv_facade.energy * p_local_pv_facade.cost_mro_per_MWh / Million
        )
        p_local_pv_park.cost_mro = (
            p_local_pv_park.energy * p_local_pv_park.cost_mro_per_MWh / Million
        )
        p_local_pv_agri.cost_mro = (
            p_local_pv_agri.energy * p_local_pv_agri.cost_mro_per_MWh / Million
        )
        p_local_wind_onshore.cost_mro = (
            p_local_wind_onshore.energy
            * p_local_wind_onshore.cost_mro_per_MWh
            / Million
        )
        p_local_biomass.cost_mro = (
            p_local_biomass.energy * p_local_biomass.cost_mro_per_MWh / Million
        )
        p_local_hydro.cost_mro = (
            p_local_hydro.energy * p_local_hydro.cost_mro_per_MWh / Million
        )
        p_renew.cost_mro = (
            p_renew_pv.cost_mro
            + p_wind.cost_mro
            + p_renew_biomass.cost_mro
            + p_renew_geoth.cost_mro
            + p_renew_hydro.cost_mro
            + p_reverse.cost_mro
        )
        p_local_pv.cost_mro = (
            p_local_pv_roof.cost_mro
            + p_local_pv_facade.cost_mro
            + p_local_pv_park.cost_mro
            + p_local_pv_agri.cost_mro
        )  # SUM(p_local_pv_roof.cost_mro:p_local_pv_agri.cost_mro)
        # SUM(p_local_pv.cost_mro,p_local_wind_onshore.cost_mro,p_local_biomass.cost_mro,p_local_hydro.cost_mro)
        p_local.cost_mro = (
            p_local_pv.cost_mro
            + p_local_wind_onshore.cost_mro
            + p_local_biomass.cost_mro
            + p_local_hydro.cost_mro
        )
        p_g.cost_mro = p_fossil.cost_mro + p_renew.cost_mro
        p.cost_mro = p_g.cost_mro + p_local.cost_mro
        p_fossil_nuclear.CO2e_cb_per_MWh = e18.p_fossil_nuclear.CO2e_cb_per_MWh
        p_fossil_coal_brown.CO2e_cb_per_MWh = e18.p_fossil_coal_brown.CO2e_cb_per_MWh
        p_fossil_coal_black.CO2e_cb_per_MWh = e18.p_fossil_coal_black.CO2e_cb_per_MWh
        p_fossil_gas.CO2e_cb_per_MWh = e18.p_fossil_gas.CO2e_cb_per_MWh
        p_fossil_gas_cogen.CO2e_cb_per_MWh = 0
        p_fossil_ofossil.CO2e_cb_per_MWh = e18.p_fossil_ofossil.CO2e_cb_per_MWh
        p_renew_biomass.CO2e_cb_per_MWh = e18.p_renew_biomass.CO2e_cb_per_MWh
        p_local_pv.CO2e_cb_per_MWh = 0
        p_local_wind_onshore.CO2e_cb_per_MWh = 0
        p_local_biomass.CO2e_cb_per_MWh = e18.p_local_biomass.CO2e_cb_per_MWh
        p_local_hydro.CO2e_cb_per_MWh = 0
        p_fossil_nuclear.CO2e_cb = (
            p_fossil_nuclear.energy * p_fossil_nuclear.CO2e_cb_per_MWh
        )
        p_fossil_coal_brown.CO2e_cb = (
            p_fossil_coal_brown.energy * p_fossil_coal_brown.CO2e_cb_per_MWh
        )
        p_fossil_coal_black.CO2e_cb = (
            p_fossil_coal_black.energy * p_fossil_coal_black.CO2e_cb_per_MWh
        )
        p_fossil_gas.CO2e_cb = p_fossil_gas.energy * p_fossil_gas.CO2e_cb_per_MWh
        p_fossil_gas_cogen.CO2e_cb = (
            p_fossil_gas_cogen.energy * p_fossil_gas_cogen.CO2e_cb_per_MWh
        )
        p_fossil_ofossil.CO2e_cb = (
            p_fossil_ofossil.energy * p_fossil_ofossil.CO2e_cb_per_MWh
        )
        p_fossil.CO2e_cb = (
            p_fossil_nuclear.CO2e_cb
            + p_fossil_coal_brown.CO2e_cb
            + p_fossil_coal_black.CO2e_cb
            + p_fossil_gas.CO2e_cb
            + p_fossil_ofossil.CO2e_cb
        )
        p_renew_biomass.CO2e_cb = (
            p_renew_biomass.energy * p_renew_biomass.CO2e_cb_per_MWh
        )
        p_renew.CO2e_cb = p_renew_biomass.CO2e_cb
        p_local_pv.CO2e_cb = p_local_pv.energy * p_local_pv.CO2e_cb_per_MWh
        p_local_wind_onshore.CO2e_cb = (
            p_local_wind_onshore.energy * p_local_wind_onshore.CO2e_cb_per_MWh
        )
        p_local_biomass.CO2e_cb = (
            p_local_biomass.energy * p_local_biomass.CO2e_cb_per_MWh
        )
        p_local_hydro.CO2e_cb = p_local_hydro.energy * p_local_hydro.CO2e_cb_per_MWh
        # SUM(p_local_pv.CO2e_cb,p_local_wind_onshore.CO2e_cb,p_local_biomass.CO2e_cb,p_local_hydro.CO2e_cb)
        p_local.CO2e_cb = (
            p_local_pv.CO2e_cb
            + p_local_wind_onshore.CO2e_cb
            + p_local_biomass.CO2e_cb
            + p_local_hydro.CO2e_cb
        )
        p_g.CO2e_cb = p_fossil.CO2e_cb + p_renew.CO2e_cb
        p.CO2e_cb = p_g.CO2e_cb + p_local.CO2e_cb
        p.CO2e_total = p.CO2e_cb
        e.CO2e_total = p.CO2e_total
        p_g.CO2e_total = p_g.CO2e_cb
        p_local.CO2e_total = p_local.CO2e_cb  # change_energy_MWh
        d.change_energy_MWh = d.energy - e18.d.energy
        d_r.change_energy_MWh = d_r.energy - e18.d_r.energy
        d_b.change_energy_MWh = d_b.energy - e18.d_b.energy
        d_i.change_energy_MWh = d_i.energy - e18.d_i.energy
        d_t.change_energy_MWh = d_t.energy - e18.d_t.energy
        d_a.change_energy_MWh = d_a.energy - e18.d_a.energy
        d_f_hydrogen.change_energy_MWh = d_f_hydrogen.energy - e18.d_f_hydrogen.energy
        d_e_hydrogen.change_energy_MWh = d_e_hydrogen.energy - e18.d_e_hydrogen.energy
        p.change_energy_MWh = p.energy - e18.p.energy
        p_fossil.change_energy_MWh = p_fossil.energy - e18.p_fossil.energy
        p_fossil_nuclear.change_energy_MWh = (
            p_fossil_nuclear.energy - e18.p_fossil_nuclear.energy
        )
        p_fossil_coal_brown.change_energy_MWh = (
            p_fossil_coal_brown.energy - e18.p_fossil_coal_brown.energy
        )
        p_fossil_coal_black.change_energy_MWh = (
            p_fossil_coal_black.energy - e18.p_fossil_coal_black.energy
        )
        p_fossil_gas.change_energy_MWh = p_fossil_gas.energy - e18.p_fossil_gas.energy
        p_fossil_ofossil.change_energy_MWh = (
            p_fossil_ofossil.energy - e18.p_fossil_ofossil.energy
        )
        p_renew.change_energy_MWh = p_renew.energy - e18.p_renew.energy
        p_renew_biomass.change_energy_MWh = (
            0
            if (ags == "DG000000")
            else e30.p_renew_biomass.energy - e18.p_renew_biomass.energy
        )
        p_renew_geoth.change_energy_MWh = (
            p_renew_geoth.energy - e18.p_renew_geoth.energy
        )
        p_renew_hydro.change_energy_MWh = (
            p_renew_hydro.energy - e18.p_renew_hydro.energy
        )
        p_reverse.change_energy_MWh = e30.p_reverse.energy
        p_local.change_energy_MWh = p_local.energy - e18.p_local.energy
        p_local_pv.change_energy_MWh = p_local_pv.energy - e18.p_local_pv.energy
        p_local_pv_roof.change_energy_MWh = (
            p_local_pv_roof.energy - e18.p_local_pv_roof.energy
        )
        p_local_pv_facade.change_energy_MWh = (
            p_local_pv_facade.energy - e18.p_local_pv_facade.energy
        )
        p_local_pv_park.change_energy_MWh = (
            p_local_pv_park.energy - e18.p_local_pv_park.energy
        )
        p_local_pv_agri.change_energy_MWh = (
            p_local_pv_agri.energy - e18.p_local_pv_agri.energy
        )
        p_local_wind_onshore.change_energy_MWh = (
            p_local_wind_onshore.energy - e18.p_local_wind_onshore.energy
        )
        p_local_biomass.change_energy_MWh = (
            p_local_biomass.energy - e18.p_local_biomass.energy
        )
        p_local_hydro.change_energy_MWh = (
            p_local_hydro.energy - e18.p_local_hydro.energy
        )
        p_g.change_energy_MWh = p_g.energy - e18.p_g.energy  # change_energy_pct
        d.change_energy_pct = d.change_energy_MWh / e18.d.energy
        d_r.change_energy_pct = d_r.change_energy_MWh / e18.d_r.energy
        d_b.change_energy_pct = d_b.change_energy_MWh / e18.d_b.energy
        d_i.change_energy_pct = d_i.change_energy_MWh / e18.d_i.energy
        d_t.change_energy_pct = d_t.change_energy_MWh / e18.d_t.energy
        d_a.change_energy_pct = d_a.change_energy_MWh / e18.d_a.energy
        p.change_energy_pct = p.change_energy_MWh / e18.p.energy
        p_g.change_energy_pct = p_g.change_energy_MWh / e18.p_g.energy
        p_fossil.change_energy_pct = p_fossil.change_energy_MWh / e18.p_fossil.energy
        p_fossil_nuclear.change_energy_pct = (
            p_fossil_nuclear.change_energy_MWh / e18.p_fossil_nuclear.energy
        )
        p_fossil_coal_brown.change_energy_pct = (
            p_fossil_coal_brown.change_energy_MWh / e18.p_fossil_coal_brown.energy
        )
        p_fossil_coal_black.change_energy_pct = (
            p_fossil_coal_black.change_energy_MWh / e18.p_fossil_coal_black.energy
        )
        p_fossil_gas.change_energy_pct = (
            p_fossil_gas.change_energy_MWh / e18.p_fossil_gas.energy
        )
        p_fossil_ofossil.change_energy_pct = (
            p_fossil_ofossil.change_energy_MWh / e18.p_fossil_ofossil.energy
        )
        p_renew.change_energy_pct = p_renew.change_energy_MWh / e18.p_renew.energy
        p_renew_biomass.change_energy_pct = (
            p_renew_biomass.change_energy_MWh / e18.p_renew_biomass.energy
        )
        p_renew_geoth.change_energy_pct = (
            p_renew_geoth.change_energy_MWh / e18.p_renew_geoth.energy
        )
        p_renew_hydro.change_energy_pct = (
            p_renew_hydro.change_energy_MWh / e18.p_renew_hydro.energy
        )
        p_local.change_energy_pct = (
            p_local.change_energy_MWh / e18.p_local.energy
        )  # change_CO2e_t
        p_fossil_nuclear.change_CO2e_t = (
            e18.p_fossil_nuclear.CO2e_cb_per_MWh
            * p_fossil_nuclear.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_fossil_coal_brown.change_CO2e_t = (
            e18.p_fossil_coal_brown.CO2e_cb_per_MWh
            * p_fossil_coal_brown.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_fossil_coal_black.change_CO2e_t = (
            e18.p_fossil_coal_black.CO2e_cb_per_MWh
            * p_fossil_coal_black.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_fossil_gas.change_CO2e_t = (
            e18.p_fossil_gas.CO2e_cb_per_MWh
            * p_fossil_gas.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_fossil_ofossil.change_CO2e_t = (
            e18.p_fossil_ofossil.CO2e_cb_per_MWh
            * p_fossil_ofossil.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_renew_biomass.change_CO2e_t = (
            e18.p_renew_biomass.CO2e_cb_per_MWh
            * p_renew_biomass.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_renew.change_CO2e_t = p_renew_biomass.change_CO2e_t
        p_local_biomass.change_CO2e_t = (
            e18.p_local_biomass.CO2e_cb_per_MWh
            * p_local_biomass.change_energy_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_local.change_CO2e_t = p_local_biomass.change_CO2e_t
        # SUM(p_fossil_nuclear.change_CO2e_t,p_fossil_coal_brown.change_CO2e_t,p_fossil_coal_black.change_CO2e_t, # p_fossil_gas.change_CO2e_t,p_fossil_ofossil.change_CO2e_t)
        p_fossil.change_CO2e_t = (
            p_fossil_nuclear.change_CO2e_t
            + p_fossil_coal_brown.change_CO2e_t
            + p_fossil_coal_black.change_CO2e_t
            + p_fossil_gas.change_CO2e_t
            + p_fossil_ofossil.change_CO2e_t
        )
        p.change_CO2e_t = (
            p_fossil.change_CO2e_t + p_renew.change_CO2e_t + p_local.change_CO2e_t
        )
        p.change_CO2ee_pct = p.change_CO2e_t / p.change_energy_MWh
        p_g.change_CO2e_t = (
            p_fossil.change_CO2e_t + p_renew.change_CO2e_t
        )  # CO2e_total_2021_estimated
        p_fossil_nuclear.CO2e_total_2021_estimated = (
            e18.p_fossil_nuclear.CO2e_cb * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fossil_coal_brown.CO2e_total_2021_estimated = (
            e18.p_fossil_coal_brown.CO2e_cb * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fossil_coal_black.CO2e_total_2021_estimated = (
            e18.p_fossil_coal_black.CO2e_cb * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_fossil_gas.CO2e_total_2021_estimated = e18.p_fossil_gas.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_fossil_ofossil.CO2e_total_2021_estimated = (
            e18.p_fossil_ofossil.CO2e_cb * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        )
        p_renew_biomass.CO2e_total_2021_estimated = e18.p_renew_biomass.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_renew.CO2e_total_2021_estimated = p_renew_biomass.CO2e_total_2021_estimated
        p_local_biomass.CO2e_total_2021_estimated = e18.p_local_biomass.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        p_local.CO2e_total_2021_estimated = p_local_biomass.CO2e_total_2021_estimated
        p_fossil.CO2e_total_2021_estimated = (
            p_fossil_coal_brown.CO2e_total_2021_estimated
            + p_fossil_coal_black.CO2e_total_2021_estimated
            + p_fossil_gas.CO2e_total_2021_estimated
            + p_fossil_ofossil.CO2e_total_2021_estimated
        )
        p_g.CO2e_total_2021_estimated = (
            p_fossil.CO2e_total_2021_estimated + p_renew.CO2e_total_2021_estimated
        )
        p.CO2e_total_2021_estimated = (
            p_g.CO2e_total_2021_estimated + p_local.CO2e_total_2021_estimated
        )
        KlimaneutraleJahre = entry("In_M_duration_neutral")  # cost_climate_saved
        p_fossil_nuclear.cost_climate_saved = (
            (p_fossil_nuclear.CO2e_total_2021_estimated - p_fossil_nuclear.CO2e_cb)
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fossil_coal_brown.cost_climate_saved = (
            (
                p_fossil_coal_brown.CO2e_total_2021_estimated
                - p_fossil_coal_brown.CO2e_cb
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fossil_coal_black.cost_climate_saved = (
            (
                p_fossil_coal_black.CO2e_total_2021_estimated
                - p_fossil_coal_black.CO2e_cb
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fossil_gas.cost_climate_saved = (
            (p_fossil_gas.CO2e_total_2021_estimated - p_fossil_gas.CO2e_cb)
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_fossil_ofossil.cost_climate_saved = (
            (p_fossil_ofossil.CO2e_total_2021_estimated - p_fossil_ofossil.CO2e_cb)
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_renew_biomass.cost_climate_saved = (
            (p_renew_biomass.CO2e_total_2021_estimated - p_renew_biomass.CO2e_cb)
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_renew.cost_climate_saved = p_renew_biomass.cost_climate_saved
        p_local_biomass.cost_climate_saved = (
            (p_local_biomass.CO2e_total_2021_estimated - p_local_biomass.CO2e_cb)
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        p_local.cost_climate_saved = p_local_biomass.cost_climate_saved
        p_fossil.cost_climate_saved = (
            p_fossil_coal_brown.cost_climate_saved
            + p_fossil_coal_black.cost_climate_saved
            + p_fossil_gas.cost_climate_saved
            + p_fossil_ofossil.cost_climate_saved
        )
        p_g.cost_climate_saved = (
            p_fossil.cost_climate_saved + p_renew.cost_climate_saved
        )
        p.cost_climate_saved = (
            p_g.cost_climate_saved + p_local.cost_climate_saved
        )  # change_cost_energy
        p_fossil_nuclear.change_cost_energy = (
            p_fossil_nuclear.cost_fuel - e18.p_fossil_nuclear.cost_fuel
        )
        p_fossil_coal_brown.change_cost_energy = (
            p_fossil_coal_brown.cost_fuel - e18.p_fossil_coal_brown.cost_fuel
        )
        p_fossil_coal_black.change_cost_energy = (
            p_fossil_coal_black.cost_fuel - e18.p_fossil_coal_black.cost_fuel
        )
        p_fossil_gas.change_cost_energy = (
            p_fossil_gas.cost_fuel - e18.p_fossil_gas.cost_fuel
        )
        p_fossil_ofossil.change_cost_energy = (
            p_fossil_ofossil.cost_fuel - e18.p_fossil_ofossil.cost_fuel
        )
        p_renew_biomass.change_cost_energy = (
            e30.p_renew_biomass.cost_fuel - e18.p_renew_biomass.cost_fuel
        )
        p_renew.change_cost_energy = p_renew_biomass.change_cost_energy
        p_fossil.change_cost_energy = (
            p_fossil_coal_brown.change_cost_energy
            + p_fossil_coal_black.change_cost_energy
            + p_fossil_gas.change_cost_energy
            + p_fossil_ofossil.change_cost_energy
        )
        p_g.change_cost_energy = (
            p_fossil.change_cost_energy + p_renew.change_cost_energy
        )
        p_local_biomass.change_cost_energy = (
            p_local_biomass.cost_fuel - e18.p_local_biomass.cost_fuel
        )
        p_local.change_cost_energy = p_local_biomass.change_cost_energy
        p.change_cost_energy = (
            p_g.change_cost_energy + p_local.change_cost_energy
        )  # change_cost_mro
        p_fossil_nuclear.change_cost_mro = (
            p_fossil_nuclear.cost_mro - e18.p_fossil_nuclear.cost_mro
        )
        p_fossil_coal_brown.change_cost_mro = (
            p_fossil_coal_brown.cost_mro - e18.p_fossil_coal_brown.cost_mro
        )
        p_fossil_coal_black.change_cost_mro = (
            p_fossil_coal_black.cost_mro - e18.p_fossil_coal_black.cost_mro
        )
        p_fossil_gas.change_cost_mro = p_fossil_gas.cost_mro - e18.p_fossil_gas.cost_mro
        p_fossil_ofossil.change_cost_mro = (
            p_fossil_ofossil.cost_mro - e18.p_fossil_ofossil.cost_mro
        )
        p_renew_biomass.change_cost_mro = (
            p_renew_biomass.cost_mro - e18.p_renew_biomass.cost_mro
        )
        p_renew.change_cost_mro = p_renew_biomass.change_cost_mro
        p_local_biomass.change_cost_mro = (
            e30.p_local_biomass.cost_mro - e18.p_local_biomass.cost_mro
        )
        p_local.change_cost_mro = 0
        p_fossil.change_cost_mro = (
            p_fossil_coal_brown.change_cost_mro
            + p_fossil_coal_black.change_cost_mro
            + p_fossil_gas.change_cost_mro
            + p_fossil_ofossil.change_cost_mro
        )
        p_g.change_cost_mro = p_fossil.change_cost_mro + p_renew.change_cost_mro
        p.change_cost_mro = (
            p_g.change_cost_mro + p_local.change_cost_mro
        )  # invest_per_x
        p_renew_wind_offshore.invest_per_x = (
            ass("Ass_E_S_wind_offshore_investcosts_2030") * 1000
        )
        p_renew_geoth.invest_per_x = ass("Ass_E_P_renew_geoth_invest") * 1000
        p_reverse.invest_per_x = ass("Ass_E_P_reverse_invest_per_x") * 1000
        p_local_pv_roof.invest_per_x = (
            ass("Ass_S_A_Investitionskosten_PV_Dach_2030") * 1000
        )
        p_local_pv_facade.invest_per_x = ass("Ass_E_S_pv_facade_investcosts") * 1000
        p_local_pv_park.invest_per_x = ass("Ass_E_S_pv_park_investcosts_2030") * 1000
        p_local_pv_agri.invest_per_x = ass("Ass_E_S_pv_agri_investcosts") * 1000
        p_local_wind_onshore.invest_per_x = (
            ass("Ass_E_S_wind_onshore_investcosts_2030") * 1000
        )
        p_local_biomass.invest_per_x = ass("Ass_E_P_biomass_invest_per_x")  # invest
        p_renew_wind_offshore.invest = (
            p_renew_wind_offshore.power_to_be_installed
            * p_renew_wind_offshore.invest_per_x
            if (ags == "DG000000")
            else 0
        )
        p_wind.invest = p_renew_wind_offshore.invest
        p_renew_geoth.invest = (
            p_renew_geoth.power_to_be_installed * p_renew_geoth.invest_per_x
            if (ags == "DG000000")
            else 0
        )
        p_reverse.invest = (
            p_reverse.power_to_be_installed * p_reverse.invest_per_x
            if (ags == "DG000000")
            else 0
        )
        p_local_pv_roof.invest = (
            p_local_pv_roof.power_to_be_installed * p_local_pv_roof.invest_per_x
        )
        p_local_pv_facade.invest = (
            p_local_pv_facade.power_to_be_installed * p_local_pv_facade.invest_per_x
        )
        p_local_pv_park.invest = (
            p_local_pv_park.power_to_be_installed * p_local_pv_park.invest_per_x
        )
        p_local_pv_agri.power_to_be_installed = max(
            0,
            p_local_pv_agri.power_installable
            * p_local_pv_agri.power_to_be_installed_pct
            - p_local_pv_agri.power_installed,
        )
        p_local_wind_onshore.invest = (
            p_local_wind_onshore.power_to_be_installed
            * p_local_wind_onshore.invest_per_x
        )
        p_local_biomass.invest = (
            p_local_biomass.power_to_be_installed * p_local_biomass.invest_per_x
        )
        # p_local.invest = SUM(p_local_pv_roof.invest:DN105)
        p_renew_wind_offshore.invest_pa = (
            p_renew_wind_offshore.invest / Kalkulationszeitraum
        )
        p_wind.invest_pa = p_renew_wind_offshore.invest_pa
        p_renew_geoth.invest_pa = p_renew_geoth.invest / Kalkulationszeitraum
        p_reverse.invest_pa = p_reverse.invest / Kalkulationszeitraum
        p_local_pv_roof.invest_pa = p_local_pv_roof.invest / Kalkulationszeitraum
        p_local_pv_facade.invest_pa = p_local_pv_facade.invest / Kalkulationszeitraum
        p_local_pv_park.invest_pa = p_local_pv_park.invest / Kalkulationszeitraum
        p_local_pv_agri.invest = (
            p_local_pv_agri.power_to_be_installed * p_local_pv_agri.invest_per_x
        )
        p_local_wind_onshore.invest_pa = (
            p_local_wind_onshore.invest / Kalkulationszeitraum
        )
        p_local_biomass.invest_pa = p_local_biomass.invest / Kalkulationszeitraum
        p_local_pv_agri.invest_pa = p_local_pv_agri.invest / Kalkulationszeitraum
        p_local_pv_roof.invest_com = (
            p_local_pv_roof.invest
            * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2)
            / (b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2)
        )
        p_local_pv_facade.invest_com = (
            p_local_pv_facade.invest
            * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2)
            / (b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2)
        )
        p_local_pv_park.invest_com = 0
        p_local_pv_agri.invest_com = 0
        p_local.invest_com = (
            p_local_pv_roof.invest_com + p_local_pv_facade.invest_com
        )  # SUM(p_local_pv_roof.invest_com:DO105)
        p_local_pv_roof.invest_pa_com = (
            p_local_pv_roof.invest_com / Kalkulationszeitraum
        )
        p_local_pv_facade.invest_pa_com = (
            p_local_pv_facade.invest_com / Kalkulationszeitraum
        )
        p_local_pv_park.invest_pa_com = (
            p_local_pv_park.invest_com / Kalkulationszeitraum
        )
        p_local_pv_agri.invest_pa_com = (
            p_local_pv_agri.invest_com / Kalkulationszeitraum
        )
        p_local.invest_pa_com = (
            p_local_pv_roof.invest_pa_com
            + p_local_pv_facade.invest_pa_com
            + p_local_pv_park.invest_pa_com
            + p_local_pv_agri.invest_pa_com
        )  # SUM(p_local_pv_roof.invest_pa_com:DL105) # nvest_pa_outside
        p_renew_wind_offshore.invest_pa_outside = (
            0
            if (ags == "DG000000")
            else p_renew_wind_offshore.power_to_be_installed
            * p_renew_wind_offshore.invest_per_x
            / Kalkulationszeitraum
            * d.energy
            / ass("Ass_E_P_total_2035")
        )
        p_renew.pct_energy = (
            p_renew_pv.pct_energy
            + e30.p_wind.pct_energy
            + p_renew_biomass.pct_energy
            + p_renew_geoth.pct_energy
            + p_renew_hydro.pct_energy
            + p_reverse.pct_energy
        )
        p_renew_geoth.invest_pa_outside = (
            0
            if (ags == "DG000000")
            else p_renew_geoth.power_to_be_installed
            * p_renew_geoth.invest_per_x
            / Kalkulationszeitraum
            * d.energy
            / ass("Ass_E_P_total_2035")
        )
        p_reverse.invest_pa_outside = (
            0
            if (ags == "DG000000")
            else p_reverse.power_to_be_installed
            * p_reverse.invest_per_x
            / Kalkulationszeitraum
            * d.energy
            / ass("Ass_E_P_total_2035")
        )
        p_renew_wind_offshore.invest_outside = (
            0
            if (ags == "DG000000")
            else p_renew_wind_offshore.invest * d.energy / ass("Ass_E_P_total_2035")
        )
        p_wind.invest_outside = p_renew_wind_offshore.invest_outside
        p_renew_geoth.invest_outside = (
            0
            if (ags == "DG000000")
            else p_renew_geoth.invest * d.energy / ass("Ass_E_P_total_2035")
        )
        p_reverse.invest_outside = (
            0
            if (ags == "DG000000")
            else p_reverse.invest * d.energy / ass("Ass_E_P_total_2035")
        )
        p_renew_wind_offshore.pct_of_wage = ass("Ass_E_P_plant_construct_cost_personel")
        p_renew_geoth.pct_of_wage = ass("Ass_E_P_plant_construct_cost_personel")
        p_reverse.pct_of_wage = ass("Ass_E_P_plant_construct_cost_personel")
        p_local_pv_roof.pct_of_wage = (
            0.32  # Todo fact('Fakt_S_B_ratio_costs_installation_PV')
        )
        p_local_pv_facade.pct_of_wage = (
            0.32  # Todo fact('Fakt_S_B_ratio_costs_installation_PV')
        )
        p_local_pv_park.pct_of_wage = (
            0.32  # Todo fact('Fakt_S_B_ratio_costs_installation_PV')
        )
        p_local_pv_agri.pct_of_wage = fact("Fakt_S_B_ratio_costs_installation_PV")
        p_local_pv_agri.pct_of_wage = (
            0.32  # Todo remove fact('Fakt_S_B_ratio_costs_installation_PV')
        )
        p_local_wind_onshore.pct_of_wage = ass("Ass_E_P_plant_construct_cost_personel")
        p_local_biomass.pct_of_wage = ass(
            "Ass_E_P_plant_construct_cost_personel"
        )  # cost_wage
        p_renew_wind_offshore.cost_wage = (
            p_renew_wind_offshore.invest_pa
            * p_renew_wind_offshore.pct_of_wage
            / Kalkulationszeitraum
        )
        p_wind.cost_wage = p_renew_wind_offshore.cost_wage
        p_renew_geoth.cost_wage = p_renew_geoth.invest_pa * p_renew_geoth.pct_of_wage
        p_reverse.cost_wage = p_reverse.invest_pa * p_reverse.pct_of_wage
        p_local_pv_roof.cost_wage = (
            p_local_pv_roof.invest_pa * p_local_pv_roof.pct_of_wage
        )
        p_local_pv_facade.cost_wage = (
            p_local_pv_facade.invest_pa * p_local_pv_facade.pct_of_wage
        )
        p_local_pv_park.cost_wage = (
            p_local_pv_park.invest_pa * p_local_pv_park.pct_of_wage
        )
        p_local_pv_agri.cost_wage = (
            p_local_pv_agri.invest_pa * p_local_pv_agri.pct_of_wage
        )
        p_local_wind_onshore.cost_wage = (
            p_local_wind_onshore.invest_pa * p_local_wind_onshore.pct_of_wage
        )
        p_local_biomass.cost_wage = (
            p_local_biomass.invest_pa
            * p_local_biomass.pct_of_wage
            / Kalkulationszeitraum
        )  # ratio_wage_to_emplo
        p_renew_wind_offshore.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_renew_geoth.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_reverse.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_local_pv_roof.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_local_pv_facade.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_local_pv_park.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_local_pv_agri.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_local_wind_onshore.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )
        p_local_biomass.ratio_wage_to_emplo = ass(
            "Ass_S_B_Stückkosten_Personalkosten_Elektriker"
        )  # demand_emplo
        p_renew_wind_offshore.demand_emplo = (
            p_renew_wind_offshore.cost_wage / p_renew_wind_offshore.ratio_wage_to_emplo
            if (ags == "DG000000")
            else 0
        )
        p_wind.demand_emplo = p_renew_wind_offshore.demand_emplo
        p_renew_geoth.demand_emplo = (
            p_renew_geoth.cost_wage / p_renew_geoth.ratio_wage_to_emplo
            if (ags == "DG000000")
            else 0
        )
        p_reverse.demand_emplo = (
            p_reverse.cost_wage / p_reverse.ratio_wage_to_emplo
            if (ags == "DG000000")
            else 0
        )
        p_renew.demand_emplo = (
            p_wind.demand_emplo + p_renew_geoth.demand_emplo + p_reverse.demand_emplo
        )
        p_local_pv_roof.demand_emplo = (
            p_local_pv_roof.cost_wage / p_local_pv_roof.ratio_wage_to_emplo
        )
        p_local_pv_facade.demand_emplo = (
            p_local_pv_facade.cost_wage / p_local_pv_facade.ratio_wage_to_emplo
        )
        p_local_pv_park.demand_emplo = (
            p_local_pv_park.cost_wage / p_local_pv_park.ratio_wage_to_emplo
        )
        p_local_pv_agri.demand_emplo = (
            p_local_pv_agri.cost_wage / p_local_pv_agri.ratio_wage_to_emplo
        )
        p_local_wind_onshore.demand_emplo = (
            p_local_wind_onshore.cost_wage / p_local_wind_onshore.ratio_wage_to_emplo
        )
        p_local_biomass.demand_emplo = (
            p_local_biomass.cost_wage / p_local_biomass.ratio_wage_to_emplo
        )
        p_local_pv.demand_emplo = (
            p_local_pv_roof.demand_emplo
            + p_local_pv_facade.demand_emplo
            + p_local_pv_park.demand_emplo
            + p_local_pv_agri.demand_emplo
        )  # SUM(p_local_pv_roof.demand_emplo:p_local_pv_agri.demand_emplo)
        p_local.demand_emplo = (
            p_local_pv.demand_emplo
            + p_local_wind_onshore.demand_emplo
            + p_local_biomass.demand_emplo
        )  # emplo_existing
        p_renew_wind_offshore.emplo_existing = (
            fact("Fact_E_P_wind_offshore_emplo_2018") if (ags == "DG000000") else 0
        )
        p_renew_geoth.emplo_existing = (
            fact("Fact_E_P_plant_construct_emplo_2018")
            * p_renew_geoth.demand_emplo
            / (p_renew_geoth.demand_emplo + p_reverse.demand_emplo)
            if (ags == "DG000000")
            else 0
        )
        p_wind.emplo_existing = p_renew_wind_offshore.emplo_existing
        p_renew.emplo_existing = p_wind.emplo_existing + p_renew_geoth.emplo_existing
        p_reverse.emplo_existing = (
            fact("Fact_E_P_plant_construct_emplo_2018")
            * p_reverse.demand_emplo
            / (p_renew_geoth.demand_emplo + p_reverse.demand_emplo)
            if (ags == "DG000000")
            else 0
        )
        p_local_pv.emplo_existing = (
            fact("Fact_B_P_install_elec_emplo_2017")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        p_local_wind_onshore.emplo_existing = (
            fact("Fact_E_P_wind_onshore_emplo_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        p_local_biomass.emplo_existing = (
            fact("Fact_E_P_bioenergy_emplo_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        p_local.emplo_existing = (
            p_local_pv.emplo_existing
            + p_local_wind_onshore.emplo_existing
            + p_local_biomass.emplo_existing
        )  # demand_emplo_new
        p_wind.demand_emplo_new = max(0, p_wind.demand_emplo - p_wind.emplo_existing)
        p_renew_geoth.demand_emplo_new = max(
            0, p_renew_geoth.demand_emplo - p_renew_geoth.emplo_existing
        )
        p_reverse.demand_emplo_new = max(
            0, p_reverse.demand_emplo - p_reverse.emplo_existing
        )
        p_renew.demand_emplo_new = (
            p_wind.demand_emplo_new
            + p_renew_geoth.demand_emplo_new
            + p_reverse.demand_emplo_new
        )
        p_local_pv.demand_emplo_new = max(
            0, p_local_pv.demand_emplo - p_local_pv.emplo_existing
        )
        p_local_wind_onshore.demand_emplo_new = max(
            0, p_local_wind_onshore.demand_emplo - p_local_wind_onshore.emplo_existing
        )
        p_local_biomass.demand_emplo_new = max(
            0, p_local_biomass.demand_emplo - p_local_biomass.emplo_existing
        )
        p_local.demand_emplo_new = (
            p_local_pv.demand_emplo_new
            + p_local_wind_onshore.demand_emplo_new
            + p_local_biomass.demand_emplo_new
        )  # lifecycle
        p_renew_wind_offshore.lifecycle = ass("Ass_S_WEA_Nutzungsdauer")
        p_local_pv_roof.lifecycle = ass("Ass_S_B_PV_Nutzungsdauer")
        p_local_pv_facade.lifecycle = ass("Ass_S_B_PV_Nutzungsdauer")
        p_local_pv_park.lifecycle = ass("Ass_S_B_PV_Nutzungsdauer")
        p_local_pv_agri.lifecycle = ass("Ass_S_B_PV_Nutzungsdauer")
        p_local_wind_onshore.lifecycle = ass("Ass_S_WEA_Nutzungsdauer")
        p_local_biomass.lifecycle = ass("Ass_S_B_Lebensdauer")  # energy_installable
        p_renew_wind_offshore.energy_installable = (
            p_renew_wind_offshore.full_load_hour
            * p_renew_wind_offshore.power_installable
        )
        p_local_pv_roof.energy_installable = (
            p_local_pv_roof.power_installable * p_local_pv_roof.full_load_hour
        )
        p_local_pv_facade.energy_installable = (
            p_local_pv_facade.full_load_hour * p_local_pv_facade.power_installable
        )
        p_local_pv_park.energy_installable = (
            p_local_pv_park.full_load_hour * p_local_pv_park.power_installable
        )
        p_local_pv.power_to_be_installed = (
            p_local_pv_roof.power_to_be_installed
            + p_local_pv_facade.power_to_be_installed
            + p_local_pv_park.power_to_be_installed
            + p_local_pv_agri.power_to_be_installed
        )  # SUM(p_local_pv_roof.power_to_be_installed:p_local_pv_agri.power_to_be_installed) # full_load_hour
        p_local_wind_onshore.energy_installable = (
            p_local_wind_onshore.full_load_hour * p_local_wind_onshore.power_installable
        )
        p_local_biomass.energy_installable = (
            p_local_biomass.power_installable * p_local_biomass.full_load_hour
        )
        p_local_pv.energy_installable = (
            p_local_pv_roof.energy_installable
            + p_local_pv_facade.energy_installable
            + p_local_pv_park.energy_installable
            + p_local_pv_agri.energy_installable
        )  # SUM(p_local_pv_roof.energy_installable:p_local_pv_agri.energy_installable) #cost_mro_pa
        p_renew.cost_mro_pa = p_renew.cost_mro
        p_renew_pv.cost_mro_pa = p_renew_pv.cost_mro
        p_renew_pv_roof.cost_mro_pa = p_renew_pv_roof.cost_mro
        p_renew_pv_facade.cost_mro_pa = p_renew_pv_facade.cost_mro
        p_renew_pv_park.cost_mro_pa = p_renew_pv_park.cost_mro
        p_renew_pv_agri.cost_mro_pa = p_renew_pv_agri.cost_mro
        p_wind.cost_mro_pa = p_wind.cost_mro
        p_renew_wind_onshore.cost_mro_pa = p_renew_wind_onshore.cost_mro
        p_renew_wind_offshore.cost_mro_pa = p_renew_wind_offshore.cost_mro
        p_renew_biomass.cost_mro_pa = p_renew_biomass.cost_mro
        p_renew_geoth.cost_mro_pa = p_renew_geoth.cost_mro
        p_renew_hydro.cost_mro_pa = p_renew_hydro.cost_mro
        p_reverse.cost_mro_pa = p_reverse.cost_mro
        p_local.cost_mro_pa = p_local.cost_mro
        p_local_pv.cost_mro_pa = p_local_pv.cost_mro
        p_local_pv_roof.cost_mro_pa = p_local_pv_roof.cost_mro
        p_local_pv_facade.cost_mro_pa = p_local_pv_facade.cost_mro
        p_local_pv_park.cost_mro_pa = p_local_pv_park.cost_mro
        p_local_pv_agri.cost_mro_pa = p_local_pv_agri.cost_mro
        p_local_wind_onshore.cost_mro_pa = p_local_wind_onshore.cost_mro
        p_local_biomass.cost_mro_pa = p_local_biomass.cost_mro
        p_local_biomass_gaseous.power_to_be_installed_pct = (
            p_local_pv_agri.energy / p_local_pv_agri.energy_installable
        )
        p_local_hydro.cost_mro_pa = p_local_hydro.cost_mro
        p_local.invest_pa = (
            p_local_pv_roof.invest_pa
            + p_local_pv_facade.invest_pa
            + p_local_pv_park.invest_pa
            + p_local_pv_agri.invest_pa
            + p_local_wind_onshore.invest_pa
            + p_local_biomass.invest_pa
        )  # SUM(p_local_pv_roof.invest_pa:DK105) # invest_com

    except Exception as e:
        print(e)
        raise
