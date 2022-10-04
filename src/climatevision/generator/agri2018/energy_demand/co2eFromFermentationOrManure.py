# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from ...common.co2eEmissions import CO2eEmissions


@dataclass(kw_only=True)
class CO2eFromFermentationOrManure(CO2eEmissions):
    # Used by p_fermen_dairycow, p_fermen_nondairy, p_fermen_swine, p_fermen_poultry, p_fermen_oanimal, p_manure_dairycow, p_manure_nondairy, p_manure_swine, p_manure_poultry, p_manure_oanimal, p_manure_deposition
    CO2e_production_based_per_t: float
    amount: float

    @classmethod
    def calc_fermen(
        cls, inputs: Inputs, what: str, alias: str | None = None
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        # This line and the next might just be a little too cute.
        # They make the callsite nice and short, but forego any type checking
        # I'll keep it like this for now, but this is one of the places where
        # a better overall design is probably lurking somewhere
        CO2e_production_based_per_t = inputs.fact(
            "Fact_A_P_fermen_" + what + "_ratio_CO2e_to_amount_2018"
        )
        # Also don't ask me why we called swine swine except when we called them pig
        amount = getattr(
            inputs.entries, "a_fermen_" + (what if alias is None else alias) + "_amount"
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )

    @classmethod
    def calc_manure(
        cls, inputs: Inputs, what: str, amount: float
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = getattr(
            inputs.entries, "a_manure_" + what + "_ratio_CO2e_to_amount"
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )

    @classmethod
    def calc_deposition(
        cls,
        inputs: Inputs,
        p_fermen_dairycow: "CO2eFromFermentationOrManure",
        p_fermen_nondairy: "CO2eFromFermentationOrManure",
        p_fermen_swine: "CO2eFromFermentationOrManure",
        p_fermen_oanimal: "CO2eFromFermentationOrManure",
    ) -> "CO2eFromFermentationOrManure":
        """This computes the deposition of reactive nitrogen of animals (excluding poultry)"""

        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = (
            inputs.entries.a_manure_deposition_ratio_CO2e_to_amount
        )
        amount = (
            p_fermen_dairycow.amount
            + p_fermen_nondairy.amount
            + p_fermen_swine.amount
            + p_fermen_oanimal.amount
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )
