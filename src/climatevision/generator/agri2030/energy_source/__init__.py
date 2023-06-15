# pyright: strict
from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions
from ...agri2018.a18 import A18

from ..energy_demand import Production

from .co2e_change_s import CO2eChangeS
from .co2e_change_energy_per_mwh import CO2eChangeEnergyPerMWh
from .co2e_change_fuel_oil_gas import CO2eChangeFuelOilGas
from .co2e_change_fuel_heatpump import CO2eChangeFuelHeatpump
from .co2e_change_fuel_emethan import CO2eChangeFuelEmethan


@dataclass(kw_only=True)
class EnergySupply:
    total: CO2eChangeS
    petrol: CO2eChangeEnergyPerMWh
    diesel: CO2eChangeEnergyPerMWh
    fueloil: CO2eChangeFuelOilGas
    lpg: CO2eChangeEnergyPerMWh
    gas: CO2eChangeFuelOilGas
    biomass: CO2eChangeEnergyPerMWh
    elec: CO2eChangeEnergyPerMWh
    heatpump: CO2eChangeFuelHeatpump
    emethan: CO2eChangeFuelEmethan


def calc_supply(
    entries: Entries,
    facts: Facts,
    assumptions: Assumptions,
    a18: A18,
    production: Production,
) -> EnergySupply:

    petrol = CO2eChangeEnergyPerMWh(
        entries=entries,
        facts=facts,
        what="s_petrol",
        a18=a18,
        energy=production.operation_vehicles.demand_epetrol,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    diesel = CO2eChangeEnergyPerMWh(
        entries=entries,
        facts=facts,
        what="s_diesel",
        a18=a18,
        energy=production.operation_vehicles.demand_ediesel,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    lpg = CO2eChangeEnergyPerMWh(
        entries=entries,
        facts=facts,
        what="s_lpg",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    biomass = CO2eChangeEnergyPerMWh(
        entries=entries,
        facts=facts,
        what="s_biomass",
        a18=a18,
        energy=production.operation.demand_biomass,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    elec = CO2eChangeEnergyPerMWh(
        entries=entries,
        facts=facts,
        what="s_elec",
        a18=a18,
        energy=production.operation.demand_electricity,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    fueloil = CO2eChangeFuelOilGas(
        entries=entries,
        facts=facts,
        what="s_fueloil",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    gas = CO2eChangeFuelOilGas(
        entries=entries,
        facts=facts,
        what="s_gas",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    heatpump = CO2eChangeFuelHeatpump(
        entries=entries,
        facts=facts,
        assumptions=assumptions,
        what="s_heatpump",
        a18=a18,
        energy=production.operation.demand_heatpump,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    emethan = CO2eChangeFuelEmethan(
        entries=entries,
        facts=facts,
        what="",
        a18=a18,
        energy=production.operation_heat.demand_emethan,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )

    total = CO2eChangeS(
        entries=entries,
        facts=facts,
        what="s",
        a18=a18,
        petrol=petrol,
        diesel=diesel,
        fueloil=fueloil,
        lpg=lpg,
        gas=gas,
        emethan=emethan,
        biomass=biomass,
        elec=elec,
        heatpump=heatpump,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )

    return EnergySupply(
        total=total,
        petrol=petrol,
        diesel=diesel,
        fueloil=fueloil,
        lpg=lpg,
        gas=gas,
        biomass=biomass,
        elec=elec,
        heatpump=heatpump,
        emethan=emethan,
    )
