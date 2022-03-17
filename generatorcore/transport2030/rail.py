from dataclasses import dataclass, asdict
from ..utils import div
from ..inputs import Inputs
from ..transport2018 import T18
from .transport import Transport
from .investmentaction import InvestmentAction


@dataclass
class RailPeople(Transport):
    # Used by rail_ppl_distance and rail_ppl_metro
    base_unit: float
    cost_wage: float
    demand_emplo_new: float
    demand_emplo: float
    emplo_existing: float
    invest_pa: float
    invest_per_x: float
    invest: float
    mileage: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc_metro(
        cls, inputs: Inputs, *, t18: T18, total_transport_capacity_pkm: float
    ) -> "RailPeople":
        ass = inputs.ass
        entries = inputs.entries
        fact = inputs.fact

        transport_capacity_pkm = div(
            total_transport_capacity_pkm * t18.rail_ppl_metro.transport_capacity_pkm,
            (
                t18.road_bus.transport_capacity_pkm
                + t18.rail_ppl_distance.transport_capacity_pkm
                + t18.rail_ppl_metro.transport_capacity_pkm
            ),
        ) * (
            ass("Ass_T_D_trnsprt_ppl_city_pt_frac_2050")
            if entries.t_rt3 == "city"
            else ass("Ass_T_D_trnsprt_ppl_smcty_pt_frac_2050")
            if entries.t_rt3 == "smcty"
            else ass("Ass_T_D_trnsprt_ppl_rural_pt_frac_2050")
            if entries.t_rt3 == "rural"
            else ass("Ass_T_D_trnsprt_ppl_nat_pt_frac_2050")
        )
        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_Rl_Metro_2050")
        demand_electricity = mileage * ass("Ass_T_S_Rl_Metro_SEC_fzkm_2050")
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        base_unit = (mileage - t18.rail_ppl_metro.mileage) / fact(
            "Fact_T_D_rail_metro_ratio_mlg_to_vehicle"
        )
        CO2e_total = CO2e_combustion_based
        change_km = transport_capacity_pkm - t18.rail_ppl_metro.transport_capacity_pkm
        invest_per_x = fact("Fact_T_D_rail_metro_vehicle_invest")
        ratio_wage_to_emplo = ass("Ass_T_D_bus_metro_wage_driver")
        demand_emplo = mileage / fact("Fact_T_D_metro_ratio_mlg_to_driver")
        emplo_existing = t18.rail_ppl_metro.mileage / fact(
            "Fact_T_D_metro_ratio_mlg_to_driver"
        )
        demand_emplo_new = demand_emplo - emplo_existing
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest = base_unit * invest_per_x + cost_wage * entries.m_duration_target
        CO2e_total_2021_estimated = t18.rail_ppl_metro.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = div(cost_wage, invest_pa)
        res = cls(
            base_unit=base_unit,
            change_km=change_km,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_total=CO2e_total,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            invest=invest,
            mileage=mileage,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
            transport2018=t18.rail_ppl_metro,
        )
        return res

    @classmethod
    def calc_distance(
        cls, inputs: Inputs, *, t18: T18, total_transport_capacity_pkm: float
    ) -> "RailPeople":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        transport_capacity_pkm = div(
            total_transport_capacity_pkm * t18.rail_ppl_distance.transport_capacity_pkm,
            t18.road_bus.transport_capacity_pkm
            + t18.rail_ppl_distance.transport_capacity_pkm
            + t18.rail_ppl_metro.transport_capacity_pkm,
        ) * (
            ass("Ass_T_D_trnsprt_ppl_city_pt_frac_2050")
            if entries.t_rt3 == "city"
            else ass("Ass_T_D_trnsprt_ppl_smcty_pt_frac_2050")
            if entries.t_rt3 == "smcty"
            else ass("Ass_T_D_trnsprt_ppl_rural_pt_frac_2050")
            if entries.t_rt3 == "rural"
            else ass("Ass_T_D_trnsprt_ppl_nat_pt_frac_2050")
        )
        demand_electricity = transport_capacity_pkm * ass(
            "Ass_T_S_Rl_Train_ppl_long_elec_SEC_2050"
        )
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        mileage = transport_capacity_pkm / fact(
            "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        )
        base_unit = (mileage - t18.rail_ppl_distance.mileage) / fact(
            "Fact_T_D_rail_ppl_ratio_mlg_to_vehicle"
        )
        demand_emplo = mileage / fact("Fact_T_D_rail_ratio_mlg_to_driver")

        emplo_existing = t18.rail_ppl_distance.mileage / fact(
            "Fact_T_D_rail_ratio_mlg_to_driver"
        )
        demand_emplo_new = demand_emplo - emplo_existing
        CO2e_total = CO2e_combustion_based
        change_km = (
            transport_capacity_pkm - t18.rail_ppl_distance.transport_capacity_pkm
        )
        ratio_wage_to_emplo = ass("Ass_T_D_rail_wage_driver")
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest_per_x = fact("Fact_T_D_rail_ppl_vehicle_invest")
        CO2e_total_2021_estimated = t18.rail_ppl_distance.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest = base_unit * invest_per_x + cost_wage * entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = div(cost_wage, invest_pa)
        res = cls(
            base_unit=base_unit,
            change_km=change_km,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_total=CO2e_total,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            invest=invest,
            mileage=mileage,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
            transport2018=t18.rail_ppl_distance,
        )
        return res


@dataclass
class RailPeopleMetroActionInfra:
    # Used by rail_ppl_metro_action_infra
    base_unit: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    emplo_existing: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    invest_per_x: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls, inputs: Inputs, *, metro_transport_capacity_pkm: float
    ) -> "RailPeopleMetroActionInfra":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_ppl_metro")
        invest = metro_transport_capacity_pkm * invest_per_x
        base_unit = 0
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        invest_pa_com = invest_com / entries.m_duration_target
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        emplo_existing = 0  # nicht existent oder ausgelastet

        demand_emplo = cost_wage / ratio_wage_to_emplo
        demand_emplo_new = demand_emplo

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class RailPeopleSum(Transport):
    # Used by rail_ppl
    base_unit: float
    cost_wage: float
    demand_emplo_new: float
    demand_emplo: float
    emplo_existing: float
    invest_com: float
    invest_pa_com: float
    invest_pa: float
    invest: float
    mileage: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        rail_ppl_metro: RailPeople,
        rail_ppl_distance: RailPeople,
        rail_ppl_metro_action_infra: RailPeopleMetroActionInfra,
    ) -> "RailPeopleSum":
        sum = Transport.sum(
            rail_ppl_metro, rail_ppl_distance, transport2018=t18.rail_ppl
        )
        base_unit = rail_ppl_distance.base_unit + rail_ppl_metro.base_unit
        invest_com = rail_ppl_metro_action_infra.invest_com
        mileage = rail_ppl_distance.mileage + rail_ppl_metro.mileage
        invest = (
            rail_ppl_distance.invest
            + rail_ppl_metro.invest
            + rail_ppl_metro_action_infra.invest
        )
        emplo_existing = (
            rail_ppl_distance.emplo_existing
            + rail_ppl_metro.emplo_existing
            + rail_ppl_metro_action_infra.emplo_existing
        )
        invest_pa = (
            rail_ppl_distance.invest_pa
            + rail_ppl_metro.invest_pa
            + rail_ppl_metro_action_infra.invest_pa
        )
        invest_pa_com = rail_ppl_metro_action_infra.invest_pa_com
        cost_wage = (
            rail_ppl_distance.cost_wage
            + rail_ppl_metro.cost_wage
            + rail_ppl_metro_action_infra.cost_wage
        )
        demand_emplo_new = (
            rail_ppl_distance.demand_emplo_new
            + rail_ppl_metro.demand_emplo_new
            + rail_ppl_metro_action_infra.demand_emplo_new
        )
        demand_emplo = (
            rail_ppl_distance.demand_emplo
            + rail_ppl_metro.demand_emplo
            + rail_ppl_metro_action_infra.demand_emplo
        )

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo_new=demand_emplo_new,
            demand_emplo=demand_emplo,
            emplo_existing=emplo_existing,
            invest=invest,
            invest_com=invest_com,
            invest_pa_com=invest_pa_com,
            invest_pa=invest_pa,
            mileage=mileage,
            **asdict(sum),
        )


