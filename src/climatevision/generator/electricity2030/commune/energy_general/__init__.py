# pyright: strict

from dataclasses import dataclass

from ....refdata import Facts, Assumptions

from ...core.g_grid_offshore import GGridOffshore
from ...core.g_grid_onshore import GGridOnshore
from ...core.g_grid_pv import GGridPV
from ...core.g import G


@dataclass(kw_only=True)
class General:
    g: G
    g_grid_offshore: GGridOffshore
    g_grid_onshore: GGridOnshore
    g_grid_pv: GGridPV


def calc_general(
    facts: Facts,
    assumptions: Assumptions,
    duration_until_target_year: int,
    p_renew_wind_offshore_power_to_be_installed: float,
    p_local_wind_onshore_power_to_be_installed: float,
    p_local_pv_power_to_be_installed: float,
    d_energy: float,
) -> General:
    g_grid_offshore = GGridOffshore.calc_commune(
        facts,
        assumptions,
        duration_until_target_year,
        p_renew_wind_offshore_power_to_be_installed,
        d_energy,
    )

    g_grid_onshore = GGridOnshore.calc(
        facts,
        assumptions,
        duration_until_target_year,
        p_local_wind_onshore_power_to_be_installed,
    )

    g_grid_pv = GGridPV.calc(
        facts, assumptions, duration_until_target_year, p_local_pv_power_to_be_installed
    )

    g = G.sum(g_grid_offshore, g_grid_onshore, g_grid_pv)

    return General(
        g=g,
        g_grid_offshore=g_grid_offshore,
        g_grid_onshore=g_grid_onshore,
        g_grid_pv=g_grid_pv,
    )
