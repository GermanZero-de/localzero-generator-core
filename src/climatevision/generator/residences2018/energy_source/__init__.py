# pyright: strict

from dataclasses import dataclass

from .dataclasses import Vars6, Vars7, Vars8, Vars9

from ...makeentries import Entries
from ...refdata import Facts
from ...utils import MILLION


@dataclass(kw_only=True)
class EnergySupply:
    total: Vars6
    fueloil: Vars7
    lpg: Vars7
    biomass: Vars8
    coal: Vars7
    petrol: Vars7
    heatnet: Vars7
    solarth: Vars7
    heatpump: Vars7
    elec_heating: Vars7
    gas: Vars7
    elec: Vars9


def calc_supply(entries: Entries, facts: Facts) -> EnergySupply:

    fact = facts.fact

    # Definitions
    total = Vars6()
    fueloil = Vars7()
    lpg = Vars7()
    biomass = Vars8()
    coal = Vars7()
    petrol = Vars7()
    heatnet = Vars7()
    solarth = Vars7()
    heatpump = Vars7()
    elec_heating = Vars7()
    gas = Vars7()
    elec = Vars9()

    # Energy
    fueloil.energy = entries.r_fueloil_fec
    lpg.energy = entries.r_lpg_fec
    biomass.energy = entries.r_biomass_fec
    coal.energy = entries.r_coal_fec
    petrol.energy = entries.r_petrol_fec
    heatnet.energy = entries.r_heatnet_fec
    solarth.energy = entries.r_orenew_fec * fact(
        "Fact_R_S_ratio_solarth_to_orenew_2018"
    )
    heatpump.energy = entries.r_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    gas.energy = entries.r_gas_fec
    elec.energy = entries.r_elec_fec
    elec_heating.energy = (
        fact("Fact_R_S_elec_heating_fec_2018")
        * entries.r_flats_wo_heatnet
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    total.energy = (
        fueloil.energy
        + lpg.energy
        + biomass.energy
        + coal.energy
        + petrol.energy
        + heatnet.energy
        + solarth.energy
        + heatpump.energy
        + gas.energy
        + elec.energy
    )
    # CO2e_cb_per_MWh
    lpg.CO2e_combustion_based_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    fueloil.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    biomass.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    coal.CO2e_combustion_based_per_MWh = fact("Fact_R_S_coal_CO2e_EF")
    petrol.CO2e_combustion_based_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    heatnet.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_heatnet_ratio_CO2e_to_fec")
    solarth.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_solarth_ratio_CO2e_to_fec")
    heatpump.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_heatpump_ratio_CO2e_to_fec"
    )
    gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    elec.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_elec_ratio_CO2e_to_fec")
    elec_heating.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_elec_ratio_CO2e_to_fec"
    )

    # CO2e_cb
    fueloil.CO2e_combustion_based = (
        fueloil.energy * fueloil.CO2e_combustion_based_per_MWh
    )
    lpg.CO2e_combustion_based = lpg.energy * lpg.CO2e_combustion_based_per_MWh
    biomass.CO2e_combustion_based = (
        biomass.energy * biomass.CO2e_combustion_based_per_MWh
    )
    coal.CO2e_combustion_based = coal.energy * coal.CO2e_combustion_based_per_MWh
    petrol.CO2e_combustion_based = petrol.energy * petrol.CO2e_combustion_based_per_MWh
    heatnet.CO2e_combustion_based = (
        heatnet.energy * heatnet.CO2e_combustion_based_per_MWh
    )
    solarth.CO2e_combustion_based = (
        solarth.energy * solarth.CO2e_combustion_based_per_MWh
    )
    heatpump.CO2e_combustion_based = (
        heatpump.energy * heatpump.CO2e_combustion_based_per_MWh
    )
    gas.CO2e_combustion_based = gas.energy * gas.CO2e_combustion_based_per_MWh
    total.CO2e_combustion_based = (
        fueloil.CO2e_combustion_based
        + lpg.CO2e_combustion_based
        + biomass.CO2e_combustion_based
        + coal.CO2e_combustion_based
        + petrol.CO2e_combustion_based
        + gas.CO2e_combustion_based
    )

    elec.CO2e_combustion_based = elec.energy * elec.CO2e_combustion_based_per_MWh
    elec_heating.CO2e_combustion_based = (
        elec_heating.energy * elec_heating.CO2e_combustion_based_per_MWh
    )
    total.CO2e_total = total.CO2e_combustion_based
    fueloil.CO2e_total = fueloil.CO2e_combustion_based
    lpg.CO2e_total = lpg.CO2e_combustion_based
    biomass.CO2e_total = biomass.CO2e_combustion_based
    coal.CO2e_total = coal.CO2e_combustion_based
    petrol.CO2e_total = petrol.CO2e_combustion_based
    heatnet.CO2e_total = heatnet.CO2e_combustion_based
    solarth.CO2e_total = solarth.CO2e_combustion_based
    heatpump.CO2e_total = heatpump.CO2e_combustion_based
    gas.CO2e_total = gas.CO2e_combustion_based
    elec.CO2e_total = elec.CO2e_combustion_based
    elec_heating.CO2e_total = elec_heating.CO2e_combustion_based

    # cost_fuel_per_MW
    fueloil.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    lpg.cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    biomass.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    coal.cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    petrol.cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    heatnet.cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    solarth.cost_fuel_per_MWh = 0
    heatpump.cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )
    elec_heating.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    gas.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")

    # cost_fuel
    fueloil.cost_fuel = fueloil.energy * fueloil.cost_fuel_per_MWh / MILLION
    lpg.cost_fuel = lpg.energy * lpg.cost_fuel_per_MWh / MILLION
    biomass.cost_fuel = biomass.energy * biomass.cost_fuel_per_MWh / MILLION
    coal.cost_fuel = coal.energy * coal.cost_fuel_per_MWh / MILLION
    petrol.cost_fuel = petrol.energy * petrol.cost_fuel_per_MWh / MILLION
    heatnet.cost_fuel = heatnet.energy * heatnet.cost_fuel_per_MWh / MILLION
    solarth.cost_fuel = solarth.energy * solarth.cost_fuel_per_MWh / MILLION
    heatpump.cost_fuel = heatpump.energy * heatpump.cost_fuel_per_MWh / MILLION
    elec_heating.cost_fuel = (
        elec_heating.energy * elec_heating.cost_fuel_per_MWh / MILLION
    )
    gas.cost_fuel = gas.energy * gas.cost_fuel_per_MWh / MILLION

    total.cost_fuel = (
        fueloil.cost_fuel
        + lpg.cost_fuel
        + biomass.cost_fuel
        + coal.cost_fuel
        + petrol.cost_fuel
        + heatnet.cost_fuel
        + solarth.cost_fuel
        + heatpump.cost_fuel
        + gas.cost_fuel
    )

    return EnergySupply(
        total=total,
        fueloil=fueloil,
        lpg=lpg,
        biomass=biomass,
        coal=coal,
        petrol=petrol,
        heatnet=heatnet,
        solarth=solarth,
        heatpump=heatpump,
        elec_heating=elec_heating,
        gas=gas,
        elec=elec,
    )
