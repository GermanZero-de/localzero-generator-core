# pyright: strict

from dataclasses import dataclass

from .energy_demand import EnergyDemand
from .energy_production.eFuelProduction import EFuelProduction
from .energy_production.fuelWithoutDirectReplacement import FuelWithoutDirectReplacement
from .energy_production.newEFuelProduction import NewEFuelProduction
from .energy_production.eFuels import EFuels
from .energy_production.totalEFuelProduction import TotalEFuelProduction
from .f import F


@dataclass(kw_only=True)
class F30:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
    d_e_hydrogen_reconv: EnergyDemand
    # TODO: Rename those to p_eptrol, p_ejetfuel, ...
    p_petrol: EFuelProduction
    p_jetfuel: EFuelProduction
    p_diesel: EFuelProduction
    p_bioethanol: FuelWithoutDirectReplacement
    p_biodiesel: FuelWithoutDirectReplacement
    p_biogas: FuelWithoutDirectReplacement
    p_emethan: NewEFuelProduction
    p_hydrogen: NewEFuelProduction
    p_hydrogen_reconv: NewEFuelProduction
    p_hydrogen_total: EnergyDemand  # Actually this is total hydrogen production
    p_efuels: EFuels
    f: F
    p: TotalEFuelProduction
