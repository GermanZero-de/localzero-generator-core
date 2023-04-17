# pyright: strict

from dataclasses import dataclass

from .energy import Energy
from .co2_equivalent_emission import CO2eEmission


@dataclass(kw_only=True)
class EnergyWithCO2e(Energy, CO2eEmission):
    pass
