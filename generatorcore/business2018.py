from dataclasses import dataclass, asdict, field
from .inputs import Inputs
from .utils import div
from . import residences2018

# Definition der relevanten Spaltennamen für den Sektor E


@dataclass
class Vars0:
    # Used by b
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars1:
    # Used by g, g_consult, s_emethan
    pass


@dataclass
class Vars2:
    # Used by p, p_elec_elcon, p_elec_heatpump, p_vehicles, p_other
    energy: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by p_nonresi
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by p_nonresi_com
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass
class Vars5:
    # Used by s
    CO2e_cb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by s_gas, s_lpg, s_petrol, s_jetfuel, s_diesel, s_fueloil, s_coal, s_heatnet, s_heatpump, s_solarth
    CO2e_cb: float = None  # type: ignore
    CO2e_cb_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by s_biomass
    CO2e_cb: float = None  # type: ignore
    CO2e_cb_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by s_elec_heating, s_elec
    CO2e_cb: float = None  # type: ignore
    CO2e_cb_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars9:
    # Used by rb
    CO2e_cb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars10:
    # Used by rp_p
    CO2e_cb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class B18:
    b: Vars0 = field(default_factory=Vars0)
    g: Vars1 = field(default_factory=Vars1)
    g_consult: Vars1 = field(default_factory=Vars1)
    p: Vars2 = field(default_factory=Vars2)
    p_nonresi: Vars3 = field(default_factory=Vars3)
    p_nonresi_com: Vars4 = field(default_factory=Vars4)
    p_elec_elcon: Vars2 = field(default_factory=Vars2)
    p_elec_heatpump: Vars2 = field(default_factory=Vars2)
    p_vehicles: Vars2 = field(default_factory=Vars2)
    p_other: Vars2 = field(default_factory=Vars2)
    s: Vars5 = field(default_factory=Vars5)
    s_gas: Vars6 = field(default_factory=Vars6)
    s_emethan: Vars1 = field(default_factory=Vars1)
    s_lpg: Vars6 = field(default_factory=Vars6)
    s_petrol: Vars6 = field(default_factory=Vars6)
    s_jetfuel: Vars6 = field(default_factory=Vars6)
    s_diesel: Vars6 = field(default_factory=Vars6)
    s_fueloil: Vars6 = field(default_factory=Vars6)
    s_biomass: Vars7 = field(default_factory=Vars7)
    s_coal: Vars6 = field(default_factory=Vars6)
    s_heatnet: Vars6 = field(default_factory=Vars6)
    s_elec_heating: Vars8 = field(default_factory=Vars8)
    s_heatpump: Vars6 = field(default_factory=Vars6)
    s_solarth: Vars6 = field(default_factory=Vars6)
    s_elec: Vars8 = field(default_factory=Vars8)
    rb: Vars9 = field(default_factory=Vars9)
    rp_p: Vars10 = field(default_factory=Vars10)

    def dict(self):
        return asdict(self)


# Berechnungsfunktion im Sektor GHD für 2018


