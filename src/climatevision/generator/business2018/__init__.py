"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/hh_ghd.html
"""

# pyright: strict

from ..makeentries import Entries
from ..refdata import Facts, Assumptions
from ..utils import div
from ..residences2018.r18 import R18
from ..common.co2_equivalent_emission import CO2eEmission
from ..common.energy_with_co2e import EnergyWithCO2e

from .b18 import B18
from . import energy_base, energy_demand, energy_source


# Berechnungsfunktion im Sektor GHD für 2018
def calc(entries: Entries, facts: Facts, assumptions: Assumptions, *, r18: R18) -> B18:
    energies = energy_base.calc(entries=entries, facts=facts)

    production = energy_demand.calc_production(entries, facts, assumptions, energies)

    building_energy_ratio = div(
        production.nonresi.number_of_buildings,
        production.nonresi.energy,
    )

    supply = energy_source.calc_supply(facts, energies, building_energy_ratio)

    b = CO2eEmission(
        CO2e_combustion_based=supply.total.CO2e_combustion_based,
        CO2e_production_based=0,
    )

    rb = EnergyWithCO2e(
        energy=r18.p.energy + production.total.energy,
        CO2e_combustion_based=r18.r.CO2e_combustion_based + b.CO2e_combustion_based,
    )

    return B18(
        b=b,
        p=production.total,
        p_nonresi=production.nonresi,
        p_nonresi_com=production.nonresi_commune,
        p_elec_elcon=production.elec_elcon,
        p_elec_heatpump=production.elec_heatpump,
        p_vehicles=production.vehicles,
        p_other=production.other,
        s=supply.total,
        s_gas=supply.gas,
        s_lpg=supply.lpg,
        s_petrol=supply.petrol,
        s_jetfuel=supply.jetfuel,
        s_diesel=supply.diesel,
        s_fueloil=supply.fueloil,
        s_biomass=supply.biomass,
        s_coal=supply.coal,
        s_heatnet=supply.heatnet,
        s_elec_heating=supply.elec_heating,
        s_heatpump=supply.heatpump,
        s_solarth=supply.solarth,
        s_elec=supply.elec,
        rb=rb,
    )
