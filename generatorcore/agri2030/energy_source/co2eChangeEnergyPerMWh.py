# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChange


@dataclass(kw_only=True)
class CO2eChangeEnergyPerMWh(CO2eChange):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_production_based = 0
        self.CO2e_combustion_based_per_MWh = getattr(
            a18, what
        ).CO2e_combustion_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved
