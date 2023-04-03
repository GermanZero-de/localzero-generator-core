"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/hh_ghd.html
"""

# pyright: strict

from ..inputs import Inputs
from ..utils import div, MILLION
from ..residences2018.r18 import R18

from .b18 import B18
from .dataclasses import (
    Vars0,
    Vars5,
    Vars6,
    Vars8,
    Vars9,
    Vars10,
)
from . import energy_demand, energy_source


# Berechnungsfunktion im Sektor GHD für 2018
def calc(inputs: Inputs, *, r18: R18) -> B18:
    fact = inputs.fact
    entries = inputs.entries

    b = Vars0()
    s = Vars5()
    s_gas = Vars6()
    s_lpg = Vars6()
    s_petrol = Vars6()
    s_jetfuel = Vars6()
    s_diesel = Vars6()
    s_fueloil = Vars6()
    s_coal = Vars6()
    s_heatnet = Vars6()
    s_elec_heating = Vars8()
    s_heatpump = Vars6()
    s_solarth = Vars6()
    s_elec = Vars8()
    rb = Vars9()
    rp_p = Vars10()

    s_gas.energy = entries.b_gas_fec
    s_gas.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")
    s_gas.cost_fuel = s_gas.energy * s_gas.cost_fuel_per_MWh / MILLION
    s_gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    s_gas.CO2e_combustion_based = s_gas.energy * s_gas.CO2e_combustion_based_per_MWh
    s_gas.CO2e_total = s_gas.CO2e_combustion_based
    s_lpg.energy = entries.b_lpg_fec
    s_lpg.cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    s_lpg.cost_fuel = s_lpg.energy * s_lpg.cost_fuel_per_MWh / MILLION
    s_lpg.CO2e_combustion_based_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    s_lpg.CO2e_combustion_based = s_lpg.energy * s_lpg.CO2e_combustion_based_per_MWh
    s_lpg.CO2e_total = s_lpg.CO2e_combustion_based
    s_petrol.energy = entries.b_petrol_fec
    s_petrol.cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    s_petrol.cost_fuel = s_petrol.energy * s_petrol.cost_fuel_per_MWh / MILLION
    s_petrol.CO2e_combustion_based_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    s_petrol.CO2e_combustion_based = (
        s_petrol.energy * s_petrol.CO2e_combustion_based_per_MWh
    )
    s_petrol.CO2e_total = s_petrol.CO2e_combustion_based
    s_jetfuel.energy = entries.b_jetfuel_fec
    s_jetfuel.cost_fuel_per_MWh = fact("Fact_R_S_kerosine_energy_cost_factor_2018")
    s_jetfuel.cost_fuel = s_jetfuel.energy * s_jetfuel.cost_fuel_per_MWh / MILLION
    s_jetfuel.CO2e_combustion_based_per_MWh = fact("Fact_H_P_kerosene_cb_EF")
    s_jetfuel.CO2e_combustion_based = (
        s_jetfuel.energy * s_jetfuel.CO2e_combustion_based_per_MWh
    )
    s_jetfuel.CO2e_total = s_jetfuel.CO2e_combustion_based
    s_diesel.energy = entries.b_diesel_fec
    s_diesel.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    s_diesel.cost_fuel = s_diesel.energy * s_diesel.cost_fuel_per_MWh / MILLION
    s_diesel.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    s_diesel.CO2e_combustion_based = (
        s_diesel.energy * s_diesel.CO2e_combustion_based_per_MWh
    )
    s_diesel.CO2e_total = s_diesel.CO2e_combustion_based
    s_fueloil.energy = entries.b_fueloil_fec
    s_fueloil.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    s_fueloil.cost_fuel = s_fueloil.energy * s_fueloil.cost_fuel_per_MWh / MILLION
    s_fueloil.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    s_fueloil.CO2e_combustion_based = (
        s_fueloil.energy * s_fueloil.CO2e_combustion_based_per_MWh
    )
    s_fueloil.CO2e_total = s_fueloil.CO2e_combustion_based
    s_coal.energy = entries.b_coal_fec
    s_coal.cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    s_coal.cost_fuel = s_coal.energy * s_coal.cost_fuel_per_MWh / MILLION
    s_coal.CO2e_combustion_based_per_MWh = fact("Fact_R_S_coal_CO2e_EF")
    s_coal.CO2e_combustion_based = s_coal.energy * s_coal.CO2e_combustion_based_per_MWh
    s_coal.CO2e_total = s_coal.CO2e_combustion_based
    s_heatnet.energy = entries.b_heatnet_fec
    s_heatnet.cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    s_heatnet.cost_fuel = s_heatnet.energy * s_heatnet.cost_fuel_per_MWh / MILLION
    s_heatnet.CO2e_combustion_based = 0
    s_heatnet.CO2e_combustion_based_per_MWh = 0
    s_heatnet.CO2e_total = 0
    s_elec_heating.energy = (
        fact("Fact_B_S_elec_heating_fec_2018")
        * entries.r_flats_wo_heatnet
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    s_elec_heating.CO2e_combustion_based = 0
    s_elec_heating.CO2e_combustion_based_per_MWh = 0
    s_elec_heating.CO2e_total = 0
    s_heatpump.energy = entries.b_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    s_heatpump.cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )
    s_heatpump.cost_fuel = s_heatpump.energy * s_heatpump.cost_fuel_per_MWh / MILLION
    s_heatpump.CO2e_combustion_based = 0
    s_heatpump.CO2e_combustion_based_per_MWh = 0
    s_heatpump.CO2e_total = 0
    s_solarth.energy = entries.b_orenew_fec * (
        1 - fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    )
    s_solarth.cost_fuel_per_MWh = 0
    s_solarth.cost_fuel = 0
    s_solarth.CO2e_combustion_based = 0
    s_solarth.CO2e_combustion_based_per_MWh = 0
    s_solarth.CO2e_total = 0
    s_elec.energy = entries.b_elec_fec
    s_elec.CO2e_combustion_based = 0
    s_elec.CO2e_combustion_based_per_MWh = 0
    s_elec.CO2e_total = 0

    supply = energy_source.calc_supply(inputs)

    s.energy = (
        s_gas.energy
        + s_lpg.energy
        + s_petrol.energy
        + s_jetfuel.energy
        + s_diesel.energy
        + s_fueloil.energy
        + supply.biomass.energy
        + s_coal.energy
        + s_heatnet.energy
        + s_heatpump.energy
        + s_solarth.energy
        + s_elec.energy
    )
    s_elec.pct_energy = div(s_elec.energy, s.energy)
    s_solarth.pct_energy = div(s_solarth.energy, s.energy)
    s_heatpump.pct_energy = div(s_heatpump.energy, s.energy)
    s_elec_heating.pct_energy = div(s_elec_heating.energy, s_elec.energy)
    s_heatnet.pct_energy = div(s_heatnet.energy, s.energy)
    s_coal.pct_energy = div(s_coal.energy, s.energy)
    supply.biomass.pct_energy = div(supply.biomass.energy, s.energy)
    s_fueloil.pct_energy = div(s_fueloil.energy, s.energy)
    s_diesel.pct_energy = div(s_diesel.energy, s.energy)
    s_petrol.pct_energy = div(s_petrol.energy, s.energy)
    s_gas.pct_energy = div(s_gas.energy, s.energy)
    s_lpg.pct_energy = div(s_lpg.energy, s.energy)
    s_jetfuel.pct_energy = div(s_jetfuel.energy, s.energy)
    s.pct_energy = (
        s_gas.pct_energy
        + s_lpg.pct_energy
        + s_petrol.pct_energy
        + s_jetfuel.pct_energy
        + s_diesel.pct_energy
        + s_fueloil.pct_energy
        + supply.biomass.pct_energy
        + s_coal.pct_energy
        + s_heatnet.pct_energy
        + s_heatpump.pct_energy
        + s_solarth.pct_energy
        + s_elec.pct_energy
    )
    s.cost_fuel = (
        s_gas.cost_fuel
        + s_lpg.cost_fuel
        + s_petrol.cost_fuel
        + s_jetfuel.cost_fuel
        + s_diesel.cost_fuel
        + s_fueloil.cost_fuel
        + supply.biomass.cost_fuel
        + s_coal.cost_fuel
        + s_heatnet.cost_fuel
        + s_heatpump.cost_fuel
        + s_solarth.cost_fuel
    )
    s.CO2e_combustion_based = (
        s_gas.CO2e_combustion_based
        + s_lpg.CO2e_combustion_based
        + s_petrol.CO2e_combustion_based
        + s_jetfuel.CO2e_combustion_based
        + s_diesel.CO2e_combustion_based
        + s_fueloil.CO2e_combustion_based
        + supply.biomass.CO2e_combustion_based
        + s_coal.CO2e_combustion_based
    )
    s.CO2e_total = s.CO2e_combustion_based

    production = energy_demand.calc_production(
        inputs,
        s_heatpump.energy,
        s_elec.energy,
        s_elec_heating.energy,
        s_petrol.energy,
        s_jetfuel.energy,
        s_diesel.energy,
        s_gas.energy,
        s_lpg.energy,
        s_fueloil.energy,
        supply.biomass.energy,
        s_coal.energy,
        s_heatnet.energy,
        s_solarth.energy,
    )

    supply.biomass.number_of_buildings = supply.biomass.energy * div(
        production.nonresi.number_of_buildings,
        production.nonresi.energy,
    )
    rp_p.CO2e_combustion_based = (
        r18.s.CO2e_combustion_based
        - r18.s_petrol.CO2e_combustion_based
        + s.CO2e_combustion_based
        - s_petrol.CO2e_combustion_based
        - s_jetfuel.CO2e_combustion_based
        - s_diesel.CO2e_combustion_based
    )
    rp_p.CO2e_total = r18.s.CO2e_combustion_based + s.CO2e_combustion_based
    rb.energy = r18.p.energy + production.total.energy
    b.CO2e_combustion_based = s.CO2e_combustion_based
    b.CO2e_total = s.CO2e_total
    b.CO2e_production_based = 0
    rb.CO2e_combustion_based = r18.r.CO2e_combustion_based + b.CO2e_combustion_based
    rb.CO2e_total = rb.CO2e_combustion_based

    return B18(
        b=b,
        p=production.total,
        p_nonresi=production.nonresi,
        p_nonresi_com=production.nonresi_commune,
        p_elec_elcon=production.elec_elcon,
        p_elec_heatpump=production.elec_heatpump,
        p_vehicles=production.vehicles,
        p_other=production.other,
        s=s,
        s_gas=s_gas,
        s_lpg=s_lpg,
        s_petrol=s_petrol,
        s_jetfuel=s_jetfuel,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_biomass=supply.biomass,
        s_coal=s_coal,
        s_heatnet=s_heatnet,
        s_elec_heating=s_elec_heating,
        s_heatpump=s_heatpump,
        s_solarth=s_solarth,
        s_elec=s_elec,
        rb=rb,
        rp_p=rp_p,
    )
