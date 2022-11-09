# pyright: strict

from dataclasses import dataclass, fields, is_dataclass
from time import time
from sys import stderr

from .inputs import Inputs
from .refdata import RefData
from .makeentries import make_entries
from .bisko import Bisko
from .methodology183x import M183X
from .lulucf2030 import lulucf2030_pyr
from .electricity2030 import electricity2030_core

# hier Sektoren Files importieren:
from .electricity2018.e18 import E18
from .business2018.b18 import B18
from .industry2018.i18 import I18
from .transport2018.t18 import T18
from .residences2018.r18 import R18
from .agri2018.a18 import A18
from .heat2018.h18 import H18
from .lulucf2018.l18 import L18
from .fuels2018.f18 import F18

from .electricity2030.e30 import E30
from .business2030.b30 import B30
from .industry2030.i30 import I30
from .transport2030.t30 import T30
from .residences2030.r30 import R30
from .agri2030.a30 import A30
from .heat2030.h30 import H30
from .lulucf2030.l30 import L30
from .fuels2030.f30 import F30

from . import electricity2018
from . import business2018
from . import industry2018
from . import transport2018
from . import residences2018
from . import agri2018
from . import heat2018
from . import lulucf2018
from . import fuels2018

from . import residences2030
from . import business2030
from . import heat2030
from . import fuels2030
from . import transport2030
from . import electricity2030
from . import heat2030
from . import agri2030
from . import lulucf2030
from . import industry2030

from . import methodology183x


def _convert_item(v: object) -> object:
    if is_dataclass(v) and not isinstance(v, type):
        return dataclass_to_result_dict(v)
    else:
        return v


def dataclass_to_result_dict(v: object) -> dict[str, object]:
    """This does basically the same as asdict from dataclasses does.

    The most important difference is that classes can contain a list
    called LIFT_INTO_RESULT_DICT and will list all values contained
    in that dictionary into the resulting dictionary.
    """
    result = {f.name: _convert_item(getattr(v, f.name)) for f in fields(v)}
    names_to_lift: list[str] = getattr(v, "LIFT_INTO_RESULT_DICT", [])
    values_to_lift: list[dict[str, object]] = []
    for name in names_to_lift:
        v = result[name]
        if isinstance(v, dict):
            values_to_lift.append(v)  # type: ignore
            del result[name]
        else:
            assert (
                False
            ), f"LIFT_INTO_RESULT_DICT encountered {v} at {name} -- which is not a dictionary"
    for v in values_to_lift:
        result.update(v)
    return result


@dataclass(kw_only=True)
class Result:
    # 2018
    r18: R18
    b18: B18
    i18: I18
    t18: T18
    a18: A18
    f18: F18
    e18: E18
    h18: H18
    l18: L18

    # Zieljahr
    r30: R30
    b30: B30
    i30: I30
    t30: T30
    f30: F30
    e30: E30
    h30: H30
    l30: L30
    a30: A30

    m183X: M183X
    bisko: Bisko

    def result_dict(self):
        return dataclass_to_result_dict(self)


