# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts, Assumptions
from ...utils import element_wise_plus, MILLION

from . import co2e


@dataclass
class Rail:
    CO2e_combustion_based: float
    CO2e_total: float
    demand_biodiesel: float
    demand_diesel: float
    demand_electricity: float
    energy: float
    mileage: float
    transport_capacity_tkm: float
    transport_capacity_pkm: float

    def __add__(self: "Rail", other: "Rail") -> "Rail":
        return element_wise_plus(self, other)

    @classmethod
    def calc_people_distance(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        ec_rail_ppl_elec: float,
        ec_rail_ppl_diesel: float,
    ) -> "Rail":
        fact = facts.fact

        demand_electricity = ec_rail_ppl_elec
        demand_diesel = ec_rail_ppl_diesel * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )
        demand_biodiesel = ec_rail_ppl_diesel * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        transport_capacity_pkm = (demand_diesel + demand_biodiesel) / fact(
            "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        ) + demand_electricity / fact("Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018")
        mileage = transport_capacity_pkm / fact(
            "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        )
        energy = demand_diesel + demand_biodiesel + demand_electricity
        CO2e_combustion_based = co2e.from_demands(
            facts,
            assumptions,
            demand_diesel=demand_diesel,
            demand_biodiesel=demand_biodiesel,
            demand_electricity=demand_electricity,
        )
        CO2e_total = CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            demand_biodiesel=demand_biodiesel,
            demand_diesel=demand_diesel,
            demand_electricity=demand_electricity,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
        )

    @classmethod
    def calc_goods(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        ec_rail_gds_elec: float,
        ec_rail_gds_diesel: float,
    ) -> "Rail":
        fact = facts.fact

        demand_electricity = ec_rail_gds_elec
        demand_diesel = ec_rail_gds_diesel * (
            1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )
        demand_biodiesel = ec_rail_gds_diesel * fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        transport_capacity_tkm = (demand_diesel + demand_biodiesel) / fact(
            "Fact_T_S_Rl_Train_gds_diesel_SEC_2018"
        ) + demand_electricity / fact("Fact_T_S_Rl_Train_gds_elec_SEC_2018")

        CO2e_combustion_based = co2e.from_demands(
            facts, assumptions, demand_diesel=demand_diesel
        )
        energy = demand_diesel + demand_biodiesel + demand_electricity
        mileage = transport_capacity_tkm / fact(
            "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
        )
        CO2e_total = CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            demand_biodiesel=demand_biodiesel,
            demand_diesel=demand_diesel,
            demand_electricity=demand_electricity,
            energy=energy,
            mileage=mileage,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=0,
        )

    @classmethod
    def calc_rail_people_metro(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        population_commune_2018: int,
        population_district_2018: int,
        t_metro_mega_km_dis: float,
    ) -> "Rail":
        fact = facts.fact

        mileage = (
            t_metro_mega_km_dis
            * MILLION
            * population_commune_2018
            / population_district_2018
        )
        demand_electricity = mileage * fact("Fact_T_S_Rl_Metro_SEC_fzkm_2018")
        energy = demand_electricity
        transport_capacity_pkm = mileage * fact("Fact_T_D_lf_Rl_Metro_2018")
        CO2e_combustion_based = co2e.from_demands(
            facts, assumptions, demand_electricity=demand_electricity
        )
        CO2e_total = CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            demand_electricity=demand_electricity,
            demand_biodiesel=0,
            demand_diesel=0,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
        )
