# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy

from ..t import T


@dataclass(kw_only=True)
class EnergySupply:
    s: Energy
    s_diesel: Energy
    s_emethan: Energy
    s_jetfuel: Energy
    s_petrol: Energy
    s_fueloil: Energy
    s_lpg: Energy
    s_gas: Energy
    s_biogas: Energy
    s_bioethanol: Energy
    s_biodiesel: Energy
    s_elec: Energy
    s_hydrogen: Energy


def calc_supply(t: T) -> EnergySupply:

    s_petrol = Energy(energy=t.transport.demand_epetrol)
    s_jetfuel = Energy(energy=t.transport.demand_ejetfuel)
    s_diesel = Energy(energy=t.transport.demand_ediesel)
    s_elec = Energy(energy=t.transport.demand_electricity)
    s_hydrogen = Energy(energy=t.transport.demand_hydrogen)

    s_emethan = Energy(energy=0)
    s_fueloil = Energy(energy=0)
    s_lpg = Energy(energy=0)
    s_gas = Energy(energy=0)
    s_biogas = Energy(energy=0)
    s_bioethanol = Energy(energy=0)
    s_biodiesel = Energy(energy=0)

    s = Energy(
        energy=s_petrol.energy
        + s_jetfuel.energy
        + s_diesel.energy
        + s_elec.energy
        + s_hydrogen.energy
        + s_emethan.energy
    )

    return EnergySupply(
        s_petrol=s_petrol,
        s_jetfuel=s_jetfuel,
        s_diesel=s_diesel,
        s_elec=s_elec,
        s_hydrogen=s_hydrogen,
        s_emethan=s_emethan,
        s=s,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biogas=s_biogas,
        s_bioethanol=s_bioethanol,
        s_biodiesel=s_biodiesel,
    )
