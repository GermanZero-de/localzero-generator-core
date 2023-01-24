# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs

from .production_branches import (
    ExtraEmission,
    ProductionSubBranch,
    ProductionSubBranchCO2viaFEC,
    ProductionSubSum,
    ProductionBranch,
    ProductionSum,
)


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


def calc_production_by_co2e(
    inputs: Inputs, inputs_germany: Inputs, production_germany: Production
) -> Production:

    entries = inputs.entries

    co2e_miner_cement_corrected = (
        entries.i_dehst_miner_cement
        * production_germany.p_miner_cement.CO2e_total
        / inputs_germany.entries.i_dehst_miner_cement
    )
    p_miner_cement = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="cement",
        co2e_sub_branch=co2e_miner_cement_corrected,
        production_germany_sub_branch=production_germany.p_miner_cement,
    )
    co2e_miner_chalk_corrected = (
        entries.i_dehst_miner_chalk
        * production_germany.p_miner_chalk.CO2e_total
        / inputs_germany.entries.i_dehst_miner_chalk
    )
    p_miner_chalk = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="chalk",
        co2e_sub_branch=co2e_miner_chalk_corrected,
        production_germany_sub_branch=production_germany.p_miner_chalk,
    )
    co2e_miner_glas_corrected = (
        entries.i_dehst_miner_glas
        * production_germany.p_miner_glas.CO2e_total
        / inputs_germany.entries.i_dehst_miner_glas
    )
    p_miner_glas = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="glas",
        co2e_sub_branch=co2e_miner_glas_corrected,
        production_germany_sub_branch=production_germany.p_miner_glas,
    )
    co2e_miner_ceram_corrected = (
        entries.i_dehst_miner_ceram
        * production_germany.p_miner_ceram.CO2e_total
        / inputs_germany.entries.i_dehst_miner_ceram
    )
    p_miner_ceram = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="ceram",
        co2e_sub_branch=co2e_miner_ceram_corrected,
        production_germany_sub_branch=production_germany.p_miner_ceram,
    )
    p_miner = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_miner_cement, p_miner_chalk, p_miner_glas, p_miner_ceram]
    )

    co2e_chem_basic_corrected = (
        entries.i_dehst_chem_basic
        * production_germany.p_chem_basic.CO2e_total
        / inputs_germany.entries.i_dehst_chem_basic
    )
    p_chem_basic = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="chem",
        sub_branch="basic",
        co2e_sub_branch=co2e_chem_basic_corrected,
        production_germany_sub_branch=production_germany.p_chem_basic,
    )
    co2e_chem_ammonia_corrected = (
        entries.i_dehst_chem_ammonia
        * production_germany.p_chem_ammonia.CO2e_total
        / inputs_germany.entries.i_dehst_chem_ammonia
    )
    p_chem_ammonia = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="chem",
        sub_branch="ammonia",
        co2e_sub_branch=co2e_chem_ammonia_corrected,
        production_germany_sub_branch=production_germany.p_chem_ammonia,
    )
    co2e_chem_other_corrected = (
        entries.i_dehst_chem_other
        * production_germany.p_chem_other.CO2e_total
        / inputs_germany.entries.i_dehst_chem_other
    )
    p_chem_other = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="chem",
        sub_branch="other",
        co2e_sub_branch=co2e_chem_other_corrected,
        production_germany_sub_branch=production_germany.p_chem_other,
    )
    p_chem = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_chem_basic, p_chem_ammonia, p_chem_other]
    )

    co2e_metal_steel_primary_corrected = (
        entries.i_dehst_metal_steel_primary
        * production_germany.p_metal_steel_primary.CO2e_total
        / inputs_germany.entries.i_dehst_metal_steel_primary
    )
    p_metal_steel_primary = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_primary",
        co2e_sub_branch=co2e_metal_steel_primary_corrected,
        production_germany_sub_branch=production_germany.p_metal_steel_primary,
    )
    co2e_metal_steel_secondary_corrected = (
        entries.i_dehst_metal_steel_secondary
        * production_germany.p_metal_steel_secondary.CO2e_total
        / inputs_germany.entries.i_dehst_metal_steel_secondary
    )
    p_metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_secondary",
        co2e_sub_branch=co2e_metal_steel_secondary_corrected,
        production_germany_sub_branch=production_germany.p_metal_steel_secondary,
    )
    co2e_metal_nonfe_corrected = (
        entries.i_dehst_metal_nonfe
        * production_germany.p_metal_nonfe.CO2e_total
        / inputs_germany.entries.i_dehst_metal_nonfe
    )
    p_metal_nonfe = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="metal",
        sub_branch="nonfe",
        co2e_sub_branch=co2e_metal_nonfe_corrected,
        production_germany_sub_branch=production_germany.p_metal_nonfe,
    )
    # intermediate result to reuse existing function calc_production_sub_sum
    energy_consumption_metal = (
        p_metal_steel_primary.energy
        + p_metal_steel_secondary.energy
        + p_metal_nonfe.energy
    )
    p_metal_steel = ProductionSubSum.calc_production_sub_sum(
        energy_consumption_branch=energy_consumption_metal,
        sub_branch_list=[p_metal_steel_primary, p_metal_steel_secondary],
    )
    p_metal = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_metal_steel, p_metal_nonfe]
    )

    co2e_other_paper_corrected = (
        entries.i_dehst_other_paper
        * production_germany.p_other_paper.CO2e_total
        / inputs_germany.entries.i_dehst_other_paper
    )
    p_other_paper = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="other",
        sub_branch="paper",
        co2e_sub_branch=co2e_other_paper_corrected,
        production_germany_sub_branch=production_germany.p_other_paper,
    )

    co2e_other_food_corrected = (
        entries.i_dehst_other_food
        * production_germany.p_other_food.CO2e_total
        / inputs_germany.entries.i_dehst_other_food
    )
    p_other_food = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="other",
        sub_branch="food",
        co2e_sub_branch=co2e_other_food_corrected,
        production_germany_sub_branch=production_germany.p_other_food,
    )

    co2e_other_further_corrected = (
        entries.i_dehst_other_further
        * production_germany.p_other_further.CO2e_total
        / inputs_germany.entries.i_dehst_other_further
    )
    p_other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="other",
        sub_branch="further",
        co2e_sub_branch=co2e_other_further_corrected,
        production_germany_sub_branch=production_germany.p_other_further,
    )

    p_other_2efgh = ExtraEmission.calc_extra_emission(
        inputs=inputs,
        branch="other",
        sub_branch="2efgh",
        energy_consumption=p_other_further.energy,
    )
    p_other = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_other_paper, p_other_food],
        sub_branch_via_FEC_list=[p_other_further],
        extra_emission_list=[p_other_2efgh],
    )

    p = ProductionSum.calc_production_sum(
        branch_list=[p_miner, p_chem, p_metal, p_other]
    )

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


