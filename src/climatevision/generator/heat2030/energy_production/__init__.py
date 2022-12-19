# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...heat2018.h18 import H18
from ...residences2030.r30 import R30
from ...business2030.b30 import B30
from ...agri2030.a30 import A30
from ...industry2030.i30 import I30

from ..dataclasses import (
    # Vars5,
    Vars6,
    Vars9,
    # Vars10,
    # Vars11,
    # Vars12,
    # Vars13,
)


@dataclass(kw_only=True)
class Production:
    # total: Vars5
    gas: Vars6
    lpg: Vars9
    fueloil: Vars6
    opetpro: Vars9
    coal: Vars6
    # heatnet: Vars10
    heatnet_cogen: Vars9
    # heatnet_plant: Vars11
    # heatnet_lheatpump: Vars12
    # heatnet_geoth: Vars13
    biomass: Vars6
    ofossil: Vars9
    orenew: Vars9
    solarth: Vars9
    heatpump: Vars9


def calc_production(
    inputs: Inputs,
    h18: H18,
    r30: R30,
    b30: B30,
    a30: A30,
    i30: I30,
    p_local_biomass_cogen_energy: float,
    p_heatnet_energy: float,
) -> Production:

    fact = inputs.fact

    gas = Vars6(
        inputs=inputs,
        what="gas",
        h18=h18,
        energy=r30.s_gas.energy + b30.s_gas.energy,
        CO2e_production_based_per_MWh=h18.p_gas.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_gas.CO2e_combustion_based_per_MWh,
    )
    coal = Vars6(
        inputs=inputs,
        what="coal",
        h18=h18,
        energy=r30.s_coal.energy + b30.s_coal.energy,
        CO2e_production_based_per_MWh=h18.p_coal.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_coal.CO2e_combustion_based_per_MWh,
    )
    fueloil = Vars6(
        inputs=inputs,
        what="fueloil",
        h18=h18,
        energy=r30.s_fueloil.energy + b30.s_fueloil.energy,
        CO2e_production_based_per_MWh=0,
        CO2e_combustion_based_per_MWh=h18.p_fueloil.CO2e_combustion_based_per_MWh,
    )

    biomass = Vars6(
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

    lpg = Vars9(
        inputs=inputs,
        what="lpg",
        h18=h18,
        energy=r30.s_lpg.energy + b30.s_lpg.energy,
        CO2e_combustion_based_per_MWh=h18.p_lpg.CO2e_combustion_based_per_MWh,
        CO2e_production_based_per_MWh=0,
    )

    opetpro = Vars9(
        inputs=inputs,
        what="opetpro",
        h18=h18,
        energy=0,
        CO2e_production_based_per_MWh=h18.p_opetpro.CO2e_production_based_per_MWh,
        CO2e_combustion_based_per_MWh=h18.p_opetpro.CO2e_combustion_based_per_MWh,
    )

    heatnet_cogen_energy = (
        p_local_biomass_cogen_energy
        if (p_local_biomass_cogen_energy < p_heatnet_energy)
        else p_heatnet_energy
    )
    heatnet_cogen = Vars9(
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

    ofossil = Vars9(
        inputs=inputs,
        what="ofossil",
        h18=h18,
        energy=0,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=0,
    )
    solarth = Vars9(
        inputs=inputs,
        what="solarth",
        h18=h18,
        energy=r30.s_solarth.energy + b30.s_solarth.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )
    heatpump = Vars9(
        inputs=inputs,
        what="heatpump",
        h18=h18,
        energy=r30.s_heatpump.energy + b30.s_heatpump.energy + a30.s_heatpump.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )
    orenew = Vars9(
        inputs=inputs,
        what="orenew",
        h18=h18,
        energy=solarth.energy + heatpump.energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=0,
    )

    return Production(
        # total=total,
        gas=gas,
        lpg=lpg,
        fueloil=fueloil,
        opetpro=opetpro,
        coal=coal,
        # heatnet=heatnet,
        heatnet_cogen=heatnet_cogen,
        # heatnet_plant=heatnet_plant,
        # heatnet_geoth=heatnet_geoth,
        # heatnet_lheatpump=heatnet_lheatpump,
        biomass=biomass,
        ofossil=ofossil,
        orenew=orenew,
        solarth=solarth,
        heatpump=heatpump,
    )
