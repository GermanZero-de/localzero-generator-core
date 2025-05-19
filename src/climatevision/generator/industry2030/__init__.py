"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/industry.html
"""

# pyright: strict

from ..industry2018.i18 import I18
from ..makeentries import Entries
from ..refdata import Assumptions, Facts
from ..utils import div
from . import energy_general
from .dataclasses import (
    Vars2,
    Vars3,
    Vars4,
    Vars5,
    Vars6,
    Vars7,
    Vars8,
    Vars9,
    Vars10,
    Vars11,
    Vars12,
    Vars13,
    Vars14,
    Vars15,
    Vars16,
)
from .i30 import I30


def calc(entries: Entries, facts: Facts, assumptions: Assumptions, *, i18: I18) -> I30:
    fact = facts.fact
    ass = assumptions.ass

    duration_until_target_year = entries.m_duration_target
    duration_CO2e_neutral_years = entries.m_duration_neutral

    population_commune_2018 = entries.m_population_com_2018
    population_germany_2018 = entries.m_population_nat

    i = Vars2()

    # p_chem_basic
    p_chem_basic = Vars5()

    p_chem_basic.demand_change = ass("Ass_I_P_chem_basic_wo_ammonia_prodvol_change")
    p_chem_basic.prod_volume = i18.p_chem_basic.prod_volume * (
        1 + p_chem_basic.demand_change
    )
    p_chem_basic.demand_electricity = p_chem_basic.prod_volume * ass(
        "Ass_I_P_chem_basic_wo_ammonia_fec_factor_electricity_2050"
    )
    p_chem_basic.demand_emethan = p_chem_basic.prod_volume * ass(
        "Ass_I_P_chem_basic_wo_ammonia_fec_factor_other_energie_2050"
    )
    p_chem_basic.energy = p_chem_basic.demand_electricity + p_chem_basic.demand_emethan

    p_chem_basic.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_chem_basic_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_chem_basic.CO2e_combustion_based = (
        p_chem_basic.prod_volume * p_chem_basic.CO2e_combustion_based_per_t
    )
    p_chem_basic.CO2e_production_based = ass("Ass_I_P_chem_all_co2e_factor_2050")
    p_chem_basic.CO2e_total = (
        p_chem_basic.CO2e_combustion_based + p_chem_basic.CO2e_production_based
    )
    p_chem_basic.change_energy_MWh = p_chem_basic.energy - i18.p_chem_basic.energy
    p_chem_basic.change_energy_pct = div(
        p_chem_basic.change_energy_MWh, i18.p_chem_basic.energy
    )
    p_chem_basic.change_CO2e_t = p_chem_basic.CO2e_total - i18.p_chem_basic.CO2e_total
    p_chem_basic.change_CO2e_pct = div(
        p_chem_basic.change_CO2e_t, i18.p_chem_basic.CO2e_total
    )
    p_chem_basic.CO2e_total_2021_estimated = i18.p_chem_basic.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_chem_basic.cost_climate_saved = (
        (p_chem_basic.CO2e_total_2021_estimated - p_chem_basic.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # investment calculation
    p_chem_basic.invest_per_x = ass(
        "Ass_I_P_chem_basic_wo_ammonia_factor_invest_per_prodvol_2050"
    )
    p_chem_basic.invest = p_chem_basic.invest_per_x * p_chem_basic.prod_volume
    p_chem_basic.invest_outside = p_chem_basic.invest
    p_chem_basic.invest_pa = p_chem_basic.invest / duration_until_target_year
    p_chem_basic.invest_pa_outside = p_chem_basic.invest_pa
    p_chem_basic.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_chem_basic.cost_wage = p_chem_basic.invest_pa * p_chem_basic.pct_of_wage
    p_chem_basic.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_chem_basic.demand_emplo = div(
        p_chem_basic.cost_wage, p_chem_basic.ratio_wage_to_emplo
    )

    # p_chem_ammonia
    p_chem_ammonia = Vars6()
    p_chem_ammonia.prod_volume = i18.p_chem_ammonia.prod_volume
    p_chem_ammonia.demand_electricity = p_chem_ammonia.prod_volume * ass(
        "Ass_I_P_chem_ammonia_fec_factor_electricity_2050"
    )
    p_chem_ammonia.energy = p_chem_ammonia.demand_electricity
    p_chem_ammonia.CO2e_combustion_based = ass("Ass_I_P_chem_all_co2e_factor_2050")
    p_chem_ammonia.CO2e_production_based = ass("Ass_I_P_chem_all_co2e_factor_2050")
    p_chem_ammonia.CO2e_total = (
        p_chem_ammonia.CO2e_combustion_based + p_chem_ammonia.CO2e_production_based
    )
    p_chem_ammonia.change_energy_MWh = p_chem_ammonia.energy - i18.p_chem_ammonia.energy
    p_chem_ammonia.change_energy_pct = div(
        p_chem_ammonia.change_energy_MWh, i18.p_chem_ammonia.energy
    )
    p_chem_ammonia.change_CO2e_t = (
        p_chem_ammonia.CO2e_total - i18.p_chem_ammonia.CO2e_total
    )
    p_chem_ammonia.change_CO2e_pct = div(
        p_chem_ammonia.change_CO2e_t, i18.p_chem_ammonia.CO2e_total
    )
    p_chem_ammonia.CO2e_total_2021_estimated = i18.p_chem_ammonia.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_chem_ammonia.cost_climate_saved = (
        (p_chem_ammonia.CO2e_total_2021_estimated - p_chem_ammonia.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # investment calculation
    p_chem_ammonia.invest_per_x = ass(
        "Ass_I_P_chem_ammonia_factor_invest_per_prodvol_2050"
    )
    p_chem_ammonia.invest = p_chem_ammonia.invest_per_x * p_chem_ammonia.prod_volume
    p_chem_ammonia.invest_outside = p_chem_ammonia.invest
    p_chem_ammonia.invest_pa = p_chem_ammonia.invest / duration_until_target_year
    p_chem_ammonia.invest_pa_outside = p_chem_ammonia.invest_pa
    p_chem_ammonia.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_chem_ammonia.cost_wage = p_chem_ammonia.invest_pa * p_chem_ammonia.pct_of_wage
    p_chem_ammonia.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_chem_ammonia.demand_emplo = div(
        p_chem_ammonia.cost_wage, p_chem_ammonia.ratio_wage_to_emplo
    )

    # p chem other
    p_chem_other = Vars5()
    p_chem_other.prod_volume = i18.p_chem_other.prod_volume
    p_chem_other.demand_electricity = p_chem_other.prod_volume * ass(
        "Ass_I_P_chem_other_fec_factor_electricity_2050"
    )
    p_chem_other.demand_emethan = p_chem_other.prod_volume * ass(
        "Ass_I_P_chem_other_fec_factor_other_energie_2050"
    )
    p_chem_other.energy = p_chem_other.demand_electricity + p_chem_other.demand_emethan
    p_chem_other.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_chem_other_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_chem_other.CO2e_combustion_based = (
        p_chem_other.prod_volume * p_chem_other.CO2e_combustion_based_per_t
    )
    p_chem_other.CO2e_production_based = ass("Ass_I_P_chem_all_co2e_factor_2050")
    p_chem_other.CO2e_total = (
        p_chem_other.CO2e_combustion_based + p_chem_other.CO2e_production_based
    )
    # change 2018 to 203X
    p_chem_other.change_energy_MWh = p_chem_other.energy - i18.p_chem_other.energy
    p_chem_other.change_energy_pct = div(
        p_chem_other.change_energy_MWh, i18.p_chem_other.energy
    )
    p_chem_other.change_CO2e_t = p_chem_other.CO2e_total - i18.p_chem_other.CO2e_total
    p_chem_other.change_CO2e_pct = div(
        p_chem_other.change_CO2e_t, i18.p_chem_other.CO2e_total
    )
    p_chem_other.CO2e_total_2021_estimated = i18.p_chem_other.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_chem_other.cost_climate_saved = (
        (p_chem_other.CO2e_total_2021_estimated - p_chem_other.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # investment calculation
    p_chem_other.invest_per_x = ass("Ass_I_P_chem_other_factor_invest_per_prodvol_2050")
    p_chem_other.invest = p_chem_other.invest_per_x * p_chem_other.prod_volume
    p_chem_other.invest_outside = p_chem_other.invest
    p_chem_other.invest_pa = p_chem_other.invest / duration_until_target_year
    p_chem_other.invest_pa_outside = p_chem_other.invest_pa
    p_chem_other.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_chem_other.cost_wage = p_chem_other.invest_pa * p_chem_other.pct_of_wage
    p_chem_other.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_chem_other.demand_emplo = div(
        p_chem_other.cost_wage, p_chem_other.ratio_wage_to_emplo
    )

    # chem total
    p_chem = Vars8()
    p_chem.energy = p_chem_basic.energy + p_chem_ammonia.energy + p_chem_other.energy
    p_chem.prod_volume = (
        p_chem_basic.prod_volume + p_chem_ammonia.prod_volume + p_chem_other.prod_volume
    )
    p_chem.CO2e_production_based = (
        p_chem_basic.CO2e_production_based
        + p_chem_ammonia.CO2e_production_based
        + p_chem_other.CO2e_production_based
    )
    p_chem.CO2e_combustion_based = (
        p_chem_basic.CO2e_combustion_based
        + p_chem_ammonia.CO2e_combustion_based
        + p_chem_other.CO2e_combustion_based
    )
    p_chem.CO2e_total = (
        p_chem_basic.CO2e_total + p_chem_ammonia.CO2e_total + p_chem_other.CO2e_total
    )
    # 2018 to 203X
    p_chem.change_energy_MWh = (
        p_chem_basic.change_energy_MWh
        + p_chem_ammonia.change_energy_MWh
        + p_chem_other.change_energy_MWh
    )
    p_chem.change_energy_pct = div(p_chem.change_energy_MWh, i18.p_chem.energy)
    p_chem.change_CO2e_t = (
        p_chem_basic.change_CO2e_t
        + p_chem_ammonia.change_CO2e_t
        + p_chem_other.change_CO2e_t
    )
    p_chem.change_CO2e_pct = div(p_chem.change_CO2e_t, i18.p_chem.CO2e_total)
    p_chem.CO2e_total_2021_estimated = (
        p_chem_basic.CO2e_total_2021_estimated
        + p_chem_ammonia.CO2e_total_2021_estimated
        + p_chem_other.CO2e_total_2021_estimated
    )
    p_chem.cost_climate_saved = (
        p_chem_basic.cost_climate_saved
        + p_chem_ammonia.cost_climate_saved
        + p_chem_other.cost_climate_saved
    )
    p_chem.invest = p_chem_basic.invest + p_chem_ammonia.invest + p_chem_other.invest
    p_chem.demand_emplo = (
        p_chem_basic.demand_emplo
        + p_chem_ammonia.demand_emplo
        + p_chem_other.demand_emplo
    )

    # metal -------------------------------------------------------------------------
    # p_metal_steel_primary
    p_metal_steel_primary = Vars11()
    p_metal_steel_primary.demand_change = ass(
        "Ass_I_P_metal_steel_primary_prodvol_change_2050"
    )
    p_metal_steel_primary.prod_volume = i18.p_metal_steel_primary.prod_volume * (
        1 + p_metal_steel_primary.demand_change
    )
    p_metal_steel_primary.demand_electricity = p_metal_steel_primary.prod_volume * (
        ass("Ass_I_P_metal_steel_primary_ratio_fec_to_prodvol_electricity_2030")
        + ass(
            "Ass_I_P_metal_steel_further_processing_ratio_fec_to_prodvol_electricity_2030"
        )
    )
    p_metal_steel_primary.demand_hydrogen = p_metal_steel_primary.prod_volume * ass(
        "Ass_I_P_metal_steel_primary_ratio_fec_to_prodvol_hydrogen_2030"
    )
    p_metal_steel_primary.energy = (
        p_metal_steel_primary.demand_electricity + p_metal_steel_primary.demand_hydrogen
    )
    # CO2 Emissions
    p_metal_steel_primary.CO2e_production_based_per_t = ass(
        "Ass_I_P_metal_steel_primary_ratio_CO2e_pb_to_rodvol_2030"
    )
    p_metal_steel_primary.CO2e_production_based = (
        p_metal_steel_primary.prod_volume
        * p_metal_steel_primary.CO2e_production_based_per_t
    )
    p_metal_steel_primary.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_metal_steel_primary_ratio_CO2e_eb_to_rodvol_2030"
    ) + ass("Ass_I_P_metal_steel_further_production_ratio_CO2e_eb_to_rodvol_2030")
    p_metal_steel_primary.CO2e_combustion_based = (
        p_metal_steel_primary.prod_volume
        * p_metal_steel_primary.CO2e_combustion_based_per_t
    )
    p_metal_steel_primary.CO2e_total = (
        p_metal_steel_primary.CO2e_production_based
        + p_metal_steel_primary.CO2e_combustion_based
    )

    # change 2018 to 203X
    p_metal_steel_primary.change_energy_MWh = (
        p_metal_steel_primary.energy - i18.p_metal_steel_primary.energy
    )
    p_metal_steel_primary.change_energy_pct = div(
        p_metal_steel_primary.change_energy_MWh, i18.p_metal_steel_primary.energy
    )
    p_metal_steel_primary.change_CO2e_t = (
        p_metal_steel_primary.CO2e_total - i18.p_metal_steel_primary.CO2e_total
    )
    p_metal_steel_primary.change_CO2e_pct = div(
        p_metal_steel_primary.change_CO2e_t, i18.p_metal_steel_primary.CO2e_total
    )
    p_metal_steel_primary.CO2e_total_2021_estimated = (
        i18.p_metal_steel_primary.CO2e_total
        * fact(f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref")
    )
    p_metal_steel_primary.cost_climate_saved = (
        (
            p_metal_steel_primary.CO2e_total_2021_estimated
            - p_metal_steel_primary.CO2e_total
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # investment calculation
    p_metal_steel_primary.invest_per_x = ass(
        "Ass_I_P_metal_steel_primary_eaf_ratio_invest_to_prodvol_2019"
    )
    p_metal_steel_primary.invest = (
        p_metal_steel_primary.invest_per_x * p_metal_steel_primary.prod_volume
    )
    p_metal_steel_primary.invest_outside = p_metal_steel_primary.invest
    p_metal_steel_primary.invest_pa = (
        p_metal_steel_primary.invest / duration_until_target_year
    )
    p_metal_steel_primary.invest_pa_outside = p_metal_steel_primary.invest_pa
    p_metal_steel_primary.pct_of_wage = fact(
        "Fact_I_P_constr_civil_revenue_pct_of_wage_2018"
    )
    p_metal_steel_primary.cost_wage = (
        p_metal_steel_primary.invest_pa * p_metal_steel_primary.pct_of_wage
    )
    p_metal_steel_primary.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_metal_steel_primary.demand_emplo = div(
        p_metal_steel_primary.cost_wage, p_metal_steel_primary.ratio_wage_to_emplo
    )

    # p_metal_steel_secondary
    p_metal_steel_secondary = Vars6()

    p_metal_steel_secondary.demand_change = ass(
        "Ass_I_P_metal_steel_secondary_prodvol_change_2050"
    )
    p_metal_steel_secondary.prod_volume = i18.p_metal_steel_secondary.prod_volume * (
        1 + p_metal_steel_secondary.demand_change
    )
    p_metal_steel_secondary.demand_electricity = p_metal_steel_secondary.prod_volume * (
        ass("Ass_I_P_metal_steel_secondary_ratio_fec_to_prodvol_electricity_2030")
        + ass(
            "Ass_I_P_metal_steel_further_processing_ratio_fec_to_prodvol_electricity_2030"
        )
    )
    p_metal_steel_secondary.energy = p_metal_steel_secondary.demand_electricity
    # CO2 Emissions
    p_metal_steel_secondary.CO2e_production_based_per_t = ass(
        "Ass_I_P_metal_steel_secundary_ratio_CO2e_pb_to_rodvol_2030"
    )
    p_metal_steel_secondary.CO2e_production_based = (
        p_metal_steel_secondary.prod_volume
        * p_metal_steel_secondary.CO2e_production_based_per_t
    )
    p_metal_steel_secondary.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_metal_steel_secundary_ratio_CO2e_eb_to_rodvol_2030"
    ) + ass("Ass_I_P_metal_steel_further_production_ratio_CO2e_eb_to_rodvol_2030")
    p_metal_steel_secondary.CO2e_combustion_based = (
        p_metal_steel_secondary.prod_volume
        * p_metal_steel_secondary.CO2e_combustion_based_per_t
    )
    p_metal_steel_secondary.CO2e_total = (
        p_metal_steel_secondary.CO2e_production_based
        + p_metal_steel_secondary.CO2e_combustion_based
    )

    # change 2018 to 203X
    p_metal_steel_secondary.change_energy_MWh = (
        p_metal_steel_secondary.energy - i18.p_metal_steel_secondary.energy
    )
    p_metal_steel_secondary.change_energy_pct = div(
        p_metal_steel_secondary.change_energy_MWh, i18.p_metal_steel_secondary.energy
    )
    p_metal_steel_secondary.change_CO2e_t = (
        p_metal_steel_secondary.CO2e_production_based
        + p_metal_steel_secondary.CO2e_combustion_based
    ) - (
        i18.p_metal_steel_secondary.CO2e_production_based
        + i18.p_metal_steel_secondary.CO2e_combustion_based
    )
    p_metal_steel_secondary.change_CO2e_pct = div(
        p_metal_steel_secondary.change_CO2e_t, i18.p_metal_steel_secondary.CO2e_total
    )
    p_metal_steel_secondary.CO2e_total_2021_estimated = (
        i18.p_metal_steel_secondary.CO2e_total
        * fact(f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref")
    )
    p_metal_steel_secondary.cost_climate_saved = (
        (
            p_metal_steel_secondary.CO2e_total_2021_estimated
            - p_metal_steel_secondary.CO2e_total
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # investment calculation
    p_metal_steel_secondary.invest_per_x = ass(
        "Ass_I_P_metal_steel_secondary_ratio_invest_to_prodvol_2018"
    )
    p_metal_steel_secondary.invest = (
        p_metal_steel_secondary.invest_per_x * p_metal_steel_secondary.prod_volume
    )
    p_metal_steel_secondary.invest_outside = p_metal_steel_secondary.invest
    p_metal_steel_secondary.invest_pa = (
        p_metal_steel_secondary.invest / duration_until_target_year
    )
    p_metal_steel_secondary.invest_pa_outside = p_metal_steel_secondary.invest_pa
    p_metal_steel_secondary.pct_of_wage = fact(
        "Fact_I_P_constr_civil_revenue_pct_of_wage_2018"
    )
    p_metal_steel_secondary.cost_wage = (
        p_metal_steel_secondary.invest_pa * p_metal_steel_secondary.pct_of_wage
    )
    p_metal_steel_secondary.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_metal_steel_secondary.demand_emplo = div(
        p_metal_steel_secondary.cost_wage, p_metal_steel_secondary.ratio_wage_to_emplo
    )

    # metal steel
    p_metal_steel = Vars10()
    p_metal_steel.energy = p_metal_steel_primary.energy + p_metal_steel_secondary.energy
    p_metal_steel.prod_volume = (
        p_metal_steel_primary.prod_volume + p_metal_steel_secondary.prod_volume
    )
    p_metal_steel.CO2e_production_based = (
        p_metal_steel_primary.CO2e_production_based
        + p_metal_steel_secondary.CO2e_production_based
    )
    p_metal_steel.CO2e_combustion_based = (
        p_metal_steel_primary.CO2e_combustion_based
        + p_metal_steel_secondary.CO2e_combustion_based
    )
    p_metal_steel.CO2e_total = (
        p_metal_steel.CO2e_production_based + p_metal_steel.CO2e_combustion_based
    )

    # change 2018 to 203X
    p_metal_steel.change_energy_MWh = p_metal_steel.energy - i18.p_metal_steel.energy
    p_metal_steel.change_energy_pct = div(
        p_metal_steel.change_energy_MWh, i18.p_metal_steel.energy
    )
    p_metal_steel.change_CO2e_t = (
        p_metal_steel.CO2e_total - i18.p_metal_steel.CO2e_total
    )
    p_metal_steel.change_CO2e_pct = div(
        p_metal_steel.change_CO2e_t, i18.p_metal_steel.CO2e_total
    )
    p_metal_steel.CO2e_total_2021_estimated = i18.p_metal_steel.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_metal_steel.cost_climate_saved = (
        (p_metal_steel.CO2e_total_2021_estimated - p_metal_steel.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_metal_steel.invest_pa = (
        p_metal_steel_primary.invest_pa + p_metal_steel_secondary.invest_pa
    )
    p_metal_steel.invest_pa_outside = p_metal_steel.invest_pa
    p_metal_steel.invest = p_metal_steel_primary.invest + p_metal_steel_secondary.invest
    p_metal_steel.invest_outside = p_metal_steel.invest
    p_metal_steel.demand_emplo = (
        p_metal_steel_primary.demand_emplo + p_metal_steel_secondary.demand_emplo
    )

    # non fe metals
    p_metal_nonfe = Vars7()
    p_metal_nonfe.demand_change = ass("Ass_I_P_metal_nonfe_prodvol_change")
    p_metal_nonfe.prod_volume = i18.p_metal_nonfe.prod_volume * (
        1 + p_metal_nonfe.demand_change
    )
    p_metal_nonfe.demand_electricity = p_metal_nonfe.prod_volume * ass(
        "Ass_I_P_metal_nonfe_ratio_fec_to_prodvol_electricity_2035"
    )
    p_metal_nonfe.demand_biomass = p_metal_nonfe.prod_volume * ass(
        "Ass_I_P_metal_nonfe_ratio_fec_to_prodvol_biomass_2035"
    )
    p_metal_nonfe.demand_hydrogen = p_metal_nonfe.prod_volume * ass(
        "Ass_I_P_metal_nonfe_ratio_fec_to_prodvol_hydrogen_2035"
    )
    p_metal_nonfe.energy = (
        p_metal_nonfe.demand_electricity
        + p_metal_nonfe.demand_biomass
        + p_metal_nonfe.demand_hydrogen
    )
    # CO2 Emissions
    p_metal_nonfe.CO2e_production_based_per_t = ass("Ass_I_P_metal_nonfe_CO2e_pb_2035")
    p_metal_nonfe.CO2e_production_based = (
        p_metal_nonfe.prod_volume * p_metal_nonfe.CO2e_production_based_per_t
    )
    p_metal_nonfe.CO2e_combustion_based_per_t = ass("Ass_I_P_metal_nonfe_CO2e_cb_2035")
    p_metal_nonfe.CO2e_combustion_based = (
        p_metal_nonfe.prod_volume * p_metal_nonfe.CO2e_combustion_based_per_t
    )
    p_metal_nonfe.CO2e_total = (
        p_metal_nonfe.CO2e_production_based + p_metal_nonfe.CO2e_combustion_based
    )

    # change 2018 to 203X
    p_metal_nonfe.change_energy_MWh = p_metal_nonfe.energy - i18.p_metal_nonfe.energy
    p_metal_nonfe.change_energy_pct = div(
        p_metal_nonfe.change_energy_MWh, i18.p_metal_nonfe.energy
    )
    p_metal_nonfe.change_CO2e_t = (
        p_metal_nonfe.CO2e_total - i18.p_metal_nonfe.CO2e_total
    )
    p_metal_nonfe.change_CO2e_pct = div(
        p_metal_nonfe.change_CO2e_t, i18.p_metal_nonfe.CO2e_total
    )
    p_metal_nonfe.CO2e_total_2021_estimated = i18.p_metal_nonfe.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_metal_nonfe.cost_climate_saved = (
        (p_metal_nonfe.CO2e_total_2021_estimated - p_metal_nonfe.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # investment calculation
    p_metal_nonfe.invest_per_x = ass(
        "Ass_I_P_metal_nonfe_alrecycl_ratio_invest_to_prodvol_2013"
    )
    p_metal_nonfe.invest = p_metal_nonfe.invest_per_x * p_metal_nonfe.prod_volume
    p_metal_nonfe.invest_outside = p_metal_nonfe.invest
    p_metal_nonfe.invest_pa = p_metal_nonfe.invest / duration_until_target_year
    p_metal_nonfe.invest_pa_outside = p_metal_nonfe.invest_pa
    p_metal_nonfe.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_metal_nonfe.cost_wage = p_metal_nonfe.invest_pa * p_metal_nonfe.pct_of_wage
    p_metal_nonfe.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_metal_nonfe.demand_emplo = div(
        p_metal_nonfe.cost_wage, p_metal_nonfe.ratio_wage_to_emplo
    )

    # metal summary
    p_metal = Vars9()
    p_metal.energy = p_metal_steel.energy + p_metal_nonfe.energy
    p_metal.CO2e_production_based = (
        p_metal_steel.CO2e_production_based + p_metal_nonfe.CO2e_production_based
    )
    p_metal.CO2e_combustion_based = (
        p_metal_steel.CO2e_combustion_based + p_metal_nonfe.CO2e_combustion_based
    )
    p_metal.CO2e_total = p_metal_steel.CO2e_total + p_metal_nonfe.CO2e_total
    p_metal.change_energy_MWh = (
        p_metal_steel.change_energy_MWh + p_metal_nonfe.change_energy_MWh
    )
    p_metal.change_energy_pct = div(p_metal.change_energy_MWh, i18.p_metal.energy)
    p_metal.change_CO2e_t = p_metal_steel.change_CO2e_t + p_metal_nonfe.change_CO2e_t
    p_metal.change_CO2e_pct = div(p_metal.change_CO2e_t, i18.p_metal.CO2e_total)
    p_metal.CO2e_total_2021_estimated = (
        p_metal_steel.CO2e_total_2021_estimated
        + p_metal_nonfe.CO2e_total_2021_estimated
    )
    p_metal.cost_climate_saved = (
        p_metal_steel.cost_climate_saved + p_metal_nonfe.cost_climate_saved
    )
    p_metal.invest = p_metal_steel.invest + p_metal_nonfe.invest
    p_metal.demand_emplo = p_metal_steel.demand_emplo + p_metal_nonfe.demand_emplo

    # p_other_paper
    p_other_paper = Vars13()
    p_other_paper.demand_change = ass("Ass_I_P_other_paper_prodvol_change")
    p_other_paper.prod_volume = i18.p_other_paper.prod_volume * (
        1 + p_other_paper.demand_change
    )
    p_other_paper.demand_electricity = p_other_paper.prod_volume * ass(
        "Ass_I_P_other_paper_ratio_fec_elec_to_prodvol_2050"
    )
    p_other_paper.demand_heatnet = p_other_paper.prod_volume * ass(
        "Ass_I_P_other_paper_ratio_fec_heatnet_to_prodvol_2050"
    )
    p_other_paper.energy = (
        p_other_paper.demand_electricity + p_other_paper.demand_heatnet
    )
    p_other_paper.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_other_paper_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_other_paper.CO2e_combustion_based = (
        p_other_paper.prod_volume * p_other_paper.CO2e_combustion_based_per_t
    )
    p_other_paper.CO2e_total = p_other_paper.CO2e_combustion_based

    # change 2018 to 203X
    p_other_paper.change_energy_MWh = p_other_paper.energy - i18.p_other_paper.energy
    p_other_paper.change_energy_pct = div(
        p_other_paper.change_energy_MWh, i18.p_other_paper.energy
    )
    p_other_paper.change_CO2e_t = (
        p_other_paper.CO2e_total - i18.p_other_paper.CO2e_total
    )
    p_other_paper.change_CO2e_pct = div(
        p_other_paper.change_CO2e_t, i18.p_other_paper.CO2e_total
    )
    p_other_paper.CO2e_total_2021_estimated = i18.p_other_paper.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_other_paper.cost_climate_saved = (
        (p_other_paper.CO2e_total_2021_estimated - p_other_paper.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    # investment calculation
    p_other_paper.invest_per_x = ass(
        "Ass_I_P_other_paper_varel_ratio_invest_to_prodvol_2019"
    )
    p_other_paper.invest = p_other_paper.invest_per_x * p_other_paper.prod_volume
    p_other_paper.invest_outside = p_other_paper.invest
    p_other_paper.invest_pa = p_other_paper.invest / duration_until_target_year
    p_other_paper.invest_pa_outside = p_other_paper.invest_pa
    p_other_paper.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_other_paper.cost_wage = p_other_paper.invest_pa * p_other_paper.pct_of_wage
    p_other_paper.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_other_paper.demand_emplo = div(
        p_other_paper.cost_wage, p_other_paper.ratio_wage_to_emplo
    )

    # p_other_food
    p_other_food = Vars13()
    p_other_food.demand_change = ass("Ass_I_P_other_food_prodvol_change")
    p_other_food.prod_volume = i18.p_other_food.prod_volume * (
        1 + p_other_food.demand_change
    )
    p_other_food.demand_electricity = p_other_food.prod_volume * ass(
        "Ass_I_P_other_food_ratio_fec_elec_to_prodvol_2050"
    )
    p_other_food.demand_heatnet = p_other_food.prod_volume * ass(
        "Ass_I_P_other_food_ratio_fec_heatnet_to_prodvol_2050"
    )
    p_other_food.energy = p_other_food.demand_electricity + p_other_food.demand_heatnet

    p_other_food.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_other_food_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_other_food.CO2e_combustion_based = (
        p_other_food.prod_volume * p_other_food.CO2e_combustion_based_per_t
    )
    p_other_food.CO2e_total = p_other_food.CO2e_combustion_based

    # change 2018 to 203X
    p_other_food.change_energy_MWh = p_other_food.energy - i18.p_other_food.energy
    p_other_food.change_energy_pct = div(
        p_other_food.change_energy_MWh, i18.p_other_food.energy
    )
    p_other_food.change_CO2e_t = p_other_food.CO2e_total - i18.p_other_food.CO2e_total
    p_other_food.change_CO2e_pct = div(
        p_other_food.change_CO2e_t, i18.p_other_food.CO2e_total
    )
    p_other_food.CO2e_total_2021_estimated = i18.p_other_food.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_other_food.cost_climate_saved = (
        (p_other_food.CO2e_total_2021_estimated - p_other_food.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    # investment calculation
    p_other_food.invest_per_x = ass(
        "Ass_I_P_other_food_coke_ratio_invest_to_prodvol_2019"
    )
    p_other_food.invest = p_other_food.invest_per_x * p_other_food.prod_volume
    p_other_food.invest_pa = p_other_food.invest / duration_until_target_year
    p_other_food.invest_pa_outside = p_other_food.invest_pa
    p_other_food.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_other_food.cost_wage = p_other_food.invest_pa * p_other_food.pct_of_wage
    p_other_food.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_other_food.demand_emplo = div(
        p_other_food.cost_wage, p_other_food.ratio_wage_to_emplo
    )

    # p_other_futther_2030
    p_other_further = Vars14()
    p_other_further.prod_volume = ass("Ass_I_P_other_further_prodvol_2050")
    p_other_further.demand_change = ass("Ass_I_P_other_further_fec_change")
    p_other_further.energy = i18.p_other_further.energy * (
        1 + p_other_further.demand_change
    )
    p_other_further.demand_electricity = p_other_further.energy * ass(
        "Ass_I_P_other_further_fec_pct_of_elec_2050"
    )
    p_other_further.demand_heatnet = p_other_further.energy * ass(
        "Ass_I_P_other_further_fec_pct_of_heatnet_2050"
    )
    p_other_further.CO2e_production_based_per_MWh = ass(
        "Ass_I_P_other_2d_ratio_of_CO2e_pb_to_fec_2050"
    )
    p_other_further.CO2e_production_based = (
        p_other_further.energy * p_other_further.CO2e_production_based_per_MWh
    )
    p_other_further.CO2e_combustion_based_per_MWh = ass(
        "Ass_I_P_other_further_ratio_of_CO2e_cb_to_fec_2050"
    )
    p_other_further.CO2e_combustion_based = (
        p_other_further.energy * p_other_further.CO2e_combustion_based_per_MWh
    )
    p_other_further.CO2e_total = (
        p_other_further.CO2e_combustion_based + p_other_further.CO2e_production_based
    )

    # change 2018 to 203X
    p_other_further.change_energy_MWh = (
        p_other_further.energy - i18.p_other_further.energy
    )
    p_other_further.change_energy_pct = div(
        p_other_further.change_energy_MWh, i18.p_other_further.energy
    )
    p_other_further.change_CO2e_t = (
        p_other_further.CO2e_total - i18.p_other_further.CO2e_total
    )
    p_other_further.change_CO2e_pct = div(
        p_other_further.change_CO2e_t, i18.p_other_further.CO2e_total
    )
    p_other_further.CO2e_total_2021_estimated = i18.p_other_further.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_other_further.cost_climate_saved = (
        (p_other_further.CO2e_total_2021_estimated - p_other_further.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    # investment calculation
    p_other_further.invest_per_x = ass(
        "Ass_I_P_other_further_boiler_ratio_invest_to_fec_2050"
    )
    p_other_further.invest = p_other_further.energy * p_other_further.invest_per_x
    p_other_further.invest_pa = p_other_further.invest / duration_until_target_year
    p_other_further.invest_pa_outside = p_other_further.invest_pa
    p_other_further.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_other_further.cost_wage = p_other_further.invest_pa * p_other_further.pct_of_wage
    p_other_further.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_other_further.demand_emplo = div(
        p_other_further.cost_wage, p_other_further.ratio_wage_to_emplo
    )

    # has to be calculatet after p_other_further_2030
    # p_other_2efgh
    p_other_2efgh = Vars15()
    p_other_2efgh.CO2e_production_based_per_MWh = ass(
        "Ass_I_P_other_2efgh_ratio_of_CO2e_pb_to_fec_2050"
    )
    p_other_2efgh.CO2e_production_based = (
        p_other_further.energy * p_other_2efgh.CO2e_production_based_per_MWh
    )
    p_other_2efgh.CO2e_total = p_other_2efgh.CO2e_production_based

    # change 2018 to 203X
    p_other_2efgh.change_CO2e_t = (
        p_other_2efgh.CO2e_total - i18.p_other_2efgh.CO2e_total
    )
    p_other_2efgh.change_CO2e_pct = div(
        p_other_2efgh.change_CO2e_t, i18.p_other_2efgh.CO2e_total
    )
    p_other_2efgh.CO2e_total_2021_estimated = i18.p_other_2efgh.CO2e_total * fact(
        f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref"
    )
    p_other_2efgh.cost_climate_saved = (
        (p_other_2efgh.CO2e_total_2021_estimated - p_other_2efgh.CO2e_total)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    # investment calculation
    p_other_2efgh.invest_per_x = ass(
        "Ass_I_P_other_further_cooling_ratio_invest_to_CO2e_2050"
    )

    p_other_2efgh.invest = (
        i18.p_other_2efgh.CO2e_production_based - p_other_2efgh.CO2e_production_based
    ) * p_other_2efgh.invest_per_x
    p_other_2efgh.invest_pa = p_other_2efgh.invest / duration_until_target_year
    p_other_2efgh.invest_pa_outside = p_other_2efgh.invest_pa
    p_other_2efgh.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_other_2efgh.cost_wage = p_other_2efgh.invest_pa * p_other_2efgh.pct_of_wage
    p_other_2efgh.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_other_2efgh.demand_emplo = div(
        p_other_2efgh.cost_wage, p_other_2efgh.ratio_wage_to_emplo
    )

    # sum other industries
    p_other = Vars12()
    p_other.energy = p_other_paper.energy + p_other_food.energy + p_other_further.energy
    p_other.prod_volume = p_other_paper.prod_volume + p_other_food.prod_volume
    p_other.CO2e_production_based = (
        p_other_further.CO2e_production_based + p_other_2efgh.CO2e_production_based
    )
    p_other.CO2e_combustion_based = (
        p_other_paper.CO2e_combustion_based
        + p_other_food.CO2e_combustion_based
        + p_other_further.CO2e_combustion_based
    )
    p_other.CO2e_total = (
        p_other_paper.CO2e_total
        + p_other_food.CO2e_total
        + p_other_further.CO2e_total
        + p_other_2efgh.CO2e_total
    )
    # 2018 to 203X
    p_other.change_energy_MWh = (
        p_other_paper.change_energy_MWh
        + p_other_food.change_energy_MWh
        + p_other_further.change_energy_MWh
    )
    p_other.change_energy_pct = div(p_other.change_energy_MWh, i18.p_other.energy)
    p_other.change_CO2e_t = (
        p_other_paper.change_CO2e_t
        + p_other_food.change_CO2e_t
        + p_other_further.change_CO2e_t
        + p_other_2efgh.change_CO2e_t
    )
    p_other.change_CO2e_pct = div(p_other.change_CO2e_t, i18.p_other.CO2e_total)
    p_other.CO2e_total_2021_estimated = (
        p_other_paper.CO2e_total_2021_estimated
        + p_other_food.CO2e_total_2021_estimated
        + p_other_further.CO2e_total_2021_estimated
        + p_other_2efgh.CO2e_total_2021_estimated
    )
    p_other.cost_climate_saved = (
        p_other_paper.cost_climate_saved
        + p_other_food.cost_climate_saved
        + p_other_further.cost_climate_saved
        + p_other_2efgh.cost_climate_saved
    )
    p_other.invest = (
        p_other_paper.invest
        + p_other_food.invest
        + p_other_further.invest
        + p_other_2efgh.invest
    )
    p_other.demand_emplo = (
        p_other_paper.demand_emplo
        + p_other_food.demand_emplo
        + p_other_further.demand_emplo
        + p_other_2efgh.demand_emplo
    )

    p_miner_cement = Vars5()
    p_miner_cement.CO2e_production_based_per_t = ass(
        "Ass_I_P_miner_cement_ratio_CO2e_pb_to_prodvol_2050"
    )
    p_miner_cement.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_miner_cement_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_miner_cement.demand_change = ass("Ass_I_P_miner_cement_prodvol_change")
    p_miner_cement.prod_volume = i18.p_miner_cement.prod_volume * (
        1 + p_miner_cement.demand_change
    )
    p_miner_cement.demand_emethan = (
        ass("Ass_I_P_miner_cement_ratio_fec_gas_to_prodvol_2050")
        * p_miner_cement.prod_volume
    )

    p_miner_ceram = Vars7()

    p_miner_ceram.CO2e_production_based_per_t = ass(
        "Ass_I_P_miner_ceramic_ratio_CO2e_pb_to_prodvol_2050"
    )
    p_miner_cement.CO2e_production_based = (
        p_miner_cement.prod_volume * p_miner_cement.CO2e_production_based_per_t
    )
    p_miner_cement.CO2e_total_2021_estimated = (
        i18.p_miner_cement.CO2e_production_based
        + i18.p_miner_cement.CO2e_combustion_based
    ) * fact(f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref")
    p_miner_cement.CO2e_combustion_based = (
        p_miner_cement.prod_volume * p_miner_cement.CO2e_combustion_based_per_t
    )

    general = energy_general.calc_general(
        assumptions, duration_until_target_year, population_commune_2018
    )

    i.demand_emplo_com = general.g.demand_emplo_com

    p_miner_cement.invest_per_x = ass(
        "Ass_I_P_miner_cement_kirchdorf_ratio_invest_to_prodvol_2020"
    )
    p_miner_cement.invest = p_miner_cement.prod_volume * p_miner_cement.invest_per_x

    p_miner_cement.invest_outside = p_miner_cement.invest

    i.invest_pa_com = general.g.invest_pa_com
    p_miner_ceram.invest_per_x = ass("Ass_I_P_miner_ceramic_ratio_invest_to_prodvol")
    i.invest_com = general.g.invest_com
    p_miner_cement.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_miner_cement.invest_pa = p_miner_cement.invest / duration_until_target_year
    p_miner_cement.cost_wage = p_miner_cement.invest_pa * p_miner_cement.pct_of_wage
    p_miner_cement.demand_electricity = (
        ass("Ass_I_P_miner_cement_ratio_fec_elec_to_prodvol_2050")
        * p_miner_cement.prod_volume
    )
    p_other.demand_heatnet = (
        p_other_paper.demand_heatnet
        + p_other_food.demand_heatnet
        + p_other_further.demand_heatnet
    )  # SUM(p_other_paper.demand_heatnet:p_other_further.demand_heatnet)
    p_miner_ceram.demand_change = ass("Ass_I_P_miner_ceramic_prodvol_change")
    p_miner_ceram.prod_volume = i18.p_miner_ceram.prod_volume * (
        1 + p_miner_ceram.demand_change
    )
    p_miner_ceram.CO2e_production_based = (
        p_miner_ceram.prod_volume * p_miner_ceram.CO2e_production_based_per_t
    )

    p_miner_chalk = Vars5()

    p_miner_chalk.demand_change = ass("Ass_I_P_miner_chalk_prodvol_change")
    p_miner_chalk.prod_volume = i18.p_miner_chalk.prod_volume * (
        1 + p_miner_chalk.demand_change
    )
    p_miner_chalk.CO2e_production_based_per_t = ass(
        "Ass_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol_2050"
    )
    p_miner_chalk.CO2e_production_based = (
        p_miner_chalk.prod_volume * p_miner_chalk.CO2e_production_based_per_t
    )

    p_miner_glas = Vars6()

    p_miner_glas.demand_change = ass("Ass_I_P_miner_glass_prodvol_change")
    p_miner_glas.prod_volume = i18.p_miner_glas.prod_volume * (
        1 + p_miner_glas.demand_change
    )
    p_miner_glas.CO2e_production_based_per_t = ass(
        "Ass_I_P_miner_glass_ratio_CO2e_pb_to_prodvol_2050"
    )
    p_miner_glas.CO2e_production_based = (
        p_miner_glas.prod_volume * p_miner_glas.CO2e_production_based_per_t
    )

    p_miner = Vars4()

    p_miner.CO2e_production_based = (
        p_miner_cement.CO2e_production_based
        + p_miner_chalk.CO2e_production_based
        + p_miner_glas.CO2e_production_based
        + p_miner_ceram.CO2e_production_based
    )  # SUM(p_miner_cement.CO2e_pb:p_miner_ceram.CO2e_pb)
    p_miner_ceram.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_miner_ceramic_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_miner_cement.CO2e_total = (
        p_miner_cement.CO2e_production_based + p_miner_cement.CO2e_combustion_based
    )
    p_miner_cement.energy = (
        p_miner_cement.demand_electricity + p_miner_cement.demand_emethan
    )
    p_miner_cement.change_energy_MWh = p_miner_cement.energy - i18.p_miner_cement.energy
    p_miner_ceram.CO2e_combustion_based = (
        p_miner_ceram.prod_volume * p_miner_ceram.CO2e_combustion_based_per_t
    )

    p = Vars3()

    p.CO2e_production_based = (
        p_miner.CO2e_production_based
        + p_chem.CO2e_production_based
        + p_metal.CO2e_production_based
        + p_other.CO2e_production_based
    )  # SUM(p_miner.CO2e_pb,p_chem.CO2e_pb,p_metal.CO2e_pb,p_other.CO2e_pb)
    p_miner_ceram.CO2e_total_2021_estimated = (
        i18.p_miner_ceram.CO2e_production_based
        + i18.p_miner_ceram.CO2e_combustion_based
    ) * fact(f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref")
    p_miner_cement.cost_climate_saved = (
        (
            p_miner_cement.CO2e_total_2021_estimated
            - (
                p_miner_cement.CO2e_production_based
                + p_miner_cement.CO2e_combustion_based
            )
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_miner_ceram.invest = p_miner_ceram.prod_volume * p_miner_ceram.invest_per_x
    p_miner_cement.invest_pa_outside = p_miner_cement.invest_pa

    p_miner_chalk.invest_per_x = ass(
        "Ass_I_P_miner_chalk_vockerode_ratio_invest_to_prodvol_2018"
    )
    p_miner_chalk.invest = p_miner_chalk.prod_volume * p_miner_chalk.invest_per_x
    p_miner_glas.invest_per_x = ass(
        "Ass_I_P_miner_glass_furnace_ratio_invest_to_prodvol_2021"
    )
    p_miner_glas.invest = p_miner_glas.prod_volume * p_miner_glas.invest_per_x
    p_miner.invest = (
        p_miner_cement.invest
        + p_miner_chalk.invest
        + p_miner_glas.invest
        + p_miner_ceram.invest
    )  # SUM(p_miner_cement.invest:p_miner_ceram.invest)
    p_miner_ceram.invest_outside = p_miner_ceram.invest
    p_miner_ceram.invest_pa = p_miner_ceram.invest / duration_until_target_year
    p_miner_cement.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p.emplo_existing = (
        fact("Fact_I_P_constr_civil_emplo_2018")
        * population_commune_2018
        / population_germany_2018
    )
    p_miner_cement.demand_emplo = div(
        p_miner_cement.cost_wage, p_miner_cement.ratio_wage_to_emplo
    )
    p_chem.demand_electricity = (
        p_chem_basic.demand_electricity
        + p_chem_ammonia.demand_electricity
        + p_chem_other.demand_electricity
    )  # SUM(p_chem_basic.demand_electricity:p_chem_other.demand_electricity)
    p_metal.demand_biomass = p_metal_nonfe.demand_biomass
    p_miner_ceram.demand_electricity = p_miner_ceram.prod_volume * ass(
        "Ass_I_P_miner_ceramic_ratio_fec_elec_to_prodvol_2050"
    )
    p_miner_ceram.demand_hydrogen = p_miner_ceram.prod_volume * ass(
        "Ass_I_P_miner_ceramic_ratio_fec_hydrogen_to_prodvol_2050"
    )
    p_miner_ceram.demand_biomass = p_miner_ceram.prod_volume * ass(
        "Ass_I_P_miner_ceramic_ratio_fec_biomass_to_prodvol_2050"
    )
    p_metal.prod_volume = p_metal_steel.prod_volume + p_metal_nonfe.prod_volume

    p_miner_chalk.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_miner_chalk.CO2e_combustion_based = (
        p_miner_chalk.prod_volume * p_miner_chalk.CO2e_combustion_based_per_t
    )
    p_miner_glas.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_miner_glass_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_miner_glas.CO2e_combustion_based = (
        p_miner_glas.prod_volume * p_miner_glas.CO2e_combustion_based_per_t
    )
    p_miner.CO2e_combustion_based = (
        p_miner_cement.CO2e_combustion_based
        + p_miner_chalk.CO2e_combustion_based
        + p_miner_glas.CO2e_combustion_based
        + p_miner_ceram.CO2e_combustion_based
    )  # SUM(p_miner_cement.CO2e_cb:p_miner_ceram.CO2e_cb)
    p.CO2e_combustion_based = (
        p_miner.CO2e_combustion_based
        + p_chem.CO2e_combustion_based
        + p_metal.CO2e_combustion_based
        + p_other.CO2e_combustion_based
    )
    p_miner_ceram.CO2e_total = (
        p_miner_ceram.CO2e_production_based + p_miner_ceram.CO2e_combustion_based
    )
    p_miner_ceram.energy = (
        p_miner_ceram.demand_electricity
        + p_miner_ceram.demand_biomass
        + p_miner_ceram.demand_hydrogen
    )
    p_miner_ceram.change_energy_MWh = p_miner_ceram.energy - i18.p_miner_ceram.energy
    p_miner_cement.change_CO2e_t = (
        p_miner_cement.CO2e_production_based + p_miner_cement.CO2e_combustion_based
    ) - (
        i18.p_miner_cement.CO2e_production_based
        + i18.p_miner_cement.CO2e_combustion_based
    )
    p_miner_ceram.change_CO2e_t = (
        p_miner_ceram.CO2e_production_based + p_miner_ceram.CO2e_combustion_based
    ) - (
        i18.p_miner_ceram.CO2e_production_based
        + i18.p_miner_ceram.CO2e_combustion_based
    )
    p_miner_chalk.CO2e_total_2021_estimated = (
        i18.p_miner_chalk.CO2e_production_based
        + i18.p_miner_chalk.CO2e_combustion_based
    ) * fact(f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref")
    p_miner_glas.CO2e_total_2021_estimated = (
        i18.p_miner_glas.CO2e_production_based + i18.p_miner_glas.CO2e_combustion_based
    ) * fact(f"Fact_M_CO2e_wo_lulucf_{entries.m_year_baseline - 1}_vs_year_ref")

    p_miner.CO2e_total_2021_estimated = (
        p_miner_cement.CO2e_total_2021_estimated
        + p_miner_chalk.CO2e_total_2021_estimated
        + p_miner_glas.CO2e_total_2021_estimated
        + p_miner_ceram.CO2e_total_2021_estimated
    )  # SUM(p_miner_cement.CO2e_total_2021_estimated:p_miner_ceram.CO2e_total_2021_estimated)
    p_miner_ceram.cost_climate_saved = (
        (
            p_miner_ceram.CO2e_total_2021_estimated
            - (
                p_miner_ceram.CO2e_production_based
                + p_miner_ceram.CO2e_combustion_based
            )
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_chem.invest_pa = (
        p_chem_basic.invest_pa + p_chem_ammonia.invest_pa + p_chem_other.invest_pa
    )  # SUM(p_chem_basic.invest_pa:p_chem_other.invest_pa)
    p_chem.invest_pa_outside = (
        p_chem_basic.invest_pa_outside
        + p_chem_ammonia.invest_pa_outside
        + p_chem_other.invest_pa_outside
    )  # SUM(p_chem_basic.invest_pa_outside:p_chem_other.invest_pa_outside)
    p.invest = p_miner.invest + p_chem.invest + p_metal.invest + p_other.invest
    p_chem.invest_outside = (
        p_chem_basic.invest_outside
        + p_chem_ammonia.invest_outside
        + p_chem_other.invest_outside
    )  # SUM(p_chem_basic.invest_outside:p_chem_other.invest_outside)
    p_chem.cost_wage = (
        p_chem_basic.cost_wage + p_chem_ammonia.cost_wage + p_chem_other.cost_wage
    )  # SUM(p_chem_basic.cost_wage:p_chem_other.cost_wage)
    p_miner_ceram.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_miner_chalk.demand_electricity = p_miner_chalk.prod_volume * ass(
        "Ass_I_P_miner_chalk_ratio_fec_elec_to_prodvol_2050"
    )
    p_miner_chalk.demand_emethan = p_miner_chalk.prod_volume * ass(
        "Ass_I_P_miner_chalk_ratio_fec_gas_to_prodvol_2050"
    )
    p_miner_chalk.energy = (
        p_miner_chalk.demand_electricity + p_miner_chalk.demand_emethan
    )
    p_miner_chalk.change_energy_MWh = p_miner_chalk.energy - i18.p_miner_chalk.energy
    p_miner_glas.demand_electricity = p_miner_glas.prod_volume * ass(
        "Ass_I_P_miner_glass_ratio_fec_elec_to_prodvol_2050"
    )
    p_miner_glas.energy = p_miner_glas.demand_electricity
    p_miner_glas.change_energy_MWh = p_miner_glas.energy - i18.p_miner_glas.energy
    p_miner.change_energy_MWh = (
        p_miner_cement.change_energy_MWh
        + p_miner_chalk.change_energy_MWh
        + p_miner_glas.change_energy_MWh
        + p_miner_ceram.change_energy_MWh
    )  # SUM(p_miner_cement.change_energy_MWh:p_miner_ceram.change_energy_MWh)
    p_miner.change_energy_pct = div(p_miner.change_energy_MWh, i18.p_miner.energy)
    p.change_energy_MWh = (
        p_miner.change_energy_MWh
        + p_chem.change_energy_MWh
        + p_metal.change_energy_MWh
        + p_other.change_energy_MWh
    )
    p.change_energy_pct = div(p.change_energy_MWh, i18.p.energy)
    p.change_CO2e_t = (p.CO2e_production_based + p.CO2e_combustion_based) - (
        i18.p.CO2e_production_based + i18.p.CO2e_combustion_based
    )
    p_miner_chalk.CO2e_total = (
        p_miner_chalk.CO2e_production_based + p_miner_chalk.CO2e_combustion_based
    )
    p_miner_glas.CO2e_total = (
        p_miner_glas.CO2e_production_based + p_miner_glas.CO2e_combustion_based
    )
    p_miner.CO2e_total = (
        p_miner_cement.CO2e_total
        + p_miner_chalk.CO2e_total
        + p_miner_glas.CO2e_total
        + p_miner_ceram.CO2e_total
    )  # SUM(p_miner_cement.CO2e_total:p_miner_ceram.CO2e_total)
    p.change_CO2e_pct = div(p.change_CO2e_t, i18.p.CO2e_total)
    p_miner_chalk.cost_climate_saved = (
        (
            p_miner_chalk.CO2e_total_2021_estimated
            - (
                p_miner_chalk.CO2e_production_based
                + p_miner_chalk.CO2e_combustion_based
            )
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_miner_glas.cost_climate_saved = (
        (
            p_miner_glas.CO2e_total_2021_estimated
            - (p_miner_glas.CO2e_production_based + p_miner_glas.CO2e_combustion_based)
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    p_miner.cost_climate_saved = (
        p_miner_cement.cost_climate_saved
        + p_miner_chalk.cost_climate_saved
        + p_miner_glas.cost_climate_saved
        + p_miner_ceram.cost_climate_saved
    )  # SUM(p_miner_cement.cost_climate_saved:p_miner_ceram.cost_climate_saved)
    p.CO2e_total = (
        p_miner.CO2e_total + p_chem.CO2e_total + p_metal.CO2e_total + p_other.CO2e_total
    )
    i.change_energy_pct = p.change_energy_pct
    p_miner_cement.change_energy_pct = div(
        p_miner_cement.change_energy_MWh, i18.p_miner_cement.energy
    )
    p_miner_chalk.change_CO2e_t = (
        p_miner_chalk.CO2e_production_based + p_miner_chalk.CO2e_combustion_based
    ) - (
        i18.p_miner_chalk.CO2e_production_based
        + i18.p_miner_chalk.CO2e_combustion_based
    )
    p_miner_glas.change_CO2e_t = (
        p_miner_glas.CO2e_production_based + p_miner_glas.CO2e_combustion_based
    ) - (
        i18.p_miner_glas.CO2e_production_based + i18.p_miner_glas.CO2e_combustion_based
    )
    p_miner.change_CO2e_t = (
        p_miner_cement.change_CO2e_t
        + p_miner_chalk.change_CO2e_t
        + p_miner_glas.change_CO2e_t
        + p_miner_ceram.change_CO2e_t
    )  # SUM(p_miner_cement.change_CO2e_t:p_miner_ceram.change_CO2e_t)
    p_miner_cement.change_CO2e_pct = div(
        p_miner_cement.change_CO2e_t, i18.p_miner_cement.CO2e_total
    )
    p.CO2e_total_2021_estimated = (
        p_miner.CO2e_total_2021_estimated
        + p_chem.CO2e_total_2021_estimated
        + p_metal.CO2e_total_2021_estimated
        + p_other.CO2e_total_2021_estimated
    )
    p.cost_climate_saved = (
        p_miner.cost_climate_saved
        + p_chem.cost_climate_saved
        + p_metal.cost_climate_saved
        + p_other.cost_climate_saved
    )
    p_miner_chalk.invest_pa = p_miner_chalk.invest / duration_until_target_year
    p_miner_glas.invest_pa = p_miner_glas.invest / duration_until_target_year
    p_miner.invest_pa = (
        p_miner_cement.invest_pa
        + p_miner_chalk.invest_pa
        + p_miner_glas.invest_pa
        + p_miner_ceram.invest_pa
    )  # SUM(p_miner_cement.invest_pa:p_miner_ceram.invest_pa)
    p_miner_ceram.invest_pa_outside = p_miner_ceram.invest_pa
    p_miner_chalk.invest_pa_outside = p_miner_chalk.invest_pa
    p_miner_glas.invest_pa_outside = p_miner_glas.invest_pa
    p_miner.invest_pa_outside = (
        p_miner_cement.invest_pa_outside
        + p_miner_chalk.invest_pa_outside
        + p_miner_glas.invest_pa_outside
        + p_miner_ceram.invest_pa_outside
    )  # SUM(p_miner_cement.invest_pa_outside:p_miner_ceram.invest_pa_outside)
    p_miner_chalk.invest_outside = p_miner_chalk.invest
    p_miner_glas.invest_outside = p_miner_glas.invest
    p_miner.invest_outside = (
        p_miner_cement.invest_outside
        + p_miner_chalk.invest_outside
        + p_miner_glas.invest_outside
        + p_miner_ceram.invest_outside
    )  # SUM(p_miner_cement.invest_outside:p_miner_ceram.invest_outside)
    p_miner_ceram.cost_wage = p_miner_ceram.invest_pa * p_miner_ceram.pct_of_wage
    p_miner_ceram.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_miner_ceram.demand_emplo = div(
        p_miner_ceram.cost_wage, p_miner_ceram.ratio_wage_to_emplo
    )
    p_miner_chalk.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_miner_chalk.cost_wage = p_miner_chalk.invest_pa * p_miner_chalk.pct_of_wage
    p_miner_chalk.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_miner_chalk.demand_emplo = div(
        p_miner_chalk.cost_wage, p_miner_chalk.ratio_wage_to_emplo
    )
    p_miner_glas.ratio_wage_to_emplo = fact(
        "Fact_I_P_constr_civil_ratio_wage_to_emplo_2018"
    )
    p_miner_glas.pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
    p_miner_glas.cost_wage = p_miner_glas.invest_pa * p_miner_glas.pct_of_wage
    p_miner_glas.demand_emplo = div(
        p_miner_glas.cost_wage, p_miner_glas.ratio_wage_to_emplo
    )
    p_miner.demand_emplo = (
        p_miner_cement.demand_emplo
        + p_miner_chalk.demand_emplo
        + p_miner_glas.demand_emplo
        + p_miner_ceram.demand_emplo
    )  # SUM(p_miner_cement.demand_emplo:p_miner_ceram.demand_emplo)
    p.demand_emplo = (
        p_miner.demand_emplo
        + p_chem.demand_emplo
        + p_metal.demand_emplo
        + p_other.demand_emplo
    )
    p_miner.demand_emethan = (
        p_miner_cement.demand_emethan + p_miner_chalk.demand_emethan
    )  # SUM(p_miner_cement.demand_emethan:p_miner_chalk.demand_emethan)
    p_miner_chalk.change_energy_pct = div(
        p_miner_chalk.change_energy_MWh, i18.p_miner_chalk.energy
    )
    p_miner_chalk.change_CO2e_pct = div(
        p_miner_chalk.change_CO2e_t, i18.p_miner_chalk.CO2e_total
    )
    p_miner_glas.change_energy_pct = div(
        p_miner_glas.change_energy_MWh, i18.p_miner_glas.energy
    )
    p_miner_glas.change_CO2e_pct = div(
        p_miner_glas.change_CO2e_t, i18.p_miner_glas.CO2e_total
    )
    p_miner.demand_electricity = (
        p_miner_cement.demand_electricity
        + p_miner_chalk.demand_electricity
        + p_miner_glas.demand_electricity
        + p_miner_ceram.demand_electricity
    )  # SUM(p_miner_cement.demand_electricity:p_miner_ceram.demand_electricity)
    p_miner.demand_biomass = p_miner_ceram.demand_biomass
    p_miner.demand_hydrogen = p_miner_ceram.demand_hydrogen
    p_miner.prod_volume = (
        p_miner_cement.prod_volume
        + p_miner_chalk.prod_volume
        + p_miner_glas.prod_volume
        + p_miner_ceram.prod_volume
    )  # SUM(p_miner_cement.prod_volume:p_miner_ceram.prod_volume)
    p_miner.energy = (
        p_miner_cement.energy
        + p_miner_chalk.energy
        + p_miner_glas.energy
        + p_miner_ceram.energy
    )  # SUM(p_miner_cement.energy:p_miner_ceram.energy)
    p.energy = (
        p_miner.energy + p_chem.energy + p_metal.energy + p_other.energy
    )  # SUM(p_miner.energy,p_chem.energy,p_metal.energy,p_other.energy)
    i.change_CO2e_t = p.change_CO2e_t
    i.CO2e_production_based = p.CO2e_production_based
    i.CO2e_combustion_based = p.CO2e_combustion_based
    i.change_CO2e_pct = p.change_CO2e_pct
    i.CO2e_total = p.CO2e_total
    i.change_energy_MWh = p.change_energy_MWh
    p_miner_ceram.change_energy_pct = div(
        p_miner_ceram.change_energy_MWh, i18.p_miner_ceram.energy
    )
    p_miner.change_CO2e_pct = div(p_miner.change_CO2e_t, i18.p_miner.CO2e_total)
    p_miner_ceram.change_CO2e_pct = div(
        p_miner_ceram.change_CO2e_t, i18.p_miner_ceram.CO2e_total
    )
    i.CO2e_total_2021_estimated = p.CO2e_total_2021_estimated
    i.cost_climate_saved = p.cost_climate_saved
    p_metal.invest_pa = (
        p_metal_steel.invest_pa + p_metal_nonfe.invest_pa
    )  # SUM(p_metal_steel.invest_pa,p_metal_nonfe.invest_pa)
    p_metal.invest_pa_outside = (
        p_metal_steel.invest_pa_outside + p_metal_nonfe.invest_pa_outside
    )
    i.invest = general.g.invest + p.invest
    p_metal.invest_outside = p_metal_steel.invest_outside + p_metal_nonfe.invest_outside
    p_miner.cost_wage = (
        p_miner_cement.cost_wage
        + p_miner_chalk.cost_wage
        + p_miner_glas.cost_wage
        + p_miner_ceram.cost_wage
    )  # SUM(p_miner_cement.cost_wage:p_miner_ceram.cost_wage)
    p_metal_steel.cost_wage = (
        p_metal_steel_primary.cost_wage + p_metal_steel_secondary.cost_wage
    )
    p.demand_emplo_new = max(0, p.demand_emplo - p.emplo_existing)
    i.demand_emplo = general.g.demand_emplo + p.demand_emplo
    i.demand_emplo_new = general.g.demand_emplo_new + p.demand_emplo_new
    p_metal_steel.demand_electricity = (
        p_metal_steel_primary.demand_electricity
        + p_metal_steel_secondary.demand_electricity
    )
    p_chem.demand_emethan = p_chem_basic.demand_emethan + p_chem_other.demand_emethan
    p_other.invest_pa = (
        p_other_paper.invest_pa
        + p_other_food.invest_pa
        + p_other_further.invest_pa
        + p_other_2efgh.invest_pa
    )  # SUM(p_other_paper.invest_pa:p_other_2efgh.invest_pa)
    p_other.invest_pa_outside = (
        p_other_paper.invest_pa_outside
        + p_other_food.invest_pa_outside
        + p_other_further.invest_pa_outside
        + p_other_2efgh.invest_pa_outside
    )  # SUM(p_other_paper.invest_pa_outside:p_other_2efgh.invest_pa_outside)
    p_other_2efgh.invest_outside = p_other_2efgh.invest
    p_metal.cost_wage = (
        p_metal_steel.cost_wage + p_metal_nonfe.cost_wage
    )  # SUM(p_metal_steel.cost_wage,p_metal_nonfe.cost_wage)

    p_chem_basic.CO2e_production_based_per_t = ass("Ass_I_P_chem_all_co2e_factor_2050")
    p_chem_ammonia.demand_change = ass("Ass_I_P_chem_ammonia_prodvol_change")
    p_chem_ammonia.CO2e_production_based_per_t = ass(
        "Ass_I_P_chem_all_co2e_factor_2050"
    )
    p_chem_ammonia.CO2e_combustion_based_per_t = ass(
        "Ass_I_P_chem_ammonia_ratio_CO2e_cb_to_prodvol_2050"
    )
    p_chem_other.demand_change = ass("Ass_I_P_chem_other_prodvol_change")
    p_chem_other.CO2e_production_based_per_t = ass("Ass_I_P_chem_all_co2e_factor_2050")
    p_other.demand_electricity = (
        p_other_paper.demand_electricity
        + p_other_food.demand_electricity
        + p_other_further.demand_electricity
    )  # SUM(p_other_paper.demand_electricity:p_other_further.demand_electricity)
    p.demand_biomass = p_miner.demand_biomass + p_metal.demand_biomass
    p_metal.demand_hydrogen = (
        p_metal_steel_primary.demand_hydrogen + p_metal_nonfe.demand_hydrogen
    )
    p.prod_volume = (
        p_miner.prod_volume
        + p_chem.prod_volume
        + p_metal.prod_volume
        + p_other.prod_volume
    )
    p.invest_pa = (
        p_miner.invest_pa + p_chem.invest_pa + p_metal.invest_pa + p_other.invest_pa
    )
    p.invest_pa_outside = (
        p_miner.invest_pa_outside
        + p_chem.invest_pa_outside
        + p_metal.invest_pa_outside
        + p_other.invest_pa_outside
    )
    p_other_food.invest_outside = p_other_food.invest
    p_other_further.invest_outside = p_other_further.invest
    p_other.invest_outside = (
        p_other_paper.invest_outside
        + p_other_food.invest_outside
        + p_other_further.invest_outside
        + p_other_2efgh.invest_outside
    )  # SUM(p_other_paper.invest_outside:p_other_2efgh.invest_outside)
    p_other.cost_wage = (
        p_other_paper.cost_wage
        + p_other_food.cost_wage
        + p_other_further.cost_wage
        + p_other_2efgh.cost_wage
    )  # SUM(p_other_paper.cost_wage:p_other_2efgh.cost_wage)
    p_metal.demand_electricity = (
        p_metal_steel.demand_electricity + p_metal_nonfe.demand_electricity
    )
    p.cost_wage = (
        p_miner.cost_wage + p_chem.cost_wage + p_metal.cost_wage + p_other.cost_wage
    )
    p.demand_electricity = (
        p_miner.demand_electricity
        + p_chem.demand_electricity
        + p_metal.demand_electricity
        + p_other.demand_electricity
    )
    p.demand_heatnet = p_other.demand_heatnet
    p_other_further.demand_emethan = p_other_further.energy * ass(
        "Ass_I_P_other_further_fec_pct_of_gas_2050"
    )
    i.invest_pa = general.g.invest_pa + p.invest_pa
    i.invest_pa_outside = p.invest_pa_outside
    p.invest_outside = (
        p_miner.invest_outside
        + p_chem.invest_outside
        + p_metal.invest_outside
        + p_other.invest_outside
    )
    i.cost_wage = general.g.cost_wage + p.cost_wage
    p_other_paper.CO2e_production_based_per_t = fact(
        "Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol"
    )
    p_other_paper.CO2e_production_based = (
        p_other_paper.prod_volume * p_other_paper.CO2e_production_based_per_t
    )
    p_other_food.CO2e_production_based_per_t = fact(
        "Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol"
    )
    p_other_food.CO2e_production_based = (
        p_other_food.prod_volume * p_other_food.CO2e_production_based_per_t
    )
    p_other.demand_emethan = p_other_further.demand_emethan

    i.invest_outside = p.invest_outside
    p.demand_hydrogen = p_miner.demand_hydrogen + p_metal.demand_hydrogen
    s_renew_hydrogen = Vars16(energy=p.demand_hydrogen)
    p.demand_emethan = (
        p_miner.demand_emethan + p_chem.demand_emethan + p_other.demand_emethan
    )
    s_renew_emethan = Vars16(energy=p.demand_emethan)
    s_renew_biomass = Vars16(energy=p.demand_biomass)
    s_renew_heatnet = Vars16(energy=p.demand_heatnet)
    s_renew_elec = Vars16(energy=p.demand_electricity)
    s_renew = Vars16(
        energy=s_renew_hydrogen.energy
        + s_renew_emethan.energy
        + s_renew_biomass.energy
        + s_renew_heatnet.energy
        + s_renew_elec.energy
    )
    s = Vars16(energy=s_renew.energy)

    s_fossil_diesel = Vars16(energy=0)
    s_fossil_fueloil = Vars16(energy=0)
    s_fossil_opetpro = Vars16(energy=0)
    s_fossil_coal = Vars16(energy=0)
    s_fossil_lpg = Vars16(energy=0)
    s_fossil_gas = Vars16(energy=0)
    s_fossil_ofossil = Vars16(energy=0)
    s_renew_heatpump = Vars16(energy=0)
    s_renew_solarth = Vars16(energy=0)

    return I30(
        g=general.g,
        g_consult=general.g_consult,
        i=i,
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
        s=s,
        s_fossil_gas=s_fossil_gas,
        s_fossil_coal=s_fossil_coal,
        s_fossil_diesel=s_fossil_diesel,
        s_fossil_fueloil=s_fossil_fueloil,
        s_fossil_lpg=s_fossil_lpg,
        s_fossil_opetpro=s_fossil_opetpro,
        s_fossil_ofossil=s_fossil_ofossil,
        s_renew=s_renew,
        s_renew_hydrogen=s_renew_hydrogen,
        s_renew_emethan=s_renew_emethan,
        s_renew_biomass=s_renew_biomass,
        s_renew_heatnet=s_renew_heatnet,
        s_renew_heatpump=s_renew_heatpump,
        s_renew_solarth=s_renew_solarth,
        s_renew_elec=s_renew_elec,
    )
