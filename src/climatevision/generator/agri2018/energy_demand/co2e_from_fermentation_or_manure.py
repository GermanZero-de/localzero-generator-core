# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts
from ...common.co2_equivalent_emission import CO2eEmission


@dataclass(kw_only=True)
class CO2eFromFermentationOrManure(CO2eEmission):
    # Used by p_fermen_dairycow, p_fermen_nondairy, p_fermen_swine, p_fermen_poultry, p_fermen_oanimal, p_manure_dairycow, p_manure_nondairy, p_manure_swine, p_manure_poultry, p_manure_oanimal, p_manure_deposition
    CO2e_production_based_per_t: float
    amount: float

    @classmethod
    def calc_fermen(
        cls, entries: Entries, facts: Facts, what: str, alias: str | None = None
    ) -> "CO2eFromFermentationOrManure":
        fact = facts.fact

        CO2e_combustion_based = 0.0
        # This line and the next might just be a little too cute.
        # They make the callsite nice and short, but forego any type checking
        # I'll keep it like this for now, but this is one of the places where
        # a better overall design is probably lurking somewhere
        CO2e_production_based_per_t = fact(
            "Fact_A_P_fermen_" + what + "_ratio_CO2e_to_amount_2018"
        )
        # Also don't ask me why we called swine swine except when we called them pig
        amount = getattr(
            entries, "a_fermen_" + (what if alias is None else alias) + "_amount"
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
        cls, entries: Entries, what: str, amount: float
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = getattr(
            entries, "a_manure_" + what + "_ratio_CO2e_to_amount"
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
        entries: Entries,
        fermen_dairycow: "CO2eFromFermentationOrManure",
        fermen_nondairy: "CO2eFromFermentationOrManure",
        fermen_swine: "CO2eFromFermentationOrManure",
        fermen_oanimal: "CO2eFromFermentationOrManure",
    ) -> "CO2eFromFermentationOrManure":
        """This computes the deposition of reactive nitrogen of animals (excluding poultry)"""

        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = entries.a_manure_deposition_ratio_CO2e_to_amount
        amount = (
            fermen_dairycow.amount
            + fermen_nondairy.amount
            + fermen_swine.amount
            + fermen_oanimal.amount
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
