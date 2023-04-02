# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...common.invest import Invest
from ...agri2018.a18 import A18

from .energy_change_agri import EnergyChangeAgri
from .energy_change_p_operation_vehicles import EnergyChangePOperationVehicles
from .energy_change_p_operation_heat import EnergyChangePOperationHeat
from .energy_change_p_operation_elec_elcon import EnergyChangePOperationElecElcon
from .energy_change_p_operation_elec_heatpump import EnergyChangePOperationElecHeatpump


@dataclass(kw_only=True)
class EnergyChangePOperation(EnergyChangeAgri, Invest):
    demand_biomass: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    operation_vehicles: InitVar[EnergyChangePOperationVehicles]
    operation_heat: InitVar[EnergyChangePOperationHeat]
    operation_elec_elcon: InitVar[EnergyChangePOperationElecElcon]
    operation_elec_heatpump: InitVar[EnergyChangePOperationElecHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        operation_vehicles: EnergyChangePOperationVehicles,
        operation_heat: EnergyChangePOperationHeat,
        operation_elec_elcon: EnergyChangePOperationElecElcon,
        operation_elec_heatpump: EnergyChangePOperationElecHeatpump,
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

        EnergyChangeAgri.__post_init__(self, inputs=inputs, what=what, a18=a18)
