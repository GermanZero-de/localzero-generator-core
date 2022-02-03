from dataclasses import dataclass, asdict
from .inputs import Inputs
from .utils import div


@dataclass
class zColVars:
    energy_18: float = None
    pct_energy_18: float = None
    CO2e_pb_18: float = None
    CO2e_cb_18: float = None
    CO2e_total_18: float = None
    pct_CO2e_total_18: float = None

    energy_30: float = None
    pct_energy_30: float = None
    CO2e_pb_30: float = None
    CO2e_cb_30: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_total_30: float = None
    pct_CO2e_total_30: float = None
    change_energy_MWh: float = None
    change_energy_pct: float = None
    change_CO2e_t: float = None
    change_CO2e_pct: float = None
    CO2e_total_2021_estimated: float = None
    cost_climate_saved: float = None
    invest_pa: float = None
    invest_pa_com: float = None
    invest_pa_outside: float = None
    invest: float = None
    invest_com: float = None
    invest_outside: float = None
    cost_wage: float = None
    demand_emplo: float = None
    demand_emplo_new: float = None
    demand_emplo_com: float = None


# definition of variable names for sector M(ethodology) - there are no rows or columns in the excel!
@dataclass
class M183X:
    # year_target: float = None
    # duration_target: float = None
    # duration_target_until_2050: float = None
    # duration_neutral: float = None

    CO2_budget_2016_to_year_target: float = None
    nonCO2_budget_2016_to_year_target: float = None
    GHG_budget_2016_to_year_target: float = None
    GHG_budget_2022_to_year_target: float = None
    GHG_budget_after_year_target: float = None

    CO2e_w_lulucf_change_pa: float = None

    CO2e_lulucf_2015: float = None
    CO2e_lulucf_2016: float = None
    CO2e_lulucf_2017: float = None
    CO2e_lulucf_2018: float = None
    CO2e_lulucf_2019: float = None
    CO2e_lulucf_2020: float = None
    CO2e_lulucf_2021: float = None

    CO2e_wo_lulucf_2015: float = None
    CO2e_wo_lulucf_2016: float = None
    CO2e_wo_lulucf_2017: float = None
    CO2e_wo_lulucf_2018: float = None
    CO2e_wo_lulucf_2019: float = None
    CO2e_wo_lulucf_2020: float = None
    CO2e_wo_lulucf_2021: float = None

    CO2e_w_lulucf_2015: float = None
    CO2e_w_lulucf_2016: float = None
    CO2e_w_lulucf_2017: float = None
    CO2e_w_lulucf_2018: float = None
    CO2e_w_lulucf_2019: float = None
    CO2e_w_lulucf_2020: float = None
    CO2e_w_lulucf_2021: float = None
    CO2e_w_lulucf_2022: float = None
    CO2e_w_lulucf_2023: float = None
    CO2e_w_lulucf_2024: float = None
    CO2e_w_lulucf_2025: float = None
    CO2e_w_lulucf_2026: float = None
    CO2e_w_lulucf_2027: float = None
    CO2e_w_lulucf_2028: float = None
    CO2e_w_lulucf_2029: float = None
    CO2e_w_lulucf_2030: float = None
    CO2e_w_lulucf_2031: float = None
    CO2e_w_lulucf_2032: float = None
    CO2e_w_lulucf_2033: float = None
    CO2e_w_lulucf_2034: float = None
    CO2e_w_lulucf_2035: float = None
    CO2e_w_lulucf_2036: float = None
    CO2e_w_lulucf_2037: float = None
    CO2e_w_lulucf_2038: float = None
    CO2e_w_lulucf_2039: float = None
    CO2e_w_lulucf_2040: float = None
    CO2e_w_lulucf_2041: float = None
    CO2e_w_lulucf_2042: float = None
    CO2e_w_lulucf_2043: float = None
    CO2e_w_lulucf_2044: float = None
    CO2e_w_lulucf_2045: float = None
    CO2e_w_lulucf_2046: float = None
    CO2e_w_lulucf_2047: float = None
    CO2e_w_lulucf_2048: float = None
    CO2e_w_lulucf_2049: float = None
    CO2e_w_lulucf_2050: float = None
    CO2e_w_lulucf_2051: float = None

    # =======Z-Script Varaibles=============================

    CO2e_lulucf_203X: float = None
    CO2e_wo_lulucf_203X: float = None
    CO2e_w_lulucf_203X: float = None

    change_CO2e_t: float = None
    change_CO2e_pct: float = None
    cost_climate_saved: float = None

    z: zColVars = zColVars()
    s: zColVars = zColVars()
    d: zColVars = zColVars()

    e: zColVars = zColVars()
    h: zColVars = zColVars()
    f: zColVars = zColVars()
    rb: zColVars = zColVars()
    r: zColVars = zColVars()
    b: zColVars = zColVars()
    t: zColVars = zColVars()
    i: zColVars = zColVars()
    a: zColVars = zColVars()
    l: zColVars = zColVars()

    CO2e_per_capita_nat: float = None
    CO2e_per_capita_com: float = None
    CO2e_per_capita_com_pct_of_nat: float = None

    # erzeuge dictionry
    def dict(self):
        return asdict(self)


