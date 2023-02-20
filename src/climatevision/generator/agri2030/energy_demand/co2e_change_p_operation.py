# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...common.invest import Invest
from ...agri2018.a18 import A18

from .co2e_change_energy import CO2eChangeEnergy
from .co2e_change_p_operation_vehicles import CO2eChangePOperationVehicles
from .co2e_change_p_operation_heat import CO2eChangePOperationHeat
from .co2e_change_p_operation_elec_elcon import CO2eChangePOperationElecElcon
from .co2e_change_p_operation_elec_heatpump import CO2eChangePOperationElecHeatpump


@dataclass(kw_only=True)
class CO2eChangePOperation(CO2eChangeEnergy, Invest):
    demand_biomass: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    operation_vehicles: InitVar[CO2eChangePOperationVehicles]
    operation_heat: InitVar[CO2eChangePOperationHeat]
    operation_elec_elcon: InitVar[CO2eChangePOperationElecElcon]
    operation_elec_heatpump: InitVar[CO2eChangePOperationElecHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        operation_vehicles: CO2eChangePOperationVehicles,
        operation_heat: CO2eChangePOperationHeat,
        operation_elec_elcon: CO2eChangePOperationElecElcon,
        operation_elec_heatpump: CO2eChangePOperationElecHeatpump,
    ):
        self.demand_epetrol = operation_vehicles.demand_epetrol
        self.demand_ediesel = operation_vehicles.demand_ediesel
        self.demand_heatpump = operation_heat.demand_heatpump
        self.demand_emplo = operation_heat.demand_emplo
        self.demand_emplo_new = operation_heat.demand_emplo_new
        self.demand_biomass = operation_heat.demand_biomass
        self.demand_electricity = (
            operation_elec_elcon.demand_electricity
            + operation_elec_heatpump.demand_electricity
        )
        self.demand_emethan = operation_heat.demand_emethan

        self.energy = (
            operation_heat.energy
            + operation_elec_elcon.energy
            + operation_elec_heatpump.energy
            + operation_vehicles.energy
        )

        self.invest = operation_heat.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target
        self.cost_wage = operation_heat.cost_wage

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct
