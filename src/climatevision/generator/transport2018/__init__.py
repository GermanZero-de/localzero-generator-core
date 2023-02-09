"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/traffic.html
"""

# pyright: strict

from ..inputs import Inputs

from .transport import Transport
from .t18 import T18
from . import energy_demand, energy_source


def calc(inputs: Inputs) -> T18:

    production = energy_demand.calc_production(inputs)

    t = (
        Transport.lift_air(production.air)
        + Transport.lift_road(production.road)
        + Transport.lift_ship(production.ship)
        + Transport.lift_rail(production.rail)
        + Transport.lift_other(production.other)
    )

    supply = energy_source.calc_supply(t, production.ship_inter)

    return T18(
        air_dmstc=production.air_dmstc,
        air_inter=production.air_inter,
        air=production.air,
        road_car_it_ot=production.road_car_it_ot,
        road_car_ab=production.road_car_ab,
        road_car=production.road_car,
        road_bus=production.road_bus,
        road_ppl=production.road_ppl,
        road_gds_mhd_it_ot=production.road_gds_mhd_it_ot,
        road_gds_mhd_ab=production.road_gds_mhd_ab,
        road_gds_mhd=production.road_gds_mhd,
        road_gds_ldt_it_ot=production.road_gds_ldt_it_ot,
        road_gds_ldt_ab=production.road_gds_ldt_ab,
        road_gds_ldt=production.road_gds_ldt,
        road_gds=production.road_gds,
        road=production.road,
        rail_ppl_distance=production.rail_ppl_distance,
        rail_ppl_metro=production.rail_ppl_metro,
        rail_ppl=production.rail_ppl,
        rail_gds=production.rail_gds,
        rail=production.rail,
        ship_dmstc=production.ship_dmstc,
        ship_inter=production.ship_inter,
        ship=production.ship,
        other_foot=production.other_foot,
        other_cycl=production.other_cycl,
        other=production.other,
        t=t,
        s_biodiesel=supply.biodiesel,
        s_bioethanol=supply.bioethanol,
        s_biogas=supply.biogas,
        s_diesel=supply.diesel,
        s_elec=supply.elec,
        s_fueloil=supply.fueloil,
        s_gas=supply.gas,
        s_jetfuel=supply.jetfuel,
        s_lpg=supply.lpg,
        s_petrol=supply.petrol,
        s=supply.total,
    )
