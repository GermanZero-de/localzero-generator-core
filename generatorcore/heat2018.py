from dataclasses import dataclass, asdict, field

from . import transport2018, electricity2018
from .inputs import Inputs
from .utils import div


@dataclass
class Vars0:
    # Used by g, g_storage, g_planning
    pass


@dataclass
class Vars1:
    # Used by d, d_r, d_b, d_i, d_t, a_t
    energy: float = None  # type: ignore


@dataclass
class Vars2:
    # Used by h
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by p_gas, p_opetpro, p_coal
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars5:
    # Used by p_lpg, p_fueloil, p_heatnet_cogen, p_heatnet_plant
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by p_heatnet
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by p_heatnet_geoth, p_heatnet_lheatpump
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by p_biomass, p_ofossil, p_orenew, p_solarth, p_heatpump
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class H18:
    g: Vars0 = field(default_factory=Vars0)
    g_storage: Vars0 = field(default_factory=Vars0)
    g_planning: Vars0 = field(default_factory=Vars0)
    d: Vars1 = field(default_factory=Vars1)
    d_r: Vars1 = field(default_factory=Vars1)
    d_b: Vars1 = field(default_factory=Vars1)
    d_i: Vars1 = field(default_factory=Vars1)
    d_t: Vars1 = field(default_factory=Vars1)
    a_t: Vars1 = field(default_factory=Vars1)
    h: Vars2 = field(default_factory=Vars2)
    p: Vars3 = field(default_factory=Vars3)
    p_gas: Vars4 = field(default_factory=Vars4)
    p_lpg: Vars5 = field(default_factory=Vars5)
    p_fueloil: Vars5 = field(default_factory=Vars5)
    p_opetpro: Vars4 = field(default_factory=Vars4)
    p_coal: Vars4 = field(default_factory=Vars4)
    p_heatnet: Vars6 = field(default_factory=Vars6)
    p_heatnet_cogen: Vars5 = field(default_factory=Vars5)
    p_heatnet_plant: Vars5 = field(default_factory=Vars5)
    p_heatnet_geoth: Vars7 = field(default_factory=Vars7)
    p_heatnet_lheatpump: Vars7 = field(default_factory=Vars7)
    p_biomass: Vars8 = field(default_factory=Vars8)
    p_ofossil: Vars8 = field(default_factory=Vars8)
    p_orenew: Vars8 = field(default_factory=Vars8)
    p_solarth: Vars8 = field(default_factory=Vars8)
    p_heatpump: Vars8 = field(default_factory=Vars8)

    def dict(self):
        return asdict(self)


