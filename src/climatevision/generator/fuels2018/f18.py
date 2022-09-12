# pyright: strict

from dataclasses import dataclass

from ..commonDataclasses.co2eEmissions import CO2eEmissions

from .energy_demand import EnergyDemand
from .energy_production import FuelProduction, TotalFuelProduction


@dataclass(kw_only=True)
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

    f: CO2eEmissions
