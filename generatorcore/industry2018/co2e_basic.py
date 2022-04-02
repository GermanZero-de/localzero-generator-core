# pyright: strict
from dataclasses import dataclass
from ..inputs import Inputs


@dataclass(kw_only=True)
class CO2e_basic:
    # Used by p_other_2efgh
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float

    @classmethod
    def calc_p_other_2efgh(
        cls, inputs: Inputs, p_other_further_energy: float
    ) -> "CO2e_basic":

        CO2e_production_based_per_MWh = inputs.fact(
            "Fact_I_P_other_2efgh_ratio_CO2e_pb_to_fec_2018"
        )
        CO2e_production_based = p_other_further_energy * CO2e_production_based_per_MWh
        CO2e_total = CO2e_production_based

        return cls(
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )
