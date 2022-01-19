#!/usr/bin/env python
# coding: utf-8

from dataclasses import dataclass, field, InitVar, asdict
from Residences2018 import *
from setup import *

# Definition der relevanten Spaltennamen für den Sektor E
@dataclass
class BColVars:
    energy: float = None
    pct_x:float = None
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
    # Klassenvariablen für GHD
    b: BColVars = BColVars()
    g: BColVars = BColVars()
    g_consult: BColVars = BColVars()
    p: BColVars = BColVars()
    p_nonresi: BColVars = BColVars()
    p_nonresi_com: BColVars = BColVars()
    p_elec_elcon: BColVars = BColVars()
    p_elec_heatpump: BColVars = BColVars()
    p_vehicles: BColVars = BColVars()
    p_other: BColVars = BColVars()
    s: BColVars = BColVars()
    s_gas: BColVars = BColVars()
    s_emethan: BColVars = BColVars()
    s_lpg: BColVars = BColVars()
    s_petrol: BColVars = BColVars()
    s_jetfuel: BColVars = BColVars()
    s_diesel: BColVars = BColVars()
    s_fueloil: BColVars = BColVars()
    s_biomass: BColVars = BColVars()
    s_coal: BColVars = BColVars()
    s_heatnet: BColVars = BColVars()
    s_elec_heating: BColVars = BColVars()
    s_heatpump: BColVars = BColVars()
    s_solarth: BColVars = BColVars()
    s_elec: BColVars = BColVars()
    rb: BColVars = BColVars()
    rp_p: BColVars = BColVars()

    # erzeuge dictionry
    def dict(self):
        return asdict(self)



# Berechnungsfunktion im Sektor GHD für 2018

