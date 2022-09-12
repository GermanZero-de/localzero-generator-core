# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .co2eFromEnergyUse import CO2eFromEnergyUse
from .co2eFromEnergyUseDetail import CO2eFromEnergyUseDetail


@dataclass(kw_only=True)
class EnergySupply:
    s: CO2eFromEnergyUse
    s_petrol: CO2eFromEnergyUseDetail
    s_diesel: CO2eFromEnergyUseDetail
    s_fueloil: CO2eFromEnergyUseDetail
    s_lpg: CO2eFromEnergyUseDetail
    s_gas: CO2eFromEnergyUseDetail
    s_biomass: CO2eFromEnergyUseDetail
    s_elec: CO2eFromEnergyUseDetail
    s_heatpump: CO2eFromEnergyUseDetail


def calc_supply(inputs: Inputs, total_energy: float) -> EnergySupply:

    entries = inputs.entries

    s_heatpump = CO2eFromEnergyUseDetail.calc(
        energy=0,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact(
            "Fact_RB_S_heatpump_ratio_CO2e_to_fec"
        ),
    )
    s_petrol = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_petrol_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact(
            "Fact_T_S_petrol_EmFa_tank_wheel_2018"
        ),
    )
    s_diesel = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_diesel_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact(
            "Fact_T_S_diesel_EmFa_tank_wheel_2018"
        ),
    )
    s_fueloil = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_fueloil_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_H_P_fueloil_cb_EF"),
    )
    s_lpg = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_lpg_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_T_S_lpg_EmFa_tank_wheel_2018"),
    )
    s_gas = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_gas_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_H_P_ngas_cb_EF"),
    )
    s_biomass = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_biomass_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_RB_S_biomass_CO2e_EF"),
    )
    s_elec = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_elec_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=inputs.fact("Fact_RB_S_elec_ratio_CO2e_to_fec"),
    )
    s = CO2eFromEnergyUse.sum(
        s_petrol, s_diesel, s_fueloil, s_lpg, s_gas, s_biomass, s_elec
    )

    return EnergySupply(
        s_petrol=s_petrol,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biomass=s_biomass,
        s_elec=s_elec,
        s_heatpump=s_heatpump,
        s=s,
    )
