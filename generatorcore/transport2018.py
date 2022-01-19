#!/usr/bin/env python
# coding: utf-8

# # Laden der Datentabellen und deren Suchfunktionen

from dataclasses import dataclass, field, InitVar, asdict
from .setup import *

# Es gibt 5 Datentabellen:
# * Fakten: <span class="mark">facts</span>
# * Annahmen: <span class="mark">assumptions</span>
# * Kommunenspezifische Daten: <span class="mark">rowCom</span>
# * Landkreisdaten: <span class="mark">rowK</span>
# * Bundesländerdaten: <span class="mark">rowBL</span>
#
# Auf die Daten könnt ihr mittels folgender Funktionen zugreifen:
# * fact()
# * ass()
# * valCom()
# * valK()
# * valBL()

# fact('Fact_A_S_biomass_fec_2018')
# display(facts)
# display(assumptions)
# display(rowK)
# display(rowBL)
# display(rowCom)


# # Template für die Sektor-Variablen (Excel-Spaltennamen)

#  Definition der relevanten Spaltennamen für den Sektor T (18)
@dataclass
class TColVars:

    energy: float = None
    mileage: float = None
    transport_capacity_pkm: float = None
    transport_capacity_tkm: float = None
    demand_petrol: float = None
    demand_jetfuel: float = None
    demand_diesel: float = None
    demand_fueloil: float = None
    demand_lpg: float = None
    demand_gas: float = None
    demand_biogas: float = None
    demand_bioethanol: float = None
    demand_biodiesel: float = None
    demand_electricity: float = None
    CO2e_cb: float = None
    CO2e_total: float = None

    def _get(self, i):

        if i == 0:
            val = self.energy
        elif i == 1:
            val = self.mileage
        elif i == 2:
            val = self.transport_capacity_pkm
        elif i == 3:
            val = self.transport_capacity_tkm
        elif i == 4:
            val = self.demand_petrol
        elif i == 5:
            val = self.demand_jetfuel
        elif i == 6:
            val = self.demand_diesel
        elif i == 7:
            val = self.demand_fueloil
        elif i == 8:
            val = self.demand_lpg
        elif i == 9:
            val = self.demand_gas
        elif i == 10:
            val = self.demand_biogas
        elif i == 11:
            val = self.demand_bioethanol
        elif i == 12:
            val = self.demand_biodiesel
        elif i == 13:
            val = self.demand_electricity
        elif i == 14:
            val = self.CO2e_cb
        else:
            val = None

        if val == None:
            return 0
        else:
            return val

    def _set(self, i, val):
        if i == 0:
            self.energy = val
        elif i == 1:
            self.mileage = val
        elif i == 2:
            self.transport_capacity_pkm = val
        elif i == 3:
            self.transport_capacity_tkm = val
        elif i == 4:
            self.demand_petrol = val
        elif i == 5:
            self.demand_jetfuel = val
        elif i == 6:
            self.demand_diesel = val
        elif i == 7:
            self.demand_fueloil = val
        elif i == 8:
            self.demand_lpg = val
        elif i == 9:
            self.demand_gas = val
        elif i == 10:
            self.demand_biogas = val
        elif i == 11:
            self.demand_bioethanol = val
        elif i == 12:
            self.demand_biodiesel = val
        elif i == 13:
            self.demand_electricity = val
        elif i == 14:
            self.CO2e_cb = val


@dataclass
class T18:
    t: TColVars = TColVars()
    g: TColVars = TColVars()
    g_planning: TColVars = TColVars()
    air_inter: TColVars = TColVars()
    air_dmstc: TColVars = TColVars()
    road: TColVars = TColVars()
    road_action_charger: TColVars = TColVars()
    road_car: TColVars = TColVars()
    road_car_it_ot: TColVars = TColVars()
    road_car_ab: TColVars = TColVars()
    road_bus: TColVars = TColVars()
    road_bus_action_infra: TColVars = TColVars()
    road_gds: TColVars = TColVars()
    road_gds_ldt: TColVars = TColVars()
    road_gds_ldt_it_ot: TColVars = TColVars()
    road_gds_ldt_ab: TColVars = TColVars()
    road_gds_mhd: TColVars = TColVars()
    road_ppl: TColVars = TColVars()
    road_gds_mhd_it_ot: TColVars = TColVars()
    road_gds_mhd_ab: TColVars = TColVars()
    rail_ppl: TColVars = TColVars()
    rail_ppl_: TColVars = TColVars()
    rail_ppl_metro: TColVars = TColVars()
    rail_ppl_metro_action_infra: TColVars = TColVars()
    rail_gds: TColVars = TColVars()
    rail_action_invest_infra: TColVars = TColVars()
    rail_action_invest_station: TColVars = TColVars()
    ship_dmstc: TColVars = TColVars()
    ship_inter: TColVars = TColVars()
    other_foot: TColVars = TColVars()
    other_cycl: TColVars = TColVars()

    # übergeordnete Zeilen
    air: TColVars = TColVars()
    rail: TColVars = TColVars()
    ship: TColVars = TColVars()
    other: TColVars = TColVars()

    # Bereitstellung (Energieträgersummen)
    s: TColVars = TColVars()
    s_petrol: TColVars = TColVars()
    s_jetfuel: TColVars = TColVars()
    s_diesel: TColVars = TColVars()
    s_fueloil: TColVars = TColVars()
    s_lpg: TColVars = TColVars()
    s_gas: TColVars = TColVars()
    s_biogas: TColVars = TColVars()
    s_bioethanol: TColVars = TColVars()
    s_biodiesel: TColVars = TColVars()
    s_elec: TColVars = TColVars()
    s_hydrogen: TColVars = TColVars()
    s_emethan: TColVars = TColVars()

    # erzeuge dictionry

    def dict(self):
        return asdict(self)


# # Berechnungsfunktion Transport 2018

# Berechnungsfunktion Transport 2018


