"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/fuel.html
"""

# pyright: strict

from ..inputs import Inputs
from ..transport2018.t18 import T18

from .f18 import F18
from .dataclasses import EnergyDemand, FuelProduction, TotalFuelProduction, F


def calc(inputs: Inputs, *, t18: T18) -> F18:
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

    d_r = EnergyDemand(energy=entries.r_petrol_fec)
    d_b = EnergyDemand(
        energy=entries.b_petrol_fec + entries.b_jetfuel_fec + entries.b_diesel_fec
    )
    d_i = EnergyDemand(energy=entries.i_diesel_fec)
    d_t = EnergyDemand(
        energy=t18.t.demand_petrol
        + t18.t.demand_jetfuel
        + t18.t.demand_diesel
        + t18.t.demand_biogas
        + t18.t.demand_bioethanol
        + t18.t.demand_biodiesel
    )
    d_a = EnergyDemand(energy=entries.a_petrol_fec + entries.a_diesel_fec)
    d = EnergyDemand(
        energy=d_r.energy + d_b.energy + d_i.energy + d_t.energy + d_a.energy
    )

    p_petrol = FuelProduction(
        energy=entries.r_petrol_fec
        + entries.b_petrol_fec
        + entries.a_petrol_fec
        + t18.t.demand_petrol,
        CO2e_combustion_based_per_MWh=fact("Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018"),
    )
    p_jetfuel = FuelProduction(
        energy=entries.b_jetfuel_fec + t18.s_jetfuel.energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_F_P_jetfuel_ratio_CO2e_cb_to_fec_2018"
        ),
    )
    p_diesel = FuelProduction(
        energy=(
            entries.b_diesel_fec
            + entries.i_diesel_fec
            + t18.t.demand_diesel
            + entries.a_diesel_fec
        ),
        CO2e_combustion_based_per_MWh=fact("Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018"),
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
        CO2e_combustion_based=p.CO2e_combustion_based,
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
