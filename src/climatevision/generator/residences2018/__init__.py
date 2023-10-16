"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/hh_ghd.html
"""

# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts
from ..utils import div
from ..common.energy import EnergyPerM2PctCommune

from .r18 import R18
from .dataclasses import Vars1, Vars2, Vars3, Vars4
from . import energy_source


def calc(entries: Entries, facts: Facts) -> R18:
    fact = facts.fact

    supply = energy_source.calc_supply(entries, facts)

    ### P - Section ###
    r = Vars1()
    p = Vars2()
    p_elec_elcon = Vars2()
    p_elec_heatpump = Vars2()
    p_vehicles = Vars2()
    p_other = Vars2()

    p_buildings_until_1919 = Vars3(number_of_buildings=entries.r_buildings_until_1919)
    p_buildings_1919_1948 = Vars3(number_of_buildings=entries.r_buildings_1919_1948)
    p_buildings_1949_1978 = Vars3(number_of_buildings=entries.r_buildings_1949_1978)
    p_buildings_1979_1995 = Vars3(
        number_of_buildings=(
            entries.r_buildings_1979_1986
            + entries.r_buildings_1987_1990
            + entries.r_buildings_1991_1995
        )
    )
    p_buildings_1996_2004 = Vars3(
        number_of_buildings=(
            entries.r_buildings_1996_2000 + entries.r_buildings_2001_2004
        )
    )
    p_buildings_2005_2011 = Vars4(
        number_of_buildings=(
            entries.r_buildings_2005_2008 + entries.r_buildings_2009_2011
        )
    )
    p_buildings_2011_today = Vars4(number_of_buildings=entries.r_buildings_2011_today)

    p_buildings_total = Vars3(
        number_of_buildings=(
            p_buildings_until_1919.number_of_buildings
            + p_buildings_1919_1948.number_of_buildings
            + p_buildings_1949_1978.number_of_buildings
            + p_buildings_1979_1995.number_of_buildings
            + p_buildings_1996_2004.number_of_buildings
            + p_buildings_2005_2011.number_of_buildings
            + p_buildings_2011_today.number_of_buildings
        )
    )

    p_buildings_until_1919.relative_building_ratio = div(
        p_buildings_until_1919.number_of_buildings,
        p_buildings_total.number_of_buildings,
    )
    p_buildings_1919_1948.relative_building_ratio = div(
        p_buildings_1919_1948.number_of_buildings, p_buildings_total.number_of_buildings
    )
    p_buildings_1949_1978.relative_building_ratio = div(
        p_buildings_1949_1978.number_of_buildings, p_buildings_total.number_of_buildings
    )
    p_buildings_1979_1995.relative_building_ratio = div(
        p_buildings_1979_1995.number_of_buildings, p_buildings_total.number_of_buildings
    )
    p_buildings_1996_2004.relative_building_ratio = div(
        p_buildings_1996_2004.number_of_buildings, p_buildings_total.number_of_buildings
    )
    p_buildings_2005_2011.relative_building_ratio = div(
        p_buildings_2005_2011.number_of_buildings, p_buildings_total.number_of_buildings
    )
    p_buildings_2011_today.relative_building_ratio = div(
        p_buildings_2011_today.number_of_buildings,
        p_buildings_total.number_of_buildings,
    )

    p_buildings_total.relative_building_ratio = (
        p_buildings_until_1919.relative_building_ratio
        + p_buildings_1919_1948.relative_building_ratio
        + p_buildings_1949_1978.relative_building_ratio
        + p_buildings_1979_1995.relative_building_ratio
        + p_buildings_1996_2004.relative_building_ratio
        + p_buildings_2005_2011.relative_building_ratio
        + p_buildings_2011_today.relative_building_ratio
    )

    p_buildings_total.area_m2 = entries.r_area_m2
    p_buildings_until_1919.area_m2 = (
        p_buildings_until_1919.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1919_1948.area_m2 = (
        p_buildings_1919_1948.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1949_1978.area_m2 = (
        p_buildings_1949_1978.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1979_1995.area_m2 = (
        p_buildings_1979_1995.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_1996_2004.area_m2 = (
        p_buildings_1996_2004.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_2005_2011.area_m2 = (
        p_buildings_2005_2011.relative_building_ratio * p_buildings_total.area_m2
    )
    p_buildings_2011_today.area_m2 = (
        p_buildings_2011_today.relative_building_ratio * p_buildings_total.area_m2
    )

    p_buildings_until_1919.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_until_1919_2014"
    )
    p_buildings_1919_1948.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1919_1948_2014"
    )
    p_buildings_1949_1978.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1949_1978_2014"
    )
    p_buildings_1979_1995.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1979_1995_2014"
    )
    p_buildings_1996_2004.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_1996_2002_2014"
    )
    p_buildings_2005_2011.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_2003_2009_2014"
    )
    p_buildings_2011_today.fec_factor_BMWi = fact(
        "Fact_R_P_ratio_fec_to_area_2010_2014_2014"
    )

    p_buildings_until_1919.fec_after_BMWi = (
        p_buildings_until_1919.fec_factor_BMWi * p_buildings_until_1919.area_m2
    )
    p_buildings_1919_1948.fec_after_BMWi = (
        p_buildings_1919_1948.fec_factor_BMWi * p_buildings_1919_1948.area_m2
    )
    p_buildings_1949_1978.fec_after_BMWi = (
        p_buildings_1949_1978.fec_factor_BMWi * p_buildings_1949_1978.area_m2
    )
    p_buildings_1979_1995.fec_after_BMWi = (
        p_buildings_1979_1995.fec_factor_BMWi * p_buildings_1979_1995.area_m2
    )
    p_buildings_1996_2004.fec_after_BMWi = (
        p_buildings_1996_2004.fec_factor_BMWi * p_buildings_1996_2004.area_m2
    )
    p_buildings_2005_2011.fec_after_BMWi = (
        p_buildings_2005_2011.fec_factor_BMWi * p_buildings_2005_2011.area_m2
    )
    p_buildings_2011_today.fec_after_BMWi = (
        p_buildings_2011_today.fec_factor_BMWi * p_buildings_2011_today.area_m2
    )

    p_buildings_total.fec_after_BMWi = (
        p_buildings_until_1919.fec_after_BMWi
        + p_buildings_1919_1948.fec_after_BMWi
        + p_buildings_1949_1978.fec_after_BMWi
        + p_buildings_1979_1995.fec_after_BMWi
        + p_buildings_1996_2004.fec_after_BMWi
        + p_buildings_2005_2011.fec_after_BMWi
        + p_buildings_2011_today.fec_after_BMWi
    )
    p_buildings_total.fec_factor_BMWi = div(
        p_buildings_total.fec_after_BMWi, p_buildings_total.area_m2
    )

    p_buildings_until_1919.relative_heat_ratio_BMWi = div(
        p_buildings_until_1919.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )
    p_buildings_1919_1948.relative_heat_ratio_BMWi = div(
        p_buildings_1919_1948.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )
    p_buildings_1949_1978.relative_heat_ratio_BMWi = div(
        p_buildings_1949_1978.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )
    p_buildings_1979_1995.relative_heat_ratio_BMWi = div(
        p_buildings_1979_1995.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )
    p_buildings_1996_2004.relative_heat_ratio_BMWi = div(
        p_buildings_1996_2004.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )
    p_buildings_2005_2011.relative_heat_ratio_BMWi = div(
        p_buildings_2005_2011.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )
    p_buildings_2011_today.relative_heat_ratio_BMWi = div(
        p_buildings_2011_today.fec_after_BMWi, p_buildings_total.fec_after_BMWi
    )

    p_buildings_total.relative_heat_ratio_BMWi = (
        p_buildings_until_1919.relative_heat_ratio_BMWi
        + p_buildings_1919_1948.relative_heat_ratio_BMWi
        + p_buildings_1949_1978.relative_heat_ratio_BMWi
        + p_buildings_1979_1995.relative_heat_ratio_BMWi
        + p_buildings_1996_2004.relative_heat_ratio_BMWi
        + p_buildings_2005_2011.relative_heat_ratio_BMWi
        + p_buildings_2011_today.relative_heat_ratio_BMWi
    )

    p_buildings_until_1919.relative_heat_ratio_buildings_until_2004 = div(
        p_buildings_until_1919.fec_after_BMWi,
        (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        ),
    )
    p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004 = div(
        p_buildings_1919_1948.fec_after_BMWi,
        (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        ),
    )
    p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004 = div(
        p_buildings_1949_1978.fec_after_BMWi,
        (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        ),
    )
    p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004 = div(
        p_buildings_1979_1995.fec_after_BMWi,
        (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        ),
    )
    p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004 = div(
        p_buildings_1996_2004.fec_after_BMWi,
        (
            p_buildings_total.fec_after_BMWi
            - p_buildings_2005_2011.fec_after_BMWi
            - p_buildings_2011_today.fec_after_BMWi
        ),
    )

    p_buildings_total.relative_heat_ratio_buildings_until_2004 = (
        p_buildings_until_1919.relative_heat_ratio_buildings_until_2004
        + p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004
        + p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004
        + p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004
        + p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_until_1919.area_m2_relative_heat_ratio = (
        p_buildings_until_1919.area_m2
        * p_buildings_until_1919.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1919_1948.area_m2_relative_heat_ratio = (
        p_buildings_1919_1948.area_m2
        * p_buildings_1919_1948.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1949_1978.area_m2_relative_heat_ratio = (
        p_buildings_1949_1978.area_m2
        * p_buildings_1949_1978.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1979_1995.area_m2_relative_heat_ratio = (
        p_buildings_1979_1995.area_m2
        * p_buildings_1979_1995.relative_heat_ratio_buildings_until_2004
    )
    p_buildings_1996_2004.area_m2_relative_heat_ratio = (
        p_buildings_1996_2004.area_m2
        * p_buildings_1996_2004.relative_heat_ratio_buildings_until_2004
    )

    p_buildings_total.area_m2_relative_heat_ratio = (
        p_buildings_until_1919.area_m2_relative_heat_ratio
        + p_buildings_1919_1948.area_m2_relative_heat_ratio
        + p_buildings_1949_1978.area_m2_relative_heat_ratio
        + p_buildings_1979_1995.area_m2_relative_heat_ratio
        + p_buildings_1996_2004.area_m2_relative_heat_ratio
    )

    p_buildings_total.energy = (
        supply.fueloil.energy
        + supply.lpg.energy
        + supply.biomass.energy
        + supply.coal.energy
        + supply.heatnet.energy
        + supply.solarth.energy
        + supply.heatpump.energy
        + supply.gas.energy
        + supply.elec_heating.energy
    )

    p_buildings_until_1919.energy = (
        p_buildings_total.energy * p_buildings_until_1919.relative_heat_ratio_BMWi
    )
    p_buildings_1919_1948.energy = (
        p_buildings_total.energy * p_buildings_1919_1948.relative_heat_ratio_BMWi
    )
    p_buildings_1949_1978.energy = (
        p_buildings_total.energy * p_buildings_1949_1978.relative_heat_ratio_BMWi
    )
    p_buildings_1979_1995.energy = (
        p_buildings_total.energy * p_buildings_1979_1995.relative_heat_ratio_BMWi
    )
    p_buildings_1996_2004.energy = (
        p_buildings_total.energy * p_buildings_1996_2004.relative_heat_ratio_BMWi
    )
    p_buildings_2005_2011.energy = (
        p_buildings_total.energy * p_buildings_2005_2011.relative_heat_ratio_BMWi
    )
    p_buildings_2011_today.energy = (
        p_buildings_total.energy * p_buildings_2011_today.relative_heat_ratio_BMWi
    )

    p_buildings_total.ratio_energy_to_m2 = div(
        p_buildings_total.energy, p_buildings_total.area_m2
    )
    p_buildings_until_1919.ratio_energy_to_m2 = div(
        p_buildings_until_1919.energy, p_buildings_until_1919.area_m2
    )
    p_buildings_1919_1948.ratio_energy_to_m2 = div(
        p_buildings_1919_1948.energy, p_buildings_1919_1948.area_m2
    )
    p_buildings_1949_1978.ratio_energy_to_m2 = div(
        p_buildings_1949_1978.energy, p_buildings_1949_1978.area_m2
    )
    p_buildings_1979_1995.ratio_energy_to_m2 = div(
        p_buildings_1979_1995.energy, p_buildings_1979_1995.area_m2
    )
    p_buildings_1996_2004.ratio_energy_to_m2 = div(
        p_buildings_1996_2004.energy, p_buildings_1996_2004.area_m2
    )
    p_buildings_2005_2011.ratio_energy_to_m2 = div(
        p_buildings_2005_2011.energy, p_buildings_2005_2011.area_m2
    )
    p_buildings_2011_today.ratio_energy_to_m2 = div(
        p_buildings_2011_today.energy, p_buildings_2011_today.area_m2
    )

    p_buildings_area_m2_com = EnergyPerM2PctCommune(
        pct_x=entries.r_pct_of_area_m2_com,
        total=p_buildings_total,
    )

    r.CO2e_combustion_based = supply.total.CO2e_combustion_based

    # CO2e_total

    r.CO2e_total = supply.total.CO2e_total

    p_elec_heatpump.energy = supply.heatpump.energy / fact(
        "Fact_R_S_heatpump_mean_annual_performance_factor_all"
    )

    p_elec_elcon.energy = (
        supply.elec.energy - p_elec_heatpump.energy - supply.elec_heating.energy
    )
    p_vehicles.energy = supply.petrol.energy
    p_other.energy = p_elec_heatpump.energy + p_elec_elcon.energy + p_vehicles.energy

    p.energy = p_buildings_total.energy + p_other.energy

    supply.biomass.number_of_buildings = div(
        supply.biomass.energy * p_buildings_total.number_of_buildings,
        (p_buildings_total.ratio_energy_to_m2 * p_buildings_total.area_m2),
    )

    return R18(
        r=r,
        p=p,
        p_buildings_total=p_buildings_total,
        p_buildings_until_1919=p_buildings_until_1919,
        p_buildings_1919_1948=p_buildings_1919_1948,
        p_buildings_1949_1978=p_buildings_1949_1978,
        p_buildings_1979_1995=p_buildings_1979_1995,
        p_buildings_1996_2004=p_buildings_1996_2004,
        p_buildings_2005_2011=p_buildings_2005_2011,
        p_buildings_2011_today=p_buildings_2011_today,
        p_buildings_area_m2_com=p_buildings_area_m2_com,
        p_elec_elcon=p_elec_elcon,
        p_elec_heatpump=p_elec_heatpump,
        p_vehicles=p_vehicles,
        p_other=p_other,
        s=supply.total,
        s_fueloil=supply.fueloil,
        s_lpg=supply.lpg,
        s_biomass=supply.biomass,
        s_coal=supply.coal,
        s_petrol=supply.petrol,
        s_heatnet=supply.heatnet,
        s_solarth=supply.solarth,
        s_heatpump=supply.heatpump,
        s_elec_heating=supply.elec_heating,
        s_gas=supply.gas,
        s_elec=supply.elec,
    )
