# pyright: strict
from dataclasses import dataclass, InitVar

from ...refdata import Facts
from ...utils import div
from ...common.invest import Invest
from ...agri2018.a18 import A18

from ..energy_demand import CO2eChangeAgri

from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh
from .co2e_change_fuel_oil_gas import CO2eChangeFuelOilGas
from .co2e_change_fuel_emethan import CO2eChangeFuelEmethan
from .co2e_change_fuel_heatpump import CO2eChangeFuelHeatpump


@dataclass(kw_only=True)
class CO2eChangeS(CO2eChangeAgri, Invest):
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    energy: float = 0

    facts: InitVar[Facts]
    duration_CO2e_neutral_years: InitVar[float]
    what: InitVar[str]
    a18: InitVar[A18]
    duration_until_target_year: InitVar[int]
    petrol: InitVar[CO2eChangeEnergyPerMWh]
    diesel: InitVar[CO2eChangeEnergyPerMWh]
    fueloil: InitVar[CO2eChangeFuelOilGas]
    lpg: InitVar[CO2eChangeEnergyPerMWh]
    gas: InitVar[CO2eChangeFuelOilGas]
    emethan: InitVar[CO2eChangeFuelEmethan]
    biomass: InitVar[CO2eChangeEnergyPerMWh]
    elec: InitVar[CO2eChangeEnergyPerMWh]
    heatpump: InitVar[CO2eChangeFuelHeatpump]

    def __post_init__(  # type: ignore[override]
        self,
        facts: Facts,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
        duration_until_target_year: int,
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
        self.invest_pa = self.invest / duration_until_target_year

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

        CO2eChangeAgri.__post_init__(
            self,
            facts=facts,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
        )
