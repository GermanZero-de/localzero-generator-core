# pyright: strict

from ....refdata import Facts
from ....utils import div
from .... import electricity2018

from .fossil_fuels_production import FossilFuelsProduction


def calc_stop_production_by_fossil_fuels(
    facts: Facts,
    duration_CO2e_neutral_years: float,
    *,
    e18_production: electricity2018.dataclasses.FossilFuelsProduction,
) -> FossilFuelsProduction:
    """Compute what happens if we stop producing electricity from a fossil fuel."""
    fact = facts.fact

    energy = 0
    CO2e_total_2021_estimated = e18_production.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_year_ref"
    )
    cost_fuel_per_MWh = e18_production.cost_fuel_per_MWh
    cost_mro_per_MWh = e18_production.cost_mro_per_MWh
    CO2e_combustion_based_per_MWh = e18_production.CO2e_combustion_based_per_MWh
    change_energy_MWh = energy - e18_production.energy
    cost_fuel = cost_fuel_per_MWh * energy / 1000000
    cost_mro = cost_mro_per_MWh * energy / 1000000
    CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
    change_energy_pct = div(change_energy_MWh, e18_production.energy)
    change_cost_energy = cost_fuel - e18_production.cost_fuel
    change_cost_mro = cost_mro - e18_production.cost_mro
    CO2e_total = CO2e_combustion_based
    cost_climate_saved = (
        (CO2e_total_2021_estimated - CO2e_combustion_based)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    change_CO2e_t = CO2e_total - e18_production.CO2e_total
    change_CO2e_pct = div(change_CO2e_t, e18_production.CO2e_total)

    return FossilFuelsProduction(
        energy=energy,
        cost_fuel_per_MWh=cost_fuel_per_MWh,
        cost_fuel=cost_fuel,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
        CO2e_combustion_based=CO2e_combustion_based,
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        CO2e_total_2021_estimated=CO2e_total_2021_estimated,
        change_energy_MWh=change_energy_MWh,
        change_energy_pct=change_energy_pct,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_energy=change_cost_energy,
        change_cost_mro=change_cost_mro,
        cost_mro_per_MWh=cost_mro_per_MWh,
    )
