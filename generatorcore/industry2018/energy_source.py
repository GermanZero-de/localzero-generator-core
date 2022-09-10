# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..commonDataclasses.energy import Energy

from .supply_classes import EnergySource


@dataclass(kw_only=True)
class EnergySupply:
    s: EnergySource
    s_fossil: Energy
    s_fossil_gas: EnergySource
    s_fossil_coal: EnergySource
    s_fossil_diesel: EnergySource
    s_fossil_fueloil: EnergySource
    s_fossil_lpg: EnergySource
    s_fossil_opetpro: EnergySource
    s_fossil_ofossil: EnergySource
    s_renew: Energy
    s_renew_biomass: EnergySource
    s_renew_heatnet: EnergySource
    s_renew_heatpump: EnergySource
    s_renew_solarth: EnergySource
    s_renew_elec: EnergySource


def calc_supply(inputs: Inputs) -> EnergySupply:
    fact = inputs.fact
    entries = inputs.entries

    total_energy_supply = entries.i_energy_total

    s_fossil_gas = EnergySource(
        energy=entries.i_gas_fec, total_energy=total_energy_supply
    )
    s_fossil_coal = EnergySource(
        energy=entries.i_coal_fec, total_energy=total_energy_supply
    )
    s_fossil_diesel = EnergySource(
        energy=entries.i_diesel_fec, total_energy=total_energy_supply
    )
    s_fossil_fueloil = EnergySource(
        energy=entries.i_fueloil_fec, total_energy=total_energy_supply
    )
    s_fossil_lpg = EnergySource(
        energy=entries.i_lpg_fec, total_energy=total_energy_supply
    )
    s_fossil_opetpro = EnergySource(
        energy=entries.i_opetpro_fec, total_energy=total_energy_supply
    )
    s_fossil_ofossil = EnergySource(
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

    s_renew_biomass = EnergySource(
        energy=entries.i_biomass_fec, total_energy=total_energy_supply
    )
    s_renew_heatnet = EnergySource(
        energy=entries.i_heatnet_fec, total_energy=total_energy_supply
    )
    s_renew_heatpump = EnergySource(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        total_energy=total_energy_supply,
    )
    s_renew_solarth = EnergySource(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        total_energy=total_energy_supply,
    )
    s_renew_elec = EnergySource(
        energy=entries.i_elec_fec, total_energy=total_energy_supply
    )

    s_renew = Energy(
        energy=s_renew_biomass.energy
        + s_renew_heatnet.energy
        + s_renew_heatpump.energy
        + s_renew_solarth.energy
        + s_renew_elec.energy
    )

    s = EnergySource(energy=entries.i_energy_total, total_energy=entries.i_energy_total)

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
