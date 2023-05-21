# pyright: strict

from dataclasses import dataclass

from ..common.co2_equivalent_emission import CO2eEmission
from ..common.energy_with_co2e import EnergyWithCO2e

from .energy_demand import (
    Energy,
    EnergyPerM2WithBuildings,
    EnergyPerM2PctCommune,
)
from .energy_source import (
    Vars5,
    EnergyWithCO2ePerMWhAndCostFuel,
    EnergyWithCO2ePerMWhAndCostFuelAndBuildings,
    EnergyWithCO2ePerMWh,
)


@dataclass(kw_only=True)
class B18:
    b: CO2eEmission
    p: Energy
    p_nonresi: EnergyPerM2WithBuildings
    p_nonresi_com: EnergyPerM2PctCommune
    p_elec_elcon: Energy
    p_elec_heatpump: Energy
    p_vehicles: Energy
    p_other: Energy
    s: Vars5
    s_gas: EnergyWithCO2ePerMWhAndCostFuel
    s_lpg: EnergyWithCO2ePerMWhAndCostFuel
    s_petrol: EnergyWithCO2ePerMWhAndCostFuel
    s_jetfuel: EnergyWithCO2ePerMWhAndCostFuel
    s_diesel: EnergyWithCO2ePerMWhAndCostFuel
    s_fueloil: EnergyWithCO2ePerMWhAndCostFuel
    s_biomass: EnergyWithCO2ePerMWhAndCostFuelAndBuildings
    s_coal: EnergyWithCO2ePerMWhAndCostFuel
    s_heatnet: EnergyWithCO2ePerMWhAndCostFuel
    s_elec_heating: EnergyWithCO2ePerMWh
    s_heatpump: EnergyWithCO2ePerMWhAndCostFuel
    s_solarth: EnergyWithCO2ePerMWhAndCostFuel
    s_elec: EnergyWithCO2ePerMWh
    rb: EnergyWithCO2e
