# pyright: strict

from typing import Any
import json
import sys
from dataclasses import dataclass

from climatevision.generator import calculate_with_default_inputs, make_entries, RefData, Result, Inputs
from climatevision.tracing import with_tracing
from climatevision.generator.generator import dataclass_to_result_dict

@dataclass(kw_only=True)
class Indicators: 
    pv_pa: float = 0 # pv panels per year to build
    wpp_pa: float = 0 # wind power plants per year to build
    hp_pa: float = 0 # heat pumps to build per year
    ren_houses_pa: float = 0  # houses to renovate per year
    elec_veh_pa: float = 0 # electrical vehicles per year to build 

    def result_dict(self):
        return dataclass_to_result_dict(self)
    
    def calculate_indicators(self, input:Inputs, cr:Result):
        """
        This function allows to calculate several indicators to enhance the comprehensibility 
        of the by the generator calculated data. All calculation are assumptions based on diverse 
        literature (see ). The indicators represent the necessary changes/possiblities per year
        to mitigate C02 emissions. Each indicator is representing a sector. Current indicators are 
        photovoltaic (pv_pa) and wind power plants (wpp_pa) for electricity, heatpumps (hp_pa) and 
        renovated houses (ren_houses_pa) for heating, elec_veh_pa for transport.
        """
        # Amount PV per year = (Savings C02 per year [g/a]) / (saving potential [g/kWh] * production of unit [kWh/a])
        self.pv_pa =  ((cr.e18.e.CO2e_total-cr.e30.e.CO2e_total)* 1e6)/((input.entries.m_year_target-input.entries.m_year_today) * (850-40) * (1000/4)) # assumption: 1000 kWh/a per 4 modules
        self.wpp_pa = ((cr.e18.e.CO2e_total-cr.e30.e.CO2e_total)* 1e6)/((input.entries.m_year_target-input.entries.m_year_today) * (850-25) * (1700 * 3.2 * 1e3)) # assumption: 1700 full-load hours per year and 3,2 MW reference wind power plant
        self.hp_pa = 0
        self.ren_houses_pa = 0
        self.elec_veh_pa = 0
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
    print("")
    d = with_tracing(
            enabled=args.trace,
            f=lambda: ind.result_dict()
    )
    json_to_output(d, args)
    
    