# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .production_branches import (
    ExtraEmission,
    ProductionSubBranch,
    ProductionSubBranchCO2viaFEC,
    ProductionBranch,
    ProductionSum,
)


@dataclass(kw_only=True)
class Production:

    total: ProductionSum

    miner: ProductionBranch
    miner_cement: ProductionSubBranch
    miner_chalk: ProductionSubBranch
    miner_glas: ProductionSubBranch
    miner_ceram: ProductionSubBranch

    chem: ProductionBranch
    chem_basic: ProductionSubBranch
    chem_ammonia: ProductionSubBranch
    chem_other: ProductionSubBranch

    metal: ProductionBranch
    metal_steel: ProductionSum
    metal_steel_primary: ProductionSubBranch
    metal_steel_secondary: ProductionSubBranch
    metal_nonfe: ProductionSubBranch

    other: ProductionBranch
    other_paper: ProductionSubBranch
    other_food: ProductionSubBranch
    other_further: ProductionSubBranchCO2viaFEC
    other_2efgh: ExtraEmission


def calc_production_by_co2e(
    inputs: Inputs, inputs_germany: Inputs, production_germany: Production
) -> Production:

    entries = inputs.entries

    co2e_miner_cement_corrected = (
        entries.i_dehst_miner_cement
        * production_germany.miner_cement.CO2e_total
        / inputs_germany.entries.i_dehst_miner_cement
    )
    miner_cement = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="cement",
        co2e_sub_branch=co2e_miner_cement_corrected,
    )
    co2e_miner_chalk_corrected = (
        entries.i_dehst_miner_chalk
        * production_germany.miner_chalk.CO2e_total
        / inputs_germany.entries.i_dehst_miner_chalk
    )
    miner_chalk = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="chalk",
        co2e_sub_branch=co2e_miner_chalk_corrected,
    )
    co2e_miner_glas_corrected = (
        entries.i_dehst_miner_glas
        * production_germany.miner_glas.CO2e_total
        / inputs_germany.entries.i_dehst_miner_glas
    )
    miner_glas = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="glas",
        co2e_sub_branch=co2e_miner_glas_corrected,
    )
    co2e_miner_ceram_corrected = (
        entries.i_dehst_miner_ceram
        * production_germany.miner_ceram.CO2e_total
        / inputs_germany.entries.i_dehst_miner_ceram
    )
    miner_ceram = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="miner",
        sub_branch="ceram",
        co2e_sub_branch=co2e_miner_ceram_corrected,
    )
    miner = ProductionBranch.calc_production_sum(
        sub_branch_list=[miner_cement, miner_chalk, miner_glas, miner_ceram]
    )

    co2e_chem_basic_corrected = (
        entries.i_dehst_chem_basic
        * production_germany.chem_basic.CO2e_total
        / inputs_germany.entries.i_dehst_chem_basic
    )
    chem_basic = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="chem",
        sub_branch="basic",
        co2e_sub_branch=co2e_chem_basic_corrected,
    )
    co2e_chem_ammonia_corrected = (
        entries.i_dehst_chem_ammonia
        * production_germany.chem_ammonia.CO2e_total
        / inputs_germany.entries.i_dehst_chem_ammonia
    )
    chem_ammonia = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="chem",
        sub_branch="ammonia",
        co2e_sub_branch=co2e_chem_ammonia_corrected,
    )
    co2e_chem_other_corrected = (
        entries.i_dehst_chem_other
        * production_germany.chem_other.CO2e_total
        / inputs_germany.entries.i_dehst_chem_other
    )
    chem_other = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="chem",
        sub_branch="other",
        co2e_sub_branch=co2e_chem_other_corrected,
    )
    chem = ProductionBranch.calc_production_sum(
        sub_branch_list=[chem_basic, chem_ammonia, chem_other]
    )

    co2e_metal_steel_primary_corrected = (
        entries.i_dehst_metal_steel_primary
        * production_germany.metal_steel_primary.CO2e_total
        / inputs_germany.entries.i_dehst_metal_steel_primary
    )
    metal_steel_primary = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_primary",
        co2e_sub_branch=co2e_metal_steel_primary_corrected,
    )
    co2e_metal_steel_secondary_corrected = (
        entries.i_dehst_metal_steel_secondary
        * production_germany.metal_steel_secondary.CO2e_total
        / inputs_germany.entries.i_dehst_metal_steel_secondary
    )
    metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_secondary",
        co2e_sub_branch=co2e_metal_steel_secondary_corrected,
    )
    co2e_metal_nonfe_corrected = (
        entries.i_dehst_metal_nonfe
        * production_germany.metal_nonfe.CO2e_total
        / inputs_germany.entries.i_dehst_metal_nonfe
    )
    metal_nonfe = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="metal",
        sub_branch="nonfe",
        co2e_sub_branch=co2e_metal_nonfe_corrected,
    )
    metal_steel = ProductionSum.calc_production_sum(
        metal_steel_primary,
        metal_steel_secondary,
    )
    metal = ProductionBranch.calc_production_sum(
        sub_branch_list=[metal_steel, metal_nonfe]
    )

    co2e_other_paper_corrected = (
        entries.i_dehst_other_paper
        * production_germany.other_paper.CO2e_total
        / inputs_germany.entries.i_dehst_other_paper
    )
    other_paper = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="other",
        sub_branch="paper",
        co2e_sub_branch=co2e_other_paper_corrected,
    )

    co2e_other_food_corrected = (
        entries.i_dehst_other_food
        * production_germany.other_food.CO2e_total
        / inputs_germany.entries.i_dehst_other_food
    )
    other_food = ProductionSubBranch.calc_production_sub_branch_by_co2e(
        inputs=inputs,
        branch="other",
        sub_branch="food",
        co2e_sub_branch=co2e_other_food_corrected,
    )

    # use old logic for calculation by area and energy for other_further and 2efgh
    fact = inputs.fact
    i_energy_total = (
        (
            fact("Fact_I_S_coal_fec_2018")
            + fact("Fact_I_S_diesel_fec_2018")
            + fact("Fact_I_S_fueloil_fec_2018")
            + fact("Fact_I_S_lpg_fec_2018")
            + fact("Fact_I_S_gas_fec_2018")
            + fact("Fact_I_S_opetpro_fec_2018")
            + fact("Fact_I_S_biomass_fec_2018")
            + fact("Fact_I_S_orenew_fec_2018")
            + fact("Fact_I_S_ofossil_fec_2018")
            + fact("Fact_I_S_elec_fec_2018")
            + fact("Fact_I_S_heatnet_fec_2018")
        )
        * inputs.entries.m_area_industry_com
        / inputs.entries.m_area_industry_nat
    )
    energy_consumption_industry = i_energy_total
    i_fec_pct_of_other = fact("Fact_I_P_other_ratio_fec_to_industry_2018")
    energy_consumption_other = energy_consumption_industry * i_fec_pct_of_other
    other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="further",
        energy_consumption_branch=energy_consumption_other,
    )
    other_2efgh = ExtraEmission.calc_extra_emission(
        inputs=inputs,
        branch="other",
        sub_branch="2efgh",
        energy_consumption=other_further.energy,
    )

    other = ProductionBranch.calc_production_sum(
        sub_branch_list=[other_paper, other_food],
        sub_branch_via_FEC_list=[other_further],
        extra_emission_list=[other_2efgh],
    )

    total = ProductionSum.calc_production_sum(miner, chem, metal, other)

    return Production(
        total=total,
        miner=miner,
        miner_cement=miner_cement,
        miner_chalk=miner_chalk,
        miner_glas=miner_glas,
        miner_ceram=miner_ceram,
        chem=chem,
        chem_basic=chem_basic,
        chem_ammonia=chem_ammonia,
        chem_other=chem_other,
        metal=metal,
        metal_steel=metal_steel,
        metal_steel_primary=metal_steel_primary,
        metal_steel_secondary=metal_steel_secondary,
        metal_nonfe=metal_nonfe,
        other=other,
        other_paper=other_paper,
        other_food=other_food,
        other_further=other_further,
        other_2efgh=other_2efgh,
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

    miner_cement = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="cement",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner_chalk = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="chalk",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner_glas = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="glas",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner_ceram = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="miner",
        sub_branch="ceram",
        energy_consumption_branch=energy_consumption_miner,
    )
    miner = ProductionBranch.calc_production_sum(
        sub_branch_list=[miner_cement, miner_chalk, miner_glas, miner_ceram]
    )

    energy_consumption_chemistry = energy_consumption_industry * i_fec_pct_of_chem
    chem_basic = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="chem",
        sub_branch="basic",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    chem_ammonia = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="chem",
        sub_branch="ammonia",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    chem_other = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="chem",
        sub_branch="other",
        energy_consumption_branch=energy_consumption_chemistry,
    )
    chem = ProductionBranch.calc_production_sum(
        sub_branch_list=[chem_basic, chem_ammonia, chem_other]
    )

    energy_consumption_metal = energy_consumption_industry * i_fec_pct_of_metal
    energy_consumption_metal_steel = energy_consumption_metal * fact(
        "Fact_I_P_metal_fec_pct_of_steel"
    )
    metal_steel_primary = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_primary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    metal_steel_secondary = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="metal",
        sub_branch="steel_secondary",
        energy_consumption_branch=energy_consumption_metal_steel,
    )
    metal_steel = ProductionSum.calc_production_sum(
        metal_steel_primary,
        metal_steel_secondary,
    )
    metal_nonfe = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="metal",
        sub_branch="nonfe",
        energy_consumption_branch=energy_consumption_metal,
    )
    metal = ProductionBranch.calc_production_sum(
        sub_branch_list=[metal_steel, metal_nonfe]
    )

    energy_consumption_other = energy_consumption_industry * i_fec_pct_of_other
    other_paper = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="other",
        sub_branch="paper",
        energy_consumption_branch=energy_consumption_other,
    )
    other_food = ProductionSubBranch.calc_production_sub_branch_by_energy(
        inputs=inputs,
        branch="other",
        sub_branch="food",
        energy_consumption_branch=energy_consumption_other,
    )
    other_further = ProductionSubBranchCO2viaFEC.calc_production_sub_branch(
        inputs=inputs,
        branch="other",
        sub_branch="further",
        energy_consumption_branch=energy_consumption_other,
    )
    other_2efgh = ExtraEmission.calc_extra_emission(
        inputs=inputs,
        branch="other",
        sub_branch="2efgh",
        energy_consumption=other_further.energy,
    )
    other = ProductionBranch.calc_production_sum(
        sub_branch_list=[other_paper, other_food],
        sub_branch_via_FEC_list=[other_further],
        extra_emission_list=[other_2efgh],
    )

    total = ProductionSum.calc_production_sum(miner, chem, metal, other)

    return Production(
        total=total,
        miner=miner,
        miner_cement=miner_cement,
        miner_chalk=miner_chalk,
        miner_glas=miner_glas,
        miner_ceram=miner_ceram,
        chem=chem,
        chem_basic=chem_basic,
        chem_ammonia=chem_ammonia,
        chem_other=chem_other,
        metal=metal,
        metal_steel=metal_steel,
        metal_steel_primary=metal_steel_primary,
        metal_steel_secondary=metal_steel_secondary,
        metal_nonfe=metal_nonfe,
        other=other,
        other_paper=other_paper,
        other_food=other_food,
        other_further=other_further,
        other_2efgh=other_2efgh,
    )
