# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.g import G, GConsult
from ...business2018.b18 import B18


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(inputs: Inputs, b18: B18) -> General:

    g_consult = GConsult.calc_for_business2030(inputs, b18)

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
