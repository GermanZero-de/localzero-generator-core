# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .co2e_from_energy_use import CO2eFromEnergyUse
from .co2e_from_energy_use_detail import CO2eFromEnergyUseDetail


@dataclass(kw_only=True)
class EnergySupply:
    total: CO2eFromEnergyUse
    petrol: CO2eFromEnergyUseDetail
    diesel: CO2eFromEnergyUseDetail
    fueloil: CO2eFromEnergyUseDetail
    lpg: CO2eFromEnergyUseDetail
    gas: CO2eFromEnergyUseDetail
    biomass: CO2eFromEnergyUseDetail
    elec: CO2eFromEnergyUseDetail
    heatpump: CO2eFromEnergyUseDetail


def calc_supply(inputs: Inputs, total_energy: float) -> EnergySupply:

    entries = inputs.entries

    heatpump = CO2eFromEnergyUseDetail.calc(
        energy=0,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact(
            "Fact_RB_S_heatpump_ratio_CO2e_to_fec"
        ),
    )
    petrol = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_petrol_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact(
            "Fact_T_S_petrol_EmFa_tank_wheel_2018"
        ),
    )
    diesel = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_diesel_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        ),
    )
    fueloil = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_fueloil_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_H_P_fueloil_cb_EF"),
    )
    lpg = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_lpg_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_T_S_lpg_EmFa_tank_wheel_2018"),
    )
    gas = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_gas_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_H_P_ngas_cb_EF"),
    )
    biomass = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_biomass_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_RB_S_biomass_CO2e_EF"),
    )
    elec = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_elec_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_RB_S_elec_ratio_CO2e_to_fec"),
    )
    total = CO2eFromEnergyUse.sum(petrol, diesel, fueloil, lpg, gas, biomass, elec)

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
