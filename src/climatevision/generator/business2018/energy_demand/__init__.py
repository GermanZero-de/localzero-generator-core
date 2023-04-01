# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div

from ..dataclasses import (
    Vars2,
    Vars3,
    # Vars4,
)


@dataclass(kw_only=True)
class Production:

    # total: Vars2

    nonresi: Vars3
    # nonresi_com: Vars4
    elec_elcon: Vars2
    elec_heatpump: Vars2
    vehicles: Vars2
    other: Vars2


def calc_production(
    inputs: Inputs,
    s_heatpump_energy: float,
    s_elec_energy: float,
    s_elec_heating_energy: float,
    s_petrol_energy: float,
    s_jetfuel_energy: float,
    s_diesel_energy: float,
    s_gas_energy: float,
    s_lpg_energy: float,
    s_fueloil_energy: float,
    s_biomass_energy: float,
    s_coal_energy: float,
    s_heatnet_energy: float,
    s_solarth_energy: float,
) -> Production:

    fact = inputs.fact
    entries = inputs.entries

    elec_heatpump = Vars2()
    elec_heatpump.energy = s_heatpump_energy / fact(
        "Fact_R_S_heatpump_mean_annual_performance_factor_all"
    )

    elec_elcon = Vars2()
    elec_elcon.energy = elec_elcon.energy = (
        s_elec_energy - elec_heatpump.energy - s_elec_heating_energy
    )

    vehicles = Vars2()
    vehicles.energy = s_petrol_energy + s_jetfuel_energy + s_diesel_energy

    other = Vars2()
    other.energy = elec_elcon.energy + elec_heatpump.energy + vehicles.energy

    nonresi = Vars3()
    nonresi.area_m2 = (
        entries.r_area_m2
        * fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016")
        / (1 - fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016"))
        * (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
    )
    nonresi.energy = (
        s_gas_energy
        + s_lpg_energy
        + s_fueloil_energy
        + s_biomass_energy
        + s_coal_energy
        + s_heatnet_energy
        + s_heatpump_energy
        + s_solarth_energy
        + s_elec_heating_energy
    )
    nonresi.number_of_buildings = (
        fact("Fact_B_P_number_business_buildings_2016")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )
    nonresi.factor_adapted_to_fec = div(nonresi.energy, nonresi.area_m2)

    return Production(
        # total=total,
        nonresi=nonresi,
        # nonresi_com=nonresi_com,
        elec_elcon=elec_elcon,
        elec_heatpump=elec_heatpump,
        vehicles=vehicles,
        other=other,
    )