def Business2018_calc(root):

    try:
        Million = 1000000.
        Kalkulationszeitraum = entry('In_M_duration_target')

        b = root.b18
        r = root.r18

        b.s_gas.energy = (
            entry('In_B_gas_fec')
        )  # 98.602.500 MWh

        b.s_lpg.energy = (
            entry('In_B_lpg_fec')
        )  # 3.007.222 MWh

        b.s_petrol.energy = (
            entry('In_B_petrol_fec')
        )  # 1.667.778 MWh

        b.s_jetfuel.energy = (
            entry('In_B_jetfuel_fec')
        )  # 284.722 MWh

        b.s_diesel.energy = (
            entry('In_B_diesel_fec')
        )  # 9.033.056 MWh

        b.s_fueloil.energy = (
            entry('In_B_fueloil_fec')
        )  # 33.370.278 MWh

        b.s_biomass.energy = (
            entry('In_B_biomass_fec')
        )  # 20.860.278 MWh

        b.s_coal.energy = (
            entry('In_B_coal_fec')
        )  # 232.778 MWh

        b.s_heatnet.energy = (
            entry('In_B_heatnet_fec')
        )  # 6.521.944 MWh

        b.s_elec_heating.energy = (
                fact('Fact_B_S_elec_heating_fec_2018') *
                entry('In_R_flats_wo_heatnet') /
                fact('Fact_R_P_flats_wo_heatnet_2011')
        )  # 13.027.778 MWh

        b.s_heatpump.energy = (
                entry('In_B_orenew_fec') *
                fact('Fact_R_S_ratio_heatpump_to_orenew_2018')
        )  # 1.262.040 MWh

        b.s_solarth.energy = (
                entry('In_B_orenew_fec') *
                (1 - fact('Fact_R_S_ratio_heatpump_to_orenew_2018'))
        )  # 1.262.040 MWh

        b.s_elec.energy = entry('In_B_elec_fec')
        # 856.293 MWh

        b.s.energy = (
                b.s_gas.energy +
                b.s_lpg.energy +
                b.s_petrol.energy +
                b.s_jetfuel.energy +
                b.s_diesel.energy +
                b.s_fueloil.energy +
                b.s_biomass.energy +
                b.s_coal.energy +
                b.s_heatnet.energy +
                b.s_heatpump.energy +
                b.s_solarth.energy +
                b.s_elec.energy
        )  # 187.870.374 MWh

        b.s_gas.pct_energy = (
                b.s_gas.energy / b.s.energy
        )  # 52,5%

        b.s_lpg.pct_energy = (
                b.s_lpg.energy / b.s.energy
        )  # 1,6%

        b.s_petrol.pct_energy = (
                b.s_petrol.energy / b.s.energy
        )  # 0,9%

        b.s_jetfuel.pct_energy = (
                b.s_jetfuel.energy / b.s.energy
        )  # 0,2%

        b.s_diesel.pct_energy = (
                b.s_diesel.energy / b.s.energy
        )  # 4,8%

        b.s_fueloil.pct_energy = (
                b.s_fueloil.energy / b.s.energy
        )  # 17,8%

        b.s_biomass.pct_energy = (
                b.s_biomass.energy / b.s.energy
        )  # 11,1%

        b.s_coal.pct_energy = (
                b.s_coal.energy / b.s.energy
        )  # 0,1%

        b.s_heatnet.pct_energy = (
                b.s_heatnet.energy / b.s.energy
        )  # 3,5%

        b.s_elec_heating.pct_energy = (
                b.s_elec_heating.energy / b.s_elec.energy
        )  # 6,9%

        b.s_heatpump.pct_energy = (
                b.s_heatpump.energy / b.s.energy
        )  # 0,7%

        b.s_solarth.pct_energy = (
                b.s_solarth.energy / b.s.energy
        )  # 0,5%

        b.s_elec.pct_energy = (
            b.s_elec.energy / b.s.energy
        )

        b.s.pct_energy = (
                b.s_gas.pct_energy +
                b.s_lpg.pct_energy +
                b.s_petrol.pct_energy +
                b.s_jetfuel.pct_energy +
                b.s_diesel.pct_energy +
                b.s_fueloil.pct_energy +
                b.s_biomass.pct_energy +
                b.s_coal.pct_energy +
                b.s_heatnet.pct_energy +
                b.s_heatpump.pct_energy +
                b.s_solarth.pct_energy +
                b.s_elec.pct_energy
        )


        # NACHFRAGE:
        b.p_nonresi.area_m2 = (
                entry('In_R_area_m2') *
                fact('Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016') /
                (1 - fact('Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016')) *
                (1 - fact('Fact_A_P_energy_buildings_ratio_A_to_B'))
        )

        b.p_nonresi_com.pct_x = ass('Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050')
        b.p_nonresi_com.area_m2 = (
                b.p_nonresi.area_m2 * b.p_nonresi_com.pct_x
        )
        b.p_nonresi.energy = (
            b.s_gas.energy +
            b.s_lpg.energy +
            b.s_fueloil.energy +
            b.s_biomass.energy +
            b.s_coal.energy +
            b.s_heatnet.energy +
            b.s_heatpump.energy +
            b.s_solarth.energy +
            b.s_elec_heating.energy
        )
        # 187.870.374 MWh

        b.p_nonresi_com.energy = (
            b.p_nonresi.energy * b.p_nonresi_com.pct_x
        )
        # 38.712.683 MWh

        b.p_nonresi.number_of_buildings = (
            fact('Fact_B_P_number_business_buildings_2016') * entry('In_M_population_com_2018') /
            entry('In_M_population_nat')
        )

        b.p_nonresi_com.factor_adapted_to_fec = (
                b.p_nonresi_com.energy / b.p_nonresi_com.area_m2
        )

        #Elektrische Energie / Bisherige elektrische Verbraucher

        #Wärmepumpen
        b.p_elec_heatpump.energy = (
                b.s_heatpump.energy /
                fact('Fact_R_S_heatpump_mean_annual_performance_factor_all')
        )

        b.p_elec_elcon.energy = b.p_elec_elcon.energy = (
            b.s_elec.energy - b.p_elec_heatpump.energy - b.s_elec_heating.energy
        )
        b.p_vehicles.energy = (
                b.s_petrol.energy +
                b.s_jetfuel.energy +
                b.s_diesel.energy
        )
        b.p_other.energy = (
                b.p_elec_elcon.energy +
                b.p_elec_heatpump.energy +
                b.p_vehicles.energy
        ) # SUM(p_elec_elcon.energy:p_vehicles.energy)
        b.p.energy = (
                b.p_nonresi.energy + b.p_other.energy
        )
        b.p_nonresi.factor_adapted_to_fec = (
                b.p_nonresi.energy /
                b.p_nonresi.area_m2
        )

        b.p_elec_elcon.demand_change = ass('Ass_R_D_fec_elec_elcon_change')

        b.p_vehicles.demand_change = ass('Ass_B_D_fec_vehicles_change')

        b.p_vehicles.demand_ediesel = (
                b.p_vehicles.energy * (1 + b.p_vehicles.demand_change)
        )

        # Primärenergiekosten
        b.s_gas.cost_fuel_per_MWh = fact('Fact_R_S_gas_energy_cost_factor_2018')
        b.s_lpg.cost_fuel_per_MWh = fact('Fact_R_S_lpg_energy_cost_factor_2018')
        b.s_petrol.cost_fuel_per_MWh = fact('Fact_R_S_petrol_energy_cost_factor_2018')
        b.s_jetfuel.cost_fuel_per_MWh = fact('Fact_R_S_kerosine_energy_cost_factor_2018')
        b.s_diesel.cost_fuel_per_MWh = fact('Fact_R_S_fueloil_energy_cost_factor_2018')
        b.s_fueloil.cost_fuel_per_MWh = fact('Fact_R_S_fueloil_energy_cost_factor_2018')
        b.s_biomass.cost_fuel_per_MWh = fact('Fact_R_S_wood_energy_cost_factor_2018')
        b.s_coal.cost_fuel_per_MWh = fact('Fact_R_S_coal_energy_cost_factor_2018')
        b.s_heatnet.cost_fuel_per_MWh = fact('Fact_R_S_heatnet_energy_cost_factor_2018')
        b.s_heatpump.cost_fuel_per_MWh = (
                fact('Fact_E_D_R_cost_fuel_per_MWh_2018') / (
                fact('Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018') +
                fact('Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018')
                ) * 2
        )

        b.s_solarth.cost_fuel_per_MWh = 0

        b.s_gas.cost_fuel = (
                b.s_gas.energy * b.s_gas.cost_fuel_per_MWh / Million
        )

        b.s_lpg.cost_fuel = (
                b.s_lpg.energy * b.s_lpg.cost_fuel_per_MWh / Million
        )
        b.s_petrol.cost_fuel = (
                b.s_petrol.energy * b.s_petrol.cost_fuel_per_MWh / Million
        )
        b.s_jetfuel.cost_fuel = (
                b.s_jetfuel.energy * b.s_jetfuel.cost_fuel_per_MWh / Million
        )
        b.s_diesel.cost_fuel = (
                b.s_diesel.energy * b.s_diesel.cost_fuel_per_MWh / Million
        )
        b.s_fueloil.cost_fuel = (
                b.s_fueloil.energy * b.s_fueloil.cost_fuel_per_MWh / Million
        )
        b.s_biomass.cost_fuel = (
                b.s_biomass.energy * b.s_biomass.cost_fuel_per_MWh / Million
        )
        b.s_coal.cost_fuel = (
                b.s_coal.energy * b.s_coal.cost_fuel_per_MWh / Million
        )
        b.s_heatnet.cost_fuel = (
                b.s_heatnet.energy * b.s_heatnet.cost_fuel_per_MWh / Million
        )
        b.s_heatpump.cost_fuel = (
                b.s_heatpump.energy * b.s_heatpump.cost_fuel_per_MWh / Million
        )
        b.s_solarth.cost_fuel = 0

        b.s.cost_fuel = (
            b.s_gas.cost_fuel +
            b.s_lpg.cost_fuel +
            b.s_petrol.cost_fuel +
            b.s_jetfuel.cost_fuel +
            b.s_diesel.cost_fuel +
            b.s_fueloil.cost_fuel +
            b.s_biomass.cost_fuel +
            b.s_coal.cost_fuel +
            b.s_heatnet.cost_fuel +
            b.s_heatpump.cost_fuel +
            b.s_solarth.cost_fuel
        )

        #Energiebedingte THG-Emissionen
        b.s_gas.CO2e_cb_per_MWh = fact('Fact_H_P_ngas_cb_EF')
        b.s_lpg.CO2e_cb_per_MWh = fact('Fact_H_P_LPG_cb_EF')
        b.s_petrol.CO2e_cb_per_MWh = fact('Fact_H_P_petrol_cb_EF')
        b.s_jetfuel.CO2e_cb_per_MWh = fact('Fact_H_P_kerosene_cb_EF')
        b.s_diesel.CO2e_cb_per_MWh = fact('Fact_H_P_fueloil_cb_EF')
        b.s_fueloil.CO2e_cb_per_MWh = fact('Fact_H_P_fueloil_cb_EF')
        b.s_biomass.CO2e_cb_per_MWh = fact('Fact_RB_S_biomass_CO2e_EF')
        b.s_coal.CO2e_cb_per_MWh = fact('Fact_R_S_coal_CO2e_EF')

        b.s_gas.CO2e_cb = b.s_gas.energy * b.s_gas.CO2e_cb_per_MWh
        b.s_lpg.CO2e_cb = b.s_lpg.energy * b.s_lpg.CO2e_cb_per_MWh
        b.s_petrol.CO2e_cb = b.s_petrol.energy * b.s_petrol.CO2e_cb_per_MWh
        b.s_jetfuel.CO2e_cb = b.s_jetfuel.energy * b.s_jetfuel.CO2e_cb_per_MWh
        b.s_diesel.CO2e_cb = b.s_diesel.energy * b.s_diesel.CO2e_cb_per_MWh
        b.s_fueloil.CO2e_cb = b.s_fueloil.energy * b.s_fueloil.CO2e_cb_per_MWh
        b.s_biomass.CO2e_cb = b.s_biomass.energy * b.s_biomass.CO2e_cb_per_MWh
        b.s_coal.CO2e_cb = b.s_coal.energy * b.s_coal.CO2e_cb_per_MWh

        b.s.CO2e_cb = (
                b.s_gas.CO2e_cb +
                b.s_lpg.CO2e_cb +
                b.s_petrol.CO2e_cb +
                b.s_jetfuel.CO2e_cb +
                b.s_diesel.CO2e_cb +
                b.s_fueloil.CO2e_cb +
                b.s_biomass.CO2e_cb +
                b.s_coal.CO2e_cb
        )
        b.s.CO2e_total = b.s.CO2e_cb

        b.p_elec_elcon.demand_electricity = (
            b.p_elec_elcon.energy * (entry('In_M_population_com_203X') / entry('In_M_population_com_2018')) *
            (1 + b.p_elec_elcon.demand_change)
        )

        b.CO2e_cb = b.s.CO2e_cb
        b.CO2e_total = b.s.CO2e_total
        b.s_gas.CO2e_total = b.s_gas.CO2e_cb
        b.s_lpg.CO2e_total = b.s_lpg.CO2e_cb
        b.s_petrol.CO2e_total = b.s_petrol.CO2e_cb
        b.s_jetfuel.CO2e_total = b.s_jetfuel.CO2e_cb
        b.s_diesel.CO2e_total = b.s_diesel.CO2e_cb
        b.s_fueloil.CO2e_total = b.s_fueloil.CO2e_cb
        b.s_biomass.CO2e_total = b.s_biomass.CO2e_cb
        b.s_coal.CO2e_total = b.s_coal.CO2e_cb
        b.s_biomass.number_of_buildings = (
                b.s_biomass.energy * b.p_nonresi.number_of_buildings /
                (b.p_nonresi.factor_adapted_to_fec * b.p_nonresi.area_m2)
        )
        b.rp_p.CO2e_cb = (
                r.s.CO2e_cb - r.s_petrol.CO2e_cb +
                b.s.CO2e_cb - b.s_petrol.CO2e_cb - b.s_jetfuel.CO2e_cb - b.s_diesel.CO2e_cb
        )
        b.rp_p.CO2e_total = (
                r.s.CO2e_cb + b.s.CO2e_cb
        )
        b.rb.energy = (
                r.p.energy + b.p.energy
        )
        b.b.CO2e_cb = b.s.CO2e_cb
        b.rb.CO2e_cb = (
            r.r.CO2e_cb + b.b.CO2e_cb
        )
        b.rb.CO2e_total = b.rb.CO2e_cb
        b.b.CO2e_total = b.s.CO2e_total

        b.b.CO2e_pb = 0
        b.s_heatnet.CO2e_cb = 0
        b.s_heatnet.CO2e_cb_per_MWh = 0
        b.s_heatnet.CO2e_total = 0
        b.s_heatpump.CO2e_cb = 0
        b.s_heatpump.CO2e_cb_per_MWh = 0
        b.s_heatpump.CO2e_total  = 0
        b.s_solarth.CO2e_cb  = 0
        b.s_solarth.CO2e_cb_per_MWh = 0
        b.s_solarth.CO2e_total = 0
        b.s_elec.CO2e_cb = 0
        b.s_elec.CO2e_cb_per_MWh = 0
        b.s_elec.CO2e_total = 0
        b.s_elec_heating.CO2e_cb = 0
        b.s_elec_heating.CO2e_cb_per_MWh = 0
        b.s_elec_heating.CO2e_total = 0

    except Exception:
        raise





