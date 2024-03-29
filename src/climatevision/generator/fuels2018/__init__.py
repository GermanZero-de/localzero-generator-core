"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/fuel.html
"""

# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts
from ..transport2018.t18 import T18
from ..industry2018.i18 import I18

from .f18 import F18, CO2eEmission
from . import energy_base, energy_demand, energy_production


def calc(entries: Entries, facts: Facts, *, t18: T18, i18: I18) -> F18:
    """This computes the CO2e that is created by the production of fuels.
    NOTE: This does not compute the CO2e caused by burning fuels, those are in
    those sectors that make use of the fuels (transport, heat, ...).
    """
    # How does this work? It's very simple in make entries we already approximated
    # much of each fuel is used by the AGS in each sector (the total required by
    # each sector in Germany is known in the reference data).
    # So now we just determine the total amounts of each fuel and then multiply
    # by the "this is how much CO2e is emitted during production" factor.

    energies = energy_base.calc(entries, t18, i18)
    demand = energy_demand.calc_demand(energies)
    production = energy_production.calc_production(facts, energies)

    f = CO2eEmission(
        CO2e_combustion_based=production.total.CO2e_combustion_based,
        CO2e_production_based=production.total.CO2e_production_based,
    )

    return F18(
        d_r=demand.residences,
        d_b=demand.business,
        d_i=demand.industry,
        d_t=demand.transport,
        d_a=demand.agri,
        d=demand.total,
        p_petrol=production.petrol,
        p_jetfuel=production.jetfuel,
        p_diesel=production.diesel,
        p_bioethanol=production.bioethanol,
        p_biodiesel=production.biodiesel,
        p_biogas=production.biogas,
        p=production.total,
        f=f,
    )
