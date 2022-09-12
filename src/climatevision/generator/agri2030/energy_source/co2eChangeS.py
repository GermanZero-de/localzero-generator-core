# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChange

from .co2eChangeEnergyPerMWh import CO2eChangeEnergyPerMWh
from .co2eChangeFuelOilGas import CO2eChangeFuelOilGas
from .co2eChangeFuelEmethan import CO2eChangeFuelEmethan
from .co2eChangeFuelHeatpump import CO2eChangeFuelHeatpump


@dataclass(kw_only=True)
class CO2eChangeS(CO2eChange):
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    energy: float = 0
    invest: float = 0
    invest_pa: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    s_petrol: InitVar[CO2eChangeEnergyPerMWh]
    s_diesel: InitVar[CO2eChangeEnergyPerMWh]
    s_fueloil: InitVar[CO2eChangeFuelOilGas]
    s_lpg: InitVar[CO2eChangeEnergyPerMWh]
    s_gas: InitVar[CO2eChangeFuelOilGas]
    s_emethan: InitVar[CO2eChangeFuelEmethan]
    s_biomass: InitVar[CO2eChangeEnergyPerMWh]
    s_elec: InitVar[CO2eChangeEnergyPerMWh]
    s_heatpump: InitVar[CO2eChangeFuelHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        s_petrol: CO2eChangeEnergyPerMWh,
        s_diesel: CO2eChangeEnergyPerMWh,
        s_fueloil: CO2eChangeFuelOilGas,
        s_lpg: CO2eChangeEnergyPerMWh,
        s_gas: CO2eChangeFuelOilGas,
        s_emethan: CO2eChangeFuelEmethan,
        s_biomass: CO2eChangeEnergyPerMWh,
        s_elec: CO2eChangeEnergyPerMWh,
        s_heatpump: CO2eChangeFuelHeatpump,
    ):

        self.CO2e_production_based = 0
        self.CO2e_combustion_based = (
            s_petrol.CO2e_combustion_based
            + s_diesel.CO2e_combustion_based
            + s_fueloil.CO2e_combustion_based
            + s_lpg.CO2e_combustion_based
            + s_gas.CO2e_combustion_based
            + s_emethan.CO2e_combustion_based
            + s_biomass.CO2e_combustion_based
            + s_elec.CO2e_combustion_based
            + s_heatpump.CO2e_combustion_based
        )

        self.invest = s_heatpump.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.energy = (
            s_petrol.energy
            + s_diesel.energy
            + s_fueloil.energy
            + s_lpg.energy
            + s_gas.energy
            + s_emethan.energy
            + s_biomass.energy
            + s_elec.energy
            + s_heatpump.energy
        )
        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        self.demand_emplo = s_heatpump.demand_emplo
        self.demand_emplo_new = s_heatpump.demand_emplo_new

        self.cost_wage = s_heatpump.cost_wage

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
