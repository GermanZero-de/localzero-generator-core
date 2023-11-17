# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts, Assumptions

from .r18_new import R18New
from . import energy_demand, energy_source


def calc(entries: Entries, facts: Facts, assumptions: Assumptions) -> R18New:

    production = energy_demand.calc_production(entries, facts, assumptions)
    supply = energy_source.calc_supply()

    r = 0

    return R18New(
        p_dummy=production.dummy,
        p=production.total,
        s_dummy=supply.dummy,
        s=supply.total,
        r=r,
    )
