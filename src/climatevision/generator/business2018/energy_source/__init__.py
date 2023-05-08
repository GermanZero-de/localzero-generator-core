# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .dataclasses import Vars5, Vars6, Vars7, EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class EnergySupply:
    total: Vars5
    gas: Vars6
    lpg: Vars6
    petrol: Vars6
    jetfuel: Vars6
    diesel: Vars6
    fueloil: Vars6
    biomass: Vars7
    coal: Vars6
    heatnet: Vars6
    elec_heating: EnergyWithCO2ePerMWh
    heatpump: Vars6
    solarth: Vars6
    elec: EnergyWithCO2ePerMWh


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

    gas = Vars6(
        energy=gas_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_gas_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_ngas_cb_EF"),
    )

    lpg = Vars6(
        energy=lpg_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_lpg_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_LPG_cb_EF"),
    )

    petrol = Vars6(
        energy=petrol_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_petrol_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_petrol_cb_EF"),
    )

    jetfuel = Vars6(
        energy=jetfuel_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_kerosine_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_kerosene_cb_EF"),
    )

    diesel = Vars6(
        energy=diesel_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_fueloil_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_fueloil_cb_EF"),
    )

    fueloil = Vars6(
        energy=fueloil_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_fueloil_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_fueloil_cb_EF"),
    )

    coal = Vars6(
        energy=coal_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_coal_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_R_S_coal_CO2e_EF"),
    )

    heatnet = Vars6(
        energy=heatnet_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_heatnet_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=0,
    )

    elec_heating = EnergyWithCO2ePerMWh(
        energy=elec_heating_energy,
        CO2e_combustion_based_per_MWh=0,
    )

    heatpump = Vars6(
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

    solarth = Vars6(
        energy=solarth_energy,
        cost_fuel_per_MWh=0,
        CO2e_combustion_based_per_MWh=0,
    )

    elec = EnergyWithCO2ePerMWh(energy=elec_energy, CO2e_combustion_based_per_MWh=0)

    biomass = Vars7(
        energy=biomass_energy,
        cost_fuel_per_MWh=fact("Fact_R_S_wood_energy_cost_factor_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_biomass_CO2e_EF"),
    )

    total = Vars5()
    total.energy = total_energy
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
