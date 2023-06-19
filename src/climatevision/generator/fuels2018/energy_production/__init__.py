# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts
from ...common.energy_with_co2e_per_mwh import EnergyWithCO2ePerMWh

from ..energy_base import Energies


@dataclass(kw_only=True)
class Production:
    petrol: EnergyWithCO2ePerMWh
    jetfuel: EnergyWithCO2ePerMWh
    diesel: EnergyWithCO2ePerMWh
    bioethanol: EnergyWithCO2ePerMWh
    biodiesel: EnergyWithCO2ePerMWh
    biogas: EnergyWithCO2ePerMWh

    total: EnergyWithCO2ePerMWh


def calc_production(facts: Facts, energies: Energies) -> Production:
    fact = facts.fact

    petrol = EnergyWithCO2ePerMWh(
        energy=energies.r18_petrol.energy
        + energies.b18_petrol.energy
        + energies.a18_petrol.energy
        + energies.t18_petrol.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018"),
    )
    jetfuel = EnergyWithCO2ePerMWh(
        energy=energies.b18_jetfuel.energy + energies.t18_jetfuel.energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_F_P_jetfuel_ratio_CO2e_cb_to_fec_2018"
        ),
    )
    diesel = EnergyWithCO2ePerMWh(
        energy=energies.b18_diesel.energy
        + energies.i18_fossil_diesel.energy
        + energies.t18_diesel.energy
        + energies.a18_diesel.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018"),
    )
    bioethanol = EnergyWithCO2ePerMWh(
        energy=energies.t18_bioethanol.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    biodiesel = EnergyWithCO2ePerMWh(
        energy=energies.t18_biodiesel.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    biogas = EnergyWithCO2ePerMWh(
        energy=energies.t18_biogas.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    total = EnergyWithCO2ePerMWh.sum(
        petrol,
        jetfuel,
        diesel,
        bioethanol,
        biodiesel,
        biogas,
    )

    return Production(
        petrol=petrol,
        jetfuel=jetfuel,
        diesel=diesel,
        bioethanol=bioethanol,
        biodiesel=biodiesel,
        biogas=biogas,
        total=total,
    )
