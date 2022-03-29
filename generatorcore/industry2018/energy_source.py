# pyright: strict
from dataclasses import dataclass
from ..inputs import Inputs
from .energy_pct import Energy_pct
from .energy_sum import EnergySum
from .empty import Empty


@dataclass
class Energy_source:
    s: Energy_pct
    s_fossil: EnergySum
    s_fossil_gas: Energy_pct
    s_fossil_coal: Energy_pct
    s_fossil_diesel: Energy_pct
    s_fossil_fueloil: Energy_pct
    s_fossil_lpg: Energy_pct
    s_fossil_opetpro: Energy_pct
    s_fossil_ofossil: Energy_pct
    s_renew: EnergySum
    s_renew_hydrogen: Empty
    s_renew_emethan: Empty
    s_renew_biomass: Energy_pct
    s_renew_heatnet: Energy_pct
    s_renew_heatpump: Energy_pct
    s_renew_solarth: Energy_pct
    s_renew_elec: Energy_pct


def calc_energy_sources(inputs: Inputs) -> Energy_source:
    fact = inputs.fact
    entries = inputs.entries

    s = Energy_pct(energy=entries.i_energy_total, total_energy=entries.i_energy_total)

    s_fossil_gas = Energy_pct(energy=entries.i_gas_fec, total_energy=s.energy)
    s_fossil_coal = Energy_pct(energy=entries.i_coal_fec, total_energy=s.energy)
    s_fossil_diesel = Energy_pct(energy=entries.i_diesel_fec, total_energy=s.energy)
    s_fossil_fueloil = Energy_pct(energy=entries.i_fueloil_fec, total_energy=s.energy)
    s_fossil_lpg = Energy_pct(energy=entries.i_lpg_fec, total_energy=s.energy)
    s_fossil_opetpro = Energy_pct(energy=entries.i_opetpro_fec, total_energy=s.energy)
    s_fossil_ofossil = Energy_pct(energy=entries.i_ofossil_fec, total_energy=s.energy)

    s_renew_biomass = Energy_pct(energy=entries.i_biomass_fec, total_energy=s.energy)
    s_renew_heatnet = Energy_pct(energy=entries.i_heatnet_fec, total_energy=s.energy)
    s_renew_heatpump = Energy_pct(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        total_energy=s.energy,
    )
    s_renew_solarth = Energy_pct(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        total_energy=s.energy,
    )
    s_renew_elec = Energy_pct(energy=entries.i_elec_fec, total_energy=s.energy)
    s_renew_hydrogen = Empty()
    s_renew_emethan = Empty()

    s_renew = EnergySum(
        s_renew_biomass.energy
        + s_renew_heatnet.energy
        + s_renew_heatpump.energy
        + s_renew_solarth.energy
        + s_renew_elec.energy
    )

    s_fossil = EnergySum(
        s_fossil_gas.energy
        + s_fossil_coal.energy
        + s_fossil_diesel.energy
        + s_fossil_fueloil.energy
        + s_fossil_lpg.energy
        + s_fossil_opetpro.energy
        + s_fossil_ofossil.energy
    )

    return Energy_source(
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
        s_renew_hydrogen=s_renew_hydrogen,
        s_renew_emethan=s_renew_emethan,
        s_renew_biomass=s_renew_biomass,
        s_renew_heatnet=s_renew_heatnet,
        s_renew_heatpump=s_renew_heatpump,
        s_renew_solarth=s_renew_solarth,
        s_renew_elec=s_renew_elec,
    )
