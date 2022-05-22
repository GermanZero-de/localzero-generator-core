from dataclasses import dataclass

from generatorcore.inputs import Inputs

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
class EnergySourceCalcIntermediate: 

    eb_energy_from_same_sector: float

    eb_CO2e_cb_from_same_sector: float|None = None

    eb_energy_from_agri: float|None = None     

    eb_CO2e_cb_from_heat: float|None = None
    eb_CO2e_cb_from_elec: float|None = None
    eb_CO2e_cb_from_fuels: float|None = None
    eb_CO2e_cb_from_agri: float|None = None

    energy: float = 0
    CO2e_cb: float = 0

    # production based Emissions
    CO2e_pb: float|None = None

    eb_CO2e_pb_from_heat: float|None = None

    def __post_init__(self):

        def sum_over_none_and_float(*args:float|None)->float:
            return_float: float = 0
            for elem in args:
                if  elem is None:
                    continue
                return_float += elem

            return return_float
        #automatically sum over all cb_based emissions    
        self.CO2e_cb = sum_over_none_and_float(self.eb_CO2e_cb_from_same_sector,self.eb_CO2e_cb_from_heat,self.eb_CO2e_cb_from_elec,self.eb_CO2e_cb_from_fuels,self.eb_CO2e_cb_from_agri)
        self.energy = sum_over_none_and_float(self.eb_energy_from_same_sector,self.eb_energy_from_agri)
        self.CO2e_pb = self.eb_CO2e_pb_from_heat


@dataclass
class SumClass:
    # energy consumption
    energy: float

    energy_from_same_eb_sector: float
    energy_from_eb_agri_sector: float

    # combustion based Emissions
    CO2e_cb: float

    eb_CO2e_from_same_sector: float
    eb_CO2e_cb_from_agri: float
    eb_CO2e_cb_from_heat: float 
    eb_CO2e_cb_from_elec: float
    eb_CO2e_cb_from_fuels: float

    # production based Emissions
    CO2e_pb: float
    eb_CO2e_pb_from_heat: float


    @classmethod
    def calc(cls,*args: EnergySourceCalcIntermediate):
        energy = sum([elem.energy if elem.energy != None else 0 for elem in args])
        energy_from_same_eb_sector = sum([elem.eb_energy_from_same_sector if elem.eb_energy_from_same_sector != None else 0 for elem in args])
        energy_from_eb_agri_sector = sum([elem.eb_energy_from_agri if elem.eb_energy_from_agri != None else 0 for elem in args])
        CO2e_cb = sum([elem.CO2e_cb if elem.CO2e_cb != None else 0 for elem in args])
        eb_CO2e_from_same_sector = sum([elem.eb_CO2e_cb_from_same_sector if elem.eb_CO2e_cb_from_same_sector != None else 0 for elem in args])
        eb_CO2e_cb_from_agri= sum([elem.eb_CO2e_cb_from_agri if elem.eb_CO2e_cb_from_agri != None else 0 for elem in args])
        eb_CO2e_cb_from_heat= sum([elem.eb_CO2e_cb_from_heat if elem.eb_CO2e_cb_from_heat != None else 0 for elem in args])
        eb_CO2e_cb_from_elec= sum([elem.eb_CO2e_cb_from_elec if elem.eb_CO2e_cb_from_elec != None else 0 for elem in args])
        eb_CO2e_cb_from_fuels= sum([elem.eb_CO2e_cb_from_fuels if elem.eb_CO2e_cb_from_fuels != None else 0 for elem in args])
        CO2e_pb = sum([elem.CO2e_pb if elem.CO2e_pb != None else 0 for elem in args])
        eb_CO2e_pb_from_heat = sum([elem.eb_CO2e_pb_from_heat if elem.eb_CO2e_pb_from_heat != None else 0 for elem in args])

        return cls(
            energy=energy,
            energy_from_same_eb_sector=energy_from_same_eb_sector,
            energy_from_eb_agri_sector = energy_from_eb_agri_sector,
            CO2e_cb=CO2e_cb,
            eb_CO2e_from_same_sector=eb_CO2e_from_same_sector,
            eb_CO2e_cb_from_agri=eb_CO2e_cb_from_agri,
            eb_CO2e_cb_from_heat = eb_CO2e_cb_from_heat,
            eb_CO2e_cb_from_elec = eb_CO2e_cb_from_elec,
            eb_CO2e_cb_from_fuels = eb_CO2e_cb_from_fuels,
            CO2e_pb = CO2e_pb,
            eb_CO2e_pb_from_heat=eb_CO2e_pb_from_heat,
        )
        
