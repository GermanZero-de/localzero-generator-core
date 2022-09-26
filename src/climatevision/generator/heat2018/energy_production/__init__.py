# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...transport2018.t18 import T18

from ..dataclasses import Vars4, Vars7


@dataclass(kw_only=True)
class Production:
    gas: Vars4
    opetpro: Vars4
    coal: Vars4
    heatnet_geoth: Vars7
    heatnet_lheatpump: Vars7


def calc_production(
    inputs: Inputs, t18: T18, p_energy: float, p_heatnet_energy: float
) -> Production:

    entries = inputs.entries
    fact = inputs.fact

    gas = Vars4(
        energy=entries.r_gas_fec
        + entries.b_gas_fec
        + entries.i_gas_fec
        + entries.a_gas_fec
        + t18.t.demand_gas,
        p_energy=p_energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
    )

    opetpro = Vars4(
        energy=entries.i_opetpro_fec,
        p_energy=p_energy,
        CO2e_production_based_per_MWh=fact(
            "Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018"
        ),
        CO2e_combustion_based_per_MWh=fact(
            "Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018"
        ),
    )

    coal = Vars4(
        energy=entries.r_coal_fec + entries.b_coal_fec + entries.i_coal_fec,
        p_energy=p_energy,
        CO2e_production_based_per_MWh=fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"),
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"),
    )

    heatnet_geoth = Vars7(p_heatnet_energy=p_heatnet_energy)

    heatnet_lheatpump = Vars7(p_heatnet_energy=p_heatnet_energy)

    return Production(
        gas=gas,
        opetpro=opetpro,
        coal=coal,
        heatnet_geoth=heatnet_geoth,
        heatnet_lheatpump=heatnet_lheatpump,
    )
