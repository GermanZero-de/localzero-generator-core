# pyright: strict
from dataclasses import dataclass
from typing import Any

from ..utils import div, MILLION
from ..agri2018.a18 import A18
from ..inputs import Inputs
from .energy_demand import CO2eChange


@dataclass
class CO2eChangeEnergy(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore

    @classmethod
    def calc_energy(
        cls, inputs: Inputs, what: str, a18: A18, energy: float
    ) -> "CO2eChangeEnergy":
        CO2e_combustion_based_per_MWh = getattr(a18, what).CO2e_combustion_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        change_energy_MWh = energy - getattr(a18, what).energy
        change_energy_pct = div(change_energy_MWh, getattr(a18, what).energy)

        parent = super().calc(inputs, what, a18, CO2e_combustion_based, 0)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            energy=energy,
        )


@dataclass
class CO2eChangeS(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
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

        parent = super().calc(inputs, what, a18, CO2e_combustion_based, 0)

        return cls(
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


@dataclass
class CO2eChangeFuelOilGas(CO2eChangeEnergy):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    area_m2: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore

    @classmethod
    def calc_energy(
        cls, inputs: Inputs, what: str, a18: A18, energy: float
    ) -> "CO2eChangeFuelOilGas":
        area_m2 = 0

        parent = super().calc_energy(inputs, what, a18, energy)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=parent.CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            area_m2=area_m2,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            change_energy_MWh=parent.change_energy_MWh,
            change_energy_pct=parent.change_energy_pct,
            energy=energy,
        )


@dataclass
class CO2eChangeFuelHeatpump(CO2eChangeEnergy):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore

    @classmethod
    def calc_energy(
        cls, inputs: Inputs, what: str, a18: A18, energy: float
    ) -> "CO2eChangeFuelHeatpump":

        cost_fuel_per_MWh = inputs.fact("Fact_R_S_gas_energy_cost_factor_2018")
        cost_fuel = energy * cost_fuel_per_MWh / MILLION

        full_load_hour = inputs.fact("Fact_B_S_full_usage_hours_buildings")
        power_installed = div(getattr(a18, what).energy, full_load_hour)
        power_to_be_installed = max(div(energy, full_load_hour) - power_installed, 0)

        invest_per_x = inputs.fact("Fact_R_S_heatpump_cost")
        invest = invest_per_x * power_to_be_installed * 1000
        invest_pa = invest / inputs.entries.m_duration_target

        pct_of_wage = inputs.fact("Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = inputs.fact("Fact_B_P_heating_wage_per_person_per_year")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        emplo_existing = (
            inputs.fact("Fact_B_P_install_heating_emplo_2017")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
            * inputs.ass("Ass_B_D_install_heating_emplo_pct_of_A_heatpump")
        )

        demand_emplo_new = max(0, demand_emplo - emplo_existing)

        parent = super().calc_energy(inputs, what, a18, energy)

        # override value from parent!
        change_CO2e_pct = div(
            parent.change_CO2e_t, 1.0  # always 0
        )  # getattr(a18, what).CO2e_total)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=parent.CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            change_energy_MWh=parent.change_energy_MWh,
            cost_fuel=cost_fuel,
            cost_fuel_per_MWh=cost_fuel_per_MWh,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            energy=energy,
            full_load_hour=full_load_hour,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            power_installed=power_installed,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class CO2eChangeFuelEmethan(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
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

        parent = super().calc(inputs, "", a18, CO2e_combustion_based, 0)

        return cls(
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
