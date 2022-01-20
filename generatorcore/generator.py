import time
from dataclasses import dataclass, asdict
import sys

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


@dataclass
class Generator:

    # Definition der Sektoren als Klassenvariablen. (Bitte Auskommentieren, wenn fertig)

    # 2018
    r18: residences2018.R18 = residences2018.R18()  # Residences
    b18: business2018.B18 = business2018.B18()  # Gewerbe Handel Dienstleisung
    i18: industry2018.I18 = industry2018.I18()  # Industry
    t18: transport2018.T18 = transport2018.T18()  # Transport
    a18: agri2018.A18 = agri2018.A18()  # Agriculture
    f18: fuels2018.F18 = fuels2018.F18()  # Fuels
    e18: electricity2018.E18 = electricity2018.E18()  # Electricity
    h18: heat2018.H18 = heat2018.H18()  # Heat
    l18: lulucf2018.L18 = lulucf2018.L18()  # Lulucf

    # Zieljahr
    r30: residences2030.R30 = residences2030.R30()
    b30: business2030.B30 = business2030.B30()
    i30: industry2030.I30 = industry2030.I30()
    t30: transport2030.T30 = transport2030.T30()
    f30: fuels2030.F30 = fuels2030.F30()
    e30: electricity2030.E30 = electricity2030.E30()
    h30: heat2030.H30 = heat2030.H30()
    l30: lulucf2030.L30 = lulucf2030.L30()
    a30: agri2030.A30 = agri2030.A30()
    h30: heat2030.H30 = heat2030.H30()

    # search value
    def search_value(self, var: str):
        sep = "."
        gen = self.dict
        for k in gen:
            for l in gen[k]:
                if type(gen[k][l]) == dict:
                    for m in gen[k][l]:
                        if l + sep + m == var:
                            print(k + sep + l + sep + m + "=", gen[k][l][m])

    # Hier werden alle fertigen Kalkulationsfunktionen pro Sektor hinzugefügt
    def calculate(self):
        start_t = time.time()
        # 2018
        print("Residence2018_calc", file=sys.stderr)
        residences2018.Residence2018_calc(self)
        print("Business2018_calc", file=sys.stderr)
        business2018.Business2018_calc(self)
        print("Industry2018_calc", file=sys.stderr)
        industry2018.Industry2018_calc(self)
        print("Transport2018_calc", file=sys.stderr)
        transport2018.Transport2018_calc(self)
        print("Fuels2018_calc", file=sys.stderr)
        fuels2018.Fuels2018_calc(self)
        print("Electricity2018_calc", file=sys.stderr)
        electricity2018.Electricity2018_calc(self)
        print("Heat2018_calc", file=sys.stderr)
        heat2018.Heat2018_calc(self)
        print("Lulucf2018_calc", file=sys.stderr)
        lulucf2018.Lulucf2018_calc(self)
        print("Agri2018_calc", file=sys.stderr)
        agri2018.Agri2018_calc(self)
        end_t = time.time()
        print(
            "elapsed time for 18-sectors: {:5.3f}s".format(end_t - start_t),
            file=sys.stderr,
        )

        # Zieljahr
        # print('Prequel_calc')
        # Prequel_calc(self)
        print("Transport2030", file=sys.stderr)
        transport2030.Transport2030_calc(self)
        print("Industry2030", file=sys.stderr)
        industry2030.Industry2030_calc(self)
        print("Residenctial2030", file=sys.stderr)
        residences2030.Residence2030_calc(self)
        print("Business2030_calc", file=sys.stderr)
        business2030.Business2030_calc(self)
        print("Lulucf2030_calc", file=sys.stderr)
        lulucf2030.Lulucf2030_calc(self)
        print("Transport2030_calc", file=sys.stderr)
        print("Agri2030_calc", file=sys.stderr)
        agri2030.Agri2030_calc(self)
        print("Heat2030_calc", file=sys.stderr)
        heat2030.Heat2030_calc(self)
        print("Fuels2030_calc", file=sys.stderr)
        fuels2030.Fuels2030_calc(self)
        print("Electricity2030_calc", file=sys.stderr)
        electricity2030.Electricity2030_calc(self)
        # print('Pyrolyse')

    # Berechnung im post init Konstruktor
    def __post_init__(self):
        self.calculate()
        # dictionary from DataClass
        self.dict = asdict(self)

    def result_dict(self):
        return self.dict
