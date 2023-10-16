# pyright: strict

from dataclasses import dataclass

from .dataclasses import Vars6, Vars7, Vars8, Vars9

from ...makeentries import Entries
from ...refdata import Facts
from ...utils import MILLION


@dataclass(kw_only=True)
class EnergySupply:
    s: Vars6
    s_fueloil: Vars7
    s_lpg: Vars7
    s_biomass: Vars8
    s_coal: Vars7
    s_petrol: Vars7
    s_heatnet: Vars7
    s_solarth: Vars7
    s_heatpump: Vars7
    s_elec_heating: Vars7
    s_gas: Vars7
    s_elec: Vars9


def calc_supply(entries: Entries, facts: Facts) -> EnergySupply:

    fact = facts.fact

    # Definitions
    s = Vars6()
    s_fueloil = Vars7()
    s_lpg = Vars7()
    s_biomass = Vars8()
    s_coal = Vars7()
    s_petrol = Vars7()
    s_heatnet = Vars7()
    s_solarth = Vars7()
    s_heatpump = Vars7()
    s_elec_heating = Vars7()
    s_gas = Vars7()
    s_elec = Vars9()

    # Energy
    s_fueloil.energy = entries.r_fueloil_fec
    s_lpg.energy = entries.r_lpg_fec
    s_biomass.energy = entries.r_biomass_fec
    s_coal.energy = entries.r_coal_fec
    s_petrol.energy = entries.r_petrol_fec
    s_heatnet.energy = entries.r_heatnet_fec
    s_solarth.energy = entries.r_orenew_fec * fact(
        "Fact_R_S_ratio_solarth_to_orenew_2018"
    )
    s_heatpump.energy = entries.r_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    s_gas.energy = entries.r_gas_fec
    s_elec.energy = entries.r_elec_fec
    s_elec_heating.energy = (
        fact("Fact_R_S_elec_heating_fec_2018")
        * entries.r_flats_wo_heatnet
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )
    s.energy = (
        s_fueloil.energy
        + s_lpg.energy
        + s_biomass.energy
        + s_coal.energy
        + s_petrol.energy
        + s_heatnet.energy
        + s_solarth.energy
        + s_heatpump.energy
        + s_gas.energy
        + s_elec.energy
    )
    # CO2e_cb_per_MWh
    s_lpg.CO2e_combustion_based_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    s_fueloil.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    s_biomass.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    s_coal.CO2e_combustion_based_per_MWh = fact("Fact_R_S_coal_CO2e_EF")
    s_petrol.CO2e_combustion_based_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    s_heatnet.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_heatnet_ratio_CO2e_to_fec"
    )
    s_solarth.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_solarth_ratio_CO2e_to_fec"
    )
    s_heatpump.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_heatpump_ratio_CO2e_to_fec"
    )
    s_gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    s_elec.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_elec_ratio_CO2e_to_fec")
    s_elec_heating.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_elec_ratio_CO2e_to_fec"
    )

    # CO2e_cb
    s_fueloil.CO2e_combustion_based = (
        s_fueloil.energy * s_fueloil.CO2e_combustion_based_per_MWh
    )
    s_lpg.CO2e_combustion_based = s_lpg.energy * s_lpg.CO2e_combustion_based_per_MWh
    s_biomass.CO2e_combustion_based = (
        s_biomass.energy * s_biomass.CO2e_combustion_based_per_MWh
    )
    s_coal.CO2e_combustion_based = s_coal.energy * s_coal.CO2e_combustion_based_per_MWh
    s_petrol.CO2e_combustion_based = (
        s_petrol.energy * s_petrol.CO2e_combustion_based_per_MWh
    )
    s_heatnet.CO2e_combustion_based = (
        s_heatnet.energy * s_heatnet.CO2e_combustion_based_per_MWh
    )
    s_solarth.CO2e_combustion_based = (
        s_solarth.energy * s_solarth.CO2e_combustion_based_per_MWh
    )
    s_heatpump.CO2e_combustion_based = (
        s_heatpump.energy * s_heatpump.CO2e_combustion_based_per_MWh
    )
    s_gas.CO2e_combustion_based = s_gas.energy * s_gas.CO2e_combustion_based_per_MWh
    s.CO2e_combustion_based = (
        s_fueloil.CO2e_combustion_based
        + s_lpg.CO2e_combustion_based
        + s_biomass.CO2e_combustion_based
        + s_coal.CO2e_combustion_based
        + s_petrol.CO2e_combustion_based
        + s_gas.CO2e_combustion_based
    )

    s_elec.CO2e_combustion_based = s_elec.energy * s_elec.CO2e_combustion_based_per_MWh
    s_elec_heating.CO2e_combustion_based = (
        s_elec_heating.energy * s_elec_heating.CO2e_combustion_based_per_MWh
    )
    s.CO2e_total = s.CO2e_combustion_based
    s_fueloil.CO2e_total = s_fueloil.CO2e_combustion_based
    s_lpg.CO2e_total = s_lpg.CO2e_combustion_based
    s_biomass.CO2e_total = s_biomass.CO2e_combustion_based
    s_coal.CO2e_total = s_coal.CO2e_combustion_based
    s_petrol.CO2e_total = s_petrol.CO2e_combustion_based
    s_heatnet.CO2e_total = s_heatnet.CO2e_combustion_based
    s_solarth.CO2e_total = s_solarth.CO2e_combustion_based
    s_heatpump.CO2e_total = s_heatpump.CO2e_combustion_based
    s_gas.CO2e_total = s_gas.CO2e_combustion_based
    s_elec.CO2e_total = s_elec.CO2e_combustion_based
    s_elec_heating.CO2e_total = s_elec_heating.CO2e_combustion_based

    # cost_fuel_per_MW
    s_fueloil.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    s_lpg.cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    s_biomass.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    s_coal.cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    s_petrol.cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    s_heatnet.cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    s_solarth.cost_fuel_per_MWh = 0
    s_heatpump.cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )
    s_elec_heating.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    s_gas.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")

    # cost_fuel
    s_fueloil.cost_fuel = s_fueloil.energy * s_fueloil.cost_fuel_per_MWh / MILLION
    s_lpg.cost_fuel = s_lpg.energy * s_lpg.cost_fuel_per_MWh / MILLION
    s_biomass.cost_fuel = s_biomass.energy * s_biomass.cost_fuel_per_MWh / MILLION
    s_coal.cost_fuel = s_coal.energy * s_coal.cost_fuel_per_MWh / MILLION
    s_petrol.cost_fuel = s_petrol.energy * s_petrol.cost_fuel_per_MWh / MILLION
    s_heatnet.cost_fuel = s_heatnet.energy * s_heatnet.cost_fuel_per_MWh / MILLION
    s_solarth.cost_fuel = s_solarth.energy * s_solarth.cost_fuel_per_MWh / MILLION
    s_heatpump.cost_fuel = s_heatpump.energy * s_heatpump.cost_fuel_per_MWh / MILLION
    s_elec_heating.cost_fuel = (
        s_elec_heating.energy * s_elec_heating.cost_fuel_per_MWh / MILLION
    )
    s_gas.cost_fuel = s_gas.energy * s_gas.cost_fuel_per_MWh / MILLION

    s.cost_fuel = (
        s_fueloil.cost_fuel
        + s_lpg.cost_fuel
        + s_biomass.cost_fuel
        + s_coal.cost_fuel
        + s_petrol.cost_fuel
        + s_heatnet.cost_fuel
        + s_solarth.cost_fuel
        + s_heatpump.cost_fuel
        + s_gas.cost_fuel
    )

    return EnergySupply(
        s=s,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_biomass=s_biomass,
        s_coal=s_coal,
        s_petrol=s_petrol,
        s_heatnet=s_heatnet,
        s_solarth=s_solarth,
        s_heatpump=s_heatpump,
        s_elec_heating=s_elec_heating,
        s_gas=s_gas,
        s_elec=s_elec,
    )
