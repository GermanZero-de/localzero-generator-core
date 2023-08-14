# pyright: strict

from dataclasses import dataclass

from ...utils import div


@dataclass(kw_only=True)
class Energy:
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyDemand(Energy):
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyDemandWithCostFuel(EnergyDemand):
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore


def calc_energy_demand(
    energy: float, energy_18: float, cost_fuel_per_MWh: float
) -> EnergyDemandWithCostFuel:
    d = EnergyDemandWithCostFuel()
    d.energy = energy
    d.cost_fuel_per_MWh = cost_fuel_per_MWh
    d.change_energy_MWh = energy - energy_18
    d.change_energy_pct = div(d.change_energy_MWh, energy_18)
    return d