@dataclass
class EnergySource: 
    # energy consumption
    energy: float = 0

    # combustion based Emissions
    CO2e_cb: float = 0

    # production based Emissions
    CO2e_pb: float|None = None


    def __init__(self,energy_source_intermediate:EnergySourceCalcIntermediate):
        self.energy = energy_source_intermediate.energy
        self.CO2e_cb = energy_source_intermediate.CO2e_cb
        self.CO2e_pb = energy_source_intermediate.CO2e_pb



@dataclass
class BiskoSector:

    total: SumClass

    lpg: EnergySource
    gas: EnergySource
    elec: EnergySource

   

@dataclass
class BiskoPH(BiskoSector):
    petrol: EnergySource
    fueloil: EnergySource
    coal: EnergySource  
    heatnet: EnergySource
    biomass: EnergySource
    solarth: EnergySource
    heatpump: EnergySource

    @classmethod
    def calc_ph_bisko(cls, r18:residences2018.R18,h18:heat2018.H18,f18:fuels2018.F18,e18:electricity2018.E18) -> "BiskoPH":

        petrol = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_petrol.energy,eb_CO2e_cb_from_same_sector=r18.s_petrol.CO2e_total,eb_CO2e_cb_from_fuels=f18.p_petrol.CO2e_production_based*div(f18.d_r.energy,f18.d.energy)) 
        fueloil = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_fueloil.energy,eb_CO2e_cb_from_same_sector=r18.s_fueloil.CO2e_total,eb_CO2e_cb_from_heat=h18.p_fueloil.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy))
        coal = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_coal.energy,eb_CO2e_cb_from_same_sector=r18.s_coal.CO2e_total,eb_CO2e_cb_from_heat=h18.p_coal.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_coal.CO2e_production_based*div(h18.d_r.energy,h18.d.energy))
        lpg = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_lpg.energy,eb_CO2e_cb_from_same_sector=r18.s_lpg.CO2e_total,eb_CO2e_cb_from_heat=h18.p_lpg.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy))
        gas = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_gas.energy,eb_CO2e_cb_from_same_sector=r18.s_gas.CO2e_total,eb_CO2e_cb_from_heat=h18.p_gas.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_gas.CO2e_production_based*div(h18.d_r.energy,h18.d.energy))
        heatnet = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_heatnet.energy,eb_CO2e_cb_from_same_sector=r18.s_heatnet.CO2e_total,eb_CO2e_cb_from_heat=h18.p_heatnet.CO2e_combustion_based*div(h18.d_r.energy,h18.d.energy))
        biomass = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_biomass.energy,eb_CO2e_cb_from_same_sector=r18.s_biomass.CO2e_total,eb_CO2e_pb_from_heat=h18.p_biomass.CO2e_production_based*div(h18.d_r.energy,h18.d.energy))
        solarth = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_solarth.energy,eb_CO2e_cb_from_same_sector=r18.s_solarth.CO2e_total,eb_CO2e_pb_from_heat=h18.p_solarth.CO2e_production_based*div(h18.d_r.energy,h18.d.energy))
        heatpump = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_heatpump.energy,eb_CO2e_cb_from_same_sector=r18.s_heatpump.CO2e_total,eb_CO2e_pb_from_heat=h18.p_heatpump.CO2e_production_based*div(h18.d_r.energy,h18.d.energy))
        elec = EnergySourceCalcIntermediate(eb_energy_from_same_sector=r18.s_elec.energy,eb_CO2e_cb_from_same_sector=r18.s_elec.CO2e_total,eb_CO2e_cb_from_elec=e18.p.CO2e_total*div(e18.d_r.energy,e18.d.energy))

        total = SumClass.calc(petrol,fueloil,coal,lpg,gas,heatnet,biomass,solarth,heatpump,elec)


        return cls(
            petrol=EnergySource(petrol),
            fueloil=EnergySource(fueloil),
            coal=EnergySource(coal),
            lpg=EnergySource(lpg),
            gas=EnergySource(gas),
            heatnet=EnergySource(heatnet),
            biomass=EnergySource(biomass),
            solarth=EnergySource(solarth),
            heatpump=EnergySource(heatpump),
            elec=EnergySource(elec),
            total=total,
        )
    
