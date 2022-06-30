# pyright: strict
from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import div
from .. import fuels2018


@dataclass
class EnergyDemand:
    # Used by d, d_r, d_b, d_i, d_t, d_a, d_e_hydrogen_reconv, p_hydrogen_total
    energy: float


@dataclass
class EFuelProduction:
    """This computes the replacement of fossil fuels by corresponding E-fuels.
    (e.g. petrol -> epetrol).
    """

    # Used by p_petrol, p_jetfuel, p_diesel
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_wage: float
    demand_electricity: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    full_load_hour: float
    invest: float
    invest_pa: float
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
        production_2018: fuels2018.FuelProduction,
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


@dataclass
class FuelWithoutDirectReplacement:
    """This computes the effect on our CO2e and energy budget of us totally stopping
    to produce some fuels without a direct replacement."""

    # Used by p_bioethanol, p_biodiesel, p_biogas
    CO2e_total_2021_estimated: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float

    @classmethod
    def calc(cls, energy2018: float) -> "FuelWithoutDirectReplacement":
        # Possible future work marker:
        # We simplified bio{ethonal,diesel,gas} to have 0 emission at
        # production and when burned.  This is not fully correct. But
        # if we didn't do that we would also have to account for growth
        # of the bio component in lulucf.
        return cls(
            change_energy_MWh=-energy2018,
            change_energy_pct=-1,
            CO2e_total_2021_estimated=0,
            change_CO2e_t=0,
            cost_climate_saved=0,
        )


@dataclass
class NewEFuelProduction:
    """Production of new style of efuels that are not yet used (at an industrial scale)."""

    # Used by p_emethan, p_hydrogen, p_hydrogen_reconv
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    cost_climate_saved: float
    cost_wage: float
    demand_electricity: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    full_load_hour: float
    invest: float
    invest_outside: float
    invest_pa: float
    invest_pa_outside: float
    invest_per_x: float
    pct_of_wage: float
    power_to_be_installed: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        energy: float,
        CO2e_emission_factor: float,
        invest_per_power: float,
        full_load_hour: float,
        fuel_efficiency: float,
    ) -> "NewEFuelProduction":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        CO2e_total_2021_estimated = 0
        # We assume that we take as much CO2e out of the air when the E-Fuel
        # is produced, as we later emit when it is burned.
        CO2e_production_based_per_MWh = -1 * CO2e_emission_factor
        CO2e_production_based = CO2e_production_based_per_MWh * energy
        CO2e_total = CO2e_production_based
        change_CO2e_t = CO2e_total
        change_CO2e_pct = 0

        pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
        ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
        demand_electricity = energy / fuel_efficiency
        change_energy_MWh = energy
        power_to_be_installed = demand_electricity / full_load_hour
        invest = power_to_be_installed * invest_per_power
        cost_climate_saved = (
            -CO2e_total * entries.m_duration_neutral * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_pa = invest / entries.m_duration_target
        invest_outside = invest
        invest_pa_outside = invest_pa
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
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            full_load_hour=full_load_hour,
            invest=invest,
            invest_outside=invest_outside,
            invest_pa=invest_pa,
            invest_pa_outside=invest_pa_outside,
            invest_per_x=invest_per_power,
            pct_of_wage=pct_of_wage,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class TotalEFuelProduction:
    # Used by p
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_wage: float
    demand_electricity: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    invest: float
    invest_outside: float
    invest_pa: float
    invest_pa_outside: float

    @classmethod
    def calc(
        cls,
        f18: fuels2018.F18,
        new_efuels: list[NewEFuelProduction],
        efuels: list[EFuelProduction],
        fuels_without_repl: list[FuelWithoutDirectReplacement],
    ) -> "TotalEFuelProduction":

        res = cls(
            CO2e_production_based=sum(x.CO2e_production_based for x in new_efuels)
            + sum(x.CO2e_production_based for x in efuels),
            CO2e_total=sum(x.CO2e_total for x in new_efuels)
            + sum(x.CO2e_total for x in efuels),
            CO2e_total_2021_estimated=sum(
                x.CO2e_total_2021_estimated for x in new_efuels
            )
            + sum(x.CO2e_total_2021_estimated for x in efuels)
            + sum(x.CO2e_total_2021_estimated for x in fuels_without_repl),
            change_CO2e_pct=0,
            change_CO2e_t=sum(x.change_CO2e_t for x in new_efuels)
            + sum(x.change_CO2e_t for x in efuels)
            + sum(x.change_CO2e_t for x in fuels_without_repl),
            change_energy_MWh=sum(x.change_energy_MWh for x in new_efuels)
            + sum(x.change_energy_MWh for x in efuels)
            + sum(x.change_energy_MWh for x in fuels_without_repl),
            change_energy_pct=0,
            cost_climate_saved=sum(x.cost_climate_saved for x in new_efuels)
            + sum(x.cost_climate_saved for x in efuels)
            + sum(x.cost_climate_saved for x in fuels_without_repl),
            cost_wage=sum(x.cost_wage for x in new_efuels)
            + sum(x.cost_wage for x in efuels),
            demand_electricity=sum(x.demand_electricity for x in new_efuels)
            + sum(x.demand_electricity for x in efuels),
            demand_emplo=sum(x.demand_emplo for x in new_efuels)
            + sum(x.demand_emplo for x in efuels),
            demand_emplo_new=sum(x.demand_emplo_new for x in new_efuels)
            + sum(x.demand_emplo_new for x in efuels),
            energy=sum(x.energy for x in new_efuels) + sum(x.energy for x in efuels),
            invest=sum(x.invest for x in new_efuels) + sum(x.invest for x in efuels),
            invest_outside=sum(x.invest_outside for x in new_efuels),
            invest_pa=sum(x.invest_pa for x in new_efuels)
            + sum(x.invest_pa for x in efuels),
            invest_pa_outside=sum(x.invest_pa_outside for x in new_efuels),
        )
        res.change_energy_pct = div(res.change_energy_MWh, f18.p.energy)
        res.change_CO2e_pct = div(res.change_CO2e_t, f18.p.CO2e_total)
        return res


@dataclass
class F:
    # Used by f
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    invest: float
    invest_outside: float
    invest_pa: float
    invest_pa_outside: float

    @classmethod
    def of_p(cls, p: TotalEFuelProduction) -> "F":
        return cls(
            CO2e_total_2021_estimated=p.CO2e_total_2021_estimated,
            CO2e_production_based=p.CO2e_production_based,
            CO2e_total=p.CO2e_total,
            change_energy_MWh=p.change_energy_MWh,
            change_CO2e_t=p.change_CO2e_t,
            cost_climate_saved=p.cost_climate_saved,
            change_energy_pct=p.change_energy_pct,
            change_CO2e_pct=p.change_CO2e_pct,
            invest=p.invest,
            invest_pa=p.invest_pa,
            invest_outside=p.invest_outside,
            invest_pa_outside=p.invest_pa_outside,
            cost_wage=p.cost_wage,
            demand_emplo=p.demand_emplo,
            demand_emplo_new=p.demand_emplo_new,
        )


@dataclass
class EFuels:
    # Used by p_efuels
    change_CO2e_t: float
    energy: float

    @classmethod
    def calc(cls, *efuels: EFuelProduction) -> "EFuels":
        change_CO2e_t = sum(e.change_CO2e_t for e in efuels)
        energy = sum(e.energy for e in efuels)
        return cls(change_CO2e_t=change_CO2e_t, energy=energy)
