# pyright: strict

from dataclasses import dataclass

from ..utils import div


@dataclass(kw_only=True)
class Vars3:
    # Used by p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4:
    CO2e_combustion_based: float
    CO2e_combustion_based_per_MWh: float
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        energy: float,
        demand_total_energy: float,
        CO2e_production_based_per_MWh: float,
        CO2e_combustion_based_per_MWh: float,
    ):
        self.energy = energy
        self.pct_energy = div(energy, demand_total_energy)

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_combustion_based_per_MWh = CO2e_combustion_based_per_MWh

        self.CO2e_production_based = energy * CO2e_production_based_per_MWh
        self.CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based


@dataclass(kw_only=True)
class Vars5:
    # Used by p_lpg, p_fueloil, p_heatnet_cogen, p_heatnet_plant
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6:
    # Used by p_heatnet
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7:
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        p_heatnet_energy: float,
    ):
        self.pct_energy = 0  # TODO: Check, why everything is 0
        self.energy = self.pct_energy * p_heatnet_energy

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based


@dataclass(kw_only=True)
class Vars8FromEnergy:
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        energy: float,
        demand_total_energy: float,
        CO2e_production_based_per_MWh: float,
    ):
        self.energy = energy
        self.pct_energy = div(energy, demand_total_energy)

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_production_based = energy * CO2e_production_based_per_MWh

        self.CO2e_total = self.CO2e_production_based


@dataclass(kw_only=True)
class Vars8FromEnergySum:
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        energy: float,
        demand_total_energy: float,
        CO2e_production_based_per_MWh: float,
        CO2e_production_based: float,
    ):
        self.energy = energy
        self.pct_energy = div(energy, demand_total_energy)

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_production_based = CO2e_production_based
        self.CO2e_total = self.CO2e_production_based


@dataclass(kw_only=True)
class Vars8FromEnergyPct:
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float
    pct_energy: float

    def __init__(
        self,
        pct_energy: float,
        p_orenew_energy: float,
        CO2e_production_based_per_MWh: float,
    ):
        self.pct_energy = pct_energy
        self.energy = p_orenew_energy * pct_energy

        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.CO2e_production_based = self.energy * self.CO2e_production_based_per_MWh
        self.CO2e_total = self.CO2e_production_based
