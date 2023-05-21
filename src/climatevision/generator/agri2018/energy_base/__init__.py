# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.energy import Energy


@dataclass(kw_only=True)
class Energies:
    heatpump: Energy
    gas: Energy
    lpg: Energy
    petrol: Energy
    diesel: Energy
    fueloil: Energy
    biomass: Energy
    elec: Energy


def calc(inputs: Inputs) -> Energies:
    entries = inputs.entries

    heatpump = Energy(energy=0)
    gas = Energy(energy=entries.a_gas_fec)
    lpg = Energy(energy=entries.a_lpg_fec)
    petrol = Energy(energy=entries.a_petrol_fec)
    diesel = Energy(energy=entries.a_diesel_fec)
    fueloil = Energy(energy=entries.a_fueloil_fec)
    biomass = Energy(energy=entries.a_biomass_fec)
    elec = Energy(energy=entries.a_elec_fec)

    return Energies(
        heatpump=heatpump,
        gas=gas,
        lpg=lpg,
        petrol=petrol,
        diesel=diesel,
        fueloil=fueloil,
        biomass=biomass,
        elec=elec,
    )
