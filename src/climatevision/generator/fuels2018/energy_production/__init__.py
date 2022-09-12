# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...transport2018.t18 import T18

from .fuelProduction import FuelProduction, TotalFuelProduction


@dataclass(kw_only=True)
class Production:
    petrol: FuelProduction
    jetfuel: FuelProduction
    diesel: FuelProduction
    bioethanol: FuelProduction
    biodiesel: FuelProduction
    biogas: FuelProduction

    total: TotalFuelProduction


def calc_production(inputs: Inputs, t18: T18) -> Production:

    entries = inputs.entries
    fact = inputs.fact

    petrol = FuelProduction(
        energy=entries.r_petrol_fec
        + entries.b_petrol_fec
        + entries.a_petrol_fec
        + t18.t.demand_petrol,
        CO2e_combustion_based_per_MWh=fact("Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018"),
    )
    jetfuel = FuelProduction(
        energy=entries.b_jetfuel_fec + t18.s_jetfuel.energy,
        CO2e_combustion_based_per_MWh=fact(
            "Fact_F_P_jetfuel_ratio_CO2e_cb_to_fec_2018"
        ),
    )
    diesel = FuelProduction(
        energy=(
            entries.b_diesel_fec
            + entries.i_diesel_fec
            + t18.t.demand_diesel
            + entries.a_diesel_fec
        ),
        CO2e_combustion_based_per_MWh=fact("Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018"),
    )
    bioethanol = FuelProduction(
        energy=t18.t.demand_bioethanol,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    biodiesel = FuelProduction(
        energy=t18.t.demand_biodiesel,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )
    biogas = FuelProduction(
        energy=t18.t.demand_biogas,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"
        ),
    )

    total = TotalFuelProduction(
        petrol,
        jetfuel,
        diesel,
        bioethanol,
        biodiesel,
        biogas,
    )

    return Production(
        petrol=petrol,
        jetfuel=jetfuel,
        diesel=diesel,
        bioethanol=bioethanol,
        biodiesel=biodiesel,
        biogas=biogas,
        total=total,
    )
