# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy

from ..t import T


@dataclass(kw_only=True)
class EnergySupply:
    total: Energy
    diesel: Energy
    emethan: Energy
    jetfuel: Energy
    petrol: Energy
    fueloil: Energy
    lpg: Energy
    gas: Energy
    biogas: Energy
    bioethanol: Energy
    biodiesel: Energy
    elec: Energy
    hydrogen: Energy


def calc_supply(t: T) -> EnergySupply:

    petrol = Energy(energy=t.transport.demand_epetrol)
    jetfuel = Energy(energy=t.transport.demand_ejetfuel)
    diesel = Energy(energy=t.transport.demand_ediesel)
    elec = Energy(energy=t.transport.demand_electricity)
    hydrogen = Energy(energy=t.transport.demand_hydrogen)

    emethan = Energy(energy=0)
    fueloil = Energy(energy=0)
    lpg = Energy(energy=0)
    gas = Energy(energy=0)
    biogas = Energy(energy=0)
    bioethanol = Energy(energy=0)
    biodiesel = Energy(energy=0)

    total = Energy(
        energy=petrol.energy
        + jetfuel.energy
        + diesel.energy
        + elec.energy
        + hydrogen.energy
        + emethan.energy
    )

    return EnergySupply(
        petrol=petrol,
        jetfuel=jetfuel,
        diesel=diesel,
        elec=elec,
        hydrogen=hydrogen,
        emethan=emethan,
        total=total,
        fueloil=fueloil,
        lpg=lpg,
        gas=gas,
        biogas=biogas,
        bioethanol=bioethanol,
        biodiesel=biodiesel,
    )
