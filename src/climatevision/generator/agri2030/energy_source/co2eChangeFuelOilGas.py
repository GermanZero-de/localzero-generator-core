# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from .co2eChangeEnergyPerMWh import CO2eChangeEnergyPerMWh


@dataclass(kw_only=True)
class CO2eChangeFuelOilGas(CO2eChangeEnergyPerMWh):
    area_m2: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0
        self.area_m2 = 0

        parent = CO2eChangeEnergyPerMWh(
            inputs=inputs,
            what=what,
            a18=a18,
            energy=self.energy,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_combustion_based_per_MWh = parent.CO2e_combustion_based_per_MWh
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved
        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct
