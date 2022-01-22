# # Laden der Datentabellen und deren Suchfunktionen

from dataclasses import dataclass, field, InitVar, asdict
from .inputs import Inputs

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
    rail_ppl_metro: TColVars = TColVars()
    rail_ppl_metro_action_infra: TColVars = TColVars()
    rail_ppl_distance: TColVars = TColVars()
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


def calc(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    # Todo remove after impl.

    if entry("In_M_AGS_com") == "DG000000":
        root.t18.rail_ppl_metro.mileage = 309000000
        root.t18.road_bus.mileage = 2531000000
    elif entry("In_M_AGS_com") == "03159016":
        root.t18.rail_ppl_metro.mileage = 0
        root.t18.road_bus.mileage = 1752789.9193474643

    # abbreviations
    t = root.t18.t
    g = root.t18.g
    g_planning = root.t18.g_planning
    air_inter = root.t18.air_inter
    air_dmstc = root.t18.air_dmstc
    road = root.t18.road
    road_action_charger = root.t18.road_action_charger
    road_car = root.t18.road_car
    road_car_it_ot = root.t18.road_car_it_ot
    road_car_ab = root.t18.road_car_ab
    road_bus = root.t18.road_bus
    road_bus_action_infra = root.t18.road_bus_action_infra
    road_gds = root.t18.road_gds
    road_gds_ldt = root.t18.road_gds_ldt
    road_gds_ldt_it_ot = root.t18.road_gds_ldt_it_ot
    road_gds_ldt_ab = root.t18.road_gds_ldt_ab
    road_gds_mhd = root.t18.road_gds_mhd
    road_ppl = root.t18.road_ppl
    road_gds_mhd_it_ot = root.t18.road_gds_mhd_it_ot
    road_gds_mhd_ab = root.t18.road_gds_mhd_ab
    rail_ppl = root.t18.rail_ppl
    # rail_ppl_ = root.t18.rail_ppl_
    rail_ppl_distance = root.t18.rail_ppl_distance
    rail_ppl_metro = root.t18.rail_ppl_metro
    rail_ppl_metro_action_infra = root.t18.rail_ppl_metro_action_infra
    rail_gds = root.t18.rail_gds
    rail_action_invest_infra = root.t18.rail_action_invest_infra
    rail_action_invest_station = root.t18.rail_action_invest_station
    ship_dmstc = root.t18.ship_dmstc
    ship_inter = root.t18.ship_inter
    other_foot = root.t18.other_foot
    other_cycl = root.t18.other_cycl
    air = root.t18.air
    rail = root.t18.rail
    ship = root.t18.ship
    other = root.t18.other
    s = root.t18.s
    s_petrol = root.t18.s_petrol
    s_jetfuel = root.t18.s_jetfuel
    s_diesel = root.t18.s_diesel
    s_fueloil = root.t18.s_fueloil
    s_lpg = root.t18.s_lpg
    s_gas = root.t18.s_gas
    s_biogas = root.t18.s_biogas
    s_bioethanol = root.t18.s_bioethanol
    s_biodiesel = root.t18.s_biodiesel
    s_elec = root.t18.s_elec
    s_hydrogen = root.t18.s_hydrogen
    s_emethan = root.t18.s_emethan

    try:
        Million = 1000000
        ags = entry("In_M_AGS_com")
        # res 61.700.000.000 Pers km
        air_inter.transport_capacity_pkm = (
            fact("Fact_T_D_Air_nat_trnsprt_ppl_2019")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 1.507.745.000 t km
        air_inter.transport_capacity_tkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * fact("Fact_T_D_Air_inter_nat_ratio_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 113.722.222 MWh
        air_inter.demand_jetfuel = (
            fact("Fact_T_S_Air_nat_EB_inter_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 30.020.293  t/a
        air_inter.CO2e_cb = (
            air_inter.demand_jetfuel
            # Todo: In der Excel werden   Emissionen durch Benzinverbrauch im nationalen Flugverkehr addiert: Prüfen (Ergebnis weicht daher ab)
            * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
        )
        # res 113.722.222 MWh
        air_inter.energy = air_inter.demand_jetfuel

        # -------------------

        # res 10.100.000.000 Pers km
        air_dmstc.transport_capacity_pkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_ppl_2019")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 79.355.000 t km
        air_dmstc.transport_capacity_tkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * fact("Fact_T_D_Air_dmstc_nat_ratio_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 108.056 MWh
        air_dmstc.demand_petrol = (
            fact("Fact_T_S_Air_petrol_fec_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 7.805.556 MWh
        air_dmstc.demand_jetfuel = (
            fact("Fact_T_S_Air_nat_EB_dmstc_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        # res 2.085.724  t/a
        air_dmstc.CO2e_cb = air_dmstc.demand_jetfuel * fact(
            "Fact_T_S_jetfuel_EmFa_tank_wheel_2018"
        ) + air_dmstc.demand_petrol * fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")

        # res 7.913.611 MWh
        air_dmstc.energy = air_dmstc.demand_jetfuel + air_dmstc.demand_petrol

        air.energy = air_inter.energy + air_dmstc.energy

        # -----------------------
        # res 456.061.500.000 Fz km
        road_car_it_ot.mileage = entry("In_T_mil_car_it_at") * Million

        # res 657.704.211.506 Pers km
        road_car_it_ot.transport_capacity_pkm = road_car_it_ot.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )

        # res 140.583.679 MWh
        road_car_it_ot.demand_petrol = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 137.907.651 MWh
        road_car_it_ot.demand_diesel = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )

        # res 3.211.348 MWh
        road_car_it_ot.demand_lpg = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 550.841 MWh
        road_car_it_ot.demand_gas = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 129.210 MWh
        road_car_it_ot.demand_biogas = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res  6.316.717 MWh
        road_car_it_ot.demand_bioethanol = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 8.026.371 MWh
        road_car_it_ot.demand_biodiesel = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )

        # res 121.985 MWh
        road_car_it_ot.demand_electricity = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_it_at_2018")
        )

        # res 36.749.000.000 Fz km
        road_gds_ldt_it_ot.mileage = entry("In_T_mil_ldt_it_at") * Million

        road_gds_ldt_it_ot.demand_electricity = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_it_at_2018")
        )

        # 14.549.300.000 Fz km

        road_gds_ldt_ab.mileage = entry("In_T_mil_ldt_ab") * Million

        road_gds_ldt_ab.demand_electricity = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_ab_2018")
        )

        # 28.430.600.000 Fz km
        road_gds_mhd_it_ot.mileage = (
            entry("In_T_mil_mhd_it_at") * Million - road_bus.mileage
        )

        road_gds_mhd_it_ot.demand_electricity = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
        )

        # 35.937.900.000 Fz km
        road_gds_mhd_ab.mileage = entry("In_T_mil_mhd_ab") * Million

        road_gds_mhd_ab.demand_electricity = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
        )
        # 308.900.000 Fz km
        # rail_ppl_metro.mileage = (
        # todo rail_ppl_metro.mileage = (VLOOKUP(LK&" *  *  * ",Verkehr_DestatisDaten!B4:I507,7,FALSE) * 10^6 * entry('In_M_population_com_2018') / entry('In_M_population_dis'))
        # )
        rail_ppl_metro.demand_electricity = rail_ppl_metro.mileage * fact(
            "Fact_T_S_Rl_Metro_SEC_fzkm_2018"
        )

        # res  75.732.141 t/a

        road_car_it_ot.CO2e_cb = (
            road_car_it_ot.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        )

        # res 296.847.801 MWh
        road_car_it_ot.energy = (
            road_car_it_ot.demand_petrol
            + road_car_it_ot.demand_diesel
            + road_car_it_ot.demand_lpg
            + road_car_it_ot.demand_gas
            + road_car_it_ot.demand_biogas
            + road_car_it_ot.demand_bioethanol
            + road_car_it_ot.demand_biodiesel
            + road_car_it_ot.demand_electricity
        )

        # --------------------

        # res 200.879.200.000 Fz km
        road_car_ab.mileage = entry("In_T_mil_car_ab") * Million

        # res 289.695.788.494 Pers km
        road_car_ab.transport_capacity_pkm = road_car_ab.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )

        # res 71.637.731 MWh
        road_car_ab.demand_petrol = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        # res 68.266.402 MWh
        road_car_ab.demand_diesel = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )

        # res 1.636.418 MWh
        road_car_ab.demand_lpg = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        # res 242.626 MWh
        road_car_ab.demand_gas = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            # Todo Prüfen warum hier ...SEC_petrol_it_at verwendet wird und nicht ...SEC_petrol_ab
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res 56.912 MWh
        road_car_ab.demand_biogas = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            # Todo Prüfen warum hier ...SEC_petrol_it_at verwendet wird und nicht ...SEC_petrol_ab
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        # res  3.218.832 MWh
        road_car_ab.demand_bioethanol = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        # res 3.973.177 MWh
        road_car_ab.demand_biodiesel = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )

        # res 85.897 MWh
        road_car_ab.demand_electricity = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_ab_2018")
        )

        # 38.048.389 t/a
        road_car_ab.CO2e_cb = (
            road_car_ab.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_car_ab.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_car_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + road_car_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        )

        # res 149.117.995 MWh
        road_car_ab.energy = (
            road_car_ab.demand_petrol
            + road_car_ab.demand_diesel
            + road_car_ab.demand_lpg
            + road_car_ab.demand_gas
            + road_car_ab.demand_biogas
            + road_car_ab.demand_bioethanol
            + road_car_ab.demand_biodiesel
            + road_car_ab.demand_electricity
        )

        # ----------------

        # res 2.343.000.000 Fz km
        # todo road_bus.mileage = (VLOOKUP(LK&" *  *  * ",Verkehr_DestatisDaten!B4:I507,8,FALSE) * 10^6 * entry('In_M_population_com_2018') / entry('In_M_population_dis'))

        # res 35.594.900.435 Pers km
        road_bus.transport_capacity_pkm = road_bus.mileage * fact(
            "Fact_T_D_lf_ppl_Bus_2018"
        )

        # res 8.426.134 MWh
        road_bus.demand_diesel = (
            road_bus.mileage
            * fact("Fact_T_S_Bus_frac_diesel_with_hybrid_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 162.136 MWh
        road_bus.demand_gas = (
            road_bus.mileage
            * fact("Fact_T_S_Bus_frac_cng_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 38.032 MWh
        road_bus.demand_biogas = (
            road_bus.mileage
            * fact("Fact_T_S_Bus_frac_cng_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 485.406 MWh
        road_bus.demand_biodiesel = (
            road_bus.mileage
            * fact("Fact_T_S_Bus_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Bus_SEC_diesel_2018")
        )

        # res 13.854 MWh
        road_bus.demand_electricity = (
            road_bus.mileage
            * fact("Fact_T_S_Bus_frac_bev_stock_2018")
            * fact("Fact_T_S_Bus_SEC_elec_2018")
        )

        # 2.278.190 t/a

        road_bus.CO2e_cb = (
            road_bus.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_bus.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + road_bus.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + road_bus.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_bus.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )

        # res 9.125.561 MWh
        road_bus.energy = (
            road_bus.demand_diesel
            + road_bus.demand_gas
            + road_bus.demand_biogas
            + road_bus.demand_biodiesel
            + road_bus.demand_electricity
        )

        # ---------------------

        # 5.516.114.569 t km
        road_gds_ldt_it_ot.transport_capacity_tkm = road_gds_ldt_it_ot.mileage * fact(
            "Fact_T_D_lf_gds_LDT_2018"
        )

        # 863.649 MWh
        road_gds_ldt_it_ot.demand_petrol = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        # 30.129.512 MWh
        road_gds_ldt_it_ot.demand_diesel = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )

        # 127.848 MWh
        road_gds_ldt_it_ot.demand_lpg = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        # 38.806 MWh
        road_gds_ldt_it_ot.demand_bioethanol = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        # 1.753.569 MWh
        road_gds_ldt_it_ot.demand_biodiesel = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )

        # 29.887 MWh
        road_gds_ldt_it_ot.demand_electricity = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_it_at_2018")
        )

        # 8.294.035 t/a
        road_gds_ldt_it_ot.CO2e_cb = (
            road_gds_ldt_it_ot.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_gds_ldt_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_gds_ldt_it_ot.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        )

        # 32.943.271 MWh
        road_gds_ldt_it_ot.energy = (
            road_gds_ldt_it_ot.demand_petrol
            + road_gds_ldt_it_ot.demand_diesel
            + road_gds_ldt_it_ot.demand_lpg
            + road_gds_ldt_it_ot.demand_bioethanol
            + road_gds_ldt_it_ot.demand_biodiesel
            + road_gds_ldt_it_ot.demand_electricity
        )

        # -------------------------

        # 2.183.885.431 t km
        road_gds_ldt_ab.transport_capacity_tkm = road_gds_ldt_ab.mileage * fact(
            "Fact_T_D_lf_gds_LDT_2018"
        )

        # 443.472 MWh
        road_gds_ldt_ab.demand_petrol = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        # 16.610.550 MWh
        road_gds_ldt_ab.demand_diesel = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )

        # 65.648 MWh
        road_gds_ldt_ab.demand_lpg = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        # 19.926 MWh
        road_gds_ldt_ab.demand_bioethanol = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        # 966.752 MWh
        road_gds_ldt_ab.demand_biodiesel = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )

        # 20.475 MWh
        road_gds_ldt_ab.demand_electricity = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_ab_2018")
        )

        # 4.562.536 t/a

        road_gds_ldt_ab.CO2e_cb = (
            road_gds_ldt_ab.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_gds_ldt_ab.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_gds_ldt_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        )

        # 18.126.823 MWh
        road_gds_ldt_ab.energy = (
            road_gds_ldt_ab.demand_petrol
            + road_gds_ldt_ab.demand_diesel
            + road_gds_ldt_ab.demand_lpg
            + road_gds_ldt_ab.demand_bioethanol
            + road_gds_ldt_ab.demand_biodiesel
            + road_gds_ldt_ab.demand_electricity
        )

        # -----------------------

        # 212.745.261.612 t km
        road_gds_mhd_it_ot.transport_capacity_tkm = road_gds_mhd_it_ot.mileage * fact(
            "Fact_T_D_lf_gds_MHD_2018"
        )

        # 75.928.091 MWh
        road_gds_mhd_it_ot.demand_diesel = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 58.690 MWh
        road_gds_mhd_it_ot.demand_gas = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 13.767 MWh
        road_gds_mhd_it_ot.demand_biogas = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 4.419.095 MWh
        road_gds_mhd_it_ot.demand_biodiesel = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )

        # 13.271 MWh
        road_gds_mhd_it_ot.demand_electricity = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
        )

        # 20.246.442 t/a

        road_gds_mhd_it_ot.CO2e_cb = road_gds_mhd_it_ot.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        ) + road_gds_mhd_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")

        # 80.432.915 MWh
        road_gds_mhd_it_ot.energy = (
            road_gds_mhd_it_ot.demand_diesel
            + road_gds_mhd_it_ot.demand_gas
            + road_gds_mhd_it_ot.demand_biogas
            + road_gds_mhd_it_ot.demand_biodiesel
            + road_gds_mhd_it_ot.demand_electricity
        )

        # --------------

        # 268.922.145.057 t km
        road_gds_mhd_ab.transport_capacity_tkm = road_gds_mhd_ab.mileage * fact(
            "Fact_T_D_lf_gds_MHD_2018"
        )

        # 98.546.344 MWh
        road_gds_mhd_ab.demand_diesel = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 76.174 MWh
        road_gds_mhd_ab.demand_gas = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 17.868 MWh
        road_gds_mhd_ab.demand_biogas = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 5.735.502 MWh
        road_gds_mhd_ab.demand_biodiesel = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )

        # 23.251 MWh
        road_gds_mhd_ab.demand_electricity = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
        )

        # 26.277.664 t/a
        road_gds_mhd_ab.CO2e_cb = road_gds_mhd_ab.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        ) + road_gds_mhd_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")

        # 104.399.138 MWh
        road_gds_mhd_ab.energy = (
            road_gds_mhd_ab.demand_diesel
            + road_gds_mhd_ab.demand_gas
            + road_gds_mhd_ab.demand_biogas
            + road_gds_mhd_ab.demand_biodiesel
            + road_gds_mhd_ab.demand_electricity
        )

        # -----------------

        # rail_ppl_.demand_diesel = entry("In_T_ec_rail_ppl_diesel") * (
        #    1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        # )
        # rail_ppl_.demand_biodiesel = entry("In_T_ec_rail_ppl_diesel") * fact(
        #    "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        # )
        # rail_ppl_.demand_electricity = entry("In_T_ec_rail_ppl_elec")
        # rail_ppl_.demand_petrol = 0
        # rail_ppl_.demand_jetfuel = 0
        # rail_ppl_.demand_lpg = 0
        # rail_ppl_.demand_gas = 0
        # rail_ppl_.demand_biogas = 0
        # rail_ppl_.demand_bioethanol = 0
        # rail_ppl_.CO2e_cb = (
        #    rail_ppl_.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
        #    + rail_ppl_.demand_jetfuel * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
        #    + rail_ppl_.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
        #    + rail_ppl_.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        #    + rail_ppl_.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        #    + rail_ppl_.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
        #    + rail_ppl_.demand_bioethanol * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
        #    + rail_ppl_.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
        #    + rail_ppl_.demand_electricity
        #    * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        # )
        # rail_ppl_.CO2e_total = rail_ppl_.CO2e_cb
        #
        # rail_ppl_.energy = (
        #    rail_ppl_.demand_diesel
        #    + rail_ppl_.demand_biodiesel
        #    + rail_ppl_.demand_electricity
        # )
        #
        # rail_ppl_.transport_capacity_pkm = (
        #    rail_ppl_.demand_diesel + rail_ppl_.demand_biodiesel
        # ) / fact(
        #    "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        # ) + rail_ppl_.demand_electricity / fact(
        #    "Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018"
        # )
        #
        # rail_ppl_.mileage = rail_ppl_.transport_capacity_pkm / fact(
        #    "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        # )
        # rail_ppl_.transport_capacity_pkm = (
        #    rail_ppl_.demand_diesel + rail_ppl_.demand_biodiesel
        # ) / fact(
        #    "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        # ) + rail_ppl_.demand_electricity / fact(
        #    "Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018"
        # )
        #
        rail_ppl_metro.demand_electricity = rail_ppl_metro.mileage * fact(
            "Fact_T_S_Rl_Metro_SEC_fzkm_2018"
        )
        #
        rail_ppl_distance.demand_electricity = entry("In_T_ec_rail_ppl_elec")
        rail_ppl.demand_electricity = (
            rail_ppl_distance.demand_electricity + rail_ppl_metro.demand_electricity
        )

        # 3.164.605 MWh
        rail_ppl.demand_diesel = entry("In_T_ec_rail_ppl_diesel") * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )

        # 184.183 MWh
        rail_ppl.demand_biodiesel = entry("In_T_ec_rail_ppl_diesel") * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )
        rail_ppl_distance.demand_diesel = entry("In_T_ec_rail_ppl_diesel") * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )
        rail_ppl_distance.demand_biodiesel = entry("In_T_ec_rail_ppl_diesel") * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        rail_ppl_distance.transport_capacity_pkm = (
            rail_ppl_distance.demand_diesel + rail_ppl_distance.demand_biodiesel
        ) / fact(
            "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        ) + rail_ppl_distance.demand_electricity / fact(
            "Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018"
        )
        # 17.700.000.000 Pers km
        rail_ppl_metro.transport_capacity_pkm = rail_ppl_metro.mileage * fact(
            "Fact_T_D_lf_Rl_Metro_2018"
        )
        rail_ppl.transport_capacity_pkm = (
            rail_ppl_distance.transport_capacity_pkm
            + rail_ppl_metro.transport_capacity_pkm
        )
        # 97.700.000.000 Pers km
        rail.transport_capacity_pkm = rail_ppl.transport_capacity_pkm

        # 843.358 t/a
        rail_ppl.CO2e_cb = rail_ppl.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        )

        # 9.646.598 MWh
        rail_ppl.energy = (
            +rail_ppl.demand_diesel
            + rail_ppl.demand_biodiesel
            + rail_ppl.demand_electricity
        )

        # --------------

        #  1.235.600 MWh
        rail_ppl_metro.demand_electricity = rail_ppl_metro.mileage * fact(
            "Fact_T_S_Rl_Metro_SEC_fzkm_2018"
        )

        # 1.235.600 MWh
        rail_ppl_metro.energy = rail_ppl_metro.demand_electricity
        # --------------

        # 4.015.518 MWh
        rail_gds.demand_electricity = entry("In_T_ec_rail_gds_elec")

        # 995.430 MWh
        rail_gds.demand_diesel = entry("In_T_ec_rail_gds_diesel") * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )

        # 57.935 MWh
        rail_gds.demand_biodiesel = entry("In_T_ec_rail_gds_diesel") * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        # 133.700.000.000 t km
        rail_gds.transport_capacity_tkm = (
            rail_gds.demand_diesel + rail_gds.demand_biodiesel
        ) / fact(
            "Fact_T_S_Rl_Train_gds_diesel_SEC_2018"
        ) + rail_gds.demand_electricity / fact(
            "Fact_T_S_Rl_Train_gds_elec_SEC_2018"
        )

        # 265.279 t/a
        rail_gds.CO2e_cb = rail_gds.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        )

        # 5.068.883 MWh
        rail_gds.energy = (
            +rail_gds.demand_diesel
            + rail_gds.demand_biodiesel
            + rail_gds.demand_electricity
        )

        # -------------

        # res 2.949.722 MWh

        ship_dmstc.transport_capacity_tkm = (
            fact("Fact_T_D_Shp_dmstc_trnsprt_gds_2018")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        # res: 46.900.000.000 t km

        ship_dmstc.demand_diesel = (
            entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
            * fact("Fact_T_S_Shp_diesel_fec_2018")
        )
        # res: 2.949.722 MWh
        ship_dmstc.energy = ship_dmstc.demand_diesel

        ship_dmstc.CO2e_cb = ship_dmstc.demand_diesel * fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        )
        # res: 786.093  t/a

        # ---------------------

        ship_inter.transport_capacity_tkm = (
            fact("Fact_T_D_Shp_sea_nat_mlg_2013")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        # res: 1.982.900.000.000 t km

        ship_inter.demand_fueloil = (
            entry("In_M_population_com_2018") / entry("In_M_population_nat")
        ) * fact("Fact_T_D_Shp_sea_nat_EC_2018")

        ship_inter.energy = ship_inter.demand_fueloil
        # res: 19.722.222 MWh

        ship_inter.CO2e_cb = ship_inter.demand_fueloil * fact(
            "Fact_T_S_fueloil_EmFa_tank_wheel_2018"
        )
        # res: 5.396.000  t/a

        # ------------------------

        if ags == "DG000000":
            other_cycl.transport_capacity_pkm = (
                365
                * entry("In_M_population_com_2018")
                * fact("Fact_T_D_modal_split_cycl_nat")
            )
        else:
            if entry("In_T_rt7") in [71, 72, 73, 74, 75, 76, 77]:

                other_foot.transport_capacity_pkm = (
                    entry("In_M_population_com_2018")
                    * 365
                    * fact("Fact_T_D_modal_split_foot_rt" + str(int(entry("In_T_rt7"))))
                )

                other_cycl.transport_capacity_pkm = (
                    entry("In_M_population_com_2018")
                    * 365
                    * fact("Fact_T_D_modal_split_cycl_rt" + str(int(entry("In_T_rt7"))))
                )

            else:
                print("You should not be here")

        # ------------------------------ Berechnung der Oberklassensummen
        for i in range(len([a for a in dir(TColVars) if not a.startswith("_")])):
            air._set(i, air_inter._get(i) + air_dmstc._get(i))
            ship._set(i, ship_dmstc._get(i) + ship_inter._get(i))

        # ----------------------------------------------------
        air.demand_petrol = air_dmstc.demand_petrol

        road_car_it_ot.demand_petrol = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )

        road_car_ab.demand_petrol = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )

        road_gds_ldt_it_ot.demand_petrol = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )

        road_gds_ldt_ab.demand_petrol = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )

        road_car.demand_petrol = (
            road_car_it_ot.demand_petrol + road_car_ab.demand_petrol
        )
        road_gds_ldt.demand_petrol = (
            road_gds_ldt_it_ot.demand_petrol + road_gds_ldt_ab.demand_petrol
        )
        road_ppl.demand_petrol = road_car.demand_petrol
        road_gds.demand_petrol = road_gds_ldt.demand_petrol

        road.demand_petrol = road_ppl.demand_petrol + road_gds.demand_petrol
        demand_petrol = air.demand_petrol + road.demand_petrol
        s_petrol.energy = demand_petrol
        s_jetfuel.energy = air_inter.demand_jetfuel + air_dmstc.demand_jetfuel
        s_diesel.energy = t.demand_diesel

        s_fueloil.energy = ship_inter.demand_fueloil

        s_gas.energy = t.demand_gas

        s_biogas.energy = t.demand_biogas

        s_bioethanol.energy = t.demand_bioethanol

        s_biodiesel.energy = t.demand_biodiesel

        s_elec.energy = t.demand_electricity

        road_car_it_ot.demand_diesel = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )
        road_car.mileage = road_car_it_ot.mileage + road_car_ab.mileage
        road_car_it_ot.transport_capacity_pkm = road_car_it_ot.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )
        road_gds_ldt_it_ot.transport_capacity_tkm = road_gds_ldt_it_ot.mileage * fact(
            "Fact_T_D_lf_gds_LDT_2018"
        )
        road_car_it_ot.demand_lpg = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        road_car_it_ot.demand_gas = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        g.CO2e_total = 0

        g_planning.CO2e_total = 0

        air.CO2e_total = air.CO2e_cb

        air_inter.CO2e_total = air_inter.CO2e_cb

        air_dmstc.CO2e_total = air_dmstc.CO2e_cb

        rail_ppl_metro.energy = rail_ppl_metro.demand_electricity
        rail_ppl_distance.mileage = rail_ppl_distance.transport_capacity_pkm / fact(
            "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        )
        rail_ppl.mileage = rail_ppl_distance.mileage + rail_ppl_metro.mileage

        rail.transport_capacity_pkm = rail_ppl.transport_capacity_pkm

        rail.transport_capacity_tkm = rail_gds.transport_capacity_tkm

        road_car_ab.demand_diesel = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )
        road_car_it_ot.demand_biogas = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        road_car_it_ot.demand_bioethanol = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        road_car_it_ot.demand_biodiesel = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_it_at_2018")
        )
        road_car_it_ot.demand_electricity = (
            road_car_it_ot.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_it_at_2018")
        )
        road_car_it_ot.CO2e_cb = (
            road_car_it_ot.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + road_car_it_ot.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + road_car_it_ot.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + road_car_it_ot.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_car_it_ot.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        road_car_ab.demand_lpg = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_lpg_mlg_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )
        rail.CO2e_cb = rail_ppl.CO2e_cb + rail_gds.CO2e_cb
        road_car_ab.demand_gas = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        road_action_charger.CO2e_total = 0

        road_gds_ldt_it_ot.demand_diesel = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )
        road_gds_ldt.mileage = road_gds_ldt_it_ot.mileage + road_gds_ldt_ab.mileage
        road_car_ab.transport_capacity_pkm = road_car_ab.mileage * fact(
            "Fact_T_D_lf_ppl_Car_2018"
        )
        road_gds_ldt_ab.demand_diesel = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )
        road_gds_ldt_it_ot.demand_lpg = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )
        road_gds_mhd_it_ot.demand_biogas = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        road_gds_ldt_it_ot.demand_bioethanol = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_it_at_2018")
        )
        road_gds_ldt_it_ot.demand_biodiesel = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_it_at_2018")
        )
        road_gds_ldt_it_ot.demand_electricity = (
            road_gds_ldt_it_ot.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_it_at_2018")
        )
        road_gds_ldt_it_ot.CO2e_cb = (
            road_gds_ldt_it_ot.demand_petrol
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_gds_ldt_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_gds_ldt_it_ot.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + road_gds_ldt_it_ot.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + road_gds_ldt_it_ot.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_gds_ldt_it_ot.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        road_car_ab.demand_biogas = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_cng_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_it_at_2018")
        )
        road_ppl.mileage = road_car.mileage + road_bus.mileage
        road_car_ab.demand_bioethanol = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_petrol_ab_2018")
        )
        road_car_ab.demand_biodiesel = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_Car_SEC_diesel_ab_2018")
        )
        road_car_ab.demand_electricity = (
            road_car_ab.mileage
            * fact("Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
            * fact("Fact_T_S_Car_SEC_elec_ab_2018")
        )
        road_car_ab.CO2e_cb = (
            road_car_ab.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_car_ab.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_car_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + road_car_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + road_car_ab.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + road_car_ab.demand_bioethanol * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + road_car_ab.demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_car_ab.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        road_car.demand_lpg = road_car_it_ot.demand_lpg + road_car_ab.demand_lpg
        road_car.transport_capacity_pkm = (
            road_car_it_ot.transport_capacity_pkm + road_car_ab.transport_capacity_pkm
        )
        road_car_it_ot.energy = (
            road_car_it_ot.demand_petrol
            + road_car_it_ot.demand_diesel
            + road_car_it_ot.demand_lpg
            + road_car_it_ot.demand_gas
            + road_car_it_ot.demand_biogas
            + road_car_it_ot.demand_bioethanol
            + road_car_it_ot.demand_biodiesel
            + road_car_it_ot.demand_electricity
        )
        road_ppl.demand_lpg = road_car.demand_lpg

        road_car.demand_gas = road_car_it_ot.demand_gas + road_car_ab.demand_gas
        road_car.CO2e_cb = road_car_it_ot.CO2e_cb + road_car_ab.CO2e_cb
        road_car.demand_bioethanol = (
            road_car_it_ot.demand_bioethanol + road_car_ab.demand_bioethanol
        )
        road_car.CO2e_total = road_car.CO2e_cb

        road_ppl.CO2e_cb = road_car.CO2e_cb + road_bus.CO2e_cb
        road_ppl.CO2e_total = road_ppl.CO2e_cb

        road_car_it_ot.CO2e_total = road_car_it_ot.CO2e_cb

        road_car_ab.energy = (
            road_car_ab.demand_petrol
            + road_car_ab.demand_diesel
            + road_car_ab.demand_lpg
            + road_car_ab.demand_gas
            + road_car_ab.demand_biogas
            + road_car_ab.demand_bioethanol
            + road_car_ab.demand_biodiesel
            + road_car_ab.demand_electricity
        )
        road_ppl.transport_capacity_pkm = (
            road_car.transport_capacity_pkm + road_bus.transport_capacity_pkm
        )
        road_car.demand_diesel = (
            road_car_it_ot.demand_diesel + road_car_ab.demand_diesel
        )
        road_car.energy = road_car_it_ot.energy + road_car_ab.energy
        road_ppl.demand_gas = road_car.demand_gas + road_bus.demand_gas
        road_car.demand_biogas = (
            road_car_it_ot.demand_biogas + road_car_ab.demand_biogas
        )
        road_ppl.demand_bioethanol = road_car.demand_bioethanol

        road_car.demand_biodiesel = (
            road_car_it_ot.demand_biodiesel + road_car_ab.demand_biodiesel
        )

        road_car.demand_electricity = (
            road_car_it_ot.demand_electricity + road_car_ab.demand_electricity
        )
        road_gds_ldt_ab.demand_lpg = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )
        road_car_ab.CO2e_total = road_car_ab.CO2e_cb

        road_ppl.energy = road_car.energy + road_bus.energy
        road.transport_capacity_pkm = road_ppl.transport_capacity_pkm
        road_ppl.demand_diesel = road_car.demand_diesel + road_bus.demand_diesel
        road_ppl.demand_biogas = road_car.demand_biogas + road_bus.demand_biogas
        road_ppl.demand_biodiesel = (
            road_car.demand_biodiesel + road_bus.demand_biodiesel
        )
        road_ppl.demand_electricity = (
            road_car.demand_electricity + road_bus.demand_electricity
        )

        road_gds_ldt_ab.demand_bioethanol = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_petrol_ab_2018")
        )
        road_bus.CO2e_total = road_bus.CO2e_cb

        road_bus_action_infra.CO2e_total = 0

        road_gds_ldt_it_ot.energy = (
            road_gds_ldt_it_ot.demand_petrol
            + road_gds_ldt_it_ot.demand_diesel
            + road_gds_ldt_it_ot.demand_lpg
            + road_gds_ldt_it_ot.demand_bioethanol
            + road_gds_ldt_it_ot.demand_biodiesel
            + road_gds_ldt_it_ot.demand_electricity
        )
        road_gds_mhd_ab.mileage = entry("In_T_mil_mhd_ab") * Million

        road_gds_ldt_ab.transport_capacity_tkm = road_gds_ldt_ab.mileage * fact(
            "Fact_T_D_lf_gds_LDT_2018"
        )
        road_gds_ldt.demand_diesel = (
            road_gds_ldt_it_ot.demand_diesel + road_gds_ldt_ab.demand_diesel
        )
        road_gds_ldt_ab.demand_biodiesel = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_LDT_SEC_diesel_ab_2018")
        )
        road_gds_mhd_it_ot.demand_gas = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        road_gds_mhd_ab.demand_biogas = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        road_gds_ldt_ab.demand_electricity = (
            road_gds_ldt_ab.mileage
            * fact("Fact_T_S_LDT_frac_bev_mlg_2018")
            * fact("Fact_T_S_LDT_SEC_elec_ab_2018")
        )
        road_gds_ldt_ab.CO2e_cb = (
            road_gds_ldt_ab.demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + road_gds_ldt_ab.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_gds_ldt_ab.demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + road_gds_ldt_ab.demand_bioethanol
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + road_gds_ldt_ab.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_gds_ldt_ab.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        road_gds_ldt.CO2e_cb = road_gds_ldt_it_ot.CO2e_cb + road_gds_ldt_ab.CO2e_cb
        other_foot.CO2e_cb = other_cycl.CO2e_cb = 0

        other.CO2e_cb = other_foot.CO2e_cb + other_cycl.CO2e_cb
        road_gds_mhd_it_ot.demand_diesel = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        road_gds_mhd_it_ot.demand_biodiesel = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
        )
        road_gds_mhd_ab.demand_gas = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        road_gds_mhd_it_ot.transport_capacity_tkm = road_gds_mhd_it_ot.mileage * fact(
            "Fact_T_D_lf_gds_MHD_2018"
        )
        road_gds_mhd_ab.demand_diesel = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        road_gds_ldt.demand_lpg = (
            road_gds_ldt_it_ot.demand_lpg + road_gds_ldt_ab.demand_lpg
        )
        road_gds_ldt.demand_bioethanol = (
            road_gds_ldt_it_ot.demand_bioethanol + road_gds_ldt_ab.demand_bioethanol
        )
        road_gds_mhd_it_ot.demand_electricity = (
            road_gds_mhd_it_ot.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
        )
        road_gds_mhd_it_ot.CO2e_cb = (
            road_gds_mhd_it_ot.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_gds_mhd_it_ot.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + road_gds_mhd_it_ot.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + road_gds_mhd_it_ot.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_gds_mhd_it_ot.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        road_gds_mhd_ab.demand_biodiesel = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_diesel_stock_2018")
            * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
            * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
        )
        road_gds_ldt.CO2e_total = road_gds_ldt.CO2e_cb

        road_gds.demand_lpg = road_gds_ldt.demand_lpg

        road_gds_ldt.transport_capacity_tkm = (
            road_gds_ldt_it_ot.transport_capacity_tkm
            + road_gds_ldt_ab.transport_capacity_tkm
        )
        road_gds_ldt_ab.energy = (
            road_gds_ldt_ab.demand_petrol
            + road_gds_ldt_ab.demand_diesel
            + road_gds_ldt_ab.demand_lpg
            + road_gds_ldt_ab.demand_bioethanol
            + road_gds_ldt_ab.demand_biodiesel
            + road_gds_ldt_ab.demand_electricity
        )
        road.demand_lpg = road_ppl.demand_lpg + road_gds.demand_lpg
        road_gds.demand_bioethanol = road_gds_ldt.demand_bioethanol
        road_gds_ldt.demand_biodiesel = (
            road_gds_ldt_it_ot.demand_biodiesel + road_gds_ldt_ab.demand_biodiesel
        )
        road_gds_ldt.demand_electricity = (
            road_gds_ldt_it_ot.demand_electricity + road_gds_ldt_ab.demand_electricity
        )
        road_gds_mhd_ab.demand_electricity = (
            road_gds_mhd_ab.mileage
            * fact("Fact_T_S_MHD_frac_bev_stock_2018")
            * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
        )
        road_gds_ldt_it_ot.CO2e_total = road_gds_ldt_it_ot.CO2e_cb

        road_gds_mhd_it_ot.energy = (
            road_gds_mhd_it_ot.demand_diesel
            + road_gds_mhd_it_ot.demand_gas
            + road_gds_mhd_it_ot.demand_biogas
            + road_gds_mhd_it_ot.demand_biodiesel
            + road_gds_mhd_it_ot.demand_electricity
        )
        road_gds_mhd_ab.transport_capacity_tkm = road_gds_mhd_ab.mileage * fact(
            "Fact_T_D_lf_gds_MHD_2018"
        )
        road_gds_mhd.demand_diesel = (
            road_gds_mhd_it_ot.demand_diesel + road_gds_mhd_ab.demand_diesel
        )
        road_gds_ldt.energy = road_gds_ldt_it_ot.energy + road_gds_ldt_ab.energy
        road.demand_bioethanol = road_ppl.demand_bioethanol + road_gds.demand_bioethanol
        road_gds_mhd_ab.CO2e_cb = (
            road_gds_mhd_ab.demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + road_gds_mhd_ab.demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + road_gds_mhd_ab.demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + road_gds_mhd_ab.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + road_gds_mhd_ab.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        road_gds_mhd.CO2e_cb = road_gds_mhd_it_ot.CO2e_cb + road_gds_mhd_ab.CO2e_cb
        road_gds.CO2e_cb = road_gds_ldt.CO2e_cb + road_gds_mhd.CO2e_cb
        road_gds_ldt_ab.CO2e_total = road_gds_ldt_ab.CO2e_cb
        road_gds_mhd_ab.energy = (
            road_gds_mhd_ab.demand_diesel
            + road_gds_mhd_ab.demand_gas
            + road_gds_mhd_ab.demand_biogas
            + road_gds_mhd_ab.demand_biodiesel
            + road_gds_mhd_ab.demand_electricity
        )
        road_gds_mhd.mileage = road_gds_mhd_it_ot.mileage + road_gds_mhd_ab.mileage
        road_gds_mhd.transport_capacity_tkm = (
            road_gds_mhd_it_ot.transport_capacity_tkm
            + road_gds_mhd_ab.transport_capacity_tkm
        )
        road_gds.demand_diesel = road_gds_ldt.demand_diesel + road_gds_mhd.demand_diesel
        road_gds_mhd.demand_gas = (
            road_gds_mhd_it_ot.demand_gas + road_gds_mhd_ab.demand_gas
        )
        road_gds_mhd.demand_biogas = (
            road_gds_mhd_it_ot.demand_biogas + road_gds_mhd_ab.demand_biogas
        )
        road_gds_mhd.demand_biodiesel = (
            road_gds_mhd_it_ot.demand_biodiesel + road_gds_mhd_ab.demand_biodiesel
        )
        road_gds_mhd.demand_electricity = (
            road_gds_mhd_it_ot.demand_electricity + road_gds_mhd_ab.demand_electricity
        )
        road.CO2e_cb = road_ppl.CO2e_cb + road_gds.CO2e_cb
        road_gds_mhd.CO2e_total = road_gds_mhd.CO2e_cb

        road_gds.demand_gas = road_gds_mhd.demand_gas

        road_gds.mileage = road_gds_ldt.mileage + road_gds_mhd.mileage
        road_gds.transport_capacity_tkm = (
            road_gds_ldt.transport_capacity_tkm + road_gds_mhd.transport_capacity_tkm
        )
        road_gds_mhd.energy = road_gds_mhd_it_ot.energy + road_gds_mhd_ab.energy
        road.demand_gas = road_ppl.demand_gas + road_gds.demand_gas
        road_gds.demand_biogas = road_gds_mhd.demand_biogas

        road_gds.demand_biodiesel = (
            road_gds_ldt.demand_biodiesel + road_gds_mhd.demand_biodiesel
        )
        road_gds.demand_electricity = (
            road_gds_ldt.demand_electricity + road_gds_mhd.demand_electricity
        )
        road_gds.CO2e_total = road_gds.CO2e_cb

        road_gds_mhd_it_ot.CO2e_total = road_gds_mhd_it_ot.CO2e_cb

        road_gds.energy = road_gds_ldt.energy + road_gds_mhd.energy
        road.mileage = road_ppl.mileage + road_gds.mileage
        road.transport_capacity_tkm = road_gds.transport_capacity_tkm

        road.demand_diesel = road_ppl.demand_diesel + road_gds.demand_diesel
        road.energy = road_ppl.energy + road_gds.energy
        road.demand_biogas = road_ppl.demand_biogas + road_gds.demand_biogas
        road.demand_biodiesel = road_ppl.demand_biodiesel + road_gds.demand_biodiesel
        road.demand_electricity = (
            road_ppl.demand_electricity + road_gds.demand_electricity
        )
        road.CO2e_total = road.CO2e_cb

        road_gds_mhd_ab.CO2e_total = road_gds_mhd_ab.CO2e_cb

        rail_ppl_distance.energy = (
            rail_ppl_distance.demand_diesel
            + rail_ppl_distance.demand_biodiesel
            + rail_ppl_distance.demand_electricity
        )
        rail.energy = rail_ppl_distance.energy + rail_ppl_metro.energy + rail_gds.energy
        other.mileage = 0
        other_foot.transport_capacity_pkm = (
            365
            * entry("In_M_population_com_2018")
            * fact("Fact_T_D_modal_split_foot_nat")
            if (ags == "DG000000")
            else entry("In_M_population_com_2018") * 365
        )  # todo lookup list
        other.transport_capacity_tkm = 0

        rail.demand_diesel = rail_ppl.demand_diesel + rail_gds.demand_diesel
        rail.demand_biodiesel = rail_ppl.demand_biodiesel + rail_gds.demand_biodiesel
        rail.demand_electricity = (
            rail_ppl.demand_electricity + rail_gds.demand_electricity
        )
        CO2e_cb = (
            air.CO2e_cb + road.CO2e_cb + rail.CO2e_cb + ship.CO2e_cb + other.CO2e_cb
        )
        rail.CO2e_total = rail.CO2e_cb

        rail_action_invest_infra.CO2e_total = 0

        rail_action_invest_station.CO2e_total = 0

        rail_gds.mileage = rail_gds.transport_capacity_tkm / fact(
            "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
        )
        rail_ppl.CO2e_total = rail_ppl.CO2e_cb

        energy = air.energy + road.energy + rail.energy + ship.energy
        demand_electricity = road.demand_electricity + rail.demand_electricity

        rail_ppl_metro.transport_capacity_pkm = rail_ppl_metro.mileage * fact(
            "Fact_T_D_lf_Rl_Metro_2018"
        )
        rail_ppl_metro.CO2e_cb = rail_ppl_metro.demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        rail_ppl_metro.CO2e_total = rail_ppl_metro.CO2e_cb

        rail_ppl_metro_action_infra.CO2e_total = 0

        rail.mileage = rail_ppl.mileage + rail_gds.mileage
        rail_gds.CO2e_total = rail_gds.CO2e_cb

        ship.CO2e_total = ship.CO2e_cb

        ship_dmstc.CO2e_total = ship_dmstc.CO2e_cb

        ship_inter.CO2e_total = ship_inter.CO2e_cb
        mileage = road.mileage + rail.mileage + other.mileage

        transport_capacity_tkm = (
            air.transport_capacity_tkm
            + road.transport_capacity_tkm
            + rail.transport_capacity_tkm
            + ship.transport_capacity_tkm
            + other.transport_capacity_tkm
        )
        CO2e_total = CO2e_cb
        other.CO2e_total = other.CO2e_cb
        other.transport_capacity_pkm = (
            other_foot.transport_capacity_pkm + other_cycl.transport_capacity_pkm
        )
        other_foot.CO2e_total = other_foot.CO2e_cb

        transport_capacity_pkm = (
            air.transport_capacity_pkm
            + road.transport_capacity_pkm
            + rail.transport_capacity_pkm
            + other.transport_capacity_pkm
        )

        other_cycl.CO2e_total = other_cycl.CO2e_cb
        s_diesel.energy = t.demand_diesel
        s_gas.energy = t.demand_gas
        s_biogas.energy = t.demand_biogas

        demand_petrol = air.demand_petrol + road.demand_petrol
        demand_jetfuel = air.demand_jetfuel

        demand_diesel = road.demand_diesel + rail.demand_diesel + ship.demand_diesel
        ship.demand_fueloil = ship_inter.demand_fueloil

        demand_fueloil = ship.demand_fueloil

        demand_lpg = road.demand_lpg

        s_lpg.energy = demand_lpg

        demand_gas = road.demand_gas

        demand_biogas = road.demand_biogas

        demand_bioethanol = road.demand_bioethanol

        demand_biodiesel = road.demand_biodiesel + rail.demand_biodiesel

        demand_biogas = road.demand_biogas
        demand_bioethanol = road.demand_bioethanol
        demand_biodiesel = road.demand_biodiesel + rail.demand_biodiesel

        s_diesel.energy = demand_diesel
        s_gas.energy = demand_gas
        s_biogas.energy = demand_biogas
        s_bioethanol.energy = demand_bioethanol
        s_biodiesel.energy = demand_biodiesel
        s_elec.energy = demand_electricity

        s_biogas.energy = demand_biogas
        s_bioethanol.energy = demand_bioethanol
        s_biodiesel.energy = demand_biodiesel

        s.energy = (
            s_petrol.energy
            + s_jetfuel.energy
            + s_diesel.energy
            + s_fueloil.energy
            + s_lpg.energy
            + s_gas.energy
            + s_biogas.energy
            + s_bioethanol.energy
            + s_biodiesel.energy
            + s_elec.energy
        )

        t.energy = air.energy + road.energy + rail.energy + ship.energy
        t.mileage = road.mileage + rail.mileage + other.mileage
        t.transport_capacity_pkm = (
            air.transport_capacity_pkm
            + road.transport_capacity_pkm
            + rail.transport_capacity_pkm
            + other.transport_capacity_pkm
        )
        t.transport_capacity_tkm = (
            air.transport_capacity_tkm
            + road.transport_capacity_tkm
            + rail.transport_capacity_tkm
            + ship.transport_capacity_tkm
            + other.transport_capacity_tkm
        )
        t.demand_petrol = air.demand_petrol + road.demand_petrol
        t.demand_jetfuel = air.demand_jetfuel
        t.demand_diesel = road.demand_diesel + rail.demand_diesel + ship.demand_diesel
        t.demand_fueloil = ship.demand_fueloil
        t.demand_lpg = road.demand_lpg
        t.demand_gas = road.demand_gas
        t.demand_biogas = road.demand_biogas
        t.demand_bioethanol = road.demand_bioethanol
        t.demand_biodiesel = road.demand_biodiesel + rail.demand_biodiesel
        t.demand_electricity = road.demand_electricity + rail.demand_electricity
        t.CO2e_cb = (
            air.CO2e_cb + road.CO2e_cb + rail.CO2e_cb + ship.CO2e_cb + other.CO2e_cb
        )
        t.CO2e_total = t.CO2e_cb
        rail_ppl_distance.CO2e_cb = (
            0 * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
            + 0 * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
            + rail_ppl_distance.demand_diesel
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
            + 0 * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
            + 0 * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
            + 0 * ass("Ass_T_S_biogas_EmFa_tank_wheel")
            + 0 * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
            + rail_ppl_distance.demand_biodiesel
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
            + rail_ppl_distance.demand_electricity
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        )
        rail_ppl_distance.CO2e_total = rail_ppl_distance.CO2e_cb

    except Exception as e:
        print("Transport: ")
        print(e)
        raise