@dataclass
class BiskoGHD(BiskoSector):
    petrol: EnergySource
    diesel: EnergySource
    jetfuel: EnergySource
    fueloil: EnergySource
    coal: EnergySource     
    heatnet: EnergySource
    biomass: EnergySource
    solarth: EnergySource
    heatpump: EnergySource

    @classmethod
    def calc_ghd_bisko(cls, b18:business2018.B18,h18:heat2018.H18,f18:fuels2018.F18,e18:electricity2018.E18,a18:agri2018.A18) -> "BiskoGHD":

        petrol = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_petrol.energy,eb_energy_from_agri=a18.s_petrol.energy,eb_CO2e_cb_from_same_sector=b18.s_petrol.CO2e_total,eb_CO2e_cb_from_agri=a18.s_petrol.CO2e_total,eb_CO2e_cb_from_fuels=f18.p_petrol.CO2e_production_based*div(f18.d_b.energy+f18.d_a.energy,f18.d.energy)) 
        diesel = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_diesel.energy,eb_energy_from_agri=a18.s_diesel.energy,eb_CO2e_cb_from_same_sector=b18.s_diesel.CO2e_total,eb_CO2e_cb_from_agri=a18.s_diesel.CO2e_total,eb_CO2e_cb_from_fuels=f18.p_diesel.CO2e_production_based*div(f18.d_b.energy+f18.d_a.energy,f18.d.energy))
        jetfuel = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_jetfuel.energy,eb_CO2e_cb_from_same_sector=b18.s_jetfuel.CO2e_total,eb_CO2e_cb_from_fuels=f18.p_jetfuel.CO2e_production_based*div(f18.d_b.energy,f18.d.energy))
        #TODO: fix h.18.a_t....
        fueloil = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_fueloil.energy,eb_energy_from_agri=a18.s_fueloil.energy,eb_CO2e_cb_from_same_sector=b18.s_fueloil.CO2e_total,eb_CO2e_cb_from_agri=a18.s_fueloil.CO2e_combustion_based,eb_CO2e_cb_from_heat=h18.p_fueloil.CO2e_combustion_based*div(h18.d_b.energy+h18.a_t.energy,h18.d.energy))
        coal = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_coal.energy,eb_CO2e_cb_from_same_sector=b18.s_coal.CO2e_total,eb_CO2e_cb_from_heat=h18.p_coal.CO2e_combustion_based*div(h18.d_b.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_coal.CO2e_production_based*div(h18.d_b.energy,h18.d.energy))
        lpg = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_lpg.energy,eb_energy_from_agri=a18.s_lpg.energy,eb_CO2e_cb_from_same_sector=b18.s_lpg.CO2e_total,eb_CO2e_cb_from_agri=a18.s_lpg.CO2e_total,eb_CO2e_cb_from_heat=h18.p_lpg.CO2e_combustion_based*div(h18.d_b.energy+h18.a_t.energy,h18.d.energy))
        gas = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_gas.energy,eb_energy_from_agri=a18.s_gas.energy,eb_CO2e_cb_from_same_sector=b18.s_gas.CO2e_total,eb_CO2e_cb_from_agri=a18.s_gas.CO2e_total,eb_CO2e_cb_from_heat=h18.p_gas.CO2e_combustion_based*div(h18.d_b.energy+h18.a_t.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_gas.CO2e_production_based*div(h18.d_b.energy+h18.a_t.energy,h18.d.energy))
        heatnet = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_heatnet.energy,eb_CO2e_cb_from_same_sector=b18.s_heatnet.CO2e_total,eb_CO2e_cb_from_heat=h18.p_heatnet.CO2e_combustion_based*div(h18.d_b.energy,h18.d.energy))
        biomass = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_biomass.energy,eb_energy_from_agri=a18.s_biomass.energy,eb_CO2e_cb_from_same_sector=b18.s_biomass.CO2e_total,eb_CO2e_cb_from_agri=a18.s_biomass.CO2e_total,eb_CO2e_pb_from_heat=h18.p_biomass.CO2e_production_based*div(h18.d_b.energy+h18.a_t.energy,h18.d.energy))
        solarth = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_solarth.energy,eb_CO2e_cb_from_same_sector=b18.s_solarth.CO2e_total,eb_CO2e_pb_from_heat=h18.p_solarth.CO2e_production_based*div(h18.d_b.energy,h18.d.energy))
        heatpump = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_heatpump.energy,eb_CO2e_cb_from_same_sector=b18.s_heatpump.CO2e_total,eb_CO2e_pb_from_heat=h18.p_heatpump.CO2e_production_based*div(h18.d_b.energy,h18.d.energy))
        elec = EnergySourceCalcIntermediate(eb_energy_from_same_sector=b18.s_elec.energy,eb_energy_from_agri=a18.s_elec.energy,eb_CO2e_cb_from_same_sector=b18.s_elec.CO2e_total,eb_CO2e_cb_from_agri=a18.s_elec.CO2e_total,eb_CO2e_cb_from_elec=e18.p.CO2e_total*div(e18.d_b.energy+e18.d_a.energy,e18.d.energy))

        total = SumClass.calc(petrol,diesel,jetfuel,fueloil,coal,lpg,gas,heatnet,biomass,solarth,heatpump,elec)


        return cls(
            petrol=EnergySource(petrol),
            diesel=EnergySource(diesel),
            jetfuel=EnergySource(jetfuel),
            fueloil=EnergySource(fueloil),            
            coal=EnergySource(coal),
            lpg=EnergySource(lpg),
            gas=EnergySource(gas),
            heatnet=EnergySource(heatnet),
            biomass=EnergySource(biomass),
            solarth=EnergySource(solarth),
            heatpump=EnergySource(heatpump),
            elec=EnergySource(elec),
            total=total,
        )
   
