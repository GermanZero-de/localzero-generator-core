# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.g import G, GConsult


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(inputs: Inputs) -> General:

    g_consult = GConsult.calc_for_residences2030(inputs)

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
