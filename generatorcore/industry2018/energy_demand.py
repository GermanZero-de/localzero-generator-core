# pyright: strict
from dataclasses import dataclass
from typing import Callable
from generatorcore.utils import div

from generatorcore import refdata
from ..inputs import Inputs
from .production_branches import ExtraEmission,ProductionSubBranch,ProductionSubBranchCO2viaFEC,ProductionSubSum,ProductionBranch,ProductionSum


@dataclass(kw_only=True)
class Production:

    p: ProductionSum

    p_miner: ProductionBranch
    p_miner_cement: ProductionSubBranch
    p_miner_chalk: ProductionSubBranch
    p_miner_glas: ProductionSubBranch
    p_miner_ceram: ProductionSubBranch

    p_chem: ProductionBranch
    p_chem_basic: ProductionSubBranch
    p_chem_ammonia: ProductionSubBranch
    p_chem_other: ProductionSubBranch

    p_metal: ProductionBranch
    p_metal_steel: ProductionSubSum
    p_metal_steel_primary: ProductionSubBranch
    p_metal_steel_secondary: ProductionSubBranch
    p_metal_nonfe: ProductionSubBranch

    p_other: ProductionBranch
    p_other_paper: ProductionSubBranch
    p_other_food: ProductionSubBranch
    p_other_further: ProductionSubBranchCO2viaFEC
    p_other_2efgh: ExtraEmission


def calc_production(inputs:Inputs) -> Production:
    fact = inputs.fact
    entries = inputs.entries

    prepare_facts(inputs=inputs)

    energy_consumption_industry = entries.i_energy_total
	
    energy_consumption_miner = energy_consumption_industry * entries.i_fec_pct_of_miner
    p_miner_cement = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="miner",sub_branch="cement",energy_consumption_branch=energy_consumption_miner) 
    p_miner_chalk = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="miner",sub_branch="chalk",energy_consumption_branch=energy_consumption_miner) 
    p_miner_glas = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="miner",sub_branch="glas",energy_consumption_branch=energy_consumption_miner) 
    p_miner_ceram = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="miner",sub_branch="ceram",energy_consumption_branch=energy_consumption_miner)
    p_miner =  ProductionBranch.calc_production_sum(sub_branch_list=[p_miner_cement,p_miner_chalk,p_miner_glas,p_miner_ceram])

    energy_consumption_chemistry = energy_consumption_industry * entries.i_fec_pct_of_chem
    p_chem_basic = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="chem",sub_branch="basic",energy_consumption_branch=energy_consumption_chemistry) 
    p_chem_ammonia = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="chem",sub_branch="ammonia",energy_consumption_branch=energy_consumption_chemistry) 
    p_chem_other = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="chem",sub_branch="other",energy_consumption_branch=energy_consumption_chemistry) 
    p_chem = ProductionBranch.calc_production_sum(sub_branch_list=[p_chem_basic,p_chem_ammonia,p_chem_other])

    energy_consumption_metal = energy_consumption_industry * entries.i_fec_pct_of_metal
    energy_consumption_metal_steel = energy_consumption_metal* fact("Fact_I_P_metal_fec_pct_of_steel")
    p_metal_steel_primary = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="metal",sub_branch="steel_primary",energy_consumption_branch=energy_consumption_metal_steel) 
    p_metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="metal",sub_branch="steel_secondary",energy_consumption_branch=energy_consumption_metal_steel)
    p_metal_steel = ProductionSubSum.calc_production_sub_sum(energy_consumption_branch=energy_consumption_metal,sub_branch_list=[p_metal_steel_primary,p_metal_steel_secondary])
    p_metal_nonfe = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="metal",sub_branch="nonfe",energy_consumption_branch=energy_consumption_metal) 
    p_metal = ProductionBranch.calc_production_sum(sub_branch_list=[p_metal_steel,p_metal_nonfe])

    energy_consumption_other = energy_consumption_industry * entries.i_fec_pct_of_other
    p_other_paper = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="other",sub_branch="paper",energy_consumption_branch=energy_consumption_other) 
    p_other_food = ProductionSubBranch.calc_production_sub_branch(inputs=inputs,branch="other",sub_branch="food",energy_consumption_branch=energy_consumption_other) 
    p_other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch(inputs=inputs,branch="other",sub_branch="further",energy_consumption_branch=energy_consumption_other)
    p_other_2efgh = ExtraEmission.calc_extra_emission(inputs=inputs,branch="other",sub_branch="2efgh",energy_consumption=p_other_further.energy)
    p_other = ProductionBranch.calc_production_sum(sub_branch_list=[p_other_paper,p_other_food],sub_branch_via_FEC_list=[p_other_further],extra_emission_list=[p_other_2efgh])

    p = ProductionSum.calc_production_sum(branch_list=[p_miner,p_chem,p_metal,p_other])

    return Production(
        p=p,
        p_miner=p_miner,
        p_miner_cement=p_miner_cement,
        p_miner_chalk=p_miner_chalk,
        p_miner_glas=p_miner_glas,
        p_miner_ceram=p_miner_ceram,
        p_chem=p_chem,
        p_chem_basic=p_chem_basic,
        p_chem_ammonia=p_chem_ammonia,
        p_chem_other=p_chem_other,
        p_metal=p_metal,
        p_metal_steel=p_metal_steel,
        p_metal_steel_primary=p_metal_steel_primary,
        p_metal_steel_secondary=p_metal_steel_secondary,
        p_metal_nonfe=p_metal_nonfe,
        p_other=p_other,
        p_other_paper=p_other_paper,
        p_other_food=p_other_food,
        p_other_further=p_other_further,
        p_other_2efgh=p_other_2efgh,
    )

