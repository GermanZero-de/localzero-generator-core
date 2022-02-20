from dataclasses import dataclass, asdict, field

from . import transport2018, electricity2018
from .inputs import Inputs
from .utils import div


# Es gibt 5 Datentabellen:
# * Fakten: <span class="mark">facts</span>
# * Annahmen: <span class="mark">assumptions</span>
# * Kommunenspezifische Daten: <span class="mark">rowCom</span>
# * Landkreisdaten: <span class="mark">rowK</span>
# * Bundesländerdaten: <span class="mark">rowBL</span>
#
# Auf die Daten könnt ihr mittels folgender Funktionen zugreifen:
# * fact()
# * ass()
# * valCom()
# * valK()
# * valBL()


# fact('Fact_A_S_biomass_fec_2018')
# display(facts)
# display(assumptions)
# display(rowK)
# display(rowBL)
# display(rowCom)


# # Template für die Sektor-Variablen (Excel-Spaltennamen)


@dataclass
class HColVars:
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_MWh: float = None  # type: ignore
    CO2e_cb: float = None  # type: ignore
    CO2e_cb_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


# Definition der Zeilennamen für den Sektor H
@dataclass
class H18:
    g: HColVars = field(default_factory=HColVars)
    g_storage: HColVars = field(default_factory=HColVars)
    g_planning: HColVars = field(default_factory=HColVars)
    d: HColVars = field(default_factory=HColVars)
    d_r: HColVars = field(default_factory=HColVars)
    d_b: HColVars = field(default_factory=HColVars)
    d_i: HColVars = field(default_factory=HColVars)
    d_t: HColVars = field(default_factory=HColVars)
    a_t: HColVars = field(default_factory=HColVars)
    h: HColVars = field(default_factory=HColVars)
    p: HColVars = field(default_factory=HColVars)
    p_gas: HColVars = field(default_factory=HColVars)
    p_lpg: HColVars = field(default_factory=HColVars)
    p_fueloil: HColVars = field(default_factory=HColVars)
    p_opetpro: HColVars = field(default_factory=HColVars)
    p_coal: HColVars = field(default_factory=HColVars)
    p_heatnet: HColVars = field(default_factory=HColVars)
    p_heatnet_cogen: HColVars = field(default_factory=HColVars)
    p_heatnet_plant: HColVars = field(default_factory=HColVars)
    p_heatnet_geoth: HColVars = field(default_factory=HColVars)
    p_heatnet_lheatpump: HColVars = field(default_factory=HColVars)
    p_biomass: HColVars = field(default_factory=HColVars)
    p_ofossil: HColVars = field(default_factory=HColVars)
    p_orenew: HColVars = field(default_factory=HColVars)
    p_solarth: HColVars = field(default_factory=HColVars)
    p_heatpump: HColVars = field(default_factory=HColVars)
    p_solarth: HColVars = field(default_factory=HColVars)

    def dict(self):
        return asdict(self)


