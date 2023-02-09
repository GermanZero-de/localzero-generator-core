"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/traffic.html
"""

# pyright: strict

from ..inputs import Inputs
from ..transport2018.t18 import T18
from . import energy_demand, energy_source, energy_general

from .t30 import T30
from .t import T


def calc(inputs: Inputs, *, t18: T18) -> T30:

    production = energy_demand.calc_production(inputs, t18)

    general = energy_general.calc_general(
        inputs,
        production.road_bus_action_infra,
        production.road_gds_mhd_action_wire,
        production.road_action_charger,
        production.rail_ppl_metro_action_infra,
        production.rail_action_invest_infra,
        production.other_cycl,
    )

    t = T.calc(
        t18=t18,
        required_domestic_transport_capacity_pkm=production.required_domestic_transport_capacity_pkm,
        air=production.air,
        rail=production.rail,
        road=production.road,
        ship=production.ship,
        other=production.other,
        g=general.g,
    )

    supply = energy_source.calc_supply(t)

    return T30(
        air_dmstc=production.air_dmstc,
        air_inter=production.air_inter,
        air=production.air,
        road_car_it_ot=production.road_car_it_ot,
        road_car_ab=production.road_car_ab,
        road_car=production.road_car,
        road_bus=production.road_bus,
        road_bus_action_infra=production.road_bus_action_infra,
        road_action_charger=production.road_action_charger,
        road_ppl=production.road_ppl,
        road_gds_ldt_it_ot=production.road_gds_ldt_it_ot,
        road_gds_ldt_ab=production.road_gds_ldt_ab,
        road_gds_ldt=production.road_gds_ldt,
        road_gds_mhd_ab=production.road_gds_mhd_ab,
        road_gds_mhd_it_ot=production.road_gds_mhd_it_ot,
        road_gds_mhd=production.road_gds_mhd,
        road_gds=production.road_gds,
        road_gds_mhd_action_wire=production.road_gds_mhd_action_wire,
        road=production.road,
        rail_ppl_metro=production.rail_ppl_metro,
        rail_ppl_distance=production.rail_ppl_distance,
        rail_ppl=production.rail_ppl,
        rail_ppl_metro_action_infra=production.rail_ppl_metro_action_infra,
        rail_action_invest_infra=production.rail_action_invest_infra,
        rail_action_invest_station=production.rail_action_invest_station,
        rail_gds=production.rail_gds,
        rail=production.rail,
        ship_dmstc=production.ship_dmstc,
        ship_inter=production.ship_inter,
        ship_dmstc_action_infra=production.ship_dmstc_action_infra,
        ship=production.ship,
        other_cycl=production.other_cycl,
        other_cycl_action_infra=production.other_cycl_action_infra,
        other_foot=production.other_foot,
        other_foot_action_infra=production.other_foot_action_infra,
        other=production.other,
        g_planning=general.g_planning,
        g=general.g,
        t=t,
        s_petrol=supply.petrol,
        s_jetfuel=supply.jetfuel,
        s_diesel=supply.diesel,
        s_elec=supply.elec,
        s_hydrogen=supply.hydrogen,
        s_emethan=supply.emethan,
        s=supply.total,
        s_fueloil=supply.fueloil,
        s_lpg=supply.lpg,
        s_gas=supply.gas,
        s_biogas=supply.biogas,
        s_bioethanol=supply.bioethanol,
        s_biodiesel=supply.biodiesel,
    )
