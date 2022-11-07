# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy

from ..transport import Transport
from ..energy_demand import Ship


@dataclass(kw_only=True)
class EnergySupply:
    s: Energy
    s_petrol: Energy
    s_jetfuel: Energy
    s_diesel: Energy
    s_fueloil: Energy
    s_lpg: Energy
    s_gas: Energy
    s_biogas: Energy
    s_bioethanol: Energy
    s_biodiesel: Energy
    s_elec: Energy


def calc_supply(t: Transport, ship_inter: Ship) -> EnergySupply:

    s_biodiesel = Energy(energy=t.demand_biodiesel)
    s_bioethanol = Energy(energy=t.demand_bioethanol)
    s_biogas = Energy(energy=t.demand_biogas)
    s_diesel = Energy(energy=t.demand_diesel)
    s_elec = Energy(energy=t.demand_electricity)
    s_fueloil = Energy(energy=ship_inter.demand_fueloil)
    s_gas = Energy(energy=t.demand_gas)
    s_jetfuel = Energy(energy=t.demand_jetfuel)
    s_lpg = Energy(energy=t.demand_lpg)
    s_petrol = Energy(energy=t.demand_petrol)

    s = Energy(
        energy=s_biodiesel.energy
        + s_bioethanol.energy
        + s_biogas.energy
        + s_diesel.energy
        + s_elec.energy
        + s_fueloil.energy
        + s_gas.energy
        + s_jetfuel.energy
        + s_lpg.energy
        + s_petrol.energy
    )

    return EnergySupply(
        s=s,
        s_petrol=s_petrol,
        s_jetfuel=s_jetfuel,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biogas=s_biogas,
        s_bioethanol=s_bioethanol,
        s_biodiesel=s_biodiesel,
        s_elec=s_elec,
    )
