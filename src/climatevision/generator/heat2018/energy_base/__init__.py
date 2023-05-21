# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.energy import Energy
from ...industry2018.i18 import I18
from ...transport2018.t18 import T18


@dataclass(kw_only=True)
class Energies:
    r18_coal: Energy
    r18_fueloil: Energy
    r18_lpg: Energy
    r18_gas: Energy
    r18_biomass: Energy
    r18_orenew: Energy
    r18_heatnet: Energy

    b18_coal: Energy
    b18_fueloil: Energy
    b18_lpg: Energy
    b18_gas: Energy
    b18_biomass: Energy
    b18_orenew: Energy
    b18_heatnet: Energy

    a18_fueloil: Energy
    a18_lpg: Energy
    a18_gas: Energy
    a18_biomass: Energy

    i18_fossil_coal: Energy
    i18_fossil_fueloil: Energy
    i18_fossil_lpg: Energy
    i18_fossil_opetpro: Energy
    i18_fossil_gas: Energy
    i18_renew_biomass: Energy
    i18_renew_orenew: Energy
    i18_fossil_ofossil: Energy
    i18_renew_heatnet: Energy

    t18_fueloil: Energy
    t18_lpg: Energy
    t18_gas: Energy


def calc(inputs: Inputs, t18: T18, i18: I18) -> Energies:
    entries = inputs.entries

    r18_coal = Energy(energy=entries.r_coal_fec)
    r18_fueloil = Energy(energy=entries.r_fueloil_fec)
    r18_lpg = Energy(energy=entries.r_lpg_fec)
    r18_gas = Energy(energy=entries.r_gas_fec)
    r18_biomass = Energy(energy=entries.r_biomass_fec)
    r18_orenew = Energy(energy=entries.r_orenew_fec)
    r18_heatnet = Energy(energy=entries.r_heatnet_fec)

    b18_coal = Energy(energy=entries.b_coal_fec)
    b18_fueloil = Energy(energy=entries.b_fueloil_fec)
    b18_lpg = Energy(energy=entries.b_lpg_fec)
    b18_gas = Energy(energy=entries.b_gas_fec)
    b18_biomass = Energy(energy=entries.b_biomass_fec)
    b18_orenew = Energy(energy=entries.b_orenew_fec)
    b18_heatnet = Energy(energy=entries.b_heatnet_fec)

    a18_fueloil = Energy(energy=entries.a_fueloil_fec)
    a18_lpg = Energy(energy=entries.a_lpg_fec)
    a18_gas = Energy(energy=entries.a_gas_fec)
    a18_biomass = Energy(energy=entries.a_biomass_fec)

    i18_fossil_coal = Energy(energy=i18.s_fossil_coal.energy)
    i18_fossil_fueloil = Energy(energy=i18.s_fossil_fueloil.energy)
    i18_fossil_lpg = Energy(energy=i18.s_fossil_lpg.energy)
    i18_fossil_opetpro = Energy(energy=i18.s_fossil_opetpro.energy)
    i18_fossil_gas = Energy(energy=i18.s_fossil_gas.energy)
    i18_renew_biomass = Energy(energy=i18.s_renew_biomass.energy)
    i18_renew_orenew = Energy(energy=i18.s_renew_orenew.energy)
    i18_fossil_ofossil = Energy(energy=i18.s_fossil_ofossil.energy)
    i18_renew_heatnet = Energy(energy=i18.s_renew_heatnet.energy)

    t18_fueloil = Energy(energy=t18.t.demand_fueloil)
    t18_lpg = Energy(energy=t18.t.demand_lpg)
    t18_gas = Energy(energy=t18.t.demand_gas)

    return Energies(
        r18_coal=r18_coal,
        r18_fueloil=r18_fueloil,
        r18_lpg=r18_lpg,
        r18_gas=r18_gas,
        r18_biomass=r18_biomass,
        r18_orenew=r18_orenew,
        r18_heatnet=r18_heatnet,
        b18_coal=b18_coal,
        b18_fueloil=b18_fueloil,
        b18_lpg=b18_lpg,
        b18_gas=b18_gas,
        b18_biomass=b18_biomass,
        b18_orenew=b18_orenew,
        b18_heatnet=b18_heatnet,
        a18_fueloil=a18_fueloil,
        a18_lpg=a18_lpg,
        a18_gas=a18_gas,
        a18_biomass=a18_biomass,
        i18_fossil_coal=i18_fossil_coal,
        i18_fossil_fueloil=i18_fossil_fueloil,
        i18_fossil_lpg=i18_fossil_lpg,
        i18_fossil_opetpro=i18_fossil_opetpro,
        i18_fossil_gas=i18_fossil_gas,
        i18_renew_biomass=i18_renew_biomass,
        i18_renew_orenew=i18_renew_orenew,
        i18_fossil_ofossil=i18_fossil_ofossil,
        i18_renew_heatnet=i18_renew_heatnet,
        t18_fueloil=t18_fueloil,
        t18_lpg=t18_lpg,
        t18_gas=t18_gas,
    )
