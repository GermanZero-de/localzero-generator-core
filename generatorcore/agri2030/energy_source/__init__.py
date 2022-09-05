# pyright: strict
from dataclasses import dataclass

from ...inputs import Inputs
from ...agri2018.a18 import A18

from ..energy_demand import Production

from .co2eChangeS import CO2eChangeS
from .co2eChangeEnergyPerMWh import CO2eChangeEnergyPerMWh
from .co2eChangeFuelOilGas import CO2eChangeFuelOilGas
from .co2eChangeFuelHeatpump import CO2eChangeFuelHeatpump
from .co2eChangeFuelEmethan import CO2eChangeFuelEmethan


@dataclass(kw_only=True)
class EnergySupply:
    s: CO2eChangeS
    s_petrol: CO2eChangeEnergyPerMWh
    s_diesel: CO2eChangeEnergyPerMWh
    s_fueloil: CO2eChangeFuelOilGas
    s_lpg: CO2eChangeEnergyPerMWh
    s_gas: CO2eChangeFuelOilGas
    s_biomass: CO2eChangeEnergyPerMWh
    s_elec: CO2eChangeEnergyPerMWh
    s_heatpump: CO2eChangeFuelHeatpump
    s_emethan: CO2eChangeFuelEmethan


def calc_supply(inputs: Inputs, a18: A18, production: Production) -> EnergySupply:

    s_petrol = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_petrol",
        a18=a18,
        energy=production.p_operation_vehicles.demand_epetrol,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_diesel = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_diesel",
        a18=a18,
        energy=production.p_operation_vehicles.demand_ediesel,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_lpg = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_lpg",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_biomass = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_biomass",
        a18=a18,
        energy=production.p_operation.demand_biomass,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_elec = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_elec",
        a18=a18,
        energy=production.p_operation.demand_electricity,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_fueloil = CO2eChangeFuelOilGas(
        inputs=inputs,
        what="s_fueloil",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_gas = CO2eChangeFuelOilGas(
        inputs=inputs,
        what="s_gas",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_heatpump = CO2eChangeFuelHeatpump(
        inputs=inputs,
        what="s_heatpump",
        a18=a18,
        energy=production.p_operation.demand_heatpump,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_emethan = CO2eChangeFuelEmethan(
        inputs=inputs,
        what="",
        a18=a18,
        energy=production.p_operation_heat.demand_emethan,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )

    s = CO2eChangeS(
        inputs=inputs,
        what="s",
        a18=a18,
        s_petrol=s_petrol,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_emethan=s_emethan,
        s_biomass=s_biomass,
        s_elec=s_elec,
        s_heatpump=s_heatpump,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )

    return EnergySupply(
        s=s,
        s_petrol=s_petrol,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biomass=s_biomass,
        s_elec=s_elec,
        s_heatpump=s_heatpump,
        s_emethan=s_emethan,
    )