def calc(inputs: Inputs, *, t18: transport2018.T18, e18: electricity2018.E18) -> H18:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    ###########################
    ### Demand of Heat 2018 ###
    ###########################

    h18 = H18()

    # starting with sectors
    # Demand Residential:
    d_r = h18.d_r  # -> Abkürzung für weniger Schreibarbeit
    # 1
    d_r.energy = (
        entry("In_R_coal_fec")
        + entry("In_R_fueloil_fec")
        + entry("In_R_lpg_fec")
        + entry("In_R_gas_fec")
        + entry("In_R_biomass_fec")
        + entry("In_R_orenew_fec")
        + entry("In_R_heatnet_fec")
    )
    # result: 516.686.389 MWh

    # Demand Business:
    d_b = h18.d_b
    # 1
    d_b.energy = (
        entry("In_B_coal_fec")
        + entry("In_B_fueloil_fec")
        + entry("In_B_lpg_fec")
        + entry("In_B_gas_fec")
        + entry("In_B_biomass_fec")
        + entry("In_B_orenew_fec")
        + entry("In_B_heatnet_fec")
    )

    # result: 164.713.333 MWh

    # Demand Industry:
    d_i = h18.d_i
    # 1
    d_i.energy = (
        entry("In_I_coal_fec")
        + entry("In_I_fueloil_fec")
        + entry("In_I_lpg_fec")
        + entry("In_I_opetpro_fec")
        + entry("In_I_gas_fec")
        + entry("In_I_biomass_fec")
        + entry("In_I_orenew_fec")
        + entry("In_I_ofossil_fec")
        + entry("In_I_heatnet_fec")
        # result: 496.210.833 MWh
    )

    # Demand Transport:
    d_t = h18.d_t

    d_t.energy = t18.t.demand_fueloil + t18.t.demand_lpg + t18.t.demand_gas
    # percentages of sectors of total heat demand 2018

    a_t = h18.a_t
    a_t.energy = (
        entry("In_A_fueloil_fec")
        + entry("In_A_lpg_fec")
        + entry("In_A_gas_fec")
        + entry("In_A_biomass_fec")
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
        entry("In_R_gas_fec")
        + entry("In_B_gas_fec")
        + entry("In_I_gas_fec")
        + entry("In_A_gas_fec")
        + t18.t.demand_gas
        # result: 607.734.356 MWh
    )

    # 2 pct of total final energy consumption
    p_gas.pct_energy = div(p_gas.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_gas.CO2e_pb_per_MWh = fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_gas.CO2e_pb = p_gas.energy * p_gas.CO2e_pb_per_MWh

    # 5 combustion-based CO2e factor per MWh final energy
    p_gas.CO2e_cb_per_MWh = fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_gas.CO2e_cb = p_gas.energy * p_gas.CO2e_cb_per_MWh

    # 7 total CO2e
    p_gas.CO2e_total = p_gas.CO2e_pb + p_gas.CO2e_cb

    # Production lpg:

    p_lpg = h18.p_lpg

    # 1 final energy consumption
    p_lpg.energy = (
        entry("In_R_lpg_fec")
        + entry("In_B_lpg_fec")
        + entry("In_I_lpg_fec")
        + entry("In_A_lpg_fec")
        + t18.s_lpg.energy
        # result: 21.907.374 MWh
    )

    # 2 pct of total final energy consumption
    p_lpg.pct_energy = div(p_lpg.energy, p.energy)

    # 4 no process-based CO2e

    # 5 combustion-based CO2e factor per MWh final energy
    p_lpg.CO2e_cb_per_MWh = fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_lpg.CO2e_cb = p_lpg.energy * p_lpg.CO2e_cb_per_MWh

    # 7 total CO2e
    p_lpg.CO2e_total = p_lpg.CO2e_cb

    # Production fueloil:

    p_fueloil = h18.p_fueloil

    # 1 final energy consumption
    p_fueloil.energy = (
        entry("In_R_fueloil_fec")
        + entry("In_B_fueloil_fec")
        + entry("In_I_fueloil_fec")
        + entry("In_A_fueloil_fec")
        + t18.s_fueloil.energy
        # result: 170.176.389 MWh
    )

    # 2 pct of total final energy consumption
    p_fueloil.pct_energy = div(p_fueloil.energy, p.energy)

    # 4 no process-based CO2e

    # 5 combustion-based CO2e factor per MWh final energy
    p_fueloil.CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_fueloil.CO2e_cb = p_fueloil.energy * p_fueloil.CO2e_cb_per_MWh

    # 7 total CO2e
    p_fueloil.CO2e_total = p_fueloil.CO2e_cb

    # Production other petrol products (opetpro):

    p_opetpro = h18.p_opetpro

    # 1 final energy consumption
    p_opetpro.energy = (
        entry("In_I_opetpro_fec")
        # result: 14.255.833 MWh
    )

    # 2 pct of total final energy consumption
    p_opetpro.pct_energy = div(p_opetpro.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_opetpro.CO2e_pb_per_MWh = fact("Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_opetpro.CO2e_pb = p_opetpro.energy * p_opetpro.CO2e_pb_per_MWh

    # 5 combustion-based CO2e factor per MWh final energy
    p_opetpro.CO2e_cb_per_MWh = fact("Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_opetpro.CO2e_cb = p_opetpro.energy * p_opetpro.CO2e_cb_per_MWh

    # 7 total CO2e
    p_opetpro.CO2e_total = p_opetpro.CO2e_pb + p_opetpro.CO2e_cb

    # Production coal:

    p_coal = h18.p_coal

    # 1 final energy consumption
    p_coal.energy = (
        entry("In_R_coal_fec")
        + entry("In_B_coal_fec")
        + entry("In_I_coal_fec")
        # result: 123.883.611 MWh
    )

    # 2 pct of total final energy consumption
    p_coal.pct_energy = div(p_coal.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_coal.CO2e_pb_per_MWh = fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_coal.CO2e_pb = p_coal.energy * p_coal.CO2e_pb_per_MWh

    # 5 combustion-based CO2e factor per MWh final energy
    p_coal.CO2e_cb_per_MWh = fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018")
    # 6 combustion-based CO2e
    p_coal.CO2e_cb = p_coal.energy * p_coal.CO2e_cb_per_MWh

    # 7 total CO2e
    p_coal.CO2e_total = p_coal.CO2e_pb + p_coal.CO2e_cb

    # Production heatnet:

    p_heatnet = h18.p_heatnet

    # 1 final energy consumption
    p_heatnet.energy = (
        entry("In_R_heatnet_fec")
        + entry("In_B_heatnet_fec")
        + entry("In_I_heatnet_fec")
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
    p_heatnet_cogen.CO2e_cb_per_MWh = fact(
        "Fact_H_P_heatnet_cogen_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_heatnet_cogen.CO2e_cb = p_heatnet_cogen.energy * p_heatnet_cogen.CO2e_cb_per_MWh
    # 7 total CO2e
    p_heatnet_cogen.CO2e_total = p_heatnet_cogen.CO2e_cb

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
    p_heatnet_plant.CO2e_cb_per_MWh = fact(
        "Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"
    )
    # 6 combustion-based CO2e
    p_heatnet_plant.CO2e_cb = p_heatnet_plant.energy * p_heatnet_plant.CO2e_cb_per_MWh
    # 7 total CO2e
    p_heatnet_plant.CO2e_total = p_heatnet_plant.CO2e_cb

    ## back to total heatnet ##

    # 4 no process-based CO2e

    # 6 combustion-based CO2e
    p_heatnet.CO2e_cb = p_heatnet_cogen.CO2e_cb + p_heatnet_plant.CO2e_cb

    # 7 total CO2e
    p_heatnet.CO2e_total = p_heatnet.CO2e_cb

    p_heatnet_geoth = h18.p_heatnet_geoth

    p_heatnet_geoth.pct_energy = 0
    p_heatnet_geoth.energy = p_heatnet_geoth.pct_energy * p_heatnet.energy

    p_heatnet_geoth.CO2e_cb = 0
    p_heatnet_geoth.CO2e_pb = 0
    p_heatnet_geoth.CO2e_total = p_heatnet_geoth.CO2e_pb + p_heatnet_geoth.CO2e_cb

    p_heatnet_lheatpump = h18.p_heatnet_lheatpump
    p_heatnet_lheatpump.pct_energy = 0
    p_heatnet_lheatpump.CO2e_pb = 0
    p_heatnet_lheatpump.CO2e_cb = 0
    p_heatnet_lheatpump.energy = p_heatnet_lheatpump.pct_energy * p_heatnet.energy
    p_heatnet_lheatpump.CO2e_total = (
        p_heatnet_lheatpump.CO2e_pb + p_heatnet_lheatpump.CO2e_cb
    )

    # Production biomass:

    p_biomass = h18.p_biomass

    # 1 final energy consumption
    p_biomass.energy = (
        entry("In_R_biomass_fec")
        + entry("In_B_biomass_fec")
        + entry("In_I_biomass_fec")
        + entry("In_A_biomass_fec")
        # result: 128.372.500 MWh
    )

    # 2 pct of total final energy consumption
    p_biomass.pct_energy = div(p_biomass.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_biomass.CO2e_pb_per_MWh = fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_biomass.CO2e_pb = p_biomass.energy * p_biomass.CO2e_pb_per_MWh

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_biomass.CO2e_total = p_biomass.CO2e_pb

    # Production ofossil:

    p_ofossil = h18.p_ofossil

    # 1 final energy consumption
    """p_coal.energy = (
        entry ('In_I_ofossil_fec')

        #result: 21.019.444 MWh
    )"""

    p_ofossil.energy = entry("In_I_ofossil_fec")

    # 2 pct of total final energy consumption
    p_ofossil.pct_energy = div(p_ofossil.energy, p.energy)

    # 3 process-based CO2e factor per MWh final energy
    p_ofossil.CO2e_pb_per_MWh = fact("Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_ofossil.CO2e_pb = p_ofossil.energy * p_ofossil.CO2e_pb_per_MWh

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_ofossil.CO2e_total = p_ofossil.CO2e_pb

    # Production other renewables:

    p_orenew = h18.p_orenew

    # 1 final energy consumption
    p_orenew.energy = (
        entry("In_R_orenew_fec")
        + entry("In_B_orenew_fec")
        + entry("In_I_orenew_fec")
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
    p_solarth.CO2e_pb_per_MWh = fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_solarth.CO2e_pb = p_solarth.energy * p_solarth.CO2e_pb_per_MWh

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_solarth.CO2e_total = p_solarth.CO2e_pb

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
    p_heatpump.CO2e_pb_per_MWh = fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018")
    # 4 process-based CO2e
    p_heatpump.CO2e_pb = p_heatpump.energy * p_heatpump.CO2e_pb_per_MWh

    # 6 no combustion-based CO2e

    # 7 total CO2e
    p_heatpump.CO2e_total = p_heatpump.CO2e_pb

    # back to other renewables

    # 4 process-based CO2e
    p_orenew.CO2e_pb = p_solarth.CO2e_pb + p_heatpump.CO2e_pb

    # 6 no combustion-based CO2e

    p_orenew.CO2e_total = p_orenew.CO2e_pb

    p_orenew.CO2e_pb_per_MWh = 0

    p_solarth = h18.p_solarth

    p_solarth.energy = p_orenew.energy * fact("Fact_R_S_ratio_solarth_to_orenew_2018")
    p_solarth.pct_energy = div(p_solarth.energy, p_orenew.energy)
    p_solarth.CO2e_pb_per_MWh = fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018")
    p_solarth.CO2e_pb = p_solarth.energy * p_solarth.CO2e_pb_per_MWh
    p_solarth.CO2e_total = p_solarth.CO2e_pb

    p_heatpump = h18.p_heatpump
    p_heatpump.energy = p_orenew.energy * fact("Fact_R_S_ratio_heatpump_to_orenew_2018")
    p_heatpump.pct_energy = div(p_heatpump.energy, p_orenew.energy)
    p_heatpump.CO2e_pb_per_MWh = fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018")

    p_heatpump.CO2e_pb = p_heatpump.energy * p_heatpump.CO2e_pb_per_MWh
    p_heatpump.CO2e_total = p_heatpump.CO2e_pb

    # 7 total CO2e
    # ### total CO2e of Heat 2018 ###

    # 4 process-based CO2e of Heat 2018
    p.CO2e_pb = (
        p_gas.CO2e_pb
        + p_opetpro.CO2e_pb
        + p_coal.CO2e_pb
        + p_biomass.CO2e_pb
        + p_ofossil.CO2e_pb
        + p_orenew.CO2e_pb
    )

    # 6 combustion-based CO2e of Heat 2018
    p.CO2e_cb = (
        p_gas.CO2e_cb
        + p_lpg.CO2e_cb
        + p_fueloil.CO2e_cb
        + p_opetpro.CO2e_cb
        + p_coal.CO2e_cb
        + p_heatnet.CO2e_cb
    )
    # 7 total CO2e of Heat 2018

    p.CO2e_cb_per_MWh = div(p.CO2e_cb, p.energy)

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
    h.CO2e_cb = p.CO2e_cb
    h.CO2e_total = p.CO2e_total
    h.CO2e_pb = p.CO2e_pb

    return h18
