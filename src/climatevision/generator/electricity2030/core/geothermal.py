# pyright: strict

from ...refdata import Facts, Assumptions

from .renewable_geothermal_production import RenewableGeothermalProduction


def calc_production_renewable_geothermal(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    *,
    d_energy: float,
) -> RenewableGeothermalProduction:
    fact = facts.fact
    ass = assumptions.ass

    CO2e_total = 0
    invest = 0
    demand_emplo = 0
    cost_mro_per_MWh = ass("Ass_E_P_renew_geoth_mro_per_MWh")
    CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    invest_per_x = ass("Ass_E_P_renew_geoth_invest") * 1000
    pct_of_wage = ass("Ass_E_P_constr_plant_invest_pct_of_wage_2017")
    ratio_wage_to_emplo = ass("Ass_E_P_constr_elec_ratio_wage_to_emplo_2017")
    emplo_existing = 0
    power_installable = ass("Ass_E_P_renew_geoth_power_installable")
    power_to_be_installed_pct = ass("Ass_E_P_renew_geoth_power_to_be_installed_2035")
    power_installed = fact("Fact_E_P_geoth_power_installed_2018")
    full_load_hour = fact("Fact_E_P_geoth_full_load_hours")

    invest_pa = invest / duration_until_target_year
    demand_emplo_new = max(0, demand_emplo - emplo_existing)
    power_to_be_installed = max(
        0,
        power_installable * power_to_be_installed_pct - power_installed,
    )
    energy_installable = (
        full_load_hour
        * power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    invest_outside = invest * d_energy / ass("Ass_E_P_renew_nep_total_2035")
    cost_wage = invest_pa * pct_of_wage
    invest_pa_outside = (
        power_to_be_installed
        * invest_per_x
        / duration_until_target_year
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    change_CO2e_pct = 0
    cost_climate_saved = 0

    # For now the below are actually computed at a later stage
    # TODO: Figure out if we can move the calculations up
    energy = 0
    CO2e_combustion_based = 0
    cost_mro = 0
    change_energy_MWh = 0
    change_energy_pct = 0
    change_CO2e_t = 0
    change_cost_mro = 0
    pct_x = 0
    return RenewableGeothermalProduction(
        energy=energy,
        energy_installable=energy_installable,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
        CO2e_combustion_based=CO2e_combustion_based,
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        demand_emplo=demand_emplo,
        power_installed=power_installed,
        power_to_be_installed_pct=power_to_be_installed_pct,
        power_to_be_installed=power_to_be_installed,
        power_installable=power_installable,
        change_energy_MWh=change_energy_MWh,
        change_energy_pct=change_energy_pct,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_mro=change_cost_mro,
        invest=invest,
        invest_pa=invest_pa,
        invest_outside=invest_outside,
        invest_pa_outside=invest_pa_outside,
        invest_per_x=invest_per_x,
        pct_of_wage=pct_of_wage,
        pct_x=pct_x,
        ratio_wage_to_emplo=ratio_wage_to_emplo,
        cost_wage=cost_wage,
        cost_mro_per_MWh=cost_mro_per_MWh,
        emplo_existing=emplo_existing,
        demand_emplo_new=demand_emplo_new,
        full_load_hour=full_load_hour,
    )
