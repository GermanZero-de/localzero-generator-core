# pyright: strict

from dataclasses import dataclass, InitVar

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18

from .co2e_change_energy_agri import CO2eChangeEnergyAgri


@dataclass(kw_only=True)
class CO2eChangePOperationVehicles(CO2eChangeEnergyAgri):
    demand_biomass: float = 0
    demand_change: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_emethan: float = 0
    demand_epetrol: float = 0
    demand_heatpump: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
    ):

        self.demand_electricity = 0
        self.demand_biomass = 0
        self.demand_heatpump = 0
        self.demand_emethan = 0

        self.demand_change = inputs.ass("Ass_B_D_fec_vehicles_change")
        self.energy = getattr(a18, what).energy * (1 + self.demand_change)

        self.demand_epetrol = div(
            self.energy * a18.s_petrol.energy,
            a18.s_petrol.energy + a18.s_diesel.energy,
        )
        self.demand_ediesel = div(
            self.energy * a18.s_diesel.energy,
            a18.s_petrol.energy + a18.s_diesel.energy,
        )

        parent = CO2eChangeEnergyAgri(
            inputs=inputs, what=what, a18=a18, energy=self.energy
        )

        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct
