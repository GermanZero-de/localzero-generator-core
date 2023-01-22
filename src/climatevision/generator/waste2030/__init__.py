"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from dataclasses import dataclass
from ..inputs import Inputs
from ..utils import div
from ..waste2018 import W18
import math

@dataclass
class container:
    pass

@dataclass(kw_only=True)
class landfilling(container):
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float 
    change_CO2e_t: float 
    cost_climate_saved: float 


    @classmethod
    def calc(cls, inputs : Inputs, w18: W18):
        entries = inputs.entries
        fact = inputs.fact
        ass = inputs.ass

        CO2e_pb = (ass.W_P_landfilling_socket+ ass.W_P_landfilling_CO2e_pb_2005 * math.exp(-(entries.m_year_target-2005)/ass.W_P_landfilling_methane_decay)) * entries.m_population_com_2018/entries.m_population_nat
        CO2e_total = CO2e_pb
        change_CO2e_t = w18.p_landfilling.CO2e_total - CO2e_total
        change_CO2e_pct = change_CO2e_t/ w18.p_landfilling.CO2e_total

        CO2e_total_2021_estimated = w18.p_landfilling.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        cost_climate_saved = (CO2e_total_2021_estimated - CO2e_total)* entries.m_duration_neutral * fact("Fact_M_cost_per_CO2e_2020") 

        return cls(
        CO2e_production_based = CO2e_pb,
        CO2e_total= CO2e_total,
        CO2e_total_2021_estimated=CO2e_total_2021_estimated,
        change_CO2e_pct = change_CO2e_pct,
        change_CO2e_t = change_CO2e_t, 
        cost_climate_saved = cost_climate_saved,
        )

@dataclass(kw_only=True)
class organic_treatment(container):
    prod_volume: float
    CO2e_pb_per_t: float
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float 
    change_CO2e_t: float 
    cost_climate_saved: float
    invest_per_x: float
    ratio_wage_to_emplo: float
    pct_of_wage: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float



    @classmethod
    def calc(cls, inputs : Inputs, w18: W18):
        entries = inputs.entries
        fact = inputs.fact
        ass = inputs.ass

        prod_volume = entries.m_population_com_203X * ass.W_P_organic_treatment_prodvol_2050_per_capita
        CO2e_pb_per_t = ass.W_P_organic_treatment_CO2e_pb_2050_per_prodvol
        CO2e_pb = prod_volume * CO2e_pb_per_t
        CO2e_total = CO2e_pb
        change_CO2e_t = w18.p_organic_treatment.CO2e_total - CO2e_total
        change_CO2e_pct = change_CO2e_t/ w18.p_organic_treatment.CO2e_total

        CO2e_total_2021_estimated = w18.p_organic_treatment.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        cost_climate_saved = (CO2e_total_2021_estimated - CO2e_total)* entries.m_duration_neutral * fact("Fact_M_cost_per_CO2e_2020") 

        invest_per_x = ass.W_P_organic_treatment_fermentation_stage_invest_per_prodvol
        ratio_wage_to_emplo = fact.I_P_constr_civil_ratio_wage_to_emplo_2018
        pct_of_wage = fact.I_P_constr_civil_revenue_pct_of_wage_2018
        invest = prod_volume * invest_per_x
        invest_com = invest
        invest_pa = invest / entries.m_duration_target
        invest_pa_com = invest_pa	
        cost_wage = invest_pa * pct_of_wage
        demand_emplo = cost_wage / ratio_wage_to_emplo
        demand_emplo_new = demand_emplo

        return cls(
            prod_volume=prod_volume,
            CO2e_pb_per_t = CO2e_pb_per_t,
            CO2e_production_based = CO2e_pb,
            CO2e_total= CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct = change_CO2e_pct,
            change_CO2e_t = change_CO2e_t, 
            cost_climate_saved = cost_climate_saved,
            invest_per_x = invest_per_x,
            ratio_wage_to_emplo = ratio_wage_to_emplo, 
            pct_of_wage = pct_of_wage,
            invest = invest,
            invest_com = invest_com,
            invest_pa = invest_pa,
            invest_pa_com = invest_pa_com,
            cost_wage = cost_wage,
            demand_emplo = demand_emplo,
            demand_emplo_new = demand_emplo_new,
        )

