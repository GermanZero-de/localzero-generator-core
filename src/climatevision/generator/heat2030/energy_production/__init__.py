# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...heat2018.h18 import H18
from ...residences2030.r30 import R30
from ...business2030.b30 import B30
from ...agri2030.a30 import A30
from ...industry2030.i30 import I30

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
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    h18: H18,
    r30: R30,
    b30: B30,
    a30: A30,
    i30: I30,
    e30_p_local_biomass_cogen_energy: float,
) -> Production:

    fact = facts.fact
    ass = assumptions.ass

    gas = HeatProductionWithCostFuel(
        entries=entries,
        facts=facts,
        assumptions=assumptions,
        what="gas",
        h18=h18,
        energy=r30.s_gas.energy + b30.s_gas.energy,
        CO2e_production_based_per_MWh=h18.p_gas.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_gas.CO2e_combustion_based_per_MWh,
    )
    coal = HeatProductionWithCostFuel(
        entries=entries,
        facts=facts,
        assumptions=assumptions,
        what="coal",
        h18=h18,
        energy=r30.s_coal.energy + b30.s_coal.energy,
        CO2e_production_based_per_MWh=h18.p_coal.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_coal.CO2e_combustion_based_per_MWh,
    )
    fueloil = HeatProductionWithCostFuel(
        entries=entries,
        facts=facts,
        assumptions=assumptions,
        what="fueloil",
        h18=h18,
        energy=r30.s_fueloil.energy + b30.s_fueloil.energy,
        CO2e_production_based_per_MWh=0,
        CO2e_combustion_based_per_MWh=h18.p_fueloil.CO2e_combustion_based_per_MWh,
    )

    biomass = HeatProductionWithCostFuel(
        entries=entries,
        facts=facts,
        assumptions=assumptions,
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
        entries=entries,
        facts=facts,
        what="lpg",
        h18=h18,
        energy=r30.s_lpg.energy + b30.s_lpg.energy,
        CO2e_combustion_based_per_MWh=h18.p_lpg.CO2e_combustion_based_per_MWh,
        CO2e_production_based_per_MWh=0,
    )

    opetpro = HeatProduction(
        entries=entries,
        facts=facts,
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
        e30_p_local_biomass_cogen_energy
        if (e30_p_local_biomass_cogen_energy < heatnet_energy)
        else heatnet_energy
    )

    heatnet_cogen = HeatProduction(
        entries=entries,
        facts=facts,
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

    heatnet_orenew_energy = heatnet_energy - heatnet_cogen_energy

    heatnet_plant = HeatnetPlantProduction(
        entries=entries,
        facts=facts,
        what="heatnet_plant",
        h18=h18,
        energy=heatnet_orenew_energy * ass("Ass_H_P_heatnet_fraction_solarth_2050"),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
        invest_per_x=fact("Fact_H_P_heatnet_solarth_park_invest_203X"),
    )

    heatnet_lheatpump = HeatnetLheatpumpProduction(
        entries=entries,
        facts=facts,
        what="heatnet_lheatpump",
        h18=h18,
        energy=heatnet_orenew_energy * ass("Ass_H_P_heatnet_fraction_lheatpump_2050"),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
        full_load_hour=fact("Fact_H_P_heatnet_lheatpump_full_load_hours"),
        invest_per_x=fact("Fact_H_P_heatnet_lheatpump_invest_203X"),
    )

    heatnet_geoth = HeatnetGeothProduction(
        entries=entries,
        facts=facts,
        what="heatnet_geoth",
        h18=h18,
        energy=heatnet_orenew_energy * ass("Ass_H_P_heatnet_fraction_geoth_2050"),
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
        full_load_hour=fact("Fact_H_P_heatnet_geoth_full_load_hours"),
        invest_per_x=fact("Fact_H_P_heatnet_geoth_invest_203X"),
    )

    heatnet = HeatnetProduction(
        entries=entries,
        facts=facts,
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
        entries=entries,
        facts=facts,
        what="ofossil",
        h18=h18,
        energy=0,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=0,
    )
    solarth = HeatProduction(
        entries=entries,
        facts=facts,
        what="solarth",
        h18=h18,
        energy=r30.s_solarth.energy + b30.s_solarth.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )
    heatpump = HeatProduction(
        entries=entries,
        facts=facts,
        what="heatpump",
        h18=h18,
        energy=r30.s_heatpump.energy + b30.s_heatpump.energy + a30.s_heatpump.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )
    orenew = HeatProduction(
        entries=entries,
        facts=facts,
        what="orenew",
        h18=h18,
        energy=solarth.energy + heatpump.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )

    total = TotalHeatProduction(
        entries=entries,
        facts=facts,
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
