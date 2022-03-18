# pyright: strict
from dataclasses import dataclass
from .air import Air
from .road import Road
from .rail import Rail
from .ship import Ship
from .other import Other
from .transport import Transport
from .energy_sum import EnergySum


@dataclass
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

    s: EnergySum
    s_petrol: EnergySum
    s_jetfuel: EnergySum
    s_diesel: EnergySum
    s_fueloil: EnergySum
    s_lpg: EnergySum
    s_gas: EnergySum
    s_biogas: EnergySum
    s_bioethanol: EnergySum
    s_biodiesel: EnergySum
    s_elec: EnergySum
