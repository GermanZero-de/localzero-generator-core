# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div, MILLION
from ...common.invest import Invest
from ...agri2018.a18 import A18

from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh


@dataclass(kw_only=True)
class CO2eChangeFuelHeatpump(CO2eChangeEnergyPerMWh, Invest):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float = 0
    emplo_existing: float = 0
    full_load_hour: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    power_installed: float = 0
    power_to_be_installed: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0

        self.cost_fuel_per_MWh = inputs.fact("Fact_R_S_gas_energy_cost_factor_2018")
        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION

        self.full_load_hour = inputs.fact("Fact_B_S_full_usage_hours_buildings")
        self.power_installed = div(getattr(a18, what).energy, self.full_load_hour)
        self.power_to_be_installed = max(
            div(self.energy, self.full_load_hour) - self.power_installed, 0
        )

        self.invest_per_x = inputs.fact("Fact_R_S_heatpump_cost")
        self.invest = self.invest_per_x * self.power_to_be_installed * 1000
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.pct_of_wage = inputs.fact(
            "Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017"
        )
        self.cost_wage = self.invest_pa * self.pct_of_wage
        self.ratio_wage_to_emplo = inputs.fact(
            "Fact_B_P_heating_wage_per_person_per_year"
        )
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)

        self.emplo_existing = (
            inputs.fact("Fact_B_P_install_heating_emplo_2017")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
            * inputs.ass("Ass_B_D_install_heating_emplo_pct_of_A_heatpump")
        )

        self.demand_emplo_new = max(0, self.demand_emplo - self.emplo_existing)

        parent = CO2eChangeEnergyPerMWh(
            inputs=inputs,
            what=what,
            a18=a18,
            energy=self.energy,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_combustion_based_per_MWh = parent.CO2e_combustion_based_per_MWh
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.cost_climate_saved = parent.cost_climate_saved
        self.change_energy_MWh = parent.change_energy_MWh

        # override value from parent!
        self.change_CO2e_pct = div(
            parent.change_CO2e_t, 1.0  # always 0
        )  # getattr(a18, what).CO2e_total)
