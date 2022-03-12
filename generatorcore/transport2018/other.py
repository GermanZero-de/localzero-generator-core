# pyright: strict
from dataclasses import dataclass
from .utils import element_wise_plus
from ..inputs import Inputs


@dataclass
class Other:
    # Used by other_foot, other_cycl
    CO2e_combustion_based: float
    CO2e_total: float
    transport_capacity_pkm: float

    def __add__(self: "Other", other: "Other") -> "Other":
        return element_wise_plus(self, other)

    @classmethod
    def calc_foot(cls, inputs: Inputs) -> "Other":
        t_rt7 = inputs.entries.t_rt7
        if t_rt7 in ["71", "72", "73", "74", "75", "76", "77"]:
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_foot_rt" + t_rt7)
            )

        # This happens if we run Local Zero for a Landkreis a Bundesland or Germany.
        # We do not have a area_kind entry in this case and just use the mean mean modal split of germany.
        elif t_rt7 == "nd":
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_foot_nat")
            )
        else:
            assert False, f"Do not know how to handle entries.t_rt7 = {t_rt7}"
        return cls(
            CO2e_total=0,
            CO2e_combustion_based=0,
            transport_capacity_pkm=transport_capacity_pkm,
        )

    @classmethod
    def calc_cycle(cls, inputs: Inputs) -> "Other":
        t_rt7 = inputs.entries.t_rt7
        if t_rt7 in ["71", "72", "73", "74", "75", "76", "77"]:
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_cycl_rt" + t_rt7)
            )

        # This happens if we run Local Zero for a Landkreis a Bundesland or Germany.
        # We do not have a area_kind entry in this case and just use the mean mean modal split of germany.
        elif t_rt7 == "nd":
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_foot_nat")
            )
        else:
            assert False, f"Do not know how to handle entries.t_rt7 = {t_rt7}"
        return cls(
            CO2e_total=0,
            CO2e_combustion_based=0,
            transport_capacity_pkm=transport_capacity_pkm,
        )
