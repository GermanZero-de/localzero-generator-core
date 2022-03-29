# pyright: strict
from dataclasses import dataclass
from .co2e_per_t import CO2e_per_t
from ..inputs import Inputs
from .co2e import CO2e


@dataclass
class CO2e_with_pct_energy(CO2e):
    # Used by p_metal_steel
    pct_energy: float = 0

    @classmethod
    def calc_p_metal_steel(
        cls,
        inputs: Inputs,
        p_metal_steel_pct_energy: float,
        p_metal_steel_energy: float,
        p_metal_steel_primary: CO2e_per_t,
        p_metal_steel_secondary: CO2e_per_t,
    ) -> "CO2e_with_pct_energy":

        pct_energy = p_metal_steel_pct_energy
        energy = p_metal_steel_energy

        prod_volume = (
            p_metal_steel_primary.prod_volume + p_metal_steel_secondary.prod_volume
        )

        CO2e_production_based = (
            p_metal_steel_primary.CO2e_production_based
            + p_metal_steel_secondary.CO2e_production_based
        )
        CO2e_combustion_based = (
            p_metal_steel_primary.CO2e_combustion_based
            + p_metal_steel_secondary.CO2e_combustion_based
        )
        CO2e_total = (
            p_metal_steel_primary.CO2e_total + p_metal_steel_secondary.CO2e_total
        )

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
            energy=energy,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )
