# pyright: strict

from dataclasses import dataclass

from ..energy_base import Energies

from ...inputs import Inputs
from ...common.energy_with_co2e import EnergyWithCO2e
from ...common.energy_with_co2e_per_mwh import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class EnergySupply:
    total: EnergyWithCO2e
    petrol: EnergyWithCO2ePerMWh
    diesel: EnergyWithCO2ePerMWh
    fueloil: EnergyWithCO2ePerMWh
    lpg: EnergyWithCO2ePerMWh
    gas: EnergyWithCO2ePerMWh
    biomass: EnergyWithCO2ePerMWh
    elec: EnergyWithCO2ePerMWh
    heatpump: EnergyWithCO2ePerMWh


def calc_supply(inputs: Inputs, energies: Energies) -> EnergySupply:
    fact = inputs.fact

    heatpump = EnergyWithCO2ePerMWh(
        energy=0,
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_heatpump_ratio_CO2e_to_fec"),
    )
    petrol = EnergyWithCO2ePerMWh(
        energy=energies.petrol.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_T_S_petrol_EmFa_tank_wheel_2018"),
    )
    diesel = EnergyWithCO2ePerMWh(
        energy=energies.diesel.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_T_S_diesel_EmFa_tank_wheel_2018"),
    )
    fueloil = EnergyWithCO2ePerMWh(
        energy=energies.fueloil.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_fueloil_cb_EF"),
    )
    lpg = EnergyWithCO2ePerMWh(
        energy=energies.lpg.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_T_S_lpg_EmFa_tank_wheel_2018"),
    )
    gas = EnergyWithCO2ePerMWh(
        energy=energies.gas.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_ngas_cb_EF"),
    )
    biomass = EnergyWithCO2ePerMWh(
        energy=energies.biomass.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_biomass_CO2e_EF"),
    )
    elec = EnergyWithCO2ePerMWh(
        energy=energies.elec.energy,
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_elec_ratio_CO2e_to_fec"),
    )
    total = EnergyWithCO2e.sum(petrol, diesel, fueloil, lpg, gas, biomass, elec)

    return EnergySupply(
        petrol=petrol,
        diesel=diesel,
        fueloil=fueloil,
        lpg=lpg,
        gas=gas,
        biomass=biomass,
        elec=elec,
        heatpump=heatpump,
        total=total,
    )
