# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...transport2018.t18 import T18
from ...electricity2018.e18 import E18

from .dataclasses import (
    HeatProduction,
    Vars6,
    Vars8FromEnergySum,
)


@dataclass(kw_only=True)
class Production:
    total: HeatProduction
    gas: HeatProduction
    lpg: HeatProduction
    fueloil: HeatProduction
    opetpro: HeatProduction
    coal: HeatProduction
    heatnet: Vars6
    heatnet_cogen: HeatProduction
    heatnet_plant: HeatProduction
    heatnet_geoth: HeatProduction
    heatnet_lheatpump: HeatProduction
    biomass: HeatProduction
    ofossil: HeatProduction
    orenew: Vars8FromEnergySum
    solarth: HeatProduction
    heatpump: HeatProduction


def calc_production(
    inputs: Inputs,
    t18: T18,
    e18: E18,
    demand_total_energy: float,
    p_heatnet_energy: float,
) -> Production:

    entries = inputs.entries
    fact = inputs.fact

    gas = HeatProduction.calc(
        energy=entries.r_gas_fec
        + entries.b_gas_fec
        + entries.i_gas_fec
        + entries.a_gas_fec
        + t18.t.demand_gas,
        total_energy=demand_total_energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
    )

    lpg = HeatProduction.calc(
        energy=entries.r_lpg_fec
        + entries.b_lpg_fec
        + entries.i_lpg_fec
        + entries.a_lpg_fec
        + t18.s_lpg.energy,
        total_energy=demand_total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018"),
    )

    fueloil = HeatProduction.calc(
        energy=entries.r_fueloil_fec
        + entries.b_fueloil_fec
        + entries.i_fueloil_fec
        + entries.a_fueloil_fec
        + t18.s_fueloil.energy,
        total_energy=demand_total_energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    opetpro = HeatProduction.calc(
        energy=entries.i_opetpro_fec,
        total_energy=demand_total_energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    coal = HeatProduction.calc(
        energy=entries.r_coal_fec + entries.b_coal_fec + entries.i_coal_fec,
        total_energy=demand_total_energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"),
    )

    if (
        e18.p_fossil_coal_brown_cogen.energy
        + e18.p_fossil_coal_black_cogen.energy
        + e18.p_fossil_gas_cogen.energy
        + e18.p_fossil_ofossil_cogen.energy
        + e18.p_renew_biomass_cogen.energy
        < p_heatnet_energy
    ):
        heatnet_cogen_energy = (
            e18.p_fossil_coal_brown_cogen.energy
            + e18.p_fossil_coal_black_cogen.energy
            + e18.p_fossil_gas_cogen.energy
            + e18.p_fossil_ofossil_cogen.energy
            + e18.p_renew_biomass_cogen.energy
        )
    else:
        heatnet_cogen_energy = p_heatnet_energy

    heatnet_cogen = HeatProduction.calc(
        energy=heatnet_cogen_energy,
        total_energy=p_heatnet_energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_heatnet_cogen_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    heatnet_plant = HeatProduction.calc(
        energy=p_heatnet_energy - heatnet_cogen.energy,
        total_energy=p_heatnet_energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    # TODO: Check, why heatnet_geoth is completely 0
    heatnet_geoth = HeatProduction.calc(energy=0, total_energy=p_heatnet_energy)
    # TODO: Check, why heatnet_lheatpump is completely 0
    heatnet_lheatpump = HeatProduction.calc(energy=0, total_energy=p_heatnet_energy)

    heatnet = Vars6(
        energy=p_heatnet_energy,
        total_energy=demand_total_energy,
        CO2e_combustion_based=heatnet_cogen.CO2e_combustion_based
        + heatnet_plant.CO2e_combustion_based,
    )

    biomass = HeatProduction.calc(
        energy=entries.r_biomass_fec
        + entries.b_biomass_fec
        + entries.i_biomass_fec
        + entries.a_biomass_fec,
        total_energy=demand_total_energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    ofossil = HeatProduction.calc(
        energy=entries.i_ofossil_fec,
        total_energy=demand_total_energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    orenew_energy = entries.r_orenew_fec + entries.b_orenew_fec + entries.i_orenew_fec

    solarth = HeatProduction.calcFromPct(
        pct_energy=fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        total_energy=orenew_energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
    )

    heatpump = HeatProduction.calcFromPct(
        pct_energy=fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        total_energy=orenew_energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
    )

    orenew = Vars8FromEnergySum(
        energy=orenew_energy,
        total_energy=demand_total_energy,
        CO2e_production_based_per_MWh=0,
        CO2e_production_based=solarth.CO2e_production_based
        + heatpump.CO2e_production_based,
    )

    total = HeatProduction.calcSum(
        demand_total_energy,
        gas,
        lpg,
        fueloil,
        opetpro,
        coal,
        heatnet,
        biomass,
        ofossil,
        orenew,
    )

    return Production(
        total=total,
        gas=gas,
        lpg=lpg,
        fueloil=fueloil,
        opetpro=opetpro,
        coal=coal,
        heatnet=heatnet,
        heatnet_cogen=heatnet_cogen,
        heatnet_plant=heatnet_plant,
        heatnet_geoth=heatnet_geoth,
        heatnet_lheatpump=heatnet_lheatpump,
        biomass=biomass,
        ofossil=ofossil,
        orenew=orenew,
        solarth=solarth,
        heatpump=heatpump,
    )
