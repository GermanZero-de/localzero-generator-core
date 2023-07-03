# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...common.g import G, GConsult


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(entries: Entries, facts: Facts, assumptions: Assumptions) -> General:
    fact = facts.fact
    ass = assumptions.ass

    invest = entries.r_buildings_le_2_apts * fact(
        "Fact_R_G_energy_consulting_cost_detached_house"
    ) + entries.r_buildings_ge_3_apts * fact(
        "Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats"
    )

    emplo_existing = (
        fact("Fact_R_G_energy_consulting_total_personel")
        * ass("Ass_B_D_energy_consulting_emplo_pct_of_R")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )

    g_consult = GConsult.calc_from_invest(entries, facts, invest, emplo_existing)

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
