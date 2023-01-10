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
    Vars11,
    Vars12,
    Vars13,
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
    ass = inputs.ass
    entries = inputs.entries

    p = Vars5()
    p_heatnet_plant = Vars11()
    p_heatnet_lheatpump = Vars12()
    p_heatnet_geoth = Vars13()

    demand = energy_demand.calc_demand(r30, b30, i30, a30)

    p_heatnet_energy = (
        r30.s_heatnet.energy + b30.s_heatnet.energy + i30.s_renew_heatnet.energy
    )
    heatnet_cogen_energy = (
        p_local_biomass_cogen.energy
        if (p_local_biomass_cogen.energy < p_heatnet_energy)
        else p_heatnet_energy
    )

    p_heatnet_plant.invest_per_x = fact("Fact_H_P_heatnet_solarth_park_invest_203X")
    p_heatnet_plant.pct_energy = ass("Ass_H_P_heatnet_fraction_solarth_2050")
    p_heatnet_plant.energy = (
        (p_heatnet_energy - heatnet_cogen_energy) * p_heatnet_plant.pct_energy
        if (heatnet_cogen_energy < p_heatnet_energy)
        else 0
    )
    p_heatnet_plant.area_ha_available = p_heatnet_plant.energy / fact(
        "Fact_H_P_heatnet_solarth_park_yield_2025"
    )
    p_heatnet_plant.invest = (
        p_heatnet_plant.invest_per_x * p_heatnet_plant.area_ha_available
    )
    p_heatnet_plant.invest_pa = p_heatnet_plant.invest / entries.m_duration_target
    p_heatnet_plant.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    p_heatnet_plant.cost_wage = p_heatnet_plant.pct_of_wage * p_heatnet_plant.invest_pa
    p_heatnet_plant.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    p_heatnet_plant.CO2e_production_based = (
        p_heatnet_plant.energy * p_heatnet_plant.CO2e_production_based_per_MWh
    )
    p_heatnet_plant.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    p_heatnet_plant.demand_emplo = div(
        p_heatnet_plant.cost_wage, p_heatnet_plant.ratio_wage_to_emplo
    )
    p_heatnet_plant.CO2e_total = p_heatnet_plant.CO2e_production_based
    p_heatnet_plant.change_energy_MWh = (
        p_heatnet_plant.energy - h18.p_heatnet_plant.energy
    )
    p_heatnet_plant.change_energy_pct = div(
        p_heatnet_plant.change_energy_MWh, h18.p_heatnet_plant.energy
    )
    p_heatnet_plant.change_CO2e_t = (
        p_heatnet_plant.CO2e_total - h18.p_heatnet_plant.CO2e_total
    )
    p_heatnet_plant.change_CO2e_pct = div(
        p_heatnet_plant.change_CO2e_t, h18.p_heatnet_plant.CO2e_total
    )
    p_heatnet_plant.CO2e_total_2021_estimated = h18.p_heatnet_plant.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_heatnet_plant.cost_climate_saved = (
        (p_heatnet_plant.CO2e_total_2021_estimated - p_heatnet_plant.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_heatnet_plant.invest_pa_com = p_heatnet_plant.invest_pa
    p_heatnet_plant.invest_com = p_heatnet_plant.invest
    p_heatnet_plant.demand_emplo_new = p_heatnet_plant.demand_emplo

    p_heatnet_lheatpump.invest_per_x = fact("Fact_H_P_heatnet_lheatpump_invest_203X")
    p_heatnet_lheatpump.pct_energy = ass("Ass_H_P_heatnet_fraction_lheatpump_2050")
    p_heatnet_lheatpump.full_load_hour = fact(
        "Fact_H_P_heatnet_lheatpump_full_load_hours"
    )
    p_heatnet_lheatpump.energy = (
        (p_heatnet_energy - heatnet_cogen_energy) * p_heatnet_lheatpump.pct_energy
        if (heatnet_cogen_energy < p_heatnet_energy)
        else 0
    )
    p_heatnet_lheatpump.pct_of_wage = fact(
        "Fact_B_P_constr_main_revenue_pct_of_wage_2017"
    )
    p_heatnet_lheatpump.power_to_be_installed = div(
        p_heatnet_lheatpump.energy, p_heatnet_lheatpump.full_load_hour
    )
    p_heatnet_lheatpump.invest = (
        p_heatnet_lheatpump.invest_per_x * p_heatnet_lheatpump.power_to_be_installed
    )
    p_heatnet_lheatpump.invest_pa = (
        p_heatnet_lheatpump.invest / entries.m_duration_target
    )
    p_heatnet_lheatpump.cost_wage = (
        p_heatnet_lheatpump.pct_of_wage * p_heatnet_lheatpump.invest_pa
    )
    p_heatnet_lheatpump.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    p_heatnet_lheatpump.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    p_heatnet_lheatpump.demand_emplo = div(
        p_heatnet_lheatpump.cost_wage, p_heatnet_lheatpump.ratio_wage_to_emplo
    )
    p_heatnet_lheatpump.demand_emplo_new = p_heatnet_lheatpump.demand_emplo
    p_heatnet_lheatpump.CO2e_production_based = (
        p_heatnet_lheatpump.energy * p_heatnet_lheatpump.CO2e_production_based_per_MWh
    )
    p_heatnet_lheatpump.demand_electricity = p_heatnet_lheatpump.energy / fact(
        "Fact_H_P_heatnet_lheatpump_apf"
    )
    p_heatnet_lheatpump.CO2e_total = p_heatnet_lheatpump.CO2e_production_based

    p_heatnet_lheatpump.change_energy_MWh = (
        p_heatnet_lheatpump.energy - h18.p_heatnet_lheatpump.energy
    )
    p_heatnet_lheatpump.change_energy_pct = 0

    p_heatnet_lheatpump.change_CO2e_t = (
        p_heatnet_lheatpump.CO2e_total - h18.p_heatnet_lheatpump.CO2e_total
    )
    p_heatnet_lheatpump.change_CO2e_pct = 0

    p_heatnet_lheatpump.CO2e_total_2021_estimated = (
        h18.p_heatnet_lheatpump.CO2e_total * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    p_heatnet_lheatpump.cost_climate_saved = (
        (p_heatnet_lheatpump.CO2e_total_2021_estimated - p_heatnet_lheatpump.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_heatnet_lheatpump.invest_pa_com = p_heatnet_lheatpump.invest_pa
    p_heatnet_lheatpump.invest_com = p_heatnet_lheatpump.invest

    p_heatnet_geoth.pct_energy = ass("Ass_H_P_heatnet_fraction_geoth_2050")
    p_heatnet_geoth.energy = (
        (p_heatnet_energy - heatnet_cogen_energy) * p_heatnet_geoth.pct_energy
        if (heatnet_cogen_energy < p_heatnet_energy)
        else 0
    )
    p_heatnet_geoth.full_load_hour = fact("Fact_H_P_heatnet_geoth_full_load_hours")
    p_heatnet_geoth.power_to_be_installed = div(
        p_heatnet_geoth.energy, p_heatnet_geoth.full_load_hour
    )
    p_heatnet_geoth.invest_per_x = fact("Fact_H_P_heatnet_geoth_invest_203X")
    p_heatnet_geoth.invest = (
        p_heatnet_geoth.invest_per_x * p_heatnet_geoth.power_to_be_installed
    )
    p_heatnet_geoth.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    p_heatnet_geoth.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    p_heatnet_geoth.invest_pa = p_heatnet_geoth.invest / entries.m_duration_target
    p_heatnet_geoth.cost_wage = p_heatnet_geoth.pct_of_wage * p_heatnet_geoth.invest_pa
    p_heatnet_geoth.ratio_wage_to_emplo = fact(
        "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
    )
    p_heatnet_geoth.demand_emplo = div(
        p_heatnet_geoth.cost_wage, p_heatnet_geoth.ratio_wage_to_emplo
    )
    p_heatnet_geoth.demand_emplo_new = p_heatnet_geoth.demand_emplo
    p_heatnet_geoth.CO2e_production_based = (
        p_heatnet_geoth.energy * p_heatnet_geoth.CO2e_production_based_per_MWh
    )
    p_heatnet_geoth.CO2e_total = p_heatnet_geoth.CO2e_production_based
    p_heatnet_geoth.change_energy_MWh = (
        p_heatnet_geoth.energy - h18.p_heatnet_geoth.energy
    )
    p_heatnet_geoth.change_energy_pct = 0
    p_heatnet_geoth.change_CO2e_t = (
        p_heatnet_geoth.CO2e_total - h18.p_heatnet_geoth.CO2e_total
    )
    p_heatnet_geoth.change_CO2e_pct = 0
    p_heatnet_geoth.CO2e_total_2021_estimated = h18.p_heatnet_geoth.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p_heatnet_geoth.cost_climate_saved = (
        (p_heatnet_geoth.CO2e_total_2021_estimated - p_heatnet_geoth.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    p_heatnet_geoth.invest_pa_com = p_heatnet_geoth.invest_pa
    p_heatnet_geoth.invest_com = p_heatnet_geoth.invest

    production = energy_production.calc_production(
        inputs,
        h18,
        r30,
        b30,
        a30,
        i30,
        heatnet_cogen_energy,
        p_heatnet_energy,
        p_heatnet_plant,
        p_heatnet_lheatpump,
        p_heatnet_geoth,
    )

    p.demand_electricity = p_heatnet_lheatpump.demand_electricity
    p.CO2e_total_2021_estimated = h18.p.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    p.energy = (
        production.gas.energy
        + production.lpg.energy
        + production.fueloil.energy
        + production.opetpro.energy
        + production.coal.energy
        + p_heatnet_energy
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
        p_heatnet_plant=p_heatnet_plant,
        p_heatnet_lheatpump=p_heatnet_lheatpump,
        p_heatnet_geoth=p_heatnet_geoth,
        p_biomass=production.biomass,
        p_ofossil=production.ofossil,
        p_orenew=production.orenew,
        p_solarth=production.solarth,
        p_heatpump=production.heatpump,
        p_fossil_change_CO2e_t=p_fossil_change_CO2e_t,
    )
