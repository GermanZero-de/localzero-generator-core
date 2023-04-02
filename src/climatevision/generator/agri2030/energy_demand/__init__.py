# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18
from ...lulucf2030.l30 import L30

from .co2e_change_agri import CO2eChangeAgri
from .co2e_change_p import CO2eChangeP
from .co2e_change_fermentation_or_manure import CO2eChangeFermentationOrManure
from .co2e_change_soil import CO2eChangeSoil
from .co2e_change_other_liming import CO2eChangeOtherLiming
from .co2e_change_other import CO2eChangeOther
from .energy_change_p_operation import EnergyChangePOperation
from .energy_change_p_operation_heat import EnergyChangePOperationHeat
from .energy_change_p_operation_elec_elcon import EnergyChangePOperationElecElcon
from .energy_change_p_operation_elec_heatpump import EnergyChangePOperationElecHeatpump
from .energy_change_p_operation_vehicles import EnergyChangePOperationVehicles


@dataclass(kw_only=True)
class Production:

    total: CO2eChangeP

    fermen: CO2eChangeAgri
    fermen_dairycow: CO2eChangeFermentationOrManure
    fermen_nondairy: CO2eChangeFermentationOrManure
    fermen_swine: CO2eChangeFermentationOrManure
    fermen_poultry: CO2eChangeFermentationOrManure
    fermen_oanimal: CO2eChangeFermentationOrManure

    manure: CO2eChangeAgri
    manure_dairycow: CO2eChangeFermentationOrManure
    manure_nondairy: CO2eChangeFermentationOrManure
    manure_swine: CO2eChangeFermentationOrManure
    manure_poultry: CO2eChangeFermentationOrManure
    manure_oanimal: CO2eChangeFermentationOrManure
    manure_deposition: CO2eChangeFermentationOrManure

    soil: CO2eChangeAgri
    soil_fertilizer: CO2eChangeSoil
    soil_manure: CO2eChangeSoil
    soil_sludge: CO2eChangeSoil
    soil_ecrop: CO2eChangeSoil
    soil_grazing: CO2eChangeSoil
    soil_residue: CO2eChangeSoil
    soil_orgfarm: CO2eChangeSoil
    soil_orgloss: CO2eChangeSoil
    soil_leaching: CO2eChangeSoil
    soil_deposition: CO2eChangeSoil

    other: CO2eChangeAgri
    other_liming: CO2eChangeOtherLiming
    other_liming_calcit: CO2eChangeOther
    other_liming_dolomite: CO2eChangeOther
    other_urea: CO2eChangeOther
    other_kas: CO2eChangeOther
    other_ecrop: CO2eChangeOther

    operation: EnergyChangePOperation
    operation_heat: EnergyChangePOperationHeat
    operation_elec_elcon: EnergyChangePOperationElecElcon
    operation_elec_heatpump: EnergyChangePOperationElecHeatpump
    operation_vehicles: EnergyChangePOperationVehicles


