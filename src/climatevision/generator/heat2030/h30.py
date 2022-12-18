# pyright: strict

from dataclasses import dataclass

from .dataclasses import (
    Vars0,
    Vars5,
    Vars6,
    Vars9,
    Vars10,
    Vars11,
    Vars12,
    Vars13,
    Vars14,
)
from .energy_demand import EnergyDemand
from .energy_general import G, GStorage, GPlanning


@dataclass(kw_only=True)
class H30:
    h: Vars0
    g: G
    g_storage: GStorage
    g_planning: GPlanning
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
    p: Vars5
    p_gas: Vars6
    p_lpg: Vars9
    p_fueloil: Vars6
    p_opetpro: Vars9
    p_coal: Vars6
    p_heatnet: Vars10
    p_heatnet_cogen: Vars9
    p_heatnet_plant: Vars11
    p_heatnet_lheatpump: Vars12
    p_heatnet_geoth: Vars13
    p_biomass: Vars14
    p_ofossil: Vars9
    p_orenew: Vars9
    p_solarth: Vars9
    p_heatpump: Vars9

    # for pdf
    p_fossil_change_CO2e_t: float = None  # type: ignore
