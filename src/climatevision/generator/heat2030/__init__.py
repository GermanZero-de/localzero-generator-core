"""
Documentation =
https://localzero-generator.readthedocs.io/de/latest/sectors/heat.html
"""

# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts, Assumptions
from ..heat2018.h18 import H18
from ..residences2030.r30 import R30
from ..business2030.b30 import B30
from ..agri2030.a30 import A30
from ..industry2030.i30 import I30

from .h30 import H30
from .h import H
from . import energy_demand, energy_general, energy_production


def calc(
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    *,
    h18: H18,
    r30: R30,
    b30: B30,
    a30: A30,
    i30: I30,
    e30_p_local_biomass_cogen_energy: float,
) -> H30:

    demand = energy_demand.calc_demand(r30, b30, i30, a30)

    production = energy_production.calc_production(
        facts,
        assumptions,
        entries.m_duration_neutral,
        entries.m_duration_target,
        h18,
        r30,
        b30,
        a30,
        i30,
        e30_p_local_biomass_cogen_energy,
    )

    general = energy_general.calc_general(
        facts=facts,
        assumptions=assumptions,
        duration_until_target_year=entries.m_duration_target,
        population_commune_2018=entries.m_population_com_2018,
        p_heatnet_energy=production.heatnet.energy,
    )

    h = H.of_p_and_g(production.total, general.g)

    p_fossil_change_CO2e_t = (
        production.total.change_CO2e_t - production.heatnet.change_CO2e_t
    )

    return H30(
        h=h,
        g=general.g,
        g_storage=general.g_storage,
        g_planning=general.g_planning,
        d=demand.total,
        d_r=demand.residences,
        d_b=demand.business,
        d_i=demand.industry,
        d_t=demand.transport,
        d_a=demand.agri,
        p=production.total,
        p_gas=production.gas,
        p_lpg=production.lpg,
        p_fueloil=production.fueloil,
        p_opetpro=production.opetpro,
        p_coal=production.coal,
        p_heatnet=production.heatnet,
        p_heatnet_cogen=production.heatnet_cogen,
        p_heatnet_plant=production.heatnet_plant,
        p_heatnet_lheatpump=production.heatnet_lheatpump,
        p_heatnet_geoth=production.heatnet_geoth,
        p_biomass=production.biomass,
        p_ofossil=production.ofossil,
        p_orenew=production.orenew,
        p_solarth=production.solarth,
        p_heatpump=production.heatpump,
        p_fossil_change_CO2e_t=p_fossil_change_CO2e_t,
    )
