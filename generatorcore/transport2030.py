from dataclasses import dataclass, field, asdict
from .inputs import Inputs
from .utils import div
from .transport2018 import T18


@dataclass
class AirDomestic:
    # Used by air_dmstc
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    change_km: float
    cost_climate_saved: float

    @classmethod
    def calc(cls, inputs: Inputs, t18: T18) -> "AirDomestic":
        """We assume that no domestic flights are allowed when Germany is carbon neutral as trains
        are a good and cheap alternative (or should be).

        So this just computes the reduction to 0.
        """
        CO2e_total_2021_estimated = t18.air_dmstc.CO2e_combustion_based * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )
        change_km = -t18.air_dmstc.transport_capacity_pkm
        change_energy_MWh = -t18.air_dmstc.energy
        change_energy_pct = div(change_energy_MWh, t18.air_dmstc.energy)
        change_CO2e_t = -t18.air_dmstc.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.air_dmstc.CO2e_combustion_based)
        return cls(
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
        )


@dataclass
class AirInternational:
    # Used by air_inter
    CO2e_combustion_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    change_km: float
    cost_climate_saved: float
    demand_ejetfuel: float
    energy: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    @classmethod
    def calc(cls, inputs: Inputs, t18: T18) -> "AirInternational":
        demand_ejetfuel = (
            inputs.ass("Ass_T_D_Air_nat_EB_2050")
            * inputs.entries.m_population_com_203X
            / inputs.entries.m_population_nat
        )
        transport_capacity_tkm = t18.air_inter.transport_capacity_tkm * div(
            demand_ejetfuel, t18.air_inter.demand_jetfuel
        )
        CO2e_combustion_based = demand_ejetfuel * inputs.ass(
            "Ass_T_S_jetfuel_EmFa_tank_wheel_2050"
        )
        CO2e_total_2021_estimated = t18.air_inter.CO2e_combustion_based * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )
        transport_capacity_pkm = t18.air_inter.transport_capacity_pkm * div(
            demand_ejetfuel, t18.air_inter.demand_jetfuel
        )
        change_km = transport_capacity_pkm - t18.air_inter.transport_capacity_pkm
        energy = demand_ejetfuel
        CO2e_total = CO2e_combustion_based
        change_energy_MWh = energy - t18.air_inter.energy
        change_energy_pct = div(change_energy_MWh, t18.air_inter.energy)
        change_CO2e_t = CO2e_combustion_based - t18.air_inter.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.air_inter.CO2e_combustion_based)
        return cls(
            CO2e_total=CO2e_total,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=transport_capacity_pkm,
            change_energy_pct=change_energy_pct,
            change_energy_MWh=change_energy_MWh,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_km=change_km,
            cost_climate_saved=cost_climate_saved,
            demand_ejetfuel=demand_ejetfuel,
            energy=energy,
        )


@dataclass
class Air:
    # Used by air
    CO2e_combustion_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    change_km: float
    cost_climate_saved: float
    demand_change: float
    demand_ejetfuel: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    @classmethod
    def calc(
        cls,
        t18: T18,
        domestic: AirDomestic,
        international: AirInternational,
    ) -> "Air":
        CO2e_combustion_based = (
            international.CO2e_combustion_based
            # SUM(air_inter.CO2e_cb:CM236)
        )
        demand_ejetfuel = (
            international.demand_ejetfuel  # SUM(air_inter.demand_ejetfuel:BD236)
        )
        energy = demand_ejetfuel
        CO2e_total = CO2e_combustion_based  # (CJ234 + air.CO2e_cb)
        change_energy_MWh = energy - t18.air.energy
        change_energy_pct = div(change_energy_MWh, t18.air.energy)
        change_CO2e_t = CO2e_combustion_based - t18.air.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.air.CO2e_combustion_based)
        transport_capacity_pkm = international.transport_capacity_pkm
        transport_capacity_tkm = international.transport_capacity_tkm
        CO2e_total_2021_estimated = (
            international.CO2e_total_2021_estimated + domestic.CO2e_total_2021_estimated
        )
        cost_climate_saved = (
            international.cost_climate_saved + domestic.cost_climate_saved
        )
        change_km = domestic.change_km + international.change_km

        return cls(
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_combustion_based=CO2e_combustion_based,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            demand_ejetfuel=demand_ejetfuel,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=transport_capacity_tkm,
            energy=energy,
            cost_climate_saved=cost_climate_saved,
            # Our simplified assumption here is that the only costs to get clean international flight is
            # using efuels. Therefore no costs show up here and all in the fuels2030 section.
            demand_change=0,
            invest_pa_com=0,
            invest_com=0,
            invest_pa=0,
            invest=0,
            demand_emplo=0,
            demand_emplo_new=0,
        )


@dataclass
class Vars2:
    # Used by road_ppl
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by road_car
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class RoadCar:
    # Used by road_car_it_ot, road_car_ab
    CO2e_combustion_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    change_km: float
    cost_climate_saved: float
    demand_electricity: float
    demand_epetrol: float
    energy: float
    mileage: float
    transport_capacity_pkm: float

    @classmethod
    def calc_it_ot(
        cls, inputs: Inputs, *, t18: T18, total_transport_capacity_pkm: float
    ) -> "RoadCar":
        ass = inputs.ass
        entries = inputs.entries
        fact = inputs.fact

        transport_capacity_pkm = (
            total_transport_capacity_pkm
            * div(
                t18.road_car_it_ot.mileage,
                t18.road_car_it_ot.mileage + t18.road_car_ab.mileage,
            )
            * (
                (
                    ass("Ass_T_D_trnsprt_ppl_city_car1_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_city_car2_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_city_car3_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_city_car4_frac_2050")
                    if entries.t_rt3 == "city"
                    else ass("Ass_T_D_trnsprt_ppl_smcty_car1_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_smcty_car2_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_smcty_car3_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_smcty_car4_frac_2050")
                    if entries.t_rt3 == "smcty"
                    else ass("Ass_T_D_trnsprt_ppl_rural_car1_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_rural_car2_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_rural_car3_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_rural_car4_frac_2050")
                    if entries.t_rt3 == "rural"
                    else ass("Ass_T_D_trnsprt_ppl_nat_car1_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_nat_car2_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_nat_car3_frac_2050")
                    + ass("Ass_T_D_trnsprt_ppl_nat_car4_frac_2050")
                )
            )
        )
        change_km = transport_capacity_pkm - t18.road_car_it_ot.transport_capacity_pkm
        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_ppl_Car_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_Car_frac_bev_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_elec_it_ot_2030")
        )
        demand_epetrol = (
            mileage
            * ass("Ass_T_S_Car_frac_petrol_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_petrol_it_ot_2050")
        )
        CO2e_combustion_based = demand_epetrol * ass(
            "Ass_T_S_petrol_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        energy = demand_electricity + demand_epetrol
        CO2e_total = CO2e_combustion_based
        change_energy_MWh = energy - t18.road_car_it_ot.energy
        change_energy_pct = div(change_energy_MWh, t18.road_car_it_ot.energy)
        change_CO2e_t = CO2e_combustion_based - t18.road_car_it_ot.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.road_car_it_ot.CO2e_combustion_based)
        CO2e_total_2021_estimated = t18.road_car_it_ot.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        return cls(
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_total=CO2e_total,
            cost_climate_saved=cost_climate_saved,
            demand_electricity=demand_electricity,
            demand_epetrol=demand_epetrol,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=transport_capacity_pkm,
        )

    @classmethod
    def calc_ab(
        cls, inputs: Inputs, *, t18: T18, total_transport_capacity_pkm: float
    ) -> "RoadCar":
        ass = inputs.ass
        entries = inputs.entries
        fact = inputs.fact

        transport_capacity_pkm = (
            total_transport_capacity_pkm
            * div(
                t18.road_car_ab.mileage,
                (t18.road_car_it_ot.mileage + t18.road_car_ab.mileage),
            )
            * (
                ass("Ass_T_D_trnsprt_ppl_city_car1_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_city_car2_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_city_car3_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_city_car4_frac_2050")
                if entries.t_rt3 == "city"
                else ass("Ass_T_D_trnsprt_ppl_smcty_car1_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_smcty_car2_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_smcty_car3_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_smcty_car4_frac_2050")
                if entries.t_rt3 == "smcty"
                else ass("Ass_T_D_trnsprt_ppl_rural_car1_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_rural_car2_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_rural_car3_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_rural_car4_frac_2050")
                if entries.t_rt3 == "rural"
                else ass("Ass_T_D_trnsprt_ppl_nat_car1_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_nat_car2_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_nat_car3_frac_2050")
                + ass("Ass_T_D_trnsprt_ppl_nat_car4_frac_2050")
            )
        )
        mileage = transport_capacity_pkm / ass("Ass_T_D_lf_ppl_Car_2050")
        demand_electricity = (
            mileage
            * ass("Ass_T_S_Car_frac_bev_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_elec_ab_2030")
        )
        demand_epetrol = (
            mileage
            * ass("Ass_T_S_Car_frac_petrol_with_phev_mlg_2050")
            * ass("Ass_T_S_Car_SEC_petrol_ab_2050")
        )
        CO2e_combustion_based = demand_epetrol * ass(
            "Ass_T_S_petrol_EmFa_tank_wheel_2050"
        ) + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        energy = demand_electricity + demand_epetrol
        change_energy_MWh = energy - t18.road_car_ab.energy
        change_km = transport_capacity_pkm - t18.road_car_ab.transport_capacity_pkm
        CO2e_total = CO2e_combustion_based
        change_energy_pct = div(change_energy_MWh, t18.road_car_ab.energy)
        change_CO2e_t = CO2e_combustion_based - t18.road_car_ab.CO2e_combustion_based
        change_CO2e_pct = div(change_CO2e_t, t18.road_car_ab.CO2e_combustion_based)
        CO2e_total_2021_estimated = t18.road_car_ab.CO2e_combustion_based * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_combustion_based)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_km=change_km,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            CO2e_total=CO2e_total,
            cost_climate_saved=cost_climate_saved,
            demand_electricity=demand_electricity,
            demand_epetrol=demand_epetrol,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=transport_capacity_pkm,
        )


@dataclass
class Vars5:
    # Used by road_bus
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    mileage: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by road_gds
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by road_gds_ldt
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by road_gds_ldt_it_ot, road_gds_ldt_ab, road_gds_mhd_it_ot, road_gds_mhd_ab
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars9:
    # Used by road_gds_mhd
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars10:
    # Used by road_gds_mhd_action_wire, other_foot_action_infra, other_cycl_action_infra, rail_action_invest_infra, rail_action_invest_station, road_bus_action_infra
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars11:
    # Used by rail_ppl
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars12:
    # Used by rail_ppl_distance
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    mileage: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars13:
    # Used by rail_ppl_metro
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    mileage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars14:
    # Used by rail_gds
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    mileage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars15:
    # Used by ship
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars16:
    # Used by ship_dmstc
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars17:
    # Used by ship_dmstc_action_infra
    CO2e_total_2021_estimated: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars18:
    # Used by ship_inter
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    energy: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars19:
    # Used by other_foot
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars20:
    # Used by other_cycl
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars21:
    # Used by g_planning
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars22:
    # Used by s, s_diesel, s_emethan, s_jetfuel, s_petrol, s_fueloil, s_lpg, s_gas, s_biogas, s_bioethanol, s_biodiesel, s_elec, s_hydrogen
    energy: float = None  # type: ignore


@dataclass
class Vars23:
    # Used by g
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore


@dataclass
class Vars24:
    # Used by t
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_ejetfuel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars26:
    # Used by road
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars27:
    # Used by rail
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    mileage: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore
    transport_capacity_tkm: float = None  # type: ignore


@dataclass
class Vars28:
    # Used by other
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    base_unit: float = None  # type: ignore
    change_km: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    transport_capacity_pkm: float = None  # type: ignore