# these budget calculations have to be done after all sector calculations
def calc_Budget(root, inputs: Inputs) -> M183X:
    def fact(n):
        return inputs.fact(n)

    def entry(n):
        return inputs.entry(n)

    ######################################
    ### budgets 2016 until target year ###
    ######################################

    m183X = M183X()
    # local greenhouse gas budget from 2016 until target year in com!!
    m183X.GHG_budget_2016_to_year_target = (
        entry("In_M_GHG_budget_2016_to_year_target")
        * entry("In_M_population_com_2018")
        / entry("In_M_population_nat")
    )

    # local nonCO2 budget from 2016 until target year in com!!
    m183X.nonCO2_budget_2016_to_year_target = (
        entry("In_M_nonCO2_budget_2016_to_year_target")
        * entry("In_M_population_com_2018")
        / entry("In_M_population_nat")
    )

    # local CO2 budget from 2016 until infinity
    m183X.CO2_budget_2016_to_year_target = (
        m183X.GHG_budget_2016_to_year_target - m183X.nonCO2_budget_2016_to_year_target
    )

    ############################################
    ### 2018 as base for emissions 2016-2021 ###
    ############################################
    ### beginning with LULUCF                ###
    ############################################

    # get the CO2e of LULUCF for 2018 as calculated
    m183X.CO2e_lulucf_2018 = root.l18.l.CO2e_total

    # calculate the CO2e of LULUCF for 2015-2017 and 2019-2021 by multiplying 2018's value with percentage
    # 2015 just as a backup, probably not needed
    m183X.CO2e_lulucf_2015 = m183X.CO2e_lulucf_2018 * fact(
        "Fact_M_CO2e_lulucf_2015_vs_2018"
    )

    m183X.CO2e_lulucf_2016 = m183X.CO2e_lulucf_2018 * fact(
        "Fact_M_CO2e_lulucf_2016_vs_2018"
    )

    m183X.CO2e_lulucf_2017 = m183X.CO2e_lulucf_2018 * fact(
        "Fact_M_CO2e_lulucf_2017_vs_2018"
    )

    m183X.CO2e_lulucf_2019 = m183X.CO2e_lulucf_2018 * fact(
        "Fact_M_CO2e_lulucf_2019_vs_2018"
    )

    m183X.CO2e_lulucf_2020 = m183X.CO2e_lulucf_2018 * fact(
        "Fact_M_CO2e_lulucf_2020_vs_2018"
    )

    m183X.CO2e_lulucf_2021 = m183X.CO2e_lulucf_2018 * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )

    ############################################
    ### 2018 as base for emissions 2016-2021 ###
    ############################################
    ### second emissions without (wo) LULUCF ###
    ############################################

    # get the CO2e of all sectors for 2018 excluding LULUCF since this is negative
    m183X.CO2e_wo_lulucf_2018 = (
        root.h18.h.CO2e_total
        + root.e18.e.CO2e_total
        + root.f18.f.CO2e_total
        + root.r18.r.CO2e_total
        + root.b18.b.CO2e_total
        + root.i18.i.CO2e_total
        + root.t18.t.CO2e_total
        + root.a18.a.CO2e_total
    )

    # calculate the CO2e of all sectors without LULUCF for 2015-2017 and 2019-2021 by multiplying 2018's value with percentage
    # 2015 just as a backup, probably not needed
    m183X.CO2e_wo_lulucf_2015 = m183X.CO2e_wo_lulucf_2018 * fact(
        "Fact_M_CO2e_wo_lulucf_2015_vs_2018"
    )

    m183X.CO2e_wo_lulucf_2016 = m183X.CO2e_wo_lulucf_2018 * fact(
        "Fact_M_CO2e_wo_lulucf_2016_vs_2018"
    )

    m183X.CO2e_wo_lulucf_2017 = m183X.CO2e_wo_lulucf_2018 * fact(
        "Fact_M_CO2e_wo_lulucf_2017_vs_2018"
    )

    m183X.CO2e_wo_lulucf_2019 = m183X.CO2e_wo_lulucf_2018 * fact(
        "Fact_M_CO2e_wo_lulucf_2019_vs_2018"
    )

    m183X.CO2e_wo_lulucf_2020 = m183X.CO2e_wo_lulucf_2018 * fact(
        "Fact_M_CO2e_wo_lulucf_2020_vs_2018"
    )

    m183X.CO2e_wo_lulucf_2021 = m183X.CO2e_wo_lulucf_2018 * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )

    #############################################
    ### 2018 as base for emissions 2016-2021  ###
    #############################################
    ### sum up CO2e_wo_lulucf and CO2e_lulucf ###
    #############################################

    # 2015 just as a backup, probably not needed
    m183X.CO2e_w_lulucf_2015 = m183X.CO2e_wo_lulucf_2015 + m183X.CO2e_lulucf_2015

    m183X.CO2e_w_lulucf_2016 = m183X.CO2e_wo_lulucf_2016 + m183X.CO2e_lulucf_2016

    m183X.CO2e_w_lulucf_2017 = m183X.CO2e_wo_lulucf_2017 + m183X.CO2e_lulucf_2017

    m183X.CO2e_w_lulucf_2018 = m183X.CO2e_wo_lulucf_2018 + m183X.CO2e_lulucf_2018

    m183X.CO2e_w_lulucf_2019 = m183X.CO2e_wo_lulucf_2019 + m183X.CO2e_lulucf_2019

    m183X.CO2e_w_lulucf_2020 = m183X.CO2e_wo_lulucf_2020 + m183X.CO2e_lulucf_2020

    m183X.CO2e_w_lulucf_2021 = m183X.CO2e_wo_lulucf_2021 + m183X.CO2e_lulucf_2021

    ####################################################################
    ### remaining local greenhouse gas budget 2022 until target year ###
    ####################################################################

    m183X.GHG_budget_2022_to_year_target = (
        m183X.GHG_budget_2016_to_year_target
        - m183X.CO2e_w_lulucf_2016
        - m183X.CO2e_w_lulucf_2017
        - m183X.CO2e_w_lulucf_2018
        - m183X.CO2e_w_lulucf_2019
        - m183X.CO2e_w_lulucf_2020
        - m183X.CO2e_w_lulucf_2021
    )

    #########################################################
    ### calculating the linear decrease until target year ###
    #########################################################
    ### these values are used for reduction path          ###
    #########################################################

    # calculating the yearly decrease of the emissions, going down linearly to 0 in target_year+1
    m183X.CO2e_w_lulucf_change_pa = m183X.CO2e_w_lulucf_2021 / (
        entry("In_M_duration_target") + 1
    )  # +1 because we want to reach 0 in target_year+1
    # reducing the yearly emissions year by year, starting with 2022
    if m183X.CO2e_w_lulucf_2021 > 0:
        m183X.CO2e_w_lulucf_2022 = (
            m183X.CO2e_w_lulucf_2021 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2022 = 0

    # 2023
    if m183X.CO2e_w_lulucf_2022 > 0:
        m183X.CO2e_w_lulucf_2023 = (
            m183X.CO2e_w_lulucf_2022 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2023 = 0

    # 2024
    if m183X.CO2e_w_lulucf_2023 > 0:
        m183X.CO2e_w_lulucf_2024 = (
            m183X.CO2e_w_lulucf_2023 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2024 = 0

    # 2025
    if m183X.CO2e_w_lulucf_2024 > 0:
        m183X.CO2e_w_lulucf_2025 = (
            m183X.CO2e_w_lulucf_2024 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2025 = 0

    # 2026
    if m183X.CO2e_w_lulucf_2025 > 0:
        m183X.CO2e_w_lulucf_2026 = (
            m183X.CO2e_w_lulucf_2025 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2026 = 0

    # 2027
    if m183X.CO2e_w_lulucf_2026 > 0:
        m183X.CO2e_w_lulucf_2027 = (
            m183X.CO2e_w_lulucf_2026 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2027 = 0

    # 2028
    if m183X.CO2e_w_lulucf_2027 > 0:
        m183X.CO2e_w_lulucf_2028 = (
            m183X.CO2e_w_lulucf_2027 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2028 = 0

    # 2029
    if m183X.CO2e_w_lulucf_2028 > 0:
        m183X.CO2e_w_lulucf_2029 = (
            m183X.CO2e_w_lulucf_2028 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2029 = 0

    # 2030
    if m183X.CO2e_w_lulucf_2029 > 0:
        m183X.CO2e_w_lulucf_2030 = (
            m183X.CO2e_w_lulucf_2029 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2030 = 0

    # 2031
    if m183X.CO2e_w_lulucf_2030 > 0:
        m183X.CO2e_w_lulucf_2031 = (
            m183X.CO2e_w_lulucf_2030 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2031 = 0

    # 2032
    if m183X.CO2e_w_lulucf_2031 > 0:
        m183X.CO2e_w_lulucf_2032 = (
            m183X.CO2e_w_lulucf_2031 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2032 = 0

    # 2033
    if m183X.CO2e_w_lulucf_2032 > 0:
        m183X.CO2e_w_lulucf_2033 = (
            m183X.CO2e_w_lulucf_2032 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2033 = 0

    # 2034
    if m183X.CO2e_w_lulucf_2033 > 0:
        m183X.CO2e_w_lulucf_2034 = (
            m183X.CO2e_w_lulucf_2033 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2034 = 0

    # 2035
    if m183X.CO2e_w_lulucf_2034 > 0:
        m183X.CO2e_w_lulucf_2035 = (
            m183X.CO2e_w_lulucf_2034 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2035 = 0

    # 2036
    if m183X.CO2e_w_lulucf_2035 > 0:
        m183X.CO2e_w_lulucf_2036 = (
            m183X.CO2e_w_lulucf_2035 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2036 = 0

    # 2037
    if m183X.CO2e_w_lulucf_2036 > 0:
        m183X.CO2e_w_lulucf_2037 = (
            m183X.CO2e_w_lulucf_2036 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2037 = 0

    # 2038
    if m183X.CO2e_w_lulucf_2037 > 0:
        m183X.CO2e_w_lulucf_2038 = (
            m183X.CO2e_w_lulucf_2037 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2038 = 0

    # 2039
    if m183X.CO2e_w_lulucf_2038 > 0:
        m183X.CO2e_w_lulucf_2039 = (
            m183X.CO2e_w_lulucf_2038 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2039 = 0

    # 2040
    if m183X.CO2e_w_lulucf_2039 > 0:
        m183X.CO2e_w_lulucf_2040 = (
            m183X.CO2e_w_lulucf_2039 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2040 = 0

    # 2041
    if m183X.CO2e_w_lulucf_2040 > 0:
        m183X.CO2e_w_lulucf_2041 = (
            m183X.CO2e_w_lulucf_2040 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2041 = 0

    # 2042
    if m183X.CO2e_w_lulucf_2041 > 0:
        m183X.CO2e_w_lulucf_2042 = (
            m183X.CO2e_w_lulucf_2041 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2042 = 0

    # 2043
    if m183X.CO2e_w_lulucf_2042 > 0:
        m183X.CO2e_w_lulucf_2043 = (
            m183X.CO2e_w_lulucf_2042 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2043 = 0

    # 2044
    if m183X.CO2e_w_lulucf_2043 > 0:
        m183X.CO2e_w_lulucf_2044 = (
            m183X.CO2e_w_lulucf_2043 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2044 = 0

    # 2045
    if m183X.CO2e_w_lulucf_2044 > 0:
        m183X.CO2e_w_lulucf_2045 = (
            m183X.CO2e_w_lulucf_2044 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2045 = 0

    # 2046
    if m183X.CO2e_w_lulucf_2045 > 0:
        m183X.CO2e_w_lulucf_2046 = (
            m183X.CO2e_w_lulucf_2046 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2046 = 0

    # 2047
    if m183X.CO2e_w_lulucf_2046 > 0:
        m183X.CO2e_w_lulucf_2047 = (
            m183X.CO2e_w_lulucf_2046 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2047 = 0

    # 2048
    if m183X.CO2e_w_lulucf_2047 > 0:
        m183X.CO2e_w_lulucf_2048 = (
            m183X.CO2e_w_lulucf_2047 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2048 = 0

    # 2049
    if m183X.CO2e_w_lulucf_2048 > 0:
        m183X.CO2e_w_lulucf_2049 = (
            m183X.CO2e_w_lulucf_2048 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2049 = 0

    # 2050
    if m183X.CO2e_w_lulucf_2049 > 0:
        m183X.CO2e_w_lulucf_2050 = (
            m183X.CO2e_w_lulucf_2049 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2050 = 0

    # 2051
    if m183X.CO2e_w_lulucf_2050 > 0:
        m183X.CO2e_w_lulucf_2051 = (
            m183X.CO2e_w_lulucf_2050 - m183X.CO2e_w_lulucf_change_pa
        )
    else:
        m183X.CO2e_w_lulucf_2051 = 0

    ##############################################################################################
    ### remaining local greenhouse gas budget after reaching climate neutrality in target year ###
    ##############################################################################################

    # all emission values until 2051 are subtracted since they are 0 after target year
    m183X.GHG_budget_after_year_target = (
        m183X.GHG_budget_2022_to_year_target
        - m183X.CO2e_w_lulucf_2022
        - m183X.CO2e_w_lulucf_2023
        - m183X.CO2e_w_lulucf_2024
        - m183X.CO2e_w_lulucf_2025
        - m183X.CO2e_w_lulucf_2026
        - m183X.CO2e_w_lulucf_2027
        - m183X.CO2e_w_lulucf_2028
        - m183X.CO2e_w_lulucf_2029
        - m183X.CO2e_w_lulucf_2030
        - m183X.CO2e_w_lulucf_2031
        - m183X.CO2e_w_lulucf_2032
        - m183X.CO2e_w_lulucf_2033
        - m183X.CO2e_w_lulucf_2034
        - m183X.CO2e_w_lulucf_2035
        - m183X.CO2e_w_lulucf_2036
        - m183X.CO2e_w_lulucf_2037
        - m183X.CO2e_w_lulucf_2038
        - m183X.CO2e_w_lulucf_2039
        - m183X.CO2e_w_lulucf_2040
        - m183X.CO2e_w_lulucf_2041
        - m183X.CO2e_w_lulucf_2042
        - m183X.CO2e_w_lulucf_2043
        - m183X.CO2e_w_lulucf_2044
        - m183X.CO2e_w_lulucf_2045
        - m183X.CO2e_w_lulucf_2046
        - m183X.CO2e_w_lulucf_2047
        - m183X.CO2e_w_lulucf_2048
        - m183X.CO2e_w_lulucf_2049
        - m183X.CO2e_w_lulucf_2050
        - m183X.CO2e_w_lulucf_2051
    )

    return m183X


def calc_Z(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def entry(n):
        return inputs.entry(n)

    ##################################################################
    ### total emissions 203X, saved emissions, saved climate costs ###
    ##################################################################

    m183X = root.m183X

    e18 = root.e18
    h18 = root.h18
    f18 = root.f18
    r18 = root.r18
    b18 = root.b18
    i18 = root.i18
    t18 = root.t18
    a18 = root.a18
    l18 = root.l18

    e30 = root.e30
    h30 = root.h30
    f30 = root.f30
    r30 = root.r30
    b30 = root.b30
    i30 = root.i30
    t30 = root.t30
    a30 = root.a30
    l30 = root.l30

    # get the CO2e of all sectors for 203X (the target year) excluding LULUCF
    m183X.CO2e_wo_lulucf_203X = (
        h30.h.CO2e_total
        + e30.e.CO2e_total
        + f30.f.CO2e_total
        + r30.r.CO2e_total
        + b30.b.CO2e_total
        + i30.i.CO2e_total
        + t30.t.CO2e_total
        + a30.a.CO2e_total
    )

    # TODO: Check with Hauke if this is correct:
    m183X.CO2e_lulucf_203X = l30.l.CO2e_total

    # get the CO2e of all sectors für 203X (the target year) which should be 0
    m183X.CO2e_w_lulucf_203X = m183X.CO2e_wo_lulucf_203X + m183X.CO2e_lulucf_203X

    # calculate the total CO2e difference in t between 2018 and 203X
    m183X.change_CO2e_t = m183X.CO2e_w_lulucf_203X - m183X.CO2e_w_lulucf_2018

    # calculate the total CO2e difference in % between 2018 and 203X
    m183X.change_CO2e_pct = div(m183X.change_CO2e_t, m183X.CO2e_w_lulucf_2018)

    # get the total saved climate cost of all sectors until 2050
    m183X.cost_climate_saved = (
        h30.h.cost_climate_saved
        + e30.e.cost_climate_saved
        + f30.f.cost_climate_saved
        + r30.r.cost_climate_saved
        + b30.b.cost_climate_saved
        + i30.i.cost_climate_saved
        + t30.t.cost_climate_saved
        + a30.a.cost_climate_saved
        + l30.l.cost_climate_saved
    )

    # ==========Excel-Z-Script Calclulations=====================
    s = m183X.s
    d = m183X.d
    z = m183X.z

    e = m183X.e
    h = m183X.h
    f = m183X.f
    r = m183X.r
    b = m183X.b
    rb = m183X.rb
    i = m183X.i
    t = m183X.t
    a = m183X.a
    l = m183X.l

    s.energy_18 = h18.p.energy + e18.p.energy + f18.p.energy
    d.energy_18 = (
        r18.p.energy + b18.p.energy + i18.p.energy + t18.t.energy + a18.p.energy
    )
    z.energy_18 = s.energy_18

    s.CO2e_pb_18 = h18.h.CO2e_pb + e18.e.CO2e_pb + f18.f.CO2e_pb
    # d.CO2e_pb_18 = r18.r.CO2e_pb + b18.b.CO2e_pb + i18.i.CO2e_pb + t18.t.CO2e_pb + a18.a.CO2e_pb + l18.l.CO2e_pb
    d.CO2e_pb_18 = i18.i.CO2e_pb + a18.a.CO2e_pb + l18.l.CO2e_pb
    z.CO2e_pb_18 = s.CO2e_pb_18 + d.CO2e_pb_18

    s.CO2e_cb_18 = h18.h.CO2e_cb + e18.e.CO2e_cb + f18.f.CO2e_cb
    d.CO2e_cb_18 = (
        r18.r.CO2e_cb
        + b18.b.CO2e_cb
        + i18.i.CO2e_cb
        + t18.t.CO2e_cb
        + a18.a.CO2e_cb
        + l18.l.CO2e_cb
    )
    z.CO2e_cb_18 = s.CO2e_cb_18 + d.CO2e_cb_18

    s.CO2e_total_18 = h18.h.CO2e_total + e18.e.CO2e_total + f18.f.CO2e_total
    d.CO2e_total_18 = (
        r18.r.CO2e_total
        + b18.b.CO2e_total
        + i18.i.CO2e_total
        + t18.t.CO2e_total
        + a18.a.CO2e_total
        + l18.l.CO2e_total
    )
    z.CO2e_total_18 = s.CO2e_total_18 + d.CO2e_total_18

    s.energy_30 = h30.p.energy + e30.p.energy + f30.p.energy
    d.energy_30 = (
        r30.p.energy + b30.p.energy + i30.p.energy + t30.t.energy + a30.p.energy
    )
    z.energy_30 = s.energy_30

    # s.CO2e_pb_30 = h30.h.CO2e_pb + e30.e.CO2e_pb + f30.f.CO2e_pb
    s.CO2e_pb_30 = h30.h.CO2e_pb + f30.f.CO2e_pb
    # d.CO2e_pb_30 = r30.r.CO2e_pb + b30.b.CO2e_pb + i30.i.CO2e_pb + t30.t.CO2e_pb + a30.a.CO2e_pb + l30.l.CO2e_pb
    d.CO2e_pb_30 = i30.i.CO2e_pb + a30.a.CO2e_pb + l30.l.CO2e_pb
    z.CO2e_pb_30 = s.CO2e_pb_30 + d.CO2e_pb_30

    # s.CO2e_cb_30 = h30.h.CO2e_cb + e30.e.CO2e_cb + f30.f.CO2e_cb
    s.CO2e_cb_30 = h30.h.CO2e_cb + e30.e.CO2e_cb
    d.CO2e_cb_30 = (
        r30.r.CO2e_cb
        + b30.b.CO2e_cb
        + i30.i.CO2e_cb
        + t30.t.CO2e_cb
        + a30.a.CO2e_cb
        + l30.l.CO2e_cb
    )
    z.CO2e_cb_30 = s.CO2e_cb_30 + d.CO2e_cb_30

    z.CO2e_cb_per_MWh = div(z.CO2e_cb_30, z.energy_30)

    s.CO2e_total_30 = h30.h.CO2e_total + e30.e.CO2e_total + f30.f.CO2e_total
    d.CO2e_total_30 = (
        r30.r.CO2e_total
        + b30.b.CO2e_total
        + i30.i.CO2e_total
        + t30.t.CO2e_total
        + a30.a.CO2e_total
        + l30.l.CO2e_total
    )
    z.CO2e_total_30 = s.CO2e_total_30 + d.CO2e_total_30

    s.change_energy_MWh = s.energy_30 - s.energy_18
    d.change_energy_MWh = d.energy_30 - d.energy_18
    z.change_energy_MWh = z.energy_30 - z.energy_18

    s.change_energy_pct = div(s.energy_30, s.energy_18)
    d.change_energy_pct = div(d.energy_30, d.energy_18)
    z.change_energy_pct = div(z.energy_30, z.energy_18)

    s.change_CO2e_t = s.CO2e_total_30 - s.CO2e_total_18
    d.change_CO2e_t = d.CO2e_total_30 - d.CO2e_total_18
    z.change_CO2e_t = z.CO2e_total_30 - z.CO2e_total_18

    s.change_CO2e_t_pct = div(s.CO2e_total_30, s.CO2e_total_18)
    d.change_CO2e_t_pct = div(d.CO2e_total_30, d.CO2e_total_18)
    z.change_CO2e_t_pct = div(z.CO2e_total_30, z.CO2e_total_18)

    s.CO2e_total_2021_estimated = s.CO2e_total_18 * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    d.CO2e_total_2021_estimated = d.CO2e_total_18 * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    z.CO2e_total_2021_estimated = (
        s.CO2e_total_2021_estimated + d.CO2e_total_2021_estimated
    )

    s.cost_climate_saved = (
        (s.CO2e_total_2021_estimated - s.CO2e_total_30)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    d.cost_climate_saved = (
        (d.CO2e_total_2021_estimated - d.CO2e_total_30)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    z.cost_climate_saved = s.cost_climate_saved + d.cost_climate_saved

    s.invest_pa = h30.h.invest_pa + e30.e.invest_pa + f30.f.invest_pa
    d.invest_pa = (
        r30.r.invest_pa
        + b30.b.invest_pa
        + i30.i.invest_pa
        + t30.t.invest_pa
        + a30.a.invest_pa
        + l30.l.invest_pa
    )
    z.invest_pa = s.invest_pa + d.invest_pa

    # s.invest_pa_com = h30.h.invest_pa_com + e30.e.invest_pa_com + f30.f.invest_pa_com
    s.invest_pa_com = h30.h.invest_pa_com + e30.e.invest_pa_com
    # d.invest_pa_com = r30.r.invest_pa_com + b30.b.invest_pa_com + i30.i.invest_pa_com + t30.t.invest_pa_com + a30.a.invest_pa_com + l30.l.invest_pa_com
    d.invest_pa_com = (
        r30.r.invest_pa_com
        + b30.b.invest_pa_com
        + i30.i.invest_pa_com
        + t30.t.invest_pa_com
        + a30.a.invest_pa_com
    )
    z.invest_pa_com = s.invest_pa_com + d.invest_pa_com

    # s.invest_pa_outside = h30.h.invest_pa_outside + e30.e.invest_pa_outside + f30.f.invest_pa_outside
    s.invest_pa_outside = e30.e.invest_pa_outside + f30.f.invest_pa_outside
    # d.invest_pa_outside = r30.r.invest_pa_outside + b30.b.invest_pa_outside + i30.i.invest_pa_outside + t30.t.invest_pa_outside + a30.a.invest_pa_outside + l30.l.invest_pa_outside
    d.invest_pa_outside = i30.i.invest_pa_outside + a30.a.invest_pa_outside
    z.invest_pa_outside = s.invest_pa_outside + d.invest_pa_outside

    s.invest = h30.h.invest + e30.e.invest + f30.f.invest
    d.invest = (
        r30.r.invest
        + b30.b.invest
        + i30.i.invest
        + t30.t.invest
        + a30.a.invest
        + l30.l.invest
    )
    z.invest = s.invest + d.invest

    # s.invest_com = h30.h.invest_com + e30.e.invest_com + f30.f.invest_com
    s.invest_com = h30.h.invest_com + e30.e.invest_com
    # d.invest_com = r30.r.invest_com + b30.b.invest_com + i30.i.invest_com + t30.t.invest_com + a30.a.invest_com + l30.l.invest_com
    d.invest_com = (
        r30.r.invest_com
        + b30.b.invest_com
        + i30.i.invest_com
        + t30.t.invest_com
        + a30.a.invest_com
    )
    z.invest_com = s.invest_com + d.invest_com

    # s.invest_outside = h30.h.invest_outside + e30.e.invest_outside + f30.f.invest_outside
    s.invest_outside = e30.e.invest_outside + f30.f.invest_outside
    # d.invest_outside = r30.r.invest_outside + b30.b.invest_outside + i30.i.invest_outside + t30.t.invest_outside + a30.a.invest_outside + l30.l.invest_outside
    d.invest_outside = i30.i.invest_outside + a30.a.invest_outside
    z.invest_outside = s.invest_outside + d.invest_outside

    s.cost_wage = h30.h.cost_wage + e30.e.cost_wage + f30.f.cost_wage
    d.cost_wage = (
        r30.r.cost_wage
        + b30.b.cost_wage
        + i30.i.cost_wage
        + t30.t.cost_wage
        + a30.a.cost_wage
        + l30.l.cost_wage
    )
    z.cost_wage = s.cost_wage + d.cost_wage

    s.demand_emplo = h30.h.demand_emplo + e30.e.demand_emplo + f30.f.demand_emplo
    d.demand_emplo = (
        r30.r.demand_emplo
        + b30.b.demand_emplo
        + i30.i.demand_emplo
        + t30.t.demand_emplo
        + a30.a.demand_emplo
        + l30.l.demand_emplo
    )
    z.demand_emplo = s.demand_emplo + d.demand_emplo

    s.demand_emplo_new = (
        h30.h.demand_emplo_new + e30.e.demand_emplo_new + f30.f.demand_emplo_new
    )
    d.demand_emplo_new = (
        r30.r.demand_emplo_new
        + b30.b.demand_emplo_new
        + i30.i.demand_emplo_new
        + t30.t.demand_emplo_new
        + a30.a.demand_emplo_new
        + l30.l.demand_emplo_new
    )
    z.demand_emplo_new = s.demand_emplo_new + d.demand_emplo_new

    # s.demand_emplo_com = h30.h.demand_emplo_com + e30.e.demand_emplo_com + f30.f.demand_emplo_com
    s.demand_emplo_com = h30.h.demand_emplo_com
    # d.demand_emplo_com = r30.r.demand_emplo_com + b30.b.demand_emplo_com + i30.i.demand_emplo_com + t30.t.demand_emplo_com + a30.a.demand_emplo_com + l30.l.demand_emplo_com
    d.demand_emplo_com = (
        r30.r.demand_emplo_com
        + b30.b.demand_emplo_com
        + t30.t.demand_emplo_com
        + a30.a.demand_emplo_com
    )
    z.demand_emplo_com = s.demand_emplo_com + d.demand_emplo_com

    # ==========Extra Calculations=====================

    m183X.CO2e_per_capita_nat = div(
        fact("Fact_M_CO2e_w_lulucf_2018"), entry("In_M_population_nat")
    )
    m183X.CO2e_per_capita_com = div(z.CO2e_total_18, entry("In_M_population_com_2018"))
    m183X.CO2e_per_capita_com_pct_of_nat = div(
        m183X.CO2e_per_capita_com, m183X.CO2e_per_capita_nat
    )

    s.pct_energy_18 = 1
    d.pct_energy_18 = 1

    e.pct_energy_18 = div(e18.p.energy, s.energy_18)
    h.pct_energy_18 = div(h18.p.energy, s.energy_18)
    f.pct_energy_18 = div(f18.p.energy, s.energy_18)

    rb.pct_energy_18 = div(b18.rb.energy, d.energy_18)
    r.pct_energy_18 = div(r18.p.energy, d.energy_18)
    b.pct_energy_18 = div(b18.p.energy, d.energy_18)
    i.pct_energy_18 = div(i18.p.energy, d.energy_18)
    t.pct_energy_18 = div(t18.t.energy, d.energy_18)
    a.pct_energy_18 = div(a18.p.energy, d.energy_18)

    z.pct_CO2e_total_18 = 1
    s.pct_CO2e_total_18 = div(s.CO2e_total_18, z.CO2e_total_18)
    d.pct_CO2e_total_18 = div(d.CO2e_total_18, z.CO2e_total_18)

    e.pct_CO2e_total_18 = div(e18.e.CO2e_total, z.CO2e_total_18)
    h.pct_CO2e_total_18 = div(h18.h.CO2e_total, z.CO2e_total_18)
    f.pct_CO2e_total_18 = div(f18.f.CO2e_total, z.CO2e_total_18)

    rb.pct_CO2e_total_18 = div(b18.rb.CO2e_total, z.CO2e_total_18)
    r.pct_CO2e_total_18 = div(r18.r.CO2e_total, z.CO2e_total_18)
    b.pct_CO2e_total_18 = div(b18.b.CO2e_total, z.CO2e_total_18)
    i.pct_CO2e_total_18 = div(i18.i.CO2e_total, z.CO2e_total_18)
    t.pct_CO2e_total_18 = div(t18.t.CO2e_total, z.CO2e_total_18)
    a.pct_CO2e_total_18 = div(a18.a.CO2e_total, z.CO2e_total_18)
    l.pct_CO2e_total_18 = div(l18.l.CO2e_total, z.CO2e_total_18)

    s.pct_energy_30 = 1
    d.pct_energy_30 = 1

    e.pct_energy_30 = div(e30.p.energy, s.energy_30)
    h.pct_energy_30 = div(h30.p.energy, s.energy_30)
    f.pct_energy_30 = div(f30.p.energy, s.energy_30)

    rb.pct_energy_30 = div(b30.rb.energy, d.energy_30)
    r.pct_energy_30 = div(r30.p.energy, d.energy_30)
    b.pct_energy_30 = div(b30.p.energy, d.energy_30)
    i.pct_energy_30 = div(i30.p.energy, d.energy_30)
    t.pct_energy_30 = div(t30.t.energy, d.energy_30)
    a.pct_energy_30 = div(a30.p.energy, d.energy_30)

    z.pct_CO2e_total_30 = 1
    s.pct_CO2e_total_30 = div(s.CO2e_total_30, z.CO2e_total_30)
    d.pct_CO2e_total_30 = div(d.CO2e_total_30, z.CO2e_total_30)

    e.pct_CO2e_total_30 = div(e30.e.CO2e_total, z.CO2e_total_30)
    h.pct_CO2e_total_30 = div(h30.h.CO2e_total, z.CO2e_total_30)
    f.pct_CO2e_total_30 = div(f30.f.CO2e_total, z.CO2e_total_30)

    rb.pct_CO2e_total_30 = div(b30.rb.CO2e_total, z.CO2e_total_30)
    r.pct_CO2e_total_30 = div(r30.r.CO2e_total, z.CO2e_total_30)
    b.pct_CO2e_total_30 = div(b30.b.CO2e_total, z.CO2e_total_30)
    i.pct_CO2e_total_30 = div(i30.i.CO2e_total, z.CO2e_total_30)
    t.pct_CO2e_total_30 = div(t30.t.CO2e_total, z.CO2e_total_30)
    a.pct_CO2e_total_30 = div(a30.a.CO2e_total, z.CO2e_total_30)