@dataclass(kw_only=True)
class wastewater(container):
    energy:float
    prod_volume: float
    CO2e_pb_per_t: float
    CO2e_production_based: float
    CO2e_total: float
    change_energy_MWh: float
    change_energy_pct: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float 
    change_CO2e_t: float 
    cost_climate_saved: float



    @classmethod
    def calc(cls, inputs : Inputs, w18: W18):
        entries = inputs.entries
        fact = inputs.fact
        ass = inputs.ass

        
        prod_volume = entries.m_population_com_203X * ass.W_P_wastewater_prodvol_2050_per_capita
        energy =  w18.p_wastewater.energy * (prod_volume / w18.p_wastewater.prod_volume)

        CO2e_pb_per_t = ass.W_P_wastewater_CO2e_pb_2050_per_prodvol
        CO2e_pb = prod_volume * CO2e_pb_per_t
        CO2e_total = CO2e_pb

        change_energy_MWh = energy - w18.p_wastewater.energy
        change_energy_pct = change_energy_MWh / w18.p_wastewater.energy

        change_CO2e_t = w18.p_organic_treatment.CO2e_total - CO2e_total
        change_CO2e_pct = div(change_CO2e_t, w18.p_organic_treatment.CO2e_total)

        CO2e_total_2021_estimated = w18.p_organic_treatment.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
        cost_climate_saved = (CO2e_total_2021_estimated - CO2e_total)* entries.m_duration_neutral * fact("Fact_M_cost_per_CO2e_2020") 


        return cls(
            prod_volume=prod_volume,
            energy=energy,
            CO2e_pb_per_t = CO2e_pb_per_t,
            CO2e_production_based = CO2e_pb,
            CO2e_total= CO2e_total,
            change_energy_MWh = change_energy_MWh,
            change_energy_pct = change_energy_pct,
            CO2e_total_2021_estimated = CO2e_total_2021_estimated,
            change_CO2e_pct = change_CO2e_pct,
            change_CO2e_t = change_CO2e_t, 
            cost_climate_saved = cost_climate_saved,
        )

@dataclass(kw_only=True)
class EnergyProduction:
    energy: float
    prod_volume: float
    CO2e_production_based: float
    CO2e_total: float
    change_energy_MWh :float 
    change_energy_pct :float 
    change_CO2e_t :float 
    change_CO2_pct :float 
    CO2e_total_2021_estimated :float 
    cost_climate_saved :float 
    invest_pa :float 
    invest_pa_com :float 
    invest :float 
    invest_com :float 
    cost_wage :float 
    demand_emplo :float 
    demand_emplo_new :float

    @classmethod
    def calc(cls, w18: W18, landfilling:landfilling, organic_treatment:organic_treatment, wastewater:wastewater):

        energy = wastewater.energy
        prod_vol = organic_treatment.prod_volume + wastewater.prod_volume
        CO2e_pb = landfilling.CO2e_production_based + organic_treatment.CO2e_production_based + wastewater.CO2e_production_based
        CO2e_total = landfilling.CO2e_total + organic_treatment.CO2e_total + wastewater.CO2e_total
        change_energy_MWh = wastewater.change_energy_MWh
        change_energy_pct = change_energy_MWh / w18.p.energy
        change_CO2e_t = landfilling.change_CO2e_t + organic_treatment.change_CO2e_t + wastewater.change_CO2e_t
        change_CO2_pct = change_CO2e_t / w18.p.CO2e_total
        CO2e_total_2021_estimated = landfilling.CO2e_total_2021_estimated + organic_treatment.CO2e_total_2021_estimated  + wastewater.CO2e_total_2021_estimated 
        cost_climate_saved = landfilling.cost_climate_saved + organic_treatment.cost_climate_saved  + wastewater.cost_climate_saved
        invest_pa = organic_treatment.invest_pa
        invest_pa_com = organic_treatment.invest_pa_com
        invest = organic_treatment.invest
        invest_com = organic_treatment.invest_com
        cost_wage = organic_treatment.cost_wage
        demand_emplo = organic_treatment.demand_emplo
        demand_emplo_new = organic_treatment.demand_emplo_new

        return cls(
            energy=energy,
            prod_volume = prod_vol,
            CO2e_production_based = CO2e_pb,
            CO2e_total = CO2e_total,
            change_energy_MWh = change_energy_MWh,
            change_energy_pct = change_energy_pct,
            change_CO2e_t = change_CO2e_t,
            change_CO2_pct = change_CO2_pct,
            CO2e_total_2021_estimated = CO2e_total_2021_estimated,
            cost_climate_saved = cost_climate_saved,
            invest_pa = invest_pa ,
            invest_pa_com = invest_pa_com,
            invest = invest,
            invest_com = invest_com,
            cost_wage = cost_wage,
            demand_emplo = demand_emplo,
            demand_emplo_new = demand_emplo_new,
        )

