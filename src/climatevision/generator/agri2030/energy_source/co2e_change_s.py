# pyright: strict
from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...common.invest import Invest
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChange

from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh
from .co2e_change_fuel_oil_gas import CO2eChangeFuelOilGas
from .co2e_change_fuel_emethan import CO2eChangeFuelEmethan
from .co2e_change_fuel_heatpump import CO2eChangeFuelHeatpump


@dataclass(kw_only=True)
class CO2eChangeS(CO2eChange, Invest):
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    energy: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    petrol: InitVar[CO2eChangeEnergyPerMWh]
    diesel: InitVar[CO2eChangeEnergyPerMWh]
    fueloil: InitVar[CO2eChangeFuelOilGas]
    lpg: InitVar[CO2eChangeEnergyPerMWh]
    gas: InitVar[CO2eChangeFuelOilGas]
    emethan: InitVar[CO2eChangeFuelEmethan]
    biomass: InitVar[CO2eChangeEnergyPerMWh]
    elec: InitVar[CO2eChangeEnergyPerMWh]
    heatpump: InitVar[CO2eChangeFuelHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        petrol: CO2eChangeEnergyPerMWh,
        diesel: CO2eChangeEnergyPerMWh,
        fueloil: CO2eChangeFuelOilGas,
        lpg: CO2eChangeEnergyPerMWh,
        gas: CO2eChangeFuelOilGas,
        emethan: CO2eChangeFuelEmethan,
        biomass: CO2eChangeEnergyPerMWh,
        elec: CO2eChangeEnergyPerMWh,
        heatpump: CO2eChangeFuelHeatpump,
    ):

        self.CO2e_production_based = 0
        self.CO2e_combustion_based = (
            petrol.CO2e_combustion_based
            + diesel.CO2e_combustion_based
            + fueloil.CO2e_combustion_based
            + lpg.CO2e_combustion_based
            + gas.CO2e_combustion_based
            + emethan.CO2e_combustion_based
            + biomass.CO2e_combustion_based
            + elec.CO2e_combustion_based
            + heatpump.CO2e_combustion_based
        )

        self.invest = heatpump.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.energy = (
            petrol.energy
            + diesel.energy
            + fueloil.energy
            + lpg.energy
            + gas.energy
            + emethan.energy
            + biomass.energy
            + elec.energy
            + heatpump.energy
        )
        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        self.demand_emplo = heatpump.demand_emplo
        self.demand_emplo_new = heatpump.demand_emplo_new

        self.cost_wage = heatpump.cost_wage

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
