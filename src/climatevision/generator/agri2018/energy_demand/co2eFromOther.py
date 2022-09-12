# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from ..co2eEmissions import CO2eEmissions


@dataclass(kw_only=True)
class CO2eFromOther(CO2eEmissions):
    # Used by p_other_liming_dolomite, p_other_urea, p_other_ecrop, p_other_liming_calcit
    CO2e_production_based_per_t: float
    prod_volume: float

    @classmethod
    def calc(
        cls, inputs: Inputs, what: str, ratio_suffix: str = "_ratio"
    ) -> "CO2eFromOther":
        # No idea why we use ratio_ with
        #   Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018
        # but not with
        #   Fact_A_P_other_urea_CO2e_pb_to_amount_2018
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = inputs.fact(
            "Fact_A_P_other_" + what + ratio_suffix + "_CO2e_pb_to_amount_2018"
        )
        prod_volume = getattr(inputs.entries, "a_other_" + what + "_prod_volume")
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            prod_volume=prod_volume,
        )
