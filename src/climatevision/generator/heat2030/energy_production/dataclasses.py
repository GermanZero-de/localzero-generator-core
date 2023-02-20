# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div, MILLION
from ...heat2018.h18 import H18
from ...common.energy import Energy
from ...common.energy_with_co2e_per_mwh import EnergyWithCO2ePerMWh
from ...common.co2_emission import CO2Emission
from ...common.invest import InvestCommune


@dataclass(kw_only=True)
class CO2eChange:
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    cost_climate_saved: float = 0


@dataclass(kw_only=True)
class CO2eChangeHeatProduction(Energy, CO2Emission, CO2eChange):
    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact
        entries = inputs.entries

        if what == "":
            h18_p_what = getattr(h18, "p" + what)
        else:
            h18_p_what = getattr(h18, "p_" + what)

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based

        self.change_energy_MWh = self.energy - h18_p_what.energy
        self.change_energy_pct = div(self.change_energy_MWh, h18_p_what.energy)

        self.change_CO2e_t = self.CO2e_total - h18_p_what.CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, h18_p_what.CO2e_total)

        self.CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )


@dataclass(kw_only=True)
class InvestPerX:
    pct_energy: float
    invest_per_x: float


@dataclass(kw_only=True)
class InvestHeatProduction(InvestCommune):
    pct_of_wage: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        entries = inputs.entries
        fact = inputs.fact

        self.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        self.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")

        self.invest_com = self.invest

        self.invest_pa = self.invest / entries.m_duration_target
        self.invest_pa_com = self.invest_pa

        self.cost_wage = self.pct_of_wage * self.invest_pa

        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo


@dataclass(kw_only=True)
class HeatProduction(EnergyWithCO2ePerMWh, CO2eChangeHeatProduction):
    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        self.CO2e_production_based = self.energy * self.CO2e_production_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        CO2eChangeHeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)


@dataclass(kw_only=True)
class HeatProductionWithCostFuel(HeatProduction):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact
        ass = inputs.ass

        HeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)

        if what == "biomass":
            self.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
        else:
            self.cost_fuel_per_MWh = ass("Ass_R_S_" + what + "_energy_cost_factor_2035")

        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION


@dataclass(kw_only=True)
class HeatnetPlantProduction(HeatProduction, InvestHeatProduction, InvestPerX):
    area_ha_available: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact

        HeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)

        self.area_ha_available = self.energy / fact(
            "Fact_H_P_heatnet_solarth_park_yield_2025"
        )
        self.invest = self.invest_per_x * self.area_ha_available

        InvestHeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)


@dataclass(kw_only=True)
class HeatnetGeothProduction(HeatProduction, InvestHeatProduction, InvestPerX):
    full_load_hour: float
    power_to_be_installed: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        HeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)

        self.power_to_be_installed = div(self.energy, self.full_load_hour)
        self.invest = self.invest_per_x * self.power_to_be_installed

        InvestHeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)


@dataclass(kw_only=True)
class HeatnetLheatpumpProduction(HeatnetGeothProduction):
    demand_electricity: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact

        HeatnetGeothProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)

        self.demand_electricity = self.energy / fact("Fact_H_P_heatnet_lheatpump_apf")


@dataclass(kw_only=True)
class HeatnetProduction(InvestHeatProduction, CO2eChangeHeatProduction):
    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        CO2eChangeHeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)
        InvestHeatProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)


@dataclass(kw_only=True)
class TotalHeatProduction(HeatnetProduction):
    cost_fuel: float = 0
    demand_electricity: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        HeatnetProduction.__post_init__(self, inputs=inputs, what=what, h18=h18)
