# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.g import G, GConsult
from ...business2018.b18 import B18


@dataclass(kw_only=True)
class General:
    g: G
    g_consult: GConsult


def calc_general(inputs: Inputs, b18: B18) -> General:

    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    invest = (
        fact("Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats")
        * b18.p_nonresi.number_of_buildings
    )

    emplo_existing = (
        fact("Fact_R_G_energy_consulting_total_personel")
        * ass("Ass_B_D_energy_consulting_emplo_pct_of_B")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )

    g_consult = GConsult.calc_from_invest(
        inputs.entries, inputs.facts, invest, emplo_existing
    )

    g = G.sum(g_consult)

    return General(g=g, g_consult=g_consult)
