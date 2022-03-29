# pyright: strict
from dataclasses import dataclass
from ..inputs import Inputs
from .co2e import CO2e


@dataclass
class CO2e_per_MWh(CO2e):
    # Used by p_other_further
    CO2e_combustion_based_per_MWh: float = 0
    CO2e_production_based_per_MWh: float = 0
    pct_energy: float = 0

    @classmethod
    def calc_p_other_further(
        cls, inputs: Inputs, p_other_energy: float
    ) -> "CO2e_per_MWh":

        pct_energy = inputs.fact("Fact_I_P_other_fec_pct_of_further_2018")
        energy = p_other_energy * pct_energy

        CO2e_production_based_per_MWh = inputs.fact(
            "Fact_I_P_other_2d_ratio_CO2e_pb_to_fec_2018"
        )
        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based_per_MWh = inputs.fact(
            "Fact_I_P_other_further_ratio_CO2e_cb_to_fec_2018"
        )
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        prod_volume = inputs.fact("Fact_I_P_other_further_prodvol_2018")

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
            energy=energy,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )
