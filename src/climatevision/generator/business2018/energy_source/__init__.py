# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .dataclasses import (
    Vars5,
    EnergyWithCO2ePerMWhAndCostFuel,
    EnergyWithCO2ePerMWhAndCostFuelAndBuildings,
    EnergyWithCO2ePerMWh,
)


@dataclass(kw_only=True)
class EnergySupply:
    total: Vars5
    gas: EnergyWithCO2ePerMWhAndCostFuel
    lpg: EnergyWithCO2ePerMWhAndCostFuel
    petrol: EnergyWithCO2ePerMWhAndCostFuel
    jetfuel: EnergyWithCO2ePerMWhAndCostFuel
    diesel: EnergyWithCO2ePerMWhAndCostFuel
    fueloil: EnergyWithCO2ePerMWhAndCostFuel
    biomass: EnergyWithCO2ePerMWhAndCostFuelAndBuildings
    coal: EnergyWithCO2ePerMWhAndCostFuel
    heatnet: EnergyWithCO2ePerMWhAndCostFuel
    elec_heating: EnergyWithCO2ePerMWh
    heatpump: EnergyWithCO2ePerMWhAndCostFuel
    solarth: EnergyWithCO2ePerMWhAndCostFuel
    elec: EnergyWithCO2ePerMWh


def calc_supply(
    inputs: Inputs,
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

    gas = EnergyWithCO2ePerMWhAndCostFuel(
        energy=gas_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_gas_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_ngas_cb_EF"),
    )

    lpg = EnergyWithCO2ePerMWhAndCostFuel(
        energy=lpg_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_lpg_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_LPG_cb_EF"),
    )

    petrol = EnergyWithCO2ePerMWhAndCostFuel(
        energy=petrol_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_petrol_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_petrol_cb_EF"),
    )

    jetfuel = EnergyWithCO2ePerMWhAndCostFuel(
        energy=jetfuel_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_kerosine_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_kerosene_cb_EF"),
    )

    diesel = EnergyWithCO2ePerMWhAndCostFuel(
        energy=diesel_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_fueloil_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_fueloil_cb_EF"),
    )

    fueloil = EnergyWithCO2ePerMWhAndCostFuel(
        energy=fueloil_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_fueloil_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_fueloil_cb_EF"),
    )

    coal = EnergyWithCO2ePerMWhAndCostFuel(
        energy=coal_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_coal_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_R_S_coal_CO2e_EF"),
    )

    heatnet = EnergyWithCO2ePerMWhAndCostFuel(
        energy=heatnet_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_heatnet_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=0,
    )

    elec_heating = EnergyWithCO2ePerMWh(
        energy=elec_heating_energy,
        CO2e_combustion_based_per_MWh=0,
    )

    heatpump = EnergyWithCO2ePerMWhAndCostFuel(
        energy=heatpump_energy,
        cost_fuel_per_MWh=(
            fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
            / (
                fact(
                    "Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018"
                )
                + fact(
                    "Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018"
                )
            )
            * 2
        ),
        CO2e_combustion_based_per_MWh=0,
    )

    solarth = EnergyWithCO2ePerMWhAndCostFuel(
        energy=solarth_energy,
        cost_fuel_per_MWh=0,
        CO2e_combustion_based_per_MWh=0,
    )

    elec = EnergyWithCO2ePerMWh(energy=elec_energy, CO2e_combustion_based_per_MWh=0)

    biomass = EnergyWithCO2ePerMWhAndCostFuelAndBuildings(
        energy=biomass_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_wood_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_biomass_CO2e_EF"),
    )

    total = Vars5()
    total.energy = (
        gas.energy
        + lpg.energy
        + petrol.energy
        + jetfuel.energy
        + diesel.energy
        + fueloil.energy
        + biomass.energy
        + coal.energy
        + heatnet.energy
        + heatpump.energy
        + solarth.energy
        + elec.energy
    )
    total.cost_fuel = (
        gas.cost_fuel
        + lpg.cost_fuel
        + petrol.cost_fuel
        + jetfuel.cost_fuel
        + diesel.cost_fuel
        + fueloil.cost_fuel
        + biomass.cost_fuel
        + coal.cost_fuel
        + heatnet.cost_fuel
        + heatpump.cost_fuel
        + solarth.cost_fuel
    )
    total.CO2e_combustion_based = (
        gas.CO2e_combustion_based
        + lpg.CO2e_combustion_based
        + petrol.CO2e_combustion_based
        + jetfuel.CO2e_combustion_based
        + diesel.CO2e_combustion_based
        + fueloil.CO2e_combustion_based
        + biomass.CO2e_combustion_based
        + coal.CO2e_combustion_based
    )
    total.CO2e_total = total.CO2e_combustion_based

    return EnergySupply(
        total=total,
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