@dataclass
class RailGoods(Transport):
    # Used by rail_gds
    base_unit: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    emplo_existing: float
    invest: float
    invest_pa: float
    invest_per_x: float
    pct_of_wage: float
    mileage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(cls, inputs: Inputs, *, t18: T18) -> "RailGoods":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        transport_capacity_tkm = t18.rail_gds.transport_capacity_tkm * (
            ass("Ass_T_D_trnsprt_gds_Rl_2050")
            / fact("Fact_T_D_Rl_train_nat_trnsprt_gds_2018")
        )
        demand_electricity = transport_capacity_tkm * ass(
            "Ass_T_S_Rl_Train_gds_elec_SEC_2050"
        )
        CO2e_combustion_based = demand_electricity * fact(
            "Fact_T_S_electricity_EmFa_tank_wheel_2018"
        )
        mileage = transport_capacity_tkm / fact(
            "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
        )
        CO2e_total_2021_estimated = t18.rail_gds.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        ratio_wage_to_emplo = ass("Ass_T_D_rail_wage_driver")
        demand_emplo = mileage / fact("Fact_T_D_rail_ratio_mlg_to_driver")
        emplo_existing = t18.rail_gds.mileage / fact(
            "Fact_T_D_rail_ratio_mlg_to_driver"
        )
        change_km = transport_capacity_tkm - t18.rail_gds.transport_capacity_tkm
        demand_emplo_new = demand_emplo - emplo_existing

        CO2e_total = CO2e_combustion_based
        base_unit = change_km / fact("Fact_T_D_rail_gds_ratio_mlg_to_vehicle")
        invest_per_x = fact("Fact_T_D_rail_gds_vehicle_invest")
        cost_wage = ratio_wage_to_emplo * demand_emplo_new
        invest = base_unit * invest_per_x + cost_wage * entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = div(cost_wage, invest_pa)

        res = cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            base_unit=base_unit,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            mileage=mileage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=0,
            transport2018=t18.rail_gds,
        )
        return res


