# pyright: strict
from dataclasses import dataclass
from .utils import element_wise_plus
from .utils import co2e_from_demands
from ..inputs import Inputs


@dataclass
class Air:
    # Used by air_dmstc, air, air_inter
    CO2e_combustion_based: float
    CO2e_total: float
    demand_jetfuel: float
    demand_petrol: float
    energy: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    def __add__(self: "Air", other: "Air") -> "Air":
        return element_wise_plus(self, other)

    @classmethod
    def calc_domestic(cls, inputs: Inputs) -> "Air":
        demand_petrol = (
            inputs.fact("Fact_T_S_Air_petrol_fec_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        demand_jetfuel = (
            inputs.fact("Fact_T_S_Air_nat_EB_dmstc_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        transport_capacity_pkm = (
            inputs.fact("Fact_T_D_Air_dmstc_nat_trnsprt_ppl_2019")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * inputs.fact("Fact_T_D_Air_dmstc_nat_ratio_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        CO2e_combustion_based = co2e_from_demands(
            inputs, demand_jetfuel=demand_jetfuel, demand_jetpetrol=demand_petrol
        )
        CO2e_total = CO2e_combustion_based

        energy = demand_jetfuel + demand_petrol
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            demand_jetfuel=demand_jetfuel,
            demand_petrol=demand_petrol,
            energy=energy,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=transport_capacity_tkm,
        )

    @classmethod
    def calc_international(cls, inputs: Inputs) -> "Air":
        transport_capacity_pkm = (
            inputs.fact("Fact_T_D_Air_nat_trnsprt_ppl_2019")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * inputs.fact("Fact_T_D_Air_inter_nat_ratio_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        demand_jetfuel = (
            inputs.fact("Fact_T_S_Air_nat_EB_inter_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        CO2e_combustion_based = co2e_from_demands(inputs, demand_jetfuel=demand_jetfuel)
        CO2e_total = CO2e_combustion_based
        energy = demand_jetfuel
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=transport_capacity_tkm,
            demand_jetfuel=demand_jetfuel,
            demand_petrol=0,
            energy=energy,
        )