def calculate(inputs: Inputs) -> Result:
    """This is the entry point to the actual calculation."""
    start_t = time()
    # 2018
    print("Residence2018_calc", file=stderr)
    r18 = residences2018.calc(inputs)

    print("Business2018_calc", file=stderr)
    b18 = business2018.calc(inputs, r18=r18)

    print("Industry2018_calc", file=stderr)
    i18 = industry2018.calc(inputs)

    print("Transport2018_calc", file=stderr)
    t18 = transport2018.calc(inputs)

    print("Fuels2018_calc", file=stderr)
    f18 = fuels2018.calc(inputs, t18=t18)

    print("Lulucf2018_calc", file=stderr)
    l18 = lulucf2018.calc(inputs)

    print("Agri2018_calc", file=stderr)
    a18 = agri2018.calc(inputs, l18=l18, b18=b18)

    print("Electricity2018_calc", file=stderr)
    e18 = electricity2018.calc(inputs, t18=t18)

    print("Heat2018_calc", file=stderr)
    h18 = heat2018.calc(inputs, t18=t18, e18=e18)

    end_t = time()
    print(
        "elapsed time for 18-sectors: {:5.3f}s".format(end_t - start_t),
        file=stderr,
    )

    # target year
    print("Transport2030", file=stderr)
    t30 = transport2030.calc(inputs, t18=t18)

    print("Industry2030", file=stderr)
    i30 = industry2030.calc(inputs, i18=i18)

    print("Residenctial2030", file=stderr)
    r30 = residences2030.calc(inputs, r18=r18, b18=b18)

    print("Business2030_calc", file=stderr)
    b30 = business2030.calc(inputs, b18=b18, r18=r18, r30=r30)

    print("Lulucf2030_calc", file=stderr)
    l30 = lulucf2030.calc(inputs, l18=l18)

    print("Agri2030_calc", file=stderr)
    a30 = agri2030.calc(inputs, a18=a18, l30=l30)

    print("Electricity2030_calc_biomass", file=stderr)
    p_local_biomass = electricity2030_core.calc_biomass(inputs)
    p_local_biomass_cogen = electricity2030_core.calc_biomass_cogen(
        inputs, p_local_biomass=p_local_biomass
    )

    print("Heat2030_calc", file=stderr)
    h30 = heat2030.calc(
        inputs,
        h18=h18,
        r30=r30,
        b30=b30,
        a30=a30,
        i30=i30,
        p_local_biomass_cogen=p_local_biomass_cogen,
    )

    print("Fuels2030_calc", file=stderr)
    f30 = fuels2030.calc(
        inputs, f18=f18, a30=a30, b30=b30, h30=h30, i30=i30, r30=r30, t30=t30
    )

    print("Electricity2030_calc", file=stderr)
    e30 = electricity2030.calc(
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
        p_local_biomass_cogen=p_local_biomass_cogen,
        p_local_biomass=p_local_biomass,
    )

    print("Methodology2030_calc", file=stderr)
    m183X = methodology183x.calc_budget(
        inputs,
        a18=a18,
        b18=b18,
        e18=e18,
        f18=f18,
        h18=h18,
        i18=i18,
        l18=l18,
        r18=r18,
        t18=t18,
    )

    print("Lulucf2030_calcPyr", file=stderr)
    lulucf2030_pyr.calc(
        inputs,
        l18=l18,
        l30=l30,
        a30=a30,
        b30=b30,
        e30=e30,
        f30=f30,
        h30=h30,
        i30=i30,
        r30=r30,
        t30=t30,
    )

    print("Methodology2030_calcZ", file=stderr)
    methodology183x.calc_z(
        inputs,
        m183X=m183X,
        a18=a18,
        b18=b18,
        e18=e18,
        f18=f18,
        h18=h18,
        i18=i18,
        l18=l18,
        r18=r18,
        t18=t18,
        a30=a30,
        b30=b30,
        e30=e30,
        f30=f30,
        h30=h30,
        i30=i30,
        l30=l30,
        r30=r30,
        t30=t30,
    )

    print("Bisko_calc", file=stderr)
    bisko = Bisko.calc(
        inputs,
        r18=r18,
        b18=b18,
        i18=i18,
        t18=t18,
        f18=f18,
        l18=l18,
        a18=a18,
        e18=e18,
        h18=h18,
    )

    return Result(
        r18=r18,
        b18=b18,
        i18=i18,
        t18=t18,
        f18=f18,
        l18=l18,
        a18=a18,
        e18=e18,
        h18=h18,
        t30=t30,
        i30=i30,
        r30=r30,
        b30=b30,
        f30=f30,
        e30=e30,
        l30=l30,
        a30=a30,
        h30=h30,
        m183X=m183X,
        bisko=bisko,
    )


def calculate_with_default_inputs(ags: str, year: int) -> Result:
    """Calculate without the ability to override entries."""
    refdata = RefData.load()
    entries = make_entries(refdata, ags=ags, year=year)
    inputs = Inputs(
        facts_and_assumptions=refdata.facts_and_assumptions(), entries=entries
    )
    return calculate(inputs)
