# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...transport2018.t18 import T18

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
from .rail import (
    Rail,
    RailGoods,
    RailPeople,
    RailPeopleMetroActionInfra,
    RailPeopleSum,
)
from .ship import Ship, ShipDomestic, ShipInternational, ShipDomesticActionInfra
from .other import Other, OtherCycle, OtherFoot
from .investmentaction import InvestmentAction, RoadInvestmentAction
from .transport import Transport


@dataclass(kw_only=True)
class Production:
    air: Air
    air_inter: Transport
    air_dmstc: Transport

    road: RoadSum
    road_ppl: RoadPeople
    road_car: RoadCar
    road_car_it_ot: Road
    road_car_ab: Road
    road_bus: RoadBus
    road_bus_action_infra: InvestmentAction
    road_gds: RoadGoods
    road_gds_ldt: RoadGoodsLightDuty
    road_gds_ldt_it_ot: Road
    road_gds_ldt_ab: Road
    road_gds_mhd: RoadGoodsMediumAndHeavyDuty
    road_gds_mhd_it_ot: Road
    road_gds_mhd_ab: Road
    road_gds_mhd_action_wire: InvestmentAction
    road_action_charger: RoadInvestmentAction

    rail: Rail
    rail_ppl: RailPeopleSum
    rail_ppl_distance: RailPeople
    rail_ppl_metro: RailPeople
    rail_gds: RailGoods
    rail_action_invest_infra: InvestmentAction
    rail_action_invest_station: InvestmentAction
    rail_ppl_metro_action_infra: RailPeopleMetroActionInfra

    ship: Ship
    ship_dmstc: ShipDomestic
    ship_dmstc_action_infra: ShipDomesticActionInfra
    ship_inter: ShipInternational

    other: Other
    other_foot: OtherFoot
    other_foot_action_infra: InvestmentAction
    other_cycl: OtherCycle
    other_cycl_action_infra: InvestmentAction

    required_domestic_transport_capacity_pkm: float


def calc_production(
    entries: Entries, facts: Facts, assumptions: Assumptions, t18: T18
) -> Production:
    ass = assumptions.ass

    # --- Air ---
    air_dmstc = calc_air_domestic(entries, facts, t18)
    air_inter = calc_air_international(entries, facts, assumptions, t18)
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
        entries,
        facts,
        assumptions,
        t18=t18,
        required_domestic_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    road_car_ab = Road.calc_car_ab(
        entries,
        facts,
        assumptions,
        t18=t18,
        required_domestic_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    road_car = RoadCar.calc(
        entries, facts, assumptions, t18=t18, it_ot=road_car_it_ot, ab=road_car_ab
    )
    road_action_charger = RoadInvestmentAction.calc_car_action_charger(
        entries,
        facts,
        assumptions,
        car_base_unit=road_car.fleet_modernisation_cost.base_unit,
    )
    road_bus = RoadBus.calc(
        entries,
        facts,
        assumptions,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    road_bus_action_infra = RoadBus.calc_action_infra(
        entries,
        facts,
        assumptions,
        bus_transport_capacity_pkm=road_bus.transport.transport_capacity_pkm,
    )
    road_ppl = RoadPeople.calc(
        t18=t18,
        car=road_car,
        bus=road_bus,
        road_bus_action_infra=road_bus_action_infra,
    )
    road_gds_ldt_it_ot = Road.calc_goods_lightduty_it_ot(
        entries, facts, assumptions, t18=t18
    )
    road_gds_ldt_ab = Road.calc_goods_lightduty_ab(entries, facts, assumptions, t18=t18)
    road_gds_ldt = RoadGoodsLightDuty.calc(
        entries,
        facts,
        assumptions,
        t18=t18,
        it_ot=road_gds_ldt_it_ot,
        ab=road_gds_ldt_ab,
    )
    road_gds_mhd_ab = Road.calc_goods_medium_and_heavy_duty_ab(
        entries, facts, assumptions, t18=t18
    )
    road_gds_mhd_it_ot = Road.calc_goods_medium_and_heavy_duty_it_ot(
        entries, facts, assumptions, t18=t18
    )
    road_gds_mhd = RoadGoodsMediumAndHeavyDuty.calc(
        entries,
        facts,
        assumptions,
        t18=t18,
        it_ot=road_gds_mhd_it_ot,
        ab=road_gds_mhd_ab,
    )
    road_gds_mhd_action_wire = RoadGoodsMediumAndHeavyDuty.calc_action_wire(
        entries, facts, assumptions
    )
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
        entries,
        facts,
        assumptions,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    rail_ppl_distance = RailPeople.calc_distance(
        entries,
        facts,
        assumptions,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    rail_action_invest_infra = InvestmentAction.calc_rail_action_invest_infra(
        entries, facts, assumptions
    )
    rail_action_invest_station = InvestmentAction.calc_rail_action_invest_station(
        entries, facts, assumptions
    )
    rail_ppl_metro_action_infra = RailPeopleMetroActionInfra.calc(
        entries,
        facts,
        assumptions,
        metro_transport_capacity_pkm=rail_ppl_metro.transport.transport_capacity_pkm,
    )
    rail_ppl = RailPeopleSum.calc(
        t18=t18,
        rail_ppl_metro=rail_ppl_metro,
        rail_ppl_distance=rail_ppl_distance,
        rail_ppl_metro_action_infra=rail_ppl_metro_action_infra,
    )
    rail_gds = RailGoods.calc(entries, facts, assumptions, t18=t18)
    rail = Rail.calc(
        t18=t18,
        rail_ppl=rail_ppl,
        rail_gds=rail_gds,
        rail_action_invest_infra=rail_action_invest_infra,
        rail_action_invest_station=rail_action_invest_station,
    )

    # --- Ship ---
    ship_dmstc = ShipDomestic.calc(entries, facts, assumptions, t18=t18)
    ship_inter = ShipInternational.calc(entries, facts, assumptions, t18=t18)
    ship_dmstc_action_infra = ShipDomesticActionInfra.calc(entries, facts, assumptions)
    ship = Ship.calc(
        t18=t18,
        ship_inter=ship_inter,
        ship_dmstc=ship_dmstc,
        ship_dmstc_action_infra=ship_dmstc_action_infra,
    )

    # --- Other ---
    other_cycl = OtherCycle.calc(
        entries,
        facts,
        assumptions,
        t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    other_cycl_action_infra = InvestmentAction.calc_other_cycl_action_infra(
        entries,
        facts,
        assumptions,
        cycle_transport_capacity_pkm=other_cycl.transport.transport_capacity_pkm,
    )
    other_foot = OtherFoot.calc(
        entries,
        facts,
        assumptions,
        t18=t18,
        total_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
    other_foot_action_infra = InvestmentAction.calc_other_foot_action_infra(
        entries, facts, assumptions
    )
    other = Other.calc(
        entries,
        t18=t18,
        other_foot=other_foot,
        other_cycl=other_cycl,
        other_cycl_action_infra=other_cycl_action_infra,
        other_foot_action_infra=other_foot_action_infra,
    )

    return Production(
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
        required_domestic_transport_capacity_pkm=required_domestic_transport_capacity_pkm,
    )
