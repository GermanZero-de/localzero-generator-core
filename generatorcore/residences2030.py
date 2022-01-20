from dataclasses import dataclass, asdict

from .electricity2018 import *
from .residences2018 import *
from .business2018 import *
from .setup import ass, entry, fact

# Definition der relevanten Spaltennamen für den Sektor R30


@dataclass
class RColVars2030:
    energy: float = None
    pct_energy: float = None
    pct_x: float = None
    area_m2: float = None
    pct_nonrehab: float = None
    pct_rehab: float = None
    pct_of_wage: float = None
    nonrehab: float = None
    area_m2_rehab: float = None
    area_m2_nonrehab: float = None
    area_ha_available: float = None
    area_ha_available_pct_of_action: float = None
    number_of_buildings_rehab: float = None
    demand_heat_nonrehab: float = None
    demand_heat_rehab: float = None
    demand_heat_rehab: float = None
    demand_heatnet: float = None
    demand_biomass: float = None
    demand_solarth: float = None
    demand_heatpump: float = None
    demand_emethan: float = None
    demand_emplo: float = None
    demand_emplo_new: float = None
    demand_change: float = None
    demand_electricity: float = None
    energy_installable: float = None
    cost_fuel: float = None
    cost_fuel_per_MWh: float = None
    cost_wage: float = None
    cost_climate_saved: float = None
    cost_mro: float = None
    ratio_wage_to_emplo: float = None
    CO2e_pb: float = None
    CO2e_cb: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_total: float = None
    CO2e_total_2021_estimated: float = None
    change_CO2e_t: float = None
    change_energy_MWh: float = None
    change_cost_energy: float = None
    change_energy_pct: float = None
    change_CO2e_pct: float = None
    rate_rehab_pa: float = None
    rate_rehab_pa: float = None
    invest: float = None
    invest_per_x: float = None
    invest_pa: float = None
    invest_com: float = None
    invest_pa_com: float = None
    power_installed: float = None
    power_to_be_installed: float = None
    power_to_be_installed_pct: float = None
    full_load_hour: float = None
    emplo_existing: float = None
    fec_factor_averaged: float = None
    action: float = None


@dataclass
class R30:
    # Klassenvariablen für Residences
    g: RColVars2030 = RColVars2030()
    g_consult: RColVars2030 = RColVars2030()
    p: RColVars2030 = RColVars2030()
    p_buildings_total: RColVars2030 = RColVars2030()
    p_buildings_until_1919: RColVars2030 = RColVars2030()
    p_buildings_1919_1948: RColVars2030 = RColVars2030()
    p_buildings_1949_1978: RColVars2030 = RColVars2030()
    p_buildings_1979_1995: RColVars2030 = RColVars2030()
    p_buildings_1996_2004: RColVars2030 = RColVars2030()
    p_buildings_2005_2011: RColVars2030 = RColVars2030()
    p_buildings_2011_today: RColVars2030 = RColVars2030()
    p_buildings_new: RColVars2030 = RColVars2030()
    p_buildings_area_m2_com: RColVars2030 = RColVars2030()
    r: RColVars2030 = RColVars2030()
    s: RColVars2030 = RColVars2030()
    s_fueloil: RColVars2030 = RColVars2030()
    s_lpg: RColVars2030 = RColVars2030()
    s_biomass: RColVars2030 = RColVars2030()
    s_coal: RColVars2030 = RColVars2030()
    s_petrol: RColVars2030 = RColVars2030()
    s_heatnet: RColVars2030 = RColVars2030()
    s_solarth: RColVars2030 = RColVars2030()
    s_heatpump: RColVars2030 = RColVars2030()
    s_gas: RColVars2030 = RColVars2030()
    s_elec_heating: RColVars2030 = RColVars2030()
    s_emethan: RColVars2030 = RColVars2030()
    s_elec: RColVars2030 = RColVars2030()
    r: RColVars2030 = RColVars2030()
    p_elec_elcon: RColVars2030 = RColVars2030()
    p_elec_heatpump: RColVars2030 = RColVars2030()
    p_other: RColVars2030 = RColVars2030()
    p_vehicles: RColVars2030 = RColVars2030()

    # erzeuge dictionary
    def dict(self):
        return asdict(self)


