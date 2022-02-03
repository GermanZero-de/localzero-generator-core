from .inputs import Inputs
from dataclasses import dataclass, asdict


#  Definition der relevanten Spaltennamen für den Sektor F (18)
@dataclass
class FColVars:

    energy: float = None
    CO2e_cb: float = None
    CO2e_pb: float = None
    CO2e_pb_per_MWh: float = None
    CO2e_total: float = None


@dataclass
class F18:
    f: FColVars = FColVars()
    g: FColVars = FColVars()
    d: FColVars = FColVars()
    d_r: FColVars = FColVars()
    d_b: FColVars = FColVars()
    d_i: FColVars = FColVars()
    d_t: FColVars = FColVars()
    d_a: FColVars = FColVars()

    d_e_hydrogen_reconv: FColVars = FColVars()

    p: FColVars = FColVars()
    p_petrol: FColVars = FColVars()
    p_jetfuel: FColVars = FColVars()
    p_diesel: FColVars = FColVars()
    p_bioethanol: FColVars = FColVars()
    p_biodiesel: FColVars = FColVars()
    p_biogas: FColVars = FColVars()
    p_emethan: FColVars = FColVars()
    p_hydrogen: FColVars = FColVars()
    p_hydrogen_reconv: FColVars = FColVars()

    # erzeuge dictionry
    def dict(self):
        return asdict(self)


# Berechnungsfunktion Fuels 2018


def calc(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    f = root.f18
    t18 = root.t18

    # ------------------------------------------------
    f.f.CO2e_cb = 0

    f.d_r.energy = entry("In_R_petrol_fec")

    f.d_b.energy = (
        entry("In_B_petrol_fec") + entry("In_B_jetfuel_fec") + entry("In_B_diesel_fec")
    )

    f.d_i.energy = entry("In_I_diesel_fec")

    f.d_t.energy = (
        t18.t.demand_petrol
        + t18.t.demand_jetfuel
        + t18.t.demand_diesel
        + t18.t.demand_biogas
        + t18.t.demand_bioethanol
        + t18.t.demand_biodiesel
    )

    f.d_a.energy = entry("In_A_petrol_fec") + entry("In_A_diesel_fec")

    f.d.energy = (
        f.d_r.energy + f.d_b.energy + f.d_i.energy + f.d_t.energy + f.d_a.energy
    )

    f.p_petrol.energy = (
        entry("In_R_petrol_fec")
        + entry("In_B_petrol_fec")
        + entry("In_A_petrol_fec")
        + root.t18.t.demand_petrol
    )
    f.p_jetfuel.energy = entry("In_B_jetfuel_fec") + root.t18.s_jetfuel.energy
    f.p_diesel.energy = (
        entry("In_B_diesel_fec")
        + entry("In_I_diesel_fec")
        + t18.t.demand_diesel
        + entry("In_A_diesel_fec")
    )
    f.p_bioethanol.energy = t18.t.demand_bioethanol
    f.p_biodiesel.energy = t18.t.demand_biodiesel
    f.p_biogas.energy = t18.t.demand_biogas

    f.p.energy = (
        f.p_petrol.energy
        + f.p_jetfuel.energy
        + f.p_diesel.energy
        + f.p_bioethanol.energy
        + f.p_biodiesel.energy
        + f.p_biogas.energy
    )
    # ------------------------------------
    f.p_petrol.CO2e_pb_per_MWh = fact("Fact_F_P_petrol_ratio_CO2e_pb_to_fec_2018")
    f.p_jetfuel.CO2e_pb_per_MWh = fact("Fact_F_P_jetfuel_ratio_CO2e_pb_to_fec_2018")
    f.p_diesel.CO2e_pb_per_MWh = fact("Fact_F_P_diesel_ratio_CO2e_pb_to_fec_2018")
    f.p_bioethanol.CO2e_pb_per_MWh = fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018")
    f.p_biodiesel.CO2e_pb_per_MWh = fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018")
    f.p_biogas.CO2e_pb_per_MWh = fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018")
    # -------------------------------------
    f.p_petrol.CO2e_pb = f.p_petrol.CO2e_pb_per_MWh * f.p_petrol.energy
    f.p_jetfuel.CO2e_pb = f.p_jetfuel.CO2e_pb_per_MWh * f.p_jetfuel.energy
    f.p_diesel.CO2e_pb = f.p_diesel.CO2e_pb_per_MWh * f.p_diesel.energy
    f.p_bioethanol.CO2e_pb = f.p_bioethanol.CO2e_pb_per_MWh * f.p_bioethanol.energy
    f.p_biodiesel.CO2e_pb = f.p_biodiesel.CO2e_pb_per_MWh * f.p_biodiesel.energy
    f.p_biogas.CO2e_pb = f.p_biogas.CO2e_pb_per_MWh * f.p_biogas.energy

    f.p.CO2e_pb = (
        f.p_petrol.CO2e_pb
        + f.p_jetfuel.CO2e_pb
        + f.p_diesel.CO2e_pb
        + f.p_bioethanol.CO2e_pb
        + f.p_biodiesel.CO2e_pb
        + f.p_biogas.CO2e_pb
    )  # SUM(p_petrol.CO2e_pb:p_biogas.CO2e_pb)

    f.f.CO2e_pb = f.p.CO2e_pb
    # --------------------------------------
    f.p_petrol.CO2e_total = f.p_petrol.CO2e_pb
    f.p_jetfuel.CO2e_total = f.p_jetfuel.CO2e_pb
    f.p_diesel.CO2e_total = f.p_diesel.CO2e_pb
    f.p_bioethanol.CO2e_total = f.p_bioethanol.CO2e_pb
    f.p_biodiesel.CO2e_total = f.p_biodiesel.CO2e_pb
    f.p_biogas.CO2e_total = f.p_biogas.CO2e_pb

    f.p.CO2e_total = (
        f.p_petrol.CO2e_total
        + f.p_jetfuel.CO2e_total
        + f.p_diesel.CO2e_total
        + f.p_bioethanol.CO2e_total
        + f.p_biodiesel.CO2e_total
        + f.p_biogas.CO2e_total
    )

    f.f.CO2e_total = f.p.CO2e_total
