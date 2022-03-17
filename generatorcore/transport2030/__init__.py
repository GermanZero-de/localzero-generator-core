# pyright: strict

from dataclasses import dataclass, asdict
from ..inputs import Inputs
from ..utils import div
from ..transport2018 import T18
from .investmentaction import InvestmentAction
from .air import calc_air_domestic, AirInternational, Air
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
from .transport import Transport


@dataclass
class GPlanning:
    # Used by g_planning
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        road_bus_action_infra: InvestmentAction,
        road_gds_mhd_action_wire: InvestmentAction,
        road_action_charger: InvestmentAction,
        rail_ppl_metro_action_infra: RailPeopleMetroActionInfra,
        rail_action_invest_infra: InvestmentAction,
        other_cycl: OtherCycle,
    ) -> "GPlanning":
        ass = inputs.ass
        entries = inputs.entries

        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")
        invest = ass("Ass_T_C_planer_cost_per_invest_cost") * (
            road_bus_action_infra.invest
            + road_gds_mhd_action_wire.invest
            + road_action_charger.invest
            + rail_ppl_metro_action_infra.invest
            + rail_action_invest_infra.invest
            + other_cycl.invest
        )
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_com = invest_com / entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        cost_wage = invest_pa
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
        demand_emplo_com = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class EnergySum:
    # Used by s, s_diesel, s_emethan, s_jetfuel, s_petrol, s_fueloil, s_lpg, s_gas, s_biogas, s_bioethanol, s_biodiesel, s_elec, s_hydrogen
    energy: float


@dataclass
class G:
    # Used by g
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float


@dataclass
class T(Transport):
    # Used by t
    cost_wage: float
    demand_emplo: float
    demand_emplo_com: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        total_transport_capacity_pkm: float,
        air: Air,
        rail: Rail,
        road: RoadSum,
        ship: Ship,
        other: Other,
        g: G,
    ) -> "T":
        sum = Transport.sum(air, rail, road, ship, other, transport2018=t18.t)
        invest_com = (
            g.invest_com
            + road.invest_com
            + rail.invest_com
            + ship.invest_com
            + other.invest_com
            + air.invest_com
        )
        invest_pa_com = (
            g.invest_pa_com
            + road.invest_pa_com
            + rail.invest_pa_com
            + ship.invest_pa_com
            + other.invest_pa_com
            + air.invest_pa_com
        )
        invest = (
            road.invest
            + rail.invest
            + ship.invest
            + other.invest
            + air.invest
            + g.invest
        )
        cost_wage = (
            g.cost_wage
            + road.cost_wage
            + rail.cost_wage
            + ship.cost_wage
            + other.cost_wage
        )
        demand_emplo = (
            g.demand_emplo
            + air.demand_emplo
            + road.demand_emplo
            + rail.demand_emplo
            + ship.demand_emplo
            + other.demand_emplo
        )
        demand_emplo_new = (
            g.demand_emplo_new
            + air.demand_emplo_new
            + road.demand_emplo_new
            + rail.demand_emplo_new
            + ship.demand_emplo_new
            + other.demand_emplo_new
        )
        invest_pa = (
            road.invest_pa
            + rail.invest_pa
            + ship.invest_pa
            + other.invest_pa
            + air.invest_pa
            + g.invest_pa
        )
        demand_emplo_com = g.demand_emplo_com

        res = cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            **asdict(sum),
        )
        # TODO: Talk with Leon about this. Because the computed transport capacity is not equal to the precomputed
        # required transport capacity.
        # For Göttingen 2050:
        # computed is: 1354291254.7988613
        # required is: 1308219008.6132076
        # So we actually have more than we precompute, so maybe this is just fine / expected?
        # In which case we probably should want this assert:
        # Maybe this is mostly caused by air and other?
        assert (
            total_transport_capacity_pkm <= res.transport_capacity_pkm
        ), "We should know have at least as much provided transport capacity as we required initially"
        res.transport_capacity_pkm = total_transport_capacity_pkm
        return res


@dataclass
class T30:
    air_inter: AirInternational
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
    s: EnergySum
    s_diesel: EnergySum
    s_emethan: EnergySum
    s_jetfuel: EnergySum
    s_petrol: EnergySum
    s_fueloil: EnergySum
    s_lpg: EnergySum
    s_gas: EnergySum
    s_biogas: EnergySum
    s_bioethanol: EnergySum
    s_biodiesel: EnergySum
    s_elec: EnergySum
    s_hydrogen: EnergySum
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


def calc(inputs: Inputs, *, t18: T18) -> T30:
    ass = inputs.ass
    entries = inputs.entries

    # --- Air ---
    air_dmstc = calc_air_domestic(inputs, t18)
    air_inter = AirInternational.calc(inputs, t18)
    air = Air.calc(t18, domestic=air_dmstc, international=air_inter)

    # First we estimate the total required transport capacity in the target year (excluding air).
    total_transport_capacity_pkm = entries.m_population_com_203X * (
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
        inputs, t18=t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    road_car_ab = Road.calc_car_ab(
        inputs, t18=t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    road_car = RoadCar.calc(inputs, t18=t18, it_ot=road_car_it_ot, ab=road_car_ab)
    road_action_charger = RoadInvestmentAction.calc_car_action_charger(
        inputs, car_base_unit=road_car.base_unit
    )
    road_bus = RoadBus.calc(
        inputs, t18=t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    road_bus_action_infra = RoadBus.calc_action_infra(
        inputs, bus_transport_capacity_pkm=road_bus.transport_capacity_pkm
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
        inputs, t18=t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    rail_ppl_distance = RailPeople.calc_distance(
        inputs, t18=t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    rail_action_invest_infra = InvestmentAction.calc_rail_action_invest_infra(inputs)
    rail_action_invest_station = InvestmentAction.calc_rail_action_invest_station(
        inputs
    )
    rail_ppl_metro_action_infra = RailPeopleMetroActionInfra.calc(
        inputs, metro_transport_capacity_pkm=rail_ppl_metro.transport_capacity_pkm
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
        inputs, t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    other_cycl_action_infra = InvestmentAction.calc_other_cycl_action_infra(
        inputs, cycle_transport_capacity_pkm=other_cycl.transport_capacity_pkm
    )
    other_foot = OtherFoot.calc(
        inputs, t18=t18, total_transport_capacity_pkm=total_transport_capacity_pkm
    )
    other_foot_action_infra = InvestmentAction.calc_other_foot_action_infra(inputs)
    other = Other.calc(
        inputs,
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
        total_transport_capacity_pkm=total_transport_capacity_pkm,
        air=air,
        rail=rail,
        road=road,
        ship=ship,
        other=other,
        g=g,
    )
    s_petrol = EnergySum(t.demand_epetrol)
    s_jetfuel = EnergySum(t.demand_ejetfuel)
    s_diesel = EnergySum(t.demand_ediesel)
    s_elec = EnergySum(t.demand_electricity)
    s_hydrogen = EnergySum(t.demand_hydrogen)

    s_emethan = EnergySum(0)
    s_fueloil = EnergySum(0)
    s_lpg = EnergySum(0)
    s_gas = EnergySum(0)
    s_biogas = EnergySum(0)
    s_bioethanol = EnergySum(0)
    s_biodiesel = EnergySum(0)

    s = EnergySum(
        s_petrol.energy
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
