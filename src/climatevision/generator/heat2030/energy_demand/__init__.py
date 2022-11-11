# pyright: strict

from dataclasses import dataclass

from ...residences2030.r30 import R30
from ...business2030.b30 import B30
from ...industry2030.i30 import I30
from ...agri2030.a30 import A30
from ...common.energy import Energy as EnergyDemand


@dataclass(kw_only=True)
class Demand:
    residences: EnergyDemand
    business: EnergyDemand
    industry: EnergyDemand
    transport: EnergyDemand
    agri: EnergyDemand

    total: EnergyDemand


def calc_demand(r30: R30, b30: B30, i30: I30, a30: A30) -> Demand:

    residences = EnergyDemand(
        energy=r30.s_biomass.energy
        + r30.s_heatnet.energy
        + r30.s_solarth.energy
        + r30.s_heatpump.energy
    )
    business = EnergyDemand(
        energy=b30.s_biomass.energy
        + b30.s_heatnet.energy
        + b30.s_heatpump.energy
        + b30.s_solarth.energy
    )
    industry = EnergyDemand(
        energy=i30.s_renew_biomass.energy + i30.s_renew_heatnet.energy
    )
    agri = EnergyDemand(energy=a30.s_biomass.energy + a30.s_heatpump.energy)
    transport = EnergyDemand(energy=0.0)

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
