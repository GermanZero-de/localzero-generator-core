# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18

from .co2eChangeEnergy import CO2eChangeEnergy


@dataclass(kw_only=True)
class CO2eChangePOperationHeat(CO2eChangeEnergy):
    area_m2: float = 0
    area_m2_nonrehab: float = 0
    area_m2_rehab: float = 0
    cost_wage: float = 0
    demand_biomass: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    demand_epetrol: float = 0
    demand_heat_nonrehab: float = 0
    demand_heat_rehab: float = 0
    demand_heatpump: float = 0
    emplo_existing: float = 0
    fec_factor_averaged: float = 0
    invest: float = 0
    invest_pa: float = 0
    invest_per_x: float = 0
    pct_nonrehab: float = 0
    pct_of_wage: float = 0
    pct_rehab: float = 0
    rate_rehab_pa: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):
        self.rate_rehab_pa = inputs.entries.r_rehab_rate_pa
        self.pct_rehab = (
            inputs.fact("Fact_B_P_ratio_renovated_to_not_renovated_2021")
            + self.rate_rehab_pa * inputs.entries.m_duration_target
        )
        self.pct_nonrehab = 1 - self.pct_rehab

        self.area_m2 = getattr(a18, what).area_m2
        self.area_m2_rehab = self.pct_rehab * getattr(a18, what).area_m2
        self.area_m2_nonrehab = self.pct_nonrehab * getattr(a18, what).area_m2

        self.invest_per_x = inputs.fact("Fact_R_P_energetical_renovation_cost_business")
        self.invest = (
            self.area_m2_rehab
            * (1 - inputs.fact("Fact_B_P_ratio_renovated_to_not_renovated_2021"))
            * self.invest_per_x
        )
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.pct_of_wage = inputs.fact(
            "Fact_B_P_renovations_ratio_wage_to_main_revenue_2017"
        )
        self.cost_wage = (
            div(self.invest, inputs.entries.m_duration_target) * self.pct_of_wage
        )

        self.ratio_wage_to_emplo = inputs.fact(
            "Fact_B_P_renovations_wage_per_person_per_year_2017"
        )
        self.emplo_existing = (
            inputs.fact("Fact_B_P_renovation_emplo_2017")
            * inputs.ass("Ass_B_D_renovation_emplo_pct_of_A")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        self.demand_electricity = 0
        self.demand_epetrol = 0
        self.demand_ediesel = 0
        self.demand_heat_rehab = self.area_m2_rehab * inputs.ass(
            "Ass_B_D_ratio_fec_to_area_2050"
        )
        self.demand_heat_nonrehab = (
            self.area_m2_nonrehab
            * (
                getattr(a18, what).factor_adapted_to_fec
                - inputs.fact("Fact_B_P_ratio_renovated_to_not_renovated_2021")
                * inputs.ass("Ass_B_D_ratio_fec_to_area_2050")
            )
            / (1 - inputs.fact("Fact_B_P_ratio_renovated_to_not_renovated_2021"))
        )
        self.demand_heatpump = self.demand_heat_rehab
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = max(0, self.demand_emplo - self.emplo_existing)

        self.energy = self.demand_heat_nonrehab + self.demand_heat_rehab

        self.demand_biomass = min(
            a18.s_biomass.energy, self.energy - self.demand_heatpump
        )
        self.demand_emethan = self.energy - self.demand_biomass - self.demand_heatpump

        self.fec_factor_averaged = div(self.energy, getattr(a18, what).area_m2)

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct
