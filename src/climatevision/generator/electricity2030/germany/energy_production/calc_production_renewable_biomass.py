# pyright: strict

from ....electricity2018.e18 import E18
from ....refdata import Assumptions, Facts
from ....utils import MILLION, div
from ...core.e_col_vars_2030 import EColVars2030


def calc_production_renewable_biomass(
    facts: Facts,
    assumptions: Assumptions,
    year_baseline: int,
    duration_CO2e_neutral_years: float,
    *,
    e18: E18,
):
    fact = facts.fact
    ass = assumptions.ass

    p_renew_biomass = EColVars2030()
    p_renew_biomass.CO2e_total_year_before_baseline_estimated = (
        e18.p_renew_biomass.CO2e_combustion_based
        * fact(f"Fact_M_CO2e_wo_lulucf_{year_baseline - 1}_vs_year_ref")
    )
    p_renew_biomass.cost_fuel_per_MWh = ass(
        "Ass_E_P_local_biomass_material_costs"
    ) / ass("Ass_E_P_local_biomass_efficiency")
    p_renew_biomass.cost_mro_per_MWh = ass("Ass_E_P_local_biomass_mro_per_MWh")
    p_renew_biomass.CO2e_combustion_based_per_MWh = (
        e18.p_renew_biomass.CO2e_combustion_based_per_MWh
    )
    p_renew_biomass.change_energy_MWh = 0
    p_renew_biomass.change_energy_pct = div(
        p_renew_biomass.change_energy_MWh, e18.p_renew_biomass.energy
    )
    p_renew_biomass.energy = 0
    p_renew_biomass.cost_fuel = (
        p_renew_biomass.energy * p_renew_biomass.cost_fuel_per_MWh / MILLION
    )
    p_renew_biomass.cost_mro = (
        p_renew_biomass.energy * p_renew_biomass.cost_mro_per_MWh / MILLION
    )
    p_renew_biomass.CO2e_combustion_based = (
        p_renew_biomass.energy * p_renew_biomass.CO2e_combustion_based_per_MWh
    )
    p_renew_biomass.change_cost_energy = (
        p_renew_biomass.cost_fuel - e18.p_renew_biomass.cost_fuel
    )
    p_renew_biomass.change_cost_mro = (
        p_renew_biomass.cost_mro - e18.p_renew_biomass.cost_mro
    )
    p_renew_biomass.CO2e_total = p_renew_biomass.CO2e_combustion_based
    p_renew_biomass.cost_climate_saved = (
        (
            p_renew_biomass.CO2e_total_year_before_baseline_estimated
            - p_renew_biomass.CO2e_combustion_based
        )
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_renew_biomass.change_CO2e_t = (
        p_renew_biomass.CO2e_total - e18.p_renew_biomass.CO2e_total
    )
    p_renew_biomass.change_CO2e_pct = div(
        p_renew_biomass.change_CO2e_t, e18.p_renew_biomass.CO2e_total
    )

    return p_renew_biomass
