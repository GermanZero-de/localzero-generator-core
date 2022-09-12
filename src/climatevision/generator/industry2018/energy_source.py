# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..common.energy import Energy, EnergyWithPercentage


@dataclass(kw_only=True)
class EnergySupply:
    s: EnergyWithPercentage
    s_fossil: Energy
    s_fossil_gas: EnergyWithPercentage
    s_fossil_coal: EnergyWithPercentage
    s_fossil_diesel: EnergyWithPercentage
    s_fossil_fueloil: EnergyWithPercentage
    s_fossil_lpg: EnergyWithPercentage
    s_fossil_opetpro: EnergyWithPercentage
    s_fossil_ofossil: EnergyWithPercentage
    s_renew: Energy
    s_renew_biomass: EnergyWithPercentage
    s_renew_heatnet: EnergyWithPercentage
    s_renew_heatpump: EnergyWithPercentage
    s_renew_solarth: EnergyWithPercentage
    s_renew_elec: EnergyWithPercentage


def calc_supply(inputs: Inputs) -> EnergySupply:
    fact = inputs.fact
    entries = inputs.entries

    total_energy_supply = entries.i_energy_total

    s_fossil_gas = EnergyWithPercentage(
        energy=entries.i_gas_fec, total_energy=total_energy_supply
    )
    s_fossil_coal = EnergyWithPercentage(
        energy=entries.i_coal_fec, total_energy=total_energy_supply
    )
    s_fossil_diesel = EnergyWithPercentage(
        energy=entries.i_diesel_fec, total_energy=total_energy_supply
    )
    s_fossil_fueloil = EnergyWithPercentage(
        energy=entries.i_fueloil_fec, total_energy=total_energy_supply
    )
    s_fossil_lpg = EnergyWithPercentage(
        energy=entries.i_lpg_fec, total_energy=total_energy_supply
    )
    s_fossil_opetpro = EnergyWithPercentage(
        energy=entries.i_opetpro_fec, total_energy=total_energy_supply
    )
    s_fossil_ofossil = EnergyWithPercentage(
        energy=entries.i_ofossil_fec, total_energy=total_energy_supply
    )

    s_fossil = Energy(
        energy=s_fossil_gas.energy
        + s_fossil_coal.energy
        + s_fossil_diesel.energy
        + s_fossil_fueloil.energy
        + s_fossil_lpg.energy
        + s_fossil_opetpro.energy
        + s_fossil_ofossil.energy
    )

    s_renew_biomass = EnergyWithPercentage(
        energy=entries.i_biomass_fec, total_energy=total_energy_supply
    )
    s_renew_heatnet = EnergyWithPercentage(
        energy=entries.i_heatnet_fec, total_energy=total_energy_supply
    )
    s_renew_heatpump = EnergyWithPercentage(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        total_energy=total_energy_supply,
    )
    s_renew_solarth = EnergyWithPercentage(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        total_energy=total_energy_supply,
    )
    s_renew_elec = EnergyWithPercentage(
        energy=entries.i_elec_fec, total_energy=total_energy_supply
    )

    s_renew = Energy(
        energy=s_renew_biomass.energy
        + s_renew_heatnet.energy
        + s_renew_heatpump.energy
        + s_renew_solarth.energy
        + s_renew_elec.energy
    )

    s = EnergyWithPercentage(
        energy=entries.i_energy_total, total_energy=entries.i_energy_total
    )

    return EnergySupply(
        s=s,
        s_fossil=s_fossil,
        s_fossil_gas=s_fossil_gas,
        s_fossil_coal=s_fossil_coal,
        s_fossil_diesel=s_fossil_diesel,
        s_fossil_fueloil=s_fossil_fueloil,
        s_fossil_lpg=s_fossil_lpg,
        s_fossil_opetpro=s_fossil_opetpro,
        s_fossil_ofossil=s_fossil_ofossil,
        s_renew=s_renew,
        s_renew_biomass=s_renew_biomass,
        s_renew_heatnet=s_renew_heatnet,
        s_renew_heatpump=s_renew_heatpump,
        s_renew_solarth=s_renew_solarth,
        s_renew_elec=s_renew_elec,
    )
