# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions

from .air import Air
from .road import Road
from .rail import Rail
from .ship import Ship
from .other import Other


@dataclass(kw_only=True)
class Production:
    air_inter: Air
    air_dmstc: Air
    air: Air

    road: Road
    road_car: Road
    road_car_it_ot: Road
    road_car_ab: Road
    road_bus: Road
    road_gds: Road
    road_gds_ldt: Road
    road_gds_ldt_it_ot: Road
    road_gds_ldt_ab: Road
    road_gds_mhd: Road
    road_ppl: Road
    road_gds_mhd_it_ot: Road
    road_gds_mhd_ab: Road

    rail_ppl: Rail
    rail_ppl_metro: Rail
    rail_ppl_distance: Rail
    rail_gds: Rail
    rail: Rail

    ship_dmstc: Ship
    ship_inter: Ship
    ship: Ship

    other_foot: Other
    other_cycl: Other
    other: Other


def calc_production(
    entries: Entries, facts: Facts, assumptions: Assumptions
) -> Production:
    # TODO: Fix the it at confusion

    population_commune_2018 = entries.m_population_com_2018
    population_district_2018 = entries.m_population_dis
    population_germany_2018 = entries.m_population_nat

    area_kind_rt7 = entries.t_rt7

    # --- Air ---
    air_dmstc = Air.calc_domestic(
        facts, entries, assumptions, population_commune_2018, population_germany_2018
    )
    air_inter = Air.calc_international(
        facts, entries, assumptions, population_commune_2018, population_germany_2018
    )
    air = air_dmstc + air_inter

    # --- Road ---
    road_car_it_ot = Road.calc_car(facts, assumptions, entries.t_mil_car_it_ot, "it_ot")
    road_car_ab = Road.calc_car(facts, assumptions, entries.t_mil_car_ab, "ab")
    road_car = road_car_it_ot + road_car_ab
    road_bus = Road.calc_bus(
        facts,
        assumptions,
        population_commune_2018,
        population_district_2018,
        entries.t_bus_mega_km_dis,
    )
    road_ppl = road_car + road_bus
    road_gds_mhd_it_ot = Road.calc_goods_medium_and_heavy_duty_it_ot(
        facts, assumptions, entries.t_mil_mhd_it_ot, road_bus_mileage=road_bus.mileage
    )
    road_gds_mhd_ab = Road.calc_goods_medium_and_heavy_duty_ab(
        facts, assumptions, entries.t_mil_mhd_ab
    )
    road_gds_mhd = road_gds_mhd_ab + road_gds_mhd_it_ot
    road_gds_ldt_it_ot = Road.calc_goods_light_duty(
        facts, assumptions, entries.t_mil_ldt_it_ot, "it_ot"
    )
    road_gds_ldt_ab = Road.calc_goods_light_duty(
        facts, assumptions, entries.t_mil_ldt_ab, "ab"
    )
    road_gds_ldt = road_gds_ldt_it_ot + road_gds_ldt_ab
    road_gds = road_gds_ldt + road_gds_mhd
    road = road_gds + road_ppl

    # --- Rail ---
    rail_ppl_metro = Rail.calc_rail_people_metro(
        facts,
        assumptions,
        population_commune_2018,
        population_district_2018,
        entries.t_metro_mega_km_dis,
    )
    rail_ppl_distance = Rail.calc_people_distance(
        facts, assumptions, entries.t_ec_rail_ppl_elec, entries.t_ec_rail_ppl_diesel
    )
    rail_ppl = rail_ppl_metro + rail_ppl_distance
    rail_gds = Rail.calc_goods(
        facts, assumptions, entries.t_ec_rail_gds_elec, entries.t_ec_rail_gds_diesel
    )
    rail = rail_ppl + rail_gds

    # --- Ship ---
    ship_dmstc = Ship.calc_ship_domestic(
        facts, entries, assumptions, population_commune_2018, population_germany_2018
    )
    ship_inter = Ship.calc_ship_international(
        facts, entries, assumptions, population_commune_2018, population_germany_2018
    )
    ship = ship_dmstc + ship_inter

    # --- Other ---
    other_foot = Other.calc_foot(facts, population_commune_2018, area_kind_rt7)
    other_cycl = Other.calc_cycle(facts, population_commune_2018, area_kind_rt7)
    other = other_foot + other_cycl

    return Production(
        air_dmstc=air_dmstc,
        air_inter=air_inter,
        air=air,
        road_car_it_ot=road_car_it_ot,
        road_car_ab=road_car_ab,
        road_car=road_car,
        road_bus=road_bus,
        road_ppl=road_ppl,
        road_gds_mhd_it_ot=road_gds_mhd_it_ot,
        road_gds_mhd_ab=road_gds_mhd_ab,
        road_gds_mhd=road_gds_mhd,
        road_gds_ldt_it_ot=road_gds_ldt_it_ot,
        road_gds_ldt_ab=road_gds_ldt_ab,
        road_gds_ldt=road_gds_ldt,
        road_gds=road_gds,
        road=road,
        rail_ppl_distance=rail_ppl_distance,
        rail_ppl_metro=rail_ppl_metro,
        rail_ppl=rail_ppl,
        rail_gds=rail_gds,
        rail=rail,
        ship_dmstc=ship_dmstc,
        ship_inter=ship_inter,
        ship=ship,
        other_foot=other_foot,
        other_cycl=other_cycl,
        other=other,
    )
