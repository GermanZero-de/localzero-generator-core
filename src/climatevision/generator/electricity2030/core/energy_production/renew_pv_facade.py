# pyright: strict

from ....refdata import Assumptions
from ....utils import div, MILLION
from ....electricity2018.e18 import E18

from ...core.e_col_vars_2030 import EColVars2030


def calc_production_renew_pv_facade(
    assumptions: Assumptions,
    *,
    e18: E18,
    p_local_pv_facade_full_load_hour: float,
    energy: float,
):
    ass = assumptions.ass

    p_renew_pv_facade = EColVars2030()
    p_renew_pv_facade.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / p_local_pv_facade_full_load_hour
        * 1000
    )
    p_renew_pv_facade.energy = energy
    p_renew_pv_facade.cost_mro = (
        p_renew_pv_facade.energy * p_renew_pv_facade.cost_mro_per_MWh / MILLION
    )
    p_renew_pv_facade.change_energy_MWh = (
        p_renew_pv_facade.energy - e18.p_renew_pv_facade.energy
    )
    p_renew_pv_facade.change_cost_mro = (
        p_renew_pv_facade.cost_mro - e18.p_renew_pv_facade.cost_mro
    )
    p_renew_pv_facade.change_energy_pct = div(
        p_renew_pv_facade.change_energy_MWh, e18.p_renew_pv_facade.energy
    )
    p_renew_pv_facade.change_CO2e_t = 0
    p_renew_pv_facade.change_CO2e_pct = 0
    p_renew_pv_facade.cost_climate_saved = 0

    return p_renew_pv_facade
