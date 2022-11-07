# pyright: strict

from dataclasses import dataclass

from ..common.energy import Energy

from .energy_demand import Air, Road, Rail, Ship, Other
from .transport import Transport


@dataclass(kw_only=True)
class T18:
    t: Transport

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

    s: Energy
    s_petrol: Energy
    s_jetfuel: Energy
    s_diesel: Energy
    s_fueloil: Energy
    s_lpg: Energy
    s_gas: Energy
    s_biogas: Energy
    s_bioethanol: Energy
    s_biodiesel: Energy
    s_elec: Energy
