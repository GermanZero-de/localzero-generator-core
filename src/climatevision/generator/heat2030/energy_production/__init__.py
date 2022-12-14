# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...heat2018.h18 import H18
from ...residences2030.r30 import R30
from ...business2030.b30 import B30

from ..dataclasses import (
    # Vars5,
    Vars6,
    Vars7,
    # Vars8,
    Vars9,
    # Vars10,
    # Vars11,
    # Vars12,
    # Vars13,
    # Vars14,
    # Vars15,
)


@dataclass(kw_only=True)
class Production:
    # total: Vars5
    gas: Vars6
    lpg: Vars7
    # fueloil: Vars8
    opetpro: Vars9
    coal: Vars6
    # heatnet: Vars10
    heatnet_cogen: Vars9
    # heatnet_plant: Vars11
    # heatnet_lheatpump: Vars12
    # heatnet_geoth: Vars13
    # biomass: Vars14
    # ofossil: Vars15
    # orenew: Vars15
    # solarth: Vars15
    # heatpump: Vars15


def calc_production(
    inputs: Inputs,
    h18: H18,
    r30: R30,
    b30: B30,
    p_local_biomass_cogen_energy: float,
    p_heatnet_energy: float,
) -> Production:

    fact = inputs.fact

    gas = Vars6.calc(inputs, "gas", h18, r30, b30)
    coal = Vars6.calc(inputs, "coal", h18, r30, b30)

    lpg = Vars7.calc(inputs, "lpg", h18, r30, b30)

    opetpro = Vars9.calc(
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
    heatnet_cogen = Vars9.calc(
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

    return Production(
        # total=total,
        gas=gas,
        lpg=lpg,
        # fueloil=fueloil,
        opetpro=opetpro,
        coal=coal,
        # heatnet=heatnet,
        heatnet_cogen=heatnet_cogen,
        # heatnet_plant=heatnet_plant,
        # heatnet_geoth=heatnet_geoth,
        # heatnet_lheatpump=heatnet_lheatpump,
        # biomass=biomass,
        # ofossil=ofossil,
        # orenew=orenew,
        # solarth=solarth,
        # heatpump=heatpump,
    )