@dataclass
class BiskoTraffic(BiskoSector):

    petrol: EnergySource
    diesel: EnergySource
    jetfuel: EnergySource
    bioethanol: EnergySource
    biodiesel: EnergySource
    biogas: EnergySource

    @classmethod
    def calc_traffic_bisko(cls, inputs:Inputs, t18:transport2018.T18,h18:heat2018.H18,f18:fuels2018.F18,e18:electricity2018.E18) -> "BiskoTraffic":

        fact = inputs.fact
        ass = inputs.ass

        petrol = EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_petrol.energy,eb_CO2e_cb_from_same_sector=t18.s_petrol.energy*fact("Fact_T_S_petrol_EmFa_tank_wheel_2018"),eb_CO2e_cb_from_fuels=f18.p_petrol.CO2e_production_based*div(f18.d_t.energy,f18.d.energy)) 
        diesel = EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_diesel.energy,eb_CO2e_cb_from_same_sector=t18.s_diesel.energy*fact("Fact_T_S_diesel_EmFa_tank_wheel_2018"),eb_CO2e_cb_from_fuels=f18.p_diesel.CO2e_production_based*div(f18.d_t.energy+f18.d_a.energy,f18.d.energy))
        jetfuel = EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_jetfuel.energy,eb_CO2e_cb_from_same_sector=t18.s_jetfuel.energy*fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018"),eb_CO2e_cb_from_fuels=f18.p_jetfuel.CO2e_production_based*div(f18.d_t.energy,f18.d.energy))
        bioethanol= EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_bioethanol.energy,eb_CO2e_cb_from_same_sector=t18.s_bioethanol.energy*ass("Ass_T_S_bioethanol_EmFa_tank_wheel"),eb_CO2e_cb_from_fuels=f18.p_bioethanol.CO2e_production_based*div(f18.d_t.energy,f18.d.energy))
        biodiesel= EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_biodiesel.energy,eb_CO2e_cb_from_same_sector=t18.s_biodiesel.energy*ass("Ass_T_S_biodiesel_EmFa_tank_wheel"),eb_CO2e_cb_from_fuels=f18.p_biodiesel.CO2e_production_based*div(f18.d_t.energy,f18.d.energy))
        biogas= EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_biogas.energy,eb_CO2e_cb_from_same_sector=t18.s_biogas.energy*ass("Ass_T_S_biogas_EmFa_tank_wheel"),eb_CO2e_cb_from_fuels=f18.p_biogas.CO2e_production_based*div(f18.d_t.energy,f18.d.energy))
        lpg = EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_lpg.energy,eb_CO2e_cb_from_same_sector=t18.s_lpg.energy*fact("Fact_T_S_lpg_EmFa_tank_wheel_2018"),eb_CO2e_cb_from_heat=h18.p_lpg.CO2e_combustion_based*div(h18.d_t.energy,h18.d.energy))
        gas = EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_gas.energy,eb_CO2e_cb_from_same_sector=t18.s_gas.energy*fact("Fact_T_S_cng_EmFa_tank_wheel_2018"),eb_CO2e_cb_from_heat=h18.p_gas.CO2e_combustion_based*div(h18.d_t.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_gas.CO2e_production_based*div(h18.d_t.energy,h18.d.energy))
        elec = EnergySourceCalcIntermediate(eb_energy_from_same_sector=t18.s_elec.energy,eb_CO2e_cb_from_same_sector=t18.s_elec.energy*fact("Fact_T_S_electricity_EmFa_tank_wheel_2018"),eb_CO2e_cb_from_elec=e18.p.CO2e_total*div(e18.d_t.energy,e18.d.energy))

        total = SumClass.calc(petrol,diesel,jetfuel,bioethanol,biodiesel,biogas,lpg,gas,elec)


        return cls(
            petrol=EnergySource(petrol),
            diesel=EnergySource(diesel),
            jetfuel=EnergySource(jetfuel),
            bioethanol=EnergySource(bioethanol),
            biodiesel=EnergySource(biodiesel),
            biogas=EnergySource(biogas),
            lpg=EnergySource(lpg),
            gas=EnergySource(gas),
            elec=EnergySource(elec),
            total=total,
        )