def Transport2018_calc(root):
    # Todo remove after impl.

    if entry("In_M_AGS_com") == "DG000000":
        root.t18.rail_ppl_metro.mileage = 309000000
        root.t18.road_bus.mileage = 2531000000
    elif entry("In_M_AGS_com") == "03159016":
        root.t18.rail_ppl_metro.mileage = 0
        root.t18.road_bus.mileage = 1752789.9193474643

    try:
        Million = 1000000
        ags = entry("In_M_AGS_com")
        t = root.t18
        # res 61.700.000.000 Pers km
        t.air_inter.transport_capacity_pkm = (
            fact("Fact_T_D_Air_nat_trnsprt_ppl_2019")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 1.507.745.000 t km
        t.air_inter.transport_capacity_tkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * fact("Fact_T_D_Air_inter_nat_ratio_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 113.722.222 MWh
        t.air_inter.demand_jetfuel = (
            fact("Fact_T_S_Air_nat_EB_inter_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 30.020.293  t/a
        t.air_inter.CO2e_cb = (
            t.air_inter.demand_jetfuel
            # Todo: In der Excel werden   Emissionen durch Benzinverbrauch im nationalen Flugverkehr addiert: Prüfen (Ergebnis weicht daher ab)
            * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
        )
        # res 113.722.222 MWh
        t.air_inter.energy = t.air_inter.demand_jetfuel

        # -------------------

        # res 10.100.000.000 Pers km
        t.air_dmstc.transport_capacity_pkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_ppl_2019")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 79.355.000 t km
        t.air_dmstc.transport_capacity_tkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * fact("Fact_T_D_Air_dmstc_nat_ratio_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 108.056 MWh
        t.air_dmstc.demand_petrol = (
            fact("Fact_T_S_Air_petrol_fec_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 7.805.556 MWh
        t.air_dmstc.demand_jetfuel = (
            fact("Fact_T_S_Air_nat_EB_dmstc_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 2.085.724  t/a
        t.air_dmstc.CO2e_cb = t.air_dmstc.demand_jetfuel * fact(
            "Fact_T_S_jetfuel_EmFa_tank_wheel_2018"
        ) + t.air_dmstc.demand_petrol * fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")

        # res 7.913.611 MWh
        t.air_dmstc.energy = t.air_dmstc.demand_jetfuel + t.air_dmstc.demand_petrol

        t.air.energy = t.air_inter.energy + t.air_dmstc.energy

        # -----------------------
        # res 456.061.500.000 Fz km
        t.road_car_it_ot.mileage = entry("In_T_mil_car_it_at") * Million

        # res 657.704.211.506 Pers km
        t.road_car_it_ot.transport_capacity_pkm = t.road_car_it_ot.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )

        # res 140.583.679 MWh
        t.road_car_it_ot.demand_petrol = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 137.907.651 MWh
        t.road_car_it_ot.demand_diesel = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )

        # res 3.211.348 MWh
        t.road_car_it_ot.demand_lpg = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 550.841 MWh
        t.road_car_it_ot.demand_gas = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 129.210 MWh
        t.road_car_it_ot.demand_biogas = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res  6.316.717 MWh
        t.road_car_it_ot.demand_bioethanol = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 8.026.371 MWh
        t.road_car_it_ot.demand_biodiesel = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )

        # res 121.985 MWh
        t.road_car_it_ot.demand_electricity = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_it_at_2018")
        )

        # res 36.749.000.000 Fz km
        t.road_gds_ldt_it_ot.mileage = entry("In_T_mil_ldt_it_at") * Million

        t.road_gds_ldt_it_ot.demand_electricity = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_it_at_2018")
        )

        # 14.549.300.000 Fz km

        t.road_gds_ldt_ab.mileage = entry("In_T_mil_ldt_ab") * Million

        t.road_gds_ldt_ab.demand_electricity = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_ab_2018")
        )

        # 28.430.600.000 Fz km
        t.road_gds_mhd_it_ot.mileage = (
            entry("In_T_mil_mhd_it_at") * Million - t.road_bus.mileage
        )

        t.road_gds_mhd_it_ot.demand_electricity = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
        )

        # 35.937.900.000 Fz km
        t.road_gds_mhd_ab.mileage = entry("In_T_mil_mhd_ab") * Million

        t.road_gds_mhd_ab.demand_electricity = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
        )
        # 308.900.000 Fz km
        # t.rail_ppl_metro.mileage = (
        # todo rail_ppl_metro.mileage = (VLOOKUP(LK&" *  *  * ",Verkehr_DestatisDaten!B4:I507,7,FALSE) * 10^6 * entry('In_M_population_com_2018') / entry('In_M_population_dis'))
        # )
        t.rail_ppl_metro.demand_electricity = t.rail_ppl_metro.mileage * fact(
            "Fact_T_S_Rl_Metro_SEC_fzkm_2018"
        )

        # res  75.732.141 t/a

        t.road_car_it_ot.CO2e_cb = (
            t.road_car_it_ot.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        )

        # res 296.847.801 MWh
        t.road_car_it_ot.energy = (
            t.road_car_it_ot.demand_petrol
            + t.road_car_it_ot.demand_diesel
            + t.road_car_it_ot.demand_lpg
            + t.road_car_it_ot.demand_gas
            + t.road_car_it_ot.demand_biogas
            + t.road_car_it_ot.demand_bioethanol
            + t.road_car_it_ot.demand_biodiesel
            + t.road_car_it_ot.demand_electricity
        )

        # --------------------

        # res 200.879.200.000 Fz km
        t.road_car_ab.mileage = entry("In_T_mil_car_ab") * Million

        # res 289.695.788.494 Pers km
        t.road_car_ab.transport_capacity_pkm = t.road_car_ab.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )

        # res 71.637.731 MWh
        t.road_car_ab.demand_petrol = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        # res 68.266.402 MWh
        t.road_car_ab.demand_diesel = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )

        # res 1.636.418 MWh
        t.road_car_ab.demand_lpg = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        # res 242.626 MWh
        t.road_car_ab.demand_gas = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            # Todo Prüfen warum hier ...SEC_petrol_it_at verwendet wird und nicht ...SEC_petrol_ab
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 56.912 MWh
        t.road_car_ab.demand_biogas = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            # Todo Prüfen warum hier ...SEC_petrol_it_at verwendet wird und nicht ...SEC_petrol_ab
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res  3.218.832 MWh
        t.road_car_ab.demand_bioethanol = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        # res 3.973.177 MWh
        t.road_car_ab.demand_biodiesel = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )

        # res 85.897 MWh
        t.road_car_ab.demand_electricity = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_ab_2018")
        )

        # 38.048.389 t/a
        t.road_car_ab.CO2e_cb = (
            t.road_car_ab.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        )

        # res 149.117.995 MWh
        t.road_car_ab.energy = (
            t.road_car_ab.demand_petrol
            + t.road_car_ab.demand_diesel
            + t.road_car_ab.demand_lpg
            + t.road_car_ab.demand_gas
            + t.road_car_ab.demand_biogas
            + t.road_car_ab.demand_bioethanol
            + t.road_car_ab.demand_biodiesel
            + t.road_car_ab.demand_electricity
        )

        # ----------------

        # res 2.343.000.000 Fz km
        # todo t.road_bus.mileage = (VLOOKUP(LK&" *  *  * ",Verkehr_DestatisDaten!B4:I507,8,FALSE) * 10^6 * entry('In_M_population_com_2018') / entry('In_M_population_dis'))

        # res 35.594.900.435 Pers km
        t.road_bus.transport_capacity_pkm = t.road_bus.mileage * fact(
            "Fact_T_D_lf_ppl_Bus_2018"
        )

        # res 8.426.134 MWh
        t.road_bus.demand_diesel = (
            t.road_bus.mileage
            * fact("Fact_T_S_Bus_frac_diesel_with_hybrid_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 162.136 MWh
        t.road_bus.demand_gas = (
            t.road_bus.mileage
            * fact("Fact_T_S_Bus_frac_cng_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 38.032 MWh
        t.road_bus.demand_biogas = (
            t.road_bus.mileage
            * fact("Fact_T_S_Bus_frac_cng_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 485.406 MWh
        t.road_bus.demand_biodiesel = (
            t.road_bus.mileage
            * fact("Fact_T_S_Bus_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 13.854 MWh
        t.road_bus.demand_electricity = (
            t.road_bus.mileage
            * fact("Fact_T_S_Bus_frac_bev_stock_2018")
            * fact("Fact_T_S_Bus_SEC_elec_2018")
        )

        t.road_bus.demand_lpg = 0

        # 2.278.190 t/a

        t.road_bus.CO2e_cb = (
            t.road_bus.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_bus.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + t.road_bus.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + t.road_bus.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_bus.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )

        # res 9.125.561 MWh
        t.road_bus.energy = (
            t.road_bus.demand_diesel
            + t.road_bus.demand_gas
            + t.road_bus.demand_biogas
            + t.road_bus.demand_biodiesel
            + t.road_bus.demand_electricity
        )

        # ---------------------

        # 5.516.114.569 t km
        t.road_gds_ldt_it_ot.transport_capacity_tkm = (
            t.road_gds_ldt_it_ot.mileage * fact("Fact_T_D_lf_gds_LDT_2018")
        )

        # 863.649 MWh
        t.road_gds_ldt_it_ot.demand_petrol = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        # 30.129.512 MWh
        t.road_gds_ldt_it_ot.demand_diesel = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )

        # 127.848 MWh
        t.road_gds_ldt_it_ot.demand_lpg = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        # 38.806 MWh
        t.road_gds_ldt_it_ot.demand_bioethanol = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        # 1.753.569 MWh
        t.road_gds_ldt_it_ot.demand_biodiesel = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )

        # 29.887 MWh
        t.road_gds_ldt_it_ot.demand_electricity = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_it_at_2018")
        )

        # 8.294.035 t/a
        t.road_gds_ldt_it_ot.CO2e_cb = (
            t.road_gds_ldt_it_ot.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_it_ot.demand_lpg
            * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        )

        # 32.943.271 MWh
        t.road_gds_ldt_it_ot.energy = (
            t.road_gds_ldt_it_ot.demand_petrol
            + t.road_gds_ldt_it_ot.demand_diesel
            + t.road_gds_ldt_it_ot.demand_lpg
            + t.road_gds_ldt_it_ot.demand_bioethanol
            + t.road_gds_ldt_it_ot.demand_biodiesel
            + t.road_gds_ldt_it_ot.demand_electricity
        )

        # -------------------------

        # 2.183.885.431 t km
        t.road_gds_ldt_ab.transport_capacity_tkm = t.road_gds_ldt_ab.mileage * fact(
            "Fact_T_D_lf_gds_LDT_2018"
        )

        # 443.472 MWh
        t.road_gds_ldt_ab.demand_petrol = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        # 16.610.550 MWh
        t.road_gds_ldt_ab.demand_diesel = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )

        # 65.648 MWh
        t.road_gds_ldt_ab.demand_lpg = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        # 19.926 MWh
        t.road_gds_ldt_ab.demand_bioethanol = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        # 966.752 MWh
        t.road_gds_ldt_ab.demand_biodiesel = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )

        # 20.475 MWh
        t.road_gds_ldt_ab.demand_electricity = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_ab_2018")
        )

        # 4.562.536 t/a

        t.road_gds_ldt_ab.CO2e_cb = (
            t.road_gds_ldt_ab.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_ab.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        )

        # 18.126.823 MWh
        t.road_gds_ldt_ab.energy = (
            t.road_gds_ldt_ab.demand_petrol
            + t.road_gds_ldt_ab.demand_diesel
            + t.road_gds_ldt_ab.demand_lpg
            + t.road_gds_ldt_ab.demand_bioethanol
            + t.road_gds_ldt_ab.demand_biodiesel
            + t.road_gds_ldt_ab.demand_electricity
        )

        # -----------------------

        # 212.745.261.612 t km
        t.road_gds_mhd_it_ot.transport_capacity_tkm = (
            t.road_gds_mhd_it_ot.mileage * fact("Fact_T_D_lf_gds_MHD_2018")
        )

        # 75.928.091 MWh
        t.road_gds_mhd_it_ot.demand_diesel = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 58.690 MWh
        t.road_gds_mhd_it_ot.demand_gas = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 13.767 MWh
        t.road_gds_mhd_it_ot.demand_biogas = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 4.419.095 MWh
        t.road_gds_mhd_it_ot.demand_biodiesel = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 13.271 MWh
        t.road_gds_mhd_it_ot.demand_electricity = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
        )

        # 20.246.442 t/a

        t.road_gds_mhd_it_ot.CO2e_cb = t.road_gds_mhd_it_ot.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        ) + t.road_gds_mhd_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")

        # 80.432.915 MWh
        t.road_gds_mhd_it_ot.energy = (
            t.road_gds_mhd_it_ot.demand_diesel
            + t.road_gds_mhd_it_ot.demand_gas
            + t.road_gds_mhd_it_ot.demand_biogas
            + t.road_gds_mhd_it_ot.demand_biodiesel
            + t.road_gds_mhd_it_ot.demand_electricity
        )

        # --------------

        # 268.922.145.057 t km
        t.road_gds_mhd_ab.transport_capacity_tkm = t.road_gds_mhd_ab.mileage * fact(
            "Fact_T_D_lf_gds_MHD_2018"
        )

        # 98.546.344 MWh
        t.road_gds_mhd_ab.demand_diesel = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 76.174 MWh
        t.road_gds_mhd_ab.demand_gas = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 17.868 MWh
        t.road_gds_mhd_ab.demand_biogas = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 5.735.502 MWh
        t.road_gds_mhd_ab.demand_biodiesel = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 23.251 MWh
        t.road_gds_mhd_ab.demand_electricity = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
        )

        # 26.277.664 t/a
        t.road_gds_mhd_ab.CO2e_cb = t.road_gds_mhd_ab.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        ) + t.road_gds_mhd_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")

        # 104.399.138 MWh
        t.road_gds_mhd_ab.energy = (
            t.road_gds_mhd_ab.demand_diesel
            + t.road_gds_mhd_ab.demand_gas
            + t.road_gds_mhd_ab.demand_biogas
            + t.road_gds_mhd_ab.demand_biodiesel
            + t.road_gds_mhd_ab.demand_electricity
        )

        # -----------------

        t.rail_ppl_.demand_diesel = entry("In_T_ec_rail_ppl_diesel") * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )
        t.rail_ppl_.demand_biodiesel = entry("In_T_ec_rail_ppl_diesel") * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )
        t.rail_ppl_.demand_electricity = entry("In_T_ec_rail_ppl_elec")
        t.rail_ppl_.demand_petrol = 0
        t.rail_ppl_.demand_jetfuel = 0
        t.rail_ppl_.demand_lpg = 0
        t.rail_ppl_.demand_gas = 0
        t.rail_ppl_.demand_biogas = 0
        t.rail_ppl_.demand_bioethanol = 0
        t.rail_ppl_.CO2e_cb = (
            t.rail_ppl_.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.rail_ppl_.demand_jetfuel * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
            + t.rail_ppl_.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.rail_ppl_.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.rail_ppl_.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + t.rail_ppl_.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + t.rail_ppl_.demand_bioethanol * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + t.rail_ppl_.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.rail_ppl_.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.rail_ppl_.CO2e_total = t.rail_ppl_.CO2e_cb

        t.rail_ppl_.energy = (
            t.rail_ppl_.demand_diesel
            + t.rail_ppl_.demand_biodiesel
            + t.rail_ppl_.demand_electricity
        )

        t.rail_ppl_.transport_capacity_pkm = (
            t.rail_ppl_.demand_diesel + t.rail_ppl_.demand_biodiesel
        ) / fact(
            "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        ) + t.rail_ppl_.demand_electricity / fact(
            "Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018"
        )

        t.rail_ppl_.mileage = t.rail_ppl_.transport_capacity_pkm / fact(
            "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        )
        t.rail_ppl_.transport_capacity_pkm = (
            t.rail_ppl_.demand_diesel + t.rail_ppl_.demand_biodiesel
        ) / fact(
            "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        ) + t.rail_ppl_.demand_electricity / fact(
            "Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018"
        )

        t.rail_ppl_metro.demand_electricity = t.rail_ppl_metro.mileage * fact(
            "Fact_T_S_Rl_Metro_SEC_fzkm_2018"
        )

        t.rail_ppl.demand_electricity = (
            t.rail_ppl_.demand_electricity + t.rail_ppl_metro.demand_electricity
        )

        # 3.164.605 MWh
        t.rail_ppl.demand_diesel = entry("In_T_ec_rail_ppl_diesel") * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )

        # 184.183 MWh
        t.rail_ppl.demand_biodiesel = entry("In_T_ec_rail_ppl_diesel") * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        # 97.700.000.000 Pers km
        t.rail_ppl.transport_capacity_pkm = (
            t.rail_ppl.demand_diesel + t.rail_ppl.demand_biodiesel
        ) / fact(
            "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        ) + t.rail_ppl.demand_electricity / fact(
            "Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018"
        )

        # 843.358 t/a
        t.rail_ppl.CO2e_cb = t.rail_ppl.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        )

        # 9.646.598 MWh
        t.rail_ppl.energy = (
            +t.rail_ppl.demand_diesel
            + t.rail_ppl.demand_biodiesel
            + t.rail_ppl.demand_electricity
        )

        # --------------

        # 17.700.000.000 Pers km
        t.rail_ppl_metro.transport_capacity_pkm = t.rail_ppl_metro.mileage * fact(
            "Fact_T_D_lf_Rl_Metro_2018"
        )

        #  1.235.600 MWh
        t.rail_ppl_metro.demand_electricity = t.rail_ppl_metro.mileage * fact(
            "Fact_T_S_Rl_Metro_SEC_fzkm_2018"
        )

        # 1.235.600 MWh
        t.rail_ppl_metro.energy = t.rail_ppl_metro.demand_electricity
        # --------------

        # 4.015.518 MWh
        t.rail_gds.demand_electricity = entry("In_T_ec_rail_gds_elec")

        # 995.430 MWh
        t.rail_gds.demand_diesel = entry("In_T_ec_rail_gds_diesel") * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )

        # 57.935 MWh
        t.rail_gds.demand_biodiesel = entry("In_T_ec_rail_gds_diesel") * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        # 133.700.000.000 t km
        t.rail_gds.transport_capacity_tkm = (
            t.rail_gds.demand_diesel + t.rail_gds.demand_biodiesel
        ) / fact(
            "Fact_T_S_Rl_Train_gds_diesel_SEC_2018"
        ) + t.rail_gds.demand_electricity / fact(
            "Fact_T_S_Rl_Train_gds_elec_SEC_2018"
        )

        # 265.279 t/a
        t.rail_gds.CO2e_cb = t.rail_gds.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        )

        # 5.068.883 MWh
        t.rail_gds.energy = (
            +t.rail_gds.demand_diesel
            + t.rail_gds.demand_biodiesel
            + t.rail_gds.demand_electricity
        )

        # -------------

        # res 2.949.722 MWh

        t.ship_dmstc.transport_capacity_tkm = (
            fact("Fact_T_D_Shp_dmstc_trnsprt_gds_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        # res: 46.900.000.000 t km

        t.ship_dmstc.demand_diesel = (
            entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
            * fact("Fact_T_S_Shp_diesel_fec_2018")
        )
        # res: 2.949.722 MWh
        t.ship_dmstc.energy = t.ship_dmstc.demand_diesel

        t.ship_dmstc.CO2e_cb = t.ship_dmstc.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        )
        # res: 786.093  t/a

        # ---------------------

        t.ship_inter.transport_capacity_tkm = (
            fact("Fact_T_D_Shp_sea_nat_mlg_2013")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        # res: 1.982.900.000.000 t km

        t.ship_inter.demand_fueloil = (
            entry("In_M_population_com_2018") / entry("In_M_population_nat")
        ) * fact("Fact_T_D_Shp_sea_nat_EC_2018")

        t.ship_inter.energy = t.ship_inter.demand_fueloil
        # res: 19.722.222 MWh

        t.ship_inter.CO2e_cb = t.ship_inter.demand_fueloil * fact(
            "Fact_T_S_fueloil_EmFa_tank_wheel_2018"
        )
        # res: 5.396.000  t/a

        # ------------------------

        if ags == "DG000000":
            t.other_cycl.transport_capacity_pkm = (
                365
                * entry("In_M_population_com_2018")
                * fact("Fact_T_D_modal_split_cycl_nat")
            )
        else:
            if entry("In_T_rt7") in [71, 72, 73, 74, 75, 76, 77]:

                t.other_foot.transport_capacity_pkm = (
                    entry("In_M_population_com_2018")
                    * 365
                    * fact("Fact_T_D_modal_split_foot_rt" + str(int(entry("In_T_rt7"))))
                )

                t.other_cycl.transport_capacity_pkm = (
                    entry("In_M_population_com_2018")
                    * 365
                    * fact("Fact_T_D_modal_split_cycl_rt" + str(int(entry("In_T_rt7"))))
                )

            else:
                print("You should not be here")

        # ------------------------------ Berechnung der Oberklassensummen
        for i in range(len([a for a in dir(TColVars) if not a.startswith("_")])):
            t.air._set(i, t.air_inter._get(i) + t.air_dmstc._get(i))
            t.ship._set(i, t.ship_dmstc._get(i) + t.ship_inter._get(i))

        # ----------------------------------------------------
        t.air.demand_petrol = t.air_dmstc.demand_petrol

        t.road_car_it_ot.demand_petrol = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        t.road_car_ab.demand_petrol = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        t.road_gds_ldt_it_ot.demand_petrol = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        t.road_gds_ldt_ab.demand_petrol = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        t.road_car.demand_petrol = (
            t.road_car_it_ot.demand_petrol + t.road_car_ab.demand_petrol
        )
        t.road_gds_ldt.demand_petrol = (
            t.road_gds_ldt_it_ot.demand_petrol + t.road_gds_ldt_ab.demand_petrol
        )
        t.road_ppl.demand_petrol = t.road_car.demand_petrol
        t.road_gds.demand_petrol = t.road_gds_ldt.demand_petrol

        t.road.demand_petrol = t.road_ppl.demand_petrol + t.road_gds.demand_petrol
        t.demand_petrol = t.air.demand_petrol + t.road.demand_petrol
        t.s_petrol.energy = t.demand_petrol
        t.s_jetfuel.energy = t.air_inter.demand_jetfuel + t.air_dmstc.demand_jetfuel
        t.s_diesel.energy = t.t.demand_diesel

        t.s_fueloil.energy = t.ship_inter.demand_fueloil

        t.s_gas.energy = t.t.demand_gas

        t.s_biogas.energy = t.t.demand_biogas

        t.s_bioethanol.energy = t.t.demand_bioethanol

        t.s_biodiesel.energy = t.t.demand_biodiesel

        t.s_elec.energy = t.t.demand_electricity

        t.road_car_it_ot.demand_diesel = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )
        t.road_car.mileage = t.road_car_it_ot.mileage + t.road_car_ab.mileage
        t.road_car_it_ot.transport_capacity_pkm = t.road_car_it_ot.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )
        t.road_gds_ldt_it_ot.transport_capacity_tkm = (
            t.road_gds_ldt_it_ot.mileage * fact("Fact_T_D_lf_gds_LDT_2018")
        )
        t.road_car_it_ot.demand_lpg = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        t.road_car_it_ot.demand_gas = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        t.g.CO2e_total = 0

        t.g_planning.CO2e_total = 0

        t.air.CO2e_total = t.air.CO2e_cb

        t.air_inter.CO2e_total = t.air_inter.CO2e_cb

        t.air_dmstc.CO2e_total = t.air_dmstc.CO2e_cb

        t.rail_ppl_metro.energy = t.rail_ppl_metro.demand_electricity

        t.rail_ppl.mileage = t.rail_ppl_.mileage + t.rail_ppl_metro.mileage

        t.rail.transport_capacity_pkm = t.rail_ppl.transport_capacity_pkm

        t.rail.transport_capacity_tkm = t.rail_gds.transport_capacity_tkm

        t.road_car_ab.demand_diesel = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )
        t.road_car_it_ot.demand_biogas = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        t.road_car_it_ot.demand_bioethanol = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        t.road_car_it_ot.demand_biodiesel = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )
        t.road_car_it_ot.demand_electricity = (
            t.road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_it_at_2018")
        )
        t.road_car_it_ot.CO2e_cb = (
            t.road_car_it_ot.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + t.road_car_it_ot.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + t.road_car_it_ot.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + t.road_car_it_ot.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_car_it_ot.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.road_car_ab.demand_lpg = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )
        t.rail.CO2e_cb = t.rail_ppl.CO2e_cb + t.rail_gds.CO2e_cb
        t.road_car_ab.demand_gas = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        t.road_action_charger.CO2e_total = 0

        t.road_gds_ldt_it_ot.demand_diesel = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )
        t.road_gds_ldt.mileage = (
            t.road_gds_ldt_it_ot.mileage + t.road_gds_ldt_ab.mileage
        )
        t.road_car_ab.transport_capacity_pkm = t.road_car_ab.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )
        t.road_gds_ldt_ab.demand_diesel = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )
        t.road_gds_ldt_it_ot.demand_lpg = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )
        t.road_gds_mhd_it_ot.demand_biogas = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        t.road_gds_ldt_it_ot.demand_bioethanol = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )
        t.road_gds_ldt_it_ot.demand_biodiesel = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )
        t.road_gds_ldt_it_ot.demand_electricity = (
            t.road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_it_at_2018")
        )
        t.road_gds_ldt_it_ot.CO2e_cb = (
            t.road_gds_ldt_it_ot.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_it_ot.demand_lpg
            * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_it_ot.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + t.road_gds_ldt_it_ot.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_gds_ldt_it_ot.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.road_car_ab.demand_biogas = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        t.road_ppl.mileage = t.road_car.mileage + t.road_bus.mileage
        t.road_car_ab.demand_bioethanol = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )
        t.road_car_ab.demand_biodiesel = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )
        t.road_car_ab.demand_electricity = (
            t.road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_ab_2018")
        )
        t.road_car_ab.CO2e_cb = (
            t.road_car_ab.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + t.road_car_ab.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + t.road_car_ab.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + t.road_car_ab.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_car_ab.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.road_car.demand_lpg = t.road_car_it_ot.demand_lpg + t.road_car_ab.demand_lpg
        t.road_car.transport_capacity_pkm = (
            t.road_car_it_ot.transport_capacity_pkm
            + t.road_car_ab.transport_capacity_pkm
        )
        t.road_car_it_ot.energy = (
            t.road_car_it_ot.demand_petrol
            + t.road_car_it_ot.demand_diesel
            + t.road_car_it_ot.demand_lpg
            + t.road_car_it_ot.demand_gas
            + t.road_car_it_ot.demand_biogas
            + t.road_car_it_ot.demand_bioethanol
            + t.road_car_it_ot.demand_biodiesel
            + t.road_car_it_ot.demand_electricity
        )
        t.road_ppl.demand_lpg = t.road_car.demand_lpg

        t.road_car.demand_gas = t.road_car_it_ot.demand_gas + t.road_car_ab.demand_gas
        t.road_car.CO2e_cb = t.road_car_it_ot.CO2e_cb + t.road_car_ab.CO2e_cb
        t.road_car.demand_bioethanol = (
            t.road_car_it_ot.demand_bioethanol + t.road_car_ab.demand_bioethanol
        )
        t.road_car.CO2e_total = t.road_car.CO2e_cb

        t.road_ppl.CO2e_cb = t.road_car.CO2e_cb + t.road_bus.CO2e_cb
        t.road_ppl.CO2e_total = t.road_ppl.CO2e_cb

        t.road_car_it_ot.CO2e_total = t.road_car_it_ot.CO2e_cb

        t.road_car_ab.energy = (
            t.road_car_ab.demand_petrol
            + t.road_car_ab.demand_diesel
            + t.road_car_ab.demand_lpg
            + t.road_car_ab.demand_gas
            + t.road_car_ab.demand_biogas
            + t.road_car_ab.demand_bioethanol
            + t.road_car_ab.demand_biodiesel
            + t.road_car_ab.demand_electricity
        )
        t.road_ppl.transport_capacity_pkm = (
            t.road_car.transport_capacity_pkm + t.road_bus.transport_capacity_pkm
        )
        t.road_car.demand_diesel = (
            t.road_car_it_ot.demand_diesel + t.road_car_ab.demand_diesel
        )
        t.road_car.energy = t.road_car_it_ot.energy + t.road_car_ab.energy
        t.road_ppl.demand_gas = t.road_car.demand_gas + t.road_bus.demand_gas
        t.road_car.demand_biogas = (
            t.road_car_it_ot.demand_biogas + t.road_car_ab.demand_biogas
        )
        t.road_ppl.demand_bioethanol = t.road_car.demand_bioethanol

        t.road_car.demand_biodiesel = (
            t.road_car_it_ot.demand_biodiesel + t.road_car_ab.demand_biodiesel
        )

        t.road_car.demand_electricity = (
            t.road_car_it_ot.demand_electricity + t.road_car_ab.demand_electricity
        )
        t.road_gds_ldt_ab.demand_lpg = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )
        t.road_car_ab.CO2e_total = t.road_car_ab.CO2e_cb

        t.road_ppl.energy = t.road_car.energy + t.road_bus.energy
        t.road.transport_capacity_pkm = t.road_ppl.transport_capacity_pkm
        t.road_ppl.demand_diesel = t.road_car.demand_diesel + t.road_bus.demand_diesel
        t.road_ppl.demand_biogas = t.road_car.demand_biogas + t.road_bus.demand_biogas
        t.road_ppl.demand_biodiesel = (
            t.road_car.demand_biodiesel + t.road_bus.demand_biodiesel
        )
        t.road_ppl.demand_electricity = (
            t.road_car.demand_electricity + t.road_bus.demand_electricity
        )

        t.road_gds_ldt_ab.demand_bioethanol = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )
        t.road_bus.CO2e_total = t.road_bus.CO2e_cb

        t.road_bus_action_infra.CO2e_total = 0

        t.road_gds_ldt_it_ot.energy = (
            t.road_gds_ldt_it_ot.demand_petrol
            + t.road_gds_ldt_it_ot.demand_diesel
            + t.road_gds_ldt_it_ot.demand_lpg
            + t.road_gds_ldt_it_ot.demand_bioethanol
            + t.road_gds_ldt_it_ot.demand_biodiesel
            + t.road_gds_ldt_it_ot.demand_electricity
        )
        t.road_gds_mhd_ab.mileage = entry("In_T_mil_mhd_ab") * Million

        t.road_gds_ldt_ab.transport_capacity_tkm = t.road_gds_ldt_ab.mileage * fact(
            "Fact_T_D_lf_gds_LDT_2018"
        )
        t.road_gds_ldt.demand_diesel = (
            t.road_gds_ldt_it_ot.demand_diesel + t.road_gds_ldt_ab.demand_diesel
        )
        t.road_gds_ldt_ab.demand_biodiesel = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )
        t.road_gds_mhd_it_ot.demand_gas = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        t.road_gds_mhd_ab.demand_biogas = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        t.road_gds_ldt_ab.demand_electricity = (
            t.road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_ab_2018")
        )
        t.road_gds_ldt_ab.CO2e_cb = (
            t.road_gds_ldt_ab.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_ab.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + t.road_gds_ldt_ab.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + t.road_gds_ldt_ab.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_gds_ldt_ab.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.road_gds_ldt.CO2e_cb = (
            t.road_gds_ldt_it_ot.CO2e_cb + t.road_gds_ldt_ab.CO2e_cb
        )
        t.other_foot.CO2e_cb = t.other_cycl.CO2e_cb = 0

        t.other.CO2e_cb = t.other_foot.CO2e_cb + t.other_cycl.CO2e_cb
        t.road_gds_mhd_it_ot.demand_diesel = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        t.road_gds_mhd_it_ot.demand_biodiesel = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        t.road_gds_mhd_ab.demand_gas = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        t.road_gds_mhd_it_ot.transport_capacity_tkm = (
            t.road_gds_mhd_it_ot.mileage * fact("Fact_T_D_lf_gds_MHD_2018")
        )
        t.road_gds_mhd_ab.demand_diesel = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        t.road_gds_ldt.demand_lpg = (
            t.road_gds_ldt_it_ot.demand_lpg + t.road_gds_ldt_ab.demand_lpg
        )
        t.road_gds_ldt.demand_bioethanol = (
            t.road_gds_ldt_it_ot.demand_bioethanol + t.road_gds_ldt_ab.demand_bioethanol
        )
        t.road_gds_mhd_it_ot.demand_electricity = (
            t.road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
        )
        t.road_gds_mhd_it_ot.CO2e_cb = (
            t.road_gds_mhd_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_gds_mhd_it_ot.demand_gas
            * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + t.road_gds_mhd_it_ot.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + t.road_gds_mhd_it_ot.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_gds_mhd_it_ot.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.road_gds_mhd_ab.demand_biodiesel = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        t.road_gds_ldt.CO2e_total = t.road_gds_ldt.CO2e_cb

        t.road_gds.demand_lpg = t.road_gds_ldt.demand_lpg

        t.road_gds_ldt.transport_capacity_tkm = (
            t.road_gds_ldt_it_ot.transport_capacity_tkm
            + t.road_gds_ldt_ab.transport_capacity_tkm
        )
        t.road_gds_ldt_ab.energy = (
            t.road_gds_ldt_ab.demand_petrol
            + t.road_gds_ldt_ab.demand_diesel
            + t.road_gds_ldt_ab.demand_lpg
            + t.road_gds_ldt_ab.demand_bioethanol
            + t.road_gds_ldt_ab.demand_biodiesel
            + t.road_gds_ldt_ab.demand_electricity
        )
        t.road.demand_lpg = t.road_ppl.demand_lpg + t.road_gds.demand_lpg
        t.road_gds.demand_bioethanol = t.road_gds_ldt.demand_bioethanol
        t.road_gds_ldt.demand_biodiesel = (
            t.road_gds_ldt_it_ot.demand_biodiesel + t.road_gds_ldt_ab.demand_biodiesel
        )
        t.road_gds_ldt.demand_electricity = (
            t.road_gds_ldt_it_ot.demand_electricity
            + t.road_gds_ldt_ab.demand_electricity
        )
        t.road_gds_mhd_ab.demand_electricity = (
            t.road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
        )
        t.road_gds_ldt_it_ot.CO2e_total = t.road_gds_ldt_it_ot.CO2e_cb

        t.road_gds_mhd_it_ot.energy = (
            t.road_gds_mhd_it_ot.demand_diesel
            + t.road_gds_mhd_it_ot.demand_gas
            + t.road_gds_mhd_it_ot.demand_biogas
            + t.road_gds_mhd_it_ot.demand_biodiesel
            + t.road_gds_mhd_it_ot.demand_electricity
        )
        t.road_gds_mhd_ab.transport_capacity_tkm = t.road_gds_mhd_ab.mileage * fact(
            "Fact_T_D_lf_gds_MHD_2018"
        )
        t.road_gds_mhd.demand_diesel = (
            t.road_gds_mhd_it_ot.demand_diesel + t.road_gds_mhd_ab.demand_diesel
        )
        t.road_gds_ldt.energy = t.road_gds_ldt_it_ot.energy + t.road_gds_ldt_ab.energy
        t.road.demand_bioethanol = (
            t.road_ppl.demand_bioethanol + t.road_gds.demand_bioethanol
        )
        t.road_gds_mhd_ab.CO2e_cb = (
            t.road_gds_mhd_ab.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + t.road_gds_mhd_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + t.road_gds_mhd_ab.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + t.road_gds_mhd_ab.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + t.road_gds_mhd_ab.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        t.road_gds_mhd.CO2e_cb = (
            t.road_gds_mhd_it_ot.CO2e_cb + t.road_gds_mhd_ab.CO2e_cb
        )
        t.road_gds.CO2e_cb = t.road_gds_ldt.CO2e_cb + t.road_gds_mhd.CO2e_cb
        t.road_gds_ldt_ab.CO2e_total = t.road_gds_ldt_ab.CO2e_cb
        t.road_gds_mhd_ab.energy = (
            t.road_gds_mhd_ab.demand_diesel
            + t.road_gds_mhd_ab.demand_gas
            + t.road_gds_mhd_ab.demand_biogas
            + t.road_gds_mhd_ab.demand_biodiesel
            + t.road_gds_mhd_ab.demand_electricity
        )
        t.road_gds_mhd.mileage = (
            t.road_gds_mhd_it_ot.mileage + t.road_gds_mhd_ab.mileage
        )
        t.road_gds_mhd.transport_capacity_tkm = (
            t.road_gds_mhd_it_ot.transport_capacity_tkm
            + t.road_gds_mhd_ab.transport_capacity_tkm
        )
        t.road_gds.demand_diesel = (
            t.road_gds_ldt.demand_diesel + t.road_gds_mhd.demand_diesel
        )
        t.road_gds_mhd.demand_gas = (
            t.road_gds_mhd_it_ot.demand_gas + t.road_gds_mhd_ab.demand_gas
        )
        t.road_gds_mhd.demand_biogas = (
            t.road_gds_mhd_it_ot.demand_biogas + t.road_gds_mhd_ab.demand_biogas
        )
        t.road_gds_mhd.demand_biodiesel = (
            t.road_gds_mhd_it_ot.demand_biodiesel + t.road_gds_mhd_ab.demand_biodiesel
        )
        t.road_gds_mhd.demand_electricity = (
            t.road_gds_mhd_it_ot.demand_electricity
            + t.road_gds_mhd_ab.demand_electricity
        )
        t.road.CO2e_cb = t.road_ppl.CO2e_cb + t.road_gds.CO2e_cb
        t.road_gds_mhd.CO2e_total = t.road_gds_mhd.CO2e_cb

        t.road_gds.demand_gas = t.road_gds_mhd.demand_gas

        t.road_gds.mileage = t.road_gds_ldt.mileage + t.road_gds_mhd.mileage
        t.road_gds.transport_capacity_tkm = (
            t.road_gds_ldt.transport_capacity_tkm
            + t.road_gds_mhd.transport_capacity_tkm
        )
        t.road_gds_mhd.energy = t.road_gds_mhd_it_ot.energy + t.road_gds_mhd_ab.energy
        t.road.demand_gas = t.road_ppl.demand_gas + t.road_gds.demand_gas
        t.road_gds.demand_biogas = t.road_gds_mhd.demand_biogas

        t.road_gds.demand_biodiesel = (
            t.road_gds_ldt.demand_biodiesel + t.road_gds_mhd.demand_biodiesel
        )
        t.road_gds.demand_electricity = (
            t.road_gds_ldt.demand_electricity + t.road_gds_mhd.demand_electricity
        )
        t.road_gds.CO2e_total = t.road_gds.CO2e_cb

        t.road_gds_mhd_it_ot.CO2e_total = t.road_gds_mhd_it_ot.CO2e_cb

        t.road_gds.energy = t.road_gds_ldt.energy + t.road_gds_mhd.energy
        t.road.mileage = t.road_ppl.mileage + t.road_gds.mileage
        t.road.transport_capacity_tkm = t.road_gds.transport_capacity_tkm

        t.road.demand_diesel = t.road_ppl.demand_diesel + t.road_gds.demand_diesel
        t.road.energy = t.road_ppl.energy + t.road_gds.energy
        t.road.demand_biogas = t.road_ppl.demand_biogas + t.road_gds.demand_biogas
        t.road.demand_biodiesel = (
            t.road_ppl.demand_biodiesel + t.road_gds.demand_biodiesel
        )
        t.road.demand_electricity = (
            t.road_ppl.demand_electricity + t.road_gds.demand_electricity
        )
        t.road.CO2e_total = t.road.CO2e_cb

        t.road_gds_mhd_ab.CO2e_total = t.road_gds_mhd_ab.CO2e_cb

        t.rail.energy = t.rail_ppl_.energy + t.rail_ppl_metro.energy + t.rail_gds.energy
        t.other.mileage = 0
        t.other_foot.transport_capacity_pkm = (
            365
            * entry("In_M_population_com_2018")
            * fact("Fact_T_D_modal_split_foot_nat")
            if (ags == "DG000000")
            else entry("In_M_population_com_2018") * 365
        )  # todo lookup list
        t.other.transport_capacity_tkm = 0

        t.rail.demand_diesel = t.rail_ppl.demand_diesel + t.rail_gds.demand_diesel
        t.rail.demand_biodiesel = (
            t.rail_ppl.demand_biodiesel + t.rail_gds.demand_biodiesel
        )
        t.rail.demand_electricity = (
            t.rail_ppl.demand_electricity + t.rail_gds.demand_electricity
        )
        t.t.CO2e_cb = (
            t.air.CO2e_cb
            + t.road.CO2e_cb
            + t.rail.CO2e_cb
            + t.ship.CO2e_cb
            + t.other.CO2e_cb
        )
        t.rail.CO2e_total = t.rail.CO2e_cb

        t.rail_action_invest_infra.CO2e_total = 0

        t.rail_action_invest_station.CO2e_total = 0

        t.rail_gds.mileage = t.rail_gds.transport_capacity_tkm / fact(
            "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
        )
        t.rail_ppl.CO2e_total = t.rail_ppl.CO2e_cb

        t.t.energy = t.air.energy + t.road.energy + t.rail.energy + t.ship.energy
        t.t.demand_electricity = t.road.demand_electricity + t.rail.demand_electricity

        t.rail_ppl_metro.transport_capacity_pkm = t.rail_ppl_metro.mileage * fact(
            "Fact_T_D_lf_Rl_Metro_2018"
        )
        t.rail_ppl_metro.CO2e_cb = t.rail_ppl_metro.demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        t.rail_ppl_metro.CO2e_total = t.rail_ppl_metro.CO2e_cb

        t.rail_ppl_metro_action_infra.CO2e_total = 0

        t.rail.mileage = t.rail_ppl.mileage + t.rail_gds.mileage
        t.rail_gds.CO2e_total = t.rail_gds.CO2e_cb

        t.ship.CO2e_total = t.ship.CO2e_cb

        t.ship_dmstc.CO2e_total = t.ship_dmstc.CO2e_cb

        t.ship_inter.CO2e_total = t.ship_inter.CO2e_cb
        t.t.mileage = t.road.mileage + t.rail.mileage + t.other.mileage

        t.t.transport_capacity_tkm = (
            t.air.transport_capacity_tkm
            + t.road.transport_capacity_tkm
            + t.rail.transport_capacity_tkm
            + t.ship.transport_capacity_tkm
            + t.other.transport_capacity_tkm
        )
        t.t.CO2e_total = t.t.CO2e_cb
        t.other.CO2e_total = t.other.CO2e_cb
        t.other.transport_capacity_pkm = (
            t.other_foot.transport_capacity_pkm + t.other_cycl.transport_capacity_pkm
        )
        t.other_foot.CO2e_total = t.other_foot.CO2e_cb

        t.t.transport_capacity_pkm = (
            t.air.transport_capacity_pkm
            + t.road.transport_capacity_pkm
            + t.rail.transport_capacity_pkm
            + t.other.transport_capacity_pkm
        )

        t.other_cycl.CO2e_total = t.other_cycl.CO2e_cb
        t.s_diesel.energy = t.t.demand_diesel
        t.s_gas.energy = t.t.demand_gas
        t.s_biogas.energy = t.t.demand_biogas

        t.t.demand_petrol = t.air.demand_petrol + t.road.demand_petrol
        t.t.demand_jetfuel = t.air.demand_jetfuel

        t.t.demand_diesel = (
            t.road.demand_diesel + t.rail.demand_diesel + t.ship.demand_diesel
        )
        t.ship.demand_fueloil = t.ship_inter.demand_fueloil

        t.t.demand_fueloil = t.ship.demand_fueloil

        t.t.demand_lpg = t.road.demand_lpg

        t.s_lpg.energy = t.t.demand_lpg

        t.t.demand_gas = t.road.demand_gas

        t.t.demand_biogas = t.road.demand_biogas

        t.t.demand_bioethanol = t.road.demand_bioethanol

        t.t.demand_biodiesel = t.road.demand_biodiesel + t.rail.demand_biodiesel

        t.t.demand_biogas = t.road.demand_biogas
        t.t.demand_bioethanol = t.road.demand_bioethanol
        t.t.demand_biodiesel = t.road.demand_biodiesel + t.rail.demand_biodiesel

        t.s_diesel.energy = t.t.demand_diesel
        t.s_gas.energy = t.t.demand_gas
        t.s_biogas.energy = t.t.demand_biogas
        t.s_bioethanol.energy = t.t.demand_bioethanol
        t.s_biodiesel.energy = t.t.demand_biodiesel
        t.s_elec.energy = t.t.demand_electricity

        t.s_biogas.energy = t.t.demand_biogas
        t.s_bioethanol.energy = t.t.demand_bioethanol
        t.s_biodiesel.energy = t.t.demand_biodiesel

        t.s.energy = (
            t.s_petrol.energy
            + t.s_jetfuel.energy
            + t.s_diesel.energy
            + t.s_fueloil.energy
            + t.s_lpg.energy
            + t.s_gas.energy
            + t.s_biogas.energy
            + t.s_bioethanol.energy
            + t.s_biodiesel.energy
            + t.s_elec.energy
        )

    except Exception as e:
        print("Transport: ")
        print(e)
        raise
