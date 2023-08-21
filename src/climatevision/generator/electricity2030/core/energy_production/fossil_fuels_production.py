# pyright: strict

from dataclasses import dataclass

from ....utils import div


@dataclass(kw_only=True)
class FossilFuelsProduction:
    """This describes energy produced by fossil fuels. Which we do not do in 2030, so this
    just describes the effect of shutting those energy providers down."""

    energy: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_combustion_based: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore

    @classmethod
    def sum(
        cls,
        *ffs: "FossilFuelsProduction",
        energy_18: float,
        CO2e_total_18: float,
    ) -> "FossilFuelsProduction":
        energy = sum(ff.energy for ff in ffs)
        CO2e_total_2021_estimated = sum(ff.CO2e_total_2021_estimated for ff in ffs)
        cost_fuel = sum(ff.cost_fuel for ff in ffs)
        cost_mro = sum(ff.cost_mro for ff in ffs)
        CO2e_combustion_based = sum(ff.CO2e_combustion_based for ff in ffs)
        change_cost_energy = sum(ff.change_cost_energy for ff in ffs)
        change_cost_mro = sum(ff.change_cost_mro for ff in ffs)
        cost_climate_saved = sum(ff.cost_climate_saved for ff in ffs)
        change_CO2e_t = sum(ff.change_CO2e_t for ff in ffs)

        change_energy_MWh = energy - energy_18

        return FossilFuelsProduction(
            energy=energy,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=div(change_energy_MWh, energy_18),
            cost_fuel=cost_fuel,
            cost_mro=cost_mro,
            CO2e_combustion_based=CO2e_combustion_based,
            change_cost_energy=change_cost_energy,
            change_cost_mro=change_cost_mro,
            cost_climate_saved=cost_climate_saved,
            change_CO2e_t=change_CO2e_t,
            change_CO2e_pct=div(change_CO2e_t, CO2e_total_18),
        )
