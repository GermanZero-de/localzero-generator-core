# pyright: strict
from dataclasses import dataclass, InitVar

from ..utils import div
from ..agri2018.a18 import A18
from ..inputs import Inputs
from .energy_demand import CO2eChangePOperation, CO2eChangeP
from .energy_source import CO2eChangeS


@dataclass(kw_only=True)
class CO2eChangeGConsult:
    area_ha_available: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_com: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]

    def __post_init__(self, inputs: Inputs):

        self.area_ha_available = inputs.entries.a_farm_amount

        self.invest_per_x = inputs.ass("Ass_A_G_consult_invest_per_farm")
        self.invest = self.area_ha_available * self.invest_per_x
        self.invest_com = self.invest * inputs.ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )
        self.invest_pa = self.invest / inputs.entries.m_duration_target
        self.invest_pa_com = self.invest_pa * inputs.ass(
            "Ass_A_G_consult_invest_pct_of_public"
        )

        self.pct_of_wage = inputs.ass("Ass_A_G_consult_invest_pct_of_wage")
        self.cost_wage = self.invest_pa * self.pct_of_wage

        self.ratio_wage_to_emplo = inputs.ass("Ass_A_G_consult_ratio_wage_to_emplo")
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo
        self.demand_emplo_com = self.demand_emplo_new


@dataclass(kw_only=True)
class CO2eChangeGOrganic:
    area_ha_available: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_pa: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    power_installed: float = 0
    power_to_be_installed: float = 0
    power_to_be_installed_pct: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]

    def __post_init__(self, inputs: Inputs):

        self.area_ha_available = inputs.entries.m_area_agri_com

        self.power_installed = inputs.entries.a_area_agri_com_pct_of_organic
        self.power_to_be_installed_pct = inputs.ass(
            "Ass_A_G_area_agri_pct_of_organic_2050"
        )
        self.power_to_be_installed = self.area_ha_available * (
            self.power_to_be_installed_pct - self.power_installed
        )

        self.invest_per_x = inputs.ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
        self.invest = self.power_to_be_installed * self.invest_per_x
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.pct_of_wage = inputs.fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        self.cost_wage = self.invest_pa * self.pct_of_wage

        self.ratio_wage_to_emplo = inputs.fact(
            "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
        )
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo


@dataclass(kw_only=True)
class CO2eChangeG:
    CO2e_total: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_com: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_outside: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0
    invest_pa_outside: float = 0

    g_consult: InitVar[CO2eChangeGConsult]
    g_organic: InitVar[CO2eChangeGOrganic]

    def __post_init__(
        self, g_consult: CO2eChangeGConsult, g_organic: CO2eChangeGOrganic
    ):

        self.CO2e_total = 0
        self.cost_wage = g_consult.cost_wage + g_organic.cost_wage

        self.demand_emplo = g_consult.demand_emplo + g_organic.demand_emplo
        self.demand_emplo_new = g_consult.demand_emplo_new + g_organic.demand_emplo_new
        self.demand_emplo_com = g_consult.demand_emplo_com

        self.invest = g_consult.invest + g_organic.invest
        self.invest_com = g_consult.invest_com
        self.invest_outside = 0

        self.invest_pa = g_consult.invest_pa + g_organic.invest_pa
        self.invest_pa_com = g_consult.invest_pa_com
        self.invest_pa_outside = 0


@dataclass(kw_only=True)
class CO2eChangeA:
    CO2e_combustion_based: float = 0
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    cost_climate_saved: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_com: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_outside: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0
    invest_pa_outside: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    p_operation: InitVar[CO2eChangePOperation]
    p: InitVar[CO2eChangeP]
    g: InitVar[CO2eChangeG]
    s: InitVar[CO2eChangeS]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation: CO2eChangePOperation,
        p: CO2eChangeP,
        g: CO2eChangeG,
        s: CO2eChangeS,
    ):

        self.CO2e_production_based = p.CO2e_production_based
        self.CO2e_combustion_based = s.CO2e_combustion_based
        self.CO2e_total = g.CO2e_total + p.CO2e_total + s.CO2e_total

        self.CO2e_total_2021_estimated = getattr(a18, what).CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        self.invest_pa_outside = g.invest_pa_outside
        self.invest_outside = g.invest_outside
        self.invest_com = g.invest_com
        self.invest = g.invest + s.invest + p.invest
        self.invest_pa_com = g.invest_pa_com
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.change_CO2e_t = self.CO2e_total - getattr(a18, what).CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, a18.a.CO2e_total)
        self.change_energy_MWh = p_operation.change_energy_MWh
        self.change_energy_pct = p_operation.change_energy_pct

        self.demand_emplo = g.demand_emplo + p.demand_emplo + s.demand_emplo
        self.demand_emplo_new = (
            g.demand_emplo_new + p.demand_emplo_new + s.demand_emplo_new
        )
        self.demand_emplo_com = g.demand_emplo_com

        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )

        self.cost_wage = g.cost_wage + p.cost_wage + s.cost_wage
