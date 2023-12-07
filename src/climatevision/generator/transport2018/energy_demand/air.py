# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts, Assumptions
from ...utils import element_wise_plus
from ...entries import Entries
from . import co2e


@dataclass
class Air:
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
    def calc_domestic(
        cls,
        facts: Facts,
        entries: Entries,
        assumptions: Assumptions,
        population_commune_2018: int,
        population_germany_2018: int,
    ) -> "Air":

        fact = facts.fact

        demand_petrol = entries.t_a_eev_petrol_inland_com

        demand_jetfuel = entries.t_a_eev_kerosene_inland_com

        transport_capacity_pkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_ppl_2019")
            * population_commune_2018
            / population_germany_2018
        )
        
        transport_capacity_tkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * fact("Fact_T_D_Air_dmstc_nat_ratio_2018")
            * population_commune_2018
            / population_germany_2018
        )

        CO2e_combustion_based = co2e.from_demands(
            facts,
            assumptions,
            demand_jetfuel=demand_jetfuel,
            demand_jetpetrol=demand_petrol,
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
    def calc_international(
        cls,
        facts: Facts,
        entries: Entries,
        assumptions: Assumptions,
        population_commune_2018: int,
        population_germany_2018: int,
    ) -> "Air":

        fact = facts.fact
        
        transport_capacity_pkm = (
            fact("Fact_T_D_Air_nat_trnsprt_ppl_2019")
            * population_commune_2018
            / population_germany_2018
        )

        transport_capacity_tkm = (
            fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * fact("Fact_T_D_Air_inter_nat_ratio_2018")
            * population_commune_2018
            / population_germany_2018
        )

        transport_capacity_tkm = entries.t_a_transport_capa_inland_tkm_com

        demand_jetfuel = entries.t_a_eev_kerosene_overseas_com

        CO2e_combustion_based = co2e.from_demands(
            facts, assumptions, demand_jetfuel=demand_jetfuel
        )
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
