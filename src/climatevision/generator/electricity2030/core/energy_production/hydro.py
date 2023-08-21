# pyright: strict

from ....makeentries import Entries
from ....refdata import Facts, Assumptions
from ....utils import MILLION
from ....electricity2018.e18 import E18

from ..e_col_vars_2030 import EColVars2030


def calc_production_local_hydro(
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    *,
    e18: E18,
):
    fact = facts.fact
    ass = assumptions.ass

    # TODO: Change the below
    p_local_hydro = EColVars2030()

    p_local_hydro.power_installed = entries.e_PV_power_inst_water
    p_local_hydro.full_load_hour = fact("Fact_E_P_hydro_full_load_hours")  # energy
    p_local_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")  # cost_mro
    p_local_hydro.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    p_local_hydro.energy = (
        p_local_hydro.power_installed
        * p_local_hydro.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_hydro.cost_mro = (
        p_local_hydro.energy * p_local_hydro.cost_mro_per_MWh / MILLION
    )
    p_local_hydro.CO2e_combustion_based = (
        p_local_hydro.energy * p_local_hydro.CO2e_combustion_based_per_MWh
    )
    p_local_hydro.CO2e_total = p_local_hydro.CO2e_combustion_based
    p_local_hydro.change_energy_MWh = p_local_hydro.energy - e18.p_local_hydro.energy
    p_local_hydro.change_CO2e_t = 0
    p_local_hydro.change_CO2e_pct = 0
    p_local_hydro.cost_climate_saved = 0

    return p_local_hydro
