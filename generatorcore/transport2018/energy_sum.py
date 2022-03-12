# pyright: strict
from dataclasses import dataclass


@dataclass
class EnergySum:
    # Used by s, s_petrol, s_jetfuel, s_diesel, s_fueloil, s_lpg, s_gas, s_biogas, s_bioethanol, s_biodiesel, s_elec
    energy: float
