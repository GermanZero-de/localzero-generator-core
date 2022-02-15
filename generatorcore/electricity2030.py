from .inputs import Inputs
from . import electricity2030_core, electricity2030_com, electricity2030_ger
from . import (
    electricity2018,
    residences2018,
    business2018,
    agri2030,
    business2030,
    fuels2030,
    heat2030,
    industry2030,
    residences2030,
    transport2030,
)

E30 = electricity2030_core.E30


def calc(
    inputs: Inputs,
    *,
    e18: electricity2018.E18,
    r18: residences2018.R18,
    b18: business2018.B18,
    a30: agri2030.A30,
    b30: business2030.B30,
    f30: fuels2030.F30,
    h30: heat2030.H30,
    i30: industry2030.I30,
    r30: residences2030.R30,
    t30: transport2030.T30,
) -> E30:

    """For electricity 203X unfortunately if-sides of conditional statements require a different sorting of formulas
    than else sides. Hence  we have to hold two files for the 2 situations
    Each change of variable calculus has to be consistently edited within the 2 files"""

    if inputs.str_entry("In_M_AGS_com") == "DG000000":
        return electricity2030_ger.calc(
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
        )
    else:
        return electricity2030_com.calc(
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
        )
