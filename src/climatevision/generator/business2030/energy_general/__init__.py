# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts, Assumptions
from ...common.g import G, GConsult
from ...business2018.b18 import B18


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    population_commune_2018: int,
    population_germany_2018: int,
    b18: B18,
) -> General:
    fact = facts.fact
    ass = assumptions.ass

    invest = (
        fact("Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats")
        * b18.p_nonresi.number_of_buildings
    )

    emplo_existing = (
        fact("Fact_R_G_energy_consulting_total_personel")
        * ass("Ass_B_D_energy_consulting_emplo_pct_of_B")
        * population_commune_2018
        / population_germany_2018
    )

    g_consult = GConsult.calc_from_invest(
        facts, duration_until_target_year, invest, emplo_existing
    )

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
