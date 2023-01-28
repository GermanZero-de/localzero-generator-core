"""
Documentation =
https://localzero-generator.readthedocs.io/de/latest/sectors/heat.html
"""

# pyright: strict

from ..inputs import Inputs
from ..utils import div
from ..heat2018.h18 import H18
from ..residences2030.r30 import R30
from ..business2030.b30 import B30
from ..agri2030.a30 import A30
from ..industry2030.i30 import I30
from ..electricity2030.electricity2030_core import EColVars2030

from .h30 import H30
from .dataclasses import (
    Vars0,
    Vars5,
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
    fact = inputs.fact
    entries = inputs.entries

    p = Vars5()

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

    p.demand_electricity = production.heatnet_lheatpump.demand_electricity
    p.CO2e_total_2021_estimated = h18.p.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p.energy = (
        production.gas.energy
        + production.lpg.energy
        + production.fueloil.energy
        + production.opetpro.energy
        + production.coal.energy
        + production.heatnet.energy
        + production.biomass.energy
        + production.ofossil.energy
        + production.orenew.energy
    )
    p.change_energy_MWh = p.energy - h18.p.energy
    p.CO2e_combustion_based = (
        production.gas.CO2e_combustion_based
        + production.lpg.CO2e_combustion_based
        + production.fueloil.CO2e_combustion_based
        + production.opetpro.CO2e_combustion_based
        + production.coal.CO2e_combustion_based
        + production.heatnet.CO2e_combustion_based
    )
    p.invest = production.heatnet.invest
    p.demand_emplo = production.heatnet.demand_emplo
    p.demand_emplo_new = production.heatnet.demand_emplo_new
    p.invest_pa_com = production.heatnet.invest_pa_com
    p.invest_pa = production.heatnet.invest_pa
    p.invest_com = production.heatnet.invest_com
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
    p.cost_wage = production.heatnet.cost_wage
    p.change_energy_pct = div(p.change_energy_MWh, h18.p.energy)
    p.cost_fuel = (
        production.gas.cost_fuel
        + production.fueloil.cost_fuel
        + production.coal.cost_fuel
        + production.biomass.cost_fuel
    )
    p.cost_climate_saved = (
        (p.CO2e_total_2021_estimated - p.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p.change_CO2e_t = p.CO2e_total - h18.p.CO2e_total
    p.change_CO2e_pct = div(p.change_CO2e_t, h18.p.CO2e_total)
    p.CO2e_production_based = (
        production.gas.CO2e_production_based
        + production.opetpro.CO2e_production_based
        + production.coal.CO2e_production_based
        + production.heatnet.CO2e_production_based
        + production.biomass.CO2e_production_based
        + production.ofossil.CO2e_production_based
        + production.orenew.CO2e_production_based
    )

    general = energy_general.calc_general(
        inputs=inputs, p_heatnet_energy=production.heatnet.energy
    )

    h = Vars0()
    h.CO2e_total_2021_estimated = p.CO2e_total_2021_estimated
    h.CO2e_combustion_based = p.CO2e_combustion_based
    h.invest_pa = general.g.invest_pa + p.invest_pa
    h.invest_pa_com = general.g.invest_pa_com + p.invest_pa_com
    h.cost_wage = general.g.cost_wage + p.cost_wage
    h.demand_emplo = general.g.demand_emplo + p.demand_emplo
    h.demand_emplo_new = general.g.demand_emplo_new + p.demand_emplo_new
    h.invest_com = general.g.invest_com + p.invest_com
    h.invest = general.g.invest + p.invest
    h.CO2e_total = p.CO2e_total
    h.cost_climate_saved = p.cost_climate_saved
    h.change_CO2e_t = p.change_CO2e_t
    h.change_energy_pct = p.change_energy_pct
    h.CO2e_production_based = p.CO2e_production_based
    h.change_CO2e_pct = p.change_CO2e_pct
    h.change_energy_MWh = p.change_energy_MWh

    # TODO: Check demand_emplo_new in Heat with Hauke
    h.demand_emplo_com = general.g.demand_emplo_com

    p_fossil_change_CO2e_t = p.change_CO2e_t - production.heatnet.change_CO2e_t

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
        p=p,
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
