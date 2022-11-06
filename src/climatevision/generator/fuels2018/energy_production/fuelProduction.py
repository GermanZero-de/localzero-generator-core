# pyright: strict

from dataclasses import dataclass

from ...common.energyWithCO2ePerMWh import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class TotalFuelProduction:
    CO2e_production_based: float
    CO2e_combustion_based: float
    CO2e_total: float
    energy: float

    def __init__(self, *fuel_productions: EnergyWithCO2ePerMWh):
        self.CO2e_production_based = sum(
            p.CO2e_production_based for p in fuel_productions
        )
        self.CO2e_combustion_based = sum(
            p.CO2e_combustion_based for p in fuel_productions
        )
        self.energy = sum(p.energy for p in fuel_productions)
        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based
