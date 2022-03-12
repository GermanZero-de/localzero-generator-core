# pyright: strict
from dataclasses import dataclass
from .utils import element_wise_plus
from .utils import co2e_from_demands
from ..inputs import Inputs


@dataclass
class Ship:
    # Used by ship_dmstc, ship_inter, ship
    CO2e_combustion_based: float
    CO2e_total: float
    demand_diesel: float
    demand_fueloil: float
    energy: float
    transport_capacity_tkm: float

    def __add__(self: "Ship", other: "Ship") -> "Ship":
        return element_wise_plus(self, other)

    @classmethod
    def calc_ship_domestic(cls, inputs: Inputs) -> "Ship":
        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Shp_dmstc_trnsprt_gds_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        demand_diesel = (
            inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
            * inputs.fact("Fact_T_S_Shp_diesel_fec_2018")
        )
        energy = demand_diesel

        CO2e_combustion_based = co2e_from_demands(inputs, demand_diesel=demand_diesel)
        CO2e_total = CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            transport_capacity_tkm=transport_capacity_tkm,
            demand_diesel=demand_diesel,
            demand_fueloil=0,
            energy=energy,
        )

    @classmethod
    def calc_ship_international(cls, inputs: Inputs) -> "Ship":
        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Shp_sea_nat_mlg_2013")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        demand_fueloil = (
            inputs.entries.m_population_com_2018 / inputs.entries.m_population_nat
        ) * inputs.fact("Fact_T_D_Shp_sea_nat_EC_2018")

        energy = demand_fueloil
        CO2e_combustion_based = co2e_from_demands(inputs, demand_fueloil=demand_fueloil)
        CO2e_total = CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            transport_capacity_tkm=transport_capacity_tkm,
            demand_fueloil=demand_fueloil,
            demand_diesel=0,
            energy=energy,
        )
