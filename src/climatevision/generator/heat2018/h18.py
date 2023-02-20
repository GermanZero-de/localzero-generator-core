# pyright: strict

from dataclasses import dataclass

from ..common.co2_emission import CO2eEmission

from .energy_demand import EnergyDemand
from .energy_production import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class H18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand

    h: CO2eEmission

    p: EnergyWithCO2ePerMWh
    p_gas: EnergyWithCO2ePerMWh
    p_lpg: EnergyWithCO2ePerMWh
    p_fueloil: EnergyWithCO2ePerMWh
    p_opetpro: EnergyWithCO2ePerMWh
    p_coal: EnergyWithCO2ePerMWh
    p_heatnet: EnergyWithCO2ePerMWh
    p_heatnet_cogen: EnergyWithCO2ePerMWh
    p_heatnet_plant: EnergyWithCO2ePerMWh
    p_heatnet_geoth: EnergyWithCO2ePerMWh
    p_heatnet_lheatpump: EnergyWithCO2ePerMWh
    p_biomass: EnergyWithCO2ePerMWh
    p_ofossil: EnergyWithCO2ePerMWh
    p_orenew: EnergyWithCO2ePerMWh
    p_solarth: EnergyWithCO2ePerMWh
    p_heatpump: EnergyWithCO2ePerMWh
