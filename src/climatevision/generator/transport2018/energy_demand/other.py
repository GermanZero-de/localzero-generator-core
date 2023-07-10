# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts
from ...utils import element_wise_plus


@dataclass
class Other:
    CO2e_combustion_based: float
    CO2e_total: float
    transport_capacity_pkm: float

    def __add__(self: "Other", other: "Other") -> "Other":
        return element_wise_plus(self, other)

    @classmethod
    def calc_foot(
        cls,
        facts: Facts,
        population_commune_2018: int,
        area_kind_rt7: str,
    ) -> "Other":
        fact = facts.fact

        if area_kind_rt7 in ["71", "72", "73", "74", "75", "76", "77"]:
            transport_capacity_pkm = (
                population_commune_2018
                * 365
                * fact("Fact_T_D_modal_split_foot_rt" + area_kind_rt7)
            )

        # This happens if we run Local Zero for a Landkreis a Bundesland or Germany.
        # We do not have a area_kind entry in this case and just use the mean mean modal split of germany.
        elif area_kind_rt7 == "nd":
            transport_capacity_pkm = (
                population_commune_2018 * 365 * fact("Fact_T_D_modal_split_foot_nat")
            )
        else:
            assert False, f"Do not know how to handle entries.t_rt7 = {area_kind_rt7}"
        return cls(
            CO2e_total=0,
            CO2e_combustion_based=0,
            transport_capacity_pkm=transport_capacity_pkm,
        )

    @classmethod
    def calc_cycle(
        cls,
        facts: Facts,
        population_commune_2018: int,
        area_kind_rt7: str,
    ) -> "Other":
        fact = facts.fact

        if area_kind_rt7 in ["71", "72", "73", "74", "75", "76", "77"]:
            transport_capacity_pkm = (
                population_commune_2018
                * 365
                * fact("Fact_T_D_modal_split_cycl_rt" + area_kind_rt7)
            )

        # This happens if we run Local Zero for a Landkreis a Bundesland or Germany.
        # We do not have a area_kind entry in this case and just use the mean mean modal split of germany.
        elif area_kind_rt7 == "nd":
            transport_capacity_pkm = (
                population_commune_2018 * 365 * fact("Fact_T_D_modal_split_foot_nat")
            )
        else:
            assert False, f"Do not know how to handle entries.t_rt7 = {area_kind_rt7}"
        return cls(
            CO2e_total=0,
            CO2e_combustion_based=0,
            transport_capacity_pkm=transport_capacity_pkm,
        )
