# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...electricity2018.e18 import E18
from ...common.energy_with_co2e_per_mwh import EnergyWithCO2ePerMWh

from ..energy_base import Energies


@dataclass(kw_only=True)
class Production:
    total: EnergyWithCO2ePerMWh
    gas: EnergyWithCO2ePerMWh
    lpg: EnergyWithCO2ePerMWh
    fueloil: EnergyWithCO2ePerMWh
    opetpro: EnergyWithCO2ePerMWh
    coal: EnergyWithCO2ePerMWh
    heatnet: EnergyWithCO2ePerMWh
    heatnet_cogen: EnergyWithCO2ePerMWh
    heatnet_plant: EnergyWithCO2ePerMWh
    heatnet_geoth: EnergyWithCO2ePerMWh
    heatnet_lheatpump: EnergyWithCO2ePerMWh
    biomass: EnergyWithCO2ePerMWh
    ofossil: EnergyWithCO2ePerMWh
    orenew: EnergyWithCO2ePerMWh
    solarth: EnergyWithCO2ePerMWh
    heatpump: EnergyWithCO2ePerMWh


def calc_production(inputs: Inputs, energies: Energies, e18: E18) -> Production:

    fact = inputs.fact

    gas = EnergyWithCO2ePerMWh(
        energy=energies.r18_gas.energy
        + energies.b18_gas.energy
        + energies.i18_fossil_gas.energy
        + energies.a18_gas.energy
        + energies.t18_gas.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
    )

    lpg = EnergyWithCO2ePerMWh(
        energy=energies.r18_lpg.energy
        + energies.b18_lpg.energy
        + energies.i18_fossil_lpg.energy
        + energies.a18_lpg.energy
        + energies.t18_lpg.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018"),
    )

    fueloil = EnergyWithCO2ePerMWh(
        energy=energies.r18_fueloil.energy
        + energies.b18_fueloil.energy
        + energies.i18_fossil_fueloil.energy
        + energies.a18_fueloil.energy
        + energies.t18_fueloil.energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    opetpro = EnergyWithCO2ePerMWh(
        energy=energies.i18_fossil_opetpro.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    coal = EnergyWithCO2ePerMWh(
        energy=energies.r18_coal.energy
        + energies.b18_coal.energy
        + energies.i18_fossil_coal.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"),
    )

    heatnet_energy = (
        energies.r18_heatnet.energy
        + energies.b18_heatnet.energy
        + energies.i18_renew_heatnet.energy
    )

    e18_energy = (
        e18.p_fossil_coal_brown_cogen.energy
        + e18.p_fossil_coal_black_cogen.energy
        + e18.p_fossil_gas_cogen.energy
        + e18.p_fossil_ofossil_cogen.energy
        + e18.p_renew_biomass_cogen.energy
    )

    if e18_energy < heatnet_energy:
        heatnet_cogen_energy = e18_energy
    else:
        heatnet_cogen_energy = heatnet_energy

    heatnet_cogen = EnergyWithCO2ePerMWh(
        energy=heatnet_cogen_energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_heatnet_cogen_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    heatnet_plant = EnergyWithCO2ePerMWh(
        energy=heatnet_energy - heatnet_cogen.energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    # TODO: Check, why heatnet_geoth is completely 0
    heatnet_geoth = EnergyWithCO2ePerMWh(energy=0)
    # TODO: Check, why heatnet_lheatpump is completely 0
    heatnet_lheatpump = EnergyWithCO2ePerMWh(energy=0)

    heatnet = EnergyWithCO2ePerMWh.sum(heatnet_cogen, heatnet_plant)

    biomass = EnergyWithCO2ePerMWh(
        energy=energies.r18_biomass.energy
        + energies.b18_biomass.energy
        + energies.i18_renew_biomass.energy
        + energies.a18_biomass.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    ofossil = EnergyWithCO2ePerMWh(
        energy=energies.i18_fossil_ofossil.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    orenew_energy = (
        energies.r18_orenew.energy
        + energies.b18_orenew.energy
        + energies.i18_renew_orenew.energy
    )

    solarth = EnergyWithCO2ePerMWh(
        energy=orenew_energy * fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
    )

    heatpump = EnergyWithCO2ePerMWh(
        energy=orenew_energy * fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
    )

    orenew = EnergyWithCO2ePerMWh.sum(solarth, heatpump)

    total = EnergyWithCO2ePerMWh.sum(
        gas,
        lpg,
        fueloil,
        opetpro,
        coal,
        heatnet,
        biomass,
        ofossil,
        orenew,
    )

    return Production(
        total=total,
        gas=gas,
        lpg=lpg,
        fueloil=fueloil,
        opetpro=opetpro,
        coal=coal,
        heatnet=heatnet,
        heatnet_cogen=heatnet_cogen,
        heatnet_plant=heatnet_plant,
        heatnet_geoth=heatnet_geoth,
        heatnet_lheatpump=heatnet_lheatpump,
        biomass=biomass,
        ofossil=ofossil,
        orenew=orenew,
        solarth=solarth,
        heatpump=heatpump,
    )
