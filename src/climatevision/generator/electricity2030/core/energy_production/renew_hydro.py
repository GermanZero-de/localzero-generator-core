# pyright: strict

from ....refdata import Facts, Assumptions
from ....utils import div, MILLION
from ....electricity2018.e18 import E18

from ..e_col_vars_2030 import EColVars2030


def calc_production_renew_hydro(
    facts: Facts,
    assumptions: Assumptions,
    *,
    e18: E18,
    energy: float,
):
    fact = facts.fact
    ass = assumptions.ass

    p_renew_hydro = EColVars2030()
    p_renew_hydro.CO2e_total = 0
    p_renew_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")
    p_renew_hydro.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )

    p_renew_hydro.energy = energy

    p_renew_hydro.cost_mro = (
        p_renew_hydro.energy * p_renew_hydro.cost_mro_per_MWh / MILLION
    )
    p_renew_hydro.CO2e_combustion_based = (
        p_renew_hydro.energy * p_renew_hydro.CO2e_combustion_based_per_MWh
    )
    p_renew_hydro.change_energy_MWh = p_renew_hydro.energy - e18.p_renew_hydro.energy
    p_renew_hydro.change_cost_mro = p_renew_hydro.cost_mro - e18.p_renew_hydro.cost_mro
    p_renew_hydro.change_energy_pct = div(
        p_renew_hydro.change_energy_MWh, e18.p_renew_hydro.energy
    )
    p_renew_hydro.cost_climate_saved = 0
    p_renew_hydro.change_CO2e_t = 0
    p_renew_hydro.change_CO2e_pct = 0
    p_renew_hydro.cost_climate_saved = 0

    return p_renew_hydro
