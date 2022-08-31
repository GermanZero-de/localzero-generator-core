"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/traffic.html
"""

# pyright: strict
from .air import Air
from .road import Road
from .rail import Rail
from .ship import Ship
from .other import Other
from .transport import Transport
from .energy_sum import EnergySum
from .t18 import T18
from ..inputs import Inputs


def calc(inputs: Inputs) -> T18:
    # TODO: Fix the it at confusion

    # --- Air ---
    air_dmstc = Air.calc_domestic(inputs)
    air_inter = Air.calc_international(inputs)
    air = air_dmstc + air_inter
    # --- Road ---
    road_car_it_ot = Road.calc_car(inputs, "it_ot")
    road_car_ab = Road.calc_car(inputs, "ab")
    road_car = road_car_it_ot + road_car_ab
    road_bus = Road.calc_bus(inputs)
    road_ppl = road_car + road_bus
    road_gds_mhd_it_ot = Road.calc_goods_medium_and_heavy_duty_it_ot(
        inputs, road_bus_mileage=road_bus.mileage
    )
    road_gds_mhd_ab = Road.calc_goods_medium_and_heavy_duty_ab(inputs)
    road_gds_mhd = road_gds_mhd_ab + road_gds_mhd_it_ot
    road_gds_ldt_it_ot = Road.calc_goods_light_duty(inputs, "it_ot")
    road_gds_ldt_ab = Road.calc_goods_light_duty(inputs, "ab")
    road_gds_ldt = road_gds_ldt_it_ot + road_gds_ldt_ab
    road_gds = road_gds_ldt + road_gds_mhd
    road = road_gds + road_ppl
    # --- Rail ---
    rail_ppl_metro = Rail.calc_rail_people_metro(inputs)
    rail_ppl_distance = Rail.calc_people_distance(inputs)
    rail_ppl = rail_ppl_metro + rail_ppl_distance
    rail_gds = Rail.calc_goods(inputs)
    rail = rail_ppl + rail_gds
    # --- Ship ---
    ship_dmstc = Ship.calc_ship_domestic(inputs)
    ship_inter = Ship.calc_ship_international(inputs)
    ship = ship_dmstc + ship_inter
    # --- Other ---
    other_foot = Other.calc_foot(inputs)
    other_cycl = Other.calc_cycle(inputs)
    other = other_foot + other_cycl

    t = (
        Transport.lift_air(air)
        + Transport.lift_road(road)
        + Transport.lift_ship(ship)
        + Transport.lift_rail(rail)
        + Transport.lift_other(other)
    )

    # ----------------------------------------------------
    s_biodiesel = EnergySum(energy=t.demand_biodiesel)
    s_bioethanol = EnergySum(energy=t.demand_bioethanol)
    s_biogas = EnergySum(energy=t.demand_biogas)
    s_diesel = EnergySum(energy=t.demand_diesel)
    s_elec = EnergySum(energy=t.demand_electricity)
    s_fueloil = EnergySum(energy=ship_inter.demand_fueloil)
    s_gas = EnergySum(energy=t.demand_gas)
    s_jetfuel = EnergySum(energy=t.demand_jetfuel)
    s_lpg = EnergySum(energy=t.demand_lpg)
    s_petrol = EnergySum(energy=t.demand_petrol)

    s = EnergySum(
        energy=s_biodiesel.energy
        + s_bioethanol.energy
        + s_biogas.energy
        + s_diesel.energy
        + s_elec.energy
        + s_fueloil.energy
        + s_gas.energy
        + s_jetfuel.energy
        + s_lpg.energy
        + s_petrol.energy
    )
    return T18(
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
        t=t,
        s_biodiesel=s_biodiesel,
        s_bioethanol=s_bioethanol,
        s_biogas=s_biogas,
        s_diesel=s_diesel,
        s_elec=s_elec,
        s_fueloil=s_fueloil,
        s_gas=s_gas,
        s_jetfuel=s_jetfuel,
        s_lpg=s_lpg,
        s_petrol=s_petrol,
        s=s,
    )
