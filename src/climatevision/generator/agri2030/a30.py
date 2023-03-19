# pyright: strict

from dataclasses import dataclass

from .energy_general import (
    CO2eChangeG,
    CO2eChangeGConsult,
    CO2eChangeGOrganic,
)
from .energy_demand import (
    CO2eChangeP,
    CO2eChangeAgri,
    CO2eChangeFermentationOrManure,
    CO2eChangeSoil,
    CO2eChangeOtherLiming,
    CO2eChangeOther,
    CO2eChangePOperation,
    CO2eChangePOperationHeat,
    CO2eChangePOperationElecElcon,
    CO2eChangePOperationElecHeatpump,
    CO2eChangePOperationVehicles,
)
from .energy_source import (
    CO2eChangeS,
    CO2eChangeEnergyPerMWh,
    CO2eChangeFuelOilGas,
    CO2eChangeFuelHeatpump,
    CO2eChangeFuelEmethan,
)
from .co2e_change_a import CO2eChangeA


@dataclass(kw_only=True)
class A30:
    a: CO2eChangeA

    g: CO2eChangeG
    g_consult: CO2eChangeGConsult
    g_organic: CO2eChangeGOrganic

    p: CO2eChangeP
    p_fermen: CO2eChangeAgri
    p_fermen_dairycow: CO2eChangeFermentationOrManure
    p_fermen_nondairy: CO2eChangeFermentationOrManure
    p_fermen_swine: CO2eChangeFermentationOrManure
    p_fermen_poultry: CO2eChangeFermentationOrManure
    p_fermen_oanimal: CO2eChangeFermentationOrManure
    p_manure: CO2eChangeAgri
    p_manure_dairycow: CO2eChangeFermentationOrManure
    p_manure_nondairy: CO2eChangeFermentationOrManure
    p_manure_swine: CO2eChangeFermentationOrManure
    p_manure_poultry: CO2eChangeFermentationOrManure
    p_manure_oanimal: CO2eChangeFermentationOrManure
    p_manure_deposition: CO2eChangeFermentationOrManure
    p_soil: CO2eChangeAgri
    p_soil_fertilizer: CO2eChangeSoil
    p_soil_manure: CO2eChangeSoil
    p_soil_sludge: CO2eChangeSoil
    p_soil_ecrop: CO2eChangeSoil
    p_soil_grazing: CO2eChangeSoil
    p_soil_residue: CO2eChangeSoil
    p_soil_orgfarm: CO2eChangeSoil
    p_soil_orgloss: CO2eChangeSoil
    p_soil_leaching: CO2eChangeSoil
    p_soil_deposition: CO2eChangeSoil
    p_other: CO2eChangeAgri
    p_other_liming: CO2eChangeOtherLiming
    p_other_liming_calcit: CO2eChangeOther
    p_other_liming_dolomite: CO2eChangeOther
    p_other_urea: CO2eChangeOther
    p_other_kas: CO2eChangeOther
    p_other_ecrop: CO2eChangeOther
    p_operation: CO2eChangePOperation
    p_operation_heat: CO2eChangePOperationHeat
    p_operation_elec_elcon: CO2eChangePOperationElecElcon
    p_operation_elec_heatpump: CO2eChangePOperationElecHeatpump
    p_operation_vehicles: CO2eChangePOperationVehicles

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
