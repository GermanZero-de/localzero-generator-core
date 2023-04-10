# pyright: strict

from dataclasses import dataclass

from ..common.co2_equivalent_emission import CO2eEmission
from ..common.energy_with_co2e import EnergyWithCO2e

from .energy_demand import (
    Energy,
    EnergyPerM2WithBuildings,
    EnergyPerM2PctCommune,
)
from .dataclasses import (
    Vars5,
    Vars6,
    Vars7,
    Vars8,
    Vars10,
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
    s_gas: Vars6
    s_lpg: Vars6
    s_petrol: Vars6
    s_jetfuel: Vars6
    s_diesel: Vars6
    s_fueloil: Vars6
    s_biomass: Vars7
    s_coal: Vars6
    s_heatnet: Vars6
    s_elec_heating: Vars8
    s_heatpump: Vars6
    s_solarth: Vars6
    s_elec: Vars8
    rb: EnergyWithCO2e
    rp_p: Vars10
