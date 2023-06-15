# pyright: strict

from dataclasses import dataclass, InitVar

from ...refdata import Facts
from ...agri2018.a18 import A18

from .energy_change_agri import EnergyChangeAgri
from .energy_change_p_operation_heat import EnergyChangePOperationHeat


@dataclass(kw_only=True)
class EnergyChangePOperationElecHeatpump(EnergyChangeAgri):
    demand_electricity: float = 0

    what: InitVar[str]
    a18: InitVar[A18]
    facts: InitVar[Facts]
    operation_heat: InitVar[EnergyChangePOperationHeat]

    def __post_init__(  # type: ignore[override]
        self,
        what: str,
        a18: A18,
        facts: Facts,
        operation_heat: EnergyChangePOperationHeat,
    ):
        fact = facts.fact

        self.energy = operation_heat.demand_heatpump / fact(
            "Fact_R_S_heatpump_mean_annual_performance_factor_all"
        )
        self.demand_electricity = self.energy

        EnergyChangeAgri.__post_init__(self, what=what, a18=a18)
