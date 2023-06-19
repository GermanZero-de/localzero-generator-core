# pyright: strict

from dataclasses import dataclass, InitVar

from ...refdata import Assumptions
from ...utils import div
from ...agri2018.a18 import A18

from .energy_change_agri import EnergyChangeAgri


@dataclass(kw_only=True)
class EnergyChangePOperationVehicles(EnergyChangeAgri):
    demand_biomass: float = 0
    demand_change: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0

    what: InitVar[str]
    a18: InitVar[A18]
    assumptions: InitVar[Assumptions]

    def __post_init__(  # type: ignore[override]
        self,
        what: str,
        a18: A18,
        assumptions: Assumptions,
    ):
        ass = assumptions.ass

        self.demand_electricity = 0
        self.demand_biomass = 0
        self.demand_heatpump = 0
        self.demand_emethan = 0

        self.demand_change = ass("Ass_B_D_fec_vehicles_change")
        self.energy = getattr(a18, what).energy * (1 + self.demand_change)

        self.demand_epetrol = div(
            self.energy * a18.s_petrol.energy,
            a18.s_petrol.energy + a18.s_diesel.energy,
        )
        self.demand_ediesel = div(
            self.energy * a18.s_diesel.energy,
            a18.s_petrol.energy + a18.s_diesel.energy,
        )

        EnergyChangeAgri.__post_init__(self, what=what, a18=a18)
