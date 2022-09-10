# pyright: strict

from dataclasses import dataclass

from ..commonDataclasses.co2eEmissions import CO2eEmissions

from .energy_demand import (
    P,
    CO2eFromFermentationOrManure,
    CO2eFromSoil,
    CO2eFromOther,
    Energy,
    EnergyWithPercentage,
    OperationHeatEnergy,
)
from .energy_source import CO2eFromEnergyUse, CO2eFromEnergyUseDetail


@dataclass(kw_only=True)
class A18:
    a: CO2eEmissions
    p: P
    p_fermen: CO2eEmissions
    p_fermen_dairycow: CO2eFromFermentationOrManure
    p_fermen_nondairy: CO2eFromFermentationOrManure
    p_fermen_swine: CO2eFromFermentationOrManure
    p_fermen_poultry: CO2eFromFermentationOrManure
    p_fermen_oanimal: CO2eFromFermentationOrManure
    p_manure: CO2eEmissions
    p_manure_dairycow: CO2eFromFermentationOrManure
    p_manure_nondairy: CO2eFromFermentationOrManure
    p_manure_swine: CO2eFromFermentationOrManure
    p_manure_poultry: CO2eFromFermentationOrManure
    p_manure_oanimal: CO2eFromFermentationOrManure
    p_manure_deposition: CO2eFromFermentationOrManure
    p_soil: CO2eEmissions
    p_soil_fertilizer: CO2eFromSoil
    p_soil_manure: CO2eFromSoil
    p_soil_sludge: CO2eFromSoil
    p_soil_ecrop: CO2eFromSoil
    p_soil_grazing: CO2eFromSoil
    p_soil_residue: CO2eFromSoil
    p_soil_orgfarm: CO2eFromSoil
    p_soil_orgloss: CO2eFromSoil
    p_soil_leaching: CO2eFromSoil
    p_soil_deposition: CO2eFromSoil
    p_other: CO2eEmissions
    p_other_liming_dolomite: CO2eFromOther
    p_other_urea: CO2eFromOther
    p_other_ecrop: CO2eFromOther
    p_other_liming: CO2eEmissions
    p_other_liming_calcit: CO2eFromOther
    p_other_kas: CO2eFromOther
    p_operation: Energy
    p_operation_heat: OperationHeatEnergy
    p_operation_elec_elcon: EnergyWithPercentage
    p_operation_elec_heatpump: Energy
    p_operation_vehicles: EnergyWithPercentage
    s: CO2eFromEnergyUse
    s_petrol: CO2eFromEnergyUseDetail
    s_diesel: CO2eFromEnergyUseDetail
    s_fueloil: CO2eFromEnergyUseDetail
    s_lpg: CO2eFromEnergyUseDetail
    s_gas: CO2eFromEnergyUseDetail
    s_biomass: CO2eFromEnergyUseDetail
    s_elec: CO2eFromEnergyUseDetail
    s_heatpump: CO2eFromEnergyUseDetail
