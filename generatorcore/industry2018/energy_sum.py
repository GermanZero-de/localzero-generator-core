# pyright: strict
from dataclasses import InitVar, dataclass
from generatorcore.utils import div


@dataclass
class EnergySum:
    # Used by s_fossil, s_renew
    energy: float


@dataclass
class Empty:
    # Used s_renew_hydrogen, s_renew_emethan
    pass


@dataclass
class Energy_pct:
    # Used by s, s_fossil_gas, s_fossil_coal, s_fossil_diesel, s_fossil_fueloil, s_fossil_lpg, s_fossil_opetpro, s_fossil_ofossil, s_renew_biomass, s_renew_heatnet, s_renew_heatpump, s_renew_solarth, s_renew_elec
    energy: float = 0
    pct_energy: float = 0
    total_energy: InitVar[float] = 0

    def __post_init__(self, total_energy: float):
        self.pct_energy = div(self.energy, total_energy)
