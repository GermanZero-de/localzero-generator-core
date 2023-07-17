# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts, Assumptions

from .co2e_change_g import CO2eChangeG
from .co2e_change_g_consult import CO2eChangeGConsult
from .co2e_change_g_organic import CO2eChangeGOrganic


@dataclass(kw_only=True)
class General:
    g: CO2eChangeG
    g_consult: CO2eChangeGConsult
    g_organic: CO2eChangeGOrganic


def calc_general(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    farm_amount: float,
    area_agri_commune: int,
    area_agri_commune_pct_of_organic: float,
) -> General:

    g_consult = CO2eChangeGConsult(
        assumptions=assumptions,
        duration_until_target_year=duration_until_target_year,
        farm_amount=farm_amount,
    )
    g_organic = CO2eChangeGOrganic(
        facts=facts,
        assumptions=assumptions,
        duration_until_target_year=duration_until_target_year,
        area_agri_commune=area_agri_commune,
        area_agri_commune_pct_of_organic=area_agri_commune_pct_of_organic,
    )

    g = CO2eChangeG(g_consult=g_consult, g_organic=g_organic)

    return General(g=g, g_consult=g_consult, g_organic=g_organic)
