from dataclasses import dataclass, asdict
from .inputs import Inputs

# definition of variable names for sector M(ethodology) - there are no rows or columns in the excel!
@dataclass
class M183X:
    year_today: float = None
    year_target: float = None
    duration_target: float = None
    duration_target_until_2050: float = None
    duration_neutral: float = None

    CO2_budget_2016_to_year_target: float = None
    nonCO2_budget_2016_to_year: float = None
    GHG_budget_2016_to_year: float = None

    CO2e_w_lulucf_change_pa:float = None

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
    CO2e_w_lulucf_2041: float = None
    CO2e_w_lulucf_2043: float = None
    CO2e_w_lulucf_2044: float = None
    CO2e_w_lulucf_2045: float = None
    CO2e_w_lulucf_2046: float = None
    CO2e_w_lulucf_2047: float = None
    CO2e_w_lulucf_2048: float = None
    CO2e_w_lulucf_2049: float = None
    CO2e_w_lulucf_2050: float = None
    CO2e_w_lulucf_2051: float = None

    GHG_budget_2022_to_year_target: float = None
    GHG_budget_after_year_target: float = None

    CO2e_lulucf_203X: float = None
    CO2e_wo_lulucf_203X: float = None
    CO2e_w_lulucf_203X: float = None

    change_CO2e_t: float = None
    change_CO2e_pct: float = None
    cost_climate_saved: float = None

    # erzeuge dictionry
    def dict(self):
        return asdict(self)


# these year calculations have to be done before all sector calculations
def calc_18(inputs: Inputs) -> M183X:
    ###########################
    ### years and durations ###
    ###########################
    def entry(n):
        return inputs.entry(n)

    m183X = M183X()

    m183X.year_today = entry('In_M_year_today')

    m183X.year_target = entry("In_M_year_target")

    #TODO: figure out where "duration target" entry variable  is used in other sector scripts, replace it with "m183X.duration_target" variable ?
    #delete entry variable afterwards

    m183X.duration_target = m183X.year_target - m183X.year_today

    m183X.duration_target_until_2050 = 2050 - m183X.year_target

    # the neutral duration is the average time of climate neutral years until 2050 if we reduce linearly
    # from now to year_target and then stay at this 0 level
    # this value is needed to calculate the saved emissions and climate costs
    m183X.duration_neutral = (
        m183X.duration_target_until_2050 + m183X.duration_target / 2
    )

    return m183X


