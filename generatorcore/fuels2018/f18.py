# pyright: strict
from dataclasses import dataclass

from .dataclasses import EnergyDemand, FuelProduction, TotalFuelProduction, F


@dataclass
class F18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
    p_petrol: FuelProduction
    p_jetfuel: FuelProduction
    p_diesel: FuelProduction
    p_bioethanol: FuelProduction
    p_biodiesel: FuelProduction
    p_biogas: FuelProduction

    p: TotalFuelProduction
    f: F
