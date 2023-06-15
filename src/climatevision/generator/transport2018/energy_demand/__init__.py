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

    # --- Air ---
    air_dmstc = Air.calc_domestic(entries, facts, assumptions)
    air_inter = Air.calc_international(entries, facts, assumptions)
    air = air_dmstc + air_inter

    # --- Road ---
    road_car_it_ot = Road.calc_car(entries, facts, assumptions, "it_ot")
    road_car_ab = Road.calc_car(entries, facts, assumptions, "ab")
    road_car = road_car_it_ot + road_car_ab
    road_bus = Road.calc_bus(entries, facts, assumptions)
    road_ppl = road_car + road_bus
    road_gds_mhd_it_ot = Road.calc_goods_medium_and_heavy_duty_it_ot(
        entries, facts, assumptions, road_bus_mileage=road_bus.mileage
    )
    road_gds_mhd_ab = Road.calc_goods_medium_and_heavy_duty_ab(
        entries, facts, assumptions
    )
    road_gds_mhd = road_gds_mhd_ab + road_gds_mhd_it_ot
    road_gds_ldt_it_ot = Road.calc_goods_light_duty(
        entries, facts, assumptions, "it_ot"
    )
    road_gds_ldt_ab = Road.calc_goods_light_duty(entries, facts, assumptions, "ab")
    road_gds_ldt = road_gds_ldt_it_ot + road_gds_ldt_ab
    road_gds = road_gds_ldt + road_gds_mhd
    road = road_gds + road_ppl

    # --- Rail ---
    rail_ppl_metro = Rail.calc_rail_people_metro(entries, facts, assumptions)
    rail_ppl_distance = Rail.calc_people_distance(entries, facts, assumptions)
    rail_ppl = rail_ppl_metro + rail_ppl_distance
    rail_gds = Rail.calc_goods(entries, facts, assumptions)
    rail = rail_ppl + rail_gds

    # --- Ship ---
    ship_dmstc = Ship.calc_ship_domestic(entries, facts, assumptions)
    ship_inter = Ship.calc_ship_international(entries, facts, assumptions)
    ship = ship_dmstc + ship_inter

    # --- Other ---
    other_foot = Other.calc_foot(entries, facts)
    other_cycl = Other.calc_cycle(entries, facts)
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
