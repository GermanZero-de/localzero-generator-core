# pyright: strict

from dataclasses import dataclass, field

from .makeentries import Entries
from .refdata import Facts
from .utils import div

from .electricity2018.e18 import E18
from .business2018.b18 import B18
from .industry2018.i18 import I18
from .transport2018.t18 import T18
from .residences2018.r18 import R18
from .agri2018.a18 import A18
from .heat2018.h18 import H18
from .lulucf2018.l18 import L18
from .fuels2018.f18 import F18
from .waste2018 import W18

from .electricity2030.e30 import E30
from .business2030.b30 import B30
from .industry2030.i30 import I30
from .transport2030.t30 import T30
from .residences2030.r30 import R30
from .agri2030.a30 import A30
from .heat2030.h30 import H30
from .lulucf2030.l30 import L30
from .fuels2030.f30 import F30
from .waste2030 import W30


@dataclass(kw_only=True)
class ZColVars:
    energy_18: float = None  # type: ignore
    pct_energy_18: float = None  # type: ignore
    CO2e_production_based_18: float = None  # type: ignore
    CO2e_combustion_based_18: float = None  # type: ignore
    CO2e_total_18: float = None  # type: ignore
    pct_CO2e_total_18: float = None  # type: ignore

    energy_30: float = None  # type: ignore
    pct_energy_30: float = None  # type: ignore
    CO2e_production_based_30: float = None  # type: ignore
    CO2e_combustion_based_30: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total_30: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    invest_pct: float = None  # type: ignore
    cost_climate_saved_pct: float = None  # type: ignore
    demand_emplo_new_pct: float = None  # type: ignore


