from dataclasses import dataclass
from site import setcopyright

from ..utils import div
from .. import (
    agri2018,
    electricity2018,
    business2018,
    fuels2018,
    heat2018,
    industry2018,
    lulucf2018,
    residences2018,
    transport2018,
    agri2030,
    business2030,
    electricity2030,
    fuels2030,
    heat2030,
    industry2030,
    lulucf2030,
    residences2030,
    transport2030,
)

@dataclass
class energy_source:
    energy: float 
    
    CO2e_cb_self: float

    CO2e_cb: float = 0 

    CO2e_cb_from_heat: float|None = None
    CO2e_cb_from_elec: float|None = None
    CO2e_cb_from_fuels: float|None = None

    CO2e_pb: float|None = None


    def __post_init__(self):

        def non_sum(*args)->float:
            return_float: float = 0
            for elem in args:
                if  elem is None:
                    continue
                return_float += elem

            return return_float
            
        self.CO2e_cb = non_sum(self.CO2e_cb_self,self.CO2e_cb_from_heat,self.CO2e_cb_from_elec,self.CO2e_cb_from_fuels) 

@dataclass
class bisko_sector:
   petrol: energy_source
   fueloil: energy_source
   coal: energy_source
   lpg: energy_source
   gas: energy_source
   heatnet: energy_source
   biomass: energy_source
   solarth: energy_source
   heatpump: energy_source
   elec: energy_source
   heatpump: energy_source
   diesel: energy_source
   jetfuel: energy_source
   biomass: energy_source
   bioethanol: energy_source
   biodiesel: energy_source
   biogas: energy_source
   other: energy_source


@dataclass
class bisko:
    ph: bisko_sector
    ghd: bisko_sector
    traffic: bisko_sector
    industry: bisko_sector

def calc(
    *,
    a18: agri2018.A18,
    b18: business2018.B18,
    e18: electricity2018.E18,
    f18: fuels2018.F18,
    h18: heat2018.H18,
    i18: industry2018.I18,
    l18: lulucf2018.L18,
    r18: residences2018.R18,
    t18: transport2018.T18,
    a30: agri2030.A30,
    b30: business2030.B30,
    e30: electricity2030.E30,
    f30: fuels2030.F30,
    h30: heat2030.H30,
    i30: industry2030.I30,
    l30: lulucf2030.L30,
    r30: residences2030.R30,
    t30: transport2030.T30,
) -> bisko:

    ph_bisko = calc_ph_bisko()
    ghd_bisko = calc_ghd_bisko()
    traffic_bisko = calc_traffic_bisko()
    industry_bisko = calc_industry_bisko()

    return bisko(
        ph=ph_bisko,


    )


def calc_ph_bisko(r18:residences2018.R18,h18:heat2018.H18,f18:fuels2018.F18,e18:electricity2018.E18,  ) -> bisko_sector:

    petrol = energy_source(energy=r18.s_petrol.energy,CO2e_cb_self=r18.s_petrol.CO2e_total,CO2e_cb_from_fuels=f18.p_petrol.CO2e_production_based*div(f18.d_r.energy,f18.d.energy)) 
    fueloil = energy_source(energy=r18.s_fueloil.energy,CO2e_cb_self=r18.s_fueloil.CO2e_total,CO2e_cb_from_heat=h18.p_fueloil.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy))
    coal = energy_source(energy=r18.s_coal.energy,CO2e_cb_self=r18.s_coal.CO2e_total,CO2e_cb_from_heat=h18.p_coal.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy),CO2e_pb=h18.p_coal.CO2e_production_based*div(h18.d_r.energy,h18.d.energy))