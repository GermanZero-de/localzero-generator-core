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
    Vars5,
    Vars6,
)
from . import energy_demand, energy_production


def calc(inputs: Inputs, *, t18: T18, e18: E18) -> H18:
    fact = inputs.fact
    entries = inputs.entries

    demand = energy_demand.calc_demand(inputs, t18)

    p_heatnet = Vars6()
    p_heatnet.energy = (
        entries.r_heatnet_fec + entries.b_heatnet_fec + entries.i_heatnet_fec
    )

    production = energy_production.calc_production(
        inputs, t18, demand.total.energy, p_heatnet.energy
    )

    p_lpg = Vars5()
    p_lpg.energy = (
        entries.r_lpg_fec
        + entries.b_lpg_fec
        + entries.i_lpg_fec
        + entries.a_lpg_fec
        + t18.s_lpg.energy
    )
    p_lpg.pct_energy = div(p_lpg.energy, demand.total.energy)
    p_lpg.CO2e_combustion_based_per_MWh = fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018")
    p_lpg.CO2e_combustion_based = p_lpg.energy * p_lpg.CO2e_combustion_based_per_MWh
    p_lpg.CO2e_total = p_lpg.CO2e_combustion_based
    p_fueloil = Vars5()
    p_fueloil.energy = (
        entries.r_fueloil_fec
        + entries.b_fueloil_fec
        + entries.i_fueloil_fec
        + entries.a_fueloil_fec
        + t18.s_fueloil.energy
    )
    p_fueloil.pct_energy = div(p_fueloil.energy, demand.total.energy)
    p_fueloil.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"
    )
    p_fueloil.CO2e_combustion_based = (
        p_fueloil.energy * p_fueloil.CO2e_combustion_based_per_MWh
    )
    p_fueloil.CO2e_total = p_fueloil.CO2e_combustion_based

    p_heatnet.pct_energy = div(p_heatnet.energy, demand.total.energy)
    p_heatnet_cogen = Vars5()
    if (
        e18.p_fossil_coal_brown_cogen.energy
        + e18.p_fossil_coal_black_cogen.energy
        + e18.p_fossil_gas_cogen.energy
        + e18.p_fossil_ofossil_cogen.energy
        + e18.p_renew_biomass_cogen.energy
        < p_heatnet.energy
    ):
        p_heatnet_cogen.energy = (
            e18.p_fossil_coal_brown_cogen.energy
            + e18.p_fossil_coal_black_cogen.energy
            + e18.p_fossil_gas_cogen.energy
            + e18.p_fossil_ofossil_cogen.energy
            + e18.p_renew_biomass_cogen.energy
        )
    else:
        p_heatnet_cogen.energy = p_heatnet.energy
    p_heatnet_cogen.pct_energy = div(p_heatnet_cogen.energy, p_heatnet.energy)
    p_heatnet_cogen.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_heatnet_cogen_ratio_CO2e_cb_to_fec_2018"
    )
    p_heatnet_cogen.CO2e_combustion_based = (
        p_heatnet_cogen.energy * p_heatnet_cogen.CO2e_combustion_based_per_MWh
    )
    p_heatnet_cogen.CO2e_total = p_heatnet_cogen.CO2e_combustion_based
    p_heatnet_plant = Vars5()
    p_heatnet_plant.energy = p_heatnet.energy - p_heatnet_cogen.energy
    p_heatnet_plant.pct_energy = div(p_heatnet_plant.energy, p_heatnet.energy)
    p_heatnet_plant.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"
    )
    p_heatnet_plant.CO2e_combustion_based = (
        p_heatnet_plant.energy * p_heatnet_plant.CO2e_combustion_based_per_MWh
    )
    p_heatnet_plant.CO2e_total = p_heatnet_plant.CO2e_combustion_based
    p_heatnet.CO2e_combustion_based = (
        p_heatnet_cogen.CO2e_combustion_based + p_heatnet_plant.CO2e_combustion_based
    )
    p_heatnet.CO2e_total = p_heatnet.CO2e_combustion_based

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
        + p_lpg.CO2e_combustion_based
        + p_fueloil.CO2e_combustion_based
        + production.opetpro.CO2e_combustion_based
        + production.coal.CO2e_combustion_based
        + p_heatnet.CO2e_combustion_based
    )
    p.CO2e_combustion_based_per_MWh = div(p.CO2e_combustion_based, p.energy)
    p.CO2e_total = (
        production.gas.CO2e_total
        + p_lpg.CO2e_total
        + p_fueloil.CO2e_total
        + production.opetpro.CO2e_total
        + production.coal.CO2e_total
        + p_heatnet.CO2e_total
        + production.biomass.CO2e_total
        + production.ofossil.CO2e_total
        + production.orenew.CO2e_total
    )
    p.pct_energy = (
        production.gas.pct_energy
        + p_lpg.pct_energy
        + p_fueloil.pct_energy
        + production.opetpro.pct_energy
        + production.coal.pct_energy
        + p_heatnet.pct_energy
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
        p_lpg=p_lpg,
        p_fueloil=p_fueloil,
        p_opetpro=production.opetpro,
        p_coal=production.coal,
        p_heatnet=p_heatnet,
        p_heatnet_cogen=p_heatnet_cogen,
        p_heatnet_plant=p_heatnet_plant,
        p_heatnet_geoth=production.heatnet_geoth,
        p_heatnet_lheatpump=production.heatnet_lheatpump,
        p_biomass=production.biomass,
        p_ofossil=production.ofossil,
        p_orenew=production.orenew,
        p_solarth=production.solarth,
        p_heatpump=production.heatpump,
    )