def calc_production_by_energy(inputs: Inputs) -> Production:
    fact = inputs.fact
    entries = inputs.entries

    # Calculation was performed in entries
    i_coal_fec = (
        fact("Fact_I_S_coal_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_diesel_fec = (
        fact("Fact_I_S_diesel_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_fueloil_fec = (
        fact("Fact_I_S_fueloil_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_lpg_fec = (
        fact("Fact_I_S_lpg_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_gas_fec = (
        fact("Fact_I_S_gas_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_opetpro_fec = (
        fact("Fact_I_S_opetpro_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_biomass_fec = (
        fact("Fact_I_S_biomass_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_orenew_fec = (
        fact("Fact_I_S_orenew_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_ofossil_fec = (
        fact("Fact_I_S_ofossil_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_elec_fec = (
        fact("Fact_I_S_elec_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )
    i_heatnet_fec = (
        fact("Fact_I_S_heatnet_fec_2018")
        * entries.m_area_industry_com
        / entries.m_area_industry_nat
    )

    i_energy_total = (
        i_coal_fec
        + i_diesel_fec
        + i_fueloil_fec
        + i_lpg_fec
        + i_gas_fec
        + i_opetpro_fec
        + i_biomass_fec
        + i_orenew_fec
        + i_ofossil_fec
        + i_elec_fec
        + i_heatnet_fec
    )

    i_fec_pct_of_miner = fact("Fact_I_P_miner_ratio_fec_to_industry_2018")
    i_fec_pct_of_chem = fact("Fact_I_S_chem_fec_ratio_to_industrie_2018")
    i_fec_pct_of_metal = fact("Fact_I_P_fec_pct_of_metal_2018")
    i_fec_pct_of_other = fact("Fact_I_P_other_ratio_fec_to_industry_2018")

    energy_consumption_industry = i_energy_total

    energy_consumption_miner = energy_consumption_industry * i_fec_pct_of_miner

    p_miner_cement = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="cement",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner_chalk = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="chalk",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner_glas = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="glas",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner_ceram = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="ceram",
        energy_consumption_branch=energy_consumption_miner,
    )
    p_miner = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_miner_cement, p_miner_chalk, p_miner_glas, p_miner_ceram]
    )

    energy_consumption_chemistry = energy_consumption_industry * i_fec_pct_of_chem
    p_chem_basic = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="chem",
        sub_branch="basic",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    p_chem_ammonia = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="chem",
        sub_branch="ammonia",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    p_chem_other = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="chem",
        sub_branch="other",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    p_chem = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_chem_basic, p_chem_ammonia, p_chem_other]
    )

    energy_consumption_metal = energy_consumption_industry * i_fec_pct_of_metal
    energy_consumption_metal_steel = energy_consumption_metal * fact(
        "Fact_I_P_metal_fec_pct_of_steel"
    )
    p_metal_steel_primary = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_primary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    p_metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_secondary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    p_metal_steel = ProductionSubSum.calc_production_sub_sum(
        energy_consumption_branch=energy_consumption_metal,
        sub_branch_list=[p_metal_steel_primary, p_metal_steel_secondary],
    )
    p_metal_nonfe = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="metal",
        sub_branch="nonfe",
        energy_consumption_branch=energy_consumption_metal,
    )
    p_metal = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_metal_steel, p_metal_nonfe]
    )

    energy_consumption_other = energy_consumption_industry * i_fec_pct_of_other
    p_other_paper = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="other",
        sub_branch="paper",
        energy_consumption_branch=energy_consumption_other,
    )
    p_other_food = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="other",
        sub_branch="food",
        energy_consumption_branch=energy_consumption_other,
    )
    p_other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="further",
        energy_consumption_branch=energy_consumption_other,
    )
    p_other_2efgh = ExtraEmission.calc_extra_emission(
        inputs=inputs,
        branch="other",
        sub_branch="2efgh",
        energy_consumption=p_other_further.energy,
    )
    p_other = ProductionBranch.calc_production_sum(
        sub_branch_list=[p_other_paper, p_other_food],
        sub_branch_via_FEC_list=[p_other_further],
        extra_emission_list=[p_other_2efgh],
    )

    p = ProductionSum.calc_production_sum(
        branch_list=[p_miner, p_chem, p_metal, p_other]
    )

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