@dataclass
class Rail(Transport):
    # Used by rail
    base_unit: float
    cost_wage: float
    demand_emplo_new: float
    demand_emplo: float
    invest_com: float
    invest_pa_com: float
    invest_pa: float
    invest: float
    mileage: float

    @classmethod
    def calc(
        cls,
        *,
        t18: T18,
        rail_ppl: RailPeopleSum,
        rail_gds: RailGoods,
        rail_action_invest_infra: InvestmentAction,
        rail_action_invest_station: InvestmentAction,
    ) -> "Rail":
        sum = Transport.sum(rail_ppl, rail_gds, transport2018=t18.rail)
        invest_com = (
            rail_action_invest_infra.invest_com
            + rail_action_invest_station.invest_com
            + rail_ppl.invest_com
        )
        demand_emplo_new = (
            rail_action_invest_infra.demand_emplo_new
            + rail_action_invest_station.demand_emplo_new
            + rail_ppl.demand_emplo_new
            + rail_gds.demand_emplo_new
        )
        invest_pa_com = (
            rail_action_invest_infra.invest_pa_com
            + rail_action_invest_station.invest_pa_com
            + rail_ppl.invest_pa_com
        )
        mileage = rail_ppl.mileage + rail_gds.mileage
        base_unit = rail_ppl.base_unit + rail_gds.base_unit
        invest_pa = (
            rail_action_invest_infra.invest_pa
            + rail_action_invest_station.invest_pa
            + rail_ppl.invest_pa
            + rail_gds.invest_pa
        )
        demand_emplo = (
            rail_action_invest_infra.demand_emplo
            + rail_action_invest_station.demand_emplo
            + rail_ppl.demand_emplo
            + rail_gds.demand_emplo
        )
        cost_wage = (
            rail_action_invest_infra.cost_wage
            + rail_action_invest_station.cost_wage
            + rail_ppl.cost_wage
            + rail_gds.cost_wage
        )
        invest = (
            rail_action_invest_infra.invest
            + rail_action_invest_station.invest
            + rail_ppl.invest
            + rail_gds.invest
        )

        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            mileage=mileage,
            **asdict(sum),
        )
