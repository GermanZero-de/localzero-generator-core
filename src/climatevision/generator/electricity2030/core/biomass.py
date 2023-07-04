# pyright: strict

from ...makeentries import Entries
from ...refdata import Facts, Assumptions

from .e_col_vars_2030 import EColVars2030


def calc_biomass(
    entries: Entries, facts: Facts, assumptions: Assumptions
) -> EColVars2030:
    fact = facts.fact
    ass = assumptions.ass

    p_local_biomass = EColVars2030()

    p_local_biomass.full_load_hour = fact("Fact_E_P_biomass_full_load_hours")

    p_local_biomass.power_installed = entries.e_PV_power_inst_biomass
    p_local_biomass.power_to_be_installed_pct = (
        entries.e_PV_power_to_be_inst_local_biomass
    )

    p_local_biomass.power_installable = entries.e_biomass_local_power_installable_sta
    p_local_biomass.power_to_be_installed = max(
        0,
        p_local_biomass.power_installable * p_local_biomass.power_to_be_installed_pct
        - p_local_biomass.power_installed,
    )
    p_local_biomass.energy = (
        (p_local_biomass.power_to_be_installed + p_local_biomass.power_installed)
        * p_local_biomass.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )

    return p_local_biomass


def calc_biomass_cogen(facts: Facts, *, p_local_biomass: EColVars2030) -> EColVars2030:
    fact = facts.fact

    p_local_biomass_cogen = EColVars2030()

    p_local_biomass_cogen.energy = p_local_biomass.energy * fact(
        "Fact_E_P_renew_cogen_ratio_2018"
    )

    return p_local_biomass_cogen