# these budget calculations have to be done after all sector calculations
def calc_3X(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def entry(n):
        return inputs.entry(n)

    ######################################
    ### budgets 2016 until target year ###
    ######################################

    m183X = root.m183X
    #TODO: add "GHG_budget_2016_to_year_target" to makeentries.py
    # local greenhouse gas budget from 2016 until target year in com!!
    #m183X.GHG_budget_2016_to_year_target = (
    #     entry("GHG_budget_2016_to_year_target")
    #     * entry("In_M_population_com_2018")
    #     / entry("In_M_population_nat")
    #    )
    m183X.GHG_budget_2016_to_year_target = 1

    #TODO: add "nonCO2_budget_2016_to_year_target" to makeentries.py
    # local nonCO2 budget from 2016 until target year in com!!
    #m183X.nonCO2_budget_2016_to_year_target = (
    #    entry("nonCO2_budget_2016_to_year_target")
    #    * entry("In_M_population_com_2018")
    #    / entry("In_M_population_nat")
    #)
    m183X.nonCO2_budget_2016_to_year_target = 1

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
    m183X.CO2e_lulucf_2018 = root.l18.CO2e_total

    # calculate the CO2e of LULUCF for 2015-2017 and 2019-2021 by multiplying 2018's value with percentage
    # 2015 just as a backup, probably not needed
    m183X.CO2e_lulucf_2015 = m183X.CO2e_lulucf_2018 * fact("Fact_M_CO2e_lulucf_2015_vs_2018")

    m183X.CO2e_lulucf_2016 = m183X.CO2e_lulucf_2018 * fact("Fact_M_CO2e_lulucf_2016_vs_2018")

    m183X.CO2e_lulucf_2017 = m183X.CO2e_lulucf_2018 * fact("Fact_M_CO2e_lulucf_2017_vs_2018")

    m183X.CO2e_lulucf_2019 = m183X.CO2e_lulucf_2018 * fact("Fact_M_CO2e_lulucf_2019_vs_2018")

    m183X.CO2e_lulucf_2020 = m183X.CO2e_lulucf_2018 * fact("Fact_M_CO2e_lulucf_2020_vs_2018")

    m183X.CO2e_lulucf_2021 = m183X.CO2e_lulucf_2018 * fact("Fact_M_CO2e_lulucf_2021_vs_2018")

    ############################################
    ### 2018 as base for emissions 2016-2021 ###
    ############################################
    ### second emissions without (wo) LULUCF ###
    ############################################

    # get the CO2e of all sectors for 2018 excluding LULUCF since this is negative
    m183X.CO2e_wo_lulucf_2018 = (
        root.h18.CO2e_total
        + root.e18.CO2e_total
        + root.f18.CO2e_total
        + root.r18.CO2e_total
        + root.b18.CO2e_total
        + root.i18.CO2e_total
        + root.t18.CO2e_total
        + root.a18.CO2e_total
    )

    # calculate the CO2e of all sectors without LULUCF for 2015-2017 and 2019-2021 by multiplying 2018's value with percentage
    # 2015 just as a backup, probably not needed
    m183X.CO2e_wo_lulucf_2015 = m183X.CO2e_wo_lulucf_2018 * fact("Fact_M_CO2e_wo_lulucf_2015_vs_2018")

    m183X.CO2e_wo_lulucf_2016 = m183X.CO2e_wo_lulucf_2018 * fact("Fact_M_CO2e_wo_lulucf_2016_vs_2018")

    m183X.CO2e_wo_lulucf_2017 = m183X.CO2e_wo_lulucf_2018 * fact("Fact_M_CO2e_wo_lulucf_2017_vs_2018")

    m183X.CO2e_wo_lulucf_2019 = m183X.CO2e_wo_lulucf_2018 * fact("Fact_M_CO2e_wo_lulucf_2019_vs_2018")

    m183X.CO2e_wo_lulucf_2020 = m183X.CO2e_wo_lulucf_2018 * fact("Fact_M_CO2e_wo_lulucf_2020_vs_2018")

    m183X.CO2e_wo_lulucf_2021 = m183X.CO2e_wo_lulucf_2018 * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")

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
    m183X.CO2e_w_lulucf_change_pa = m183X.CO2e_w_lulucf_2021 / (m183X.duration_target + 1)  # +1 because we want to reach 0 in target_year+1

    # reducing the yearly emissions year by year, starting with 2022
    if m183X.CO2e_w_lulucf_2021 > 0:
        m183X.CO2e_w_lulucf_2022 = m183X.CO2e_w_lulucf_2021 - m183X.CO2e_w_lulucf_change_pa      )
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

    ##################################################################
    ### total emissions 203X, saved emissions, saved climate costs ###
    ##################################################################

    # get the CO2e of all sectors for 203X (the target year) excluding LULUCF
    m183X.CO2e_wo_lulucf_203X = (
        root.h30.CO2e_total
        + root.e30.CO2e_total
        + root.f30.CO2e_total
        + root.r30.CO2e_total
        + root.b30.CO2e_total
        + root.i30.CO2e_total
        + root.t30.CO2e_total
        + root.a30.CO2e_total
    )

    # get the CO2e of all sectors für 203X (the target year) which should be 0
    m183X.CO2e_w_lulucf_203X = m183X.CO2e_wo_lulucf_203X + m183X.CO2e_lulucf_203X

    # calculate the total CO2e difference in t between 2018 and 203X
    m183X.change_CO2e_t = m183X.CO2e_w_lulucf_203X - m183X.CO2e_w_lulucf_2018

    # calculate the total CO2e difference in % between 2018 and 203X
    m183X.change_CO2e_pct = m183X.change_CO2e_t / m183X.CO2e_w_lulucf_2018

    # get the total saved climate cost of all sectors until 2050
    m183X.cost_climate_saved = (
        root.h30.cost_climate_saved
        + root.e30.cost_climate_saved
        + root.f30.cost_climate_saved
        + root.r30.cost_climate_saved
        + root.b30.cost_climate_saved
        + root.i30.cost_climate_saved
        + root.t30.cost_climate_saved
        + root.a30.cost_climate_saved
        + root.l30.cost_climate_saved
    )
