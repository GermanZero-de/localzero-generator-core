# pyright: strict

from dataclasses import dataclass

from ..common.co2_equivalent_emission import CO2eEmission

from .energy_demand import EnergyDemand
from .energy_production import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class F18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand

    p_petrol: EnergyWithCO2ePerMWh
    p_jetfuel: EnergyWithCO2ePerMWh
    p_diesel: EnergyWithCO2ePerMWh
    p_bioethanol: EnergyWithCO2ePerMWh
    p_biodiesel: EnergyWithCO2ePerMWh
    p_biogas: EnergyWithCO2ePerMWh
    p: EnergyWithCO2ePerMWh

    f: CO2eEmission
