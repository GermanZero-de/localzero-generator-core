# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div
from ...common.energy import Energy
from ...common.co2e_change import CO2eChange, CO2eChangeEnergy
from ...common.invest import Invest
from ...fuels2018.energy_production import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class EFuelProduction(Energy, CO2eChange, CO2eChangeEnergy, Invest):
    """This computes the replacement of fossil fuels by corresponding E-fuels.
    (e.g. petrol -> epetrol).
    """

    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    demand_electricity: float
    full_load_hour: float
    invest_per_x: float
    pct_of_wage: float
    power_to_be_installed: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        energy: float,
        inputs: Inputs,
        CO2e_emission_factor: float,
        production_2018: EnergyWithCO2ePerMWh,
    ) -> "EFuelProduction":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        CO2e_total_2021_estimated = production_2018.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        # We assume that we take as much CO2e out of the air when the E-Fuel
        # is produced, as we later emit when it is burned.
        CO2e_production_based_per_MWh = -1 * CO2e_emission_factor
        pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
        ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
        invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
        full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
        demand_electricity = energy / ass("Ass_S_power_to_x_efficiency")
        change_energy_MWh = energy - production_2018.energy
        CO2e_production_based = CO2e_production_based_per_MWh * energy
        power_to_be_installed = div(demand_electricity, full_load_hour)
        change_energy_pct = div(change_energy_MWh, production_2018.energy)
        CO2e_total = CO2e_production_based
        invest = power_to_be_installed * ass("Ass_S_power_to_x_invest_per_power")
        change_CO2e_t = CO2e_total - production_2018.CO2e_total
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_pa = invest / entries.m_duration_target
        change_CO2e_pct = div(change_CO2e_t, production_2018.CO2e_total)
        cost_wage = invest_pa * pct_of_wage
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        return cls(
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            full_load_hour=full_load_hour,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
