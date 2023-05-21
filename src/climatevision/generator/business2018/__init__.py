"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/hh_ghd.html
"""

# pyright: strict

from ..inputs import Inputs
from ..utils import div
from ..residences2018.r18 import R18
from ..common.co2_equivalent_emission import CO2eEmission
from ..common.energy_with_co2e import EnergyWithCO2e

from .b18 import B18
from . import energy_demand, energy_source


# Berechnungsfunktion im Sektor GHD für 2018
def calc(inputs: Inputs, *, r18: R18) -> B18:
    fact = inputs.fact
    entries = inputs.entries

    gas_energy = entries.b_gas_fec
    lpg_energy = entries.b_lpg_fec
    petrol_energy = entries.b_petrol_fec
    jetfuel_energy = entries.b_jetfuel_fec
    diesel_energy = entries.b_diesel_fec
    fueloil_energy = entries.b_fueloil_fec
    biomass_energy = entries.b_biomass_fec
    coal_energy = entries.b_coal_fec
    heatnet_energy = entries.b_heatnet_fec
    elec_heating_energy = (
        fact("Fact_B_S_elec_heating_fec_2018")
        * entries.r_flats_wo_heatnet
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    heatpump_energy = entries.b_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    solarth_energy = entries.b_orenew_fec * (
        1 - fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    )
    elec_energy = entries.b_elec_fec

    supply = energy_source.calc_supply(
        inputs,
        gas_energy,
        lpg_energy,
        petrol_energy,
        jetfuel_energy,
        diesel_energy,
        fueloil_energy,
        biomass_energy,
        coal_energy,
        heatnet_energy,
        elec_heating_energy,
        heatpump_energy,
        solarth_energy,
        elec_energy,
    )

    production = energy_demand.calc_production(
        inputs,
        heatpump_energy,
        elec_energy,
        elec_heating_energy,
        petrol_energy,
        jetfuel_energy,
        diesel_energy,
        gas_energy,
        lpg_energy,
        fueloil_energy,
        biomass_energy,
        coal_energy,
        heatnet_energy,
        solarth_energy,
    )

    supply.biomass.number_of_buildings = supply.biomass.energy * div(
        production.nonresi.number_of_buildings,
        production.nonresi.energy,
    )

    b = CO2eEmission(
        CO2e_combustion_based=supply.total.CO2e_combustion_based,
        CO2e_production_based=0,
    )

    rb = EnergyWithCO2e(
        energy=r18.p.energy + production.total.energy,
        CO2e_combustion_based=r18.r.CO2e_combustion_based + b.CO2e_combustion_based,
    )

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
    )