@dataclass
class Vars29:
    # Used by rail_ppl_metro_action_infra
    base_unit: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars30:
    # Used by road_action_charger
    base_unit: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class T30:
    air_inter: AirInternational = None  # type: ignore
    air_dmstc: AirDomestic = None  # type: ignore
    road_ppl: Vars2 = field(default_factory=Vars2)
    road_car: Vars3 = field(default_factory=Vars3)
    road_car_it_ot: RoadCar = None  # type: ignore
    road_car_ab: RoadCar = None  # type: ignore
    road_bus: Vars5 = field(default_factory=Vars5)
    road_gds: Vars6 = field(default_factory=Vars6)
    road_gds_ldt: Vars7 = field(default_factory=Vars7)
    road_gds_ldt_it_ot: Vars8 = field(default_factory=Vars8)
    road_gds_ldt_ab: Vars8 = field(default_factory=Vars8)
    road_gds_mhd: Vars9 = field(default_factory=Vars9)
    road_gds_mhd_it_ot: Vars8 = field(default_factory=Vars8)
    road_gds_mhd_ab: Vars8 = field(default_factory=Vars8)
    road_gds_mhd_action_wire: Vars10 = field(default_factory=Vars10)
    rail_ppl: Vars11 = field(default_factory=Vars11)
    rail_ppl_distance: Vars12 = field(default_factory=Vars12)
    rail_ppl_metro: Vars13 = field(default_factory=Vars13)
    rail_gds: Vars14 = field(default_factory=Vars14)
    ship: Vars15 = field(default_factory=Vars15)
    ship_dmstc: Vars16 = field(default_factory=Vars16)
    ship_dmstc_action_infra: Vars17 = field(default_factory=Vars17)
    ship_inter: Vars18 = field(default_factory=Vars18)
    other_foot: Vars19 = field(default_factory=Vars19)
    other_foot_action_infra: Vars10 = field(default_factory=Vars10)
    other_cycl: Vars20 = field(default_factory=Vars20)
    other_cycl_action_infra: Vars10 = field(default_factory=Vars10)
    g_planning: Vars21 = field(default_factory=Vars21)
    s: Vars22 = field(default_factory=Vars22)
    s_diesel: Vars22 = field(default_factory=Vars22)
    s_emethan: Vars22 = field(default_factory=Vars22)
    s_jetfuel: Vars22 = field(default_factory=Vars22)
    s_petrol: Vars22 = field(default_factory=Vars22)
    s_fueloil: Vars22 = field(default_factory=Vars22)
    s_lpg: Vars22 = field(default_factory=Vars22)
    s_gas: Vars22 = field(default_factory=Vars22)
    s_biogas: Vars22 = field(default_factory=Vars22)
    s_bioethanol: Vars22 = field(default_factory=Vars22)
    s_biodiesel: Vars22 = field(default_factory=Vars22)
    g: Vars23 = field(default_factory=Vars23)
    t: Vars24 = field(default_factory=Vars24)
    air: Air = None  # type: ignore
    road: Vars26 = field(default_factory=Vars26)
    rail: Vars27 = field(default_factory=Vars27)
    other: Vars28 = field(default_factory=Vars28)
    rail_action_invest_infra: Vars10 = field(default_factory=Vars10)
    rail_action_invest_station: Vars10 = field(default_factory=Vars10)
    rail_ppl_metro_action_infra: Vars29 = field(default_factory=Vars29)
    road_action_charger: Vars30 = field(default_factory=Vars30)
    road_bus_action_infra: Vars10 = field(default_factory=Vars10)
    s_elec: Vars22 = field(default_factory=Vars22)
    s_hydrogen: Vars22 = field(default_factory=Vars22)

    def dict(self):
        return asdict(self)


