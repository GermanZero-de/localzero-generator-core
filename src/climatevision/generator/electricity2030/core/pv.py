# pyright: strict

from ...makeentries import Entries
from ...refdata import Assumptions
from ...utils import MILLION, div
from ...business2018.b18 import B18
from ...electricity2018.e18 import E18
from ...residences2018.r18 import R18

from .e_col_vars_2030 import EColVars2030


def calc_production_local_pv_roof(
    entries: Entries,
    assumptions: Assumptions,
    *,
    e18: E18,
    b18: B18,
    r18: R18,
):
    ass = assumptions.ass

    duration_until_target_year = entries.m_duration_target

    # TODO: Change the below
    p_local_pv_roof = EColVars2030()

    p_local_pv_roof.full_load_hour = entries.e_pv_full_load_hours_sta
    p_local_pv_roof.power_installed = entries.e_PV_power_inst_roof
    p_local_pv_roof.invest_per_x = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2030") * 1000
    )
    p_local_pv_roof.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_roof.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_roof.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_roof
    p_local_pv_roof.area_ha_available = (
        (4 / 3)
        * (
            (
                entries.r_area_m2_1flat
                / 100
                * ass("Ass_E_P_local_pv_roof_area_building1")
                + entries.r_area_m2_2flat
                / 100
                * ass("Ass_E_P_local_pv_roof_area_building2")
                + entries.r_area_m2_3flat
                / 100
                * ass("Ass_E_P_local_pv_roof_area_buildingD")
                + entries.r_area_m2_dorm
                / 100
                * ass("Ass_E_P_local_pv_roof_area_buildingD")
            )
        )
        / 10000
    )
    p_local_pv_roof.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_roof_potential"
    )
    p_local_pv_roof.ratio_power_to_area_ha = ass(
        "Ass_E_P_local_pv_roof_ratio_power_to_area_ha"
    )
    p_local_pv_roof.power_installable = (
        p_local_pv_roof.area_ha_available
        * p_local_pv_roof.area_ha_available_pct_of_action
        * p_local_pv_roof.ratio_power_to_area_ha
    )
    p_local_pv_roof.power_to_be_installed = max(
        0,
        p_local_pv_roof.power_installable * p_local_pv_roof.power_to_be_installed_pct
        - p_local_pv_roof.power_installed,
    )
    p_local_pv_roof.energy_installable = (
        p_local_pv_roof.power_installable
        * p_local_pv_roof.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_roof.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / p_local_pv_roof.full_load_hour
        * 1000
    )
    p_local_pv_roof.energy = (
        (p_local_pv_roof.power_to_be_installed + p_local_pv_roof.power_installed)
        * p_local_pv_roof.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_roof.invest = (
        p_local_pv_roof.power_to_be_installed * p_local_pv_roof.invest_per_x
    )
    p_local_pv_roof.cost_mro = (
        p_local_pv_roof.energy * p_local_pv_roof.cost_mro_per_MWh / MILLION
    )
    p_local_pv_roof.change_energy_MWh = (
        p_local_pv_roof.energy - e18.p_local_pv_roof.energy
    )
    p_local_pv_roof.invest_pa = p_local_pv_roof.invest / duration_until_target_year
    p_local_pv_roof.invest_com = div(
        p_local_pv_roof.invest
        * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2),
        b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2,
    )
    p_local_pv_roof.change_cost_mro = (
        p_local_pv_roof.cost_mro - e18.p_local_pv_roof.cost_mro
    )
    p_local_pv_roof.change_energy_pct = div(
        p_local_pv_roof.change_energy_MWh, e18.p_local_pv_roof.energy
    )
    p_local_pv_roof.cost_wage = p_local_pv_roof.invest_pa * p_local_pv_roof.pct_of_wage
    p_local_pv_roof.invest_pa_com = (
        p_local_pv_roof.invest_com / duration_until_target_year
    )
    p_local_pv_roof.change_CO2e_t = 0
    p_local_pv_roof.cost_climate_saved = 0
    p_local_pv_roof.CO2e_total = 0
    p_local_pv_roof.change_CO2e_pct = 0

    return p_local_pv_roof


