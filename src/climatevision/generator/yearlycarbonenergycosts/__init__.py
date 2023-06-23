# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import convert_MWh_to_TJ

from ..agri2018.a18 import A18
from ..business2018.b18 import B18
from ..electricity2018.e18 import E18
from ..heat2018.h18 import H18
from ..industry2018.i18 import I18
from ..residences2018.r18 import R18
from ..transport2018.t18 import T18


@dataclass(kw_only=True)
class Fueloil:
    agriculture: float
    business: float
    transport: float

    def total(self) -> float:
        return self.agriculture + self.business + self.transport


@dataclass(kw_only=True)
class Diesel:
    agriculture: float
    business: float
    industry: float
    transport: float

    def total(self) -> float:
        return self.agriculture + self.business + self.industry + self.transport


@dataclass(kw_only=True)
class Gas:
    agriculture: float
    business: float
    electricity: float
    heat: float
    industry: float
    residences: float
    transport: float

    def total(self) -> float:
        return (
            self.agriculture
            + self.business
            + self.electricity
            + self.heat
            + self.industry
            + self.residences
            + self.transport
        )


@dataclass(kw_only=True)
class YCEC:
    """Yearly carbon energy costs -- All energy in MWh per year. All costs in EUR per year."""

    energy_diesel: Diesel
    cost_diesel: float
    energy_fueloil: Fueloil
    cost_fueloil: float
    energy_gas: Gas
    cost_gas: float


# From https://www.bafa.de/DE/Energie/Rohstoffe/Erdgasstatistik/erdgas_node.html
# Grenzübergangspreis 2021:  7.067 EUR/TJ
#                     2022: 21.008 EUR/TJ
# Here I'm just using the average over those two years.  Who knows what's right?
# This seems awfully low in comparison to 67,80 EUR/MWh (2018 average end user price)
# 67,80 EUR/MWh
# In particular because 2018 the grenzübergangspreis was: 5.359 EUR/TJ
PRICE_GAS_EUR_PER_TJ = 14.037  # EUR/TJ


def calc(
    inputs: Inputs,
    *,
    a18: A18,
    b18: B18,
    e18: E18,
    h18: H18,
    i18: I18,
    r18: R18,
    t18: T18,
) -> YCEC:
    """The prices used here are end user prices.  Maybe that's not right?"""
    energy_diesel = Diesel(
        agriculture=a18.s_diesel.energy,
        business=b18.s_diesel.energy,
        industry=i18.s_fossil_diesel.energy,
        transport=t18.s_diesel.energy,
    )
    # TODO:  Need a price here
    cost_diesel = energy_diesel.total() * 0
    energy_fueloil = Fueloil(
        agriculture=a18.s_fueloil.energy,
        business=b18.s_fueloil.energy,
        transport=t18.s_fueloil.energy,
    )
    cost_fueloil = energy_fueloil.total() * inputs.fact(
        "Fact_R_S_fueloil_energy_cost_factor_2018"
    )
    energy_gas = Gas(
        agriculture=a18.s_gas.energy,
        business=b18.s_gas.energy,
        electricity=e18.p_fossil_gas.energy,
        heat=h18.p_gas.energy,
        industry=i18.s_fossil_gas.energy,
        residences=r18.s_gas.energy,
        transport=t18.s_gas.energy,
    )
    cost_gas = convert_MWh_to_TJ(energy_gas.total()) * PRICE_GAS_EUR_PER_TJ
    return YCEC(
        energy_diesel=energy_diesel,
        cost_diesel=cost_diesel,
        energy_fueloil=energy_fueloil,
        cost_fueloil=cost_fueloil,
        energy_gas=energy_gas,
        cost_gas=cost_gas,
    )
