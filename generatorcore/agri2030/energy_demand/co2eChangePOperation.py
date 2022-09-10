# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from .co2eChangeEnergy import CO2eChangeEnergy
from .co2eChangePOperationVehicles import CO2eChangePOperationVehicles
from .co2eChangePOperationHeat import CO2eChangePOperationHeat
from .co2eChangePOperationElecElcon import CO2eChangePOperationElecElcon
from .co2eChangePOperationElecHeatpump import CO2eChangePOperationElecHeatpump


@dataclass(kw_only=True)
class CO2eChangePOperation(CO2eChangeEnergy):
    cost_wage: float = 0
    demand_biomass: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0
    invest: float = 0
    invest_pa: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    p_operation_vehicles: InitVar[CO2eChangePOperationVehicles]
    p_operation_heat: InitVar[CO2eChangePOperationHeat]
    p_operation_elec_elcon: InitVar[CO2eChangePOperationElecElcon]
    p_operation_elec_heatpump: InitVar[CO2eChangePOperationElecHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation_vehicles: CO2eChangePOperationVehicles,
        p_operation_heat: CO2eChangePOperationHeat,
        p_operation_elec_elcon: CO2eChangePOperationElecElcon,
        p_operation_elec_heatpump: CO2eChangePOperationElecHeatpump,
    ):
        self.demand_epetrol = p_operation_vehicles.demand_epetrol
        self.demand_ediesel = p_operation_vehicles.demand_ediesel
        self.demand_heatpump = p_operation_heat.demand_heatpump
        self.demand_emplo = p_operation_heat.demand_emplo
        self.demand_emplo_new = p_operation_heat.demand_emplo_new
        self.demand_biomass = p_operation_heat.demand_biomass
        self.demand_electricity = (
            p_operation_elec_elcon.demand_electricity
            + p_operation_elec_heatpump.demand_electricity
        )
        self.demand_emethan = p_operation_heat.demand_emethan

        self.energy = (
            p_operation_heat.energy
            + p_operation_elec_elcon.energy
            + p_operation_elec_heatpump.energy
            + p_operation_vehicles.energy
        )

        self.invest = p_operation_heat.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target
        self.cost_wage = p_operation_heat.cost_wage

        parent = CO2eChangeEnergy(inputs=inputs, what=what, a18=a18, energy=self.energy)

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct
