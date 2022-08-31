# pyright: strict
from dataclasses import dataclass
from ..utils import element_wise_plus, MILLION
from . import co2e
from ..inputs import Inputs
import typing


@dataclass
class Road:
    """Emissions caused by transport on the Road (car, bus, lorry, ...) of both goods and people."""

    CO2e_combustion_based: float
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
        CO2e_combustion_based = co2e.from_demands(
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
        CO2e_total = CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
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
        cls, inputs: Inputs, subsection: typing.Literal["it_ot", "ab"]
    ) -> "Road":
        fact = inputs.fact

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
                * fact(f"Fact_T_S_Car_SEC_petrol_it_ot_2018")
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
                * fact(f"Fact_T_S_Car_SEC_petrol_it_ot_2018")
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
        fact = inputs.fact

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
    def calc_goods_light_duty(
        cls, inputs: Inputs, section: typing.Literal["it_ot", "ab"]
    ) -> "Road":
        fact = inputs.fact

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
    def calc_goods_medium_and_heavy_duty_it_ot(
        cls, inputs: Inputs, road_bus_mileage: float
    ):
        fact = inputs.fact

        return cls.calc_road(
            inputs,
            mileage=inputs.entries.t_mil_mhd_it_ot * MILLION - road_bus_mileage,
            transport_capacity_tkm_factor=fact("Fact_T_D_lf_gds_MHD_2018"),
            transport_capacity_pkm_factor=0,
            biogas=(
                fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
                * fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018")
                * fact("Fact_T_S_MHD_SEC_diesel_it_ot_2018")
            ),
            biodiesel=(
                fact("Fact_T_S_MHD_frac_diesel_stock_2018")
                * fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018")
                * fact("Fact_T_S_MHD_SEC_diesel_it_ot_2018")
            ),
            diesel=(
                fact("Fact_T_S_MHD_frac_diesel_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_diesel_bio_frac_2018"))
                * fact("Fact_T_S_MHD_SEC_diesel_it_ot_2018")
            ),
            electricity=(
                fact("Fact_T_S_MHD_frac_bev_stock_2018")
                * fact("Fact_T_S_MHD_SEC_elec_it_ot_2018")
            ),
            gas=(
                fact("Fact_T_S_MHD_frac_cng_lngl_stock_2018")
                * (1 - fact("Fact_T_S_Rl_Rd_cng_bio_frac_2018"))
                * fact("Fact_T_S_MHD_SEC_diesel_it_ot_2018")
            ),
            bioethanol=0,
            lpg=0,
            petrol=0,
        )

    @classmethod
    def calc_goods_medium_and_heavy_duty_ab(cls, inputs: Inputs):
        fact = inputs.fact

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
