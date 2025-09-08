# pyright: strict

from ....makeentries import Entries
from ....refdata import Facts, Assumptions
from ....utils import MILLION
from ....electricity2018.e18 import E18

from ..e_col_vars_2030 import EColVars2030


def calc_production_local_hydro(
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    *,
    e18: E18,
):
    fact = facts.fact
    ass = assumptions.ass

    power_installed = entries.e_PV_power_inst_water
    full_load_hour = fact("Fact_E_P_hydro_full_load_hours")  # energy
    cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")  # cost_mro
    CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    energy = (
        power_installed
        * full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    cost_mro = energy * cost_mro_per_MWh / MILLION
    CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
    CO2e_total = CO2e_combustion_based
    change_CO2e_t = 0
    change_CO2e_pct = 0
    cost_climate_saved = 0

    cost_fuel_per_MWh = None
    cost_fuel = None
    pet_sites = None
    energy_installable = None
    CO2e_total_year_before_baseline_estimated = None
    demand_electricity = None
    demand_emplo = None
    demand_emplo_com = None
    power_to_be_installed_pct = None
    power_to_be_installed = None
    power_installable = None
    area_ha_available = None
    area_ha_available_pct_of_action = None
    ratio_power_to_area_ha = None
    change_cost_energy = None
    change_cost_mro = None
    invest = None
    invest_pa = None
    invest_com = None
    invest_pa_com = None
    invest_outside = None
    invest_pa_outside = None
    invest_per_x = None
    pct_of_wage = None
    pct_x = None
    ratio_wage_to_emplo = None
    cost_wage = None
    emplo_existing = None
    demand_emplo_new = None

    p_local_hydro = EColVars2030(
        cost_fuel_per_MWh=cost_fuel_per_MWh,  # type: ignore
        cost_fuel=cost_fuel,  # type: ignore
        pet_sites=pet_sites,  # type: ignore
        energy_installable=energy_installable,  # type: ignore
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
        CO2e_combustion_based=CO2e_combustion_based,
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        CO2e_total_year_before_baseline_estimated=CO2e_total_year_before_baseline_estimated,  # type: ignore
        demand_electricity=demand_electricity,  # type: ignore
        demand_emplo=demand_emplo,  # type: ignore
        demand_emplo_com=demand_emplo_com,  # type: ignore
        power_installed=power_installed,
        power_to_be_installed_pct=power_to_be_installed_pct,  # type: ignore
        power_to_be_installed=power_to_be_installed,  # type: ignore
        power_installable=power_installable,  # type: ignore
        area_ha_available=area_ha_available,  # type: ignore
        area_ha_available_pct_of_action=area_ha_available_pct_of_action,  # type: ignore
        ratio_power_to_area_ha=ratio_power_to_area_ha,  # type: ignore
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_energy=change_cost_energy,  # type: ignore
        change_cost_mro=change_cost_mro,  # type: ignore
        invest=invest,  # type: ignore
        invest_pa=invest_pa,  # type: ignore
        invest_com=invest_com,  # type: ignore
        invest_pa_com=invest_pa_com,  # type: ignore
        invest_outside=invest_outside,  # type: ignore
        invest_pa_outside=invest_pa_outside,  # type: ignore
        invest_per_x=invest_per_x,  # type: ignore
        pct_of_wage=pct_of_wage,  # type: ignore
        pct_x=pct_x,  # type: ignore
        ratio_wage_to_emplo=ratio_wage_to_emplo,  # type: ignore
        cost_wage=cost_wage,  # type: ignore
        cost_mro_per_MWh=cost_mro_per_MWh,
        emplo_existing=emplo_existing,  # type: ignore
        demand_emplo_new=demand_emplo_new,  # type: ignore
        full_load_hour=full_load_hour,
    )

    p_local_hydro.change_energy_MWh = energy - e18.p_local_hydro.energy

    p_local_hydro.energy = energy

    return p_local_hydro
