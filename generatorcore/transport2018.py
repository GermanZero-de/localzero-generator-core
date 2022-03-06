# # Laden der Datentabellen und deren Suchfunktionen

from dataclasses import dataclass, field, asdict, fields
from .inputs import Inputs
import typing

MILLION = 1000000

T = typing.TypeVar("T")


def element_wise_plus(a: T, b: T) -> T:
    return type(a)(*(getattr(a, f.name) + getattr(b, f.name) for f in fields(a)))


def co2e_from_demands(
    inputs: Inputs,
    *,
    demand_biodiesel: float = 0,
    demand_bioethanol: float = 0,
    demand_biogas: float = 0,
    demand_diesel: float = 0,
    demand_electricity: float = 0,
    demand_fueloil: float = 0,
    demand_gas: float = 0,
    demand_jetfuel: float = 0,
    demand_lpg: float = 0,
    demand_petrol: float = 0,
    demand_jetpetrol: float = 0,
) -> float:
    return (
        demand_biodiesel * inputs.ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
        + demand_bioethanol * inputs.ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
        + demand_biogas * inputs.ass("Ass_T_S_biogas_EmFa_tank_wheel")
        + demand_diesel * inputs.fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
        + demand_electricity * inputs.fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        + demand_fueloil * inputs.fact("Fact_T_S_fueloil_EmFa_tank_wheel_2018")
        + demand_gas * inputs.fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        + demand_jetfuel * inputs.fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
        + demand_lpg * inputs.fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        + demand_petrol * inputs.fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
        + demand_jetpetrol * inputs.fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")
    )


