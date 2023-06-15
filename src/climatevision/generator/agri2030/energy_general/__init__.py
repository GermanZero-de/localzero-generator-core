# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions

from .co2e_change_g import CO2eChangeG
from .co2e_change_g_consult import CO2eChangeGConsult
from .co2e_change_g_organic import CO2eChangeGOrganic


@dataclass(kw_only=True)
class General:
    g: CO2eChangeG
    g_consult: CO2eChangeGConsult
    g_organic: CO2eChangeGOrganic


def calc_general(entries: Entries, facts: Facts, assumptions: Assumptions) -> General:

    g_consult = CO2eChangeGConsult(entries=entries, assumptions=assumptions)
    g_organic = CO2eChangeGOrganic(
        entries=entries, facts=facts, assumptions=assumptions
    )

    g = CO2eChangeG(g_consult=g_consult, g_organic=g_organic)

    return General(g=g, g_consult=g_consult, g_organic=g_organic)
