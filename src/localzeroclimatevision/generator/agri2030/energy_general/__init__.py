# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs

from .co2eChangeG import CO2eChangeG
from .co2eChangeGConsult import CO2eChangeGConsult
from .co2eChangeGOrganic import CO2eChangeGOrganic


@dataclass(kw_only=True)
class G:
    g: CO2eChangeG
    g_consult: CO2eChangeGConsult
    g_organic: CO2eChangeGOrganic


def calc_general(inputs: Inputs) -> G:

    g_consult = CO2eChangeGConsult(inputs=inputs)
    g_organic = CO2eChangeGOrganic(inputs=inputs)

    g = CO2eChangeG(g_consult=g_consult, g_organic=g_organic)

    return G(g=g, g_consult=g_consult, g_organic=g_organic)
