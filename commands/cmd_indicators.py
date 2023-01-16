# pyright: strict

from typing import Any
import json
import sys
import os
from dataclasses import dataclass

from climatevision.generator import calculate_with_default_inputs, make_entries, RefData, Result, Inputs
from climatevision.tracing import with_tracing
from climatevision.generator.generator import dataclass_to_result_dict

@dataclass(kw_only=True)
class References:
    # reference modules for calculation
    def __init__(self):
        self.pv_panel: float = 0.010 # 8-12 kWp = 0.08 MWp .. per standardized family home (https://solar-ratgeber.ch/photovoltaik/rendite-ertrag/#)
        self.wind_power_plant: float = 3.2 # 3.2 MW reference wind power plant (2013_Umweltbundesamt_PotenzialWindenergieAnLand, P.15)
        self.large_heatpump: float = 20 # 20 MW standardized large heat pump
        self.heatpump: float = 0.012 # 12 kW standardized heat pump
        self.biomass_plant: float = 0.750 # 750 kW standardized biomass plant (2022, Statista Research Department, Biogasanlagen - Anzahl in Deutschland bis 2022) 

    def change_refs(self):
        return 0

@dataclass(kw_only=True)
class Indicators: 
    
    refs = References() # sector electricity:  reference modules 
    pv_panels_peryear: float = 0 # sector electricity: pv panels to build per year 
    wind_power_plants_peryear: float = 0 # sector electricity:  wind power plants to build per year 
    heatnet_power_plants_area_ha: float = 0 # sector heat: area with heat power plants to build per year 
    large_heatpumps: float = 0 # sector heat: large heat power plants to build
    # biomass_plants: float = 0 # sector heat: biomass plants
    heatpumps_peryear_residence: float = 0 #  sector residences: heat pumps to build per year 
    renovated_houses_peryear: float = 0  # sector residences: houses to renovate per year
    electric_bus_peryear: float = 0 # sector transport: electrical bus to build per year
    electric_car_peryear: float = 0 # sector transport: electrical cars to build per year 
    heatpumps_peryear_business: float = 0 # sector business: heat pumps to build per year

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
        self.pv_panels_peryear = cr.e30.p_local.power_to_be_installed / (self.refs.pv_panel*inputs.entries.m_duration_neutral)
        self.wind_power_plants_peryear = cr.e30.p_local_wind_onshore.power_to_be_installed / (self.refs.wind_power_plant*inputs.entries.m_duration_neutral)
        # heating
        self.heatnet_power_plants_area_ha = cr.h30.p_heatnet_plant.area_ha_available
        self.large_heatpumps = cr.h30.p_heatnet_lheatpump.power_to_be_installed / (self.refs.large_heatpump)
        # residences
        self.heatpumps_peryear_residence = cr.r30.s_heatpump.power_to_be_installed / ((self.refs.heatpump)*inputs.entries.m_duration_neutral)
        self.renovated_houses_peryear = cr.r18.p_buildings_total.number_of_buildings * inputs.entries.r_rehab_rate_pa
        # transport
        self.electric_bus_peryear = cr.t30.road_bus.invest_pa_com / cr.t30.road_bus.invest_per_x
        self.electric_car_peryear = cr.t30.road_car.fleet_modernisation_cost.invest_pa / cr.t30.road_car.fleet_modernisation_cost.invest_per_x
        # business
        self.heatpumps_peryear_business = cr.b30.s_heatpump.power_to_be_installed / ((self.refs.heatpump)*inputs.entries.m_duration_neutral)
        # agriculture
        # -> reduction of animals per year
        # industry
        # -> change x production to carbon neutrality
        # fuels
        # -> Change to efuels
        # lulucf
        # plants x trees, ha moor

        # tbd
        return self

    def output_to_txt(self, inputs:Inputs):
        out_path = os.environ["temp"] # delete afterwards as probably only working for windows
        out_file = open(out_path + "/indicators_output_" + inputs.entries.ags + "_" + str(inputs.entries.m_year_target) + ".txt", "w")
        txt= """Um die Transition zu einer klimaneutralen Kommune bis zum Jahre {} zu bewerkstelligen, können unter anderem folgende Maßnahmen ergriffen werden:\n 
        • Zur Stromversorgung werden pro Jahr {:.0f} Photovoltaikanlagen mit einer Leistung von {:.0f} kWp sowie {:.2f} Windräder à {} MW gebaut.\n
        • Die Wärmeversorgung wird durch ein solarthermisches Kraftwerk mit {:.2f} Hektar und {:.2f} Großwärmepumpen à {} MW gewährleistet.\n
        • Die Renovierungen von jährlich {:.0f} Wohngebäuden sowie der Bau von {:.0f} Wärmepumpen à {} kW in Wohnhäusern wird vorangetrieben.\n
        • Im Transportwesen werden die Verbrennermotoren jährlich durch {:.0f} elektrische Busse sowie {:.0f} elektrische Autos ersetzt.\n
        • Die fossile Wärmeversorgung in Geschäftsgebäuden wird pro Jahr durch {:.0f} Wärmepumpen erneuert."""
        print(txt.format(inputs.entries.m_year_target,self.pv_panels_peryear, self.refs.pv_panel*1000, self.wind_power_plants_peryear, self.refs.wind_power_plant,
                        self.heatnet_power_plants_area_ha, self.large_heatpumps, self.refs.large_heatpump, self.renovated_houses_peryear, self.heatpumps_peryear_residence,
                        self.refs.heatpump*1000, self.electric_bus_peryear, self.electric_car_peryear, self.heatpumps_peryear_business), file=out_file)
        out_file.close

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
    ind.output_to_txt(inputs)
    
    