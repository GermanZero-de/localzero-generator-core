# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.energy import Energy, EnergyPerM2PctCommune, EnergyPerM2WithBuildings


@dataclass(kw_only=True)
class Production:
    total: Energy
    nonresi: EnergyPerM2WithBuildings
    nonresi_commune: EnergyPerM2PctCommune
    elec_elcon: Energy
    elec_heatpump: Energy
    vehicles: Energy
    other: Energy


def calc_production(
    inputs: Inputs,
    heatpump_energy: float,
    elec_energy: float,
    elec_heating_energy: float,
    petrol_energy: float,
    jetfuel_energy: float,
    diesel_energy: float,
    gas_energy: float,
    lpg_energy: float,
    fueloil_energy: float,
    biomass_energy: float,
    coal_energy: float,
    heatnet_energy: float,
    solarth_energy: float,
) -> Production:

    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    elec_heatpump = Energy(
        energy=heatpump_energy
        / fact("Fact_R_S_heatpump_mean_annual_performance_factor_all")
    )

    elec_elcon = Energy(energy=elec_energy - elec_heatpump.energy - elec_heating_energy)

    vehicles = Energy(energy=petrol_energy + jetfuel_energy + diesel_energy)

    other = Energy(energy=elec_elcon.energy + elec_heatpump.energy + vehicles.energy)

    nonresi = EnergyPerM2WithBuildings(
        area_m2=(
            entries.r_area_m2
            * fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016")
            / (1 - fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016"))
            * (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
        ),
        energy=(
            gas_energy
            + lpg_energy
            + fueloil_energy
            + biomass_energy
            + coal_energy
            + heatnet_energy
            + heatpump_energy
            + solarth_energy
            + elec_heating_energy
        ),
        number_of_buildings=(
            fact("Fact_B_P_number_business_buildings_2016")
            * entries.m_population_com_2018
            / entries.m_population_nat
        ),
    )

    nonresi_commune = EnergyPerM2PctCommune(
        pct_x=ass(
            "Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050"
        ),
        total=nonresi,
    )

    total = Energy(energy=nonresi.energy + other.energy)

    return Production(
        total=total,
        nonresi=nonresi,
        nonresi_commune=nonresi_commune,
        elec_elcon=elec_elcon,
        elec_heatpump=elec_heatpump,
        vehicles=vehicles,
        other=other,
    )
