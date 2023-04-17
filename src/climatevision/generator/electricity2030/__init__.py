"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/electricity.html
"""

# pyright: strict

from ..inputs import Inputs
from ..electricity2018.e18 import E18
from ..residences2018.r18 import R18
from ..business2018.b18 import B18
from ..agri2030.a30 import A30
from ..business2030.b30 import B30
from ..fuels2030.f30 import F30
from ..heat2030.h30 import H30
from ..industry2030.i30 import I30
from ..residences2030.r30 import R30
from ..transport2030.t30 import T30
from ..waste2030 import WasteLines

from .e30 import E30
from .electricity2030_core import EColVars2030
from . import electricity2030_germany, electricity2030_commune


def calc(
    inputs: Inputs,
    *,
    e18: E18,
    r18: R18,
    b18: B18,
    a30: A30,
    b30: B30,
    f30: F30,
    h30: H30,
    i30: I30,
    r30: R30,
    t30: T30,
    wastelines : WasteLines,
    p_local_biomass_cogen: EColVars2030,
    p_local_biomass: EColVars2030,
) -> E30:

    """For electricity 203X unfortunately if-sides of conditional statements require a different sorting of formulas
    than else sides. Hence  we have to hold two files for the 2 situations
    Each change of variable calculus has to be consistently edited within the 2 files"""

    if inputs.entries.m_AGS_com == "DG000000":
        return electricity2030_germany.calc(
            inputs,
            e18=e18,
            r18=r18,
            b18=b18,
            a30=a30,
            b30=b30,
            f30=f30,
            h30=h30,
            i30=i30,
            r30=r30,
            t30=t30,
            wastelines=wastelines,
            p_local_biomass_cogen=p_local_biomass_cogen,
            p_local_biomass=p_local_biomass,
        )
    else:
        return electricity2030_commune.calc(
            inputs,
            e18=e18,
            r18=r18,
            b18=b18,
            a30=a30,
            b30=b30,
            f30=f30,
            h30=h30,
            i30=i30,
            r30=r30,
            t30=t30,
            wastelines=wastelines,
            p_local_biomass_cogen=p_local_biomass_cogen,
            p_local_biomass=p_local_biomass,
        )
