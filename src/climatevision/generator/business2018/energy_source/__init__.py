# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import MILLION

from ..dataclasses import Vars6, Vars7, Vars8


@dataclass(kw_only=True)
class EnergySupply:
    # total: Vars5
    gas: Vars6
    lpg: Vars6
    petrol: Vars6
    jetfuel: Vars6
    diesel: Vars6
    fueloil: Vars6
    biomass: Vars7
    coal: Vars6
    heatnet: Vars6
    elec_heating: Vars8
    heatpump: Vars6
    solarth: Vars6
    elec: Vars8


def calc_supply(
    inputs: Inputs,
    total_energy: float,
    gas_energy: float,
    lpg_energy: float,
    petrol_energy: float,
    jetfuel_energy: float,
    diesel_energy: float,
    fueloil_energy: float,
    biomass_energy: float,
    coal_energy: float,
    heatnet_energy: float,
    elec_heating_energy: float,
    heatpump_energy: float,
    solarth_energy: float,
    elec_energy: float,
) -> EnergySupply:

    fact = inputs.fact

    gas = Vars6(energy=gas_energy, total_energy=total_energy)
    gas.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")
    gas.cost_fuel = gas.energy * gas.cost_fuel_per_MWh / MILLION
    gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    gas.CO2e_combustion_based = gas.energy * gas.CO2e_combustion_based_per_MWh
    gas.CO2e_total = gas.CO2e_combustion_based

    lpg = Vars6(energy=lpg_energy, total_energy=total_energy)
    lpg.cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    lpg.cost_fuel = lpg.energy * lpg.cost_fuel_per_MWh / MILLION
    lpg.CO2e_combustion_based_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    lpg.CO2e_combustion_based = lpg.energy * lpg.CO2e_combustion_based_per_MWh
    lpg.CO2e_total = lpg.CO2e_combustion_based

    petrol = Vars6(energy=petrol_energy, total_energy=total_energy)
    petrol.cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    petrol.cost_fuel = petrol.energy * petrol.cost_fuel_per_MWh / MILLION
    petrol.CO2e_combustion_based_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    petrol.CO2e_combustion_based = petrol.energy * petrol.CO2e_combustion_based_per_MWh
    petrol.CO2e_total = petrol.CO2e_combustion_based

    jetfuel = Vars6(energy=jetfuel_energy, total_energy=total_energy)
    jetfuel.cost_fuel_per_MWh = fact("Fact_R_S_kerosine_energy_cost_factor_2018")
    jetfuel.cost_fuel = jetfuel.energy * jetfuel.cost_fuel_per_MWh / MILLION
    jetfuel.CO2e_combustion_based_per_MWh = fact("Fact_H_P_kerosene_cb_EF")
    jetfuel.CO2e_combustion_based = (
        jetfuel.energy * jetfuel.CO2e_combustion_based_per_MWh
    )
    jetfuel.CO2e_total = jetfuel.CO2e_combustion_based

    diesel = Vars6(energy=diesel_energy, total_energy=total_energy)
    diesel.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    diesel.cost_fuel = diesel.energy * diesel.cost_fuel_per_MWh / MILLION
    diesel.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    diesel.CO2e_combustion_based = diesel.energy * diesel.CO2e_combustion_based_per_MWh
    diesel.CO2e_total = diesel.CO2e_combustion_based

    fueloil = Vars6(energy=fueloil_energy, total_energy=total_energy)
    fueloil.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    fueloil.cost_fuel = fueloil.energy * fueloil.cost_fuel_per_MWh / MILLION
    fueloil.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    fueloil.CO2e_combustion_based = (
        fueloil.energy * fueloil.CO2e_combustion_based_per_MWh
    )
    fueloil.CO2e_total = fueloil.CO2e_combustion_based

    coal = Vars6(energy=coal_energy, total_energy=total_energy)
    coal.cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    coal.cost_fuel = coal.energy * coal.cost_fuel_per_MWh / MILLION
    coal.CO2e_combustion_based_per_MWh = fact("Fact_R_S_coal_CO2e_EF")
    coal.CO2e_combustion_based = coal.energy * coal.CO2e_combustion_based_per_MWh
    coal.CO2e_total = coal.CO2e_combustion_based

    heatnet = Vars6(energy=heatnet_energy, total_energy=total_energy)
    heatnet.cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    heatnet.cost_fuel = heatnet.energy * heatnet.cost_fuel_per_MWh / MILLION
    heatnet.CO2e_combustion_based = 0
    heatnet.CO2e_combustion_based_per_MWh = 0
    heatnet.CO2e_total = 0

    elec_heating = Vars8(energy=elec_heating_energy, total_energy=elec_energy)
    elec_heating.CO2e_combustion_based = 0
    elec_heating.CO2e_combustion_based_per_MWh = 0
    elec_heating.CO2e_total = 0

    heatpump = Vars6(energy=heatpump_energy, total_energy=total_energy)
    heatpump.cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )
    heatpump.cost_fuel = heatpump.energy * heatpump.cost_fuel_per_MWh / MILLION
    heatpump.CO2e_combustion_based = 0
    heatpump.CO2e_combustion_based_per_MWh = 0
    heatpump.CO2e_total = 0

    solarth = Vars6(energy=solarth_energy, total_energy=total_energy)
    solarth.cost_fuel_per_MWh = 0
    solarth.cost_fuel = 0
    solarth.CO2e_combustion_based = 0
    solarth.CO2e_combustion_based_per_MWh = 0
    solarth.CO2e_total = 0

    elec = Vars8(energy=elec_energy, total_energy=total_energy)
    elec.CO2e_combustion_based = 0
    elec.CO2e_combustion_based_per_MWh = 0
    elec.CO2e_total = 0

    biomass = Vars7(energy=biomass_energy, total_energy=total_energy)
    biomass.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    biomass.cost_fuel = biomass.energy * biomass.cost_fuel_per_MWh / MILLION
    biomass.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    biomass.CO2e_combustion_based = (
        biomass.energy * biomass.CO2e_combustion_based_per_MWh
    )
    biomass.CO2e_total = biomass.CO2e_combustion_based

    return EnergySupply(
        # total=total,
        gas=gas,
        lpg=lpg,
        petrol=petrol,
        jetfuel=jetfuel,
        diesel=diesel,
        fueloil=fueloil,
        biomass=biomass,
        coal=coal,
        heatnet=heatnet,
        elec_heating=elec_heating,
        heatpump=heatpump,
        solarth=solarth,
        elec=elec,
    )
