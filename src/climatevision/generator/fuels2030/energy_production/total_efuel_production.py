# pyright: strict

from dataclasses import dataclass

from ...utils import div
from ...common.energy import Energy, EnergyChange
from ...common.co2e_change import CO2eChange
from ...common.invest import Invest
from ...fuels2018.f18 import F18

from .efuel_production import EFuelProduction
from .new_efuel_production import NewEFuelProduction
from .fuel_without_direct_replacement import FuelWithoutDirectReplacement


@dataclass(kw_only=True)
class TotalEFuelProduction(Energy, CO2eChange, EnergyChange, Invest):
    CO2e_production_based: float
    CO2e_total: float
    demand_electricity: float
    invest_outside: float
    invest_pa_outside: float

    @classmethod
    def calc(
        cls,
        f18: F18,
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
