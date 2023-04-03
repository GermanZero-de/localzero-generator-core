# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div, MILLION

from ..dataclasses import Vars7

# from ..dataclasses import Vars5, Vars6, Vars8


@dataclass(kw_only=True)
class EnergySupply:
    # total: Vars5
    # gas: Vars6
    # lpg: Vars6
    # petrol: Vars6
    # jetfuel: Vars6
    # diesel: Vars6
    # fueloil: Vars6
    biomass: Vars7
    # coal: Vars6
    # heatnet: Vars6
    # elec_heating: Vars8
    # heatpump: Vars6
    # solarth: Vars6
    # elec: Vars8


def calc_supply(
    inputs: Inputs, total_energy: float, biomass_energy: float
) -> EnergySupply:

    fact = inputs.fact

    biomass = Vars7()
    biomass.energy = biomass_energy
    biomass.pct_energy = div(biomass_energy, total_energy)
    biomass.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
    biomass.cost_fuel = biomass.energy * biomass.cost_fuel_per_MWh / MILLION
    biomass.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    biomass.CO2e_combustion_based = (
        biomass.energy * biomass.CO2e_combustion_based_per_MWh
    )
    biomass.CO2e_total = biomass.CO2e_combustion_based

    return EnergySupply(
        # total=total,
        # gas=gas,
        # lpg=lpg,
        # petrol=petrol,
        # jetfuel=jetfuel,
        # diesel=diesel,
        # fueloil=fueloil,
        biomass=biomass,
        # coal=coal,
        # heatnet=heatnet,
        # elec_heating=elec_heating,
        # heatpump=heatpump,
        # solarth=solarth,
        # elec=elec,
    )
