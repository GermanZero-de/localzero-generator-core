"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/heat.html
"""

# pyright: strict

from ..inputs import Inputs
from ..transport2018.t18 import T18
from ..electricity2018.e18 import E18
from climatevision.generator import diffs

from .h18 import H18, CO2eEmissions
from . import energy_demand, energy_production


def calc(inputs: Inputs, *, t18: T18, e18: E18) -> H18:
    entries = inputs.entries

    demand = energy_demand.calc_demand(inputs, t18)

    p_heatnet_energy = (
        entries.r_heatnet_fec + entries.b_heatnet_fec + entries.i_heatnet_fec
    )

    production = energy_production.calc_production(inputs, t18, e18, p_heatnet_energy)

    assert diffs.float_matches(
        actual=demand.total.energy, expected=production.total.energy, rel=1e-9
    )

    h = CO2eEmissions(
        CO2e_combustion_based=production.total.CO2e_combustion_based,
        CO2e_production_based=production.total.CO2e_production_based,
        CO2e_total=production.total.CO2e_total,
    )

    return H18(
        d=demand.total,
        d_r=demand.residences,
        d_b=demand.business,
        d_i=demand.industry,
        d_t=demand.transport,
        d_a=demand.agri,
        h=h,
        p=production.total,
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
