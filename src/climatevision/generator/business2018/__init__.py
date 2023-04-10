"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/hh_ghd.html
"""

# pyright: strict

from ..inputs import Inputs
from ..utils import div
from ..residences2018.r18 import R18
from ..common.co2_equivalent_emission import CO2eEmission

from .b18 import B18
from .dataclasses import Vars9, Vars10
from . import energy_demand, energy_source


# Berechnungsfunktion im Sektor GHD für 2018
def calc(inputs: Inputs, *, r18: R18) -> B18:
    fact = inputs.fact
    entries = inputs.entries

    supply_gas_energy = entries.b_gas_fec
    supply_lpg_energy = entries.b_lpg_fec
    supply_petrol_energy = entries.b_petrol_fec
    supply_jetfuel_energy = entries.b_jetfuel_fec
    supply_diesel_energy = entries.b_diesel_fec
    supply_fueloil_energy = entries.b_fueloil_fec
    supply_biomass_energy = entries.b_biomass_fec
    supply_coal_energy = entries.b_coal_fec
    supply_heatnet_energy = entries.b_heatnet_fec
    supply_elec_heating_energy = (
        fact("Fact_B_S_elec_heating_fec_2018")
        * entries.r_flats_wo_heatnet
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    supply_heatpump_energy = entries.b_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    supply_solarth_energy = entries.b_orenew_fec * (
        1 - fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    )
    supply_elec_energy = entries.b_elec_fec

    supply_total_energy = (
        supply_gas_energy
        + supply_lpg_energy
        + supply_petrol_energy
        + supply_jetfuel_energy
        + supply_diesel_energy
        + supply_fueloil_energy
        + supply_biomass_energy
        + supply_coal_energy
        + supply_heatnet_energy
        + supply_heatpump_energy
        + supply_solarth_energy
        + supply_elec_energy
    )

    supply = energy_source.calc_supply(
        inputs,
        supply_total_energy,
        supply_gas_energy,
        supply_lpg_energy,
        supply_petrol_energy,
        supply_jetfuel_energy,
        supply_diesel_energy,
        supply_fueloil_energy,
        supply_biomass_energy,
        supply_coal_energy,
        supply_heatnet_energy,
        supply_elec_heating_energy,
        supply_heatpump_energy,
        supply_solarth_energy,
        supply_elec_energy,
    )

    production = energy_demand.calc_production(
        inputs,
        supply.heatpump.energy,
        supply.elec.energy,
        supply.elec_heating.energy,
        supply.petrol.energy,
        supply.jetfuel.energy,
        supply.diesel.energy,
        supply.gas.energy,
        supply.lpg.energy,
        supply.fueloil.energy,
        supply.biomass.energy,
        supply.coal.energy,
        supply.heatnet.energy,
        supply.solarth.energy,
    )

    supply.biomass.number_of_buildings = supply.biomass.energy * div(
        production.nonresi.number_of_buildings,
        production.nonresi.energy,
    )

    b = CO2eEmission()
    b.CO2e_combustion_based = supply.total.CO2e_combustion_based
    b.CO2e_total = supply.total.CO2e_total
    b.CO2e_production_based = 0

    rp_p = Vars10()
    rp_p.CO2e_combustion_based = (
        r18.s.CO2e_combustion_based
        - r18.s_petrol.CO2e_combustion_based
        + supply.total.CO2e_combustion_based
        - supply.petrol.CO2e_combustion_based
        - supply.jetfuel.CO2e_combustion_based
        - supply.diesel.CO2e_combustion_based
    )
    rp_p.CO2e_total = r18.s.CO2e_combustion_based + supply.total.CO2e_combustion_based

    rb = Vars9()
    rb.energy = r18.p.energy + production.total.energy
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
        s=supply.total,
        s_gas=supply.gas,
        s_lpg=supply.lpg,
        s_petrol=supply.petrol,
        s_jetfuel=supply.jetfuel,
        s_diesel=supply.diesel,
        s_fueloil=supply.fueloil,
        s_biomass=supply.biomass,
        s_coal=supply.coal,
        s_heatnet=supply.heatnet,
        s_elec_heating=supply.elec_heating,
        s_heatpump=supply.heatpump,
        s_solarth=supply.solarth,
        s_elec=supply.elec,
        rb=rb,
        rp_p=rp_p,
    )
