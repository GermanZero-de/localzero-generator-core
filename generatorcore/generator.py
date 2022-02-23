import time
from dataclasses import dataclass, asdict
import sys
from generatorcore import electricity2030_core, methodology183x

from .refdata import RefData
from .inputs import Inputs
from .makeentries import make_entries

# hier Sektoren Files importieren:
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
from . import lulucf2030_pyr


@dataclass
class Result:
    # 2018
    r18: residences2018.R18
    b18: business2018.B18
    i18: industry2018.I18
    t18: transport2018.T18
    a18: agri2018.A18
    f18: fuels2018.F18
    e18: electricity2018.E18
    h18: heat2018.H18
    l18: lulucf2018.L18

    # Zieljahr
    r30: residences2030.R30
    b30: business2030.B30
    i30: industry2030.I30
    t30: transport2030.T30
    f30: fuels2030.F30
    e30: electricity2030.E30
    h30: heat2030.H30
    l30: lulucf2030.L30
    a30: agri2030.A30
    h30: heat2030.H30

    m183X: methodology183x.M183X

    # search value
    def search_value(self, var: str):
        sep = "."
        gen = self.result_dict()
        for k in gen:
            for l in gen[k]:
                if type(gen[k][l]) == dict:
                    for m in gen[k][l]:
                        if l + sep + m == var:
                            print(k + sep + l + sep + m + "=", gen[k][l][m])

    def result_dict(self):
        return asdict(self)


def calculate(inputs: Inputs) -> Result:
    """This is the entry point to the actual calculation."""
    start_t = time.time()
    # 2018
    print("Residence2018_calc", file=sys.stderr)
    r18 = residences2018.calc(inputs)

    print("Business2018_calc", file=sys.stderr)
    b18 = business2018.calc(inputs, r18=r18)

    print("Industry2018_calc", file=sys.stderr)
    i18 = industry2018.calc(inputs)

    print("Transport2018_calc", file=sys.stderr)
    t18 = transport2018.calc(inputs)

    print("Fuels2018_calc", file=sys.stderr)
    f18 = fuels2018.calc(inputs, t18=t18)

    print("Lulucf2018_calc", file=sys.stderr)
    l18 = lulucf2018.calc(inputs)

    print("Agri2018_calc", file=sys.stderr)
    a18 = agri2018.calc(inputs, l18=l18, b18=b18)

    print("Electricity2018_calc", file=sys.stderr)
    e18 = electricity2018.calc(inputs, t18=t18)

    print("Heat2018_calc", file=sys.stderr)
    h18 = heat2018.calc(inputs, t18=t18, e18=e18)

    end_t = time.time()
    print(
        "elapsed time for 18-sectors: {:5.3f}s".format(end_t - start_t),
        file=sys.stderr,
    )

    # target year
    print("Transport2030", file=sys.stderr)
    t30 = transport2030.calc(inputs, t18=t18)

    print("Industry2030", file=sys.stderr)
    i30 = industry2030.calc(inputs, i18=i18)

    print("Residenctial2030", file=sys.stderr)
    r30 = residences2030.calc(inputs, r18=r18, b18=b18)

    print("Business2030_calc", file=sys.stderr)
    b30 = business2030.calc(inputs, b18=b18, r18=r18, r30=r30)

    print("Lulucf2030_calc", file=sys.stderr)
    l30 = lulucf2030.calc(inputs, l18=l18)

    print("Agri2030_calc", file=sys.stderr)
    a30 = agri2030.calc(inputs, a18=a18, l30=l30)

    print("Electricity2030_calc_biomass", file=sys.stderr)
    p_local_biomass = electricity2030_core.calc_biomass(inputs)
    p_local_biomass_cogen = electricity2030_core.calc_biomass_cogen(inputs,p_local_biomass=p_local_biomass)

    print("Heat2030_calc", file=sys.stderr)
    h30 = heat2030.calc(inputs, h18=h18, r30=r30, b30=b30, a30=a30, i30=i30, p_local_biomass_cogen = p_local_biomass_cogen)

    print("Fuels2030_calc", file=sys.stderr)
    f30 = fuels2030.calc(
        inputs, f18=f18, a30=a30, b30=b30, h30=h30, i30=i30, r30=r30, t30=t30
    )

    print("Electricity2030_calc", file=sys.stderr)
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
        p_local_biomass_cogen = p_local_biomass_cogen,
        p_local_biomass = p_local_biomass,
    )

    print("Methodology2030_calc", file=sys.stderr)
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

    print("Lulucf2030_calcPyr", file=sys.stderr)
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

    print("Methodology2030_calcZ", file=sys.stderr)
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
    )


def calculate_with_default_inputs(ags: str, year: int) -> Result:
    """Calculate without the ability to override entries."""
    refdata = RefData.load()
    entries = make_entries(refdata, ags=ags, year=year)
    inputs = Inputs(
        facts_and_assumptions=refdata.facts_and_assumptions(), entries=entries
    )
    return calculate(inputs)