@dataclass
class Air:
    # Used by air_dmstc, air, air_inter
    CO2e_cb: float
    CO2e_total: float
    demand_jetfuel: float
    demand_petrol: float
    energy: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    def __add__(self: "Air", other: "Air") -> "Air":
        return element_wise_plus(self, other)

    @classmethod
    def calc_domestic(cls, inputs: Inputs) -> "Air":
        demand_petrol = (
            inputs.fact("Fact_T_S_Air_petrol_fec_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        demand_jetfuel = (
            inputs.fact("Fact_T_S_Air_nat_EB_dmstc_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        transport_capacity_pkm = (
            inputs.fact("Fact_T_D_Air_dmstc_nat_trnsprt_ppl_2019")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * inputs.fact("Fact_T_D_Air_dmstc_nat_ratio_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        CO2e_cb = co2e_from_demands(
            inputs, demand_jetfuel=demand_jetfuel, demand_jetpetrol=demand_petrol
        )
        CO2e_total = CO2e_cb

        energy = demand_jetfuel + demand_petrol
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            demand_jetfuel=demand_jetfuel,
            demand_petrol=demand_petrol,
            energy=energy,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=transport_capacity_tkm,
        )

    @classmethod
    def calc_international(
        cls, inputs: Inputs, air_dmstc_demand_petrol: float
    ) -> "Air":
        transport_capacity_pkm = (
            inputs.fact("Fact_T_D_Air_nat_trnsprt_ppl_2019")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Air_dmstc_nat_trnsprt_gds_2019")
            * inputs.fact("Fact_T_D_Air_inter_nat_ratio_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        demand_jetfuel = (
            inputs.fact("Fact_T_S_Air_nat_EB_inter_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )

        CO2e_cb = co2e_from_demands(
            inputs, demand_petrol=air_dmstc_demand_petrol, demand_jetfuel=demand_jetfuel
        )
        CO2e_total = CO2e_cb
        energy = demand_jetfuel
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=transport_capacity_tkm,
            demand_jetfuel=demand_jetfuel,
            demand_petrol=0,
            energy=energy,
        )


@dataclass
class Road:
    """Emissions caused by transport on the Road (car, bus, lorry, ...) of both goods and people."""

    CO2e_cb: float
    CO2e_total: float
    demand_biodiesel: float
    demand_bioethanol: float
    demand_biogas: float
    demand_diesel: float
    demand_electricity: float
    demand_gas: float
    demand_lpg: float
    demand_petrol: float
    energy: float
    mileage: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    def __add__(self: "Road", other: "Road") -> "Road":
        return element_wise_plus(self, other)

    @classmethod
    def calc_road(
        cls,
        inputs: Inputs,
        *,
        mileage: float,
        transport_capacity_pkm_factor: float,
        transport_capacity_tkm_factor: float,
        biodiesel: float,
        bioethanol: float,
        biogas: float,
        diesel: float,
        electricity: float,
        gas: float,
        lpg: float,
        petrol: float,
    ) -> "Road":
        demand_biodiesel = mileage * biodiesel
        demand_bioethanol = mileage * bioethanol
        demand_biogas = mileage * biogas
        demand_diesel = mileage * diesel
        demand_electricity = mileage * electricity
        demand_gas = mileage * gas
        demand_lpg = mileage * lpg
        demand_petrol = mileage * petrol
        CO2e_cb = co2e_from_demands(
            inputs,
            demand_petrol=demand_petrol,
            demand_diesel=demand_diesel,
            demand_lpg=demand_lpg,
            demand_gas=demand_gas,
            demand_biogas=demand_biogas,
            demand_bioethanol=demand_bioethanol,
            demand_biodiesel=demand_biodiesel,
            demand_electricity=demand_electricity,
        )
        energy = (
            demand_petrol
            + demand_diesel
            + demand_lpg
            + demand_gas
            + demand_biogas
            + demand_bioethanol
            + demand_biodiesel
            + demand_electricity
        )
        CO2e_total = CO2e_cb
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            demand_biodiesel=demand_biodiesel,
            demand_bioethanol=demand_bioethanol,
            demand_biogas=demand_biogas,
            demand_diesel=demand_diesel,
            demand_electricity=demand_electricity,
            demand_gas=demand_gas,
            demand_lpg=demand_lpg,
            demand_petrol=demand_petrol,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=mileage * transport_capacity_pkm_factor,
            transport_capacity_tkm=mileage * transport_capacity_tkm_factor,
        )

    @classmethod
    def calc_car(
        cls, inputs: Inputs, subsection: typing.Literal["it_at", "ab"]
    ) -> "Road":
        def fact(n: str) -> float:
            return inputs.fact(n)

        return cls.calc_road(
            inputs,
            mileage=getattr(inputs.entries, "t_mil_car_" + subsection) * MILLION,
            transport_capacity_pkm_factor=fact(f"Fact_T_D_lf_ppl_Car_2018"),
            transport_capacity_tkm_factor=0,
            biodiesel=(
                fact(f"Fact_T_S_Car_frac_diesel_mlg_2018")
                * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
                * fact(f"Fact_T_S_Car_SEC_diesel_{subsection}_2018")
            ),
            bioethanol=(
                fact(f"Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
                * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
                * fact(f"Fact_T_S_Car_SEC_petrol_{subsection}_2018")
            ),
            biogas=(
                fact(f"Fact_T_S_Car_frac_cng_mlg_2018")
                * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
                * fact(f"Fact_T_S_Car_SEC_petrol_it_at_2018")
            ),
            diesel=(
                fact(f"Fact_T_S_Car_frac_diesel_mlg_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
                * fact(f"Fact_T_S_Car_SEC_diesel_{subsection}_2018")
            ),
            electricity=(
                fact(f"Fact_T_S_Car_frac_bev_with_phev_mlg_2018")
                * fact(f"Fact_T_S_Car_SEC_elec_{subsection}_2018")
            ),
            gas=(
                fact(f"Fact_T_S_Car_frac_cng_mlg_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
                * fact(f"Fact_T_S_Car_SEC_petrol_it_at_2018")
            ),
            lpg=(
                fact(f"Fact_T_S_Car_frac_lpg_mlg_2018")
                * fact(f"Fact_T_S_Car_SEC_petrol_{subsection}_2018")
            ),
            petrol=(
                fact(f"Fact_T_S_Car_frac_petrol_with_phev_mlg_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
                * fact(f"Fact_T_S_Car_SEC_petrol_{subsection}_2018")
            ),
        )

    @classmethod
    def calc_bus(cls, inputs: Inputs) -> "Road":
        def fact(n: str) -> float:
            return inputs.fact(n)

        return cls.calc_road(
            inputs,
            mileage=(
                inputs.entries.t_bus_mega_km_dis
                * MILLION
                * inputs.entries.m_population_com_2018
                / inputs.entries.m_population_dis
            ),
            transport_capacity_pkm_factor=fact("Fact_T_D_lf_ppl_Bus_2018"),
            transport_capacity_tkm_factor=0,
            biodiesel=(
                fact("Fact_T_S_Bus_frac_diesel_stock_2018")
                * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
                * fact("Fact_T_S_Bus_SEC_diesel_2018")
            ),
            biogas=(
                fact("Fact_T_S_Bus_frac_cng_stock_2018")
                * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
                * fact("Fact_T_S_Bus_SEC_diesel_2018")
            ),
            diesel=(
                fact("Fact_T_S_Bus_frac_diesel_with_hybrid_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
                * fact("Fact_T_S_Bus_SEC_diesel_2018")
            ),
            electricity=(
                fact("Fact_T_S_Bus_frac_bev_stock_2018")
                * fact("Fact_T_S_Bus_SEC_elec_2018")
            ),
            gas=(
                fact("Fact_T_S_Bus_frac_cng_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
                * fact("Fact_T_S_Bus_SEC_diesel_2018")
            ),
            # Buses do not use the below
            bioethanol=0,
            lpg=0,
            petrol=0,
        )

    @classmethod
    def calc_goods_light_weight(
        cls, inputs: Inputs, section: typing.Literal["it_at", "ab"]
    ) -> "Road":
        def fact(n: str) -> float:
            return inputs.fact(n)

        return cls.calc_road(
            inputs,
            mileage=getattr(inputs.entries, "t_mil_ldt_" + section) * MILLION,
            transport_capacity_pkm_factor=0,
            transport_capacity_tkm_factor=fact("Fact_T_D_lf_gds_LDT_2018"),
            biodiesel=(
                fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
                * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
                * fact(f"Fact_T_S_LDT_SEC_diesel_{section}_2018")
            ),
            bioethanol=(
                fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
                * fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018")
                * fact(f"Fact_T_S_LDT_SEC_petrol_{section}_2018")
            ),
            diesel=(
                fact("Fact_T_S_LDT_frac_diesel_mlg_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
                * fact(f"Fact_T_S_LDT_SEC_diesel_{section}_2018")
            ),
            electricity=(
                fact("Fact_T_S_LDT_frac_bev_mlg_2018")
                * fact(f"Fact_T_S_LDT_SEC_elec_{section}_2018")
            ),
            lpg=(
                fact("Fact_T_S_LDT_frac_lpg_mlg_2018")
                * fact(f"Fact_T_S_LDT_SEC_petrol_{section}_2018")
            ),
            petrol=(
                fact("Fact_T_S_LDT_frac_petrol_mlg_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_benzin_bio_frac_2018"))
                * fact(f"Fact_T_S_LDT_SEC_petrol_{section}_2018")
            ),
            # Neither biogas nor gas are used by light goods transports
            biogas=0,
            gas=0,
        )

    @classmethod
    def calc_goods_mhd_it_at(cls, inputs: Inputs, road_bus_mileage: float):
        def fact(n: str) -> float:
            return inputs.fact(n)

        return cls.calc_road(
            inputs,
            mileage=inputs.entries.t_mil_mhd_it_at * MILLION - road_bus_mileage,
            transport_capacity_tkm_factor=fact("Fact_T_D_lf_gds_MHD_2018"),
            transport_capacity_pkm_factor=0,
            biogas=(
                fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
                * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
                * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
            ),
            biodiesel=(
                fact("Fact_T_S_MHD_frac_diesel_stock_2018")
                * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
                * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
            ),
            diesel=(
                fact("Fact_T_S_MHD_frac_diesel_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
                * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
            ),
            electricity=(
                fact("Fact_T_S_MHD_frac_bev_stock_2018")
                * fact("Fact_T_S_MHD_SEC_elec_it_at_2018")
            ),
            gas=(
                fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
                * fact("Fact_T_S_MHD_SEC_diesel_it_at_2018")
            ),
            bioethanol=0,
            lpg=0,
            petrol=0,
        )

    @classmethod
    def calc_mhd_ab(cls, inputs: Inputs):
        def fact(n: str) -> float:
            return inputs.fact(n)

        return cls.calc_road(
            inputs,
            mileage=inputs.entries.t_mil_mhd_ab * MILLION,
            transport_capacity_tkm_factor=fact("Fact_T_D_lf_gds_MHD_2018"),
            transport_capacity_pkm_factor=0,
            biodiesel=(
                fact("Fact_T_S_MHD_frac_diesel_stock_2018")
                * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
                * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
            ),
            biogas=(
                fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
                * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
                * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
            ),
            diesel=(
                fact("Fact_T_S_MHD_frac_diesel_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
                * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
            ),
            electricity=(
                fact("Fact_T_S_MHD_frac_bev_stock_2018")
                * fact("Fact_T_S_MHD_SEC_elec_ab_2018")
            ),
            gas=(
                fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
                * fact("Fact_T_S_MHD_SEC_diesel_ab_2018")
            ),
            bioethanol=0,
            lpg=0,
            petrol=0,
        )


@dataclass
class Rail:
    # Used by rail_gds, rail_ppl_metro, rail_ppl_distance, rail_ppl, rail
    CO2e_cb: float
    CO2e_total: float
    demand_biodiesel: float
    demand_diesel: float
    demand_electricity: float
    energy: float
    mileage: float
    transport_capacity_tkm: float
    transport_capacity_pkm: float

    def __add__(self: "Rail", other: "Rail") -> "Rail":
        return element_wise_plus(self, other)

    @classmethod
    def calc_people_distance(cls, inputs: Inputs) -> "Rail":
        demand_electricity = inputs.entries.t_ec_rail_ppl_elec
        demand_diesel = inputs.entries.t_ec_rail_ppl_diesel * (
            1 - inputs.fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )
        demand_biodiesel = inputs.entries.t_ec_rail_ppl_diesel * inputs.fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        transport_capacity_pkm = (demand_diesel + demand_biodiesel) / inputs.fact(
            "Fact_T_S_Rl_Train_ppl_long_diesel_SEC_2018"
        ) + demand_electricity / inputs.fact("Fact_T_S_Rl_Train_ppl_long_elec_SEC_2018")
        mileage = transport_capacity_pkm / inputs.fact(
            "Fact_T_D_rail_ppl_ratio_pkm_to_fzkm_2018"
        )
        energy = demand_diesel + demand_biodiesel + demand_electricity
        CO2e_cb = co2e_from_demands(
            inputs,
            demand_diesel=demand_diesel,
            demand_biodiesel=demand_biodiesel,
            demand_electricity=demand_electricity,
        )
        CO2e_total = CO2e_cb
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            demand_biodiesel=demand_biodiesel,
            demand_diesel=demand_diesel,
            demand_electricity=demand_electricity,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
        )

    @classmethod
    def calc_goods(cls, inputs: Inputs) -> "Rail":
        demand_electricity = inputs.entries.t_ec_rail_gds_elec
        demand_diesel = inputs.entries.t_ec_rail_gds_diesel * (
            1 - inputs.fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
        )
        demand_biodiesel = inputs.entries.t_ec_rail_gds_diesel * inputs.fact(
            "Fact_T_S_Rl_Rd_diesel_bio_frac_2018"
        )

        transport_capacity_tkm = (demand_diesel + demand_biodiesel) / inputs.fact(
            "Fact_T_S_Rl_Train_gds_diesel_SEC_2018"
        ) + demand_electricity / inputs.fact("Fact_T_S_Rl_Train_gds_elec_SEC_2018")

        CO2e_cb = co2e_from_demands(inputs, demand_diesel=demand_diesel)
        energy = demand_diesel + demand_biodiesel + demand_electricity
        mileage = transport_capacity_tkm / inputs.fact(
            "Fact_T_D_rail_gds_ratio_tkm_to_fzkm_2018"
        )
        CO2e_total = CO2e_cb
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            demand_biodiesel=demand_biodiesel,
            demand_diesel=demand_diesel,
            demand_electricity=demand_electricity,
            energy=energy,
            mileage=mileage,
            transport_capacity_tkm=transport_capacity_tkm,
            transport_capacity_pkm=0,
        )

    @classmethod
    def calc_rail_people_metro(cls, inputs: Inputs) -> "Rail":
        mileage = (
            inputs.entries.t_metro_mega_km_dis
            * MILLION
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_dis
        )
        demand_electricity = mileage * inputs.fact("Fact_T_S_Rl_Metro_SEC_fzkm_2018")
        energy = demand_electricity
        transport_capacity_pkm = mileage * inputs.fact("Fact_T_D_lf_Rl_Metro_2018")
        CO2e_cb = co2e_from_demands(inputs, demand_electricity=demand_electricity)
        CO2e_total = CO2e_cb
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            demand_electricity=demand_electricity,
            demand_biodiesel=0,
            demand_diesel=0,
            energy=energy,
            mileage=mileage,
            transport_capacity_pkm=transport_capacity_pkm,
            transport_capacity_tkm=0,
        )


@dataclass
class Ship:
    # Used by ship_dmstc, ship_inter, ship
    CO2e_cb: float
    CO2e_total: float
    demand_diesel: float
    demand_fueloil: float
    energy: float
    transport_capacity_tkm: float

    def __add__(self: "Ship", other: "Ship") -> "Ship":
        return element_wise_plus(self, other)

    @classmethod
    def calc_ship_domestic(cls, inputs: Inputs) -> "Ship":
        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Shp_dmstc_trnsprt_gds_2018")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        demand_diesel = (
            inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
            * inputs.fact("Fact_T_S_Shp_diesel_fec_2018")
        )
        energy = demand_diesel

        CO2e_cb = co2e_from_demands(inputs, demand_diesel=demand_diesel)
        CO2e_total = CO2e_cb
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            transport_capacity_tkm=transport_capacity_tkm,
            demand_diesel=demand_diesel,
            demand_fueloil=0,
            energy=energy,
        )

    @classmethod
    def calc_ship_international(cls, inputs: Inputs) -> "Ship":
        transport_capacity_tkm = (
            inputs.fact("Fact_T_D_Shp_sea_nat_mlg_2013")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
        )
        demand_fueloil = (
            inputs.entries.m_population_com_2018 / inputs.entries.m_population_nat
        ) * inputs.fact("Fact_T_D_Shp_sea_nat_EC_2018")

        energy = demand_fueloil
        CO2e_cb = co2e_from_demands(inputs, demand_fueloil=demand_fueloil)
        CO2e_total = CO2e_cb
        return cls(
            CO2e_cb=CO2e_cb,
            CO2e_total=CO2e_total,
            transport_capacity_tkm=transport_capacity_tkm,
            demand_fueloil=demand_fueloil,
            demand_diesel=0,
            energy=energy,
        )


@dataclass
class Other:
    # Used by other_foot, other_cycl
    CO2e_cb: float
    CO2e_total: float
    transport_capacity_pkm: float

    def __add__(self: "Other", other: "Other") -> "Other":
        return element_wise_plus(self, other)

    @classmethod
    def calc_foot(cls, inputs: Inputs) -> "Other":
        t_rt7 = inputs.entries.t_rt7
        if t_rt7 in ["71", "72", "73", "74", "75", "76", "77"]:
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_foot_rt" + t_rt7)
            )
        elif t_rt7 == "nd":
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_foot_nat")
            )
        else:
            assert False, f"Do not know how to handle entries.t_rt7 = {t_rt7}"
        return cls(
            CO2e_total=0, CO2e_cb=0, transport_capacity_pkm=transport_capacity_pkm
        )

    @classmethod
    def calc_cycle(cls, inputs: Inputs) -> "Other":
        t_rt7 = inputs.entries.t_rt7
        if t_rt7 in ["71", "72", "73", "74", "75", "76", "77"]:
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_cycl_rt" + t_rt7)
            )

        # This happens if we run Local Zero for a Landkreis a Bundesland or Germany.
        # We do not have a area_kind entry in this case and just use the mean mean modal split of germany.
        elif t_rt7 == "nd":
            transport_capacity_pkm = (
                inputs.entries.m_population_com_2018
                * 365
                * inputs.fact("Fact_T_D_modal_split_foot_nat")
            )
        else:
            assert False, f"Do not know how to handle entries.t_rt7 = {t_rt7}"
        return cls(
            CO2e_total=0, CO2e_cb=0, transport_capacity_pkm=transport_capacity_pkm
        )


@dataclass
class Transport:
    # Used by t
    CO2e_cb: float
    CO2e_total: float
    demand_biodiesel: float = 0
    demand_bioethanol: float = 0
    demand_biogas: float = 0
    demand_diesel: float = 0
    demand_electricity: float = 0
    demand_fueloil: float = 0
    demand_gas: float = 0
    demand_jetfuel: float = 0
    demand_lpg: float = 0
    demand_petrol: float = 0
    energy: float = 0
    mileage: float = 0  # We should delete this
    transport_capacity_pkm: float = 0
    transport_capacity_tkm: float = 0

    def __add__(self: "Transport", other: "Transport") -> "Transport":
        return element_wise_plus(self, other)

    @classmethod
    def lift_air(cls, a: Air) -> "Transport":
        return cls(
            CO2e_cb=a.CO2e_cb,
            CO2e_total=a.CO2e_total,
            demand_jetfuel=a.demand_jetfuel,
            demand_petrol=a.demand_petrol,
            energy=a.energy,
            transport_capacity_pkm=a.transport_capacity_pkm,
            transport_capacity_tkm=a.transport_capacity_tkm,
        )

    @classmethod
    def lift_ship(cls, s: Ship) -> "Transport":
        return cls(
            CO2e_cb=s.CO2e_cb,
            CO2e_total=s.CO2e_total,
            demand_diesel=s.demand_diesel,
            demand_fueloil=s.demand_fueloil,
            energy=s.energy,
            transport_capacity_tkm=s.transport_capacity_tkm,
        )

    @classmethod
    def lift_road(cls, r: Road) -> "Transport":
        return cls(
            CO2e_cb=r.CO2e_cb,
            CO2e_total=r.CO2e_total,
            demand_diesel=r.demand_diesel,
            demand_biodiesel=r.demand_biodiesel,
            demand_bioethanol=r.demand_bioethanol,
            demand_biogas=r.demand_biogas,
            demand_electricity=r.demand_electricity,
            demand_gas=r.demand_gas,
            demand_lpg=r.demand_lpg,
            demand_petrol=r.demand_petrol,
            energy=r.energy,
            mileage=r.mileage,
            transport_capacity_tkm=r.transport_capacity_tkm,
            transport_capacity_pkm=r.transport_capacity_pkm,
        )

    @classmethod
    def lift_rail(cls, r: Rail) -> "Transport":
        return cls(
            CO2e_cb=r.CO2e_cb,
            CO2e_total=r.CO2e_total,
            demand_biodiesel=r.demand_biodiesel,
            demand_diesel=r.demand_diesel,
            demand_electricity=r.demand_electricity,
            mileage=r.mileage,
            energy=r.energy,
            transport_capacity_pkm=r.transport_capacity_pkm,
            transport_capacity_tkm=r.transport_capacity_tkm,
        )

    @classmethod
    def lift_other(cls, o: Other) -> "Transport":
        return cls(
            CO2e_cb=o.CO2e_cb,
            CO2e_total=o.CO2e_total,
            transport_capacity_pkm=o.transport_capacity_pkm,
        )


@dataclass
class Vars20:
    # Used by s, s_petrol, s_jetfuel, s_diesel, s_fueloil, s_lpg, s_gas, s_biogas, s_bioethanol, s_biodiesel, s_elec
    energy: float = None  # type: ignore


@dataclass
class T18:
    t: Transport = None  # type: ignore
    air_inter: Air = None  # type: ignore
    air_dmstc: Air = None  # type: ignore
    road: Road = None  # type: ignore
    road_car: Road = None  # type: ignore
    road_car_it_ot: Road = None  # type: ignore
    road_car_ab: Road = None  # type: ignore
    road_bus: Road = None  # type: ignore
    road_gds: Road = None  # type: ignore
    road_gds_ldt: Road = None  # type: ignore
    road_gds_ldt_it_ot: Road = None  # type: ignore
    road_gds_ldt_ab: Road = None  # type: ignore
    road_gds_mhd: Road = None  # type: ignore
    road_ppl: Road = None  # type: ignore
    road_gds_mhd_it_ot: Road = None  # type: ignore
    road_gds_mhd_ab: Road = None  # type: ignore
    rail_ppl: Rail = None  # type: ignore
    rail_ppl_metro: Rail = None  # type: ignore
    rail_ppl_distance: Rail = None  # type: ignore
    rail_gds: Rail = None  # type: ignore
    ship_dmstc: Ship = None  # type: ignore
    ship_inter: Ship = None  # type: ignore
    other_foot: Other = None  # type: ignore
    other_cycl: Other = None  # type: ignore
    air: Air = None  # type: ignore
    rail: Rail = None  # type: ignore
    ship: Ship = None  # type: ignore
    other: Other = None  # type: ignore
    s: Vars20 = field(default_factory=Vars20)
    s_petrol: Vars20 = field(default_factory=Vars20)
    s_jetfuel: Vars20 = field(default_factory=Vars20)
    s_diesel: Vars20 = field(default_factory=Vars20)
    s_fueloil: Vars20 = field(default_factory=Vars20)
    s_lpg: Vars20 = field(default_factory=Vars20)
    s_gas: Vars20 = field(default_factory=Vars20)
    s_biogas: Vars20 = field(default_factory=Vars20)
    s_bioethanol: Vars20 = field(default_factory=Vars20)
    s_biodiesel: Vars20 = field(default_factory=Vars20)
    s_elec: Vars20 = field(default_factory=Vars20)

    def dict(self):
        return asdict(self)


def calc(inputs: Inputs) -> T18:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    entries = inputs.entries

    # abbreviations
    t18 = T18()
    s = t18.s
    s_petrol = t18.s_petrol
    s_jetfuel = t18.s_jetfuel
    s_diesel = t18.s_diesel
    s_fueloil = t18.s_fueloil
    s_lpg = t18.s_lpg
    s_gas = t18.s_gas
    s_biogas = t18.s_biogas
    s_bioethanol = t18.s_bioethanol
    s_biodiesel = t18.s_biodiesel
    s_elec = t18.s_elec

    # TODO: Fix the it at confusion

    # --- Air ---
    air_dmstc = Air.calc_domestic(inputs)
    air_inter = Air.calc_international(
        inputs, air_dmstc_demand_petrol=air_dmstc.demand_petrol
    )
    air = air_dmstc + air_inter
    # --- Road ---
    road_car_it_ot = Road.calc_car(inputs, "it_at")
    road_car_ab = Road.calc_car(inputs, "ab")
    road_car = road_car_it_ot + road_car_ab
    road_bus = Road.calc_bus(inputs)
    road_ppl = road_car + road_bus
    road_gds_mhd_it_ot = Road.calc_goods_mhd_it_at(
        inputs, road_bus_mileage=road_bus.mileage
    )
    road_gds_mhd_ab = Road.calc_mhd_ab(inputs)
    road_gds_mhd = road_gds_mhd_ab + road_gds_mhd_it_ot
    road_gds_ldt_it_ot = Road.calc_goods_light_weight(inputs, "it_at")
    road_gds_ldt_ab = Road.calc_goods_light_weight(inputs, "ab")
    road_gds_ldt = road_gds_ldt_it_ot + road_gds_ldt_ab
    road_gds = road_gds_ldt + road_gds_mhd
    road = road_gds + road_ppl
    # --- Rail ---
    rail_ppl_metro = Rail.calc_rail_people_metro(inputs)
    rail_ppl_distance = Rail.calc_people_distance(inputs)
    rail_ppl = rail_ppl_metro + rail_ppl_distance
    rail_gds = Rail.calc_goods(inputs)
    rail = rail_ppl + rail_gds
    # --- Ship ---
    ship_dmstc = Ship.calc_ship_domestic(inputs)
    ship_inter = Ship.calc_ship_international(inputs)
    ship = ship_dmstc + ship_inter
    # --- Other ---
    other_foot = Other.calc_foot(inputs)
    other_cycl = Other.calc_cycle(inputs)
    other = other_foot + other_cycl

    t = (
        Transport.lift_air(air)
        + Transport.lift_road(road)
        + Transport.lift_ship(ship)
        + Transport.lift_rail(rail)
        + Transport.lift_other(other)
    )

    # ----------------------------------------------------
    s_petrol.energy = t.demand_petrol
    s_jetfuel.energy = air_inter.demand_jetfuel + air_dmstc.demand_jetfuel
    s_diesel.energy = t.demand_diesel

    s_fueloil.energy = ship_inter.demand_fueloil

    s_gas.energy = t.demand_gas

    s_biogas.energy = t.demand_biogas

    s_bioethanol.energy = t.demand_bioethanol

    s_biodiesel.energy = t.demand_biodiesel

    s_elec.energy = t.demand_electricity

    # t.demand_petrol = air.demand_petrol + road.demand_petrol
    # t.CO2e_cb = air.CO2e_cb + road.CO2e_cb + rail.CO2e_cb + ship.CO2e_cb + other.CO2e_cb
    # t.energy = air.energy + road.energy + rail.energy + ship.energy
    # t.demand_electricity = road.demand_electricity + rail.demand_electricity
    # t.mileage = road.mileage + rail.mileage
    # t.transport_capacity_tkm = (
    #     air.transport_capacity_tkm
    #     + road.transport_capacity_tkm
    #     + rail.transport_capacity_tkm
    #     + ship.transport_capacity_tkm
    # )
    # t.CO2e_total = t.CO2e_cb
    # t.transport_capacity_pkm = (
    #     air.transport_capacity_pkm
    #     + road.transport_capacity_pkm
    #     + rail.transport_capacity_pkm
    #     + other.transport_capacity_pkm
    # )
    # t.demand_petrol = air.demand_petrol + road.demand_petrol
    # t.demand_jetfuel = air.demand_jetfuel
    # t.demand_diesel = road.demand_diesel + rail.demand_diesel + ship.demand_diesel
    # t.demand_fueloil = ship.demand_fueloil
    # t.demand_lpg = road.demand_lpg
    # t.demand_gas = road.demand_gas
    # t.demand_biogas = road.demand_biogas
    # t.demand_bioethanol = road.demand_bioethanol
    # t.demand_biodiesel = road.demand_biodiesel + rail.demand_biodiesel
    # t.demand_biogas = road.demand_biogas
    # t.demand_bioethanol = road.demand_bioethanol
    # t.demand_biodiesel = road.demand_biodiesel + rail.demand_biodiesel
    # t.energy = air.energy + road.energy + rail.energy + ship.energy
    # t.mileage = road.mileage + rail.mileage
    # t.transport_capacity_pkm = (
    #     air.transport_capacity_pkm
    #     + road.transport_capacity_pkm
    #     + rail.transport_capacity_pkm
    # )
    # t.transport_capacity_tkm = (
    #     air.transport_capacity_tkm
    #     + road.transport_capacity_tkm
    #     + rail.transport_capacity_tkm
    #     + ship.transport_capacity_tkm
    # )
    # t.demand_petrol = air.demand_petrol + road.demand_petrol
    # t.demand_jetfuel = air.demand_jetfuel
    # t.demand_diesel = road.demand_diesel + rail.demand_diesel + ship.demand_diesel
    # t.demand_fueloil = ship.demand_fueloil
    # t.demand_lpg = road.demand_lpg
    # t.demand_gas = road.demand_gas
    # t.demand_biogas = road.demand_biogas
    # t.demand_bioethanol = road.demand_bioethanol
    # t.demand_biodiesel = road.demand_biodiesel + rail.demand_biodiesel
    # t.demand_electricity = road.demand_electricity + rail.demand_electricity
    # t.CO2e_cb = air.CO2e_cb + road.CO2e_cb + rail.CO2e_cb + ship.CO2e_cb
    # t.CO2e_total = t.CO2e_cb

    s_lpg.energy = t.demand_lpg

    s_diesel.energy = t.demand_diesel
    s_gas.energy = t.demand_gas
    s_biogas.energy = t.demand_biogas

    s_diesel.energy = t.demand_diesel
    s_gas.energy = t.demand_gas
    s_biogas.energy = t.demand_biogas
    s_bioethanol.energy = t.demand_bioethanol
    s_biodiesel.energy = t.demand_biodiesel
    s_elec.energy = t.demand_electricity

    s_biogas.energy = t.demand_biogas
    s_bioethanol.energy = t.demand_bioethanol
    s_biodiesel.energy = t.demand_biodiesel

    s.energy = (
        s_petrol.energy
        + s_jetfuel.energy
        + s_diesel.energy
        + s_fueloil.energy
        + s_lpg.energy
        + s_gas.energy
        + s_biogas.energy
        + s_bioethanol.energy
        + s_biodiesel.energy
        + s_elec.energy
    )

    t18.air_dmstc = air_dmstc
    t18.air_inter = air_inter
    t18.air = air

    t18.road_car_it_ot = road_car_it_ot
    t18.road_car_ab = road_car_ab
    t18.road_car = road_car
    t18.road_bus = road_bus
    t18.road_ppl = road_ppl
    t18.road_gds_mhd_it_ot = road_gds_mhd_it_ot
    t18.road_gds_mhd_ab = road_gds_mhd_ab
    t18.road_gds_mhd = road_gds_mhd
    t18.road_gds_ldt_it_ot = road_gds_ldt_it_ot
    t18.road_gds_ldt_ab = road_gds_ldt_ab
    t18.road_gds_ldt = road_gds_ldt
    t18.road_gds = road_gds
    t18.road = road

    t18.rail_ppl_distance = rail_ppl_distance
    t18.rail_ppl_metro = rail_ppl_metro
    t18.rail_ppl = rail_ppl
    t18.rail_gds = rail_gds
    t18.rail = rail

    t18.ship_dmstc = ship_dmstc
    t18.ship_inter = ship_inter
    t18.ship = ship

    t18.other_foot = other_foot
    t18.other_cycl = other_cycl
    t18.other = other
    t18.t = t

    return t18
