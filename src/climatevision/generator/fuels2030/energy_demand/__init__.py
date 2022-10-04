# pyright: strict

from dataclasses import dataclass

from ...agri2030.a30 import A30
from ...business2030.b30 import B30
from ...industry2030.i30 import I30
from ...residences2030.r30 import R30
from ...transport2030.t30 import T30
from ...common.energy import Energy as EnergyDemand

from ..energy_production.newEFuelProduction import NewEFuelProduction


@dataclass(kw_only=True)
class Demand:
    residences: EnergyDemand
    business: EnergyDemand
    industry: EnergyDemand
    transport: EnergyDemand
    agri: EnergyDemand

    electricity_hydrogen_reconv: EnergyDemand

    total: EnergyDemand


def calc_demand(
    a30: A30,
    b30: B30,
    i30: I30,
    r30: R30,
    t30: T30,
    p_hydrogen_reconv: NewEFuelProduction,
) -> Demand:

    residences = EnergyDemand(energy=r30.p.demand_emethan)
    business = EnergyDemand(energy=b30.p.demand_ediesel + b30.p.demand_emethan)
    industry = EnergyDemand(energy=i30.p.demand_emethan + i30.p.demand_hydrogen)
    transport = EnergyDemand(
        energy=t30.t.transport.demand_epetrol
        + t30.t.transport.demand_ediesel
        + t30.t.transport.demand_ejetfuel
        + t30.t.transport.demand_hydrogen
    )
    agri = EnergyDemand(
        energy=a30.p_operation.demand_epetrol
        + a30.p_operation.demand_ediesel
        + a30.p_operation.demand_emethan
    )

    electricity_hydrogen_reconv = EnergyDemand(energy=p_hydrogen_reconv.energy)

    total = EnergyDemand(
        energy=residences.energy
        + business.energy
        + industry.energy
        + transport.energy
        + agri.energy
        + electricity_hydrogen_reconv.energy
    )

    return Demand(
        residences=residences,
        business=business,
        industry=industry,
        transport=transport,
        agri=agri,
        electricity_hydrogen_reconv=electricity_hydrogen_reconv,
        total=total,
    )
