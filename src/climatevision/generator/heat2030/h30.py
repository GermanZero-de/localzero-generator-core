# pyright: strict

from dataclasses import dataclass

from .dataclasses import (
    H,
    TotalHeatProduction,
    HeatProductionWithCostFuel,
    HeatProduction,
    HeatnetProduction,
    HeatnetPlantProduction,
    HeatnetLheatpumpProduction,
    HeatnetGeothProduction,
)
from .energy_demand import EnergyDemand
from .energy_general import G, GStorage, GPlanning


@dataclass(kw_only=True)
class H30:
    h: H
    g: G
    g_storage: GStorage
    g_planning: GPlanning
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
    p: TotalHeatProduction
    p_gas: HeatProductionWithCostFuel
    p_lpg: HeatProduction
    p_fueloil: HeatProductionWithCostFuel
    p_opetpro: HeatProduction
    p_coal: HeatProductionWithCostFuel
    p_heatnet: HeatnetProduction
    p_heatnet_cogen: HeatProduction
    p_heatnet_plant: HeatnetPlantProduction
    p_heatnet_lheatpump: HeatnetLheatpumpProduction
    p_heatnet_geoth: HeatnetGeothProduction
    p_biomass: HeatProductionWithCostFuel
    p_ofossil: HeatProduction
    p_orenew: HeatProduction
    p_solarth: HeatProduction
    p_heatpump: HeatProduction

    # for pdf
    p_fossil_change_CO2e_t: float = None  # type: ignore
