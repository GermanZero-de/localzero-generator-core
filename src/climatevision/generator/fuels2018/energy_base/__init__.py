# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...common.energy import Energy
from ...industry2018.i18 import I18
from ...transport2018.t18 import T18


@dataclass(kw_only=True)
class Energies:
    r18_petrol: Energy

    b18_petrol: Energy
    b18_jetfuel: Energy
    b18_diesel: Energy

    a18_petrol: Energy
    a18_diesel: Energy

    i18_fossil_diesel: Energy

    t18_petrol: Energy
    t18_jetfuel: Energy
    t18_diesel: Energy
    t18_biogas: Energy
    t18_bioethanol: Energy
    t18_biodiesel: Energy


def calc(entries: Entries, t18: T18, i18: I18) -> Energies:
    r18_petrol = Energy(energy=entries.r_petrol_fec)

    b18_petrol = Energy(energy=entries.b_petrol_fec)
    b18_jetfuel = Energy(energy=entries.b_jetfuel_fec)
    b18_diesel = Energy(energy=entries.b_diesel_fec)

    a18_petrol = Energy(energy=entries.a_petrol_fec)
    a18_diesel = Energy(energy=entries.a_diesel_fec)

    i18_fossil_diesel = Energy(energy=i18.s_fossil_diesel.energy)

    t18_petrol = Energy(energy=t18.t.demand_petrol)
    t18_jetfuel = Energy(energy=t18.t.demand_jetfuel)
    t18_diesel = Energy(energy=t18.t.demand_diesel)
    t18_biogas = Energy(energy=t18.t.demand_biogas)
    t18_bioethanol = Energy(energy=t18.t.demand_bioethanol)
    t18_biodiesel = Energy(energy=t18.t.demand_biodiesel)

    return Energies(
        r18_petrol=r18_petrol,
        b18_petrol=b18_petrol,
        b18_jetfuel=b18_jetfuel,
        b18_diesel=b18_diesel,
        a18_petrol=a18_petrol,
        a18_diesel=a18_diesel,
        i18_fossil_diesel=i18_fossil_diesel,
        t18_petrol=t18_petrol,
        t18_jetfuel=t18_jetfuel,
        t18_diesel=t18_diesel,
        t18_biogas=t18_biogas,
        t18_bioethanol=t18_bioethanol,
        t18_biodiesel=t18_biodiesel,
    )