def calc(inputs: Inputs, *, t18: T18) -> T30:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    entries = inputs.entries

    t30 = T30()

    g = t30.g
    g_planning = t30.g_planning
    other = t30.other
    other_cycl = t30.other_cycl
    other_cycl_action_infra = t30.other_cycl_action_infra
    other_foot = t30.other_foot
    other_foot_action_infra = t30.other_foot_action_infra
    rail = t30.rail
    rail_action_invest_infra = t30.rail_action_invest_infra
    rail_action_invest_station = t30.rail_action_invest_station
    rail_gds = t30.rail_gds
    rail_ppl = t30.rail_ppl
    rail_ppl_distance = t30.rail_ppl_distance
    rail_ppl_metro = t30.rail_ppl_metro
    rail_ppl_metro_action_infra = t30.rail_ppl_metro_action_infra
    road = t30.road
    road_action_charger = t30.road_action_charger
    road_bus = t30.road_bus
    road_bus_action_infra = t30.road_bus_action_infra
    road_car = t30.road_car
    road_car_ab = t30.road_car_ab
    road_gds = t30.road_gds
    road_gds_ldt = t30.road_gds_ldt
    road_gds_ldt_ab = t30.road_gds_ldt_ab
    road_gds_ldt_it_ot = t30.road_gds_ldt_it_ot
    road_gds_mhd = t30.road_gds_mhd
    road_gds_mhd_ab = t30.road_gds_mhd_ab
    road_gds_mhd_action_wire = t30.road_gds_mhd_action_wire
    road_gds_mhd_it_ot = t30.road_gds_mhd_it_ot
    road_ppl = t30.road_ppl
    rail_ppl_distance = t30.rail_ppl_distance
    s = t30.s
    s_diesel = t30.s_diesel
    s_elec = t30.s_elec
    s_emethan = t30.s_emethan
    s_hydrogen = t30.s_hydrogen
    s_jetfuel = t30.s_jetfuel
    s_petrol = t30.s_petrol
    s_fueloil = t30.s_fueloil
    s_lpg = t30.s_lpg
    s_gas = t30.s_gas
    s_biogas = t30.s_biogas
    s_bioethanol = t30.s_bioethanol
    s_biodiesel = t30.s_biodiesel
    ship = t30.ship
    ship_dmstc = t30.ship_dmstc
    ship_dmstc_action_infra = t30.ship_dmstc_action_infra
    ship_inter = t30.ship_inter
    t = t30.t

    s_fueloil.energy = 0
    s_lpg.energy = 0
    s_gas.energy = 0
    s_biogas.energy = 0
    s_bioethanol.energy = 0
    s_biodiesel.energy = 0

    air_dmstc = AirDomestic.calc(inputs, t18)
    air_inter = AirInternational.calc(inputs, t18)
    air = Air.calc(t18, domestic=air_dmstc, international=air_inter)
    t30.air_dmstc = air_dmstc
    t30.air_inter = air_inter
    t30.air = air

    # First we estimate the total required transport capacity in the target year (excluding air).
    t.transport_capacity_pkm = entries.m_population_com_203X * (
        ass("Ass_T_D_ratio_trnsprt_ppl_to_ppl_city")
        if entries.t_rt3 == "city"
        else ass("Ass_T_D_ratio_trnsprt_ppl_to_ppl_smcity")
        if entries.t_rt3 == "smcty"
        else ass("Ass_T_D_ratio_trnsprt_ppl_to_ppl_rural")
        if entries.t_rt3 == "rural"
        else ass("Ass_T_D_trnsprt_ppl_nat") / entries.m_population_nat
    )

    road_car_it_ot = RoadCar.calc_it_ot(
        inputs, t18=t18, total_transport_capacity_pkm=t.transport_capacity_pkm
    )
    road_car_ab = RoadCar.calc_ab(
        inputs, t18=t18, total_transport_capacity_pkm=t.transport_capacity_pkm
    )

    t30.road_car_it_ot = road_car_it_ot
    t30.road_car_ab = road_car_ab

    road_gds_ldt_it_ot.transport_capacity_tkm = (
        ass("Ass_T_D_trnsprt_gds_Rd_2050")
        / fact("Fact_T_D_trnsprt_gds_Rd_2018")
        * t18.road_gds_ldt_it_ot.transport_capacity_tkm
    )
    road_gds_ldt_it_ot.mileage = road_gds_ldt_it_ot.transport_capacity_tkm / ass(
        "Ass_T_D_lf_gds_LDT_2050"
    )

    road_car.base_unit = (
        road_car_it_ot.transport_capacity_pkm + road_car_ab.transport_capacity_pkm
    ) / fact("Fact_T_S_Car_ratio_mlg_to_stock_2018")
    road_action_charger.base_unit = road_car.base_unit / (
        ass("Ass_S_ratio_bev_car_per_charge_point_city")
        if entries.t_rt3 == "city"
        else ass("Ass_S_ratio_bev_car_per_charge_point_smcity_rural")
        if entries.t_rt3 == "smcty"
        else ass("Ass_S_ratio_bev_car_per_charge_point_smcity_rural")
        if entries.t_rt3 == "rural"
        else ass("Ass_S_ratio_bev_car_per_charge_point_nat")
    )
    road_action_charger.invest_per_x = ass("Ass_T_C_cost_per_charge_point")

    g_planning.ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")

    road_action_charger.invest = (
        road_action_charger.base_unit * road_action_charger.invest_per_x
    )
    road_bus_action_infra.invest_per_x = ass(
        "Ass_T_C_cost_per_trnsprt_ppl_bus_infrstrctr"
    )
    road_bus.transport_capacity_pkm = div(
        t.transport_capacity_pkm * t18.road_bus.transport_capacity_pkm,
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
    road_bus_action_infra.invest = (
        road_bus.transport_capacity_pkm * road_bus_action_infra.invest_per_x
    )
    road_gds_mhd_action_wire.invest_per_x = ass(
        "Ass_T_C_cost_per_trnsprt_gds_truck_infrstrctr"
    )
    road_gds_mhd_action_wire.invest = (
        entries.m_population_com_203X * road_gds_mhd_action_wire.invest_per_x
    )

    rail_action_invest_infra.invest_per_x = ass(
        "Ass_T_C_cost_per_trnsprt_rail_infrstrctr"
    )
    road_action_charger.invest_pa = (
        road_action_charger.invest / entries.m_duration_target
    )
    road.demand_change = 0  # (SUM(BJ239:BJ252))

    road_gds_ldt_ab.transport_capacity_tkm = (
        ass("Ass_T_D_trnsprt_gds_Rd_2050")
        / fact("Fact_T_D_trnsprt_gds_Rd_2018")
        * t18.road_gds_ldt_ab.transport_capacity_tkm
    )

    road_ppl.CO2e_total_2021_estimated = t18.road_ppl.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    road_action_charger.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    road_action_charger.invest_com = road_action_charger.invest * ass(
        "Ass_T_C_invest_state_charge_point_prctg"
    )
    road_car.invest_per_x = ass("Ass_T_S_car_average_price_2050")
    road_bus.ratio_wage_to_emplo = ass("Ass_T_D_bus_metro_wage_driver")
    road_action_charger.cost_wage = (
        road_action_charger.invest_pa * road_action_charger.pct_of_wage
    )
    road_action_charger.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    t.demand_ejetfuel = air.demand_ejetfuel  # + BD237 + BD253 + BD261 + BD265

    road_gds_ldt_it_ot.demand_electricity = (
        road_gds_ldt_it_ot.mileage
        * ass("Ass_T_S_LDT_frac_bev_mlg_2050")
        * ass("Ass_T_S_LDT_SEC_elec_it_ot_2030")
    )

    road_car.demand_electricity = (
        road_car_it_ot.demand_electricity + road_car_ab.demand_electricity
    )
    ship_dmstc.demand_ediesel = (
        ass("Ass_T_D_Shp_dmstc_nat_EB_2050")
        * entries.m_population_com_203X
        / entries.m_population_nat
    )
    road_gds_ldt_ab.mileage = road_gds_ldt_ab.transport_capacity_tkm / ass(
        "Ass_T_D_lf_gds_LDT_2050"
    )
    rail.demand_change = 0  # SUM(BJ256:BJ260))
    rail_action_invest_infra.invest = (
        rail_action_invest_infra.invest_per_x * entries.m_population_com_203X
    )
    road_car.CO2e_combustion_based = (
        road_car_it_ot.CO2e_combustion_based + road_car_ab.CO2e_combustion_based
    )
    road_car.transport_capacity_pkm = (
        road_car_it_ot.transport_capacity_pkm + road_car_ab.transport_capacity_pkm
    )
    rail_gds.transport_capacity_tkm = t18.rail_gds.transport_capacity_tkm * (
        ass("Ass_T_D_trnsprt_gds_Rl_2050")
        / fact("Fact_T_D_Rl_train_nat_trnsprt_gds_2018")
    )
    road_bus.mileage = road_bus.transport_capacity_pkm / ass("Ass_T_D_lf_ppl_Bus_2050")
    road_bus.demand_electricity = (
        road_bus.mileage
        * ass("Ass_T_S_bus_frac_bev_mlg_2050")
        * ass("Ass_T_S_Bus_SEC_elec_2030")
    )
    road_gds_ldt_ab.demand_electricity = (
        road_gds_ldt_ab.mileage
        * ass("Ass_T_S_LDT_frac_bev_mlg_2050")
        * ass("Ass_T_S_LDT_SEC_elec_ab_2030")
    )
    road_bus.CO2e_combustion_based = road_bus.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    road_ppl.CO2e_combustion_based = (
        road_car.CO2e_combustion_based + road_bus.CO2e_combustion_based
    )
    rail_ppl.CO2e_total_2021_estimated = t18.rail_ppl.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )

    rail_ppl_metro_action_infra.invest_per_x = ass("Ass_T_C_cost_per_trnsprt_ppl_metro")

    rail_ppl_metro.transport_capacity_pkm = div(
        t.transport_capacity_pkm * t18.rail_ppl_metro.transport_capacity_pkm,
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
    rail_ppl_distance.ratio_wage_to_emplo = ass("Ass_T_D_rail_wage_driver")
    rail_ppl_metro_action_infra.invest = (
        rail_ppl_metro.transport_capacity_pkm * rail_ppl_metro_action_infra.invest_per_x
    )
    rail_action_invest_infra.invest_pa = (
        rail_action_invest_infra.invest / entries.m_duration_target
    )
    other_cycl.invest_per_x = fact("Fact_T_D_cycl_vehicle_invest_hannah")
    rail_action_invest_infra.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    rail_action_invest_infra.cost_wage = (
        rail_action_invest_infra.invest_pa * rail_action_invest_infra.pct_of_wage
    )
    road_action_charger.demand_emplo = div(
        road_action_charger.cost_wage, road_action_charger.ratio_wage_to_emplo
    )
    road_bus_action_infra.invest_pa = (
        road_bus_action_infra.invest / entries.m_duration_target
    )
    road_car.invest = road_car.base_unit * road_car.invest_per_x
    road_bus.demand_emplo = road_bus.mileage / fact(
        "Fact_T_S_bus_ratio_mlg_to_driver_2018"
    )
    road_ppl.demand_electricity = (
        road_car.demand_electricity + road_bus.demand_electricity
    )
    road_action_charger.invest_pa_com = (
        road_action_charger.invest_com / entries.m_duration_target
    )
    road_bus_action_infra.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    road_gds_ldt_it_ot.demand_ediesel = (
        road_gds_ldt_it_ot.mileage
        * ass("Ass_T_S_LDT_frac_diesel_mlg_2050")
        * ass("Ass_T_S_LDT_SEC_diesel_it_ot_2030")
    )
    road_bus_action_infra.cost_wage = (
        road_bus_action_infra.invest_pa * road_bus_action_infra.pct_of_wage
    )
    other_cycl.transport_capacity_pkm = t.transport_capacity_pkm * (
        ass("Ass_T_D_trnsprt_ppl_city_cycl_frac_2050")
        if entries.t_rt3 == "city"
        else ass("Ass_T_D_trnsprt_ppl_smcty_cycl_frac_2050")
        if entries.t_rt3 == "smcty"
        else ass("Ass_T_D_trnsprt_ppl_rural_cycl_frac_2050")
        if entries.t_rt3 == "rural"
        else ass("Ass_T_D_trnsprt_ppl_nat_cycl_frac_2050")
    )
    road_action_charger.demand_emplo_new = road_action_charger.demand_emplo
    road_bus_action_infra.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    # road_action_charger.emplo_existingnicht existent oder ausgelastet)
    road_bus_action_infra.demand_emplo = div(
        road_bus_action_infra.cost_wage, road_bus_action_infra.ratio_wage_to_emplo
    )
    road_gds_ldt_it_ot.CO2e_combustion_based = road_gds_ldt_it_ot.demand_ediesel * ass(
        "Ass_T_S_diesel_EmFa_tank_wheel_2050"
    ) + road_gds_ldt_it_ot.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    road_car.demand_epetrol = road_car_it_ot.demand_epetrol + road_car_ab.demand_epetrol
    road_gds_ldt_ab.demand_hydrogen = (
        road_gds_ldt_ab.mileage
        * ass("Ass_T_S_LDT_frac_fcev_mlg_2050")
        * ass("Ass_T_S_LDT_SEC_fcev_2030")
    )
    road_ppl.transport_capacity_pkm = (
        road_car.transport_capacity_pkm + road_bus.transport_capacity_pkm
    )
    road_gds_ldt_ab.demand_ediesel = (
        road_gds_ldt_ab.mileage
        * ass("Ass_T_S_LDT_frac_diesel_mlg_2050")
        * ass("Ass_T_S_LDT_SEC_diesel_ab_2030")
    )
    road_ppl.change_CO2e_t = (
        road_ppl.CO2e_combustion_based - t18.road_ppl.CO2e_combustion_based
    )
    road_ppl.change_CO2e_pct = div(
        road_ppl.change_CO2e_t, t18.road_ppl.CO2e_combustion_based
    )
    road_gds_mhd_ab.CO2e_total_2021_estimated = (
        t18.road_gds_mhd_ab.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    road_gds.CO2e_total_2021_estimated = t18.road_gds.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    other_cycl.base_unit = (
        other_cycl.transport_capacity_pkm
        * ass("Ass_T_D_cycl_ratio_cargo_to_bikes")
        / ass("Ass_T_D_cycl_cargo_mlg")
    )
    other_cycl.invest = other_cycl.base_unit * other_cycl.invest_per_x
    g_planning.invest = ass("Ass_T_C_planer_cost_per_invest_cost") * (
        road_bus_action_infra.invest
        + road_gds_mhd_action_wire.invest
        + road_action_charger.invest
        + rail_ppl_metro_action_infra.invest
        + rail_action_invest_infra.invest
        + other_cycl.invest
    )
    g_planning.invest_com = g_planning.invest * ass("Ass_T_C_ratio_public_sector_100")
    g.invest_com = g_planning.invest_com
    g_planning.invest_pa_com = g_planning.invest_com / entries.m_duration_target
    g.invest_pa_com = g_planning.invest_pa_com
    road_gds_ldt.base_unit = (
        road_gds_ldt_it_ot.transport_capacity_tkm
        + road_gds_ldt_ab.transport_capacity_tkm
    ) / fact("Fact_T_S_LDT_ratio_mlg_to_stock_2018")
    road_gds_mhd_action_wire.invest_com = road_gds_mhd_action_wire.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )
    road_gds_mhd_action_wire.invest_pa = (
        road_gds_mhd_action_wire.invest / entries.m_duration_target
    )
    road_gds_mhd_action_wire.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    road_gds_mhd_it_ot.transport_capacity_tkm = (
        ass("Ass_T_D_trnsprt_gds_Rd_2050")
        / fact("Fact_T_D_trnsprt_gds_Rd_2018")
        * t18.road_gds_mhd_it_ot.transport_capacity_tkm
    )
    road_gds_mhd_it_ot.mileage = road_gds_mhd_it_ot.transport_capacity_tkm / ass(
        "Ass_T_D_lf_gds_MHD_2050"
    )
    road_gds_mhd_ab.transport_capacity_tkm = (
        ass("Ass_T_D_trnsprt_gds_Rd_2050")
        / fact("Fact_T_D_trnsprt_gds_Rd_2018")
        * t18.road_gds_mhd_ab.transport_capacity_tkm
    )
    road_gds_mhd_ab.mileage = road_gds_mhd_ab.transport_capacity_tkm / ass(
        "Ass_T_D_lf_gds_MHD_2050"
    )
    road_gds_mhd.demand_emplo = (
        road_gds_mhd_it_ot.mileage + road_gds_mhd_ab.mileage
    ) / fact("Fact_T_D_MHD_ratio_mlg_to_driver")
    road_gds_mhd.emplo_existing = (
        t18.road_gds_mhd_it_ot.mileage + t18.road_gds_mhd_ab.mileage
    ) / fact("Fact_T_D_MHD_ratio_mlg_to_driver")
    road_gds_mhd.demand_emplo_new = (
        road_gds_mhd.demand_emplo - road_gds_mhd.emplo_existing
    )
    road_gds.demand_emplo_new = road_gds_mhd.demand_emplo_new  # (SUM(DM247:DM252))

    road_bus.emplo_existing = (
        div(t18.road_bus.mileage, road_bus.mileage) * road_bus.demand_emplo
    )
    road_bus.base_unit = road_bus.mileage / fact("Fact_T_S_Bus_ratio_mlg_to_stock_2018")
    road_ppl.demand_epetrol = road_car.demand_epetrol

    road_gds_ldt.demand_electricity = (
        road_gds_ldt_it_ot.demand_electricity + road_gds_ldt_ab.demand_electricity
    )
    road_car.mileage = road_car_it_ot.mileage + road_car_ab.mileage
    road.transport_capacity_pkm = road_ppl.transport_capacity_pkm
    road_gds_ldt_ab.CO2e_combustion_based = road_gds_ldt_ab.demand_ediesel * ass(
        "Ass_T_S_diesel_EmFa_tank_wheel_2050"
    ) + road_gds_ldt_ab.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    road_bus.CO2e_total = road_bus.CO2e_combustion_based

    road_bus.energy = (
        road_bus.demand_electricity
    )  # (SUM(road_bus.demand_electricity:BJ243))

    road_car.change_CO2e_t = (
        road_car.CO2e_combustion_based - t18.road_car.CO2e_combustion_based
    )
    road_car.change_CO2e_pct = div(
        road_car.change_CO2e_t, t18.road_car.CO2e_combustion_based
    )
    road_car.CO2e_total_2021_estimated = t18.road_car.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    road_car.cost_climate_saved = (
        (road_car.CO2e_total_2021_estimated - road_car.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_bus.change_km = (
        road_bus.transport_capacity_pkm - t18.road_bus.transport_capacity_pkm
    )
    road_bus.invest_per_x = ass("Ass_T_S_bus_average_price_2050")
    road_bus.demand_emplo_new = road_bus.demand_emplo - road_bus.emplo_existing
    g_planning.invest_pa = g_planning.invest / entries.m_duration_target
    road_car.invest_pa = road_car.invest / entries.m_duration_target

    road.demand_epetrol = road_ppl.demand_epetrol

    road_car.change_energy_MWh = (
        road_car_it_ot.change_energy_MWh + road_car_ab.change_energy_MWh
    )

    road_gds_ldt.CO2e_combustion_based = (
        road_gds_ldt_it_ot.CO2e_combustion_based + road_gds_ldt_ab.CO2e_combustion_based
    )
    road_gds_mhd_it_ot.demand_electricity = (
        road_gds_mhd_it_ot.mileage
        * ass("Ass_T_S_MHD_frac_bev_mlg_2050")
        * ass("Ass_T_S_MHD_SEC_elec_it_ot_2030")
    )
    road_car.change_energy_pct = div(road_car.change_energy_MWh, t18.road_car.energy)
    road_car.change_km = road_car_it_ot.change_km + road_car_ab.change_km
    road_gds_mhd_it_ot.demand_ediesel = (
        road_gds_mhd_it_ot.mileage
        * ass("Ass_T_S_MHD_frac_diesel_mlg_2050")
        * ass("Ass_T_S_MHD_SEC_diesel_it_ot_2030")
    )
    t.demand_epetrol = (
        road.demand_epetrol
    )  # (BB234 + road.demand_epetrol + BB253 + BB261 + BB265)
    road_car.energy = road_car_it_ot.energy + road_car_ab.energy
    road_ppl.mileage = road_car.mileage + road_bus.mileage
    g_planning.cost_wage = g_planning.invest_pa
    road_gds_mhd_it_ot.CO2e_combustion_based = road_gds_mhd_it_ot.demand_ediesel * ass(
        "Ass_T_S_diesel_EmFa_tank_wheel_2050"
    ) + road_gds_mhd_it_ot.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    road_car.CO2e_total = road_car_it_ot.CO2e_total + road_car_ab.CO2e_total
    road_bus.change_energy_MWh = road_bus.energy - t18.road_bus.energy
    # road_car.actionKauf von E - Autos  +  Anzahl E - PKW im entry('In_M_year_target'))

    road_ppl.energy = road_car.energy + road_bus.energy
    road_ppl.change_energy_MWh = road_car.change_energy_MWh + road_bus.change_energy_MWh
    road_bus.cost_wage = road_bus.ratio_wage_to_emplo * road_bus.demand_emplo_new
    road_ppl.cost_climate_saved = (
        (road_ppl.CO2e_total_2021_estimated - road_ppl.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_ppl.CO2e_total = road_car.CO2e_total + road_bus.CO2e_total
    road_ppl.change_energy_pct = div(road_ppl.change_energy_MWh, t18.road_ppl.energy)
    road_bus.change_energy_pct = div(road_bus.change_energy_MWh, t18.road_bus.energy)
    road_bus.change_CO2e_t = (
        road_bus.CO2e_combustion_based - t18.road_bus.CO2e_combustion_based
    )
    road_bus.change_CO2e_pct = div(
        road_bus.change_CO2e_t, t18.road_bus.CO2e_combustion_based
    )
    road_bus.CO2e_total_2021_estimated = t18.road_bus.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    road_bus.cost_climate_saved = (
        (road_bus.CO2e_total_2021_estimated - road_bus.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_ppl.change_km = road_car.change_km + road_bus.change_km
    # road_bus.actionKauf E - Busse)

    road_bus_action_infra.demand_emplo_new = road_bus_action_infra.demand_emplo
    road_bus_action_infra.invest_com = road_bus_action_infra.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )
    road_bus.invest = (
        road_bus.base_unit * road_bus.invest_per_x
        + road_bus.cost_wage * entries.m_duration_target
    )
    road_bus.invest_com = road_bus.invest * ass("Ass_T_C_ratio_public_sector_100")
    road_bus.invest_pa = road_bus.invest / entries.m_duration_target
    road_ppl.demand_emplo_new = (
        road_bus.demand_emplo_new + road_bus_action_infra.demand_emplo_new
    )  # (DM241:road_bus_action_infra.demand_emplo_new))
    road_bus.pct_of_wage = div(road_bus.cost_wage, road_bus.invest_pa)
    road.demand_emplo_new = (
        road_action_charger.demand_emplo_new
        + road_ppl.demand_emplo_new
        + road_gds.demand_emplo_new
    )
    road_ppl.invest = road_car.invest + road_bus.invest + road_bus_action_infra.invest
    road_ppl.invest_com = road_bus.invest_com + road_bus_action_infra.invest_com
    road_ppl.base_unit = road_car.base_unit + road_bus.base_unit
    road_bus.invest_pa_com = road_bus.invest_com / entries.m_duration_target
    # road_bus_action_infra.actionAusbau Businfrastruktur )

    road_ppl.invest_pa = (
        road_car.invest_pa + road_bus.invest_pa + road_bus_action_infra.invest_pa
    )
    road_bus_action_infra.invest_pa_com = (
        road_bus_action_infra.invest_com / entries.m_duration_target
    )
    g_planning.demand_emplo = div(g_planning.cost_wage, g_planning.ratio_wage_to_emplo)
    road_ppl.invest_pa_com = (
        road_bus.invest_pa_com + road_bus_action_infra.invest_pa_com
    )
    road_ppl.cost_wage = road_bus.cost_wage + road_bus_action_infra.cost_wage
    road_gds_mhd_action_wire.cost_wage = (
        road_gds_mhd_action_wire.invest_pa * road_gds_mhd_action_wire.pct_of_wage
    )
    rail_action_invest_infra.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    road_ppl.demand_emplo = road_bus.demand_emplo + road_bus_action_infra.demand_emplo
    # road_bus_action_infra.emplo_existingnicht existent oder ausgelastet)
    # road.base_unitAnzahl)

    g.demand_emplo = g_planning.demand_emplo

    g.cost_wage = g_planning.cost_wage

    road_gds_ldt_it_ot.demand_hydrogen = (
        road_gds_ldt_it_ot.mileage
        * ass("Ass_T_S_LDT_frac_fcev_mlg_2050")
        * ass("Ass_T_S_LDT_SEC_fcev_2030")
    )
    road_gds_ldt_it_ot.energy = (
        road_gds_ldt_it_ot.demand_electricity
        + road_gds_ldt_it_ot.demand_ediesel
        + road_gds_ldt_it_ot.demand_hydrogen
    )  # SUM(road_gds_ldt_it_ot.demand_electricity:BJ248))
    road_gds_ldt.mileage = road_gds_ldt_it_ot.mileage + road_gds_ldt_ab.mileage
    road_gds_ldt.transport_capacity_tkm = (
        road_gds_ldt_it_ot.transport_capacity_tkm
        + road_gds_ldt_ab.transport_capacity_tkm
    )
    rail_gds.demand_electricity = rail_gds.transport_capacity_tkm * ass(
        "Ass_T_S_Rl_Train_gds_elec_SEC_2050"
    )
    road_gds_ldt_it_ot.CO2e_total = road_gds_ldt_it_ot.CO2e_combustion_based

    road_gds_ldt_it_ot.change_energy_MWh = (
        road_gds_ldt_it_ot.energy - t18.road_gds_ldt_it_ot.energy
    )
    road_gds_ldt_ab.energy = (
        road_gds_ldt_ab.demand_electricity
        + road_gds_ldt_ab.demand_ediesel
        + road_gds_ldt_ab.demand_hydrogen
    )  # SUM(road_gds_ldt_ab.demand_electricity:BJ249))
    road_gds_mhd_ab.demand_electricity = (
        road_gds_mhd_ab.mileage
        * ass("Ass_T_S_MHD_frac_bev_mlg_2050")
        * ass("Ass_T_S_MHD_SEC_elec_ab_2030")
    )
    road_gds_mhd_ab.demand_ediesel = (
        road_gds_mhd_ab.mileage
        * ass("Ass_T_S_MHD_frac_diesel_mlg_2050")
        * ass("Ass_T_S_MHD_SEC_diesel_ab_2030")
    )
    road_gds_mhd_ab.CO2e_combustion_based = road_gds_mhd_ab.demand_ediesel * ass(
        "Ass_T_S_diesel_EmFa_tank_wheel_2050"
    ) + road_gds_mhd_ab.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    road_gds_mhd.CO2e_combustion_based = (
        road_gds_mhd_it_ot.CO2e_combustion_based + road_gds_mhd_ab.CO2e_combustion_based
    )
    road_gds_ldt_it_ot.change_km = (
        road_gds_ldt_it_ot.transport_capacity_tkm
        - t18.road_gds_ldt_it_ot.transport_capacity_tkm
    )
    road_gds_ldt.invest_per_x = ass("Ass_T_S_LCV_average_price_2050")
    road_gds_mhd_action_wire.invest_pa_com = (
        road_gds_mhd_action_wire.invest_com / entries.m_duration_target
    )
    road_gds.CO2e_combustion_based = (
        road_gds_ldt.CO2e_combustion_based + road_gds_mhd.CO2e_combustion_based
    )
    road_gds.invest_com = road_gds_mhd_action_wire.invest_com
    road_gds.cost_wage = road_gds_mhd_action_wire.cost_wage
    road_gds_mhd_action_wire.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    # road_action_charger.actionAusbau Ladesäulen  +  Anzahl öffentliche Ladesäulen entry('In_M_year_target'))

    road_gds.cost_climate_saved = (
        (road_gds.CO2e_total_2021_estimated - road_gds.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_gds_mhd.base_unit = (
        road_gds_mhd_it_ot.transport_capacity_tkm
        + road_gds_mhd_ab.transport_capacity_tkm
    ) / fact("Fact_T_S_MHD_ratio_mlg_to_stock_2018")
    road_gds_mhd.invest_per_x = ass("Ass_T_S_MHCV_BEV_FCEV_average_price_2050")
    road_gds.invest_pa_com = road_gds_mhd_action_wire.invest_pa_com
    road.cost_wage = (
        road_action_charger.cost_wage + road_ppl.cost_wage + road_gds.cost_wage
    )
    road.invest_pa_com = (
        road_action_charger.invest_pa_com
        + road_ppl.invest_pa_com
        + road_gds.invest_pa_com
    )
    road_gds_mhd_action_wire.demand_emplo = div(
        road_gds_mhd_action_wire.cost_wage, road_gds_mhd_action_wire.ratio_wage_to_emplo
    )

    # road.ratio_wage_to_emploDauerstellen!)

    road_gds_mhd.demand_electricity = (
        road_gds_mhd_it_ot.demand_electricity + road_gds_mhd_ab.demand_electricity
    )
    road_gds.demand_electricity = (
        road_gds_ldt.demand_electricity + road_gds_mhd.demand_electricity
    )
    # road_gds_mhd_action_wire.emplo_existingnicht existent oder ausgelastet)
    road_gds_mhd_action_wire.demand_emplo_new = road_gds_mhd_action_wire.demand_emplo
    road.invest_com = (
        road_action_charger.invest_com
        + road_ppl.invest_com
        # + road_bus.invest_com
        # + road_bus_action_infra.invest_com
        + road_gds.invest_com
    )  # SUM(road_action_charger.invest_com:road_ppl.invest_com,road_gds.invest_com))

    road.demand_electricity = road_ppl.demand_electricity + road_gds.demand_electricity
    road.cost_climate_saved = road_ppl.cost_climate_saved + road_gds.cost_climate_saved
    road_gds_mhd_it_ot.demand_hydrogen = (
        road_gds_mhd_it_ot.mileage
        * ass("Ass_T_S_MHD_frac_fcev_mlg_2050")
        * ass("Ass_T_S_MHD_SEC_fcev_2030")
    )

    road_gds_mhd_it_ot.energy = (
        road_gds_mhd_it_ot.demand_electricity
        + road_gds_mhd_it_ot.demand_ediesel
        + road_gds_mhd_it_ot.demand_hydrogen
    )
    road_gds.base_unit = road_gds_ldt.base_unit + road_gds_mhd.base_unit
    road_gds_mhd.transport_capacity_tkm = (
        road_gds_mhd_it_ot.transport_capacity_tkm
        + road_gds_mhd_ab.transport_capacity_tkm
    )
    road_gds.change_CO2e_t = (
        road_gds.CO2e_combustion_based - t18.road_gds.CO2e_combustion_based
    )
    road_gds_mhd_it_ot.CO2e_total = road_gds_mhd_it_ot.CO2e_combustion_based
    road_gds_mhd_it_ot.change_energy_MWh = (
        road_gds_mhd_it_ot.energy - t18.road_gds_mhd_it_ot.energy
    )
    road_gds_ldt_ab.change_energy_MWh = (
        road_gds_ldt_ab.energy - t18.road_gds_ldt_ab.energy
    )
    road_gds_ldt.change_CO2e_t = (
        road_gds_ldt.CO2e_combustion_based - t18.road_gds_ldt.CO2e_combustion_based
    )
    road_gds_ldt.change_CO2e_pct = div(
        road_gds_ldt.change_CO2e_t, t18.road_gds_ldt.CO2e_combustion_based
    )
    road_gds_ldt.CO2e_total_2021_estimated = (
        t18.road_gds_ldt.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    road_gds_ldt.cost_climate_saved = (
        (road_gds_ldt.CO2e_total_2021_estimated - road_gds_ldt.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_gds_mhd_it_ot.change_km = (
        road_gds_mhd_it_ot.transport_capacity_tkm
        - t18.road_gds_mhd_it_ot.transport_capacity_tkm
    )
    road_gds_ldt_ab.change_km = (
        road_gds_ldt_ab.transport_capacity_tkm
        - t18.road_gds_ldt_ab.transport_capacity_tkm
    )
    road_gds_mhd.invest = road_gds_mhd.base_unit * road_gds_mhd.invest_per_x
    road_gds_ldt.invest = road_gds_ldt.base_unit * road_gds_ldt.invest_per_x
    road_gds.invest = road_gds_ldt.invest + road_gds_mhd.invest
    road_gds_ldt.invest_pa = road_gds_ldt.invest / entries.m_duration_target
    road_gds_ldt.demand_ediesel = (
        road_gds_ldt_it_ot.demand_ediesel + road_gds_ldt_ab.demand_ediesel
    )
    road_gds_mhd.demand_ediesel = (
        road_gds_mhd_it_ot.demand_ediesel + road_gds_mhd_ab.demand_ediesel
    )

    road_gds.demand_ediesel = road_gds_ldt.demand_ediesel + road_gds_mhd.demand_ediesel
    road_gds_mhd_ab.demand_hydrogen = (
        road_gds_mhd_ab.mileage
        * ass("Ass_T_S_MHD_frac_fcev_mlg_2050")
        * ass("Ass_T_S_MHD_SEC_fcev_2030")
    )
    road_gds_ldt.demand_hydrogen = (
        road_gds_ldt_it_ot.demand_hydrogen + road_gds_ldt_ab.demand_hydrogen
    )
    road_gds_mhd.demand_hydrogen = (
        road_gds_mhd_it_ot.demand_hydrogen + road_gds_mhd_ab.demand_hydrogen
    )
    road_gds.demand_hydrogen = (
        road_gds_ldt.demand_hydrogen + road_gds_mhd.demand_hydrogen
    )
    road.demand_ediesel = road_gds.demand_ediesel

    road.demand_hydrogen = road_gds.demand_hydrogen

    road.energy = (
        road.demand_electricity
        + road.demand_epetrol
        + road.demand_ediesel
        + road.demand_hydrogen
        + road.demand_change
    )  # SUM(road.demand_electricity:road.demand_change))

    road_gds_ldt.change_energy_MWh = (
        road_gds_ldt_it_ot.change_energy_MWh + road_gds_ldt_ab.change_energy_MWh
    )
    road_gds.change_CO2e_pct = div(
        road_gds.change_CO2e_t, t18.road_gds.CO2e_combustion_based
    )

    road.CO2e_combustion_based = (
        road_ppl.CO2e_combustion_based + road_gds.CO2e_combustion_based
    )
    road_gds_ldt_ab.CO2e_total = road_gds_ldt_ab.CO2e_combustion_based
    road_gds_ldt.change_energy_pct = div(
        road_gds_ldt.change_energy_MWh, t18.road_gds_ldt.energy
    )
    road_gds_ldt_it_ot.change_energy_pct = div(
        road_gds_ldt_it_ot.change_energy_MWh, t18.road_gds_ldt_it_ot.energy
    )
    road_gds_ldt_it_ot.change_CO2e_t = (
        road_gds_ldt_it_ot.CO2e_combustion_based
        - t18.road_gds_ldt_it_ot.CO2e_combustion_based
    )
    road_gds_ldt_it_ot.change_CO2e_pct = div(
        road_gds_ldt_it_ot.change_CO2e_t, t18.road_gds_ldt_it_ot.CO2e_combustion_based
    )
    road_gds_ldt_it_ot.CO2e_total_2021_estimated = (
        t18.road_gds_ldt_it_ot.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    road_gds_ldt_it_ot.cost_climate_saved = (
        (
            road_gds_ldt_it_ot.CO2e_total_2021_estimated
            - road_gds_ldt_it_ot.CO2e_combustion_based
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_gds_ldt.change_km = road_gds_ldt_it_ot.change_km + road_gds_ldt_ab.change_km
    road.change_energy_MWh = road.energy - t18.road.energy
    road.change_CO2e_t = road.CO2e_combustion_based - t18.road.CO2e_combustion_based

    road_gds_ldt.energy = road_gds_ldt_it_ot.energy + road_gds_ldt_ab.energy
    road_gds_mhd.mileage = road_gds_mhd_it_ot.mileage + road_gds_mhd_ab.mileage
    road_gds.transport_capacity_tkm = (
        road_gds_ldt.transport_capacity_tkm + road_gds_mhd.transport_capacity_tkm
    )
    road.change_CO2e_pct = div(road.change_CO2e_t, t18.road.CO2e_combustion_based)
    road_gds_ldt.CO2e_total = road_gds_ldt_it_ot.CO2e_total + road_gds_ldt_ab.CO2e_total
    road_gds_mhd_ab.energy = (
        road_gds_mhd_ab.demand_electricity
        + road_gds_mhd_ab.demand_ediesel
        + road_gds_mhd_ab.demand_hydrogen
    )  # SUM(road_gds_mhd_ab.demand_electricity:BJ252))
    road_gds_ldt_ab.change_energy_pct = div(
        road_gds_ldt_ab.change_energy_MWh, t18.road_gds_ldt_ab.energy
    )
    road_gds_ldt_ab.change_CO2e_t = (
        road_gds_ldt_ab.CO2e_combustion_based
        - t18.road_gds_ldt_ab.CO2e_combustion_based
    )
    road_gds_ldt_ab.change_CO2e_pct = div(
        road_gds_ldt_ab.change_CO2e_t, t18.road_gds_ldt_ab.CO2e_combustion_based
    )
    road_gds_ldt_ab.CO2e_total_2021_estimated = (
        t18.road_gds_ldt_ab.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    road_gds_ldt_ab.cost_climate_saved = (
        (
            road_gds_ldt_ab.CO2e_total_2021_estimated
            - road_gds_ldt_ab.CO2e_combustion_based
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # road_gds_ldt.actionAntriebswechsel leichte Nutzfahrzeuge)
    rail_ppl_metro.mileage = rail_ppl_metro.transport_capacity_pkm / ass(
        "Ass_T_D_lf_Rl_Metro_2050"
    )

    road_gds_mhd_ab.change_energy_MWh = (
        road_gds_mhd_ab.energy - t18.road_gds_mhd_ab.energy
    )
    road_gds.mileage = road_gds_ldt.mileage + road_gds_mhd.mileage
    road.transport_capacity_tkm = road_gds.transport_capacity_tkm
    rail_ppl_metro.demand_electricity = rail_ppl_metro.mileage * ass(
        "Ass_T_S_Rl_Metro_SEC_fzkm_2050"
    )
    road_gds_mhd_ab.CO2e_total = road_gds_mhd_ab.CO2e_combustion_based
    road_gds_mhd.change_energy_MWh = (
        road_gds_mhd_it_ot.change_energy_MWh + road_gds_mhd_ab.change_energy_MWh
    )
    road_gds_mhd.change_energy_pct = div(
        road_gds_mhd.change_energy_MWh, t18.road_gds_mhd.energy
    )
    road_gds_mhd.change_CO2e_t = (
        road_gds_mhd.CO2e_combustion_based - t18.road_gds_mhd.CO2e_combustion_based
    )
    road_gds_mhd.change_CO2e_pct = div(
        road_gds_mhd.change_CO2e_t, t18.road_gds_mhd.CO2e_combustion_based
    )
    road_gds_mhd.CO2e_total_2021_estimated = (
        t18.road_gds_mhd.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    road_gds_mhd.cost_climate_saved = (
        (road_gds_mhd.CO2e_total_2021_estimated - road_gds_mhd.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_gds_mhd_ab.change_km = (
        road_gds_mhd_ab.transport_capacity_tkm
        - t18.road_gds_mhd_ab.transport_capacity_tkm
    )
    road_gds_mhd.change_km = road_gds_mhd_it_ot.change_km + road_gds_mhd_ab.change_km
    road_gds_mhd.invest_pa = road_gds_mhd.invest / entries.m_duration_target
    road_gds.invest_pa = (
        road_gds_mhd_action_wire.invest_pa
        + road_gds_ldt.invest_pa
        + road_gds_mhd.invest_pa
    )
    # road_gds_mhd_action_wire.actionOberleitung - LKW - Infrastruktur)
    road.invest = road_action_charger.invest + road_ppl.invest + road_gds.invest
    road.change_energy_pct = div(road.change_energy_MWh, t18.road.energy)
    road_gds_mhd.energy = road_gds_mhd_it_ot.energy + road_gds_mhd_ab.energy
    road_gds.demand_emplo = (
        road_gds_mhd_action_wire.demand_emplo + road_gds_mhd.demand_emplo
    )
    road.invest_pa = (
        road_action_charger.invest_pa + road_ppl.invest_pa + road_gds.invest_pa
    )
    road.CO2e_total = road.CO2e_combustion_based
    road_gds_mhd.CO2e_total = road_gds_mhd_it_ot.CO2e_total + road_gds_mhd_ab.CO2e_total
    road_gds.change_energy_MWh = (
        road_gds_ldt.change_energy_MWh + road_gds_mhd.change_energy_MWh
    )
    road_gds_mhd_it_ot.change_energy_pct = div(
        road_gds_mhd_it_ot.change_energy_MWh, t18.road_gds_mhd_it_ot.energy
    )
    road_gds_mhd_it_ot.change_CO2e_t = (
        road_gds_mhd_it_ot.CO2e_combustion_based
        - t18.road_gds_mhd_it_ot.CO2e_combustion_based
    )
    road_gds_mhd_it_ot.change_CO2e_pct = div(
        road_gds_mhd_it_ot.change_CO2e_t, t18.road_gds_mhd_it_ot.CO2e_combustion_based
    )
    road_gds_mhd_it_ot.CO2e_total_2021_estimated = (
        t18.road_gds_mhd_it_ot.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    road_gds_mhd_it_ot.cost_climate_saved = (
        (
            road_gds_mhd_it_ot.CO2e_total_2021_estimated
            - road_gds_mhd_it_ot.CO2e_combustion_based
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    road_gds.change_km = road_gds_ldt.change_km + road_gds_mhd.change_km
    rail_ppl_distance.transport_capacity_pkm = div(
        t.transport_capacity_pkm * t18.rail_ppl_distance.transport_capacity_pkm,
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
    rail_ppl_distance.demand_electricity = (
        rail_ppl_distance.transport_capacity_pkm
        * ass("Ass_T_S_Rl_Train_ppl_long_elec_SEC_2050")
    )
    rail_ppl_distance.CO2e_combustion_based = (
        rail_ppl_distance.demand_electricity
        * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
    )

    rail_ppl.demand_electricity = (
        rail_ppl_distance.demand_electricity + rail_ppl_metro.demand_electricity
    )
    t.demand_hydrogen = road.demand_hydrogen

    road_gds.energy = road_gds_ldt.energy + road_gds_mhd.energy
    road.mileage = road_ppl.mileage + road_gds.mileage
    road.demand_emplo = (
        road_action_charger.demand_emplo + road_ppl.demand_emplo + road_gds.demand_emplo
    )
    rail_ppl_metro.CO2e_combustion_based = rail_ppl_metro.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    road_gds.CO2e_total = road_gds_ldt.CO2e_total + road_gds_mhd.CO2e_total
    road_gds.change_energy_pct = div(road_gds.change_energy_MWh, t18.road_gds.energy)
    road_gds_mhd_ab.change_energy_pct = div(
        road_gds_mhd_ab.change_energy_MWh, t18.road_gds_mhd_ab.energy
    )
    road_gds_mhd_ab.change_CO2e_t = (
        road_gds_mhd_ab.CO2e_combustion_based
        - t18.road_gds_mhd_ab.CO2e_combustion_based
    )
    road_gds_mhd_ab.change_CO2e_pct = div(
        road_gds_mhd_ab.change_CO2e_t, t18.road_gds_mhd_ab.CO2e_combustion_based
    )
    road.CO2e_total_2021_estimated = (
        road_ppl.CO2e_total_2021_estimated
        + road_car.CO2e_total_2021_estimated
        + road_car_it_ot.CO2e_total_2021_estimated
        + road_car_ab.CO2e_total_2021_estimated
        + road_bus.CO2e_total_2021_estimated
        + road_gds.CO2e_total_2021_estimated
        + road_gds_ldt.CO2e_total_2021_estimated
        + road_gds_ldt_it_ot.CO2e_total_2021_estimated
        + road_gds_ldt_ab.CO2e_total_2021_estimated
        + road_gds_mhd.CO2e_total_2021_estimated
        + road_gds_mhd_it_ot.CO2e_total_2021_estimated
        + road_gds_mhd_ab.CO2e_total_2021_estimated
        # SUM(road_ppl.CO2e_total_2021_estimated:road_gds_mhd_ab.CO2e_total_2021_estimated)
    )
    road_gds_mhd_ab.cost_climate_saved = (
        (
            road_gds_mhd_ab.CO2e_total_2021_estimated
            - road_gds_mhd_ab.CO2e_combustion_based
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    # road_gds_mhd.actionAntriebswechsel Lkw  -  BEV / FCEV

    ship.demand_change = 0

    other.demand_change = 0

    rail.demand_electricity = rail_ppl.demand_electricity + rail_gds.demand_electricity
    rail_ppl_distance.mileage = rail_ppl_distance.transport_capacity_pkm / fact(
        "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
    )
    rail_ppl.CO2e_combustion_based = (
        rail_ppl_distance.CO2e_combustion_based + rail_ppl_metro.CO2e_combustion_based
    )
    ship_dmstc.transport_capacity_tkm = (
        ass("Ass_T_D_trnsprt_gds_ship_2050")
        * entries.m_population_com_203X
        / entries.m_population_nat
    )
    ship_dmstc.CO2e_combustion_based = ship_dmstc.demand_ediesel * ass(
        "Ass_T_S_diesel_EmFa_tank_wheel_2050"
    )
    rail_gds.CO2e_combustion_based = rail_gds.demand_electricity * fact(
        "Fact_T_S_electricity_EmFa_tank_wheel_2018"
    )
    rail.energy = (
        rail.demand_electricity + rail.demand_change
    )  # SUM(rail.demand_electricity:rail.demand_change)
    rail.change_energy_MWh = rail.energy - t18.rail.energy
    rail.CO2e_combustion_based = (
        rail_ppl.CO2e_combustion_based + rail_gds.CO2e_combustion_based
    )
    rail.change_CO2e_t = rail.CO2e_combustion_based - t18.rail.CO2e_combustion_based
    ship_dmstc.CO2e_total_2021_estimated = t18.ship_dmstc.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    ship_dmstc.cost_climate_saved = (
        (ship_dmstc.CO2e_total_2021_estimated - ship_dmstc.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    ship_dmstc_action_infra.invest = (
        ass("Ass_T_C_invest_water_ways")
        * entries.m_population_com_203X
        / entries.m_population_nat
    )
    ship_dmstc_action_infra.invest_com = ship_dmstc_action_infra.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )
    ship.invest = (
        ship_dmstc_action_infra.invest
    )  # SUM(ship_dmstc_action_infra.invest:DD264)
    ship.invest_com = (
        ship_dmstc_action_infra.invest_com
    )  # SUM(ship_dmstc_action_infra.invest_com:DE264)
    ship_dmstc.ratio_wage_to_emplo = ass("Ass_T_D_shp_wage_driver")
    ship_dmstc.demand_emplo = ship_dmstc.transport_capacity_tkm / fact(
        "Fact_T_D_shp_ratio_mlg_to_driver"
    )
    ship_dmstc.emplo_existing = t18.ship_dmstc.transport_capacity_tkm / fact(
        "Fact_T_D_shp_ratio_mlg_to_driver"
    )
    rail_ppl_distance.base_unit = (
        rail_ppl_distance.mileage - t18.rail_ppl_distance.mileage
    ) / fact("Fact_T_D_rail_ppl_ratio_mlg_to_vehicle")
    rail_ppl_metro.base_unit = (
        rail_ppl_metro.mileage - t18.rail_ppl_metro.mileage
    ) / fact("Fact_T_D_rail_metro_ratio_mlg_to_vehicle")
    rail_ppl_metro_action_infra.base_unit = 0
    rail_ppl.base_unit = (
        rail_ppl_distance.base_unit
        + rail_ppl_metro.base_unit
        + rail_ppl_metro_action_infra.base_unit
    )  # SUM(rail_ppl_distance.base_unit:DO259)
    rail_ppl_distance.demand_emplo = rail_ppl_distance.mileage / fact(
        "Fact_T_D_rail_ratio_mlg_to_driver"
    )
    rail_ppl_metro_action_infra.invest_com = rail_ppl_metro_action_infra.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )

    rail_action_invest_infra.demand_emplo = div(
        rail_action_invest_infra.cost_wage, rail_action_invest_infra.ratio_wage_to_emplo
    )

    rail_action_invest_infra.invest_com = rail_action_invest_infra.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )
    rail_action_invest_infra.demand_emplo_new = rail_action_invest_infra.demand_emplo
    rail_ppl_metro_action_infra.invest_pa = (
        rail_ppl_metro_action_infra.invest / entries.m_duration_target
    )
    rail_action_invest_station.invest_per_x = ass(
        "Ass_T_C_cost_per_trnsprt_rail_train station"
    )
    rail_action_invest_station.invest = (
        rail_action_invest_station.invest_per_x * entries.m_population_com_203X
    )
    rail_action_invest_station.invest_com = rail_action_invest_station.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )
    rail_action_invest_station.invest_pa_com = (
        rail_action_invest_station.invest_com / entries.m_duration_target
    )

    # rail_action_invest_infra.emplo_existingnicht existent oder ausgelastet

    rail_action_invest_station.invest_pa = (
        rail_action_invest_station.invest / entries.m_duration_target
    )
    rail_action_invest_infra.invest_pa_com = (
        rail_action_invest_infra.invest_com / entries.m_duration_target
    )
    # rail_action_invest_station.actionSchienenverkehr Investitionen  Bahnhöfe

    rail_action_invest_station.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    rail_action_invest_station.cost_wage = (
        rail_action_invest_station.invest_pa * rail_action_invest_station.pct_of_wage
    )
    rail_action_invest_station.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )

    rail_action_invest_station.demand_emplo = div(
        rail_action_invest_station.cost_wage,
        rail_action_invest_station.ratio_wage_to_emplo,
    )

    rail_action_invest_station.demand_emplo_new = (
        rail_action_invest_station.demand_emplo
    )
    rail_ppl_distance.emplo_existing = t18.rail_ppl_distance.mileage / fact(
        "Fact_T_D_rail_ratio_mlg_to_driver"
    )
    rail_ppl_distance.demand_emplo_new = (
        rail_ppl_distance.demand_emplo - rail_ppl_distance.emplo_existing
    )
    rail_ppl_metro_action_infra.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    # rail_action_invest_station.emplo_existingnicht existent oder ausgelastet

    rail.change_CO2e_pct = div(rail.change_CO2e_t, t18.rail.CO2e_combustion_based)
    rail_ppl_distance.energy = rail_ppl_distance.demand_electricity
    rail_gds.mileage = rail_gds.transport_capacity_tkm / fact(
        "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
    )
    rail_ppl.transport_capacity_pkm = (
        rail_ppl_distance.transport_capacity_pkm + rail_ppl_metro.transport_capacity_pkm
    )
    ship_inter.demand_ediesel = (
        ass("Ass_T_D_Shp_sea_nat_EB_2050")
        * entries.m_population_com_203X
        / entries.m_population_nat
    )
    rail_ppl_distance.CO2e_total = rail_ppl_distance.CO2e_combustion_based
    rail_ppl_distance.change_energy_MWh = (
        rail_ppl_distance.energy - t18.rail_ppl_distance.energy
    )
    rail_ppl_metro.energy = rail_ppl_metro.demand_electricity
    rail_ppl.change_CO2e_t = (
        rail_ppl.CO2e_combustion_based - t18.rail_ppl.CO2e_combustion_based
    )
    rail_ppl.change_CO2e_pct = div(
        rail_ppl.change_CO2e_t, t18.rail_ppl.CO2e_combustion_based
    )
    rail_gds.CO2e_total_2021_estimated = t18.rail_gds.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    rail_gds.cost_climate_saved = (
        (rail_gds.CO2e_total_2021_estimated - rail_gds.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    rail_ppl_distance.change_km = (
        rail_ppl_distance.transport_capacity_pkm
        - t18.rail_ppl_distance.transport_capacity_pkm
    )
    rail_gds.ratio_wage_to_emplo = ass("Ass_T_D_rail_wage_driver")
    rail_ppl_metro_action_infra.invest_pa_com = (
        rail_ppl_metro_action_infra.invest_com / entries.m_duration_target
    )
    rail_ppl_distance.cost_wage = (
        rail_ppl_distance.ratio_wage_to_emplo * rail_ppl_distance.demand_emplo_new
    )
    rail_ppl.invest_com = rail_ppl_metro_action_infra.invest_com
    rail_ppl_metro_action_infra.cost_wage = (
        rail_ppl_metro_action_infra.invest_pa * rail_ppl_metro_action_infra.pct_of_wage
    )
    rail_gds.demand_emplo = rail_gds.mileage / fact("Fact_T_D_rail_ratio_mlg_to_driver")
    rail_ppl_distance.invest_per_x = fact("Fact_T_D_rail_ppl_vehicle_invest")
    rail_gds.emplo_existing = t18.rail_gds.mileage / fact(
        "Fact_T_D_rail_ratio_mlg_to_driver"
    )
    rail_gds.change_km = (
        rail_gds.transport_capacity_tkm - t18.rail_gds.transport_capacity_tkm
    )
    rail.change_energy_pct = div(rail.change_energy_MWh, t18.rail.energy)
    rail_ppl_metro.change_energy_MWh = rail_ppl_metro.energy - t18.rail_ppl_metro.energy
    rail_ppl.mileage = rail_ppl_distance.mileage + rail_ppl_metro.mileage
    rail.CO2e_total = rail.CO2e_combustion_based
    ship_inter.CO2e_combustion_based = ship_inter.demand_ediesel * ass(
        "Ass_T_S_diesel_EmFa_tank_wheel_2050"
    )
    rail_ppl_metro.CO2e_total = rail_ppl_metro.CO2e_combustion_based
    rail_ppl.change_energy_MWh = (
        rail_ppl_distance.change_energy_MWh + rail_ppl_metro.change_energy_MWh
    )
    rail_ppl_distance.change_energy_pct = div(
        rail_ppl_distance.change_energy_MWh, t18.rail_ppl_distance.energy
    )
    rail_ppl_distance.change_CO2e_t = (
        rail_ppl_distance.CO2e_combustion_based
        - t18.rail_ppl_distance.CO2e_combustion_based
    )
    rail_ppl_distance.change_CO2e_pct = div(
        rail_ppl_distance.change_CO2e_t, t18.rail_ppl_distance.CO2e_combustion_based
    )
    rail_ppl_distance.CO2e_total_2021_estimated = (
        t18.rail_ppl_distance.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    rail_ppl_distance.cost_climate_saved = (
        (
            rail_ppl_distance.CO2e_total_2021_estimated
            - rail_ppl_distance.CO2e_combustion_based
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    rail_ppl_metro.change_km = (
        rail_ppl_metro.transport_capacity_pkm
        - t18.rail_ppl_metro.transport_capacity_pkm
    )
    # rail_ppl_distance.actionInvestitionen in zusätzliche Eisenbahnen und Personal

    rail_ppl_metro_action_infra.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    rail_gds.demand_emplo_new = rail_gds.demand_emplo - rail_gds.emplo_existing
    rail_ppl_distance.invest = (
        rail_ppl_distance.base_unit * rail_ppl_distance.invest_per_x
        + rail_ppl_distance.cost_wage * entries.m_duration_target
    )
    rail_ppl_distance.invest_pa = rail_ppl_distance.invest / entries.m_duration_target
    rail_ppl_metro.invest_per_x = fact("Fact_T_D_rail_metro_vehicle_invest")
    rail_ppl_metro.ratio_wage_to_emplo = ass("Ass_T_D_bus_metro_wage_driver")
    rail_ppl_metro.demand_emplo = rail_ppl_metro.mileage / fact(
        "Fact_T_D_metro_ratio_mlg_to_driver"
    )
    rail_ppl_metro.emplo_existing = t18.rail_ppl_metro.mileage / fact(
        "Fact_T_D_metro_ratio_mlg_to_driver"
    )
    rail_ppl_metro.demand_emplo_new = (
        rail_ppl_metro.demand_emplo - rail_ppl_metro.emplo_existing
    )
    rail_ppl_metro.cost_wage = (
        rail_ppl_metro.ratio_wage_to_emplo * rail_ppl_metro.demand_emplo_new
    )
    rail_ppl_metro.invest = (
        rail_ppl_metro.base_unit * rail_ppl_metro.invest_per_x
        + rail_ppl_metro.cost_wage * entries.m_duration_target
    )
    rail_ppl.invest = (
        rail_ppl_distance.invest
        + rail_ppl_metro.invest
        + rail_ppl_metro_action_infra.invest
    )  # SUM(rail_ppl_distance.invest:rail_ppl_metro_action_infra.invest)

    rail_ppl_metro_action_infra.emplo_existing = 0  # nicht existent oder ausgelastet

    rail_ppl.emplo_existing = (
        rail_ppl_distance.emplo_existing
        + rail_ppl_metro.emplo_existing
        + rail_ppl_metro_action_infra.emplo_existing
    )  # SUM(rail_ppl_distance.emplo_existing:rail_ppl_metro_action_infra.emplo_existing)
    rail_ppl_metro_action_infra.demand_emplo = (
        rail_ppl_metro_action_infra.cost_wage
        / rail_ppl_metro_action_infra.ratio_wage_to_emplo
    )
    rail_gds.base_unit = rail_gds.change_km / fact(
        "Fact_T_D_rail_gds_ratio_mlg_to_vehicle"
    )
    rail_ppl_distance.pct_of_wage = div(
        rail_ppl_distance.cost_wage, rail_ppl_distance.invest_pa
    )
    t.demand_change = (
        air.demand_change
        + road.demand_change
        + rail.demand_change
        + ship.demand_change
        + other.demand_change
    )
    rail_ppl.energy = rail_ppl_distance.energy + rail_ppl_metro.energy
    t.demand_electricity = road.demand_electricity + rail.demand_electricity
    rail.transport_capacity_pkm = rail_ppl.transport_capacity_pkm
    rail_ppl.cost_climate_saved = (
        (rail_ppl.CO2e_total_2021_estimated - rail_ppl.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    rail_ppl.CO2e_total = rail_ppl_distance.CO2e_total + rail_ppl_metro.CO2e_total
    rail_ppl.change_energy_pct = div(rail_ppl.change_energy_MWh, t18.rail_ppl.energy)
    rail_ppl_metro.change_energy_pct = div(
        rail_ppl_metro.change_energy_MWh, t18.rail_ppl_metro.energy
    )
    rail_ppl_metro.change_CO2e_t = (
        rail_ppl_metro.CO2e_combustion_based - t18.rail_ppl_metro.CO2e_combustion_based
    )
    rail_ppl_metro.change_CO2e_pct = (
        0  # div(rail_ppl_metro.change_CO2e_t, t18.rail_ppl_metro.CO2e_cb)
    )
    rail_ppl_metro.CO2e_total_2021_estimated = (
        t18.rail_ppl_metro.CO2e_combustion_based
        * fact("Fact_M_CO2e_wo_lulucf_2021_vs_2018")
    )
    rail_ppl_metro.cost_climate_saved = (
        (
            rail_ppl_metro.CO2e_total_2021_estimated
            - rail_ppl_metro.CO2e_combustion_based
        )
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    rail_ppl.change_km = rail_ppl_distance.change_km + rail_ppl_metro.change_km
    # rail_ppl_metro.actionInvestitionen in zusätzliche SSU - Bahnen und Personal
    rail_ppl_metro_action_infra.demand_emplo_new = (
        rail_ppl_metro_action_infra.demand_emplo
    )
    rail_ppl_metro.invest_pa = rail_ppl_metro.invest / entries.m_duration_target
    rail_ppl_metro.pct_of_wage = div(rail_ppl_metro.cost_wage, rail_ppl_metro.invest_pa)
    # rail_ppl_metro_action_infra.actionInvesitionen in Verkehrsnetze für SSU Bahnen
    rail_ppl.invest_pa = (
        rail_ppl_distance.invest_pa
        + rail_ppl_metro.invest_pa
        + rail_ppl_metro_action_infra.invest_pa
    )  # SUM(rail_ppl_distance.invest_pa:rail_ppl_metro_action_infra.invest_pa)
    rail_ppl.invest_pa_com = rail_ppl_metro_action_infra.invest_pa_com
    g.invest_pa = g_planning.invest_pa
    rail.invest_com = (
        rail_action_invest_infra.invest_com
        + rail_action_invest_station.invest_com
        + rail_ppl.invest_com
    )  # SUM(rail_action_invest_infra.invest_com:rail_ppl.invest_com,DE260)
    rail_ppl.cost_wage = (
        rail_ppl_distance.cost_wage
        + rail_ppl_metro.cost_wage
        + rail_ppl_metro_action_infra.cost_wage
    )  # SUM(rail_ppl_distance.cost_wage:rail_ppl_metro_action_infra.cost_wage)
    rail_gds.cost_wage = rail_gds.ratio_wage_to_emplo * rail_gds.demand_emplo_new
    rail_ppl.demand_emplo_new = (
        rail_ppl_distance.demand_emplo_new
        + rail_ppl_metro.demand_emplo_new
        + rail_ppl_metro_action_infra.demand_emplo_new
    )  # SUM(rail_ppl_distance.demand_emplo_new:rail_ppl_metro_action_infra.demand_emplo_new)
    rail_ppl.demand_emplo = (
        rail_ppl_distance.demand_emplo
        + rail_ppl_metro.demand_emplo
        + rail_ppl_metro_action_infra.demand_emplo
    )
    rail.demand_emplo_new = (
        rail_action_invest_infra.demand_emplo_new
        + rail_action_invest_station.demand_emplo_new
        + rail_ppl.demand_emplo_new
        + rail_gds.demand_emplo_new
    )
    rail.invest_pa_com = (
        rail_action_invest_infra.invest_pa_com
        + rail_action_invest_station.invest_pa_com
        + rail_ppl.invest_pa_com
    )  # SUM(rail_action_invest_infra.invest_pa_com:rail_ppl.invest_pa_com,DB260)

    ship_dmstc_action_infra.demand_ediesel = 0
    ship.demand_ediesel = (
        ship_dmstc.demand_ediesel
        + ship_dmstc_action_infra.demand_ediesel
        + ship_inter.demand_ediesel
    )  # SUM(ship_dmstc.demand_ediesel:ship_inter.demand_ediesel)
    t.demand_ediesel = road.demand_ediesel + ship.demand_ediesel

    t.energy = (
        t.demand_electricity
        + t.demand_epetrol
        + t.demand_ediesel
        + t.demand_ejetfuel
        + t.demand_hydrogen
        + t.demand_change
    )  # SUM(t.demand_electricity:t.demand_change)
    rail_gds.energy = (
        rail_gds.demand_electricity
    )  # SUM(rail_gds.demand_electricity:BJ260)
    rail.mileage = rail_ppl.mileage + rail_gds.mileage
    rail.transport_capacity_tkm = rail_gds.transport_capacity_tkm
    ship.CO2e_combustion_based = (
        ship_dmstc.CO2e_combustion_based + ship_inter.CO2e_combustion_based
    )
    rail_gds.CO2e_total = rail_gds.CO2e_combustion_based
    rail_gds.change_energy_MWh = rail_gds.energy - t18.rail_gds.energy
    rail_gds.change_energy_pct = div(rail_gds.change_energy_MWh, t18.rail_gds.energy)
    rail_gds.change_CO2e_t = (
        rail_gds.CO2e_combustion_based - t18.rail_gds.CO2e_combustion_based
    )
    rail_gds.change_CO2e_pct = div(
        rail_gds.change_CO2e_t, t18.rail_gds.CO2e_combustion_based
    )
    rail.CO2e_total_2021_estimated = (
        rail_ppl.CO2e_total_2021_estimated + rail_gds.CO2e_total_2021_estimated
    )
    rail.cost_climate_saved = rail_ppl.cost_climate_saved + rail_gds.cost_climate_saved
    rail.base_unit = rail_ppl.base_unit + rail_gds.base_unit
    #  rail_gds.actionInvestitionen in zusätzliche Eisenbahnen und Personal

    rail_gds.invest_per_x = fact("Fact_T_D_rail_gds_vehicle_invest")
    rail_gds.invest = (
        rail_gds.base_unit * rail_gds.invest_per_x
        + rail_gds.cost_wage * entries.m_duration_target
    )
    rail_gds.invest_pa = rail_gds.invest / entries.m_duration_target
    rail_gds.pct_of_wage = div(rail_gds.cost_wage, rail_gds.invest_pa)
    rail.invest_pa = (
        rail_action_invest_infra.invest_pa
        + rail_action_invest_station.invest_pa
        + rail_ppl.invest_pa
        + rail_gds.invest_pa
    )
    rail.demand_emplo = (
        rail_action_invest_infra.demand_emplo
        + rail_action_invest_station.demand_emplo
        + rail_ppl.demand_emplo
        + rail_gds.demand_emplo
    )
    rail.cost_wage = (
        rail_action_invest_infra.cost_wage
        + rail_action_invest_station.cost_wage
        + rail_ppl.cost_wage
        + rail_gds.cost_wage
    )  # SUM(rail_action_invest_infra.cost_wage:rail_ppl.cost_wage,rail_gds.cost_wage)
    ship_dmstc.demand_emplo_new = ship_dmstc.demand_emplo - ship_dmstc.emplo_existing
    # rail_action_invest_infra.actionInvestitionen Schienennetzausbau

    rail.invest = (
        rail_action_invest_infra.invest
        + rail_action_invest_station.invest
        + rail_ppl.invest
        + rail_gds.invest
    )  # SUM(rail_action_invest_infra.invest:rail_ppl.invest,rail_gds.invest)
    t.CO2e_combustion_based = (
        air.CO2e_combustion_based
        + road.CO2e_combustion_based
        + rail.CO2e_combustion_based
        + ship.CO2e_combustion_based
    )
    t.change_energy_MWh = t.energy - t18.t.energy
    ship.energy = ship.demand_ediesel + ship.demand_change
    ship.transport_capacity_tkm = ship_dmstc.transport_capacity_tkm
    t.CO2e_total = t.CO2e_combustion_based
    ship.CO2e_total = ship.CO2e_combustion_based
    ship.change_energy_MWh = ship.energy - t18.ship.energy
    ship.change_energy_pct = div(ship.change_energy_MWh, t18.ship.energy)
    ship.change_CO2e_t = ship.CO2e_combustion_based - t18.ship.CO2e_combustion_based
    ship.change_CO2e_pct = div(ship.change_CO2e_t, t18.ship.CO2e_combustion_based)
    other_foot.CO2e_total_2021_estimated = t18.other_foot.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    other_foot.cost_climate_saved = (
        (other_foot.CO2e_total_2021_estimated)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    other_foot.invest_pa = 0
    other_foot.invest = 0
    other_foot.invest_com = other_foot.invest

    ship_dmstc_action_infra.invest_pa = (
        ship_dmstc_action_infra.invest / entries.m_duration_target
    )
    ship_dmstc.change_km = (
        ship_dmstc.transport_capacity_tkm - t18.ship_dmstc.transport_capacity_tkm
    )

    ship_dmstc.energy = ship_dmstc.demand_ediesel
    t.transport_capacity_tkm = (
        air.transport_capacity_tkm
        + road.transport_capacity_tkm
        + rail.transport_capacity_tkm
        + ship.transport_capacity_tkm
    )
    t.change_CO2e_t = t.CO2e_combustion_based - t18.t.CO2e_combustion_based
    ship_dmstc.CO2e_total = ship_dmstc.CO2e_combustion_based
    ship_dmstc.change_energy_MWh = ship_dmstc.energy - t18.ship_dmstc.energy
    ship_dmstc.change_energy_pct = div(
        ship_dmstc.change_energy_MWh, t18.ship_dmstc.energy
    )
    ship_dmstc.change_CO2e_t = (
        ship_dmstc.CO2e_combustion_based - t18.ship_dmstc.CO2e_combustion_based
    )
    ship_dmstc.change_CO2e_pct = div(
        ship_dmstc.change_CO2e_t, t18.ship_dmstc.CO2e_combustion_based
    )
    ship_inter.CO2e_total_2021_estimated = t18.ship_inter.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    ship_inter.cost_climate_saved = (
        (ship_inter.CO2e_total_2021_estimated - ship_inter.CO2e_combustion_based)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    ship_dmstc.base_unit = ship_dmstc.change_km / fact(
        "Fact_T_D_Shp_dmstc_nat_ratio_mlg_to_vehicle"
    )
    # ship_dmstc.actionKauf Schiffe

    ship_dmstc.invest_per_x = fact("Fact_T_D_Shp_dmstc_vehicle_invest")
    ship_dmstc.cost_wage = ship_dmstc.ratio_wage_to_emplo * ship_dmstc.demand_emplo_new
    ship_dmstc.invest = (
        ship_dmstc.base_unit * ship_dmstc.invest_per_x
        + ship_dmstc.cost_wage * entries.m_duration_target
    )
    ship_dmstc_action_infra.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    ship_dmstc.invest_pa = ship_dmstc.invest / entries.m_duration_target
    ship_dmstc_action_infra.cost_wage = (
        ship_dmstc_action_infra.invest_pa * ship_dmstc_action_infra.pct_of_wage
    )
    ship.emplo_existing = ship_dmstc.emplo_existing
    ship_dmstc_action_infra.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    ship.base_unit = ship_dmstc.base_unit
    ship_dmstc.pct_of_wage = div(ship_dmstc.cost_wage, ship_dmstc.invest_pa)
    # ship_dmstc_action_infra.actionAus -  und Neubau der Bundeswasserstraßen

    ship.invest_pa = (
        ship_dmstc_action_infra.invest_pa
    )  # SUM(ship_dmstc_action_infra.invest_pa:DA264)
    ship_dmstc_action_infra.invest_pa_com = (
        ship_dmstc_action_infra.invest_com / entries.m_duration_target
    )
    ship_dmstc_action_infra.demand_emplo = div(
        ship_dmstc_action_infra.cost_wage, ship_dmstc_action_infra.ratio_wage_to_emplo
    )
    ship.invest_pa_com = (
        ship_dmstc_action_infra.invest_pa_com
    )  # SUM(ship_dmstc_action_infra.invest_pa_com:DB264)
    ship_dmstc_action_infra.demand_emplo_new = ship_dmstc_action_infra.demand_emplo
    ship.cost_wage = ship_dmstc.cost_wage + ship_dmstc_action_infra.cost_wage
    ship.demand_emplo_new = (
        ship_dmstc.demand_emplo_new + ship_dmstc_action_infra.demand_emplo_new
    )
    ship.demand_emplo = ship_dmstc.demand_emplo + ship_dmstc_action_infra.demand_emplo
    # ship_dmstc_action_infra.emplo_existingnicht existent oder ausgelastet

    ship_inter.energy = ship_inter.demand_ediesel  # SUM(AW264:BJ264)
    t.change_CO2e_pct = div(t.change_CO2e_t, t18.t.CO2e_combustion_based)
    ship_inter.CO2e_total = ship_inter.CO2e_combustion_based
    ship_inter.change_energy_MWh = ship_inter.energy - t18.ship_inter.energy
    ship_inter.change_energy_pct = div(
        ship_inter.change_energy_MWh, t18.ship_inter.energy
    )
    ship_inter.change_CO2e_t = (
        ship_inter.CO2e_combustion_based - t18.ship_inter.CO2e_combustion_based
    )
    ship_inter.change_CO2e_pct = div(
        ship_inter.change_CO2e_t, t18.ship_inter.CO2e_combustion_based
    )
    ship_dmstc_action_infra.CO2e_total_2021_estimated = 0
    ship.CO2e_total_2021_estimated = (
        ship_dmstc.CO2e_total_2021_estimated
        + ship_dmstc_action_infra.CO2e_total_2021_estimated
        + ship_inter.CO2e_total_2021_estimated
    )  # SUM(ship_dmstc.CO2e_total_2021_estimated:ship_inter.CO2e_total_2021_estimated)

    ship_dmstc_action_infra.cost_climate_saved = 0
    ship.cost_climate_saved = (
        ship_dmstc.cost_climate_saved
        + ship_dmstc_action_infra.cost_climate_saved
        + ship_inter.cost_climate_saved
    )  # SUM(ship_dmstc.cost_climate_saved:ship_inter.cost_climate_saved)

    # TODO: hier evtl. nochmal bessere Daten rausfinden
    ship_inter.transport_capacity_tkm = t18.ship_inter.transport_capacity_tkm * div(
        ship_inter.energy, t18.ship_inter.energy
    )

    ship_inter.change_km = (
        ship_inter.transport_capacity_tkm - t18.ship_inter.transport_capacity_tkm
    )
    # ship_inter.actionReduktion der Transportleistung

    t.change_energy_pct = div(t.change_energy_MWh, t18.t.energy)
    other_foot.transport_capacity_pkm = t.transport_capacity_pkm * (
        ass("Ass_T_D_trnsprt_ppl_city_foot_frac_2050")
        if entries.t_rt3 == "city"
        else ass("Ass_T_D_trnsprt_ppl_smcty_foot_frac_2050")
        if entries.t_rt3 == "smcty"
        else ass("Ass_T_D_trnsprt_ppl_rural_foot_frac_2050")
        if entries.t_rt3 == "rural"
        else ass("Ass_T_D_trnsprt_ppl_nat_foot_frac_2050")
    )
    other.CO2e_total = 0  # CJ265 + CM265(

    other_cycl.CO2e_total_2021_estimated = t18.other_cycl.CO2e_combustion_based * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    other_cycl.cost_climate_saved = (
        (other_cycl.CO2e_total_2021_estimated)
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    other_foot.change_km = (
        other_foot.transport_capacity_pkm - t18.other_foot.transport_capacity_pkm
    )
    other_foot.invest_pa_com = other_foot.invest_pa
    other_cycl_action_infra.invest_per_x = ass("Ass_T_C_cost_per_trnsprt_ppl_cycle")

    other_cycl.invest_com = 0
    other_cycl_action_infra.invest = (
        other_cycl.transport_capacity_pkm * other_cycl_action_infra.invest_per_x
    )
    other_cycl_action_infra.invest_com = other_cycl_action_infra.invest * ass(
        "Ass_T_C_ratio_public_sector_100"
    )
    # other_foot.actionSchaffung fußgängerfreundlicher Städte und Gemeinden
    other_foot_action_infra.invest_per_x = ass("Ass_T_D_invest_pedestrians")
    other_foot_action_infra.invest_pa = (
        other_foot_action_infra.invest_per_x * entries.m_population_com_203X
    )
    other_foot_action_infra.invest = (
        other_foot_action_infra.invest_pa * entries.m_duration_target
    )
    other_foot_action_infra.invest_com = other_foot_action_infra.invest
    other.invest_com = (
        other_foot.invest_com
        + other_cycl.invest_com
        + other_foot_action_infra.invest_com
        + other_cycl_action_infra.invest_com
    )  # SUM(other_foot.invest_com:DE268)
    other_cycl.invest_pa = other_cycl.invest / entries.m_duration_target

    g_planning.demand_emplo_new = g_planning.demand_emplo

    other_foot.CO2e_total = 0

    other.CO2e_total_2021_estimated = (
        other_foot.CO2e_total_2021_estimated + other_cycl.CO2e_total_2021_estimated
    )
    other.cost_climate_saved = (
        other_foot.cost_climate_saved + other_cycl.cost_climate_saved
    )  # SUM(other_foot.cost_climate_saved:other_cycl.cost_climate_saved)
    other_cycl.change_km = (
        other_cycl.transport_capacity_pkm - t18.other_cycl.transport_capacity_pkm
    )

    other.invest = (
        other_foot.invest
        + other_cycl.invest
        + other_foot_action_infra.invest
        + other_cycl_action_infra.invest
    )  # SUM(other_foot.invest:other_cycl_action_infra.invest)

    other_cycl.invest_pa_com = other_cycl.invest_com / entries.m_duration_target
    other_foot_action_infra.invest_pa_com = other_foot_action_infra.invest_pa
    other_cycl_action_infra.invest_pa_com = (
        other_cycl_action_infra.invest_com / entries.m_duration_target
    )
    other.invest_pa_com = (
        other_foot.invest_pa_com
        + other_cycl.invest_pa_com
        + other_foot_action_infra.invest_pa_com
        + other_cycl_action_infra.invest_pa_com
    )  # SUM(other_foot.invest_pa_com:DB268)
    g.invest = g_planning.invest
    t.invest_com = (
        g.invest_com
        + road.invest_com
        + rail.invest_com
        + ship.invest_com
        + other.invest_com
        + air.invest_com
    )
    # other_foot.emplo_existingnicht existent oder ausgelastet
    other_foot_action_infra.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    other_foot_action_infra.cost_wage = (
        other_foot_action_infra.invest_pa * other_foot_action_infra.pct_of_wage
    )
    other_foot_action_infra.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    other_foot_action_infra.demand_emplo = div(
        other_foot_action_infra.cost_wage, other_foot_action_infra.ratio_wage_to_emplo
    )
    other_foot_action_infra.demand_emplo_new = other_foot_action_infra.demand_emplo
    other_cycl_action_infra.ratio_wage_to_emplo = fact(
        "Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018"
    )
    other_cycl_action_infra.pct_of_wage = fact(
        "Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018"
    )
    other_cycl_action_infra.invest_pa = (
        other_cycl_action_infra.invest / entries.m_duration_target
    )
    other_cycl_action_infra.cost_wage = (
        other_cycl_action_infra.invest_pa * other_cycl_action_infra.pct_of_wage
    )
    other_cycl_action_infra.demand_emplo = div(
        other_cycl_action_infra.cost_wage, other_cycl_action_infra.ratio_wage_to_emplo
    )
    other_cycl_action_infra.demand_emplo_new = other_cycl_action_infra.demand_emplo
    other.demand_emplo_new = (
        other_foot_action_infra.demand_emplo_new
        + other_cycl_action_infra.demand_emplo_new
    )
    t.invest_pa_com = (
        g.invest_pa_com
        + road.invest_pa_com
        + rail.invest_pa_com
        + ship.invest_pa_com
        + other.invest_pa_com
        + air.invest_pa_com
    )
    other.transport_capacity_pkm = (
        other_foot.transport_capacity_pkm + other_cycl.transport_capacity_pkm
    )
    other_cycl.CO2e_total = 0

    t.CO2e_total_2021_estimated = (
        air.CO2e_total_2021_estimated
        + road.CO2e_total_2021_estimated
        + rail.CO2e_total_2021_estimated
        + ship.CO2e_total_2021_estimated
        + other.CO2e_total_2021_estimated
    )
    t.cost_climate_saved = (
        air.cost_climate_saved
        + road.cost_climate_saved
        + rail.cost_climate_saved
        + ship.cost_climate_saved
        + other.cost_climate_saved
    )
    other.change_km = other_foot.change_km + other_cycl.change_km
    # other_cycl.actionAufbau Radinfrastruktur

    g.demand_emplo_new = g_planning.demand_emplo_new

    t.invest = (
        road.invest + rail.invest + ship.invest + other.invest + air.invest + g.invest
    )

    other.cost_wage = (
        other_foot_action_infra.cost_wage + other_cycl_action_infra.cost_wage
    )
    t.cost_wage = (
        g.cost_wage + road.cost_wage + rail.cost_wage + ship.cost_wage + other.cost_wage
    )

    other_cycl_action_infra.invest_pa = (
        other_cycl_action_infra.invest / entries.m_duration_target
    )

    other_cycl_action_infra.demand_emplo = div(
        other_cycl_action_infra.cost_wage, other_cycl_action_infra.ratio_wage_to_emplo
    )
    other.demand_emplo = (
        other_foot_action_infra.demand_emplo + other_cycl_action_infra.demand_emplo
    )
    t.demand_emplo = (
        g.demand_emplo
        + air.demand_emplo
        + road.demand_emplo
        + rail.demand_emplo
        + ship.demand_emplo
        + other.demand_emplo
    )
    # other_cycl.emplo_existingnicht existent oder ausgelastet

    t.demand_emplo_new = (
        g.demand_emplo_new
        + air.demand_emplo_new
        + road.demand_emplo_new
        + rail.demand_emplo_new
        + ship.demand_emplo_new
        + other.demand_emplo_new
    )
    # g_planning.actionNeue Stellen im Bereich "Verkehrsplanung"
    # other_cycl_action_infra.actionInvestitionen in (E - )Lastenräder

    other.invest_pa = (
        other_foot.invest_pa
        + other_cycl.invest_pa
        + other_foot_action_infra.invest_pa
        + other_cycl_action_infra.invest_pa
    )
    other.base_unit = other_cycl.base_unit
    t.invest_pa = (
        road.invest_pa
        + rail.invest_pa
        + ship.invest_pa
        + other.invest_pa
        + air.invest_pa
        + g.invest_pa
    )
    s_petrol.energy = t.demand_epetrol
    s_jetfuel.energy = t.demand_ejetfuel
    s_diesel.energy = t.demand_ediesel
    s_elec.energy = t.demand_electricity
    s_hydrogen.energy = t.demand_hydrogen
    s_emethan.energy = 0

    s.energy = (
        s_petrol.energy
        + s_jetfuel.energy
        + s_diesel.energy
        + s_elec.energy
        + s_hydrogen.energy
        + s_emethan.energy
    )

    g_planning.demand_emplo_com = g_planning.demand_emplo_new
    g.demand_emplo_com = g.demand_emplo_new
    t.demand_emplo_com = g.demand_emplo_com

    return t30
