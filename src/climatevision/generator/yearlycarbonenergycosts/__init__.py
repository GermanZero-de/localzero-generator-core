# pyright: strict

from dataclasses import dataclass
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


@dataclass(kw_only=True)
class Diesel:
    agriculture: float
    business: float
    industry: float
    transport: float


@dataclass(kw_only=True)
class Gas:
    agriculture: float
    business: float
    electricity: float
    heat: float
    industry: float
    residences: float
    transport: float


@dataclass(kw_only=True)
class YCEC:
    """Yearly carbon energy costs -- All energy in MWh per year"""

    energy_diesel: Diesel
    energy_fueloil: Fueloil
    energy_gas: Gas


def calc(
    *, a18: A18, b18: B18, e18: E18, h18: H18, i18: I18, r18: R18, t18: T18
) -> YCEC:
    energy_diesel = Diesel(
        agriculture=a18.s_diesel.energy,
        business=b18.s_diesel.energy,
        industry=i18.s_fossil_diesel.energy,
        transport=t18.s_diesel.energy,
    )
    energy_fueloil = Fueloil(
        agriculture=a18.s_fueloil.energy,
        business=b18.s_fueloil.energy,
        transport=t18.s_fueloil.energy,
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
    return YCEC(
        energy_diesel=energy_diesel,
        energy_fueloil=energy_fueloil,
        energy_gas=energy_gas,
    )
