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
from .dataclasses import (
    Vars0,
)
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

    h = Vars0()
    h.CO2e_total_2021_estimated = production.total.CO2e_total_2021_estimated
    h.CO2e_combustion_based = production.total.CO2e_combustion_based
    h.invest_pa = general.g.invest_pa + production.total.invest_pa
    h.invest_pa_com = general.g.invest_pa_com + production.total.invest_pa_com
    h.cost_wage = general.g.cost_wage + production.total.cost_wage
    h.demand_emplo = general.g.demand_emplo + production.total.demand_emplo
    h.demand_emplo_new = general.g.demand_emplo_new + production.total.demand_emplo_new
    h.invest_com = general.g.invest_com + production.total.invest_com
    h.invest = general.g.invest + production.total.invest
    h.CO2e_total = production.total.CO2e_total
    h.cost_climate_saved = production.total.cost_climate_saved
    h.change_CO2e_t = production.total.change_CO2e_t
    h.change_energy_pct = production.total.change_energy_pct
    h.CO2e_production_based = production.total.CO2e_production_based
    h.change_CO2e_pct = production.total.change_CO2e_pct
    h.change_energy_MWh = production.total.change_energy_MWh

    # TODO: Check demand_emplo_new in Heat with Hauke
    h.demand_emplo_com = general.g.demand_emplo_com

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
