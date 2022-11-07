# pyright: strict

from dataclasses import dataclass, asdict

from ..common.energy import Energy

from .energy_demand import (
    InvestmentAction,
    Air,
    Road,
    RoadBus,
    RoadCar,
    RoadGoods,
    RoadGoodsLightDuty,
    RoadGoodsMediumAndHeavyDuty,
    RoadPeople,
    RoadSum,
    RoadInvestmentAction,
    Rail,
    RailGoods,
    RailPeople,
    RailPeopleMetroActionInfra,
    RailPeopleSum,
    Ship,
    ShipDomestic,
    ShipInternational,
    ShipDomesticActionInfra,
    Other,
    OtherCycle,
    OtherFoot,
)
from .transport import Transport
from .dataclasses import GPlanning, G, T


@dataclass(kw_only=True)
class T30:
    air_inter: Transport
    air_dmstc: Transport
    road_ppl: RoadPeople
    road_car: RoadCar
    road_car_it_ot: Road
    road_car_ab: Road
    road_bus: RoadBus
    road_gds: RoadGoods
    road_gds_ldt: RoadGoodsLightDuty
    road_gds_ldt_it_ot: Road
    road_gds_ldt_ab: Road
    road_gds_mhd: RoadGoodsMediumAndHeavyDuty
    road_gds_mhd_it_ot: Road
    road_gds_mhd_ab: Road
    road_gds_mhd_action_wire: InvestmentAction
    rail_ppl: RailPeopleSum
    rail_ppl_distance: RailPeople
    rail_ppl_metro: RailPeople
    rail_gds: RailGoods
    ship: Ship
    ship_dmstc: ShipDomestic
    ship_dmstc_action_infra: ShipDomesticActionInfra
    ship_inter: ShipInternational
    other_foot: OtherFoot
    other_foot_action_infra: InvestmentAction
    other_cycl: OtherCycle
    other_cycl_action_infra: InvestmentAction
    g_planning: GPlanning
    s: Energy
    s_diesel: Energy
    s_emethan: Energy
    s_jetfuel: Energy
    s_petrol: Energy
    s_fueloil: Energy
    s_lpg: Energy
    s_gas: Energy
    s_biogas: Energy
    s_bioethanol: Energy
    s_biodiesel: Energy
    s_elec: Energy
    s_hydrogen: Energy
    g: G
    t: T
    air: Air
    road: RoadSum
    rail: Rail
    other: Other
    rail_action_invest_infra: InvestmentAction
    rail_action_invest_station: InvestmentAction
    rail_ppl_metro_action_infra: RailPeopleMetroActionInfra
    road_action_charger: RoadInvestmentAction
    road_bus_action_infra: InvestmentAction

    def dict(self):
        return asdict(self)