# definition of variable names for sector M(ethodology) - there are no rows or columns in the excel!
@dataclass(kw_only=True)
class M183X:
    # year_target: float = None
    # duration_target: float = None
    # duration_target_until_2050: float = None
    # duration_neutral: float = None

    CO2_budget_2016_to_year_target: float = None  # type: ignore
    nonCO2_budget_2016_to_year_target: float = None  # type: ignore
    GHG_budget_2016_to_year_target: float = None  # type: ignore
    GHG_budget_2022_to_year_target: float = None  # type: ignore
    GHG_budget_after_year_target: float = None  # type: ignore

    CO2e_w_lulucf_change_pa: float = None  # type: ignore

    CO2e_lulucf_2015: float = None  # type: ignore
    CO2e_lulucf_2016: float = None  # type: ignore
    CO2e_lulucf_2017: float = None  # type: ignore
    CO2e_lulucf_2018: float = None  # type: ignore
    CO2e_lulucf_2019: float = None  # type: ignore
    CO2e_lulucf_2020: float = None  # type: ignore
    CO2e_lulucf_2021: float = None  # type: ignore

    CO2e_wo_lulucf_2015: float = None  # type: ignore
    CO2e_wo_lulucf_2016: float = None  # type: ignore
    CO2e_wo_lulucf_2017: float = None  # type: ignore
    CO2e_wo_lulucf_2018: float = None  # type: ignore
    CO2e_wo_lulucf_2019: float = None  # type: ignore
    CO2e_wo_lulucf_2020: float = None  # type: ignore
    CO2e_wo_lulucf_2021: float = None  # type: ignore

    CO2e_w_lulucf_2015: float = None  # type: ignore
    CO2e_w_lulucf_2016: float = None  # type: ignore
    CO2e_w_lulucf_2017: float = None  # type: ignore
    CO2e_w_lulucf_2018: float = None  # type: ignore
    CO2e_w_lulucf_2019: float = None  # type: ignore
    CO2e_w_lulucf_2020: float = None  # type: ignore
    CO2e_w_lulucf_2021: float = None  # type: ignore
    CO2e_w_lulucf_2022: float = None  # type: ignore
    CO2e_w_lulucf_2023: float = None  # type: ignore
    CO2e_w_lulucf_2024: float = None  # type: ignore
    CO2e_w_lulucf_2025: float = None  # type: ignore
    CO2e_w_lulucf_2026: float = None  # type: ignore
    CO2e_w_lulucf_2027: float = None  # type: ignore
    CO2e_w_lulucf_2028: float = None  # type: ignore
    CO2e_w_lulucf_2029: float = None  # type: ignore
    CO2e_w_lulucf_2030: float = None  # type: ignore
    CO2e_w_lulucf_2031: float = None  # type: ignore
    CO2e_w_lulucf_2032: float = None  # type: ignore
    CO2e_w_lulucf_2033: float = None  # type: ignore
    CO2e_w_lulucf_2034: float = None  # type: ignore
    CO2e_w_lulucf_2035: float = None  # type: ignore
    CO2e_w_lulucf_2036: float = None  # type: ignore
    CO2e_w_lulucf_2037: float = None  # type: ignore
    CO2e_w_lulucf_2038: float = None  # type: ignore
    CO2e_w_lulucf_2039: float = None  # type: ignore
    CO2e_w_lulucf_2040: float = None  # type: ignore
    CO2e_w_lulucf_2041: float = None  # type: ignore
    CO2e_w_lulucf_2042: float = None  # type: ignore
    CO2e_w_lulucf_2043: float = None  # type: ignore
    CO2e_w_lulucf_2044: float = None  # type: ignore
    CO2e_w_lulucf_2045: float = None  # type: ignore
    CO2e_w_lulucf_2046: float = None  # type: ignore
    CO2e_w_lulucf_2047: float = None  # type: ignore
    CO2e_w_lulucf_2048: float = None  # type: ignore
    CO2e_w_lulucf_2049: float = None  # type: ignore
    CO2e_w_lulucf_2050: float = None  # type: ignore
    CO2e_w_lulucf_2051: float = None  # type: ignore

    # =======Z-Script Varaibles=============================

    CO2e_lulucf_203X: float = None  # type: ignore
    CO2e_wo_lulucf_203X: float = None  # type: ignore
    CO2e_w_lulucf_203X: float = None  # type: ignore

    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore

    z: ZColVars = field(default_factory=ZColVars)
    s: ZColVars = field(default_factory=ZColVars)
    d: ZColVars = field(default_factory=ZColVars)

    e: ZColVars = field(default_factory=ZColVars)
    h: ZColVars = field(default_factory=ZColVars)
    f: ZColVars = field(default_factory=ZColVars)
    rb: ZColVars = field(default_factory=ZColVars)
    r: ZColVars = field(default_factory=ZColVars)
    b: ZColVars = field(default_factory=ZColVars)
    t: ZColVars = field(default_factory=ZColVars)
    i: ZColVars = field(default_factory=ZColVars)
    a: ZColVars = field(default_factory=ZColVars)
    l: ZColVars = field(default_factory=ZColVars)
    w: ZColVars = field(default_factory=ZColVars)

    CO2e_per_capita_nat: float = None  # type: ignore
    CO2e_per_capita_com: float = None  # type: ignore
    CO2e_per_capita_com_pct_of_nat: float = None  # type: ignore

    GHG_budget_2022_to_year_target_nat: float = None  # type: ignore  # INFO THG Budget Deutschland
    CO2e_2022_to_year_target: float = None  # type: ignore  # INFO CO2e sind Emissionen für Kommune