def Residence2030_calc(root: Generator):
    """"""
    """ import external values"""
    import json

    if entry("In_M_AGS_com") == "DG000000":
        excel_path = "excel/germany_values.json"
    elif entry("In_M_AGS_com") == "03159016":
        excel_path = "excel/goettingen_values.json"

    with open(excel_path, "r") as fp:
        exl = json.load(fp)
    fp.close()
    """end"""

    root.e30.p_local_pv_roof.area_ha_available = exl["e30"]["p_local_pv_roof"][
        "area_ha_available"
    ]
    root.b30.p_nonresi.demand_emplo = exl["b30"]["p_nonresi"]["demand_emplo"]
    root.b30.s_heatpump.demand_emplo = exl["b30"]["s_heatpump"]["demand_emplo"]
    root.b30.s_solarth.demand_emplo = exl["b30"]["s_solarth"]["demand_emplo"]
    root.b30.g_consult.demand_emplo = exl["b30"]["g_consult"]["demand_emplo"]
    root.a30.s_heatpump.demand_emplo = exl["a30"]["s_heatpump"]["demand_emplo"]
    #    root.a30.p_operation_heat.demand_emplo = exl['a30']['p_operation_heat']['demand_emplo']

    try:
        ### P - Section ###
        e30 = root.e30
        r30 = root.r30
        r18 = root.r18
        b30 = root.b30
        a30 = root.a30
        g = r30.g
        p = r30.p
        r = r30.r
        s = r30.s

        Kalkulationszeitraum = entry("In_M_duration_target")
        g_consult = r30.g_consult

        p_buildings_total = r30.p_buildings_total
        p_buildings_until_1919 = r30.p_buildings_until_1919
        p_buildings_1919_1948 = r30.p_buildings_1919_1948
        p_buildings_1949_1978 = r30.p_buildings_1949_1978
        p_buildings_1979_1995 = r30.p_buildings_1979_1995
        p_buildings_1996_2004 = r30.p_buildings_1996_2004
        p_buildings_2005_2011 = r30.p_buildings_2005_2011
        p_buildings_2011_today = r30.p_buildings_2011_today
        p_buildings_new = r30.p_buildings_new
        p_buildings_area_m2_com = r30.p_buildings_area_m2_com

        p_elec_elcon = r30.p_elec_elcon
        p_elec_heatpump = r30.p_elec_heatpump
        p_other = r30.p_other
        p_vehicles = r30.p_vehicles

        p_buildings_total.rate_rehab_pa = entry("In_R_rehab_rate_pa")

        p_buildings_until_1919.area_m2 = r18.p_buildings_until_1919.area_m2
        p_buildings_1919_1948.area_m2 = r18.p_buildings_1919_1948.area_m2
        p_buildings_1949_1978.area_m2 = r18.p_buildings_1949_1978.area_m2
        p_buildings_1979_1995.area_m2 = r18.p_buildings_1979_1995.area_m2
        p_buildings_1996_2004.area_m2 = r18.p_buildings_1996_2004.area_m2
        p_buildings_2005_2011.area_m2 = r18.p_buildings_2005_2011.area_m2
        p_buildings_2011_today.area_m2 = r18.p_buildings_2011_today.area_m2

        p_buildings_total.area_m2 = (
            p_buildings_until_1919.area_m2
            + p_buildings_1919_1948.area_m2
            + p_buildings_1949_1978.area_m2
            + p_buildings_1979_1995.area_m2
            + p_buildings_1996_2004.area_m2
        )  # SUM(p_buildings_until_1919.area_m2:p_buildings_1996_2004.area_m2)

        p_buildings_until_1919.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * r18.p_buildings_until_1919.relative_heat_ratio_buildings_until_2004
            * p_buildings_total.area_m2
            / p_buildings_until_1919.area_m2,
        )
        p_buildings_1919_1948.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * r18.p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004
            * p_buildings_total.area_m2
            / p_buildings_1919_1948.area_m2,
        )
        p_buildings_1919_1948.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * p_buildings_total.area_m2
            * r18.p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004
            / p_buildings_1919_1948.area_m2,
        )

        p_buildings_1949_1978.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * r18.p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004
            * p_buildings_total.area_m2
            / p_buildings_1949_1978.area_m2,
        )
        p_buildings_1949_1978.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * p_buildings_total.area_m2
            * r18.p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004
            / p_buildings_1949_1978.area_m2,
        )
        p_buildings_1979_1995.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * r18.p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004
            * p_buildings_total.area_m2
            / p_buildings_1979_1995.area_m2,
        )
        p_buildings_1996_2004.pct_rehab = min(
            1.0,
            fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
            + p_buildings_total.rate_rehab_pa
            * Kalkulationszeitraum
            * r18.p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004
            * p_buildings_total.area_m2
            / p_buildings_1996_2004.area_m2,
        )
        p_buildings_2005_2011.pct_nonrehab = 0
        p_buildings_2011_today.pct_nonrehab = 0
        p_buildings_2005_2011.pct_rehab = 1 - p_buildings_2005_2011.pct_nonrehab
        p_buildings_2011_today.pct_rehab = 1 - p_buildings_2011_today.pct_nonrehab

        p_buildings_new.pct_x = max(
            entry("In_M_population_com_203X") / entry("In_M_population_com_2018") - 1, 0
        )

        p_buildings_new.area_m2 = p_buildings_total.area_m2 * p_buildings_new.pct_x

        p_buildings_until_1919.area_m2_rehab = (
            p_buildings_until_1919.pct_rehab * p_buildings_until_1919.area_m2
        )
        p_buildings_1919_1948.area_m2_rehab = (
            p_buildings_1919_1948.pct_rehab * p_buildings_1919_1948.area_m2
        )
        p_buildings_1949_1978.area_m2_rehab = (
            p_buildings_1949_1978.pct_rehab * p_buildings_1949_1978.area_m2
        )
        p_buildings_1979_1995.area_m2_rehab = (
            p_buildings_1979_1995.pct_rehab * p_buildings_1979_1995.area_m2
        )
        p_buildings_1996_2004.area_m2_rehab = (
            p_buildings_1996_2004.pct_rehab * p_buildings_1996_2004.area_m2
        )
        p_buildings_2005_2011.area_m2_rehab = (
            p_buildings_2005_2011.pct_rehab * p_buildings_2005_2011.area_m2
        )
        p_buildings_2011_today.area_m2_rehab = (
            p_buildings_2011_today.pct_rehab * p_buildings_2011_today.area_m2
        )

        p_buildings_total.area_m2_rehab = (
            p_buildings_until_1919.area_m2_rehab
            + p_buildings_1919_1948.area_m2_rehab
            + p_buildings_1949_1978.area_m2_rehab
            + p_buildings_1979_1995.area_m2_rehab
            + p_buildings_1996_2004.area_m2_rehab
            + p_buildings_2005_2011.area_m2_rehab
            + p_buildings_2011_today.area_m2_rehab
        )

        p_buildings_area_m2_com.area_m2_rehab = (
            p_buildings_total.area_m2_rehab * r18.p_buildings_area_m2_com.pct_x
        )

        p_buildings_total.pct_rehab = (
            p_buildings_total.area_m2_rehab / r18.p_buildings_total.area_m2
        )

        p_buildings_total.pct_nonrehab = 1 - p_buildings_total.pct_rehab
        p_buildings_until_1919.pct_nonrehab = 1 - p_buildings_until_1919.pct_rehab
        p_buildings_1919_1948.pct_nonrehab = 1 - p_buildings_1919_1948.pct_rehab
        p_buildings_1949_1978.pct_nonrehab = 1 - p_buildings_1949_1978.pct_rehab
        p_buildings_1979_1995.pct_nonrehab = 1 - p_buildings_1979_1995.pct_rehab
        p_buildings_1996_2004.pct_nonrehab = 1 - p_buildings_1996_2004.pct_rehab

        p_buildings_until_1919.area_m2_nonrehab = (
            p_buildings_until_1919.pct_nonrehab * p_buildings_until_1919.area_m2
        )
        p_buildings_1919_1948.area_m2_nonrehab = (
            p_buildings_1919_1948.pct_nonrehab * p_buildings_1919_1948.area_m2
        )
        p_buildings_1949_1978.area_m2_nonrehab = (
            p_buildings_1949_1978.pct_nonrehab * p_buildings_1949_1978.area_m2
        )
        p_buildings_1979_1995.area_m2_nonrehab = (
            p_buildings_1979_1995.pct_nonrehab * p_buildings_1979_1995.area_m2
        )
        p_buildings_1996_2004.area_m2_nonrehab = (
            p_buildings_1996_2004.pct_nonrehab * p_buildings_1996_2004.area_m2
        )
        p_buildings_2005_2011.area_m2_nonrehab = (
            p_buildings_2005_2011.pct_nonrehab * p_buildings_2005_2011.area_m2
        )
        p_buildings_2011_today.area_m2_nonrehab = (
            p_buildings_2011_today.pct_nonrehab * p_buildings_2011_today.area_m2
        )

        p_buildings_total.area_m2_nonrehab = (
            p_buildings_until_1919.area_m2_nonrehab
            + p_buildings_1919_1948.area_m2_nonrehab
            + p_buildings_1949_1978.area_m2_nonrehab
            + p_buildings_1979_1995.area_m2_nonrehab
            + p_buildings_1996_2004.area_m2_nonrehab
            + p_buildings_2005_2011.area_m2_nonrehab
            + p_buildings_2011_today.area_m2_nonrehab
        )

        p_buildings_until_1919.demand_heat_nonrehab = (
            p_buildings_until_1919.area_m2_nonrehab
            * r18.p_buildings_until_1919.factor_adapted_to_fec
        )
        p_buildings_1919_1948.demand_heat_nonrehab = (
            p_buildings_1919_1948.area_m2_nonrehab
            * r18.p_buildings_1919_1948.factor_adapted_to_fec
        )
        p_buildings_1949_1978.demand_heat_nonrehab = (
            p_buildings_1949_1978.area_m2_nonrehab
            * r18.p_buildings_1949_1978.factor_adapted_to_fec
        )
        p_buildings_1979_1995.demand_heat_nonrehab = (
            p_buildings_1979_1995.area_m2_nonrehab
            * r18.p_buildings_1979_1995.factor_adapted_to_fec
        )
        p_buildings_1996_2004.demand_heat_nonrehab = (
            p_buildings_1996_2004.area_m2_nonrehab
            * r18.p_buildings_1996_2004.factor_adapted_to_fec
        )
        p_buildings_2005_2011.demand_heat_nonrehab = (
            p_buildings_2005_2011.area_m2_nonrehab
            * r18.p_buildings_2005_2011.fec_factor_BMWi
        )
        p_buildings_2011_today.demand_heat_nonrehab = (
            p_buildings_2011_today.area_m2_nonrehab
            * r18.p_buildings_2011_today.fec_factor_BMWi
        )
        p_buildings_total.demand_heat_nonrehab = (
            p_buildings_until_1919.demand_heat_nonrehab
            + p_buildings_1919_1948.demand_heat_nonrehab
            + p_buildings_1949_1978.demand_heat_nonrehab
            + p_buildings_1979_1995.demand_heat_nonrehab
            + p_buildings_1996_2004.demand_heat_nonrehab
            + p_buildings_2005_2011.demand_heat_nonrehab
            + p_buildings_2011_today.demand_heat_nonrehab
        )

        p_buildings_until_1919.demand_heat_rehab = (
            p_buildings_until_1919.area_m2_rehab
            * ass("Ass_R_P_heat_consumption_after_renovation_per_area")
        )
        p_buildings_1919_1948.demand_heat_rehab = (
            p_buildings_1919_1948.area_m2_rehab
            * ass("Ass_R_P_heat_consumption_after_renovation_per_area")
        )
        p_buildings_1949_1978.demand_heat_rehab = (
            p_buildings_1949_1978.area_m2_rehab
            * ass("Ass_R_P_heat_consumption_after_renovation_per_area")
        )
        p_buildings_1979_1995.demand_heat_rehab = (
            p_buildings_1979_1995.area_m2_rehab
            * ass("Ass_R_P_heat_consumption_after_renovation_per_area")
        )
        p_buildings_1996_2004.demand_heat_rehab = (
            p_buildings_1996_2004.area_m2_rehab
            * ass("Ass_R_P_heat_consumption_after_renovation_per_area")
        )
        p_buildings_2005_2011.demand_heat_rehab = (
            p_buildings_2005_2011.area_m2_rehab
            * r18.p_buildings_2005_2011.factor_adapted_to_fec
        )
        p_buildings_2011_today.demand_heat_rehab = (
            p_buildings_2011_today.area_m2_rehab
            * r18.p_buildings_2011_today.factor_adapted_to_fec
        )
        p_buildings_total.demand_heat_rehab = (
            p_buildings_until_1919.demand_heat_rehab
            + p_buildings_1919_1948.demand_heat_rehab
            + p_buildings_1949_1978.demand_heat_rehab
            + p_buildings_1979_1995.demand_heat_rehab
            + p_buildings_1996_2004.demand_heat_rehab
            + p_buildings_2005_2011.demand_heat_rehab
            + p_buildings_2011_today.demand_heat_rehab
        )

        p_buildings_until_1919.energy = (
            p_buildings_until_1919.demand_heat_nonrehab
            + p_buildings_until_1919.demand_heat_rehab
        )
        p_buildings_1919_1948.energy = (
            p_buildings_1919_1948.demand_heat_nonrehab
            + p_buildings_1919_1948.demand_heat_rehab
        )
        p_buildings_1949_1978.energy = (
            p_buildings_1949_1978.demand_heat_nonrehab
            + p_buildings_1949_1978.demand_heat_rehab
        )
        p_buildings_1979_1995.energy = (
            p_buildings_1979_1995.demand_heat_nonrehab
            + p_buildings_1979_1995.demand_heat_rehab
        )
        p_buildings_1996_2004.energy = (
            p_buildings_1996_2004.demand_heat_nonrehab
            + p_buildings_1996_2004.demand_heat_rehab
        )
        p_buildings_2005_2011.energy = (
            p_buildings_2005_2011.demand_heat_nonrehab
            + p_buildings_2005_2011.demand_heat_rehab
        )
        p_buildings_2011_today.energy = (
            p_buildings_2011_today.demand_heat_nonrehab
            + p_buildings_2011_today.demand_heat_rehab
        )

        p_buildings_total.fec_factor_averaged = (
            p_buildings_total.demand_heat_rehab + p_buildings_total.demand_heat_nonrehab
        ) / r18.p_buildings_total.area_m2
        p_buildings_until_1919.fec_factor_averaged = (
            p_buildings_until_1919.demand_heat_rehab
            + p_buildings_until_1919.demand_heat_nonrehab
        ) / p_buildings_until_1919.area_m2
        p_buildings_1919_1948.fec_factor_averaged = (
            p_buildings_1919_1948.demand_heat_rehab
            + p_buildings_1919_1948.demand_heat_nonrehab
        ) / p_buildings_1919_1948.area_m2
        p_buildings_1949_1978.fec_factor_averaged = (
            p_buildings_1949_1978.demand_heat_rehab
            + p_buildings_1949_1978.demand_heat_nonrehab
        ) / p_buildings_1949_1978.area_m2
        p_buildings_1979_1995.fec_factor_averaged = (
            p_buildings_1979_1995.demand_heat_rehab
            + p_buildings_1979_1995.demand_heat_nonrehab
        ) / p_buildings_1979_1995.area_m2
        p_buildings_1996_2004.fec_factor_averaged = (
            p_buildings_1996_2004.demand_heat_rehab
            + p_buildings_1996_2004.demand_heat_nonrehab
        ) / p_buildings_1996_2004.area_m2
        p_buildings_2005_2011.fec_factor_averaged = (
            p_buildings_2005_2011.demand_heat_rehab
            + p_buildings_2005_2011.demand_heat_nonrehab
        ) / p_buildings_2005_2011.area_m2
        p_buildings_2011_today.fec_factor_averaged = (
            p_buildings_2011_today.demand_heat_rehab
            + p_buildings_2011_today.demand_heat_nonrehab
        ) / p_buildings_2011_today.area_m2
        p_buildings_area_m2_com.fec_factor_averaged = (
            p_buildings_total.fec_factor_averaged
        )
        p_buildings_new.fec_factor_averaged = ass(
            "Ass_R_P_heat_consumption_new_building_2021"
        )

        p_buildings_area_m2_com.area_m2 = (
            p_buildings_total.area_m2 * r18.p_buildings_area_m2_com.pct_x
        )
        p_buildings_area_m2_com.energy = (
            p_buildings_area_m2_com.area_m2
            * p_buildings_area_m2_com.fec_factor_averaged
        )
        p_buildings_new.energy = (
            p_buildings_new.area_m2 * p_buildings_new.fec_factor_averaged
        )

        p_buildings_total.energy = (
            p_buildings_until_1919.energy
            + p_buildings_1919_1948.energy
            + p_buildings_1949_1978.energy
            + p_buildings_1979_1995.energy
            + p_buildings_1996_2004.energy
            + p_buildings_2005_2011.energy
            + p_buildings_2011_today.energy
        )  # SUM(p_buildings_until_1919.energy:p_buildings_2011_today.energy)

        p_elec_elcon.demand_change = ass("Ass_R_D_fec_elec_elcon_change")
        p_elec_elcon.energy = r18.p_elec_elcon.energy * (1 + p_elec_elcon.demand_change)
        p_elec_elcon.demand_electricity = p_elec_elcon.energy

        p_buildings_area_m2_com.pct_x = r18.p_buildings_area_m2_com.pct_x

        p_buildings_until_1919.pct_nonrehab = 1 - p_buildings_until_1919.pct_rehab
        p_buildings_1919_1948.pct_nonrehab = 1 - p_buildings_1919_1948.pct_rehab
        p_buildings_1949_1978.pct_nonrehab = 1 - p_buildings_1949_1978.pct_rehab
        p_buildings_1979_1995.pct_nonrehab = 1 - p_buildings_1979_1995.pct_rehab
        p_buildings_1996_2004.pct_nonrehab = 1 - p_buildings_1996_2004.pct_rehab

        p_buildings_total.number_of_buildings_rehab = (
            p_buildings_total.pct_rehab * r18.p_buildings_total.number_of_buildings
        )
        p_buildings_until_1919.number_of_buildings_rehab = (
            p_buildings_until_1919.pct_rehab
            * r18.p_buildings_until_1919.number_of_buildings
        )
        p_buildings_1919_1948.number_of_buildings_rehab = (
            p_buildings_1919_1948.pct_rehab
            * r18.p_buildings_1919_1948.number_of_buildings
        )
        p_buildings_1949_1978.number_of_buildings_rehab = (
            p_buildings_1949_1978.pct_rehab
            * r18.p_buildings_1949_1978.number_of_buildings
        )
        p_buildings_1979_1995.number_of_buildings_rehab = (
            p_buildings_1979_1995.pct_rehab
            * r18.p_buildings_1979_1995.number_of_buildings
        )
        p_buildings_1996_2004.number_of_buildings_rehab = (
            p_buildings_1996_2004.pct_rehab
            * r18.p_buildings_1996_2004.number_of_buildings
        )
        p_buildings_2005_2011.number_of_buildings_rehab = (
            p_buildings_2005_2011.pct_rehab
            * r18.p_buildings_2005_2011.number_of_buildings
        )
        p_buildings_2011_today.number_of_buildings_rehab = (
            p_buildings_2011_today.pct_rehab
            * r18.p_buildings_2011_today.number_of_buildings
        )
        p_buildings_area_m2_com.number_of_buildings_rehab = (
            r18.p_buildings_area_m2_com.pct_x
            * p_buildings_total.number_of_buildings_rehab
        )

        p_buildings_until_1919.rate_rehab_pa = (
            p_buildings_until_1919.pct_rehab
            - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
        ) / Kalkulationszeitraum
        p_buildings_1919_1948.rate_rehab_pa = (
            p_buildings_1919_1948.pct_rehab
            - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
        ) / Kalkulationszeitraum
        p_buildings_1949_1978.rate_rehab_pa = (
            p_buildings_1949_1978.pct_rehab
            - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
        ) / Kalkulationszeitraum
        p_buildings_1979_1995.rate_rehab_pa = (
            p_buildings_1979_1995.pct_rehab
            - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
        ) / Kalkulationszeitraum
        p_buildings_1996_2004.rate_rehab_pa = (
            p_buildings_1996_2004.pct_rehab
            - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021")
        ) / Kalkulationszeitraum

        ### S - Section ###

        Million = 1000000

        # Definitions
        b18 = root.b18
        e18 = root.e18
        s = r30.s

        s_fueloil = root.r30.s_fueloil
        s_lpg = root.r30.s_lpg
        s_biomass = root.r30.s_biomass
        s_coal = root.r30.s_coal
        s_petrol = root.r30.s_petrol
        s_heatnet = root.r30.s_heatnet
        s_solarth = root.r30.s_solarth
        s_heatpump = root.r30.s_heatpump
        s_elec_heating = root.r30.s_elec_heating
        s_gas = root.r30.s_gas
        s_emethan = root.r30.s_emethan
        s_elec = root.r30.s_elec

        # pct_energy
        s_fueloil.pct_energy = 0

        s_lpg.pct_energy = 0

        s_biomass.energy = (
            r18.s_biomass.number_of_buildings
            * p_buildings_total.fec_factor_averaged
            * r18.p_buildings_total.area_m2
            / r18.p_buildings_total.number_of_buildings
        )

        s_coal.pct_energy = 0

        s_petrol.pct_energy = 0

        s_heatnet.energy = (
            entry("In_R_heatnet_ratio_year_target")
            * p_buildings_total.fec_factor_averaged
            * r18.p_buildings_total.area_m2
        )
        s_gas.energy = 0

        # formula from e30 not still calc here
        e30.p_local_pv_roof.area_ha_available = (
            (4 / 3)
            * (
                (
                    entry("In_R_area_m2_1flat")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_building1")
                    + entry("In_R_area_m2_2flat")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_building2")
                    + entry("In_R_area_m2_3flat")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_building3")
                    + entry("In_R_area_m2_dorm")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_buildingD")
                )
            )
            / 10000
        )
        s_solarth.area_ha_available = e30.p_local_pv_roof.area_ha_available
        s_solarth.area_ha_available_pct_of_action = ass(
            "Ass_E_P_local_pv_roof_potential"
        )
        s_solarth.energy_installable = (
            s_solarth.area_ha_available
            * s_solarth.area_ha_available_pct_of_action
            * ass("Ass_R_P_soltherm_specific_yield_per_sqm")
            * 10000
        )
        s_solarth.power_to_be_installed_pct = entry("In_H_solartherm_to_be_inst")
        s_solarth.energy = max(
            r18.p_buildings_total.number_of_buildings
            / (
                r18.p_buildings_total.number_of_buildings
                + b18.p_nonresi.number_of_buildings
            )
            * s_solarth.energy_installable
            * s_solarth.power_to_be_installed_pct,
            r18.s_solarth.energy,
        )

        s_heatpump.energy = (
            p_buildings_total.demand_heat_rehab
            - (s_biomass.energy + s_heatnet.energy + s_solarth.energy)
            * p_buildings_total.pct_rehab
        )

        p_elec_heatpump.demand_electricity = s_heatpump.energy / fact(
            "Fact_R_S_heatpump_mean_annual_performance_factor_all"
        )
        p_elec_heatpump.energy = p_elec_heatpump.demand_electricity
        p_vehicles.demand_change = ass("Ass_R_D_fec_vehicles_change")
        p_vehicles.energy = r18.p_vehicles.energy * (1 + p_vehicles.demand_change)
        p_other.energy = (
            p_elec_heatpump.energy + p_elec_elcon.energy + p_vehicles.energy
        )
        p.energy = p_buildings_total.energy + p_other.energy
        p_other.demand_electricity = (
            p_elec_heatpump.demand_electricity + p_elec_elcon.demand_electricity
        )  # SUM(p_elec_heatpump.demand_electricity:p_elec_elcon.demand_electricity)

        p.demand_electricity = p_other.demand_electricity
        s_elec.energy = p.demand_electricity
        s.energy = p_buildings_total.energy + s_elec.energy
        s_fueloil.energy = s_fueloil.pct_energy * s.energy
        s_lpg.energy = s_lpg.pct_energy * s.energy
        s_biomass.pct_energy = s_biomass.energy / s.energy
        s_coal.energy = s_coal.pct_energy * s.energy
        s_petrol.energy = s_petrol.pct_energy * s.energy
        s_heatnet.pct_energy = s_heatnet.energy / s.energy
        s_solarth.pct_energy = s_solarth.energy / s.energy
        s_heatpump.pct_energy = s_heatpump.energy / s.energy

        sum_fueloil_to_heatpump_energy = (
            s_fueloil.energy
            + s_lpg.energy
            + s_biomass.energy
            + s_coal.energy
            + s_petrol.energy
            + s_heatnet.energy
            + s_solarth.energy
            + s_heatpump.energy
        )
        s_elec_heating.energy = 0
        s_emethan.energy = max(
            0, p_buildings_total.energy - sum_fueloil_to_heatpump_energy
        )

        s_emethan.pct_energy = s_emethan.energy / s.energy

        s_elec.pct_energy = s_elec.energy / s.energy

        s.pct_energy = (
            s_fueloil.pct_energy
            + s_lpg.pct_energy
            + s_biomass.pct_energy
            + s_coal.pct_energy
            + s_petrol.pct_energy
            + s_heatnet.pct_energy
            + s_solarth.pct_energy
            + s_heatpump.pct_energy
            + s_emethan.pct_energy
            + s_elec.pct_energy
        )  # SUM(s_fueloil.pct_energy:s_elec.pct_energy)

        s.demand_heat_nonrehab = p_buildings_total.demand_heat_nonrehab
        s.demand_heat_rehab = p_buildings_total.demand_heat_rehab

        s_fueloil.cost_fuel_per_MWh = ass("Ass_R_S_fueloil_energy_cost_factor_2035")
        s_lpg.cost_fuel_per_MWh = 0
        s_coal.cost_fuel_per_MWh = ass("Ass_R_S_coal_energy_cost_factor_2035")
        s_biomass.cost_fuel_per_MWh = 48  # €/MWh
        s_petrol.cost_fuel_per_MWh = 0
        s_heatnet.cost_fuel_per_MWh = 0
        s_solarth.cost_fuel_per_MWh = 0
        s_heatpump.cost_fuel_per_MWh = 0
        s_emethan.cost_fuel_per_MWh = ass("Ass_R_S_gas_energy_cost_factor_2035")

        s_fueloil.cost_fuel = s_fueloil.energy * s_fueloil.cost_fuel_per_MWh / Million
        s_lpg.cost_fuel = s_lpg.energy * s_lpg.cost_fuel_per_MWh / Million
        s_biomass.cost_fuel = s_biomass.energy * s_biomass.cost_fuel_per_MWh / Million
        s_coal.cost_fuel = s_coal.energy * s_coal.cost_fuel_per_MWh / Million
        s_petrol.cost_fuel = s_petrol.energy * s_petrol.cost_fuel_per_MWh / Million
        s_heatnet.cost_fuel = s_heatnet.energy * s_heatnet.cost_fuel_per_MWh / Million
        s_solarth.cost_fuel = s_solarth.energy * s_solarth.cost_fuel_per_MWh / Million
        s_heatpump.cost_fuel = (
            s_heatpump.energy * s_heatpump.cost_fuel_per_MWh / Million
        )
        s_emethan.cost_fuel = s_emethan.energy * s_emethan.cost_fuel_per_MWh / Million
        s.cost_fuel = (
            s_fueloil.cost_fuel
            + s_lpg.cost_fuel
            + s_biomass.cost_fuel
            + s_coal.cost_fuel
            + s_petrol.cost_fuel
            + s_heatnet.cost_fuel
            + s_solarth.cost_fuel
        )  # SUM(s_fueloil.cost_fuel:s_solarth.cost_fuel)

        s_fueloil.CO2e_cb_per_MWh = r18.s_fueloil.CO2e_cb_per_MWh
        s_lpg.CO2e_cb_per_MWh = 0
        s_biomass.CO2e_cb_per_MWh = r18.s_biomass.CO2e_cb_per_MWh
        s_coal.CO2e_cb_per_MWh = r18.s_coal.CO2e_cb_per_MWh
        s_petrol.CO2e_cb_per_MWh = r18.s_petrol.CO2e_cb_per_MWh
        s_heatnet.CO2e_cb_per_MWh = 0
        s_solarth.CO2e_cb_per_MWh = 0
        s_heatpump.CO2e_cb_per_MWh = 0
        s_gas.CO2e_cb_per_MWh = r18.s_gas.CO2e_cb_per_MWh

        s_emethan.CO2e_cb_per_MWh = fact("Fact_T_S_methan_EmFa_tank_wheel_2018")
        s_elec.CO2e_cb = 0
        s_fueloil.CO2e_cb = s_fueloil.energy * s_fueloil.CO2e_cb_per_MWh
        s_lpg.CO2e_cb = s_lpg.energy * s_lpg.CO2e_cb_per_MWh
        s_biomass.CO2e_cb = s_biomass.energy * s_biomass.CO2e_cb_per_MWh
        s_coal.CO2e_cb = s_coal.energy * s_coal.CO2e_cb_per_MWh
        s_petrol.CO2e_cb = s_petrol.energy * s_petrol.CO2e_cb_per_MWh
        s_heatnet.CO2e_cb = s_heatnet.energy * s_heatnet.CO2e_cb_per_MWh
        s_solarth.CO2e_cb = s_solarth.energy * s_solarth.CO2e_cb_per_MWh
        s_heatpump.CO2e_cb = s_heatpump.energy * s_heatpump.CO2e_cb_per_MWh
        s_gas.CO2e_cb = s_gas.energy * s_gas.CO2e_cb_per_MWh
        s_emethan.CO2e_cb = s_emethan.energy * s_emethan.CO2e_cb_per_MWh

        s.CO2e_cb = (
            s_fueloil.CO2e_cb
            + s_lpg.CO2e_cb
            + s_biomass.CO2e_cb
            + s_coal.CO2e_cb
            + s_petrol.CO2e_cb
            + s_heatnet.CO2e_cb
            + s_solarth.CO2e_cb
            + s_heatpump.CO2e_cb
            + s_gas.CO2e_cb
            + s_emethan.CO2e_cb
            + s_elec.CO2e_cb
        )

        s.change_energy_MWh = s.energy - r18.s.energy
        s_fueloil.change_energy_MWh = s_fueloil.energy - r18.s_fueloil.energy
        s_lpg.change_energy_MWh = s_lpg.energy - r18.s_lpg.energy
        s_biomass.change_energy_MWh = s_biomass.energy - r18.s_biomass.energy
        s_coal.change_energy_MWh = s_coal.energy - r18.s_coal.energy
        s_petrol.change_energy_MWh = s_petrol.energy - r18.s_petrol.energy
        s_heatnet.change_energy_MWh = s_heatnet.energy - r18.s_heatnet.energy
        s_solarth.change_energy_MWh = s_solarth.energy - r18.s_solarth.energy
        s_heatpump.change_energy_MWh = s_heatpump.energy - r18.s_heatpump.energy
        s_elec_heating.change_energy_MWh = (
            s_elec_heating.energy - r18.s_elec_heating.energy
        )
        s_emethan.change_energy_MWh = s_emethan.energy - 0
        s_elec.change_energy_MWh = s_elec.energy - r18.s_elec.energy

        p_buildings_total.change_energy_MWh = (
            p_buildings_total.energy - r18.p_buildings_total.energy
        )
        p_buildings_total.change_energy_pct = (
            p_buildings_total.change_energy_MWh / r18.p_buildings_total.energy
        )

        s.change_energy_pct = s.change_energy_MWh / r18.s.energy
        s_fueloil.change_energy_pct = s_fueloil.change_energy_MWh / r18.s_fueloil.energy
        s_lpg.change_energy_pct = s_lpg.change_energy_MWh / r18.s_lpg.energy
        s_biomass.change_energy_pct = s_biomass.change_energy_MWh / r18.s_biomass.energy
        s_coal.change_energy_pct = s_coal.change_energy_MWh / r18.s_coal.energy
        s_petrol.change_energy_pct = s_petrol.change_energy_MWh / r18.s_petrol.energy
        s_heatnet.change_energy_pct = s_heatnet.change_energy_MWh / r18.s_heatnet.energy
        s_solarth.change_energy_pct = s_solarth.change_energy_MWh / r18.s_solarth.energy
        s_heatpump.change_energy_pct = (
            s_heatpump.change_energy_MWh / r18.s_heatpump.energy
        )
        s_elec.change_energy_pct = s_elec.change_energy_MWh / r18.s_elec.energy
        s_elec_heating.change_energy_pct = (
            s_elec_heating.change_energy_MWh / r18.s_elec_heating.energy
        )
        s_emethan.change_energy_pct = s_emethan.change_energy_MWh / r18.s_gas.energy

        s.change_CO2e_t = s.CO2e_cb - r18.s.CO2e_cb
        s_fueloil.change_CO2e_t = s_fueloil.CO2e_cb - r18.s_fueloil.CO2e_cb
        s_lpg.change_CO2e_t = s_lpg.CO2e_cb - r18.s_lpg.CO2e_cb
        s_biomass.change_CO2e_t = s_biomass.CO2e_cb - r18.s_biomass.CO2e_cb
        s_coal.change_CO2e_t = s_coal.CO2e_cb - r18.s_coal.CO2e_cb
        s_petrol.change_CO2e_t = s_petrol.CO2e_cb - r18.s_petrol.CO2e_cb

        # not set in r18
        r18.s_heatnet.CO2e_cb = r18.s_solarth.CO2e_cb = r18.s_heatpump.CO2e_cb = 0
        s_heatnet.change_CO2e_t = s_heatnet.CO2e_cb - r18.s_heatnet.CO2e_cb
        s_solarth.change_CO2e_t = s_solarth.CO2e_cb - r18.s_solarth.CO2e_cb

        s_elec_heating.change_CO2e_t = 0
        s_emethan.change_CO2e_t = s_emethan.CO2e_cb - 0
        s_heatpump.change_CO2e_t = s.change_CO2e_t - s_emethan.change_CO2e_t

        s.change_CO2ee_pct = s.change_CO2e_t / r18.s.CO2e_cb

        s_fueloil.CO2e_total_2021_estimated = r18.s_fueloil.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_lpg.CO2e_total_2021_estimated = r18.s_lpg.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_biomass.CO2e_total_2021_estimated = r18.s_biomass.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_coal.CO2e_total_2021_estimated = r18.s_coal.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_petrol.CO2e_total_2021_estimated = r18.s_petrol.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_heatnet.CO2e_total_2021_estimated = r18.s_heatnet.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_solarth.CO2e_total_2021_estimated = r18.s_solarth.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_heatpump.CO2e_total_2021_estimated = r18.s_heatpump.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_gas.CO2e_total_2021_estimated = r18.s_gas.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_emethan.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        s.CO2e_total_2021_estimated = r18.s.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        KlimaneutraleJahre = entry("In_M_duration_neutral")

        s_fueloil.CO2e_pb = 0
        s_lpg.CO2e_pb = 0
        s_biomass.CO2e_pb = 0
        s_coal.CO2e_pb = 0
        s_petrol.CO2e_pb = 0
        s_heatnet.CO2e_pb = 0
        s_solarth.CO2e_pb = 0
        s_heatpump.CO2e_pb = 0

        s_fueloil.cost_climate_saved = (
            (
                s_fueloil.CO2e_total_2021_estimated
                - (s_fueloil.CO2e_pb + s_fueloil.CO2e_cb)
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_lpg.cost_climate_saved = (
            (s_lpg.CO2e_total_2021_estimated - (s_lpg.CO2e_pb + s_lpg.CO2e_cb))
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_biomass.cost_climate_saved = (
            (
                s_biomass.CO2e_total_2021_estimated
                - (s_biomass.CO2e_pb + s_biomass.CO2e_cb)
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_coal.cost_climate_saved = (
            (s_coal.CO2e_total_2021_estimated - (s_coal.CO2e_pb + s_coal.CO2e_cb))
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_petrol.cost_climate_saved = (
            (s_petrol.CO2e_total_2021_estimated - (s_petrol.CO2e_pb + s_petrol.CO2e_cb))
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_heatnet.cost_climate_saved = (
            (
                s_heatnet.CO2e_total_2021_estimated
                - (s_heatnet.CO2e_pb + s_heatnet.CO2e_cb)
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_solarth.cost_climate_saved = (
            (
                s_solarth.CO2e_total_2021_estimated
                - (s_solarth.CO2e_pb + s_solarth.CO2e_cb)
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_heatpump.cost_climate_saved = (
            (
                s_heatpump.CO2e_total_2021_estimated
                - (s_heatpump.CO2e_pb + s_heatpump.CO2e_cb)
            )
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_gas.cost_climate_saved = (
            (s_gas.CO2e_total_2021_estimated - (0 + s_gas.CO2e_cb))
            * KlimaneutraleJahre
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s_emethan.cost_climate_saved = (
            (s_emethan.CO2e_total_2021_estimated - s_emethan.CO2e_cb)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_elec_heating.cost_climate_saved = 0

        s.cost_climate_saved = (
            (s.CO2e_total_2021_estimated - s.CO2e_cb)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        s.change_cost_energy = s.cost_fuel - r18.s.cost_fuel
        s_fueloil.change_cost_energy = s_fueloil.cost_fuel - r18.s_fueloil.cost_fuel
        s_lpg.change_cost_energy = s_lpg.cost_fuel - r18.s_lpg.cost_fuel
        s_biomass.change_cost_energy = s_biomass.cost_fuel - r18.s_biomass.cost_fuel
        s_coal.change_cost_energy = s_coal.cost_fuel - r18.s_coal.cost_fuel
        s_petrol.change_cost_energy = s_petrol.cost_fuel - r18.s_petrol.cost_fuel
        s_heatnet.change_cost_energy = s_heatnet.cost_fuel - r18.s_heatnet.cost_fuel
        s_solarth.change_cost_energy = s_solarth.cost_fuel - r18.s_solarth.cost_fuel
        s_heatpump.change_cost_energy = s_heatpump.cost_fuel - r18.s_heatpump.cost_fuel
        s_emethan.change_cost_energy = s_emethan.cost_fuel - r18.s_gas.cost_fuel

        # s_solarth.action Ausbau Solarthermie
        # s_heatpump.action Ausbau Wärmepumpe

        # formula from e30 not still calc here
        e30.p_local_pv_roof.area_ha_available = (
            (4 / 3)
            * (
                (
                    entry("In_R_area_m2_1flat")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_building1")
                    + entry("In_R_area_m2_2flat")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_building2")
                    + entry("In_R_area_m2_3flat")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_building3")
                    + entry("In_R_area_m2_dorm")
                    / 100
                    * ass("Ass_E_P_local_pv_roof_area_buildingD")
                )
            )
            / 10000
        )
        p_buildings_until_1919.invest_per_x = fact(
            "Fact_R_P_energetical_renovation_cost_detached_house_until_1949"
        ) * (entry("In_R_area_m2_1flat") + entry("In_R_area_m2_2flat")) / entry(
            "In_R_area_m2"
        ) + fact(
            "Fact_R_P_energetical_renovation_cost_apartm_building_until_1949"
        ) * (
            entry("In_R_area_m2_3flat") + entry("In_R_area_m2_dorm")
        ) / entry(
            "In_R_area_m2"
        )
        p_buildings_1919_1948.invest_per_x = p_buildings_until_1919.invest_per_x
        p_buildings_1949_1978.invest_per_x = fact(
            "Fact_R_P_energetical_renovation_cost_detached_house_1949_1979"
        ) * (entry("In_R_area_m2_1flat") + entry("In_R_area_m2_2flat")) / entry(
            "In_R_area_m2"
        ) + fact(
            "Fact_R_P_energetical_renovation_cost_apartm_building_1949_1979"
        ) * (
            entry("In_R_area_m2_3flat") + entry("In_R_area_m2_dorm")
        ) / entry(
            "In_R_area_m2"
        )

        p_buildings_1979_1995.invest_per_x = fact(
            "Fact_R_P_energetical_renovation_cost_detached_house_1980+"
        ) * (entry("In_R_area_m2_1flat") + entry("In_R_area_m2_2flat")) / entry(
            "In_R_area_m2"
        ) + fact(
            "Fact_R_P_energetical_renovation_cost_apartm_building_1980+"
        ) * (
            entry("In_R_area_m2_3flat") + entry("In_R_area_m2_dorm")
        ) / entry(
            "In_R_area_m2"
        )
        p_buildings_1996_2004.invest_per_x = p_buildings_1979_1995.invest_per_x
        p_buildings_area_m2_com.invest_per_x = fact(
            "Fact_R_P_energetical_renovation_cost_housing_complex"
        )
        s_solarth.invest_per_x = ass("Ass_R_P_soltherm_cost_per_sqm")
        s_heatpump.invest_per_x = fact("Fact_R_S_heatpump_cost")

        s_solarth.invest = (
            r18.p_buildings_total.area_m2
            / (r18.p_buildings_total.area_m2 + b18.p_nonresi.area_m2)
            * e30.p_local_pv_roof.area_ha_available
            * entry("In_H_solartherm_to_be_inst")
            * s_solarth.invest_per_x
            * 10000
        )

        p_buildings_until_1919.invest = (
            p_buildings_until_1919.area_m2_rehab
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * p_buildings_until_1919.invest_per_x
        )
        p_buildings_1919_1948.invest = (
            p_buildings_1919_1948.area_m2_rehab
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * p_buildings_1919_1948.invest_per_x
        )
        p_buildings_1949_1978.invest = (
            p_buildings_1949_1978.area_m2_rehab
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * p_buildings_1949_1978.invest_per_x
        )
        p_buildings_1979_1995.invest = (
            p_buildings_1979_1995.area_m2_rehab
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * p_buildings_1979_1995.invest_per_x
        )
        p_buildings_1996_2004.invest = (
            p_buildings_1996_2004.area_m2_rehab
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * p_buildings_1996_2004.invest_per_x
        )

        s_heatpump.full_load_hour = fact("Fact_R_S_fhou")
        s_heatpump.power_installed = r18.s_heatpump.energy / s_heatpump.full_load_hour
        s_heatpump.power_to_be_installed = (
            p_buildings_total.area_m2_rehab
            * ass("Ass_R_S_heating_power_renovated")
            / Million
            - s_heatpump.power_installed
        )
        s_heatpump.invest = (
            s_heatpump.invest_per_x * s_heatpump.power_to_be_installed * 1000
        )

        p_buildings_total.invest = (
            p_buildings_until_1919.invest
            + p_buildings_1919_1948.invest
            + p_buildings_1949_1978.invest
            + p_buildings_1979_1995.invest
            + p_buildings_1996_2004.invest
        )  # SUM(p_buildings_until_1919.invest:p_buildings_1996_2004.invest)
        p_buildings_total.cost_mro = 0
        g_consult.invest = entry("In_R_buildings_le_2_apts") * fact(
            "Fact_R_G_energy_consulting_cost_detached_house"
        ) + entry("In_R_buildings_ge_3_apts") * fact(
            "Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats"
        )
        g.invest = g_consult.invest

        s.invest = s_solarth.invest + s_heatpump.invest

        s_solarth.invest_pa = s_solarth.invest / Kalkulationszeitraum
        s_heatpump.invest_pa = s_heatpump.invest / Kalkulationszeitraum

        s_solarth.pct_of_wage = fact(
            "Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017"
        )
        s_heatpump.pct_of_wage = fact(
            "Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017"
        )
        p_buildings_total.pct_of_wage = fact(
            "Fact_B_P_renovations_ratio_wage_to_main_revenue_2017"
        )

        s_solarth.cost_wage = s_solarth.invest_pa * s_solarth.pct_of_wage
        s_heatpump.cost_wage = s_heatpump.invest_pa * s_heatpump.pct_of_wage
        p_buildings_total.cost_wage = (
            p_buildings_total.invest
            / Kalkulationszeitraum
            * p_buildings_total.pct_of_wage
        )

        g_consult.cost_wage = g_consult.invest / Kalkulationszeitraum

        s_solarth.ratio_wage_to_emplo = fact(
            "Fact_B_P_heating_wage_per_person_per_year"
        )
        s_heatpump.ratio_wage_to_emplo = fact(
            "Fact_B_P_heating_wage_per_person_per_year"
        )
        p_buildings_total.ratio_wage_to_emplo = fact(
            "Fact_B_P_renovations_wage_per_person_per_year_2017"
        )
        g_consult.ratio_wage_to_emplo = fact("Fact_R_G_energy_consulting_cost_personel")

        s_solarth.demand_emplo = s_solarth.cost_wage / s_solarth.ratio_wage_to_emplo
        s_heatpump.demand_emplo = s_heatpump.cost_wage / s_heatpump.ratio_wage_to_emplo
        s.demand_emplo = s_solarth.demand_emplo + s_heatpump.demand_emplo
        p_buildings_total.demand_emplo = (
            p_buildings_total.cost_wage / p_buildings_total.ratio_wage_to_emplo
        )
        g_consult.demand_emplo = g_consult.cost_wage / g_consult.ratio_wage_to_emplo

        p_buildings_total.emplo_existing = (
            fact("Fact_B_P_renovation_emplo_2017")
            * p_buildings_total.demand_emplo
            / (
                p_buildings_total.demand_emplo
                + b30.p_nonresi.demand_emplo
                + a30.p_operation_heat.demand_emplo
            )
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )

        s_solarth.emplo_existing = (
            fact("Fact_B_P_install_heating_emplo_2017")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
            * s_solarth.demand_emplo
            / (
                s_solarth.demand_emplo
                + s_heatpump.demand_emplo
                + b30.s_heatpump.demand_emplo
                + b30.s_solarth.demand_emplo
                + a30.s_heatpump.demand_emplo
            )
        )
        s_heatpump.emplo_existing = (
            fact("Fact_B_P_install_heating_emplo_2017")
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
            * s_heatpump.demand_emplo
            / (
                s_solarth.demand_emplo
                + s_heatpump.demand_emplo
                + b30.s_heatpump.demand_emplo
                + b30.s_solarth.demand_emplo
                + a30.s_heatpump.demand_emplo
            )
        )

        p_buildings_total.demand_emplo_new = max(
            0, p_buildings_total.demand_emplo - p_buildings_total.emplo_existing
        )

        g_consult.emplo_existing = (
            fact("Fact_R_G_energy_consulting_total_personel")
            * g_consult.demand_emplo
            / (g_consult.demand_emplo + b30.g_consult.demand_emplo)
            * entry("In_M_population_com_2018")
            / entry("In_M_population_nat")
        )
        g_consult.demand_emplo_new = max(
            0, g_consult.demand_emplo - g_consult.emplo_existing
        )
        s_solarth.demand_emplo_new = max(
            0, s_solarth.demand_emplo - s_solarth.emplo_existing
        )
        s_heatpump.demand_emplo_new = max(
            0, s_heatpump.demand_emplo - s_heatpump.emplo_existing
        )
        s.demand_emplo_new = s_solarth.demand_emplo_new + s_heatpump.demand_emplo_new

        # s_solarth.base_unit € / qm
        # s_heatpump.base_unit € / kW

        p_buildings_area_m2_com.invest_com = (
            (
                p_buildings_until_1919.area_m2_rehab
                + p_buildings_1919_1948.area_m2_rehab
                + p_buildings_1949_1978.area_m2_rehab
                + p_buildings_1979_1995.area_m2_rehab
                + p_buildings_1996_2004.area_m2_rehab
            )
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * r18.p_buildings_area_m2_com.pct_x
            * p_buildings_area_m2_com.invest_per_x
        )
        p_buildings_total.invest_com = p_buildings_area_m2_com.invest_com

        g_consult.invest_com = g_consult.invest
        s_solarth.invest_com = s_solarth.invest * entry("In_R_pct_of_area_m2_com")
        s_heatpump.invest_com = s_heatpump.invest * entry("In_R_pct_of_area_m2_com")
        s.invest_com = s_solarth.invest_com + s_heatpump.invest_com

        p_buildings_total.invest_pa_com = (
            p_buildings_total.invest_com / Kalkulationszeitraum
        )
        s_solarth.invest_pa_com = s_solarth.invest_com / Kalkulationszeitraum
        s_heatpump.invest_pa_com = s_heatpump.invest_com / Kalkulationszeitraum

        g_consult.invest_pa = g_consult.invest / Kalkulationszeitraum
        s_gas.pct_energy = s_gas.energy / s.energy
        s_gas.cost_fuel_per_MWh = ass("Ass_R_S_gas_energy_cost_factor_2035")
        s_gas.cost_fuel = s_gas.energy * s_gas.cost_fuel_per_MWh / Million
        s_gas.change_energy_MWh = s_gas.energy - r18.s_gas.energy
        s_gas.change_energy_pct = s_gas.change_energy_MWh / r18.s_gas.energy
        s_gas.change_CO2e_t = s_gas.CO2e_cb - r18.s_gas.CO2e_cb
        s_gas.change_cost_energy = s_gas.cost_fuel - r18.s_gas.cost_fuel
        p_buildings_total.invest_pa = p_buildings_total.invest / Kalkulationszeitraum
        s_elec_heating.pct_energy = 0

        g.invest_pa = g_consult.invest_pa
        g_consult.invest_pa_com = g_consult.invest_pa
        g.invest_pa_com = g_consult.invest_pa_com
        g.invest_com = g_consult.invest_com
        g.cost_wage = g_consult.cost_wage
        g.demand_emplo = g_consult.demand_emplo
        g.demand_emplo_new = g_consult.demand_emplo_new
        g.demand_emplo_new = g_consult.demand_emplo_new
        g.invest_pa_com = g_consult.invest_pa_com
        p.demand_heatnet = s_heatnet.energy
        p.demand_biomass = s_biomass.energy
        p.demand_solarth = s_solarth.energy
        p.demand_heatpump = s_heatpump.energy
        p.demand_emethan = s_emethan.energy
        p.change_energy_MWh = p.energy - r18.p.energy
        p.change_energy_pct = p.change_energy_MWh / r18.p.energy
        p.invest_pa = p_buildings_total.invest_pa
        p.invest_pa_com = p_buildings_total.invest_pa_com
        p.invest = p_buildings_total.invest
        p.invest_com = p_buildings_total.invest_com
        p.invest_com = p_buildings_total.invest_com
        p.cost_wage = p_buildings_total.cost_wage
        p.demand_emplo = p_buildings_total.demand_emplo
        p.demand_emplo_new = p_buildings_total.demand_emplo_new
        p.demand_emplo_new = p_buildings_total.demand_emplo_new
        p_buildings_until_1919.change_energy_MWh = (
            p_buildings_until_1919.energy - r18.p_buildings_until_1919.energy
        )
        p_buildings_until_1919.change_energy_pct = (
            p_buildings_until_1919.change_energy_MWh / r18.p_buildings_until_1919.energy
        )
        p_buildings_1919_1948.change_energy_MWh = (
            p_buildings_1919_1948.energy - r18.p_buildings_1919_1948.energy
        )
        p_buildings_1919_1948.change_energy_pct = (
            p_buildings_1919_1948.change_energy_MWh / r18.p_buildings_1919_1948.energy
        )
        p_buildings_1949_1978.change_energy_MWh = (
            p_buildings_1949_1978.energy - r18.p_buildings_1949_1978.energy
        )
        p_buildings_1949_1978.change_energy_pct = (
            p_buildings_1949_1978.change_energy_MWh / r18.p_buildings_1949_1978.energy
        )
        p_buildings_1979_1995.change_energy_MWh = (
            p_buildings_1979_1995.energy - r18.p_buildings_1979_1995.energy
        )
        p_buildings_1979_1995.change_energy_pct = (
            p_buildings_1979_1995.change_energy_MWh / r18.p_buildings_1979_1995.energy
        )
        p_buildings_1996_2004.change_energy_MWh = (
            p_buildings_1996_2004.energy - r18.p_buildings_1996_2004.energy
        )
        p_buildings_1996_2004.change_energy_pct = (
            p_buildings_1996_2004.change_energy_MWh / r18.p_buildings_1996_2004.energy
        )
        p_buildings_2005_2011.change_energy_MWh = (
            p_buildings_2005_2011.energy - r18.p_buildings_2005_2011.energy
        )
        p_buildings_2005_2011.change_energy_pct = (
            p_buildings_2005_2011.change_energy_MWh / r18.p_buildings_2005_2011.energy
        )
        p_buildings_2011_today.change_energy_MWh = (
            p_buildings_2011_today.energy - r18.p_buildings_2011_today.energy
        )
        p_buildings_2011_today.change_energy_pct = (
            p_buildings_2011_today.change_energy_MWh / r18.p_buildings_2011_today.energy
        )
        p_buildings_area_m2_com.change_energy_MWh = (
            p_buildings_area_m2_com.energy - r18.p_buildings_area_m2_com.energy
        )
        p_buildings_area_m2_com.change_energy_pct = (
            p_buildings_area_m2_com.change_energy_MWh
            / r18.p_buildings_area_m2_com.energy
        )
        p_buildings_area_m2_com.invest_per_x = fact(
            "Fact_R_P_energetical_renovation_cost_housing_complex"
        )
        p_buildings_area_m2_com.invest = (
            (
                p_buildings_until_1919.area_m2_rehab
                + p_buildings_1919_1948.area_m2_rehab
                + p_buildings_1949_1978.area_m2_rehab
                + p_buildings_1979_1995.area_m2_rehab
                + p_buildings_1996_2004.area_m2_rehab
            )
            * (1 - fact("Fact_R_P_ratio_renovated_buildings to_not_renovated_2021"))
            * r18.p_buildings_area_m2_com.pct_x
            * p_buildings_area_m2_com.invest_per_x
        )
        p_buildings_area_m2_com.invest_com = p_buildings_area_m2_com.invest
        p_buildings_area_m2_com.invest_pa = p_buildings_area_m2_com.invest / entry(
            "In_M_duration_target"
        )
        p_buildings_area_m2_com.invest_pa_com = (
            p_buildings_area_m2_com.invest_com / entry("In_M_duration_target")
        )
        p_buildings_area_m2_com.invest_pa = p_buildings_area_m2_com.invest / entry(
            "In_M_duration_target"
        )
        p_buildings_area_m2_com.invest_pa_com = (
            p_buildings_area_m2_com.invest_com / entry("In_M_duration_target")
        )
        p_buildings_area_m2_com.invest_pa_com = (
            p_buildings_area_m2_com.invest_com / entry("In_M_duration_target")
        )
        p_buildings_new.change_energy_MWh = p_buildings_new.energy - 0
        p_other.change_energy_MWh = p_other.energy - r18.p_other.energy
        p_other.change_energy_pct = p_other.change_energy_MWh / r18.p_other.energy
        p_elec_heatpump.demand_change = (
            p_elec_heatpump.energy / r18.p_elec_heatpump.energy - 1
        )
        p_elec_heatpump.change_energy_MWh = (
            p_elec_heatpump.energy - r18.p_elec_heatpump.energy
        )
        p_elec_heatpump.change_energy_pct = (
            p_elec_heatpump.change_energy_MWh / r18.p_elec_heatpump.energy
        )
        p_elec_elcon.change_energy_MWh = p_elec_elcon.energy - r18.p_elec_elcon.energy
        p_elec_elcon.change_energy_pct = (
            p_elec_elcon.change_energy_MWh / r18.p_elec_elcon.energy
        )
        p_vehicles.change_energy_MWh = p_vehicles.energy - r18.p_vehicles.energy
        p_vehicles.change_energy_pct = (
            p_vehicles.change_energy_MWh / r18.p_vehicles.energy
        )
        s_fueloil.CO2e_total = s_fueloil.CO2e_cb
        s.CO2e_total_2021_estimated = r18.s.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s.change_CO2e_pct = s.change_CO2e_t / r18.s.CO2e_cb
        s.invest_pa = s_solarth.invest_pa + s_heatpump.invest_pa
        s.invest_pa_com = s_solarth.invest_pa_com + s_heatpump.invest_pa_com
        s.cost_wage = s_solarth.cost_wage + s_heatpump.cost_wage
        s.emplo_existing = s_solarth.emplo_existing + s_heatpump.emplo_existing
        s_lpg.CO2e_total = s_lpg.CO2e_cb
        s_fueloil.CO2e_total_2021_estimated = r18.s_fueloil.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_fueloil.change_CO2e_pct = s_fueloil.change_CO2e_t / r18.s_fueloil.CO2e_cb
        s_biomass.CO2e_total = s_biomass.CO2e_cb
        s_lpg.CO2e_total_2021_estimated = r18.s_lpg.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_lpg.change_CO2e_pct = s_lpg.change_CO2e_t / r18.s_lpg.CO2e_cb
        s_coal.CO2e_total = s_coal.CO2e_cb
        s_biomass.CO2e_total_2021_estimated = r18.s_biomass.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_biomass.change_CO2e_pct = s_biomass.change_CO2e_t / r18.s_biomass.CO2e_cb
        s_petrol.CO2e_total = s_petrol.CO2e_cb
        s_coal.CO2e_total_2021_estimated = r18.s_coal.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_coal.change_CO2e_pct = s_coal.change_CO2e_t / r18.s_coal.CO2e_cb
        s_heatnet.CO2e_total = s_heatnet.CO2e_cb
        s_petrol.CO2e_total_2021_estimated = r18.s_petrol.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_petrol.change_CO2e_pct = s_petrol.change_CO2e_t / r18.s_petrol.CO2e_cb
        s_solarth.CO2e_total = s_solarth.CO2e_cb
        s_heatnet.CO2e_total_2021_estimated = r18.s_heatnet.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_heatpump.CO2e_total = s_heatpump.CO2e_cb
        s_solarth.CO2e_total_2021_estimated = r18.s_solarth.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_gas.CO2e_total = s_gas.CO2e_cb
        s_heatpump.CO2e_total_2021_estimated = r18.s_heatpump.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_emethan.CO2e_total = s_emethan.CO2e_cb
        s_gas.CO2e_total_2021_estimated = r18.s_gas.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_gas.change_CO2e_pct = s_gas.change_CO2e_t / r18.s_gas.CO2e_cb
        s_elec.CO2e_total = s_elec.CO2e_cb
        s_emethan.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_elec.CO2e_cb_per_MWh = r18.s_elec.CO2e_cb_per_MWh
        s.CO2e_total = (
            s_fueloil.CO2e_total
            + s_lpg.CO2e_total
            + s_biomass.CO2e_total
            + s_coal.CO2e_total
            + s_petrol.CO2e_total
            + s_heatnet.CO2e_total
            + s_solarth.CO2e_total
            + s_heatpump.CO2e_total
            + s_gas.CO2e_total
            + s_emethan.CO2e_total
            + s_elec.CO2e_total
        )
        s_elec.CO2e_total_2021_estimated = r18.s_elec.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_elec.change_CO2e_t = s_elec.CO2e_cb - r18.s_elec.CO2e_cb
        s_elec.CO2e_total_2021_estimated = r18.s_elec.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_elec.cost_climate_saved = (
            (s_elec.CO2e_total_2021_estimated - s_elec.CO2e_cb)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        s_elec.change_cost_energy = 0
        s_elec_heating.CO2e_cb_per_MWh = r18.s_elec_heating.CO2e_cb_per_MWh
        s_elec_heating.CO2e_cb_per_MWh = r18.s_elec_heating.CO2e_cb_per_MWh
        s_elec_heating.CO2e_cb = s_elec_heating.energy * s_elec_heating.CO2e_cb_per_MWh
        s_elec_heating.CO2e_total = s_elec_heating.CO2e_cb
        s_elec_heating.CO2e_total_2021_estimated = r18.s_elec_heating.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_elec_heating.CO2e_total_2021_estimated = r18.s_elec_heating.CO2e_cb * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        s_elec_heating.change_cost_energy = 0 - r18.s_elec_heating.cost_fuel

        r.CO2e_cb = s.CO2e_cb
        r.CO2e_total = s.CO2e_total
        r.change_energy_MWh = s.change_energy_MWh
        r.change_energy_pct = s.change_energy_pct
        r.change_CO2e_t = s.change_CO2e_t
        r.change_CO2e_pct = s.change_CO2e_pct
        r.CO2e_total_2021_estimated = s.CO2e_total_2021_estimated
        r.cost_climate_saved = s.cost_climate_saved
        r.invest_pa = g.invest_pa + p.invest_pa + s.invest_pa

        r.invest_pa_com = g.invest_pa_com + p.invest_pa_com + s.invest_pa_com

        r.invest = g.invest + p.invest + s.invest
        r.invest_com = g.invest_com + p.invest_com + s.invest_com

        r.cost_wage = g.cost_wage + p.cost_wage + s.cost_wage
        r.demand_emplo = g.demand_emplo + p.demand_emplo + s.demand_emplo
        r.demand_emplo_new = (
            g.demand_emplo_new + p.demand_emplo_new + s.demand_emplo_new
        )

    except Exception as e:
        print(e)
        raise
