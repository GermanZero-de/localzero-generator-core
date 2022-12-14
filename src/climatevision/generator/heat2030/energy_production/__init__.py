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
    # Vars9,
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
    # opetpro: Vars9
    coal: Vars6
    # heatnet: Vars10
    # heatnet_cogen: Vars9
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
) -> Production:

    gas = Vars6.calc(inputs, "gas", h18, r30, b30)
    coal = Vars6.calc(inputs, "coal", h18, r30, b30)

    lpg = Vars7.calc(inputs, "lpg", h18, r30, b30)

    return Production(
        # total=total,
        gas=gas,
        lpg=lpg,
        # fueloil=fueloil,
        # opetpro=opetpro,
        coal=coal,
        # heatnet=heatnet,
        # heatnet_cogen=heatnet_cogen,
        # heatnet_plant=heatnet_plant,
        # heatnet_geoth=heatnet_geoth,
        # heatnet_lheatpump=heatnet_lheatpump,
        # biomass=biomass,
        # ofossil=ofossil,
        # orenew=orenew,
        # solarth=solarth,
        # heatpump=heatpump,
    )