def calc_production_local_pv_facade(
    entries: Entries,
    assumptions: Assumptions,
    *,
    e18: E18,
    b18: B18,
    r18: R18,
):
    ass = assumptions.ass

    duration_until_target_year = entries.m_duration_target

    # TODO: Change the below
    p_local_pv_facade = EColVars2030()
    p_local_pv_facade.full_load_hour = ass("Ass_E_P_local_pv_facade_full_load_hours")

    p_local_pv_facade.power_installed = entries.e_PV_power_inst_facade
    p_local_pv_facade.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / ass("Ass_E_P_local_pv_facade_full_load_hours")
        * 1000
    )
    p_local_pv_facade.invest_per_x = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power") * 1000
    )
    p_local_pv_facade.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_facade.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_facade.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_facade
    p_local_pv_facade.ratio_power_to_area_ha = ass(
        "Ass_E_P_local_pv_facade_ratio_power_to_area_ha"
    )
    p_local_pv_facade.area_ha_available = (
        ass("Ass_E_P_lcoal_pv_facade_potential")
        * entries.r_buildings_com
        / entries.r_buildings_nat
    )
    p_local_pv_facade.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_facade_potential_usable"
    )
    p_local_pv_facade.power_installable = (
        p_local_pv_facade.ratio_power_to_area_ha
        * p_local_pv_facade.area_ha_available
        * p_local_pv_facade.area_ha_available_pct_of_action
    )
    p_local_pv_facade.power_to_be_installed = max(
        0,
        p_local_pv_facade.power_installable
        * p_local_pv_facade.power_to_be_installed_pct
        - p_local_pv_facade.power_installed,
    )
    p_local_pv_facade.energy_installable = (
        p_local_pv_facade.full_load_hour
        * p_local_pv_facade.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_facade.energy = (
        (p_local_pv_facade.power_to_be_installed + p_local_pv_facade.power_installed)
        * p_local_pv_facade.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_facade.invest = (
        p_local_pv_facade.power_to_be_installed * p_local_pv_facade.invest_per_x
    )
    p_local_pv_facade.cost_mro = (
        p_local_pv_facade.energy * p_local_pv_facade.cost_mro_per_MWh / MILLION
    )
    p_local_pv_facade.change_energy_MWh = (
        p_local_pv_facade.energy - e18.p_local_pv_facade.energy
    )
    p_local_pv_facade.invest_pa = p_local_pv_facade.invest / duration_until_target_year
    p_local_pv_facade.invest_com = div(
        p_local_pv_facade.invest
        * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2),
        b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2,
    )
    p_local_pv_facade.change_cost_mro = (
        p_local_pv_facade.cost_mro - e18.p_local_pv_facade.cost_mro
    )
    p_local_pv_facade.change_energy_pct = div(
        p_local_pv_facade.change_energy_MWh, e18.p_local_pv_facade.energy
    )
    p_local_pv_facade.cost_wage = (
        p_local_pv_facade.invest_pa * p_local_pv_facade.pct_of_wage
    )
    p_local_pv_facade.invest_pa_com = (
        p_local_pv_facade.invest_com / duration_until_target_year
    )
    p_local_pv_facade.demand_emplo = div(
        p_local_pv_facade.cost_wage, p_local_pv_facade.ratio_wage_to_emplo
    )
    p_local_pv_facade.change_CO2e_t = 0
    p_local_pv_facade.cost_climate_saved = 0
    p_local_pv_facade.CO2e_total = 0
    p_local_pv_facade.change_CO2e_pct = 0
    return p_local_pv_facade


def calc_production_local_pv_agri(
    entries: Entries,
    assumptions: Assumptions,
    *,
    e18: E18,
    local_pv_roof_full_load_hour: float,
    local_pv_park_full_load_hour: float,
):
    ass = assumptions.ass

    duration_until_target_year = entries.m_duration_target

    # TODO: Change the below
    p_local_pv_agri = EColVars2030()
    p_local_pv_agri.power_installed = entries.e_PV_power_inst_agripv
    p_local_pv_agri.invest_per_x = (
        ass("Ass_E_P_local_pv_agri_ratio_invest_to_power") * 1000
    )
    p_local_pv_agri.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_agri.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_agri.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_agri
    p_local_pv_agri.ratio_power_to_area_ha = ass("Ass_E_P_local_pv_agri_power_per_ha")
    p_local_pv_agri.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_agri_power_installable"
    ) / (ass("Ass_E_P_local_pv_agri_power_per_ha") * entries.m_area_agri_nat)
    p_local_pv_agri.area_ha_available = entries.m_area_agri_com
    p_local_pv_agri.full_load_hour = local_pv_roof_full_load_hour  # WHAT?
    p_local_pv_agri.power_installable = (
        p_local_pv_agri.ratio_power_to_area_ha
        * p_local_pv_agri.area_ha_available_pct_of_action
        * p_local_pv_agri.area_ha_available
    )
    p_local_pv_agri.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_agri_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_agri_mro_per_year")
        / local_pv_park_full_load_hour  # AGAIN WHAT ?
        * 1000
    )
    p_local_pv_agri.power_to_be_installed = max(
        0,
        p_local_pv_agri.power_installable * p_local_pv_agri.power_to_be_installed_pct
        - p_local_pv_agri.power_installed,
    )
    p_local_pv_agri.energy_installable = (
        p_local_pv_agri.full_load_hour
        * p_local_pv_agri.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_agri.energy = (
        (p_local_pv_agri.power_to_be_installed + p_local_pv_agri.power_installed)
        * p_local_pv_agri.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_agri.invest = (
        p_local_pv_agri.power_to_be_installed * p_local_pv_agri.invest_per_x
    )
    p_local_pv_agri.cost_mro = (
        p_local_pv_agri.energy * p_local_pv_agri.cost_mro_per_MWh / MILLION
    )
    p_local_pv_agri.change_energy_MWh = (
        p_local_pv_agri.energy - e18.p_local_pv_agri.energy
    )
    p_local_pv_agri.invest_pa = p_local_pv_agri.invest / duration_until_target_year
    p_local_pv_agri.change_cost_mro = (
        p_local_pv_agri.cost_mro - e18.p_local_pv_agri.cost_mro
    )
    p_local_pv_agri.change_energy_pct = div(
        p_local_pv_agri.change_energy_MWh, e18.p_local_pv_agri.energy
    )
    p_local_pv_agri.cost_wage = p_local_pv_agri.invest_pa * p_local_pv_agri.pct_of_wage
    p_local_pv_agri.change_CO2e_t = 0
    p_local_pv_agri.CO2e_total = 0
    p_local_pv_agri.change_CO2e_pct = 0
    p_local_pv_agri.cost_climate_saved = 0
    p_local_pv_agri.cost_climate_saved = 0
    return p_local_pv_agri


def calc_production_local_pv_park(
    entries: Entries,
    assumptions: Assumptions,
    *,
    e18: E18,
    local_pv_roof_full_load_hour: float,
):
    ass = assumptions.ass

    duration_until_target_year = entries.m_duration_target

    # TODO: Change the below
    p_local_pv_park = EColVars2030()

    p_local_pv_park.power_installed = entries.e_PV_power_inst_park
    p_local_pv_park.invest_per_x = (
        ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2030") * 1000
    )
    p_local_pv_park.pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    p_local_pv_park.ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    p_local_pv_park.power_to_be_installed_pct = entries.e_PV_power_to_be_inst_park
    p_local_pv_park.ratio_power_to_area_ha = ass("Ass_E_P_local_pv_park_power_per_ha")
    p_local_pv_park.area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_park_area_pct_of_available"
    )
    p_local_pv_park.area_ha_available = entries.m_area_total_com
    p_local_pv_park.power_installable = (
        p_local_pv_park.ratio_power_to_area_ha
        * p_local_pv_park.area_ha_available_pct_of_action
        * p_local_pv_park.area_ha_available
    )
    p_local_pv_park.full_load_hour = local_pv_roof_full_load_hour
    p_local_pv_park.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_pv_park_mro_per_year")
        / p_local_pv_park.full_load_hour
        * 1000
    )
    p_local_pv_park.power_to_be_installed = max(
        0,
        p_local_pv_park.power_installable * p_local_pv_park.power_to_be_installed_pct
        - p_local_pv_park.power_installed,
    )
    p_local_pv_park.energy_installable = (
        p_local_pv_park.full_load_hour
        * p_local_pv_park.power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_park.energy = (
        (p_local_pv_park.power_to_be_installed + p_local_pv_park.power_installed)
        * p_local_pv_park.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_park.invest = (
        p_local_pv_park.power_to_be_installed * p_local_pv_park.invest_per_x
    )
    p_local_pv_park.cost_mro = (
        p_local_pv_park.energy * p_local_pv_park.cost_mro_per_MWh / MILLION
    )
    p_local_pv_park.change_energy_MWh = (
        p_local_pv_park.energy - e18.p_local_pv_park.energy
    )
    p_local_pv_park.invest_pa = p_local_pv_park.invest / duration_until_target_year
    p_local_pv_park.change_cost_mro = (
        p_local_pv_park.cost_mro - e18.p_local_pv_park.cost_mro
    )
    p_local_pv_park.change_energy_pct = div(
        p_local_pv_park.change_energy_MWh, e18.p_local_pv_park.energy
    )
    p_local_pv_park.cost_wage = p_local_pv_park.invest_pa * p_local_pv_park.pct_of_wage
    p_local_pv_park.change_CO2e_t = 0
    p_local_pv_park.CO2e_total = 0
    p_local_pv_park.change_CO2e_pct = 0
    p_local_pv_park.cost_climate_saved = 0

    return p_local_pv_park
