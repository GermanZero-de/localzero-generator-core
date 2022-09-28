"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/heat.html
"""

# pyright: strict

from ..inputs import Inputs
from ..utils import div
from ..transport2018.t18 import T18
from ..electricity2018.e18 import E18

from .h18 import H18, CO2eEmissions
from .dataclasses import (
    Vars3,
)
from . import energy_demand, energy_production


def calc(inputs: Inputs, *, t18: T18, e18: E18) -> H18:
    entries = inputs.entries

    demand = energy_demand.calc_demand(inputs, t18)

    p_heatnet_energy = (
        entries.r_heatnet_fec + entries.b_heatnet_fec + entries.i_heatnet_fec
    )

    production = energy_production.calc_production(
        inputs, t18, e18, demand.total.energy, p_heatnet_energy
    )

    p = Vars3()
    p.energy = demand.total.energy
    p.CO2e_production_based = (
        production.gas.CO2e_production_based
        + production.opetpro.CO2e_production_based
        + production.coal.CO2e_production_based
        + production.biomass.CO2e_production_based
        + production.ofossil.CO2e_production_based
        + production.orenew.CO2e_production_based
    )
    p.CO2e_combustion_based = (
        production.gas.CO2e_combustion_based
        + production.lpg.CO2e_combustion_based
        + production.fueloil.CO2e_combustion_based
        + production.opetpro.CO2e_combustion_based
        + production.coal.CO2e_combustion_based
        + production.heatnet.CO2e_combustion_based
    )
    p.CO2e_combustion_based_per_MWh = div(p.CO2e_combustion_based, p.energy)
    p.CO2e_total = (
        production.gas.CO2e_total
        + production.lpg.CO2e_total
        + production.fueloil.CO2e_total
        + production.opetpro.CO2e_total
        + production.coal.CO2e_total
        + production.heatnet.CO2e_total
        + production.biomass.CO2e_total
        + production.ofossil.CO2e_total
        + production.orenew.CO2e_total
    )
    p.pct_energy = (
        production.gas.pct_energy
        + production.lpg.pct_energy
        + production.fueloil.pct_energy
        + production.opetpro.pct_energy
        + production.coal.pct_energy
        + production.heatnet.pct_energy
        + production.biomass.pct_energy
        + production.ofossil.pct_energy
        + production.orenew.pct_energy
    )

    h = CO2eEmissions(
        CO2e_combustion_based=p.CO2e_combustion_based,
        CO2e_production_based=p.CO2e_production_based,
        CO2e_total=p.CO2e_total,
    )

    return H18(
        d=demand.total,
        d_r=demand.residences,
        d_b=demand.business,
        d_i=demand.industry,
        d_t=demand.transport,
        d_a=demand.agri,
        h=h,
        p=p,
        p_gas=production.gas,
        p_lpg=production.lpg,
        p_fueloil=production.fueloil,
        p_opetpro=production.opetpro,
        p_coal=production.coal,
        p_heatnet=production.heatnet,
        p_heatnet_cogen=production.heatnet_cogen,
        p_heatnet_plant=production.heatnet_plant,
        p_heatnet_geoth=production.heatnet_geoth,
        p_heatnet_lheatpump=production.heatnet_lheatpump,
        p_biomass=production.biomass,
        p_ofossil=production.ofossil,
        p_orenew=production.orenew,
        p_solarth=production.solarth,
        p_heatpump=production.heatpump,
    )
