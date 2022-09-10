"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/traffic.html
"""

# pyright: strict

from ..inputs import Inputs
from ..transport2018.t18 import T18
from ..commonDataclasses.energy import Energy

from .investmentaction import InvestmentAction
from .air import calc_air_domestic, calc_air_international, Air
from .road import (
    Road,
    RoadBus,
    RoadCar,
    RoadGoods,
    RoadGoodsLightDuty,
    RoadGoodsMediumAndHeavyDuty,
    RoadPeople,
    RoadSum,
    RoadInvestmentAction,
)
from .rail import Rail, RailGoods, RailPeople, RailPeopleMetroActionInfra, RailPeopleSum
from .ship import Ship, ShipDomestic, ShipInternational, ShipDomesticActionInfra
from .other import Other, OtherCycle, OtherFoot
from .t30 import T30
from .dataclasses import GPlanning, G, T


def calc(inputs: Inputs, *, t18: T18) -> T30:
    ass = inputs.ass
    entries = inputs.entries

    # --- Air ---
    air_dmstc = calc_air_domestic(inputs, t18)
    air_inter = calc_air_international(inputs, t18)
    air = Air.calc(t18, domestic=air_dmstc, international=air_inter)

    # First we estimate the total required transport capacity in the target year (excluding air).
    required_domestic_transport_capacity_pkm = entries.m_population_com_203X * (
        ass("Ass_T_D_ratio_trnsprt_ppl_to_ppl_city")
        if entries.t_rt3 == "city"
        else ass("Ass_T_D_ratio_trnsprt_ppl_to_ppl_smcity")
        if entries.t_rt3 == "smcty"
        else ass("Ass_T_D_ratio_trnsprt_ppl_to_ppl_rural")
        if entries.t_rt3 == "rural"
        else ass("Ass_T_D_trnsprt_ppl_nat") / entries.m_population_nat
    )

    # -- Road ---
    road_car_it_ot = Road.calc_car_it_ot(
        inputs,
        t18=t18,
        required_domestic_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    road_car_ab = Road.calc_car_ab(
        inputs,
        t18=t18,
        required_domestic_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    road_car = RoadCar.calc(inputs, t18=t18, it_ot=road_car_it_ot, ab=road_car_ab)
    road_action_charger = RoadInvestmentAction.calc_car_action_charger(
        inputs, car_base_unit=road_car.fleet_modernisation_cost.base_unit
    )
    road_bus = RoadBus.calc(
        inputs,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    road_bus_action_infra = RoadBus.calc_action_infra(
        inputs, bus_transport_capacity_pkm=road_bus.transport.transport_capacity_pkm
    )
    road_ppl = RoadPeople.calc(
        inputs,
        t18=t18,
        car=road_car,
        bus=road_bus,
        road_bus_action_infra=road_bus_action_infra,
    )
    road_gds_ldt_it_ot = Road.calc_goods_lightduty_it_ot(inputs, t18=t18)
    road_gds_ldt_ab = Road.calc_goods_lightduty_ab(inputs, t18=t18)
    road_gds_ldt = RoadGoodsLightDuty.calc(
        inputs,
        t18=t18,
        it_ot=road_gds_ldt_it_ot,
        ab=road_gds_ldt_ab,
    )
    road_gds_mhd_ab = Road.calc_goods_medium_and_heavy_duty_ab(inputs, t18=t18)
    road_gds_mhd_it_ot = Road.calc_goods_medium_and_heavy_duty_it_ot(inputs, t18=t18)
    road_gds_mhd = RoadGoodsMediumAndHeavyDuty.calc(
        inputs, t18=t18, it_ot=road_gds_mhd_it_ot, ab=road_gds_mhd_ab
    )
    road_gds_mhd_action_wire = RoadGoodsMediumAndHeavyDuty.calc_action_wire(inputs)
    road_gds = RoadGoods.calc(
        t18=t18,
        ldt=road_gds_ldt,
        mhd=road_gds_mhd,
        road_gds_mhd_action_wire=road_gds_mhd_action_wire,
    )
    road = RoadSum.calc(
        t18=t18,
        goods=road_gds,
        people=road_ppl,
        road_action_charger=road_action_charger,
    )

    # --- Rail ---
    rail_ppl_metro = RailPeople.calc_metro(
        inputs,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    rail_ppl_distance = RailPeople.calc_distance(
        inputs,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    rail_action_invest_infra = InvestmentAction.calc_rail_action_invest_infra(inputs)
    rail_action_invest_station = InvestmentAction.calc_rail_action_invest_station(
        inputs
    )
    rail_ppl_metro_action_infra = RailPeopleMetroActionInfra.calc(
        inputs,
        metro_transport_capacity_pkm=rail_ppl_metro.transport.transport_capacity_pkm,
    )
    rail_ppl = RailPeopleSum.calc(
        t18=t18,
        rail_ppl_metro=rail_ppl_metro,
        rail_ppl_distance=rail_ppl_distance,
        rail_ppl_metro_action_infra=rail_ppl_metro_action_infra,
    )
    rail_gds = RailGoods.calc(inputs, t18=t18)
    rail = Rail.calc(
        t18=t18,
        rail_ppl=rail_ppl,
        rail_gds=rail_gds,
        rail_action_invest_infra=rail_action_invest_infra,
        rail_action_invest_station=rail_action_invest_station,
    )

    # --- Ship ---
    ship_dmstc = ShipDomestic.calc(inputs, t18=t18)
    ship_inter = ShipInternational.calc(inputs, t18=t18)
    ship_dmstc_action_infra = ShipDomesticActionInfra.calc(inputs)
    ship = Ship.calc(
        t18=t18,
        ship_inter=ship_inter,
        ship_dmstc=ship_dmstc,
        ship_dmstc_action_infra=ship_dmstc_action_infra,
    )

    # --- Other ---
    other_cycl = OtherCycle.calc(
        inputs,
        t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    other_cycl_action_infra = InvestmentAction.calc_other_cycl_action_infra(
        inputs, cycle_transport_capacity_pkm=other_cycl.transport.transport_capacity_pkm
    )
    other_foot = OtherFoot.calc(
        inputs,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    other_foot_action_infra = InvestmentAction.calc_other_foot_action_infra(inputs)
    other = Other.calc(
        inputs,
        t18=t18,
        other_foot=other_foot,
        other_cycl=other_cycl,
        other_cycl_action_infra=other_cycl_action_infra,
        other_foot_action_infra=other_foot_action_infra,
    )

    # --- Planning and other aggregates ---
    g_planning = GPlanning.calc(
        inputs,
        road_bus_action_infra=road_bus_action_infra,
        road_gds_mhd_action_wire=road_gds_mhd_action_wire,
        road_action_charger=road_action_charger,
        rail_ppl_metro_action_infra=rail_ppl_metro_action_infra,
        rail_action_invest_infra=rail_action_invest_infra,
        other_cycl=other_cycl,
    )
    # TODO: This Seems to be a pointless rename?
    g = G(
        invest_com=g_planning.invest_com,
        invest_pa_com=g_planning.invest_pa_com,
        demand_emplo=g_planning.demand_emplo,
        cost_wage=g_planning.cost_wage,
        invest_pa=g_planning.invest_pa,
        invest=g_planning.invest,
        demand_emplo_new=g_planning.demand_emplo_new,
        demand_emplo_com=g_planning.demand_emplo_new,
    )
    t = T.calc(
        t18=t18,
        required_domestic_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
        air=air,
        rail=rail,
        road=road,
        ship=ship,
        other=other,
        g=g,
    )
    s_petrol = Energy(energy=t.transport.demand_epetrol)
    s_jetfuel = Energy(energy=t.transport.demand_ejetfuel)
    s_diesel = Energy(energy=t.transport.demand_ediesel)
    s_elec = Energy(energy=t.transport.demand_electricity)
    s_hydrogen = Energy(energy=t.transport.demand_hydrogen)

    s_emethan = Energy(energy=0)
    s_fueloil = Energy(energy=0)
    s_lpg = Energy(energy=0)
    s_gas = Energy(energy=0)
    s_biogas = Energy(energy=0)
    s_bioethanol = Energy(energy=0)
    s_biodiesel = Energy(energy=0)

    s = Energy(
        energy=s_petrol.energy
        + s_jetfuel.energy
        + s_diesel.energy
        + s_elec.energy
        + s_hydrogen.energy
        + s_emethan.energy
    )

    # --- Populate result ---
    return T30(
        air_dmstc=air_dmstc,
        air_inter=air_inter,
        air=air,
        road_car_it_ot=road_car_it_ot,
        road_car_ab=road_car_ab,
        road_car=road_car,
        road_bus=road_bus,
        road_bus_action_infra=road_bus_action_infra,
        road_action_charger=road_action_charger,
        road_ppl=road_ppl,
        road_gds_ldt_it_ot=road_gds_ldt_it_ot,
        road_gds_ldt_ab=road_gds_ldt_ab,
        road_gds_ldt=road_gds_ldt,
        road_gds_mhd_ab=road_gds_mhd_ab,
        road_gds_mhd_it_ot=road_gds_mhd_it_ot,
        road_gds_mhd=road_gds_mhd,
        road_gds=road_gds,
        road_gds_mhd_action_wire=road_gds_mhd_action_wire,
        road=road,
        rail_ppl_metro=rail_ppl_metro,
        rail_ppl_distance=rail_ppl_distance,
        rail_ppl=rail_ppl,
        rail_ppl_metro_action_infra=rail_ppl_metro_action_infra,
        rail_action_invest_infra=rail_action_invest_infra,
        rail_action_invest_station=rail_action_invest_station,
        rail_gds=rail_gds,
        rail=rail,
        ship_dmstc=ship_dmstc,
        ship_inter=ship_inter,
        ship_dmstc_action_infra=ship_dmstc_action_infra,
        ship=ship,
        other_cycl=other_cycl,
        other_cycl_action_infra=other_cycl_action_infra,
        other_foot=other_foot,
        other_foot_action_infra=other_foot_action_infra,
        other=other,
        g_planning=g_planning,
        g=g,
        t=t,
        s_petrol=s_petrol,
        s_jetfuel=s_jetfuel,
        s_diesel=s_diesel,
        s_elec=s_elec,
        s_hydrogen=s_hydrogen,
        s_emethan=s_emethan,
        s=s,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biogas=s_biogas,
        s_bioethanol=s_bioethanol,
        s_biodiesel=s_biodiesel,
    )
