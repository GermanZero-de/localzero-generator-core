# pyright: strict

from dataclasses import dataclass, InitVar

from ...refdata import Assumptions
from ...agri2018.a18 import A18

from .energy_change_agri import EnergyChangeAgri


@dataclass(kw_only=True)
class EnergyChangePOperationElecElcon(EnergyChangeAgri):
    demand_biomass: float = 0
    demand_change: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_heatpump: float = 0

    assumptions: InitVar[Assumptions]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(  # type: ignore[override]
        self,
        what: str,
        a18: A18,
        assumptions: Assumptions,
    ):
        ass = assumptions.ass

        self.demand_biomass = 0
        self.demand_heatpump = 0
        self.demand_ediesel = 0
        self.demand_emethan = 0

        self.demand_change = ass("Ass_B_D_fec_elec_elcon_change")
        self.energy = getattr(a18, what).energy * (1 + self.demand_change)

        self.demand_electricity = self.energy

        EnergyChangeAgri.__post_init__(self, what=what, a18=a18)
