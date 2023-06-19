# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts
from ...common.energy import Energy


@dataclass(kw_only=True)
class Energies:
    gas: Energy
    lpg: Energy
    petrol: Energy
    jetfuel: Energy
    diesel: Energy
    fueloil: Energy
    biomass: Energy
    coal: Energy
    heatnet: Energy
    elec_heating: Energy
    heatpump: Energy
    solarth: Energy
    elec: Energy


def calc(entries: Entries, facts: Facts) -> Energies:
    fact = facts.fact

    gas = Energy(energy=entries.b_gas_fec)
    lpg = Energy(energy=entries.b_lpg_fec)
    petrol = Energy(energy=entries.b_petrol_fec)
    jetfuel = Energy(energy=entries.b_jetfuel_fec)
    diesel = Energy(energy=entries.b_diesel_fec)
    fueloil = Energy(energy=entries.b_fueloil_fec)
    biomass = Energy(energy=entries.b_biomass_fec)
    coal = Energy(energy=entries.b_coal_fec)
    heatnet = Energy(energy=entries.b_heatnet_fec)
    elec_heating = Energy(
        energy=(
            fact("Fact_B_S_elec_heating_fec_2018")
            * entries.r_flats_wo_heatnet
            / fact("Fact_R_P_flats_wo_heatnet_2011")
        )
    )
    heatpump = Energy(
        energy=entries.b_orenew_fec * fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    )
    solarth = Energy(
        energy=entries.b_orenew_fec
        * (1 - fact("Fact_R_S_ratio_heatpump_to_orenew_2018"))
    )
    elec = Energy(energy=entries.b_elec_fec)

    return Energies(
        gas=gas,
        lpg=lpg,
        petrol=petrol,
        jetfuel=jetfuel,
        diesel=diesel,
        fueloil=fueloil,
        biomass=biomass,
        coal=coal,
        heatnet=heatnet,
        elec_heating=elec_heating,
        heatpump=heatpump,
        solarth=solarth,
        elec=elec,
    )
