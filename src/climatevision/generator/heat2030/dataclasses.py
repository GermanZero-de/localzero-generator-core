# pyright: strict

from dataclasses import dataclass, InitVar

from ..inputs import Inputs
from ..utils import div, MILLION
from ..heat2018.h18 import H18
from ..common.energyWithCO2ePerMWh import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class VarsInvest:
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0


@dataclass(kw_only=True)
class VarsChange:
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    cost_climate_saved: float = 0


@dataclass(kw_only=True)
class Vars0(VarsInvest, VarsChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5(VarsInvest, VarsChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9(EnergyWithCO2ePerMWh, VarsChange):
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

        h18_p_what = getattr(h18, "p_" + what)

        self.CO2e_production_based = self.energy * self.CO2e_production_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

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
class Vars6(Vars9):
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

        super().__post_init__(inputs=inputs, what=what, h18=h18)

        if what == "biomass":
            self.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
        else:
            self.cost_fuel_per_MWh = ass("Ass_R_S_" + what + "_energy_cost_factor_2035")

        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION


@dataclass(kw_only=True)
class Vars11(Vars9, VarsInvest):
    area_ha_available: float = 0
    invest_per_x: float = 0
    pct_energy: float
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
        fact = inputs.fact
        entries = inputs.entries

        super().__post_init__(inputs=inputs, what=what, h18=h18)

        self.invest_per_x = fact("Fact_H_P_heatnet_solarth_park_invest_203X")
        self.area_ha_available = self.energy / fact(
            "Fact_H_P_heatnet_solarth_park_yield_2025"
        )
        self.invest = self.invest_per_x * self.area_ha_available
        self.invest_pa = self.invest / entries.m_duration_target

        self.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        self.cost_wage = self.pct_of_wage * self.invest_pa

        self.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)

        self.invest_pa_com = self.invest_pa
        self.invest_com = self.invest
        self.demand_emplo_new = self.demand_emplo


@dataclass(kw_only=True)
class Vars12(Vars9, VarsInvest):
    demand_electricity: float = 0
    full_load_hour: float = 0
    invest_per_x: float = 0
    pct_energy: float
    pct_of_wage: float = 0
    power_to_be_installed: float = 0
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
        fact = inputs.fact
        entries = inputs.entries

        super().__post_init__(inputs=inputs, what=what, h18=h18)

        self.invest_per_x = fact("Fact_H_P_heatnet_lheatpump_invest_203X")
        self.full_load_hour = fact("Fact_H_P_heatnet_lheatpump_full_load_hours")
        self.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        self.power_to_be_installed = div(self.energy, self.full_load_hour)
        self.invest = self.invest_per_x * self.power_to_be_installed
        self.invest_pa = self.invest / entries.m_duration_target
        self.cost_wage = self.pct_of_wage * self.invest_pa
        self.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo
        self.demand_electricity = self.energy / fact("Fact_H_P_heatnet_lheatpump_apf")

        self.invest_pa_com = self.invest_pa
        self.invest_com = self.invest


@dataclass(kw_only=True)
class Vars13(VarsInvest, VarsChange):
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars10(VarsInvest, VarsChange):
    CO2e_combustion_based: float = 0
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    energy: float

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]
    heatnet_cogen: InitVar[Vars9]
    p_heatnet_plant: InitVar[Vars11]
    p_heatnet_lheatpump: InitVar[Vars12]
    p_heatnet_geoth: InitVar[Vars13]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
        heatnet_cogen: Vars9,
        p_heatnet_plant: Vars11,
        p_heatnet_lheatpump: Vars12,
        p_heatnet_geoth: Vars13,
    ):
        fact = inputs.fact
        entries = inputs.entries

        h18_p_what = getattr(h18, "p_" + what)

        self.CO2e_total = heatnet_cogen.CO2e_total

        self.CO2e_combustion_based = heatnet_cogen.CO2e_combustion_based

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

        self.invest = (
            p_heatnet_plant.invest + p_heatnet_lheatpump.invest + p_heatnet_geoth.invest
        )
        self.invest_pa = (
            p_heatnet_plant.invest_pa
            + p_heatnet_lheatpump.invest_pa
            + p_heatnet_geoth.invest_pa
        )
        self.invest_pa_com = self.invest_pa
        self.demand_emplo = (
            p_heatnet_plant.demand_emplo
            + p_heatnet_lheatpump.demand_emplo
            + p_heatnet_geoth.demand_emplo
        )
        self.invest_com = self.invest
        self.cost_wage = (
            p_heatnet_plant.cost_wage
            + p_heatnet_lheatpump.cost_wage
            + p_heatnet_geoth.cost_wage
        )
        self.demand_emplo_new = (
            p_heatnet_plant.demand_emplo_new
            + p_heatnet_lheatpump.demand_emplo_new
            + p_heatnet_geoth.demand_emplo_new
        )
        self.CO2e_production_based = (
            heatnet_cogen.CO2e_production_based
            + p_heatnet_plant.CO2e_production_based
            + p_heatnet_lheatpump.CO2e_production_based
            + p_heatnet_geoth.CO2e_production_based
        )