@dataclass(kw_only=True)
class EnergySupplyDetail:
    energy: float
    CO2e_combustion_based: float
    CO2e_cb_per_MWh: float
    CO2e_total: float
    
    @classmethod
    def calc(cls, energy: float, CO2e_cb_per_MWh: float):
        CO2e_cb = CO2e_cb_per_MWh * energy
        return cls(
            energy = energy,
            CO2e_cb_per_MWh = CO2e_cb_per_MWh,
            CO2e_combustion_based = CO2e_cb,
            CO2e_total = CO2e_cb
        )

@dataclass(kw_only=True)
class EnergySupply:
    energy: float
    CO2e_combustion_based: float
    CO2e_total: float

    @classmethod
    def calc(cls, *energy_supplies: EnergySupplyDetail):
    
        energy = sum([supply.energy for supply in energy_supplies])
        CO2e_cb = sum([supply.CO2e_combustion_based for supply in energy_supplies])
        CO2e_total = sum([supply.CO2e_total for supply in energy_supplies])

        return cls(
            energy=energy,
            CO2e_combustion_based = CO2e_cb,
            CO2e_total = CO2e_total
        )

    

@dataclass(kw_only=True)
class W18:
    w: EnergyProduction
    p: EnergyProduction
    p_landfilling: landfilling
    p_organic_treatment: organic_treatment
    p_wastewater: wastewater

    s: EnergySupply
    s_elec: EnergySupplyDetail
    


    @classmethod
    def calc(cls, inputs: Inputs):

        entries = inputs.entries
        fact = inputs.fact

        s_elec = EnergySupplyDetail.calc(energy=entries.w_elec_fec,CO2e_cb_per_MWh=0)
        s = EnergySupply.calc(s_elec)

        p_landfilling = landfilling.calc(inputs=inputs,energy=0,use_prod_vol=False,CO2e_pb_per_t=fact.W_P_landfilling_CO2e_pb_2018_per_capita)
        p_organic_treatment = WasteBranch.calc(inputs=inputs,energy=0,use_prod_vol=True,prod_vol_per_cap=fact.W_P_organic_treatment_prodvol_2018_per_capita,CO2e_pb_per_t=fact.W_P_organic_treatment_CO2e_pb_2018_per_prodvol)
        p_wastewater = WasteBranch.calc(inputs=inputs,energy=entries.EEV_18K_AW_Strom,use_prod_vol=True,prod_vol_per_cap=fact.W_P_organic_treatment_prodvol_2018_per_capita,CO2e_pb_per_t=fact.W_P_organic_treatment_CO2e_pb_2018_per_prodvol)
        
        p = EnergyProduction.calc(p_landfilling,p_organic_treatment,p_wastewater)
        w=p
        return cls(
            w=w,
            p = p,
            p_landfilling = p_landfilling,
            p_organic_treatment = p_organic_treatment,
            p_wastewater =p_wastewater,
            s=s,
            s_elec = s_elec
        )