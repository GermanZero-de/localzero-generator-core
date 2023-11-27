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
        p_heating=production.heating,
        p_heating_fossil=production.heating_fossil,
        p_heating_fossil_gas=production.heating_fossil_gas,
        p_heating_fossil_lpg=production.heating_fossil_lpg,
        p_heating_fossil_fueloil=production.heating_fossil_fueloil,
        p_heating_fossil_coal=production.heating_fossil_coal,
        p_heating_renew=production.heating_renew,
        p_heating_renew_heatnet=production.heating_renew_heatnet,
        p_heating_renew_biomass=production.heating_renew_biomass,
        p_heating_renew_elec_heating=production.heating_renew_elec_heating,
        p_heating_renew_elec_heatpump=production.heating_renew_elec_heatpump,
        p_heating_renew_without_heating=production.heating_renew_without_heating,
        p=production.total,
        s_dummy=supply.dummy,
        s=supply.total,
        r=r,
    )
