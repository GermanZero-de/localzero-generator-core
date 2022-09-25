# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...transport2018.t18 import T18
from ...common.energy import Energy as EnergyDemand


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

    residences = EnergyDemand(
        energy=entries.r_coal_fec
        + entries.r_fueloil_fec
        + entries.r_lpg_fec
        + entries.r_gas_fec
        + entries.r_biomass_fec
        + entries.r_orenew_fec
        + entries.r_heatnet_fec
    )

    business = EnergyDemand(
        energy=entries.b_coal_fec
        + entries.b_fueloil_fec
        + entries.b_lpg_fec
        + entries.b_gas_fec
        + entries.b_biomass_fec
        + entries.b_orenew_fec
        + entries.b_heatnet_fec
    )

    industry = EnergyDemand(
        energy=entries.i_coal_fec
        + entries.i_fueloil_fec
        + entries.i_lpg_fec
        + entries.i_opetpro_fec
        + entries.i_gas_fec
        + entries.i_biomass_fec
        + entries.i_orenew_fec
        + entries.i_ofossil_fec
        + entries.i_heatnet_fec
    )

    transport = EnergyDemand(
        energy=t18.t.demand_fueloil + t18.t.demand_lpg + t18.t.demand_gas
    )

    agri = EnergyDemand(
        energy=entries.a_fueloil_fec
        + entries.a_lpg_fec
        + entries.a_gas_fec
        + entries.a_biomass_fec
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
