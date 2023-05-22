# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.energy import Energy, EnergyPerM2PctCommune, EnergyPerM2WithBuildings

from ..energy_base import Energies


@dataclass(kw_only=True)
class Production:
    total: Energy
    nonresi: EnergyPerM2WithBuildings
    nonresi_commune: EnergyPerM2PctCommune
    elec_elcon: Energy
    elec_heatpump: Energy
    vehicles: Energy
    other: Energy


def calc_production(inputs: Inputs, energies: Energies) -> Production:
    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    elec_heatpump = Energy(
        energy=energies.heatpump.energy
        / fact("Fact_R_S_heatpump_mean_annual_performance_factor_all")
    )

    elec_elcon = Energy(
        energy=energies.elec.energy
        - elec_heatpump.energy
        - energies.elec_heating.energy
    )

    vehicles = Energy(
        energy=energies.petrol.energy + energies.jetfuel.energy + energies.diesel.energy
    )

    other = Energy(energy=elec_elcon.energy + elec_heatpump.energy + vehicles.energy)

    nonresi = EnergyPerM2WithBuildings(
        area_m2=(
            entries.r_area_m2
            * fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016")
            / (1 - fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016"))
            * (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
        ),
        energy=(
            energies.gas.energy
            + energies.lpg.energy
            + energies.fueloil.energy
            + energies.biomass.energy
            + energies.coal.energy
            + energies.heatnet.energy
            + energies.heatpump.energy
            + energies.solarth.energy
            + energies.elec_heating.energy
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
