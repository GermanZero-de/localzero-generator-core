from dataclasses import dataclass, field

from . import transport2018
from .inputs import Inputs


@dataclass
class F:
    # Used by f
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class EnergyDemand:
    # Used by d, d_r, d_b, d_i, d_t, d_a
    energy: float


@dataclass
class FuelProduction:
    # Used by p_petrol, p_jetfuel, p_diesel, p_bioethanol, p_biodiesel, p_biogas
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    energy: float

    def __init__(self, energy: float, CO2e_production_based_per_MWh: float):
        self.CO2e_production_based_per_MWh = CO2e_production_based_per_MWh
        self.energy = energy
        self.CO2e_production_based = CO2e_production_based_per_MWh * energy
        self.CO2e_total = self.CO2e_production_based


@dataclass
class TotalFuelProduction:
    # Used by p
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore

    def __init__(self, *fuel_productions: FuelProduction):
        self.CO2e_production_based = sum(
            p.CO2e_production_based for p in fuel_productions
        )
        self.energy = sum(p.energy for p in fuel_productions)
        self.CO2e_total = self.CO2e_production_based


@dataclass
class F18:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
    p_petrol: FuelProduction
    p_jetfuel: FuelProduction
    p_diesel: FuelProduction
    p_bioethanol: FuelProduction
    p_biodiesel: FuelProduction
    p_biogas: FuelProduction

    p: TotalFuelProduction
    f: F


def calc(inputs: Inputs, *, t18: transport2018.T18) -> F18:
    """This computes the CO2e that is created by the production of fuels.
    NOTE: This does not compute the CO2e caused by burning fuels, those are in
    those sectors that make use of the fuels (transport, heat, ...).
    """
    fact = inputs.fact
    entries = inputs.entries
    # How does this work? It's very simple in make entries we already approximated
    # much of each fuel is used by the AGS in each sector (the total required by
    # each sector in Germany is known in the reference data).
    # So now we just determine the total amounts of each fuel and then multiply
    # by the "this is how much CO2e is emitted during production" factor.

    d_r = EnergyDemand(entries.r_petrol_fec)
    d_b = EnergyDemand(
        entries.b_petrol_fec + entries.b_jetfuel_fec + entries.b_diesel_fec
    )
    d_i = EnergyDemand(entries.i_diesel_fec)
    d_t = EnergyDemand(
        t18.t.demand_petrol
        + t18.t.demand_jetfuel
        + t18.t.demand_diesel
        + t18.t.demand_biogas
        + t18.t.demand_bioethanol
        + t18.t.demand_biodiesel
    )
    d_a = EnergyDemand(entries.a_petrol_fec + entries.a_diesel_fec)
    d = EnergyDemand(d_r.energy + d_b.energy + d_i.energy + d_t.energy + d_a.energy)

    p_petrol = FuelProduction(
        energy=entries.r_petrol_fec
        + entries.b_petrol_fec
        + entries.a_petrol_fec
        + t18.t.demand_petrol,
        CO2e_production_based_per_MWh=fact("Fact_F_P_petrol_ratio_CO2e_pb_to_fec_2018"),
    )
    p_jetfuel = FuelProduction(
        energy=entries.b_jetfuel_fec + t18.s_jetfuel.energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_F_P_jetfuel_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    p_diesel = FuelProduction(
        energy=(
            entries.b_diesel_fec
            + entries.i_diesel_fec
            + t18.t.demand_diesel
            + entries.a_diesel_fec
        ),
        CO2e_production_based_per_MWh=fact("Fact_F_P_diesel_ratio_CO2e_pb_to_fec_2018"),
    )
    p_bioethanol = FuelProduction(
        energy=t18.t.demand_bioethanol,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    p_biodiesel = FuelProduction(
        energy=t18.t.demand_biodiesel,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    p_biogas = FuelProduction(
        energy=t18.t.demand_biogas,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    p = TotalFuelProduction(
        p_petrol,
        p_jetfuel,
        p_diesel,
        p_bioethanol,
        p_biodiesel,
        p_biogas,
    )

    f = F(
        CO2e_combustion_based=0,
        CO2e_production_based=p.CO2e_production_based,
        CO2e_total=p.CO2e_total,
    )

    return F18(
        d_r=d_r,
        d_b=d_b,
        d_i=d_i,
        d_t=d_t,
        d_a=d_a,
        d=d,
        p_petrol=p_petrol,
        p_jetfuel=p_jetfuel,
        p_diesel=p_diesel,
        p_bioethanol=p_bioethanol,
        p_biodiesel=p_biodiesel,
        p_biogas=p_biogas,
        p=p,
        f=f,
    )
