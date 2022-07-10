# pyright: strict
from dataclasses import dataclass, InitVar
from typing import Any

from ..utils import div, MILLION
from ..agri2018.a18 import A18
from ..inputs import Inputs
from .energy_demand import CO2eChange


@dataclass(kw_only=True)
class CO2eChangeEnergyPerMWh(CO2eChange):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_combustion_based_per_MWh = getattr(
            a18, what
        ).CO2e_combustion_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=0,
        )

        self.CO2e_combustion_based = parent.CO2e_combustion_based
        self.CO2e_production_based = parent.CO2e_production_based
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved


@dataclass(kw_only=True)
class CO2eChangeS(CO2eChange):
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore

    @classmethod
    def calc_s(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        s_petrol: Any,
        s_diesel: Any,
        s_fueloil: Any,
        s_lpg: Any,
        s_gas: Any,
        s_emethan: Any,
        s_biomass: Any,
        s_elec: Any,
        s_heatpump: Any,
    ) -> "CO2eChangeS":

        CO2e_combustion_based = (
            s_petrol.CO2e_combustion_based
            + s_diesel.CO2e_combustion_based
            + s_fueloil.CO2e_combustion_based
            + s_lpg.CO2e_combustion_based
            + s_gas.CO2e_combustion_based
            + s_emethan.CO2e_combustion_based
            + s_biomass.CO2e_combustion_based
            + s_elec.CO2e_combustion_based
            + s_heatpump.CO2e_combustion_based
        )

        invest = s_heatpump.invest
        invest_pa = invest / inputs.entries.m_duration_target

        energy = (
            s_petrol.energy
            + s_diesel.energy
            + s_fueloil.energy
            + s_lpg.energy
            + s_gas.energy
            + s_emethan.energy
            + s_biomass.energy
            + s_elec.energy
            + s_heatpump.energy
        )
        change_energy_MWh = energy - getattr(a18, what).energy
        change_energy_pct = div(change_energy_MWh, getattr(a18, what).energy)

        demand_emplo = s_heatpump.demand_emplo
        demand_emplo_new = s_heatpump.demand_emplo_new

        cost_wage = s_heatpump.cost_wage

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=0,
        )

        return cls(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=parent.cost_climate_saved,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            invest=invest,
            invest_pa=invest_pa,
        )


@dataclass(kw_only=True)
class CO2eChangeFuelOilGas(CO2eChangeEnergyPerMWh):
    area_m2: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.area_m2 = 0

        parent = CO2eChangeEnergyPerMWh(
            inputs=inputs,
            what=what,
            a18=a18,
            energy=self.energy,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_combustion_based = parent.CO2e_combustion_based
        self.CO2e_production_based = parent.CO2e_production_based
        self.CO2e_combustion_based_per_MWh = parent.CO2e_combustion_based_per_MWh
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved
        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct


@dataclass(kw_only=True)
class CO2eChangeFuelHeatpump(CO2eChangeEnergyPerMWh):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    emplo_existing: float = 0
    full_load_hour: float = 0
    invest: float = 0
    invest_pa: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    power_installed: float = 0
    power_to_be_installed: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

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

        self.CO2e_combustion_based = parent.CO2e_combustion_based
        self.CO2e_production_based = parent.CO2e_production_based
        self.CO2e_combustion_based_per_MWh = parent.CO2e_combustion_based_per_MWh
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.cost_climate_saved = parent.cost_climate_saved
        self.change_energy_MWh = parent.change_energy_MWh

        # override value from parent!
        self.change_CO2e_pct = div(
            parent.change_CO2e_t, 1.0  # always 0
        )  # getattr(a18, what).CO2e_total)


@dataclass(kw_only=True)
class CO2eChangeFuelEmethan(CO2eChange):
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    energy: float = None  # type: ignore

    @classmethod
    def calc_energy(
        cls, inputs: Inputs, a18: A18, energy: float
    ) -> "CO2eChangeFuelEmethan":
        CO2e_combustion_based = 0
        CO2e_combustion_based_per_MWh = inputs.fact(
            "Fact_T_S_methan_EmFa_tank_wheel_2018"
        )

        change_energy_MWh = energy
        demand_emethan = energy

        parent = CO2eChange(
            inputs=inputs,
            what="",
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=0,
        )

        return cls(
            inputs=inputs,
            what="",
            a18=a18,
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            cost_climate_saved=parent.cost_climate_saved,
            demand_emethan=demand_emethan,
            energy=energy,
        )
