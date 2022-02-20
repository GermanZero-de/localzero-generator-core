from dataclasses import dataclass, asdict, field

from . import transport2018
from .inputs import Inputs


#  Definition der relevanten Spaltennamen für den Sektor F (18)
@dataclass
class FColVars:
    energy: float = None  # type: ignore
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class F18:
    f: FColVars = field(default_factory=FColVars)
    g: FColVars = field(default_factory=FColVars)
    d: FColVars = field(default_factory=FColVars)
    d_r: FColVars = field(default_factory=FColVars)
    d_b: FColVars = field(default_factory=FColVars)
    d_i: FColVars = field(default_factory=FColVars)
    d_t: FColVars = field(default_factory=FColVars)
    d_a: FColVars = field(default_factory=FColVars)

    d_e_hydrogen_reconv: FColVars = field(default_factory=FColVars)

    p: FColVars = field(default_factory=FColVars)
    p_petrol: FColVars = field(default_factory=FColVars)
    p_jetfuel: FColVars = field(default_factory=FColVars)
    p_diesel: FColVars = field(default_factory=FColVars)
    p_bioethanol: FColVars = field(default_factory=FColVars)
    p_biodiesel: FColVars = field(default_factory=FColVars)
    p_biogas: FColVars = field(default_factory=FColVars)
    p_emethan: FColVars = field(default_factory=FColVars)
    p_hydrogen: FColVars = field(default_factory=FColVars)
    p_hydrogen_reconv: FColVars = field(default_factory=FColVars)

    # erzeuge dictionry
    def dict(self):
        return asdict(self)


# Berechnungsfunktion Fuels 2018


def calc(inputs: Inputs, *, t18: transport2018.T18) -> F18:
    def fact(n):
        return inputs.fact(n)

    def entry(n):
        return inputs.entry(n)

    f18 = F18()

    # ------------------------------------------------
    f18.f.CO2e_cb = 0

    f18.d_r.energy = entry("In_R_petrol_fec")

    f18.d_b.energy = (
        entry("In_B_petrol_fec") + entry("In_B_jetfuel_fec") + entry("In_B_diesel_fec")
    )

    f18.d_i.energy = entry("In_I_diesel_fec")

    f18.d_t.energy = (
        t18.t.demand_petrol
        + t18.t.demand_jetfuel
        + t18.t.demand_diesel
        + t18.t.demand_biogas
        + t18.t.demand_bioethanol
        + t18.t.demand_biodiesel
    )

    f18.d_a.energy = entry("In_A_petrol_fec") + entry("In_A_diesel_fec")

    f18.d.energy = (
        f18.d_r.energy
        + f18.d_b.energy
        + f18.d_i.energy
        + f18.d_t.energy
        + f18.d_a.energy
    )

    f18.p_petrol.energy = (
        entry("In_R_petrol_fec")
        + entry("In_B_petrol_fec")
        + entry("In_A_petrol_fec")
        + t18.t.demand_petrol
    )
    f18.p_jetfuel.energy = entry("In_B_jetfuel_fec") + t18.s_jetfuel.energy
    f18.p_diesel.energy = (
        entry("In_B_diesel_fec")
        + entry("In_I_diesel_fec")
        + t18.t.demand_diesel
        + entry("In_A_diesel_fec")
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
