# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...transport2018.t18 import T18

from .dataclasses import Vars1


@dataclass(kw_only=True)
class Demand:
    residences: Vars1
    business: Vars1
    industry: Vars1
    transport: Vars1
    agri: Vars1

    total: Vars1


def calc_demand(inputs: Inputs, t18: T18) -> Demand:

    entries = inputs.entries

    residences = Vars1(
        energy=entries.r_coal_fec
        + entries.r_fueloil_fec
        + entries.r_lpg_fec
        + entries.r_gas_fec
        + entries.r_biomass_fec
        + entries.r_orenew_fec
        + entries.r_heatnet_fec
    )

    business = Vars1(
        energy=entries.b_coal_fec
        + entries.b_fueloil_fec
        + entries.b_lpg_fec
        + entries.b_gas_fec
        + entries.b_biomass_fec
        + entries.b_orenew_fec
        + entries.b_heatnet_fec
    )

    industry = Vars1(
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

    transport = Vars1(energy=t18.t.demand_fueloil + t18.t.demand_lpg + t18.t.demand_gas)

    agri = Vars1(
        energy=entries.a_fueloil_fec
        + entries.a_lpg_fec
        + entries.a_gas_fec
        + entries.a_biomass_fec
    )

    total = Vars1(
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
