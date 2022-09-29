# pyright: strict

from dataclasses import dataclass

from ..common.co2eEmissions import CO2eEmissions

from .energy_demand import EnergyDemand
from .dataclasses import (
    Vars3,
    Vars4,
    Vars6,
    Vars8FromEnergySum,
    Vars8FromEnergyPct,
)


@dataclass(kw_only=True)
class H18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand

    h: CO2eEmissions

    p: Vars3
    p_gas: Vars4
    p_lpg: Vars4
    p_fueloil: Vars4
    p_opetpro: Vars4
    p_coal: Vars4
    p_heatnet: Vars6
    p_heatnet_cogen: Vars4
    p_heatnet_plant: Vars4
    p_heatnet_geoth: Vars4
    p_heatnet_lheatpump: Vars4
    p_biomass: Vars4
    p_ofossil: Vars4
    p_orenew: Vars8FromEnergySum
    p_solarth: Vars8FromEnergyPct
    p_heatpump: Vars8FromEnergyPct
