# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy as EnergyDemand

from ..energy_base import Energies


@dataclass(kw_only=True)
class Demand:
    residences: EnergyDemand
    business: EnergyDemand
    industry: EnergyDemand
    transport: EnergyDemand
    agri: EnergyDemand

    total: EnergyDemand


def calc_demand(energies: Energies) -> Demand:

    residences = EnergyDemand(
        energy=energies.r18_coal.energy
        + energies.r18_fueloil.energy
        + energies.r18_lpg.energy
        + energies.r18_gas.energy
        + energies.r18_biomass.energy
        + energies.r18_orenew.energy
        + energies.r18_heatnet.energy
    )

    business = EnergyDemand(
        energy=energies.b18_coal.energy
        + energies.b18_fueloil.energy
        + energies.b18_lpg.energy
        + energies.b18_gas.energy
        + energies.b18_biomass.energy
        + energies.b18_orenew.energy
        + energies.b18_heatnet.energy
    )

    industry = EnergyDemand(
        energy=energies.i18_fossil_coal.energy
        + energies.i18_fossil_fueloil.energy
        + energies.i18_fossil_lpg.energy
        + energies.i18_fossil_opetpro.energy
        + energies.i18_fossil_gas.energy
        + energies.i18_renew_biomass.energy
        + energies.i18_renew_orenew.energy
        + energies.i18_fossil_ofossil.energy
        + energies.i18_renew_heatnet.energy
    )

    transport = EnergyDemand(
        energy=energies.t18_fueloil.energy
        + energies.t18_lpg.energy
        + energies.t18_gas.energy
    )

    agri = EnergyDemand(
        energy=energies.a18_fueloil.energy
        + energies.a18_lpg.energy
        + energies.a18_gas.energy
        + energies.a18_biomass.energy
    )

    total = EnergyDemand(
        energy=residences.energy
        + business.energy
        + industry.energy
        + transport.energy
        + agri.energy
    )

    return Demand(
        residences=residences,
        business=business,
        industry=industry,
        transport=transport,
        agri=agri,
        total=total,
    )
