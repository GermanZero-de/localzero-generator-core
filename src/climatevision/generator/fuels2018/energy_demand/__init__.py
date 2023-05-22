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

    residences = EnergyDemand(energy=energies.r18_petrol.energy)

    business = EnergyDemand(
        energy=energies.b18_petrol.energy
        + energies.b18_jetfuel.energy
        + energies.b18_diesel.energy
    )

    # industry = EnergyDemand(energy=entries.i_diesel_fec)
    industry = EnergyDemand(energy=energies.i18_fossil_diesel.energy)

    transport = EnergyDemand(
        energy=energies.t18_petrol.energy
        + energies.t18_jetfuel.energy
        + energies.t18_diesel.energy
        + energies.t18_biogas.energy
        + energies.t18_bioethanol.energy
        + energies.t18_biodiesel.energy
    )

    agri = EnergyDemand(energy=energies.a18_petrol.energy + energies.a18_diesel.energy)

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