def calc_budget(
    entries: Entries,
    facts: Facts,
    *,
    a18: A18,
    b18: B18,
    e18: E18,
    f18: F18,
    h18: H18,
    i18: I18,
    l18: L18,
    r18: R18,
    t18: T18,
    w18: W18,
) -> M183X:
    """Calculate the budget needed."""

    fact = facts.fact

    population_commune_2018 = entries.m_population_com_2018
    population_germany_2018 = entries.m_population_nat

    ######################################
    ### budgets 2016 until target year ###
    ######################################

    m183X = M183X()
    # local greenhouse gas budget from 2016 until target year in com!!
    m183X.GHG_budget_2016_to_year_target = (
        entries.m_GHG_budget_2016_to_year_target
        * population_commune_2018
        / population_germany_2018
    )

    # local nonCO2 budget from 2016 until target year in com!!
    m183X.nonCO2_budget_2016_to_year_target = (
        entries.m_nonCO2_budget_2016_to_year_target
        * population_commune_2018
        / population_germany_2018
    )

    # local CO2 budget from 2016 until infinity
    m183X.CO2_budget_2016_to_year_target = (
        m183X.GHG_budget_2016_to_year_target - m183X.nonCO2_budget_2016_to_year_target
    )

    ################################################
    ### year_ref as base for emissions 2016-2021 ###
    ################################################
    ### beginning with LULUCF                    ###
    ################################################
    year_baseline = entries.m_year_baseline
    year_before_baseline = year_baseline - 1
    year_ref = entries.m_year_ref

    years_list_2015_to_year_before_baseline = list(range(2015, year_baseline))
    years_list_2016_to_year_before_baseline = list(range(2016, year_baseline))

    years_list_2015_to_year_before_baseline_wo_year_ref = (
        years_list_2015_to_year_before_baseline.copy()
    )
    years_list_2015_to_year_before_baseline_wo_year_ref.remove(year_ref)

    years_list_2015_to_2051 = list(range(2015, 2052))

    years_predicted = list(range(year_baseline, 2052))

    years_dict: dict[int, dict[str, float]] = {
        year: {} for year in years_list_2015_to_year_before_baseline
    }

    # get the CO2e of LULUCF for year_ref as calculated
    years_dict[year_ref]["CO2e_lulucf"] = l18.l.CO2e_total

    # calculate the CO2e of LULUCF for 2015-2021 by multiplying year_ref's value with percentage
    # 2015 just as a backup, probably not needed

    for year in years_list_2015_to_year_before_baseline_wo_year_ref:
        years_dict[year]["CO2e_lulucf"] = years_dict[year_ref]["CO2e_lulucf"] * fact(
            f"Fact_M_CO2e_lulucf_{year}_vs_year_ref"
        )

    ################################################
    ### year_ref as base for emissions 2016-2021 ###
    ################################################
    ### second emissions without (wo) LULUCF     ###
    ################################################

    # get the CO2e of all sectors for year_ref excluding LULUCF since this is negative
    years_dict[year_ref]["CO2e_wo_lulucf"] = (
        h18.h.CO2e_total
        + e18.e.CO2e_total
        + f18.f.CO2e_total
        + r18.r.CO2e_total
        + b18.b.CO2e_total
        + i18.i.CO2e_total
        + t18.t.CO2e_total
        + a18.a.CO2e_total
        + w18.w.CO2e_total
    )

    # calculate the CO2e of all sectors without LULUCF for 2015-2021 by multiplying year_ref's value with percentage
    # 2015 just as a backup, probably not needed
    for year in years_list_2015_to_year_before_baseline_wo_year_ref:
        years_dict[year]["CO2e_wo_lulucf"] = years_dict[year_ref][
            "CO2e_wo_lulucf"
        ] * fact(f"Fact_M_CO2e_wo_lulucf_{year}_vs_year_ref")

    #################################################
    ### year_ref as base for emissions 2016-2021  ###
    #################################################
    ### sum up CO2e_wo_lulucf and CO2e_lulucf     ###
    #################################################

    # 2015 just as a backup, probably not needed
    for year in years_list_2015_to_year_before_baseline:
        years_dict[year]["CO2e_w_lulucf"] = (
            years_dict[year]["CO2e_wo_lulucf"] + years_dict[year]["CO2e_lulucf"]
        )

    ####################################################################
    ### remaining local greenhouse gas budget 2022 until target year ###
    ####################################################################

    temp_val = m183X.GHG_budget_2016_to_year_target
    for year in years_list_2016_to_year_before_baseline:
        temp_val -= years_dict[year]["CO2e_w_lulucf"]

    m183X.GHG_budget_2022_to_year_target = temp_val

    #########################################################
    ### calculating the linear decrease until target year ###
    #########################################################
    ### these values are used for reduction path          ###
    #########################################################

    # calculating the yearly decrease of the emissions, going down linearly to 0 in target_year+1
    m183X.CO2e_w_lulucf_change_pa = years_dict[year_before_baseline][
        "CO2e_w_lulucf"
    ] / (
        entries.m_year_target
        - (year_before_baseline)
        + 1  # TODO end of 2022,  substract year 2021 as emissions are only known until that year
    )  # +1 because we want to reach 0 in target_year+1
    # reducing the yearly emissions year by year, starting with 2022

    for year in years_predicted:
        # INFO  '> 1' instead '> 0' to avoid having very small numbers such as 0.00000001 and unwanted additional substraction of CO2e_w_lulucf_change_pa
        if years_dict[year - 1]["CO2e_w_lulucf"] > 1:
            years_dict[year] = {
                "CO2e_w_lulucf": (
                    years_dict[year - 1]["CO2e_w_lulucf"]
                    - m183X.CO2e_w_lulucf_change_pa
                )
            }
        else:
            years_dict[year] = {"CO2e_w_lulucf": 0}

    ##############################################################################################
    ### remaining local greenhouse gas budget after reaching climate neutrality in target year ###
    ##############################################################################################

    # all emission values until 2051 are subtracted since they are 0 after target year
    temp_val = m183X.GHG_budget_2022_to_year_target
    for year in years_predicted:
        temp_val -= years_dict[year]["CO2e_w_lulucf"]
    m183X.GHG_budget_after_year_target = temp_val

    temp_val = entries.m_GHG_budget_2016_to_year_target
    for year in years_list_2016_to_year_before_baseline:
        temp_val -= fact(f"Fact_M_CO2e_lulucf_{year}") + fact(
            f"Fact_M_CO2e_wo_lulucf_{year}"
        )

    m183X.GHG_budget_2022_to_year_target_nat = temp_val

    m183X.CO2e_2022_to_year_target = (
        m183X.GHG_budget_2022_to_year_target - m183X.GHG_budget_after_year_target
    )

    # safe dict values in class variables
    (
        m183X.CO2e_lulucf_2015,
        m183X.CO2e_lulucf_2016,
        m183X.CO2e_lulucf_2017,
        m183X.CO2e_lulucf_2018,
        m183X.CO2e_lulucf_2019,
        m183X.CO2e_lulucf_2020,
        m183X.CO2e_lulucf_2021,
    ) = [
        years_dict[year]["CO2e_lulucf"]
        for year in years_list_2015_to_year_before_baseline
    ]

    (
        m183X.CO2e_wo_lulucf_2015,
        m183X.CO2e_wo_lulucf_2016,
        m183X.CO2e_wo_lulucf_2017,
        m183X.CO2e_wo_lulucf_2018,
        m183X.CO2e_wo_lulucf_2019,
        m183X.CO2e_wo_lulucf_2020,
        m183X.CO2e_wo_lulucf_2021,
    ) = [
        years_dict[year]["CO2e_wo_lulucf"]
        for year in years_list_2015_to_year_before_baseline
    ]

    (
        m183X.CO2e_w_lulucf_2015,
        m183X.CO2e_w_lulucf_2016,
        m183X.CO2e_w_lulucf_2017,
        m183X.CO2e_w_lulucf_2018,
        m183X.CO2e_w_lulucf_2019,
        m183X.CO2e_w_lulucf_2020,
        m183X.CO2e_w_lulucf_2021,
        m183X.CO2e_w_lulucf_2022,
        m183X.CO2e_w_lulucf_2023,
        m183X.CO2e_w_lulucf_2024,
        m183X.CO2e_w_lulucf_2025,
        m183X.CO2e_w_lulucf_2026,
        m183X.CO2e_w_lulucf_2027,
        m183X.CO2e_w_lulucf_2028,
        m183X.CO2e_w_lulucf_2029,
        m183X.CO2e_w_lulucf_2030,
        m183X.CO2e_w_lulucf_2031,
        m183X.CO2e_w_lulucf_2032,
        m183X.CO2e_w_lulucf_2033,
        m183X.CO2e_w_lulucf_2034,
        m183X.CO2e_w_lulucf_2035,
        m183X.CO2e_w_lulucf_2036,
        m183X.CO2e_w_lulucf_2037,
        m183X.CO2e_w_lulucf_2038,
        m183X.CO2e_w_lulucf_2039,
        m183X.CO2e_w_lulucf_2040,
        m183X.CO2e_w_lulucf_2041,
        m183X.CO2e_w_lulucf_2042,
        m183X.CO2e_w_lulucf_2043,
        m183X.CO2e_w_lulucf_2044,
        m183X.CO2e_w_lulucf_2045,
        m183X.CO2e_w_lulucf_2046,
        m183X.CO2e_w_lulucf_2047,
        m183X.CO2e_w_lulucf_2048,
        m183X.CO2e_w_lulucf_2049,
        m183X.CO2e_w_lulucf_2050,
        m183X.CO2e_w_lulucf_2051,
    ) = [years_dict[year]["CO2e_w_lulucf"] for year in years_list_2015_to_2051]

    return m183X


