"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/fuel.html
"""

# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts, Assumptions
from ..fuels2018.f18 import F18
from ..agri2030.a30 import A30
from ..business2030.b30 import B30
from ..heat2030.h30 import H30
from ..industry2030.i30 import I30
from ..residences2030.r30 import R30
from ..transport2030.t30 import T30
from ..waste2030 import WasteLines
from .f30 import F30
from .f import F
from .energy_demand import EnergyDemand
from . import energy_demand, energy_production


def calc(
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    *,
    f18: F18,
    a30: A30,
    b30: B30,
    h30: H30,
    i30: I30,
    r30: R30,
    t30: T30,
    wastelines: WasteLines,
) -> F30:

    production = energy_production.calc_production(
        entries, facts, assumptions, f18, a30, b30, h30, i30, r30, t30, wastelines
    )
    demand = energy_demand.calc_demand(
        a30, b30, i30, r30, t30, production.hydrogen_reconv
    )

    f = F.of_p(production.total)

    return F30(
        d=demand.total,
        d_r=demand.residences,
        d_b=demand.business,
        d_i=demand.industry,
        d_t=demand.transport,
        d_a=demand.agri,
        d_e_hydrogen_reconv=demand.electricity_hydrogen_reconv,
        p_petrol=production.petrol,
        p_jetfuel=production.jetfuel,
        p_diesel=production.diesel,
        p_biogas=production.biogas,
        p_biodiesel=production.biodiesel,
        p_bioethanol=production.bioethanol,
        p_emethan=production.emethan,
        p_hydrogen=production.hydrogen,
        p_hydrogen_reconv=production.hydrogen_reconv,
        p_efuels=production.efuels,
        p_hydrogen_total=EnergyDemand(
            energy=production.hydrogen.energy + production.hydrogen_reconv.energy
        ),
        p=production.total,
        f=f,
    )