def calc(inputs: Inputs, *, t18: transport2018.T18, e18: electricity2018.E18) -> H18:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    entries = inputs.entries

    ###########################
    ### Demand of Heat 2018 ###
    ###########################

    h18 = H18()

    # starting with sectors
    # Demand Residential:
    d_r = h18.d_r  # -> Abkürzung für weniger Schreibarbeit
    # 1
    d_r.energy = (
        entries.r_coal_fec
        + entries.r_fueloil_fec
        + entries.r_lpg_fec
        + entries.r_gas_fec
        + entries.r_biomass_fec
        + entries.r_orenew_fec
        + entries.r_heatnet_fec
    )
    # result: 516.686.389 MWh

    # Demand Business:
    d_b = h18.d_b
    # 1
    d_b.energy = (
        entries.b_coal_fec
        + entries.b_fueloil_fec
        + entries.b_lpg_fec
        + entries.b_gas_fec
        + entries.b_biomass_fec
        + entries.b_orenew_fec
        + entries.b_heatnet_fec
    )

    # result: 164.713.333 MWh

    # Demand Industry:
    d_i = h18.d_i
    # 1
    d_i.energy = (
        entries.i_coal_fec
        + entries.i_fueloil_fec
        + entries.i_lpg_fec
        + entries.i_opetpro_fec
        + entries.i_gas_fec
        + entries.i_biomass_fec
        + entries.i_orenew_fec
        + entries.i_ofossil_fec
        + entries.i_heatnet_fec
        # result: 496.210.833 MWh
    )

    # Demand Transport:
    d_t = h18.d_t

    d_t.energy = t18.t.demand_fueloil + t18.t.demand_lpg + t18.t.demand_gas
    # percentages of sectors of total heat demand 2018

    a_t = h18.a_t
    a_t.energy = (
        entries.a_fueloil_fec
        + entries.a_lpg_fec
        + entries.a_gas_fec
        + entries.a_biomass_fec
    )

    # Demand Heat 2018 in total:

    d = h18.d
    # 1
    d.energy = (
        d_r.energy
        + d_b.energy
        + d_i.energy
        + d_t.energy
        + a_t.energy
        # result: 1.220.186.729 MWh
    )

    ###############################
    ### Production of Heat 2018 ###
    ###############################

    # Production Heat 2018 in total:

    p = h18.p
    # 1
    p.energy = (
        d.energy
        # result: 1.220.186.729 MWh
    )

    ### calculating the energy sources ###

    # Production gas:

    p_gas = h18.p_gas

    # 1 final energy consumption
    p_gas.energy = (
        entries.r_gas_fec
        + entries.b_gas_fec
        + entries.i_gas_fec
        + entries.a_gas_fec
        + t18.t.demand_gas
        # result: 607.734.356 MWh
    )

    # 2 pct of total final energy consumption
    p_gas.pct_energy = div(p_gas.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_gas.CO2e_production_based_per_MWh = fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_gas.CO2e_production_based = p_gas.energy * p_gas.CO2e_production_based_per_MWh

    # 5 combustion-based CO2e factor per MWh final energy
    p_gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_gas.CO2e_combustion_based = p_gas.energy * p_gas.CO2e_combustion_based_per_MWh

    # 7 total CO2e
    p_gas.CO2e_total = p_gas.CO2e_production_based + p_gas.CO2e_combustion_based

    # Production lpg:

    p_lpg = h18.p_lpg

    # 1 final energy consumption
    p_lpg.energy = (
        entries.r_lpg_fec
        + entries.b_lpg_fec
        + entries.i_lpg_fec
        + entries.a_lpg_fec
        + t18.s_lpg.energy
        # result: 21.907.374 MWh
    )

    # 2 pct of total final energy consumption
    p_lpg.pct_energy = div(p_lpg.energy, p.energy)

    # 4 no process-based CO2e

    # 5 combustion-based CO2e factor per MWh final energy
    p_lpg.CO2e_combustion_based_per_MWh = fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_lpg.CO2e_combustion_based = p_lpg.energy * p_lpg.CO2e_combustion_based_per_MWh

    # 7 total CO2e
    p_lpg.CO2e_total = p_lpg.CO2e_combustion_based

    # Production fueloil:

    p_fueloil = h18.p_fueloil

    # 1 final energy consumption
    p_fueloil.energy = (
        entries.r_fueloil_fec
        + entries.b_fueloil_fec
        + entries.i_fueloil_fec
        + entries.a_fueloil_fec
        + t18.s_fueloil.energy
        # result: 170.176.389 MWh
    )

    # 2 pct of total final energy consumption
    p_fueloil.pct_energy = div(p_fueloil.energy, p.energy)

    # 4 no process-based CO2e

    # 5 combustion-based CO2e factor per MWh final energy
    p_fueloil.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_fueloil.CO2e_combustion_based = (
        p_fueloil.energy * p_fueloil.CO2e_combustion_based_per_MWh
    )

    # 7 total CO2e
    p_fueloil.CO2e_total = p_fueloil.CO2e_combustion_based

    # Production other petrol products (opetpro):

    p_opetpro = h18.p_opetpro

    # 1 final energy consumption
    p_opetpro.energy = (
        entries.i_opetpro_fec
        # result: 14.255.833 MWh
    )

    # 2 pct of total final energy consumption
    p_opetpro.pct_energy = div(p_opetpro.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_opetpro.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018"
    )
    # 4 process-based CO2e
    p_opetpro.CO2e_production_based = (
        p_opetpro.energy * p_opetpro.CO2e_production_based_per_MWh
    )

    # 5 combustion-based CO2e factor per MWh final energy
    p_opetpro.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_opetpro.CO2e_combustion_based = (
        p_opetpro.energy * p_opetpro.CO2e_combustion_based_per_MWh
    )

    # 7 total CO2e
    p_opetpro.CO2e_total = (
        p_opetpro.CO2e_production_based + p_opetpro.CO2e_combustion_based
    )

    # Production coal:

    p_coal = h18.p_coal

    # 1 final energy consumption
    p_coal.energy = (
        entries.r_coal_fec
        + entries.b_coal_fec
        + entries.i_coal_fec
        # result: 123.883.611 MWh
    )

    # 2 pct of total final energy consumption
    p_coal.pct_energy = div(p_coal.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_coal.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"
    )
    # 4 process-based CO2e
    p_coal.CO2e_production_based = p_coal.energy * p_coal.CO2e_production_based_per_MWh

    # 5 combustion-based CO2e factor per MWh final energy
    p_coal.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_coal.CO2e_combustion_based = p_coal.energy * p_coal.CO2e_combustion_based_per_MWh

    # 7 total CO2e
    p_coal.CO2e_total = p_coal.CO2e_production_based + p_coal.CO2e_combustion_based

    # Production heatnet:

    p_heatnet = h18.p_heatnet

    # 1 final energy consumption
    p_heatnet.energy = (
        entries.r_heatnet_fec
        + entries.b_heatnet_fec
        + entries.i_heatnet_fec
        # result: 109.472.500 MWh
    )

    # 2 pct of total final energy consumption
    p_heatnet.pct_energy = div(p_heatnet.energy, p.energy)

    # Production cogenerated heatnet:

    p_heatnet_cogen = h18.p_heatnet_cogen

    # 1 final energy consumption
    # if-sequence is necessary to avoid more cogenerated heat produced than used - and later negative heatnet_plant
    if (
        e18.p_fossil_coal_brown_cogen.energy
        + e18.p_fossil_coal_black_cogen.energy
        + e18.p_fossil_gas_cogen.energy
        + e18.p_fossil_ofossil_cogen.energy
        + e18.p_renew_biomass_cogen.energy
    ) < p_heatnet.energy:

        p_heatnet_cogen.energy = (
            e18.p_fossil_coal_brown_cogen.energy
            + e18.p_fossil_coal_black_cogen.energy
            + e18.p_fossil_gas_cogen.energy
            + e18.p_fossil_ofossil_cogen.energy
            + e18.p_renew_biomass_cogen.energy
            # result: 82.686.089 MWh
        )

    else:
        p_heatnet_cogen.energy = p_heatnet.energy

    # 2 pct of total final energy consumption of heatnet
    p_heatnet_cogen.pct_energy = div(p_heatnet_cogen.energy, p_heatnet.energy)

    # 4 no process-based CO2e

    # 5 combustion-based CO2e factor per MWh final energy
    p_heatnet_cogen.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_heatnet_cogen_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_heatnet_cogen.CO2e_combustion_based = (
        p_heatnet_cogen.energy * p_heatnet_cogen.CO2e_combustion_based_per_MWh
    )
    # 7 total CO2e
    p_heatnet_cogen.CO2e_total = p_heatnet_cogen.CO2e_combustion_based

    # Production heatnet in plants:

    p_heatnet_plant = h18.p_heatnet_plant

    # 1 final energy consumption
    # due to the if-sequence in p_heatnet_cogen this value cannot become negative
    p_heatnet_plant.energy = (
        p_heatnet.energy
        - p_heatnet_cogen.energy
        # result: 26.786.411 MWh
    )

    # 2 pct of total final energy consumption of heatnet
    p_heatnet_plant.pct_energy = div(p_heatnet_plant.energy, p_heatnet.energy)

    # 4 no process-based CO2e

    # 5 combustion-based CO2e factor per MWh final energy
    p_heatnet_plant.CO2e_combustion_based_per_MWh = fact(
        "Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_heatnet_plant.CO2e_combustion_based = (
        p_heatnet_plant.energy * p_heatnet_plant.CO2e_combustion_based_per_MWh
    )
    # 7 total CO2e
    p_heatnet_plant.CO2e_total = p_heatnet_plant.CO2e_combustion_based

    ## back to total heatnet ##

    # 4 no process-based CO2e

    # 6 combustion-based CO2e
    p_heatnet.CO2e_combustion_based = (
        p_heatnet_cogen.CO2e_combustion_based + p_heatnet_plant.CO2e_combustion_based
    )

    # 7 total CO2e
    p_heatnet.CO2e_total = p_heatnet.CO2e_combustion_based

    p_heatnet_geoth = h18.p_heatnet_geoth

    p_heatnet_geoth.pct_energy = 0
    p_heatnet_geoth.energy = p_heatnet_geoth.pct_energy * p_heatnet.energy

    p_heatnet_geoth.CO2e_combustion_based = 0
    p_heatnet_geoth.CO2e_production_based = 0
    p_heatnet_geoth.CO2e_total = (
        p_heatnet_geoth.CO2e_production_based + p_heatnet_geoth.CO2e_combustion_based
    )

    p_heatnet_lheatpump = h18.p_heatnet_lheatpump
    p_heatnet_lheatpump.pct_energy = 0
    p_heatnet_lheatpump.CO2e_production_based = 0
    p_heatnet_lheatpump.CO2e_combustion_based = 0
    p_heatnet_lheatpump.energy = p_heatnet_lheatpump.pct_energy * p_heatnet.energy
    p_heatnet_lheatpump.CO2e_total = (
        p_heatnet_lheatpump.CO2e_production_based
        + p_heatnet_lheatpump.CO2e_combustion_based
    )

    # Production biomass:

    p_biomass = h18.p_biomass

    # 1 final energy consumption
    p_biomass.energy = (
        entries.r_biomass_fec
        + entries.b_biomass_fec
        + entries.i_biomass_fec
        + entries.a_biomass_fec
        # result: 128.372.500 MWh
    )

    # 2 pct of total final energy consumption
    p_biomass.pct_energy = div(p_biomass.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_biomass.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
    )
    # 4 process-based CO2e
    p_biomass.CO2e_production_based = (
        p_biomass.energy * p_biomass.CO2e_production_based_per_MWh
    )

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_biomass.CO2e_total = p_biomass.CO2e_production_based

    # Production ofossil:

    p_ofossil = h18.p_ofossil

    # 1 final energy consumption
    """p_coal.energy = (
        entry ('In_I_ofossil_fec')

        #result: 21.019.444 MWh
    )"""

    p_ofossil.energy = entries.i_ofossil_fec

    # 2 pct of total final energy consumption
    p_ofossil.pct_energy = div(p_ofossil.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_ofossil.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"
    )
    # 4 process-based CO2e
    p_ofossil.CO2e_production_based = (
        p_ofossil.energy * p_ofossil.CO2e_production_based_per_MWh
    )

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_ofossil.CO2e_total = p_ofossil.CO2e_production_based

    # Production other renewables:

    p_orenew = h18.p_orenew

    # 1 final energy consumption
    p_orenew.energy = (
        entries.r_orenew_fec
        + entries.b_orenew_fec
        + entries.i_orenew_fec
        # result: 123.883.611 MWh
    )

    # 2 pct of total final energy consumption
    p_orenew.pct_energy = div(p_orenew.energy, p.energy)

    # Production solarthermal energy within other renewables:

    p_solarth = h18.p_solarth

    # 2 pct of other renewables' final energy consumption
    p_solarth.pct_energy = fact("Fact_R_S_ratio_solarth_to_orenew_2018")

    # 1 final energy consumption
    p_solarth.energy = (
        p_orenew.energy
        * p_solarth.pct_energy
        # result: 9.444.712 MWh
    )

    # 3 process-based CO2e factor per MWh final energy
    p_solarth.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    # 4 process-based CO2e
    p_solarth.CO2e_production_based = (
        p_solarth.energy * p_solarth.CO2e_production_based_per_MWh
    )

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_solarth.CO2e_total = p_solarth.CO2e_production_based

    # Production heatpump energy within other renewables:

    p_heatpump = h18.p_heatpump

    # 2 pct of other renewables' final energy consumption
    p_heatpump.pct_energy = fact("Fact_R_S_ratio_heatpump_to_orenew_2018")

    # 1 final energy consumption
    p_heatpump.energy = (
        p_orenew.energy
        * p_heatpump.pct_energy
        # result: 13.920.010 MWh
    )

    # 3 process-based CO2e factor per MWh final energy
    p_heatpump.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    # 4 process-based CO2e
    p_heatpump.CO2e_production_based = (
        p_heatpump.energy * p_heatpump.CO2e_production_based_per_MWh
    )

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_heatpump.CO2e_total = p_heatpump.CO2e_production_based

    # back to other renewables

    # 4 process-based CO2e
    p_orenew.CO2e_production_based = (
        p_solarth.CO2e_production_based + p_heatpump.CO2e_production_based
    )

    # 6 no combustion-based CO2e

    p_orenew.CO2e_total = p_orenew.CO2e_production_based

    p_orenew.CO2e_production_based_per_MWh = 0

    p_solarth = h18.p_solarth

    p_solarth.energy = p_orenew.energy * fact("Fact_R_S_ratio_solarth_to_orenew_2018")
    p_solarth.pct_energy = div(p_solarth.energy, p_orenew.energy)
    p_solarth.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )
    p_solarth.CO2e_production_based = (
        p_solarth.energy * p_solarth.CO2e_production_based_per_MWh
    )
    p_solarth.CO2e_total = p_solarth.CO2e_production_based

    p_heatpump = h18.p_heatpump
    p_heatpump.energy = p_orenew.energy * fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    p_heatpump.pct_energy = div(p_heatpump.energy, p_orenew.energy)
    p_heatpump.CO2e_production_based_per_MWh = fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"
    )

    p_heatpump.CO2e_production_based = (
        p_heatpump.energy * p_heatpump.CO2e_production_based_per_MWh
    )
    p_heatpump.CO2e_total = p_heatpump.CO2e_production_based

    # 7 total CO2e
    # ### total CO2e of Heat 2018 ###

    # 4 process-based CO2e of Heat 2018
    p.CO2e_production_based = (
        p_gas.CO2e_production_based
        + p_opetpro.CO2e_production_based
        + p_coal.CO2e_production_based
        + p_biomass.CO2e_production_based
        + p_ofossil.CO2e_production_based
        + p_orenew.CO2e_production_based
    )

    # 6 combustion-based CO2e of Heat 2018
    p.CO2e_combustion_based = (
        p_gas.CO2e_combustion_based
        + p_lpg.CO2e_combustion_based
        + p_fueloil.CO2e_combustion_based
        + p_opetpro.CO2e_combustion_based
        + p_coal.CO2e_combustion_based
        + p_heatnet.CO2e_combustion_based
    )
    # 7 total CO2e of Heat 2018

    p.CO2e_combustion_based_per_MWh = div(p.CO2e_combustion_based, p.energy)

    p.CO2e_total = (
        p_gas.CO2e_total
        + p_lpg.CO2e_total
        + p_fueloil.CO2e_total
        + p_opetpro.CO2e_total
        + p_coal.CO2e_total
        + p_heatnet.CO2e_total
        + p_biomass.CO2e_total
        + p_ofossil.CO2e_total
        + p_orenew.CO2e_total
    )

    p.pct_energy = (
        p_gas.pct_energy
        + p_lpg.pct_energy
        + p_fueloil.pct_energy
        + p_opetpro.pct_energy
        + p_coal.pct_energy
        + p_heatnet.pct_energy
        + p_biomass.pct_energy
        + p_ofossil.pct_energy
        + p_orenew.pct_energy
    )

    h = h18.h
    h.CO2e_combustion_based = p.CO2e_combustion_based
    h.CO2e_total = p.CO2e_total
    h.CO2e_production_based = p.CO2e_production_based

    return h18
