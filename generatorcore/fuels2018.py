from dataclasses import dataclass, asdict, field

from . import transport2018
from .inputs import Inputs


@dataclass
class Vars0:
    # Used by f
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars1:
    # Used by g, d_e_hydrogen_reconv, p_emethan, p_hydrogen, p_hydrogen_reconv
    pass


@dataclass
class Vars2:
    # Used by d, d_r, d_b, d_i, d_t, d_a
    energy: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by p
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by p_petrol, p_jetfuel, p_diesel, p_bioethanol, p_biodiesel, p_biogas
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class F18:
    f: Vars0 = field(default_factory=Vars0)
    g: Vars1 = field(default_factory=Vars1)
    d: Vars2 = field(default_factory=Vars2)
    d_r: Vars2 = field(default_factory=Vars2)
    d_b: Vars2 = field(default_factory=Vars2)
    d_i: Vars2 = field(default_factory=Vars2)
    d_t: Vars2 = field(default_factory=Vars2)
    d_a: Vars2 = field(default_factory=Vars2)
    d_e_hydrogen_reconv: Vars1 = field(default_factory=Vars1)
    p: Vars3 = field(default_factory=Vars3)
    p_petrol: Vars4 = field(default_factory=Vars4)
    p_jetfuel: Vars4 = field(default_factory=Vars4)
    p_diesel: Vars4 = field(default_factory=Vars4)
    p_bioethanol: Vars4 = field(default_factory=Vars4)
    p_biodiesel: Vars4 = field(default_factory=Vars4)
    p_biogas: Vars4 = field(default_factory=Vars4)
    p_emethan: Vars1 = field(default_factory=Vars1)
    p_hydrogen: Vars1 = field(default_factory=Vars1)
    p_hydrogen_reconv: Vars1 = field(default_factory=Vars1)

    def dict(self):
        return asdict(self)


# Berechnungsfunktion Fuels 2018


def calc(inputs: Inputs, *, t18: transport2018.T18) -> F18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries

    f18 = F18()

    # ------------------------------------------------
    f18.f.CO2e_cb = 0

    f18.d_r.energy = entries.r_petrol_fec

    f18.d_b.energy = entries.b_petrol_fec + entries.b_jetfuel_fec + entries.b_diesel_fec

    f18.d_i.energy = entries.i_diesel_fec

    f18.d_t.energy = (
        t18.t.demand_petrol
        + t18.t.demand_jetfuel
        + t18.t.demand_diesel
        + t18.t.demand_biogas
        + t18.t.demand_bioethanol
        + t18.t.demand_biodiesel
    )

    f18.d_a.energy = entries.a_petrol_fec + entries.a_diesel_fec

    f18.d.energy = (
        f18.d_r.energy
        + f18.d_b.energy
        + f18.d_i.energy
        + f18.d_t.energy
        + f18.d_a.energy
    )

    f18.p_petrol.energy = (
        entries.r_petrol_fec
        + entries.b_petrol_fec
        + entries.a_petrol_fec
        + t18.t.demand_petrol
    )
    f18.p_jetfuel.energy = entries.b_jetfuel_fec + t18.s_jetfuel.energy
    f18.p_diesel.energy = (
        entries.b_diesel_fec
        + entries.i_diesel_fec
        + t18.t.demand_diesel
        + entries.a_diesel_fec
    )
    f18.p_bioethanol.energy = t18.t.demand_bioethanol
    f18.p_biodiesel.energy = t18.t.demand_biodiesel
    f18.p_biogas.energy = t18.t.demand_biogas

    f18.p.energy = (
        f18.p_petrol.energy
        + f18.p_jetfuel.energy
        + f18.p_diesel.energy
        + f18.p_bioethanol.energy
        + f18.p_biodiesel.energy
        + f18.p_biogas.energy
    )
    # ------------------------------------
    f18.p_petrol.CO2e_pb_per_MWh = fact("Fact_F_P_petrol_ratio_CO2e_pb_to_fec_2018")
    f18.p_jetfuel.CO2e_pb_per_MWh = fact("Fact_F_P_jetfuel_ratio_CO2e_pb_to_fec_2018")
    f18.p_diesel.CO2e_pb_per_MWh = fact("Fact_F_P_diesel_ratio_CO2e_pb_to_fec_2018")
    f18.p_bioethanol.CO2e_pb_per_MWh = fact(
        "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
    )
    f18.p_biodiesel.CO2e_pb_per_MWh = fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018")
    f18.p_biogas.CO2e_pb_per_MWh = fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018")
    # -------------------------------------
    f18.p_petrol.CO2e_pb = f18.p_petrol.CO2e_pb_per_MWh * f18.p_petrol.energy
    f18.p_jetfuel.CO2e_pb = f18.p_jetfuel.CO2e_pb_per_MWh * f18.p_jetfuel.energy
    f18.p_diesel.CO2e_pb = f18.p_diesel.CO2e_pb_per_MWh * f18.p_diesel.energy
    f18.p_bioethanol.CO2e_pb = (
        f18.p_bioethanol.CO2e_pb_per_MWh * f18.p_bioethanol.energy
    )
    f18.p_biodiesel.CO2e_pb = f18.p_biodiesel.CO2e_pb_per_MWh * f18.p_biodiesel.energy
    f18.p_biogas.CO2e_pb = f18.p_biogas.CO2e_pb_per_MWh * f18.p_biogas.energy

    f18.p.CO2e_pb = (
        f18.p_petrol.CO2e_pb
        + f18.p_jetfuel.CO2e_pb
        + f18.p_diesel.CO2e_pb
        + f18.p_bioethanol.CO2e_pb
        + f18.p_biodiesel.CO2e_pb
        + f18.p_biogas.CO2e_pb
    )  # SUM(p_petrol.CO2e_pb:p_biogas.CO2e_pb)

    f18.f.CO2e_pb = f18.p.CO2e_pb
    # --------------------------------------
    f18.p_petrol.CO2e_total = f18.p_petrol.CO2e_pb
    f18.p_jetfuel.CO2e_total = f18.p_jetfuel.CO2e_pb
    f18.p_diesel.CO2e_total = f18.p_diesel.CO2e_pb
    f18.p_bioethanol.CO2e_total = f18.p_bioethanol.CO2e_pb
    f18.p_biodiesel.CO2e_total = f18.p_biodiesel.CO2e_pb
    f18.p_biogas.CO2e_total = f18.p_biogas.CO2e_pb

    f18.p.CO2e_total = (
        f18.p_petrol.CO2e_total
        + f18.p_jetfuel.CO2e_total
        + f18.p_diesel.CO2e_total
        + f18.p_bioethanol.CO2e_total
        + f18.p_biodiesel.CO2e_total
        + f18.p_biogas.CO2e_total
    )

    f18.f.CO2e_total = f18.p.CO2e_total

    return f18
