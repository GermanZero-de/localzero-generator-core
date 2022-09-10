# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...transport2018.t18 import T18
from ...commonDataclasses.energy import Energy as EnergyDemand


@dataclass(kw_only=True)
class Demand:
    residences: EnergyDemand
    business: EnergyDemand
    industry: EnergyDemand
    transport: EnergyDemand
    agri: EnergyDemand

    total: EnergyDemand


def calc_demand(inputs: Inputs, t18: T18) -> Demand:

    entries = inputs.entries

    residences = EnergyDemand(energy=entries.r_petrol_fec)

    business = EnergyDemand(
        energy=entries.b_petrol_fec + entries.b_jetfuel_fec + entries.b_diesel_fec
    )

    industry = EnergyDemand(energy=entries.i_diesel_fec)

    transport = EnergyDemand(
        energy=t18.t.demand_petrol
        + t18.t.demand_jetfuel
        + t18.t.demand_diesel
        + t18.t.demand_biogas
        + t18.t.demand_bioethanol
        + t18.t.demand_biodiesel
    )

    agri = EnergyDemand(energy=entries.a_petrol_fec + entries.a_diesel_fec)

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
