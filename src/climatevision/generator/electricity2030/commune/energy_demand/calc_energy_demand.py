# pyright: strict

from ....refdata import Facts
from ....utils import div

from ...core.energy import EnergyDemandWithCostFuel


def calc_energy_demand(
    facts: Facts, *, energy: float, energy_18: float, cost_fuel_per_MWh: str
) -> EnergyDemandWithCostFuel:
    d = EnergyDemandWithCostFuel()
    d.energy = energy
    d.cost_fuel_per_MWh = facts.fact(cost_fuel_per_MWh)
    d.change_energy_MWh = energy - energy_18
    d.change_energy_pct = div(d.change_energy_MWh, energy_18)
    return d