@dataclass
class BiskoIndustry(BiskoSector):
    diesel: EnergySource
    fueloil: EnergySource
    coal: EnergySource
    other_fossil: EnergySource
    heatnet: EnergySource
    biomass: EnergySource
    solarth: EnergySource
    heatpump: EnergySource

    @classmethod
    def calc_industry_bisko(cls, i18:industry2018.I18,h18:heat2018.H18,f18:fuels2018.F18,e18:electricity2018.E18,a18:agri2018.A18) -> "BiskoIndustry":

        diesel = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_fossil_diesel.energy,eb_CO2e_cb_from_fuels=f18.p_diesel.CO2e_production_based*div(f18.d_i.energy,f18.d.energy))
        fueloil = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_fossil_fueloil.energy,eb_CO2e_cb_from_heat=h18.p_fueloil.CO2e_combustion_based*div(h18.d_i.energy,h18.d.energy))
        coal = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_fossil_coal.energy,eb_CO2e_cb_from_heat=h18.p_coal.CO2e_combustion_based*div(h18.d_i.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_coal.CO2e_production_based*div(h18.d_i.energy,h18.d.energy))
        lpg = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_fossil_lpg.energy,eb_CO2e_cb_from_heat=h18.p_lpg.CO2e_combustion_based*div(h18.d_i.energy,h18.d.energy))
        gas = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_fossil_gas.energy,eb_CO2e_cb_from_heat=h18.p_gas.CO2e_combustion_based*div(h18.d_i.energy,h18.d.energy),eb_CO2e_pb_from_heat=h18.p_gas.CO2e_production_based*div(h18.d_i.energy,h18.d.energy))
        other_fossil = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_fossil_ofossil.energy+i18.s_fossil_opetpro.energy,eb_CO2e_cb_from_heat=h18.p_opetpro.CO2e_combustion_based,eb_CO2e_pb_from_heat=h18.p_opetpro.CO2e_production_based+h18.p_ofossil.CO2e_production_based)
        
        heatnet = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_renew_heatnet.energy,eb_CO2e_cb_from_heat=h18.p_heatnet.CO2e_combustion_based*div(h18.d_i.energy,h18.d.energy))
        biomass = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_renew_biomass.energy,eb_CO2e_pb_from_heat=h18.p_biomass.CO2e_production_based*div(h18.d_i.energy,h18.d.energy))
        solarth = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_renew_solarth.energy,eb_CO2e_pb_from_heat=h18.p_solarth.CO2e_production_based*div(h18.d_i.energy,h18.d.energy))
        heatpump = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_renew_heatpump.energy,eb_CO2e_pb_from_heat=h18.p_heatpump.CO2e_production_based*div(h18.d_i.energy,h18.d.energy))
        elec = EnergySourceCalcIntermediate(eb_energy_from_same_sector=i18.s_renew_elec.energy,eb_CO2e_cb_from_elec=e18.p.CO2e_total*div(e18.d_i.energy,e18.d.energy))

        total = SumClass.calc(diesel,fueloil,coal,lpg,gas,other_fossil,heatnet,biomass,solarth,heatpump,elec)


        return cls(
            diesel=EnergySource(diesel),
            fueloil=EnergySource(fueloil),            
            coal=EnergySource(coal),
            lpg=EnergySource(lpg),
            gas=EnergySource(gas),
            other_fossil=EnergySource(other_fossil),
            heatnet=EnergySource(heatnet),
            biomass=EnergySource(biomass),
            solarth=EnergySource(solarth),
            heatpump=EnergySource(heatpump),
            elec=EnergySource(elec),
            total=total,
        )



@dataclass
class Bisko:
    ph: BiskoPH
    ghd: BiskoGHD
    traffic: BiskoTraffic
    #industry: BiskoSector

    
    @classmethod
    def calc(cls,
        inputs: Inputs,
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
    ) -> "Bisko":

        ph_bisko = BiskoPH.calc_ph_bisko(r18=r18,h18=h18,f18=f18,e18=e18)
        ghd_bisko = BiskoGHD.calc_ghd_bisko(b18=b18,h18=h18,f18=f18,e18=e18,a18=a18)
        traffic_bisko = BiskoTraffic.calc_traffic_bisko(inputs=inputs,t18=t18,h18=h18,f18=f18,e18=e18)
        #industry_bisko = calc_industry_bisko()

        return cls(
            ph=ph_bisko,
            ghd=ghd_bisko,
            traffic=traffic_bisko,
            #industry=industry_bisko,
        )


    