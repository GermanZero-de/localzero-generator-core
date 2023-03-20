# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...heat2018.h18 import H18
from ...residences2030.r30 import R30
from ...business2030.b30 import B30
from ...agri2030.a30 import A30
from ...industry2030.i30 import I30
from ...electricity2030.electricity2030_core import EColVars2030

from .dataclasses import (
    TotalHeatProduction,
    HeatProductionWithCostFuel,
    HeatProduction,
    HeatnetProduction,
    HeatnetPlantProduction,
    HeatnetLheatpumpProduction,
    HeatnetGeothProduction,
)


@dataclass(kw_only=True)
class Production:
    total: TotalHeatProduction
    gas: HeatProductionWithCostFuel
    lpg: HeatProduction
    fueloil: HeatProductionWithCostFuel
    opetpro: HeatProduction
    coal: HeatProductionWithCostFuel
    heatnet: HeatnetProduction
    heatnet_cogen: HeatProduction
    heatnet_plant: HeatnetPlantProduction
    heatnet_lheatpump: HeatnetLheatpumpProduction
    heatnet_geoth: HeatnetGeothProduction
    biomass: HeatProductionWithCostFuel
    ofossil: HeatProduction
    orenew: HeatProduction
    solarth: HeatProduction
    heatpump: HeatProduction


