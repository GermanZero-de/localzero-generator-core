# pyright: strict

from typing import Any
import json
import sys
from dataclasses import dataclass

from climatevision.generator import calculate_with_default_inputs, make_entries, RefData, Result, Inputs
from climatevision.tracing import with_tracing
from climatevision.generator.generator import dataclass_to_result_dict

@dataclass(kw_only=True)
class References:
    # reference modules for calculation
    def __init__(self):
        self.pv_panel: float = 0.010 # 8-12 kWp = 0.08 MWp .. per standardized family home https://solar-ratgeber.ch/photovoltaik/rendite-ertrag/# 
        self.wind_power_plant: float = 3.2 # 3.2 MW reference wind power plant (Source: 2013_Umweltbundesamt_PotenzialWindenergieAnLand, P.15)
        self.large_heatpump: float = 20 # 20 MW standardized large heat pump
        self.heatpump: float = 0.012 # 12 kW standardized heat pump

    def change_refs(self):
        return 0

@dataclass(kw_only=True)
class Indicators: 
    
    refs = References() # sector electricity:  reference modules 
    pv_panels_peryear: float = 0 # sector electricity: pv panels to build per year 
    wind_power_plants_peryear: float = 0 # sector electricity:  wind power plants to build per year 
    heat_power_plants_area: float = 0 # sector heat: area with heat power plants to build per year 
    large_heatpumps: float = 0 # sector heat: large heat power plants to build
    heatpumps_peryear: float = 0 #  sector residences: heat pumps per year to build 
    renovated_houses_peryear: float = 0  # sector residences: houses to renovate per year
    electric_bus_peryear: float = 0 # sector transport: electrical bus to build per year
    electric_car_peryear: float = 0 # sector transport: electrical cars to build per year 

    def result_dict(self):
        return dataclass_to_result_dict(self)
    
    def calculate_indicators(self, inputs:Inputs, cr:Result):
        """
        This function allows to calculate several indicators to enhance the comprehensibility 
        of the by the generator calculated data. All calculation are assumptions based on diverse 
        literature (see ). The indicators represent the necessary changes/possiblities per year
        to mitigate C02 emissions. Each indicator is representing a sector. Current indicators are 
        photovoltaic (pv_pa) and wind power plants (wpp_pa) for electricity, heatpumps (hp_pa) and 
        renovated houses (ren_houses_pa) for heating, elec_veh_pa for transport.
        """
        # ass = inputs.ass
        # fact = inputs.fact

        # Amount per year = (Savings C02 per year [g/a]) / (saving potential [g/kWh] * production of unit [kWh/a])
        # self.pv_panels_peryear =  ((cr.e18.e.CO2e_total-cr.e30.e.CO2e_total)* 1e6)/((inputs.entries.m_year_target-inputs.entries.m_year_today) * (850-40) * (1000/4)) # assumption: 1000 kWh/a per 4 modules
        # self.wind_power_plants_peryear = ((cr.e18.e.CO2e_total-cr.e30.e.CO2e_total)* 1e6)/((inputs.entries.m_year_target-inputs.entries.m_year_today) * (850-25) * (1700 * 3.2 * 1e3)) # assumption: 1700 full-load hours per year and 3,2 MW reference wind power plant
        # Amount per year = LocalToBeInstalledPower / (Reference * years) 
        # electricity
        duration = inputs.entries.m_year_target - inputs.entries.m_year_today
        self.pv_panels_peryear = cr.e30.p_local.power_to_be_installed / (self.refs.pv_panel*duration)
        self.wind_power_plants_peryear = cr.e30.p_local_wind_onshore.power_to_be_installed / (self.refs.wind_power_plant*duration)
        # heating
        self.heat_power_plants_area = cr.h30.p_heatnet_plant.area_ha_available
        self.large_heatpumps = cr.h30.p_heatnet_lheatpump.power_to_be_installed / (self.refs.large_heatpump)
        # residences
        self.heatpumps_peryear = cr.r30.s_heatpump.power_to_be_installed / ((self.refs.heatpump)*duration)
        self.renovated_houses_peryear = cr.r18.p_buildings_total.number_of_buildings * inputs.entries.r_rehab_rate_pa
        # transport
        self.electric_bus_peryear = cr.t30.road_bus.invest_pa_com / cr.t30.road_bus.invest_per_x
        self.electric_car_peryear = cr.t30.road_car.fleet_modernisation_cost.invest_pa / cr.t30.road_car.fleet_modernisation_cost.invest_per_x
        # industry, business, agriculture, fuels, lulucf
        # tbd
        return self

def json_to_output(json_object: Any, args: Any):
    """Write json_object to stdout or a file depending on args"""
    if args.o is not None:
        with open(args.o, mode="w") as fp:
            json.dump(json_object, indent=4, fp=fp)
    else:
        json.dump(json_object, indent=4, fp=sys.stdout)

def cmd_indicators(args: Any):
    refdata = RefData.load()
    entries = make_entries(refdata, ags=args.ags, year=int(args.year))
    inputs = Inputs(facts_and_assumptions=refdata.facts_and_assumptions(), entries=entries)
    ind = Indicators()
    ind = ind.calculate_indicators(inputs, calculate_with_default_inputs(ags=args.ags, year=int(args.year)))
    # ind.calculate_indicators(inputs, calculate_with_default_inputs(ags=args.ags, year=int(args.year)))
    print("What can be done to safe the climate?")
    d = with_tracing(
            enabled=args.trace,
            f=lambda: ind.result_dict()
    )
    json_to_output(d, args)
    
    