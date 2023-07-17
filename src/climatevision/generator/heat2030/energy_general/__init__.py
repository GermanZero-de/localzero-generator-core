# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts, Assumptions
from ...common.g import G, GConsult as GPlanning, GConsult as GStorage


@dataclass(kw_only=True)
class General:
    g: G
    g_storage: GStorage
    g_planning: GPlanning


def calc_general(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    population_commune_2018: int,
    p_heatnet_energy: float,
) -> General:

    fact = facts.fact

    invest = (
        fact("Fact_H_P_planning_cost_basis")
        + fact("Fact_H_P_planning_cost_per_capita") * population_commune_2018
    )

    g_planning = GPlanning.calc_from_invest_calc_planning(
        facts, assumptions, duration_until_target_year, invest
    )
    g_storage = GStorage.calc_storage(
        facts, duration_until_target_year, energy=p_heatnet_energy
    )

    g = G.sum(g_planning, g_storage)

    return General(g=g, g_planning=g_planning, g_storage=g_storage)
