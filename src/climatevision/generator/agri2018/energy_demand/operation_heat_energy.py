# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div
from ...business2018.b18 import B18
from ...common.energy import EnergyWithPercentage


@dataclass(kw_only=True)
class OperationHeatEnergy(EnergyWithPercentage):
    # Used by p_operation_heat
    area_m2: float
    ratio_energy_to_m2: float

    @classmethod
    def calc(  # type: ignore
        cls, inputs: Inputs, b18: B18, energy: float, total_energy: float
    ):
        area_m2 = (
            b18.p_nonresi.area_m2
            * inputs.fact("Fact_A_P_energy_buildings_ratio_A_to_B")
            / (1 - inputs.fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
        )
        ratio_energy_to_m2 = div(energy, area_m2)

        return cls(
            energy=energy,
            total_energy=total_energy,
            ratio_energy_to_m2=ratio_energy_to_m2,
            area_m2=area_m2,
        )
