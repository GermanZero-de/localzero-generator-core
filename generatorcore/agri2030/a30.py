# pyright: strict

from dataclasses import dataclass, field


from .dataclasses import (
    Vars0,
    Vars1,
    Vars2,
    Vars3,
    Vars4,
    CO2eChange,
    CO2eChangeFermentationOrManure,
    CO2eChangeSoil,
    CO2eChangeOtherLiming,
    CO2eChangeOther,
    Vars10,
    Vars11,
    Vars12,
    Vars13,
    Vars14,
    Vars15,
    CO2eChangeFuel,
    CO2eChangeFuelOilGas,
    CO2eChangeFuelHeatpump,
    Vars19,
)


@dataclass
class A30:
    a: Vars0 = field(default_factory=Vars0)
    p: Vars1 = field(default_factory=Vars1)
    g: Vars2 = field(default_factory=Vars2)
    g_consult: Vars3 = field(default_factory=Vars3)
    g_organic: Vars4 = field(default_factory=Vars4)
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
    p_operation: Vars10 = field(default_factory=Vars10)
    p_operation_heat: Vars11 = field(default_factory=Vars11)
    p_operation_elec_elcon: Vars12 = field(default_factory=Vars12)
    p_operation_elec_heatpump: Vars13 = field(default_factory=Vars13)
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
    s_emethan: Vars19 = field(default_factory=Vars19)
