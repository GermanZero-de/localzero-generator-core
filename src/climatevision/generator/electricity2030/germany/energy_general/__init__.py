# pyright: strict

from dataclasses import dataclass

from ....refdata import Facts, Assumptions

from ...core.g_grid_offshore import GGridOffshore
from ...core.g_grid_onshore_or_pv import GGridOnshoreOrPV
from ...core.g import G


@dataclass(kw_only=True)
class General:
    g: G
    g_grid_offshore: GGridOffshore
    g_grid_onshore: GGridOnshoreOrPV
    g_grid_pv: GGridOnshoreOrPV


def calc_general(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    wind_offshore_power_to_be_installed: float,
    wind_onshore_power_to_be_installed: float,
    pv_power_to_be_installed: float,
) -> General:
    ass = assumptions.ass

    g_grid_offshore = GGridOffshore.calc_germany(
        facts,
        assumptions,
        duration_until_target_year,
        wind_offshore_power_to_be_installed,
    )

    g_grid_onshore = GGridOnshoreOrPV.calc(
        facts,
        duration_until_target_year,
        wind_onshore_power_to_be_installed,
        invest_per_x=ass("Ass_E_G_grid_onshore_ratio_invest_to_power"),
        mro=ass("Ass_E_G_grid_onshore_mro"),
    )

    g_grid_pv = GGridOnshoreOrPV.calc(
        facts,
        duration_until_target_year,
        pv_power_to_be_installed,
        invest_per_x=ass("Ass_E_G_grid_pv_ratio_invest_to_power"),
        mro=ass("Ass_E_G_grid_pv_mro"),
    )

    g = G.sum(g_grid_offshore, g_grid_onshore, g_grid_pv)

    return General(
        g=g,
        g_grid_offshore=g_grid_offshore,
        g_grid_onshore=g_grid_onshore,
        g_grid_pv=g_grid_pv,
    )