def prepare_facts(inputs:Inputs):

    new_facts_and_assumptions = inputs.return_facts()
    new_facts:refdata.DataFrame[str] = new_facts_and_assumptions.return_fact_data_frame()

    def replace_value(instr:str, replace_value_functions: Callable[[float],float] = lambda x : x, inputs:refdata.DataFrame[str] = new_facts) -> list[str]:
        
        header = inputs.header
        string_list = [x for x in inputs.get(instr)] #copy by value
        string_list[header["value"]] = str(replace_value_functions(float(string_list[header["value"]])))

        return string_list

    additional_facts = {
    #mineralische Industrie Fakten
    "Fact_I_P_miner_fec_pct_of_cement":replace_value("Fact_I_P_miner_fec_pct_of_cement_2018"),
    "Fact_I_P_miner_cement_ratio_prodvol_to_fec":replace_value("Fact_I_P_miner_cement_energy_use_factor_2017"),
    "Fact_I_P_miner_cement_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_miner_cement_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_miner_cement_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_miner_cement_ratio_CO2e_cb_to_prodvol_2018"),

    "Fact_I_P_miner_fec_pct_of_chalk":replace_value("Fact_I_P_miner_fec_pct_of_chalk_2017"),
    "Fact_I_P_miner_chalk_ratio_prodvol_to_fec":replace_value("Fact_I_P_miner_chalk_energy_use_factor_2017"),
    "Fact_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol_2018"),

    "Fact_I_P_miner_fec_pct_of_glas":replace_value("Fact_I_P_miner_fec_pct_of_glas_2017"),
    "Fact_I_P_miner_glas_ratio_prodvol_to_fec":replace_value("Fact_I_P_miner_glas_energy_use_factor_2017"),
    "Fact_I_P_miner_glas_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_miner_glas_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_miner_glas_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_miner_glas_ratio_CO2e_cb_to_prodvol_2018"),

    "Fact_I_P_miner_fec_pct_of_ceram":replace_value("Fact_I_P_miner_fec_pct_of_ceram_2017"),
    "Fact_I_P_miner_ceram_ratio_prodvol_to_fec":replace_value("Fact_I_P_miner_ceram_energy_use_factor_2017"),
    "Fact_I_P_miner_ceram_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_miner_ceram_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_miner_ceram_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_miner_ceram_ratio_CO2e_cb_to_prodvol_2018"),

    #chemische Industrie Fakten
    "Fact_I_P_chem_fec_pct_of_basic":replace_value("Fact_I_S_chem_basic_wo_ammonia_fec_ratio_to_chem_all_2018"),
    "Fact_I_P_chem_basic_ratio_prodvol_to_fec":replace_value("Fact_I_P_chem_basic_wo_ammonia_ratio_prodvol_to_fec_2018"),
    "Fact_I_P_chem_basic_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_chem_basic_wo_ammonia_CO2e_pb_ratio_per_t_product_2018"),
    "Fact_I_P_chem_basic_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_chem_basic_wo_ammonia_CO2e_eb_ratio_per_t_product_2018"),

    "Fact_I_P_chem_fec_pct_of_ammonia":replace_value("Fact_I_S_chem_ammonia_fec_ratio_to_chem_all_2018"),
    "Fact_I_P_chem_ammonia_ratio_prodvol_to_fec":replace_value("Fact_I_P_chem_ammonia_fec_ratio_per_t_product_2013",lambda x: div(1,x)),
    "Fact_I_P_chem_ammonia_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_chem_ammonia_CO2e_pb_ratio_per_t_product_2018"),
    "Fact_I_P_chem_ammonia_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_chem_ammonia_CO2e_eb_ratio_per_t_product_2018"),

    "Fact_I_P_chem_fec_pct_of_other":replace_value("Fact_I_S_chem_other_fec_ratio_to_chem_all_2018"),
    "Fact_I_P_chem_other_ratio_prodvol_to_fec":replace_value("Fact_I_P_chem_other_ratio_prodvol_to_fec_2018"),
    "Fact_I_P_chem_other_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_chem_other_CO2e_pb_ratio_per_t_product_2018"),
    "Fact_I_P_chem_other_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_chem_other_CO2e_eb_ratio_per_t_product_2018"),

    #metallherstellende Industrie Fakten
    "Fact_I_P_metal_fec_pct_of_steel":replace_value("Fact_I_P_metal_fec_pct_of_steel_2018"),

    "Fact_I_P_metal_fec_pct_of_steel_primary":replace_value("Fakt_I_N_metallh_Primaerroute_EEV_2018_Anteil"),
    "Fact_I_P_metal_steel_primary_ratio_prodvol_to_fec":replace_value("Fact_I_P_metal_steel_primary_ratio_fec_to_prodvol_2018",lambda x: div(1,x)),
    "Fact_I_P_metal_steel_primary_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_metal_steel_primary_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_metal_steel_primary_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_metal_steel_primary_ratio_CO2e_eb_to_prodvol_2018"),

    "Fact_I_P_metal_fec_pct_of_steel_secondary":replace_value("Fakt_I_N_metallh_Sekundaerroute_EEV_2018_Anteil"),
    "Fact_I_P_metal_steel_secondary_ratio_prodvol_to_fec":replace_value("Fact_I_P_metal_steel_secondary_ratio_fec_to_prodvol_2018",lambda x: div(1,x)),
    "Fact_I_P_metal_steel_secondary_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_metal_steel_secondary_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_metal_steel_secondary_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_metal_steel_secondary_ratio_CO2e_eb_to_prodvol_2018"),

    "Fact_I_P_metal_fec_pct_of_nonfe":replace_value("Fact_I_P_metal_fec_pct_of_nonfe_2018"),
    "Fact_I_P_metal_nonfe_ratio_prodvol_to_fec":replace_value("Fact_I_P_metal_nonfe_ratio_fec_to_prodvol_2018",lambda x: div(1,x)),
    "Fact_I_P_metal_nonfe_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_metal_nonfe_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_metal_nonfe_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_metal_nonfe_ratio_CO2e_cb_to_prodvol_2018"),

    #sontige Industrie Fakten
    "Fact_I_P_other_fec_pct_of_paper":replace_value("Fact_I_P_other_fec_pct_of_paper_2018"),
    "Fact_I_P_other_paper_ratio_prodvol_to_fec":replace_value("Fact_I_P_other_paper_ratio_fec_to_prodvol_2018",lambda x: div(1,x)),
    "Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_other_paper_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_other_paper_ratio_CO2e_cb_to_prodvol_2018"),

    "Fact_I_P_other_fec_pct_of_food":replace_value("Fact_I_P_other_fec_pct_of_food_2018"),
    "Fact_I_P_other_food_ratio_prodvol_to_fec":replace_value("Fact_I_P_other_food_ratio_fec_to_prodvol_2018",lambda x: div(1,x)),
    "Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol":replace_value("Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol_2018"),
    "Fact_I_P_other_food_ratio_CO2e_cb_to_prodvol":replace_value("Fact_I_P_other_food_ratio_CO2e_cb_to_prodvol_2018"),

    "Fact_I_P_other_fec_pct_of_further":replace_value("Fact_I_P_other_fec_pct_of_further_2018"),
    "Fact_I_P_other_further_prodvol":replace_value("Fact_I_P_other_further_prodvol_2018"),
    "Fact_I_P_other_further_ratio_CO2e_pb_to_fec":replace_value("Fact_I_P_other_2d_ratio_CO2e_pb_to_fec_2018"),
    "Fact_I_P_other_further_ratio_CO2e_cb_to_fec":replace_value("Fact_I_P_other_further_ratio_CO2e_cb_to_fec_2018"),

    "Fact_I_P_other_2efgh_ratio_CO2e_pb_to_fec":replace_value("Fact_I_P_other_2efgh_ratio_CO2e_pb_to_fec_2018"),

    }

    new_facts.append_rows(additional_facts)

