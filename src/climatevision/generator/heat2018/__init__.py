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
from .dataclasses import Vars3, Vars4, Vars5, Vars6, Vars7, Vars8
from . import energy_demand


def calc(inputs: Inputs, *, t18: T18, e18: E18) -> H18:
    fact = inputs.fact
    entries = inputs.entries

    demand = energy_demand.calc_demand(inputs, t18)

    p = Vars3()
    p.energy = demand.total.energy
    p_gas = Vars4()
    p_gas.energy = (
        entries.r_gas_fec
        + entries.b_gas_fec
        + entries.i_gas_fec
        + entries.a_gas_fec
        + t18.t.demand_gas
    )
    p_gas.pct_energy = div(p_gas.energy, p.energy)
    p_gas.CO2e_production_based_per_MWh = fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018")
    p_gas.CO2e_production_based = p_gas.energy * p_gas.CO2e_production_based_per_MWh
    p_gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018")
    p_gas.CO2e_combustion_based = p_gas.energy * p_gas.CO2e_combustion_based_per_MWh
    p_gas.CO2e_total = p_gas.CO2e_production_based + p_gas.CO2e_combustion_based
    p_lpg = Vars5()
    p_lpg.energy = (
        entries.r_lpg_fec
        + entries.b_lpg_fec
        + entries.i_lpg_fec
        + entries.a_lpg_fec
        + t18.s_lpg.energy
    )
    p_lpg.pct_energy = div(p_lpg.energy, p.energy)
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
    p_fueloil.pct_energy = div(p_fueloil.energy, p.energy)
    p_fueloil.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"
    )
    p_fueloil.CO2e_combustion_based = (
        p_fueloil.energy * p_fueloil.CO2e_combustion_based_per_MWh
    )
    p_fueloil.CO2e_total = p_fueloil.CO2e_combustion_based
    p_opetpro = Vars4()
    p_opetpro.energy = entries.i_opetpro_fec
    p_opetpro.pct_energy = div(p_opetpro.energy, p.energy)
    p_opetpro.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018"
    )
    p_opetpro.CO2e_production_based = (
        p_opetpro.energy * p_opetpro.CO2e_production_based_per_MWh
    )
    p_opetpro.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018"
    )
    p_opetpro.CO2e_combustion_based = (
        p_opetpro.energy * p_opetpro.CO2e_combustion_based_per_MWh
    )
    p_opetpro.CO2e_total = (
        p_opetpro.CO2e_production_based + p_opetpro.CO2e_combustion_based
    )
    p_coal = Vars4()
    p_coal.energy = entries.r_coal_fec + entries.b_coal_fec + entries.i_coal_fec
    p_coal.pct_energy = div(p_coal.energy, p.energy)
    p_coal.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"
    )
    p_coal.CO2e_production_based = p_coal.energy * p_coal.CO2e_production_based_per_MWh
    p_coal.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"
    )
    p_coal.CO2e_combustion_based = p_coal.energy * p_coal.CO2e_combustion_based_per_MWh
    p_coal.CO2e_total = p_coal.CO2e_production_based + p_coal.CO2e_combustion_based
    p_heatnet = Vars6()
    p_heatnet.energy = (
        entries.r_heatnet_fec + entries.b_heatnet_fec + entries.i_heatnet_fec
    )
    p_heatnet.pct_energy = div(p_heatnet.energy, p.energy)
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
    p_heatnet_geoth = Vars7()
    p_heatnet_geoth.pct_energy = 0
    p_heatnet_geoth.energy = p_heatnet_geoth.pct_energy * p_heatnet.energy
    p_heatnet_geoth.CO2e_combustion_based = 0
    p_heatnet_geoth.CO2e_production_based = 0
    p_heatnet_geoth.CO2e_total = (
        p_heatnet_geoth.CO2e_production_based + p_heatnet_geoth.CO2e_combustion_based
    )
    p_heatnet_lheatpump = Vars7()
    p_heatnet_lheatpump.pct_energy = 0
    p_heatnet_lheatpump.CO2e_production_based = 0
    p_heatnet_lheatpump.CO2e_combustion_based = 0
    p_heatnet_lheatpump.energy = p_heatnet_lheatpump.pct_energy * p_heatnet.energy
    p_heatnet_lheatpump.CO2e_total = (
        p_heatnet_lheatpump.CO2e_production_based
        + p_heatnet_lheatpump.CO2e_combustion_based
    )
    p_biomass = Vars8()
    p_biomass.energy = (
        entries.r_biomass_fec
        + entries.b_biomass_fec
        + entries.i_biomass_fec
        + entries.a_biomass_fec
    )
    p_biomass.pct_energy = div(p_biomass.energy, p.energy)
    p_biomass.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
    )
    p_biomass.CO2e_production_based = (
        p_biomass.energy * p_biomass.CO2e_production_based_per_MWh
    )
    p_biomass.CO2e_total = p_biomass.CO2e_production_based
    p_ofossil = Vars8()
    "p_coal.energy = (\n        entry ('In_I_ofossil_fec')\n\n        #result: 21.019.444 MWh\n    )"
    p_ofossil.energy = entries.i_ofossil_fec
    p_ofossil.pct_energy = div(p_ofossil.energy, p.energy)
    p_ofossil.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
    )
    p_ofossil.CO2e_production_based = (
        p_ofossil.energy * p_ofossil.CO2e_production_based_per_MWh
    )
    p_ofossil.CO2e_total = p_ofossil.CO2e_production_based

    p_orenew = Vars8()
    p_orenew.energy = entries.r_orenew_fec + entries.b_orenew_fec + entries.i_orenew_fec
    p_orenew.pct_energy = div(p_orenew.energy, p.energy)

    p_solarth = Vars8()
    p_solarth.pct_energy = fact("Fact_R_S_ratio_solarth_to_orenew_2018")
    p_solarth.energy = p_orenew.energy * p_solarth.pct_energy

    p_heatpump = Vars8()
    p_heatpump.pct_energy = fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    p_heatpump.energy = p_orenew.energy * p_heatpump.pct_energy

    p_solarth.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    p_solarth.CO2e_production_based = (
        p_solarth.energy * p_solarth.CO2e_production_based_per_MWh
    )
    p_solarth.CO2e_total = p_solarth.CO2e_production_based

    p_heatpump.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    p_heatpump.CO2e_production_based = (
        p_heatpump.energy * p_heatpump.CO2e_production_based_per_MWh
    )
    p_heatpump.CO2e_total = p_heatpump.CO2e_production_based

    p_orenew.CO2e_production_based = (
        p_solarth.CO2e_production_based + p_heatpump.CO2e_production_based
    )
    p_orenew.CO2e_total = p_orenew.CO2e_production_based
    p_orenew.CO2e_production_based_per_MWh = 0

    p.CO2e_production_based = (
        p_gas.CO2e_production_based
        + p_opetpro.CO2e_production_based
        + p_coal.CO2e_production_based
        + p_biomass.CO2e_production_based
        + p_ofossil.CO2e_production_based
        + p_orenew.CO2e_production_based
    )
    p.CO2e_combustion_based = (
        p_gas.CO2e_combustion_based
        + p_lpg.CO2e_combustion_based
        + p_fueloil.CO2e_combustion_based
        + p_opetpro.CO2e_combustion_based
        + p_coal.CO2e_combustion_based
        + p_heatnet.CO2e_combustion_based
    )
    p.CO2e_combustion_based_per_MWh = div(p.CO2e_combustion_based, p.energy)
    p.CO2e_total = (
        p_gas.CO2e_total
        + p_lpg.CO2e_total
        + p_fueloil.CO2e_total
        + p_opetpro.CO2e_total
        + p_coal.CO2e_total
        + p_heatnet.CO2e_total
        + p_biomass.CO2e_total
        + p_ofossil.CO2e_total
        + p_orenew.CO2e_total
    )
    p.pct_energy = (
        p_gas.pct_energy
        + p_lpg.pct_energy
        + p_fueloil.pct_energy
        + p_opetpro.pct_energy
        + p_coal.pct_energy
        + p_heatnet.pct_energy
        + p_biomass.pct_energy
        + p_ofossil.pct_energy
        + p_orenew.pct_energy
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
        p_gas=p_gas,
        p_lpg=p_lpg,
        p_fueloil=p_fueloil,
        p_opetpro=p_opetpro,
        p_coal=p_coal,
        p_heatnet=p_heatnet,
        p_heatnet_cogen=p_heatnet_cogen,
        p_heatnet_plant=p_heatnet_plant,
        p_heatnet_geoth=p_heatnet_geoth,
        p_heatnet_lheatpump=p_heatnet_lheatpump,
        p_biomass=p_biomass,
        p_ofossil=p_ofossil,
        p_orenew=p_orenew,
        p_solarth=p_solarth,
        p_heatpump=p_heatpump,
    )
