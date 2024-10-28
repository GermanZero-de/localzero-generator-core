# pyright: strict

from ....makeentries import Entries
from ....refdata import Assumptions
from ....utils import MILLION, div
from ....business2018.b18 import B18
from ....electricity2018.e18 import E18
from ....residences2018.r18 import R18

from ..e_col_vars_2030 import EColVars2030


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

    full_load_hour = entries.e_pv_full_load_hours_sta
    power_installed = entries.e_PV_power_inst_roof
    invest_per_x = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2030") * 1000
    )
    pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    power_to_be_installed_pct = entries.e_PV_power_to_be_inst_roof
    area_ha_available = (
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
    area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_roof_potential"
    )
    ratio_power_to_area_ha = ass(
        "Ass_E_P_local_pv_roof_ratio_power_to_area_ha"
    )
    power_installable = (
        area_ha_available
        * area_ha_available_pct_of_action
        * ratio_power_to_area_ha
    )
    power_to_be_installed = max(
        0,
        power_installable * power_to_be_installed_pct
        - power_installed,
    )
    energy_installable = (
        power_installable
        * full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2030")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / full_load_hour
        * 1000
    )
    energy = (
        (power_to_be_installed + power_installed)
        * full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    invest = (
        power_to_be_installed * invest_per_x
    )
    cost_mro = (
        energy * cost_mro_per_MWh / MILLION
    )
    invest_pa = invest / duration_until_target_year
    invest_com = div(
        invest
        * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2),
        b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2,
    )
    change_cost_mro = (
        cost_mro - e18.p_local_pv_roof.cost_mro
    )
    cost_wage = invest_pa * pct_of_wage
    invest_pa_com = (
        invest_com / duration_until_target_year
    )
    change_CO2e_t = 0
    cost_climate_saved = 0
    CO2e_total = 0
    change_CO2e_pct = 0

    cost_fuel_per_MWh = None
    cost_fuel = None
    pet_sites = None
    CO2e_combustion_based_per_MWh = None
    CO2e_combustion_based = None
    CO2e_total_2021_estimated = None
    demand_electricity = None
    demand_emplo = None
    demand_emplo_com = None
    change_cost_energy = None
    invest_outside = None
    invest_pa_outside = None
    pct_x = None
    emplo_existing = None
    demand_emplo_new = None

    p_local_pv_roof = EColVars2030(
        cost_fuel_per_MWh=cost_fuel_per_MWh, # type: ignore
        cost_fuel=cost_fuel, # type: ignore
        pet_sites=pet_sites, # type: ignore
        energy_installable=energy_installable,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh, # type: ignore
        CO2e_combustion_based=CO2e_combustion_based, # type: ignore
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        CO2e_total_2021_estimated=CO2e_total_2021_estimated, # type: ignore
        demand_electricity=demand_electricity, # type: ignore
        demand_emplo=demand_emplo, # type: ignore
        demand_emplo_com=demand_emplo_com, # type: ignore
        power_installed=power_installed,
        power_to_be_installed_pct=power_to_be_installed_pct,
        power_to_be_installed=power_to_be_installed,
        power_installable=power_installable,
        area_ha_available=area_ha_available,
        area_ha_available_pct_of_action=area_ha_available_pct_of_action,
        ratio_power_to_area_ha=ratio_power_to_area_ha,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_energy=change_cost_energy, # type: ignore
        change_cost_mro=change_cost_mro,
        invest=invest,
        invest_pa=invest_pa,
        invest_com=invest_com,
        invest_pa_com=invest_pa_com,
        invest_outside=invest_outside, # type: ignore
        invest_pa_outside=invest_pa_outside, # type: ignore
        invest_per_x=invest_per_x,
        pct_of_wage=pct_of_wage,
        pct_x=pct_x, # type: ignore
        ratio_wage_to_emplo=ratio_wage_to_emplo,
        cost_wage=cost_wage,
        cost_mro_per_MWh=cost_mro_per_MWh,
        emplo_existing=emplo_existing, # type: ignore
        demand_emplo_new=demand_emplo_new, # type: ignore
        full_load_hour=full_load_hour,
        )
        
    p_local_pv_roof.change_energy_MWh = (
        energy - e18.p_local_pv_roof.energy
    )

    p_local_pv_roof.change_energy_pct = div(
        p_local_pv_roof.change_energy_MWh, e18.p_local_pv_roof.energy
    )

    p_local_pv_roof.energy = energy

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

    full_load_hour = ass("Ass_E_P_local_pv_facade_full_load_hours")

    power_installed = entries.e_PV_power_inst_facade
    cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / ass("Ass_E_P_local_pv_facade_full_load_hours")
        * 1000
    )
    invest_per_x = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power") * 1000
    )
    pct_of_wage = ass("Ass_E_P_pv_invest_pct_of_wage")
    ratio_wage_to_emplo = ass(
        "Ass_E_P_constr_elec_ratio_wage_to_emplo_2017"
    )
    power_to_be_installed_pct = entries.e_PV_power_to_be_inst_facade
    ratio_power_to_area_ha = ass(
        "Ass_E_P_local_pv_facade_ratio_power_to_area_ha"
    )
    area_ha_available = (
        ass("Ass_E_P_lcoal_pv_facade_potential")
        * entries.r_buildings_com
        / entries.r_buildings_nat
    )
    area_ha_available_pct_of_action = ass(
        "Ass_E_P_local_pv_facade_potential_usable"
    )
    power_installable = (
        ratio_power_to_area_ha
        * area_ha_available
        * area_ha_available_pct_of_action
    )
    power_to_be_installed = max(
        0,
        power_installable
        * power_to_be_installed_pct
        - power_installed,
    )
    energy_installable = (
        full_load_hour
        * power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    energy = (
        (power_to_be_installed + power_installed)
        * full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    invest = (
        power_to_be_installed * invest_per_x
    )
    cost_mro = (
        energy * cost_mro_per_MWh / MILLION
    )
    invest_pa = invest / duration_until_target_year
    invest_com = div(
        invest
        * (r18.p_buildings_area_m2_com.area_m2 + b18.p_nonresi_com.area_m2),
        b18.p_nonresi.area_m2 + r18.p_buildings_total.area_m2,
    )
    change_cost_mro = (
        cost_mro - e18.p_local_pv_facade.cost_mro
    )
    cost_wage = (
        invest_pa * pct_of_wage
    )
    invest_pa_com = (
        invest_com / duration_until_target_year
    )
    demand_emplo = div(
        cost_wage, ratio_wage_to_emplo
    )
    change_CO2e_t = 0
    cost_climate_saved = 0
    CO2e_total = 0
    change_CO2e_pct = 0

    cost_fuel_per_MWh = None
    cost_fuel = None
    pet_sites = None
    CO2e_combustion_based_per_MWh = None
    CO2e_combustion_based = None
    CO2e_total_2021_estimated = None
    demand_electricity = None
    demand_emplo_com = None
    change_cost_energy = None
    invest_outside = None
    invest_pa_outside = None
    pct_x = None
    emplo_existing = None
    demand_emplo_new = None

    p_local_pv_facade = EColVars2030(
        cost_fuel_per_MWh=cost_fuel_per_MWh, # type: ignore
        cost_fuel=cost_fuel, # type: ignore
        pet_sites=pet_sites, # type: ignore
        energy_installable=energy_installable,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh, # type: ignore
        CO2e_combustion_based=CO2e_combustion_based, # type: ignore
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        CO2e_total_2021_estimated=CO2e_total_2021_estimated, # type: ignore
        demand_electricity=demand_electricity, # type: ignore
        demand_emplo=demand_emplo,
        demand_emplo_com=demand_emplo_com, # type: ignore
        power_installed=power_installed,
        power_to_be_installed_pct=power_to_be_installed_pct,
        power_to_be_installed=power_to_be_installed,
        power_installable=power_installable,
        area_ha_available=area_ha_available,
        area_ha_available_pct_of_action=area_ha_available_pct_of_action,
        ratio_power_to_area_ha=ratio_power_to_area_ha,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_energy=change_cost_energy, # type: ignore
        change_cost_mro=change_cost_mro,
        invest=invest,
        invest_pa=invest_pa,
        invest_com=invest_com,
        invest_pa_com=invest_pa_com,
        invest_outside=invest_outside, # type: ignore
        invest_pa_outside=invest_pa_outside, # type: ignore
        invest_per_x=invest_per_x,
        pct_of_wage=pct_of_wage,
        pct_x=pct_x, # type: ignore
        ratio_wage_to_emplo=ratio_wage_to_emplo,
        cost_wage=cost_wage,
        cost_mro_per_MWh=cost_mro_per_MWh,
        emplo_existing=emplo_existing, # type: ignore
        demand_emplo_new=demand_emplo_new, # type: ignore
        full_load_hour=full_load_hour,
        )
        
    p_local_pv_facade.change_energy_MWh = (
        energy - e18.p_local_pv_facade.energy
    )

    p_local_pv_facade.change_energy_pct = div(
        p_local_pv_facade.change_energy_MWh, e18.p_local_pv_facade.energy
    )

    p_local_pv_facade.energy = energy

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
