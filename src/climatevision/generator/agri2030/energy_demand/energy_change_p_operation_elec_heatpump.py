# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...agri2018.a18 import A18

from .energy_change_agri import EnergyChangeAgri
from .energy_change_p_operation_heat import EnergyChangePOperationHeat


@dataclass(kw_only=True)
class EnergyChangePOperationElecHeatpump(EnergyChangeAgri):
    demand_electricity: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    operation_heat: InitVar[EnergyChangePOperationHeat]

    def __post_init__(  # type: ignore[override]
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        operation_heat: EnergyChangePOperationHeat,
    ):

        self.energy = operation_heat.demand_heatpump / inputs.fact(
            "Fact_R_S_heatpump_mean_annual_performance_factor_all"
        )
        self.demand_electricity = self.energy

        EnergyChangeAgri.__post_init__(self, inputs=inputs, what=what, a18=a18)
