# pyright: strict
from dataclasses import dataclass, InitVar

from ..utils import div
from ..agri2018.a18 import A18
from ..inputs import Inputs


@dataclass(kw_only=True)
class CO2eChange:
    CO2e_combustion_based: float
    CO2e_production_based: float

    CO2e_total: float = 0
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    cost_climate_saved: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):

        if not what:
            a18_CO2e_total = 0
        else:
            a18_CO2e_total = getattr(a18, what).CO2e_total

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based
        self.change_CO2e_t = self.CO2e_total - a18_CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, a18_CO2e_total)

        self.CO2e_total_2021_estimated = a18_CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )


@dataclass(kw_only=True)
class CO2eChangeEnergy:
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    energy: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)


@dataclass(kw_only=True)
class CO2eChangeFermentationOrManure(CO2eChange):
    CO2e_production_based_per_t: float = 0
    amount: float = 0
    demand_change: float = 0

    @classmethod
    def calc_fermen(
        cls, inputs: Inputs, what: str, ass_demand_change: str, a18: A18
    ) -> "CO2eChangeFermentationOrManure":
        CO2e_combustion_based = 0

        demand_change = inputs.ass(ass_demand_change)
        amount = getattr(a18, what).amount * (1 + demand_change)

        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t
        CO2e_production_based = amount * CO2e_production_based_per_t

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
        )

        return cls(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            amount=amount,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )

    @classmethod
    def calc_manure(
        cls, inputs: Inputs, what: str, a18: A18, amount: float
    ) -> "CO2eChangeFermentationOrManure":
        CO2e_combustion_based = 0

        demand_change = inputs.ass("Ass_A_P_manure_ratio_CO2e_to_amount_change")

        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t * (
            1 + demand_change
        )
        CO2e_production_based = amount * CO2e_production_based_per_t

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
        )

        return cls(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            amount=amount,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )


@dataclass(kw_only=True)
class CO2eChangeSoil(CO2eChange):
    CO2e_production_based_per_t: float = 0
    area_ha: float = 0
    area_ha_change: float = 0
    demand_change: float = 0

    @classmethod
    def calc_soil_special(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        area_ha: float,
        CO2e_production_based_per_t: float,
    ) -> "CO2eChangeSoil":

        CO2e_combustion_based = 0

        demand_change = (
            div(
                CO2e_production_based_per_t,
                getattr(a18, what).CO2e_production_based_per_t,
            )
            - 1
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
        )

        return cls(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            area_ha=area_ha,
            area_ha_change=area_ha_change,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )

    @classmethod
    def calc_soil(
        cls, inputs: Inputs, what: str, a18: A18, area_ha: float
    ) -> "CO2eChangeSoil":
        CO2e_combustion_based = 0

        demand_change = inputs.ass("Ass_A_P_soil_N_application_2030_change")
        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t * (
            1 + demand_change
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
        )

        return cls(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            area_ha=area_ha,
            area_ha_change=area_ha_change,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )


@dataclass(kw_only=True)
class CO2eChangeOtherLiming(CO2eChange):
    prod_volume: float

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):

        self.CO2e_combustion_based = 0

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved


@dataclass(kw_only=True)
class CO2eChangeOther(CO2eChange):
    CO2e_production_based_per_t: float = 0
    demand_change: float = 0
    prod_volume: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    ass_demand_change: InitVar[str]
    fact_production_based_per_t: InitVar[str]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        ass_demand_change: str,
        fact_production_based_per_t: str,
    ):

        self.CO2e_combustion_based = 0

        self.demand_change = inputs.ass(ass_demand_change)
        self.prod_volume = getattr(a18, what).prod_volume * (1 + self.demand_change)

        self.CO2e_production_based_per_t = inputs.fact(fact_production_based_per_t)
        self.CO2e_production_based = self.prod_volume * self.CO2e_production_based_per_t

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved


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


@dataclass(kw_only=True)
class CO2eChangePOperationElecElcon(CO2eChangeEnergy):
    demand_biomass: float = 0
    demand_change: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_heatpump: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):

        self.demand_biomass = 0
        self.demand_heatpump = 0
        self.demand_ediesel = 0
        self.demand_emethan = 0

        self.demand_change = inputs.ass("Ass_B_D_fec_elec_elcon_change")
        self.energy = getattr(a18, what).energy * (1 + self.demand_change)

        self.demand_electricity = self.energy

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct


@dataclass(kw_only=True)
class CO2eChangePOperationElecHeatpump(CO2eChangeEnergy):
    demand_electricity: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    p_operation_heat: InitVar[CO2eChangePOperationHeat]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18, p_operation_heat: CO2eChangePOperationHeat):  # type: ignore

        self.energy = p_operation_heat.demand_heatpump / inputs.fact(
            "Fact_R_S_heatpump_mean_annual_performance_factor_all"
        )
        self.demand_electricity = self.energy

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh


@dataclass(kw_only=True)
class CO2eChangePOperationVehicles(CO2eChangeEnergy):
    demand_biomass: float = 0
    demand_change: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):

        self.demand_electricity = 0
        self.demand_biomass = 0
        self.demand_heatpump = 0
        self.demand_emethan = 0

        self.demand_change = inputs.ass("Ass_B_D_fec_vehicles_change")
        self.energy = getattr(a18, what).energy * (1 + self.demand_change)

        self.demand_epetrol = div(
            self.energy * a18.s_petrol.energy,
            a18.s_petrol.energy + a18.s_diesel.energy,
        )
        self.demand_ediesel = div(
            self.energy * a18.s_diesel.energy,
            a18.s_petrol.energy + a18.s_diesel.energy,
        )

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct


@dataclass(kw_only=True)
class CO2eChangePOperation(CO2eChangeEnergy):
    cost_wage: float = 0
    demand_biomass: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0
    invest: float = 0
    invest_pa: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    p_operation_vehicles: InitVar[CO2eChangePOperationVehicles]
    p_operation_heat: InitVar[CO2eChangePOperationHeat]
    p_operation_elec_elcon: InitVar[CO2eChangePOperationElecElcon]
    p_operation_elec_heatpump: InitVar[CO2eChangePOperationElecHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation_vehicles: CO2eChangePOperationVehicles,
        p_operation_heat: CO2eChangePOperationHeat,
        p_operation_elec_elcon: CO2eChangePOperationElecElcon,
        p_operation_elec_heatpump: CO2eChangePOperationElecHeatpump,
    ):
        self.demand_epetrol = p_operation_vehicles.demand_epetrol
        self.demand_ediesel = p_operation_vehicles.demand_ediesel
        self.demand_heatpump = p_operation_heat.demand_heatpump
        self.demand_emplo = p_operation_heat.demand_emplo
        self.demand_emplo_new = p_operation_heat.demand_emplo_new
        self.demand_biomass = p_operation_heat.demand_biomass
        self.demand_electricity = (
            p_operation_elec_elcon.demand_electricity
            + p_operation_elec_heatpump.demand_electricity
        )
        self.demand_emethan = p_operation_heat.demand_emethan

        self.energy = (
            p_operation_heat.energy
            + p_operation_elec_elcon.energy
            + p_operation_elec_heatpump.energy
            + p_operation_vehicles.energy
        )

        self.invest = p_operation_heat.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target
        self.cost_wage = p_operation_heat.cost_wage

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct


@dataclass(kw_only=True)
class CO2eChangeP:
    CO2e_production_based: float = 0
    CO2e_total: float = 0
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    cost_climate_saved: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    energy: float = 0
    invest: float = 0
    invest_pa: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    p_operation: InitVar[CO2eChangePOperation]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation: CO2eChangePOperation,
    ):

        a18_CO2e_total = getattr(a18, what).CO2e_total

        self.CO2e_total_2021_estimated = a18_CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        self.change_CO2e_t = self.CO2e_total - a18_CO2e_total
        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )
        self.change_CO2e_pct = div(self.change_CO2e_t, a18_CO2e_total)
        self.demand_emplo = p_operation.demand_emplo

        self.invest = p_operation.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.demand_emplo_new = p_operation.demand_emplo_new
        self.energy = p_operation.energy
        self.cost_wage = p_operation.cost_wage
