# pyright: strict

from dataclasses import dataclass, field


from .dataclasses import (
    Vars0,
    CO2eChangeP,
    CO2eChangeG,
    CO2eChangeGConsult,
    CO2eChangeGOrganic,
    CO2eChange,
    CO2eChangeFermentationOrManure,
    CO2eChangeSoil,
    CO2eChangeOtherLiming,
    CO2eChangeOther,
    CO2eChangePOperation,
    CO2eChangePOperationHeat,
    CO2eChangePOperationElecElcon,
    CO2eChangePOperationElecHeatpump,
    Vars14,
    Vars15,
    CO2eChangeFuel,
    CO2eChangeFuelOilGas,
    CO2eChangeFuelHeatpump,
    CO2eChangeFuelEmethan,
)


@dataclass
class A30:
    a: Vars0 = field(default_factory=Vars0)
    p: CO2eChangeP = field(default_factory=CO2eChangeP)
    g: CO2eChangeG = field(default_factory=CO2eChangeG)
    g_consult: CO2eChangeGConsult = field(default_factory=CO2eChangeGConsult)
    g_organic: CO2eChangeGOrganic = field(default_factory=CO2eChangeGOrganic)
    p_fermen: CO2eChange = field(default_factory=CO2eChange)
    p_fermen_dairycow: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_fermen_nondairy: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_fermen_swine: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_fermen_poultry: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_fermen_oanimal: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_manure: CO2eChange = field(default_factory=CO2eChange)
    p_manure_dairycow: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_manure_nondairy: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_manure_swine: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_manure_poultry: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_manure_oanimal: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_manure_deposition: CO2eChangeFermentationOrManure = field(
        default_factory=CO2eChangeFermentationOrManure
    )
    p_soil: CO2eChange = field(default_factory=CO2eChange)
    p_soil_fertilizer: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_manure: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_sludge: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_ecrop: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_grazing: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_residue: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_orgfarm: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_orgloss: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_leaching: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_soil_deposition: CO2eChangeSoil = field(default_factory=CO2eChangeSoil)
    p_other: CO2eChange = field(default_factory=CO2eChange)
    p_other_liming: CO2eChangeOtherLiming = field(default_factory=CO2eChangeOtherLiming)
    p_other_liming_calcit: CO2eChangeOther = field(default_factory=CO2eChangeOther)
    p_other_liming_dolomite: CO2eChangeOther = field(default_factory=CO2eChangeOther)
    p_other_urea: CO2eChangeOther = field(default_factory=CO2eChangeOther)
    p_other_kas: CO2eChangeOther = field(default_factory=CO2eChangeOther)
    p_other_ecrop: CO2eChangeOther = field(default_factory=CO2eChangeOther)
    p_operation: CO2eChangePOperation = field(default_factory=CO2eChangePOperation)
    p_operation_heat: CO2eChangePOperationHeat = field(
        default_factory=CO2eChangePOperationHeat
    )
    p_operation_elec_elcon: CO2eChangePOperationElecElcon = field(
        default_factory=CO2eChangePOperationElecElcon
    )
    p_operation_elec_heatpump: CO2eChangePOperationElecHeatpump = field(
        default_factory=CO2eChangePOperationElecHeatpump
    )
    p_operation_vehicles: Vars14 = field(default_factory=Vars14)
    s: Vars15 = field(default_factory=Vars15)
    s_petrol: CO2eChangeFuel = field(default_factory=CO2eChangeFuel)
    s_diesel: CO2eChangeFuel = field(default_factory=CO2eChangeFuel)
    s_fueloil: CO2eChangeFuelOilGas = field(default_factory=CO2eChangeFuelOilGas)
    s_lpg: CO2eChangeFuel = field(default_factory=CO2eChangeFuel)
    s_gas: CO2eChangeFuelOilGas = field(default_factory=CO2eChangeFuelOilGas)
    s_biomass: CO2eChangeFuel = field(default_factory=CO2eChangeFuel)
    s_elec: CO2eChangeFuel = field(default_factory=CO2eChangeFuel)
    s_heatpump: CO2eChangeFuelHeatpump = field(default_factory=CO2eChangeFuelHeatpump)
    s_emethan: CO2eChangeFuelEmethan = field(default_factory=CO2eChangeFuelEmethan)
