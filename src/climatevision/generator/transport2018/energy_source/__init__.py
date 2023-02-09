# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy

from ..transport import Transport
from ..energy_demand import Ship


@dataclass(kw_only=True)
class EnergySupply:
    total: Energy
    petrol: Energy
    jetfuel: Energy
    diesel: Energy
    fueloil: Energy
    lpg: Energy
    gas: Energy
    biogas: Energy
    bioethanol: Energy
    biodiesel: Energy
    elec: Energy


def calc_supply(t: Transport, ship_inter: Ship) -> EnergySupply:

    biodiesel = Energy(energy=t.demand_biodiesel)
    bioethanol = Energy(energy=t.demand_bioethanol)
    biogas = Energy(energy=t.demand_biogas)
    diesel = Energy(energy=t.demand_diesel)
    elec = Energy(energy=t.demand_electricity)
    fueloil = Energy(energy=ship_inter.demand_fueloil)
    gas = Energy(energy=t.demand_gas)
    jetfuel = Energy(energy=t.demand_jetfuel)
    lpg = Energy(energy=t.demand_lpg)
    petrol = Energy(energy=t.demand_petrol)

    total = Energy(
        energy=biodiesel.energy
        + bioethanol.energy
        + biogas.energy
        + diesel.energy
        + elec.energy
        + fueloil.energy
        + gas.energy
        + jetfuel.energy
        + lpg.energy
        + petrol.energy
    )

    return EnergySupply(
        total=total,
        petrol=petrol,
        jetfuel=jetfuel,
        diesel=diesel,
        fueloil=fueloil,
        lpg=lpg,
        gas=gas,
        biogas=biogas,
        bioethanol=bioethanol,
        biodiesel=biodiesel,
        elec=elec,
    )
