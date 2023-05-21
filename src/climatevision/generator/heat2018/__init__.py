"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/heat.html
"""

# pyright: strict

from ..inputs import Inputs
from ..transport2018.t18 import T18
from ..electricity2018.e18 import E18
from ..industry2018.i18 import I18

from .h18 import H18, CO2eEmission
from . import energy_base, energy_demand, energy_production


def calc(inputs: Inputs, *, t18: T18, e18: E18, i18: I18) -> H18:

    energies = energy_base.calc(inputs, t18, i18, e18)
    demand = energy_demand.calc_demand(energies)
    production = energy_production.calc_production(inputs, energies)

    h = CO2eEmission(
        CO2e_combustion_based=production.total.CO2e_combustion_based,
        CO2e_production_based=production.total.CO2e_production_based,
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
