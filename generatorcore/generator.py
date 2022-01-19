#!/usr/bin/env python
# coding: utf-8

# hier Sektoren Files importieren:
from prequel import *
from electricity2018 import *
from business2018 import *
from industry2018 import *
from transport2018 import *
from residences2018 import *
from agri2018 import *
from heat2018 import *
from lulucf2018 import *
from fuels2018 import *

from residences2030 import *
from business2030 import *
from heat2030 import *
from fuels2030 import *
from transport2030 import *
from electricity2030 import *
from heat2030 import *
from agri2030 import *
from lulucf2030 import *
from industry2030 import *
from setup import *
import time


@dataclass
class Generator:

    # Definition der Sektoren als Klassenvariablen. (Bitte Auskommentieren, wenn fertig)

    # 2018
    r18: R18 = R18()  # Residences
    b18: B18 = B18()  # Gewerbe Handel Dienstleisung
    i18: I18 = I18()  # Industry
    t18: T18 = T18()  # Transport
    a18: A18 = A18()  # Agriculture
    f18: F18 = F18()  # Fuels
    e18: E18 = E18()  # Electricity
    h18: H18 = H18()  # Heat
    l18: L18 = L18()  # Lulucf
    a18: A18 = A18()

    # Zieljahr
    r30: R30 = R30()
    b30: B30 = B30()
    i30: I30 = I30()
    t30: T30 = T30()
    f30: F30 = F30()
    e30: E30 = E30()
    h30: H30 = H30()
    l30: L30 = L30()
    a30: A30 = A30()
    h30: H30 = H30()

    # search value
    def search_value(self, var: str):
        sep = '.'
        gen = self.dict
        for k in gen:
            for l in gen[k]:
                if type(gen[k][l]) == dict:
                    for m in gen[k][l]:
                        if l+sep+m == var:
                            print(k+sep+l+sep+m+"=", gen[k][l][m])

    # Hier werden alle fertigen Kalkulationsfunktionen pro Sektor hinzugefügt
    def calculate(self):
        start_t = time.time()
        # 2018
        print('Residence2018_calc')
        Residence2018_calc(self)
        print('Business2018_calc')
        Business2018_calc(self)
        print('Industry2018_calc')
        Industry2018_calc(self)
        print('Transport2018_calc')
        Transport2018_calc(self)
        print('Fuels2018_calc')
        Fuels2018_calc(self)
        print('Electricity2018_calc')
        Electricity2018_calc(self)
        print('Heat2018_calc')
        Heat2018_calc(self)
        print('Lulucf2018_calc')
        Lulucf2018_calc(self)
        print('Agri2018_calc')
        Agri2018_calc(self)
        end_t = time.time()
        print('elapsed time for 18-sectors: {:5.3f}s'.format(end_t-start_t))

        # Zieljahr
        # print('Prequel_calc')
        # Prequel_calc(self)
        print('Transport2030')
        Transport2030_calc(self)
        print('Industry2030')
        Industry2030_calc(self)
        print('Residenctial2030')
        Residence2030_calc(self)
        print('Business2030_calc')
        Business2030_calc(self)
        print('Lulucf2030_calc')
        Lulucf2030_calc(self)
        print('Transport2030_calc')
        print('Agri2030_calc')
        Agri2030_calc(self)
        print('Heat2030_calc')
        Heat2030_calc(self)
        print('Fuels2030_calc')
        Fuels2030_calc(self)
        print('Electricity2030_calc')
        Electricity2030_calc(self)
        # print('Pyrolyse')

    # Berechnung im post init Konstruktor
    def __post_init__(self):
        self.calculate()
        # dictionary from DataClass
        self.dict = asdict(self)


# Generator Object
g = Generator()
