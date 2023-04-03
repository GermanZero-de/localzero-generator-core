# pyright: strict

from dataclasses import dataclass

from ..utils import MILLION
from ..common.energy import EnergyWithPercentage


@dataclass(kw_only=True)
class Vars0:
    # Used by b
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8(EnergyWithPercentage):
    CO2e_combustion_based: float = 0
    CO2e_combustion_based_per_MWh: float
    CO2e_total: float = 0

    def __post_init__(self, total_energy: float):
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh
        self.CO2e_total = self.CO2e_combustion_based

        EnergyWithPercentage.__post_init__(self, total_energy)


@dataclass(kw_only=True)
class Vars6(Vars8):
    CO2e_combustion_based: float = 0
    CO2e_combustion_based_per_MWh: float
    CO2e_total: float = 0
    cost_fuel: float = 0
    cost_fuel_per_MWh: float

    def __post_init__(self, total_energy: float):
        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION

        Vars8.__post_init__(self, total_energy)


@dataclass(kw_only=True)
class Vars7(Vars6):
    number_of_buildings: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9:
    # Used by rb
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars10:
    # Used by rp_p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
