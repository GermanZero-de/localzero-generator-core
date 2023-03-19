# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.energy import Energy, EnergyWithPercentage


@dataclass(kw_only=True)
class EnergySupply:
    total: EnergyWithPercentage
    fossil: Energy
    fossil_gas: EnergyWithPercentage
    fossil_coal: EnergyWithPercentage
    fossil_diesel: EnergyWithPercentage
    fossil_fueloil: EnergyWithPercentage
    fossil_lpg: EnergyWithPercentage
    fossil_opetpro: EnergyWithPercentage
    fossil_ofossil: EnergyWithPercentage
    renew: Energy
    renew_biomass: EnergyWithPercentage
    renew_heatnet: EnergyWithPercentage
    renew_heatpump: EnergyWithPercentage
    renew_solarth: EnergyWithPercentage
    renew_elec: EnergyWithPercentage


def calc_supply(inputs: Inputs) -> EnergySupply:
    fact = inputs.fact
    entries = inputs.entries

    total_energy_supply = entries.i_energy_total

    fossil_gas = EnergyWithPercentage(
        energy=entries.i_gas_fec, total_energy=total_energy_supply
    )
    fossil_coal = EnergyWithPercentage(
        energy=entries.i_coal_fec, total_energy=total_energy_supply
    )
    fossil_diesel = EnergyWithPercentage(
        energy=entries.i_diesel_fec, total_energy=total_energy_supply
    )
    fossil_fueloil = EnergyWithPercentage(
        energy=entries.i_fueloil_fec, total_energy=total_energy_supply
    )
    fossil_lpg = EnergyWithPercentage(
        energy=entries.i_lpg_fec, total_energy=total_energy_supply
    )
    fossil_opetpro = EnergyWithPercentage(
        energy=entries.i_opetpro_fec, total_energy=total_energy_supply
    )
    fossil_ofossil = EnergyWithPercentage(
        energy=entries.i_ofossil_fec, total_energy=total_energy_supply
    )

    fossil = Energy(
        energy=fossil_gas.energy
        + fossil_coal.energy
        + fossil_diesel.energy
        + fossil_fueloil.energy
        + fossil_lpg.energy
        + fossil_opetpro.energy
        + fossil_ofossil.energy
    )

    renew_biomass = EnergyWithPercentage(
        energy=entries.i_biomass_fec, total_energy=total_energy_supply
    )
    renew_heatnet = EnergyWithPercentage(
        energy=entries.i_heatnet_fec, total_energy=total_energy_supply
    )
    renew_heatpump = EnergyWithPercentage(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        total_energy=total_energy_supply,
    )
    renew_solarth = EnergyWithPercentage(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        total_energy=total_energy_supply,
    )
    renew_elec = EnergyWithPercentage(
        energy=entries.i_elec_fec, total_energy=total_energy_supply
    )

    renew = Energy(
        energy=renew_biomass.energy
        + renew_heatnet.energy
        + renew_heatpump.energy
        + renew_solarth.energy
        + renew_elec.energy
    )

    total = EnergyWithPercentage(
        energy=entries.i_energy_total, total_energy=entries.i_energy_total
    )

    return EnergySupply(
        total=total,
        fossil=fossil,
        fossil_gas=fossil_gas,
        fossil_coal=fossil_coal,
        fossil_diesel=fossil_diesel,
        fossil_fueloil=fossil_fueloil,
        fossil_lpg=fossil_lpg,
        fossil_opetpro=fossil_opetpro,
        fossil_ofossil=fossil_ofossil,
        renew=renew,
        renew_biomass=renew_biomass,
        renew_heatnet=renew_heatnet,
        renew_heatpump=renew_heatpump,
        renew_solarth=renew_solarth,
        renew_elec=renew_elec,
    )
