# pyright: strict

from ..inputs import Inputs
from ..utils import div
from ..lulucf2018.l18 import L18
from ..lulucf2030.l30 import L30
from ..agri2030.a30 import A30
from ..business2030.b30 import B30
from ..electricity2030.e30 import E30
from ..fuels2030.f30 import F30
from ..heat2030.h30 import H30
from ..industry2030.i30 import I30
from ..residences2030.r30 import R30
from ..transport2030.t30 import T30


def calc(
    inputs: Inputs,
    *,
    l18: L18,
    l30: L30,
    a30: A30,
    b30: B30,
    e30: E30,
    f30: F30,
    h30: H30,
    i30: I30,
    r30: R30,
    t30: T30,
) -> None:
    """This updates the l and pyr sections in l30 inplace."""

    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    pyr = l30.pyr
    l = l30.l
    g = l30.g

    pyr.CO2e_total = min(
        -(
            h30.h.CO2e_total
            + e30.e.CO2e_total
            + f30.f.CO2e_total
            + r30.r.CO2e_total
            + b30.b.CO2e_total
            + i30.i.CO2e_total
            + t30.t.transport.CO2e_total
            + a30.a.CO2e_total
            + l30.g.CO2e_total
        ),
        0,
    )

    pyr.CO2e_production_based = pyr.CO2e_total
    pyr.CO2e_production_based_per_t = fact("Fact_L_P_biochar_ratio_CO2e_pb_to_prodvol")
    pyr.prod_volume = div(pyr.CO2e_production_based, pyr.CO2e_production_based_per_t)

    pyr.change_CO2e_t = pyr.CO2e_production_based

    pyr.change_CO2e_pct = 0
    pyr.CO2e_total_2021_estimated = 0

    pyr.cost_climate_saved = (
        (pyr.CO2e_total_2021_estimated - pyr.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    pyr.invest_per_x = ass("Ass_L_P_pyrolysis_plant_ratio_invest_to_biochar_pa")
    pyr.invest = pyr.prod_volume * pyr.invest_per_x
    pyr.invest_pa = div(pyr.invest, entries.m_duration_target)
    pyr.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    pyr.cost_wage = pyr.invest_pa * pyr.pct_of_wage

    pyr.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
    pyr.demand_emplo = div(pyr.cost_wage, pyr.ratio_wage_to_emplo)
    pyr.demand_emplo_new = pyr.demand_emplo

    l.CO2e_total = g.CO2e_total + pyr.CO2e_total
    l.CO2e_production_based = g.CO2e_production_based + pyr.CO2e_production_based
    l.CO2e_combustion_based = g.CO2e_combustion_based
    l.change_CO2e_t = l.CO2e_total - l18.l.CO2e_total
    l.change_CO2e_pct = div(l.change_CO2e_t, l18.l.CO2e_total)
    l.CO2e_total_2021_estimated = l18.l.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )

    l.cost_climate_saved = (
        (l.CO2e_total_2021_estimated - l.CO2e_total)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    l.invest_pa = g.invest_pa + pyr.invest_pa
    l.invest = g.invest + pyr.invest
    l.cost_wage = g.cost_wage + pyr.cost_wage
    l.demand_emplo = g.demand_emplo + pyr.demand_emplo
    l.demand_emplo_new = g.demand_emplo_new + pyr.demand_emplo_new
