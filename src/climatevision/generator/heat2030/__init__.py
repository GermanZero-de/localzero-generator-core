"""
Documentation =
https://localzero-generator.readthedocs.io/de/latest/sectors/heat.html
"""

# pyright: strict

from ..inputs import Inputs
from ..heat2018.h18 import H18
from ..residences2030.r30 import R30
from ..business2030.b30 import B30
from ..agri2030.a30 import A30
from ..industry2030.i30 import I30
from ..electricity2030.electricity2030_core import EColVars2030

from .h30 import H30
from .h import H
from . import energy_demand, energy_general, energy_production


def calc(
    inputs: Inputs,
    *,
    h18: H18,
    r30: R30,
    b30: B30,
    a30: A30,
    i30: I30,
    p_local_biomass_cogen: EColVars2030,
) -> H30:

    demand = energy_demand.calc_demand(r30, b30, i30, a30)

    production = energy_production.calc_production(
        inputs,
        h18,
        r30,
        b30,
        a30,
        i30,
        p_local_biomass_cogen,
    )

    general = energy_general.calc_general(
        inputs=inputs, p_heatnet_energy=production.heatnet.energy
    )

    h = H.of_p_and_g(production.total, general.g)

    p_fossil_change_CO2e_t = (
        production.total.change_CO2e_t - production.heatnet.change_CO2e_t
    )

    return H30(
        h=h,
        g=general.g,
        g_storage=general.g_storage,
        g_planning=general.g_planning,
        d=demand.total,
        d_r=demand.residences,
        d_b=demand.business,
        d_i=demand.industry,
        d_t=demand.transport,
        d_a=demand.agri,
        p=production.total,
        p_gas=production.gas,
        p_lpg=production.lpg,
        p_fueloil=production.fueloil,
        p_opetpro=production.opetpro,
        p_coal=production.coal,
        p_heatnet=production.heatnet,
        p_heatnet_cogen=production.heatnet_cogen,
        p_heatnet_plant=production.heatnet_plant,
        p_heatnet_lheatpump=production.heatnet_lheatpump,
        p_heatnet_geoth=production.heatnet_geoth,
        p_biomass=production.biomass,
        p_ofossil=production.ofossil,
        p_orenew=production.orenew,
        p_solarth=production.solarth,
        p_heatpump=production.heatpump,
        p_fossil_change_CO2e_t=p_fossil_change_CO2e_t,
    )