def calc_z(
    entries: Entries,
    facts: Facts,
    *,
    m183X: M183X,
    a18: A18,
    b18: B18,
    e18: E18,
    f18: F18,
    h18: H18,
    i18: I18,
    l18: L18,
    r18: R18,
    t18: T18,
    w18: W18,
    a30: A30,
    b30: B30,
    e30: E30,
    f30: F30,
    h30: H30,
    i30: I30,
    l30: L30,
    r30: R30,
    t30: T30,
    w30: W30,
):
    """This updates several values in m183X inplace."""

    fact = facts.fact

    duration_CO2e_neutral_years = entries.m_duration_neutral

    population_commune_2018 = entries.m_population_com_2018
    population_germany_2018 = entries.m_population_nat

    ##################################################################
    ### total emissions 203X, saved emissions, saved climate costs ###
    ##################################################################

    # get the CO2e of all sectors for 203X (the target year) excluding LULUCF
    # TODO: Warum exkludieren wir LULUCF?
    #   Weil es negativ ist?  Dann müssten wir auch Fuels2030 exkludieren?
    #   Ist es die Pyrolyse?
    m183X.CO2e_wo_lulucf_203X = (
        h30.h.CO2e_total
        + e30.e.CO2e_total
        + f30.f.CO2e_total
        + r30.r.CO2e_total
        + b30.b.CO2e_total
        + i30.i.CO2e_total
        + t30.t.transport.CO2e_total
        + a30.a.CO2e_total
        + w30.w.CO2e_total
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
        + t30.t.transport.cost_climate_saved
        + a30.a.cost_climate_saved
        + l30.l.cost_climate_saved
        + w30.w.cost_climate_saved
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
    w = m183X.w

    s.energy_18 = h18.p.energy + e18.p.energy + f18.p.energy
    d.energy_18 = (
        r18.p.energy
        + b18.p.energy
        + i18.p.energy
        + t18.t.energy
        + a18.p.energy
        + w18.p.energy
    )
    z.energy_18 = s.energy_18

    s.CO2e_production_based_18 = (
        h18.h.CO2e_production_based
        + e18.e.CO2e_production_based
        + f18.f.CO2e_production_based
    )
    d.CO2e_production_based_18 = (
        i18.i.CO2e_production_based
        + a18.a.CO2e_production_based
        + l18.l.CO2e_production_based
        + w18.w.CO2e_production_based
        # + r18.r.CO2e_production_based
        # + b18.b.CO2e_production_based
        # + t18.t.CO2e_production_based
    )
    z.CO2e_production_based_18 = s.CO2e_production_based_18 + d.CO2e_production_based_18

    s.CO2e_combustion_based_18 = (
        h18.h.CO2e_combustion_based
        + e18.e.CO2e_combustion_based
        + f18.f.CO2e_combustion_based
    )
    d.CO2e_combustion_based_18 = (
        r18.r.CO2e_combustion_based
        + b18.b.CO2e_combustion_based
        + i18.i.CO2e_combustion_based
        + t18.t.CO2e_combustion_based
        + a18.a.CO2e_combustion_based
        + l18.l.CO2e_combustion_based
        # + w18.w.CO2e_combustion_based = 0 ### <--- no combustion based emissions in waste sector
    )
    z.CO2e_combustion_based_18 = s.CO2e_combustion_based_18 + d.CO2e_combustion_based_18

    s.CO2e_total_18 = h18.h.CO2e_total + e18.e.CO2e_total + f18.f.CO2e_total
    d.CO2e_total_18 = (
        r18.r.CO2e_total
        + b18.b.CO2e_total
        + i18.i.CO2e_total
        + t18.t.CO2e_total
        + a18.a.CO2e_total
        + l18.l.CO2e_total
        + w18.w.CO2e_total
    )
    z.CO2e_total_18 = s.CO2e_total_18 + d.CO2e_total_18

    s.energy_30 = h30.p.energy + e30.p.energy + f30.p.energy
    d.energy_30 = (
        r30.p.energy
        + b30.p.energy
        + i30.p.energy
        + t30.t.transport.energy
        + a30.p.energy
        + w30.w.energy
    )
    z.energy_30 = s.energy_30

    s.CO2e_production_based_30 = (
        h30.h.CO2e_production_based
        + f30.f.CO2e_production_based
        # + e30.e.CO2e_production_based
    )
    d.CO2e_production_based_30 = (
        i30.i.CO2e_production_based
        + a30.a.CO2e_production_based
        + l30.l.CO2e_production_based
        + w30.w.CO2e_production_based
        # + r30.r.CO2e_production_based
        # + b30.b.CO2e_production_based
        # + t30.t.CO2e_production_based
    )
    z.CO2e_production_based_30 = s.CO2e_production_based_30 + d.CO2e_production_based_30

    s.CO2e_combustion_based_30 = (
        h30.h.CO2e_combustion_based
        + e30.e.CO2e_combustion_based
        # + f30.f.CO2e_combustion_based
    )
    d.CO2e_combustion_based_30 = (
        r30.r.CO2e_combustion_based
        + b30.b.CO2e_combustion_based
        + i30.i.CO2e_combustion_based
        + t30.t.transport.CO2e_combustion_based
        + a30.a.CO2e_combustion_based
        + l30.l.CO2e_combustion_based
        # + w30.w.CO2e_combustion_based = 0 ### <--- no combustion based emissions in waste sector
    )
    z.CO2e_combustion_based_30 = s.CO2e_combustion_based_30 + d.CO2e_combustion_based_30

    z.CO2e_combustion_based_per_MWh = div(z.CO2e_combustion_based_30, z.energy_30)

    s.CO2e_total_30 = h30.h.CO2e_total + e30.e.CO2e_total + f30.f.CO2e_total
    d.CO2e_total_30 = (
        r30.r.CO2e_total
        + b30.b.CO2e_total
        + i30.i.CO2e_total
        + t30.t.transport.CO2e_total
        + a30.a.CO2e_total
        + l30.l.CO2e_total
        + w30.w.CO2e_total
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

    s.change_CO2e_pct = div(s.CO2e_total_30, s.CO2e_total_18)
    d.change_CO2e_pct = div(d.CO2e_total_30, d.CO2e_total_18)
    z.change_CO2e_pct = div(z.CO2e_total_30, z.CO2e_total_18)

    s.CO2e_total_2021_estimated = s.CO2e_total_18 * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_year_ref"
    )
    d.CO2e_total_2021_estimated = d.CO2e_total_18 * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_year_ref"
    )
    z.CO2e_total_2021_estimated = (
        s.CO2e_total_2021_estimated + d.CO2e_total_2021_estimated
    )

    s.cost_climate_saved = (
        (s.CO2e_total_2021_estimated - s.CO2e_total_30)
        * duration_CO2e_neutral_years
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    d.cost_climate_saved = (
        (d.CO2e_total_2021_estimated - d.CO2e_total_30)
        * duration_CO2e_neutral_years
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
        + w30.w.invest_pa
    )
    z.invest_pa = s.invest_pa + d.invest_pa

    s.invest_pa_com = h30.h.invest_pa_com + e30.e.invest_pa_com  # + f30.f.invest_pa_com
    d.invest_pa_com = (
        r30.r.invest_pa_com
        + b30.b.invest_pa_com
        + i30.i.invest_pa_com
        + t30.t.invest_pa_com
        + a30.a.invest_pa_com
        + w30.w.invest_pa_com
        # + l30.l.invest_pa_com
    )
    z.invest_pa_com = s.invest_pa_com + d.invest_pa_com

    s.invest_pa_outside = (
        e30.e.invest_pa_outside
        + f30.f.invest_pa_outside
        # + h30.h.invest_pa_outside
    )
    d.invest_pa_outside = (
        i30.i.invest_pa_outside
        + a30.a.invest_pa_outside
        # + r30.r.invest_pa_outside
        # + b30.b.invest_pa_outside
        # + t30.t.invest_pa_outside
        # + l30.l.invest_pa_outside
    )
    z.invest_pa_outside = s.invest_pa_outside + d.invest_pa_outside

    s.invest = h30.h.invest + e30.e.invest + f30.f.invest
    d.invest = (
        r30.r.invest
        + b30.b.invest
        + i30.i.invest
        + t30.t.invest
        + a30.a.invest
        + l30.l.invest
        + w30.w.invest
    )
    z.invest = s.invest + d.invest

    s.invest_com = (
        h30.h.invest_com
        + e30.e.invest_com
        # + f30.f.invest_com
    )
    d.invest_com = (
        r30.r.invest_com
        + b30.b.invest_com
        + i30.i.invest_com
        + t30.t.invest_com
        + a30.a.invest_com
        + w30.w.invest_com
        # + l30.l.invest_com
    )
    z.invest_com = s.invest_com + d.invest_com

    s.invest_outside = (
        e30.e.invest_outside
        + f30.f.invest_outside
        # + h30.h.invest_outside
    )
    d.invest_outside = (
        i30.i.invest_outside
        + a30.a.invest_outside
        # + r30.r.invest_outside
        # + b30.b.invest_outside
        # + t30.t.invest_outside
        # + l30.l.invest_outside
    )
    z.invest_outside = s.invest_outside + d.invest_outside

    s.cost_wage = h30.h.cost_wage + e30.e.cost_wage + f30.f.cost_wage
    d.cost_wage = (
        r30.r.cost_wage
        + b30.b.cost_wage
        + i30.i.cost_wage
        + t30.t.cost_wage
        + a30.a.cost_wage
        + l30.l.cost_wage
        + w30.w.cost_wage
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
        + w30.w.demand_emplo
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
        + w30.w.demand_emplo_new
    )
    z.demand_emplo_new = s.demand_emplo_new + d.demand_emplo_new

    s.demand_emplo_com = (
        h30.h.demand_emplo_com
        # + e30.e.demand_emplo_com
        # + f30.f.demand_emplo_com
    )
    d.demand_emplo_com = (
        r30.r.demand_emplo_com
        + b30.b.demand_emplo_com
        + t30.t.demand_emplo_com
        + a30.a.demand_emplo_com
        # + i30.i.demand_emplo_com
        # + l30.l.demand_emplo_com
    )
    z.demand_emplo_com = s.demand_emplo_com + d.demand_emplo_com

    # ==========Extra Calculations=====================

    m183X.CO2e_per_capita_nat = div(
        fact("Fact_M_CO2e_wo_lulucf_2018") + fact("Fact_M_CO2e_lulucf_2018"),
        population_germany_2018,
    )
    m183X.CO2e_per_capita_com = div(z.CO2e_total_18, population_commune_2018)
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
    w.pct_energy_18 = div(w18.p.energy, d.energy_18)

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
    w.pct_CO2e_total_18 = div(w18.w.CO2e_total, z.CO2e_total_18)

    s.pct_energy_30 = 1
    d.pct_energy_30 = 1

    e.pct_energy_30 = div(e30.p.energy, s.energy_30)
    h.pct_energy_30 = div(h30.p.energy, s.energy_30)
    f.pct_energy_30 = div(f30.p.energy, s.energy_30)

    rb.pct_energy_30 = div(b30.rb.energy, d.energy_30)
    r.pct_energy_30 = div(r30.p.energy, d.energy_30)
    b.pct_energy_30 = div(b30.p.energy, d.energy_30)
    i.pct_energy_30 = div(i30.p.energy, d.energy_30)
    t.pct_energy_30 = div(t30.t.transport.energy, d.energy_30)
    a.pct_energy_30 = div(a30.p.energy, d.energy_30)
    w.pct_energy_30 = div(w30.w.energy, d.energy_30)

    h.invest_pct = div(h30.h.invest, z.invest)
    e.invest_pct = div(e30.e.invest, z.invest)
    f.invest_pct = div(f30.f.invest, z.invest)
    r.invest_pct = div(r30.r.invest, z.invest)
    b.invest_pct = div(b30.b.invest, z.invest)
    i.invest_pct = div(i30.i.invest, z.invest)
    t.invest_pct = div(t30.t.invest, z.invest)
    a.invest_pct = div(a30.a.invest, z.invest)
    l.invest_pct = div(l30.l.invest, z.invest)
    w.invest_pct = div(w30.w.invest, z.invest)

    h.cost_climate_saved_pct = div(h30.h.cost_climate_saved, z.cost_climate_saved)
    e.cost_climate_saved_pct = div(e30.e.cost_climate_saved, z.cost_climate_saved)
    f.cost_climate_saved_pct = div(f30.f.cost_climate_saved, z.cost_climate_saved)
    r.cost_climate_saved_pct = div(r30.r.cost_climate_saved, z.cost_climate_saved)
    b.cost_climate_saved_pct = div(b30.b.cost_climate_saved, z.cost_climate_saved)
    i.cost_climate_saved_pct = div(i30.i.cost_climate_saved, z.cost_climate_saved)
    t.cost_climate_saved_pct = div(
        t30.t.transport.cost_climate_saved, z.cost_climate_saved
    )
    a.cost_climate_saved_pct = div(a30.a.cost_climate_saved, z.cost_climate_saved)
    l.cost_climate_saved_pct = div(l30.l.cost_climate_saved, z.cost_climate_saved)
    w.cost_climate_saved_pct = div(w30.w.cost_climate_saved, z.cost_climate_saved)

    h.demand_emplo_new_pct = div(h30.h.demand_emplo_new, z.demand_emplo_new)
    e.demand_emplo_new_pct = div(e30.e.demand_emplo_new, z.demand_emplo_new)
    f.demand_emplo_new_pct = div(f30.f.demand_emplo_new, z.demand_emplo_new)
    r.demand_emplo_new_pct = div(r30.r.demand_emplo_new, z.demand_emplo_new)
    b.demand_emplo_new_pct = div(b30.b.demand_emplo_new, z.demand_emplo_new)
    i.demand_emplo_new_pct = div(i30.i.demand_emplo_new, z.demand_emplo_new)
    t.demand_emplo_new_pct = div(t30.t.demand_emplo_new, z.demand_emplo_new)
    a.demand_emplo_new_pct = div(a30.a.demand_emplo_new, z.demand_emplo_new)
    l.demand_emplo_new_pct = div(l30.l.demand_emplo_new, z.demand_emplo_new)
    w.demand_emplo_new_pct = div(w30.w.demand_emplo_new, z.demand_emplo_new)