def calc_production(
    inputs: Inputs,
    h18: H18,
    r30: R30,
    b30: B30,
    a30: A30,
    i30: I30,
    p_local_biomass_cogen: EColVars2030,
) -> Production:

    fact = inputs.fact
    ass = inputs.ass

    gas = HeatProductionWithCostFuel(
        inputs=inputs,
        what="gas",
        h18=h18,
        energy=r30.s_gas.energy + b30.s_gas.energy,
        CO2e_production_based_per_MWh=h18.p_gas.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_gas.CO2e_combustion_based_per_MWh,
    )
    coal = HeatProductionWithCostFuel(
        inputs=inputs,
        what="coal",
        h18=h18,
        energy=r30.s_coal.energy + b30.s_coal.energy,
        CO2e_production_based_per_MWh=h18.p_coal.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_coal.CO2e_combustion_based_per_MWh,
    )
    fueloil = HeatProductionWithCostFuel(
        inputs=inputs,
        what="fueloil",
        h18=h18,
        energy=r30.s_fueloil.energy + b30.s_fueloil.energy,
        CO2e_production_based_per_MWh=0,
        CO2e_combustion_based_per_MWh=h18.p_fueloil.CO2e_combustion_based_per_MWh,
    )

    biomass = HeatProductionWithCostFuel(
        inputs=inputs,
        what="biomass",
        h18=h18,
        energy=r30.s_biomass.energy
        + b30.s_biomass.energy
        + i30.s_renew_biomass.energy
        + a30.s_biomass.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=0,
    )

    lpg = HeatProduction(
        inputs=inputs,
        what="lpg",
        h18=h18,
        energy=r30.s_lpg.energy + b30.s_lpg.energy,
        CO2e_combustion_based_per_MWh=h18.p_lpg.CO2e_combustion_based_per_MWh,
        CO2e_production_based_per_MWh=0,
    )

    opetpro = HeatProduction(
        inputs=inputs,
        what="opetpro",
        h18=h18,
        energy=0,
        CO2e_production_based_per_MWh=h18.p_opetpro.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_opetpro.CO2e_combustion_based_per_MWh,
    )

    heatnet_energy = (
        r30.s_heatnet.energy + b30.s_heatnet.energy + i30.s_renew_heatnet.energy
    )

    heatnet_cogen_energy = (
        p_local_biomass_cogen.energy
        if (p_local_biomass_cogen.energy < heatnet_energy)
        else heatnet_energy
    )

    heatnet_cogen = HeatProduction(
        inputs=inputs,
        what="heatnet_cogen",
        h18=h18,
        energy=heatnet_cogen_energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_heatnet_biomass_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    heatnet_plant_pct_energy = ass("Ass_H_P_heatnet_fraction_solarth_2050")
    heatnet_plant = HeatnetPlantProduction(
        inputs=inputs,
        what="heatnet_plant",
        h18=h18,
        energy=(
            (heatnet_energy - heatnet_cogen_energy) * heatnet_plant_pct_energy
            if (heatnet_cogen_energy < heatnet_energy)
            else 0
        ),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
        pct_energy=heatnet_plant_pct_energy,
        invest_per_x=fact("Fact_H_P_heatnet_solarth_park_invest_203X"),
    )

    heatnet_lheatpump_pct_energy = ass("Ass_H_P_heatnet_fraction_lheatpump_2050")
    heatnet_lheatpump = HeatnetLheatpumpProduction(
        inputs=inputs,
        what="heatnet_lheatpump",
        h18=h18,
        energy=(
            (heatnet_energy - heatnet_cogen_energy) * heatnet_lheatpump_pct_energy
            if (heatnet_cogen_energy < heatnet_energy)
            else 0
        ),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
        pct_energy=heatnet_lheatpump_pct_energy,
        full_load_hour=fact("Fact_H_P_heatnet_lheatpump_full_load_hours"),
        invest_per_x=fact("Fact_H_P_heatnet_lheatpump_invest_203X"),
    )

    heatnet_geoth_pct_energy = ass("Ass_H_P_heatnet_fraction_geoth_2050")
    heatnet_geoth = HeatnetGeothProduction(
        inputs=inputs,
        what="heatnet_geoth",
        h18=h18,
        energy=(
            (heatnet_energy - heatnet_cogen_energy) * heatnet_geoth_pct_energy
            if (heatnet_cogen_energy < heatnet_energy)
            else 0
        ),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
        pct_energy=heatnet_geoth_pct_energy,
        full_load_hour=fact("Fact_H_P_heatnet_geoth_full_load_hours"),
        invest_per_x=fact("Fact_H_P_heatnet_geoth_invest_203X"),
    )

    heatnet = HeatnetProduction(
        inputs=inputs,
        what="heatnet",
        h18=h18,
        energy=heatnet_energy,
        CO2e_combustion_based=heatnet_cogen.CO2e_combustion_based,
        CO2e_production_based=(
            heatnet_cogen.CO2e_production_based
            + heatnet_plant.CO2e_production_based
            + heatnet_lheatpump.CO2e_production_based
            + heatnet_geoth.CO2e_production_based
        ),
        invest=heatnet_plant.invest + heatnet_lheatpump.invest + heatnet_geoth.invest,
    )

    ofossil = HeatProduction(
        inputs=inputs,
        what="ofossil",
        h18=h18,
        energy=0,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=0,
    )
    solarth = HeatProduction(
        inputs=inputs,
        what="solarth",
        h18=h18,
        energy=r30.s_solarth.energy + b30.s_solarth.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )
    heatpump = HeatProduction(
        inputs=inputs,
        what="heatpump",
        h18=h18,
        energy=r30.s_heatpump.energy + b30.s_heatpump.energy + a30.s_heatpump.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )
    orenew = HeatProduction(
        inputs=inputs,
        what="orenew",
        h18=h18,
        energy=solarth.energy + heatpump.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )

    total = TotalHeatProduction(
        inputs=inputs,
        what="",
        h18=h18,
        energy=(
            gas.energy
            + lpg.energy
            + fueloil.energy
            + opetpro.energy
            + coal.energy
            + heatnet.energy
            + biomass.energy
            + ofossil.energy
            + orenew.energy
        ),
        CO2e_combustion_based=(
            gas.CO2e_combustion_based
            + lpg.CO2e_combustion_based
            + fueloil.CO2e_combustion_based
            + opetpro.CO2e_combustion_based
            + coal.CO2e_combustion_based
            + heatnet.CO2e_combustion_based
        ),
        CO2e_production_based=(
            gas.CO2e_production_based
            + opetpro.CO2e_production_based
            + coal.CO2e_production_based
            + heatnet.CO2e_production_based
            + biomass.CO2e_production_based
            + ofossil.CO2e_production_based
            + orenew.CO2e_production_based
        ),
        invest=heatnet.invest,
        cost_fuel=(
            gas.cost_fuel + fueloil.cost_fuel + coal.cost_fuel + biomass.cost_fuel
        ),
        demand_electricity=heatnet_lheatpump.demand_electricity,
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
