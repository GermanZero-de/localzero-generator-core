# pyright: strict

from dataclasses import dataclass

from ..common.co2eEmissions import CO2eEmissions

from .energy_demand import EnergyDemand
from .energy_production import HeatProduction


@dataclass(kw_only=True)
class H18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand

    h: CO2eEmissions

    p: HeatProduction
    p_gas: HeatProduction
    p_lpg: HeatProduction
    p_fueloil: HeatProduction
    p_opetpro: HeatProduction
    p_coal: HeatProduction
    p_heatnet: HeatProduction
    p_heatnet_cogen: HeatProduction
    p_heatnet_plant: HeatProduction
    p_heatnet_geoth: HeatProduction
    p_heatnet_lheatpump: HeatProduction
    p_biomass: HeatProduction
    p_ofossil: HeatProduction
    p_orenew: HeatProduction
    p_solarth: HeatProduction
    p_heatpump: HeatProduction