def calc(inputs: Inputs, *, r18: residences2018.R18) -> B18:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    entries = inputs.entries

    Million = 1000000.0

    b18 = B18()

    b18.s_gas.energy = entries.b_gas_fec  # 98.602.500 MWh

    b18.s_lpg.energy = entries.b_lpg_fec  # 3.007.222 MWh

    b18.s_petrol.energy = entries.b_petrol_fec  # 1.667.778 MWh

    b18.s_jetfuel.energy = entries.b_jetfuel_fec  # 284.722 MWh

    b18.s_diesel.energy = entries.b_diesel_fec  # 9.033.056 MWh

    b18.s_fueloil.energy = entries.b_fueloil_fec  # 33.370.278 MWh

    b18.s_biomass.energy = entries.b_biomass_fec  # 20.860.278 MWh

    b18.s_coal.energy = entries.b_coal_fec  # 232.778 MWh

    b18.s_heatnet.energy = entries.b_heatnet_fec  # 6.521.944 MWh

    b18.s_elec_heating.energy = (
        fact("Fact_B_S_elec_heating_fec_2018")
        * entries.r_flats_wo_heatnet
        / fact("Fact_R_P_flats_wo_heatnet_2011")
    )  # 13.027.778 MWh

    b18.s_heatpump.energy = entries.b_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )  # 1.262.040 MWh

    b18.s_solarth.energy = entries.b_orenew_fec * (
        1 - fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    )  # 1.262.040 MWh

    b18.s_elec.energy = entries.b_elec_fec
    # 856.293 MWh

    b18.s.energy = (
        b18.s_gas.energy
        + b18.s_lpg.energy
        + b18.s_petrol.energy
        + b18.s_jetfuel.energy
        + b18.s_diesel.energy
        + b18.s_fueloil.energy
        + b18.s_biomass.energy
        + b18.s_coal.energy
        + b18.s_heatnet.energy
        + b18.s_heatpump.energy
        + b18.s_solarth.energy
        + b18.s_elec.energy
    )  # 187.870.374 MWh

    b18.s_gas.pct_energy = div(b18.s_gas.energy, b18.s.energy)  # 52,5%

    b18.s_lpg.pct_energy = div(b18.s_lpg.energy, b18.s.energy)  # 1,6%

    b18.s_petrol.pct_energy = div(b18.s_petrol.energy, b18.s.energy)  # 0,9%

    b18.s_jetfuel.pct_energy = div(b18.s_jetfuel.energy, b18.s.energy)  # 0,2%

    b18.s_diesel.pct_energy = div(b18.s_diesel.energy, b18.s.energy)  # 4,8%

    b18.s_fueloil.pct_energy = div(b18.s_fueloil.energy, b18.s.energy)  # 17,8%

    b18.s_biomass.pct_energy = div(b18.s_biomass.energy, b18.s.energy)  # 11,1%

    b18.s_coal.pct_energy = div(b18.s_coal.energy, b18.s.energy)  # 0,1%

    b18.s_heatnet.pct_energy = div(b18.s_heatnet.energy, b18.s.energy)  # 3,5%

    b18.s_elec_heating.pct_energy = div(
        b18.s_elec_heating.energy, b18.s_elec.energy
    )  # 6,9%

    b18.s_heatpump.pct_energy = div(b18.s_heatpump.energy, b18.s.energy)  # 0,7%

    b18.s_solarth.pct_energy = div(b18.s_solarth.energy, b18.s.energy)  # 0,5%

    b18.s_elec.pct_energy = div(b18.s_elec.energy, b18.s.energy)

    b18.s.pct_energy = (
        b18.s_gas.pct_energy
        + b18.s_lpg.pct_energy
        + b18.s_petrol.pct_energy
        + b18.s_jetfuel.pct_energy
        + b18.s_diesel.pct_energy
        + b18.s_fueloil.pct_energy
        + b18.s_biomass.pct_energy
        + b18.s_coal.pct_energy
        + b18.s_heatnet.pct_energy
        + b18.s_heatpump.pct_energy
        + b18.s_solarth.pct_energy
        + b18.s_elec.pct_energy
    )

    # NACHFRAGE:
    b18.p_nonresi.area_m2 = (
        entries.r_area_m2
        * fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016")
        / (1 - fact("Fact_B_P_ratio_buisness_buildings_to_all_buildings_area_2016"))
        * (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
    )

    b18.p_nonresi_com.pct_x = ass(
        "Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050"
    )
    b18.p_nonresi_com.area_m2 = b18.p_nonresi.area_m2 * b18.p_nonresi_com.pct_x
    b18.p_nonresi.energy = (
        b18.s_gas.energy
        + b18.s_lpg.energy
        + b18.s_fueloil.energy
        + b18.s_biomass.energy
        + b18.s_coal.energy
        + b18.s_heatnet.energy
        + b18.s_heatpump.energy
        + b18.s_solarth.energy
        + b18.s_elec_heating.energy
    )
    # 187.870.374 MWh

    b18.p_nonresi_com.energy = b18.p_nonresi.energy * b18.p_nonresi_com.pct_x
    # 38.712.683 MWh

    b18.p_nonresi.number_of_buildings = (
        fact("Fact_B_P_number_business_buildings_2016")
        * entries.m_population_com_2018
        / entries.m_population_nat
    )

    b18.p_nonresi_com.factor_adapted_to_fec = div(
        b18.p_nonresi_com.energy, b18.p_nonresi_com.area_m2
    )

    # Elektrische Energie / Bisherige elektrische Verbraucher

    # Wärmepumpen
    b18.p_elec_heatpump.energy = b18.s_heatpump.energy / fact(
        "Fact_R_S_heatpump_mean_annual_performance_factor_all"
    )

    b18.p_elec_elcon.energy = b18.p_elec_elcon.energy = (
        b18.s_elec.energy - b18.p_elec_heatpump.energy - b18.s_elec_heating.energy
    )
    b18.p_vehicles.energy = (
        b18.s_petrol.energy + b18.s_jetfuel.energy + b18.s_diesel.energy
    )
    b18.p_other.energy = (
        b18.p_elec_elcon.energy + b18.p_elec_heatpump.energy + b18.p_vehicles.energy
    )  # SUM(p_elec_elcon.energy:p_vehicles.energy)
    b18.p.energy = b18.p_nonresi.energy + b18.p_other.energy
    b18.p_nonresi.factor_adapted_to_fec = div(
        b18.p_nonresi.energy, b18.p_nonresi.area_m2
    )

    # Primärenergiekosten
    b18.s_gas.cost_fuel_per_MWh = fact("Fact_R_S_gas_energy_cost_factor_2018")
    b18.s_lpg.cost_fuel_per_MWh = fact("Fact_R_S_lpg_energy_cost_factor_2018")
    b18.s_petrol.cost_fuel_per_MWh = fact("Fact_R_S_petrol_energy_cost_factor_2018")
    b18.s_jetfuel.cost_fuel_per_MWh = fact("Fact_R_S_kerosine_energy_cost_factor_2018")
    b18.s_diesel.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    b18.s_fueloil.cost_fuel_per_MWh = fact("Fact_R_S_fueloil_energy_cost_factor_2018")
    b18.s_biomass.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    b18.s_coal.cost_fuel_per_MWh = fact("Fact_R_S_coal_energy_cost_factor_2018")
    b18.s_heatnet.cost_fuel_per_MWh = fact("Fact_R_S_heatnet_energy_cost_factor_2018")
    b18.s_heatpump.cost_fuel_per_MWh = (
        fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
        / (
            fact("Fact_R_S_ground_heatpump_mean_annual_performance_factor_stock_2018")
            + fact("Fact_R_S_air_heatpump_mean_annual_performance_factor_stock_2018")
        )
        * 2
    )

    b18.s_solarth.cost_fuel_per_MWh = 0

    b18.s_gas.cost_fuel = b18.s_gas.energy * b18.s_gas.cost_fuel_per_MWh / Million

    b18.s_lpg.cost_fuel = b18.s_lpg.energy * b18.s_lpg.cost_fuel_per_MWh / Million
    b18.s_petrol.cost_fuel = (
        b18.s_petrol.energy * b18.s_petrol.cost_fuel_per_MWh / Million
    )
    b18.s_jetfuel.cost_fuel = (
        b18.s_jetfuel.energy * b18.s_jetfuel.cost_fuel_per_MWh / Million
    )
    b18.s_diesel.cost_fuel = (
        b18.s_diesel.energy * b18.s_diesel.cost_fuel_per_MWh / Million
    )
    b18.s_fueloil.cost_fuel = (
        b18.s_fueloil.energy * b18.s_fueloil.cost_fuel_per_MWh / Million
    )
    b18.s_biomass.cost_fuel = (
        b18.s_biomass.energy * b18.s_biomass.cost_fuel_per_MWh / Million
    )
    b18.s_coal.cost_fuel = b18.s_coal.energy * b18.s_coal.cost_fuel_per_MWh / Million
    b18.s_heatnet.cost_fuel = (
        b18.s_heatnet.energy * b18.s_heatnet.cost_fuel_per_MWh / Million
    )
    b18.s_heatpump.cost_fuel = (
        b18.s_heatpump.energy * b18.s_heatpump.cost_fuel_per_MWh / Million
    )
    b18.s_solarth.cost_fuel = 0

    b18.s.cost_fuel = (
        b18.s_gas.cost_fuel
        + b18.s_lpg.cost_fuel
        + b18.s_petrol.cost_fuel
        + b18.s_jetfuel.cost_fuel
        + b18.s_diesel.cost_fuel
        + b18.s_fueloil.cost_fuel
        + b18.s_biomass.cost_fuel
        + b18.s_coal.cost_fuel
        + b18.s_heatnet.cost_fuel
        + b18.s_heatpump.cost_fuel
        + b18.s_solarth.cost_fuel
    )

    # Energiebedingte THG-Emissionen
    b18.s_gas.CO2e_cb_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    b18.s_lpg.CO2e_cb_per_MWh = fact("Fact_H_P_LPG_cb_EF")
    b18.s_petrol.CO2e_cb_per_MWh = fact("Fact_H_P_petrol_cb_EF")
    b18.s_jetfuel.CO2e_cb_per_MWh = fact("Fact_H_P_kerosene_cb_EF")
    b18.s_diesel.CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    b18.s_fueloil.CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    b18.s_biomass.CO2e_cb_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    b18.s_coal.CO2e_cb_per_MWh = fact("Fact_R_S_coal_CO2e_EF")

    b18.s_gas.CO2e_cb = b18.s_gas.energy * b18.s_gas.CO2e_cb_per_MWh
    b18.s_lpg.CO2e_cb = b18.s_lpg.energy * b18.s_lpg.CO2e_cb_per_MWh
    b18.s_petrol.CO2e_cb = b18.s_petrol.energy * b18.s_petrol.CO2e_cb_per_MWh
    b18.s_jetfuel.CO2e_cb = b18.s_jetfuel.energy * b18.s_jetfuel.CO2e_cb_per_MWh
    b18.s_diesel.CO2e_cb = b18.s_diesel.energy * b18.s_diesel.CO2e_cb_per_MWh
    b18.s_fueloil.CO2e_cb = b18.s_fueloil.energy * b18.s_fueloil.CO2e_cb_per_MWh
    b18.s_biomass.CO2e_cb = b18.s_biomass.energy * b18.s_biomass.CO2e_cb_per_MWh
    b18.s_coal.CO2e_cb = b18.s_coal.energy * b18.s_coal.CO2e_cb_per_MWh

    b18.s.CO2e_cb = (
        b18.s_gas.CO2e_cb
        + b18.s_lpg.CO2e_cb
        + b18.s_petrol.CO2e_cb
        + b18.s_jetfuel.CO2e_cb
        + b18.s_diesel.CO2e_cb
        + b18.s_fueloil.CO2e_cb
        + b18.s_biomass.CO2e_cb
        + b18.s_coal.CO2e_cb
    )
    b18.s.CO2e_total = b18.s.CO2e_cb

    b18.s_gas.CO2e_total = b18.s_gas.CO2e_cb
    b18.s_lpg.CO2e_total = b18.s_lpg.CO2e_cb
    b18.s_petrol.CO2e_total = b18.s_petrol.CO2e_cb
    b18.s_jetfuel.CO2e_total = b18.s_jetfuel.CO2e_cb
    b18.s_diesel.CO2e_total = b18.s_diesel.CO2e_cb
    b18.s_fueloil.CO2e_total = b18.s_fueloil.CO2e_cb
    b18.s_biomass.CO2e_total = b18.s_biomass.CO2e_cb
    b18.s_coal.CO2e_total = b18.s_coal.CO2e_cb
    b18.s_biomass.number_of_buildings = b18.s_biomass.energy * div(
        b18.p_nonresi.number_of_buildings,
        (b18.p_nonresi.factor_adapted_to_fec * b18.p_nonresi.area_m2),
    )
    b18.rp_p.CO2e_cb = (
        r18.s.CO2e_cb
        - r18.s_petrol.CO2e_cb
        + b18.s.CO2e_cb
        - b18.s_petrol.CO2e_cb
        - b18.s_jetfuel.CO2e_cb
        - b18.s_diesel.CO2e_cb
    )
    b18.rp_p.CO2e_total = r18.s.CO2e_cb + b18.s.CO2e_cb
    b18.rb.energy = r18.p.energy + b18.p.energy
    b18.b.CO2e_cb = b18.s.CO2e_cb
    b18.rb.CO2e_cb = r18.r.CO2e_cb + b18.b.CO2e_cb
    b18.rb.CO2e_total = b18.rb.CO2e_cb
    b18.b.CO2e_total = b18.s.CO2e_total

    b18.b.CO2e_pb = 0
    b18.s_heatnet.CO2e_cb = 0
    b18.s_heatnet.CO2e_cb_per_MWh = 0
    b18.s_heatnet.CO2e_total = 0
    b18.s_heatpump.CO2e_cb = 0
    b18.s_heatpump.CO2e_cb_per_MWh = 0
    b18.s_heatpump.CO2e_total = 0
    b18.s_solarth.CO2e_cb = 0
    b18.s_solarth.CO2e_cb_per_MWh = 0
    b18.s_solarth.CO2e_total = 0
    b18.s_elec.CO2e_cb = 0
    b18.s_elec.CO2e_cb_per_MWh = 0
    b18.s_elec.CO2e_total = 0
    b18.s_elec_heating.CO2e_cb = 0
    b18.s_elec_heating.CO2e_cb_per_MWh = 0
    b18.s_elec_heating.CO2e_total = 0

    return b18