def calc_production(inputs: Inputs, a18: A18, l30: L30) -> Production:
    fermen_dairycow = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_dairycow", "Ass_A_P_fermen_dairycow_change", a18
    )
    fermen_nondairy = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_nondairy", "Ass_A_P_fermen_nondairy_change", a18
    )
    fermen_swine = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_swine", "Ass_A_P_fermen_swine_change", a18
    )
    fermen_poultry = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_poultry", "Ass_A_P_fermen_poultry_change", a18
    )
    fermen_oanimal = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_oanimal", "Ass_A_P_fermen_oanimal_change", a18
    )

    manure_dairycow = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_dairycow", a18, fermen_dairycow.amount
    )
    manure_nondairy = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_nondairy", a18, fermen_nondairy.amount
    )
    manure_swine = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_swine", a18, fermen_swine.amount
    )
    manure_poultry = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_poultry", a18, fermen_poultry.amount
    )
    manure_oanimal = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_oanimal", a18, fermen_oanimal.amount
    )
    manure_deposition = CO2eChangeFermentationOrManure.calc_manure(
        inputs,
        "p_manure_deposition",
        a18,
        fermen_dairycow.amount
        + fermen_nondairy.amount
        + fermen_swine.amount
        + fermen_oanimal.amount,
    )

    soil_fertilizer = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_fertilizer", a18, l30.g_crop.area_ha
    )
    soil_manure = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_manure", a18, l30.g_crop.area_ha
    )
    soil_sludge = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_sludge", a18, l30.g_crop.area_ha
    )
    soil_ecrop = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_ecrop", a18, l30.g_crop.area_ha
    )
    soil_grazing = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_grazing",
        a18,
        l30.g_grass.area_ha,
        div(
            a18.p_soil_grazing.CO2e_production_based_per_t
            * (fermen_dairycow.amount + fermen_nondairy.amount + fermen_oanimal.amount),
            a18.p_fermen_dairycow.amount
            + a18.p_fermen_nondairy.amount
            + a18.p_fermen_oanimal.amount,
        ),
    )
    soil_residue = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_residue",
        a18,
        l30.g_crop.area_ha,
        a18.p_soil_residue.CO2e_production_based_per_t,
    )
    soil_orgfarm = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_orgfarm",
        a18,
        l30.g_crop_org_low.area_ha
        + l30.g_crop_org_high.area_ha
        + l30.g_grass_org_low.area_ha
        + l30.g_grass_org_high.area_ha,
        a18.p_soil_orgfarm.CO2e_production_based_per_t,
    )
    soil_orgloss = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_orgloss",
        a18,
        l30.g_crop_org_low.area_ha + l30.g_crop_org_high.area_ha,
        a18.p_soil_orgloss.CO2e_production_based_per_t,
    )
    soil_leaching = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_leaching", a18, l30.g_crop.area_ha + l30.g_grass.area_ha
    )
    soil_deposition = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_deposition", a18, l30.g_crop.area_ha + l30.g_grass.area_ha
    )

    other_liming_calcit = CO2eChangeOther(
        inputs=inputs,
        what="p_other_liming_calcit",
        a18=a18,
        ass_demand_change="Ass_A_P_other_liming_calcit_amount_change",
        fact_production_based_per_t="Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    other_liming_dolomite = CO2eChangeOther(
        inputs=inputs,
        what="p_other_liming_dolomite",
        a18=a18,
        ass_demand_change="Ass_A_P_other_liming_dolomit_amount_change",
        fact_production_based_per_t="Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    other_urea = CO2eChangeOther(
        inputs=inputs,
        what="p_other_urea",
        a18=a18,
        ass_demand_change="Ass_A_P_other_urea_amount_change",
        fact_production_based_per_t="Fact_A_P_other_urea_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    other_kas = CO2eChangeOther(
        inputs=inputs,
        what="p_other_kas",
        a18=a18,
        ass_demand_change="Ass_A_P_other_kas_amount_change",
        fact_production_based_per_t="Fact_A_P_other_kas_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    other_ecrop = CO2eChangeOther(
        inputs=inputs,
        what="p_other_ecrop",
        a18=a18,
        ass_demand_change="Ass_A_P_other_ecrop_amount_change",
        fact_production_based_per_t="Fact_A_P_other_ecrop_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    other_liming = CO2eChangeOtherLiming(
        inputs=inputs,
        what="p_other_liming",
        a18=a18,
        prod_volume=other_liming_calcit.prod_volume + other_liming_dolomite.prod_volume,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=other_liming_calcit.CO2e_production_based
        + other_liming_dolomite.CO2e_production_based,
    )

    fermen = CO2eChangeAgri(
        inputs=inputs,
        what="p_fermen",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=fermen_dairycow.CO2e_production_based
        + fermen_nondairy.CO2e_production_based
        + fermen_swine.CO2e_production_based
        + fermen_poultry.CO2e_production_based
        + fermen_oanimal.CO2e_production_based,
    )
    manure = CO2eChangeAgri(
        inputs=inputs,
        what="p_manure",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=manure_dairycow.CO2e_production_based
        + manure_nondairy.CO2e_production_based
        + manure_swine.CO2e_production_based
        + manure_poultry.CO2e_production_based
        + manure_oanimal.CO2e_production_based
        + manure_deposition.CO2e_production_based,
    )
    soil = CO2eChangeAgri(
        inputs=inputs,
        what="p_soil",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=soil_fertilizer.CO2e_production_based
        + soil_manure.CO2e_production_based
        + soil_sludge.CO2e_production_based
        + soil_ecrop.CO2e_production_based
        + soil_grazing.CO2e_production_based
        + soil_residue.CO2e_production_based
        + soil_orgfarm.CO2e_production_based
        + soil_orgloss.CO2e_production_based
        + soil_leaching.CO2e_production_based
        + soil_deposition.CO2e_production_based,
    )
    other = CO2eChangeAgri(
        inputs=inputs,
        what="p_other",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=other_liming.CO2e_production_based
        + other_urea.CO2e_production_based
        + other_kas.CO2e_production_based
        + other_ecrop.CO2e_production_based,
    )

    operation_heat = EnergyChangePOperationHeat(
        inputs=inputs, what="p_operation_heat", a18=a18
    )

    operation_elec_elcon = EnergyChangePOperationElecElcon(
        inputs=inputs, what="p_operation_elec_elcon", a18=a18
    )

    operation_elec_heatpump = EnergyChangePOperationElecHeatpump(
        inputs=inputs,
        what="p_operation_elec_heatpump",
        a18=a18,
        operation_heat=operation_heat,
    )

    operation_vehicles = EnergyChangePOperationVehicles(
        inputs=inputs, what="p_operation_vehicles", a18=a18
    )

    operation = EnergyChangePOperation(
        inputs=inputs,
        what="p_operation",
        a18=a18,
        operation_vehicles=operation_vehicles,
        operation_heat=operation_heat,
        operation_elec_elcon=operation_elec_elcon,
        operation_elec_heatpump=operation_elec_heatpump,
    )

    total = CO2eChangeP(
        inputs=inputs,
        what="p",
        a18=a18,
        operation=operation,
        CO2e_production_based=fermen.CO2e_production_based
        + manure.CO2e_production_based
        + soil.CO2e_production_based
        + other.CO2e_production_based,
        CO2e_total=fermen.CO2e_total
        + manure.CO2e_total
        + soil.CO2e_total
        + other.CO2e_total,
    )

    return Production(
        total=total,
        fermen=fermen,
        fermen_dairycow=fermen_dairycow,
        fermen_nondairy=fermen_nondairy,
        fermen_swine=fermen_swine,
        fermen_poultry=fermen_poultry,
        fermen_oanimal=fermen_oanimal,
        manure=manure,
        manure_dairycow=manure_dairycow,
        manure_nondairy=manure_nondairy,
        manure_swine=manure_swine,
        manure_poultry=manure_poultry,
        manure_oanimal=manure_oanimal,
        manure_deposition=manure_deposition,
        soil=soil,
        soil_fertilizer=soil_fertilizer,
        soil_manure=soil_manure,
        soil_sludge=soil_sludge,
        soil_ecrop=soil_ecrop,
        soil_grazing=soil_grazing,
        soil_residue=soil_residue,
        soil_orgfarm=soil_orgfarm,
        soil_orgloss=soil_orgloss,
        soil_leaching=soil_leaching,
        soil_deposition=soil_deposition,
        other=other,
        other_liming=other_liming,
        other_liming_calcit=other_liming_calcit,
        other_liming_dolomite=other_liming_dolomite,
        other_urea=other_urea,
        other_kas=other_kas,
        other_ecrop=other_ecrop,
        operation=operation,
        operation_heat=operation_heat,
        operation_elec_elcon=operation_elec_elcon,
        operation_elec_heatpump=operation_elec_heatpump,
        operation_vehicles=operation_vehicles,
    )
