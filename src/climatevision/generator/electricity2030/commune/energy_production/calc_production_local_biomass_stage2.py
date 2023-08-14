# pyright: strict

from ....refdata import Facts, Assumptions
from ....utils import div, MILLION
from ....electricity2018.e18 import E18

from ...core.e_col_vars_2030 import EColVars2030


def calc_production_local_biomass_stage2(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    duration_CO2e_neutral_years: float,
    population_commune_2018: int,
    population_germany_2018: int,
    *,
    e18: E18,
    p_local_biomass: EColVars2030,
) -> None:
    fact = facts.fact
    ass = assumptions.ass

    p_local_biomass.cost_fuel_per_MWh = ass(
        "Ass_E_P_local_biomass_material_costs"
    ) / ass("Ass_E_P_local_biomass_efficiency")
    p_local_biomass.cost_mro_per_MWh = ass("Ass_E_P_local_biomass_mro_per_MWh")
    p_local_biomass.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_biomass_ratio_CO2e_cb_nonCO2_to_gep_2018"
    ) / (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    p_local_biomass.invest_per_x = ass(
        "Ass_E_P_local_biomass_ratio_invest_to_power"
    )  # invest
    p_local_biomass.pct_of_wage = ass(
        "Ass_E_P_constr_plant_invest_pct_of_wage_2017"
    )  # cost_wage
    p_local_biomass.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )  # demand_emplo
    p_local_biomass.emplo_existing = (
        fact("Fact_E_P_biomass_emplo_2018")
        * population_commune_2018
        / population_germany_2018
    )
    p_local_biomass.energy_installable = (
        p_local_biomass.power_installable
        * p_local_biomass.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_biomass.cost_fuel = (
        p_local_biomass.cost_fuel_per_MWh * p_local_biomass.energy / MILLION
    )
    p_local_biomass.cost_mro = (
        p_local_biomass.energy * p_local_biomass.cost_mro_per_MWh / MILLION
    )
    p_local_biomass.CO2e_combustion_based = (
        p_local_biomass.energy * p_local_biomass.CO2e_combustion_based_per_MWh
    )
    p_local_biomass.change_energy_MWh = (
        p_local_biomass.energy - e18.p_local_biomass.energy
    )
    p_local_biomass.invest = (
        p_local_biomass.power_to_be_installed * p_local_biomass.invest_per_x
    )
    p_local_biomass.invest_pa = p_local_biomass.invest / duration_until_target_year
    p_local_biomass.change_cost_energy = (
        p_local_biomass.cost_fuel - e18.p_local_biomass.cost_fuel
    )
    p_local_biomass.change_cost_mro = (
        p_local_biomass.cost_mro - e18.p_local_biomass.cost_mro
    )
    p_local_biomass.CO2e_total = p_local_biomass.CO2e_combustion_based
    p_local_biomass.cost_climate_saved = (
        (
            p_local_biomass.CO2e_total_2021_estimated
            - p_local_biomass.CO2e_combustion_based
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_local_biomass.cost_wage = (
        p_local_biomass.invest_pa
        * p_local_biomass.pct_of_wage
        / duration_until_target_year
    )
    p_local_biomass.change_CO2e_t = p_local_biomass.CO2e_total - 0
    p_local_biomass.demand_emplo = div(
        p_local_biomass.cost_wage, p_local_biomass.ratio_wage_to_emplo
    )
    p_local_biomass.demand_emplo_new = max(
        0, p_local_biomass.demand_emplo - p_local_biomass.emplo_existing
    )
