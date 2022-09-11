# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...utils import div
from ...agri2018.a18 import A18
from ...lulucf2030.l30 import L30

from .co2eChange import CO2eChange
from .co2eChangeP import CO2eChangeP
from .co2eChangeFermentationOrManure import CO2eChangeFermentationOrManure
from .co2eChangeSoil import CO2eChangeSoil
from .co2eChangeOtherLiming import CO2eChangeOtherLiming
from .co2eChangeOther import CO2eChangeOther
from .co2eChangePOperation import CO2eChangePOperation
from .co2eChangePOperationHeat import CO2eChangePOperationHeat
from .co2eChangePOperationElecElcon import CO2eChangePOperationElecElcon
from .co2eChangePOperationElecHeatpump import CO2eChangePOperationElecHeatpump
from .co2eChangePOperationVehicles import CO2eChangePOperationVehicles


@dataclass(kw_only=True)
class Production:

    p: CO2eChangeP

    p_fermen: CO2eChange
    p_fermen_dairycow: CO2eChangeFermentationOrManure
    p_fermen_nondairy: CO2eChangeFermentationOrManure
    p_fermen_swine: CO2eChangeFermentationOrManure
    p_fermen_poultry: CO2eChangeFermentationOrManure
    p_fermen_oanimal: CO2eChangeFermentationOrManure

    p_manure: CO2eChange
    p_manure_dairycow: CO2eChangeFermentationOrManure
    p_manure_nondairy: CO2eChangeFermentationOrManure
    p_manure_swine: CO2eChangeFermentationOrManure
    p_manure_poultry: CO2eChangeFermentationOrManure
    p_manure_oanimal: CO2eChangeFermentationOrManure
    p_manure_deposition: CO2eChangeFermentationOrManure

    p_soil: CO2eChange
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

    p_other: CO2eChange
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


def calc_production(inputs: Inputs, a18: A18, l30: L30) -> Production:
    p_fermen_dairycow = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_dairycow", "Ass_A_P_fermen_dairycow_change", a18
    )
    p_fermen_nondairy = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_nondairy", "Ass_A_P_fermen_nondairy_change", a18
    )
    p_fermen_swine = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_swine", "Ass_A_P_fermen_swine_change", a18
    )
    p_fermen_poultry = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_poultry", "Ass_A_P_fermen_poultry_change", a18
    )
    p_fermen_oanimal = CO2eChangeFermentationOrManure.calc_fermen(
        inputs, "p_fermen_oanimal", "Ass_A_P_fermen_oanimal_change", a18
    )

    p_manure_dairycow = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_dairycow", a18, p_fermen_dairycow.amount
    )
    p_manure_nondairy = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_nondairy", a18, p_fermen_nondairy.amount
    )
    p_manure_swine = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_swine", a18, p_fermen_swine.amount
    )
    p_manure_poultry = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_poultry", a18, p_fermen_poultry.amount
    )
    p_manure_oanimal = CO2eChangeFermentationOrManure.calc_manure(
        inputs, "p_manure_oanimal", a18, p_fermen_oanimal.amount
    )
    p_manure_deposition = CO2eChangeFermentationOrManure.calc_manure(
        inputs,
        "p_manure_deposition",
        a18,
        p_fermen_dairycow.amount
        + p_fermen_nondairy.amount
        + p_fermen_swine.amount
        + p_fermen_oanimal.amount,
    )

    p_soil_fertilizer = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_fertilizer", a18, l30.g_crop.area_ha
    )
    p_soil_manure = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_manure", a18, l30.g_crop.area_ha
    )
    p_soil_sludge = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_sludge", a18, l30.g_crop.area_ha
    )
    p_soil_ecrop = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_ecrop", a18, l30.g_crop.area_ha
    )
    p_soil_grazing = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_grazing",
        a18,
        l30.g_grass.area_ha,
        div(
            a18.p_soil_grazing.CO2e_production_based_per_t
            * (
                p_fermen_dairycow.amount
                + p_fermen_nondairy.amount
                + p_fermen_oanimal.amount
            ),
            a18.p_fermen_dairycow.amount
            + a18.p_fermen_nondairy.amount
            + a18.p_fermen_oanimal.amount,
        ),
    )
    p_soil_residue = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_residue",
        a18,
        l30.g_crop.area_ha,
        a18.p_soil_residue.CO2e_production_based_per_t,
    )
    p_soil_orgfarm = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_orgfarm",
        a18,
        l30.g_crop_org_low.area_ha
        + l30.g_crop_org_high.area_ha
        + l30.g_grass_org_low.area_ha
        + l30.g_grass_org_high.area_ha,
        a18.p_soil_orgfarm.CO2e_production_based_per_t,
    )
    p_soil_orgloss = CO2eChangeSoil.calc_soil_special(
        inputs,
        "p_soil_orgloss",
        a18,
        l30.g_crop_org_low.area_ha + l30.g_crop_org_high.area_ha,
        a18.p_soil_orgloss.CO2e_production_based_per_t,
    )
    p_soil_leaching = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_leaching", a18, l30.g_crop.area_ha + l30.g_grass.area_ha
    )
    p_soil_deposition = CO2eChangeSoil.calc_soil(
        inputs, "p_soil_deposition", a18, l30.g_crop.area_ha + l30.g_grass.area_ha
    )

    p_other_liming_calcit = CO2eChangeOther(
        inputs=inputs,
        what="p_other_liming_calcit",
        a18=a18,
        ass_demand_change="Ass_A_P_other_liming_calcit_amount_change",
        fact_production_based_per_t="Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    p_other_liming_dolomite = CO2eChangeOther(
        inputs=inputs,
        what="p_other_liming_dolomite",
        a18=a18,
        ass_demand_change="Ass_A_P_other_liming_dolomit_amount_change",
        fact_production_based_per_t="Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    p_other_urea = CO2eChangeOther(
        inputs=inputs,
        what="p_other_urea",
        a18=a18,
        ass_demand_change="Ass_A_P_other_urea_amount_change",
        fact_production_based_per_t="Fact_A_P_other_urea_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    p_other_kas = CO2eChangeOther(
        inputs=inputs,
        what="p_other_kas",
        a18=a18,
        ass_demand_change="Ass_A_P_other_kas_amount_change",
        fact_production_based_per_t="Fact_A_P_other_kas_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    p_other_ecrop = CO2eChangeOther(
        inputs=inputs,
        what="p_other_ecrop",
        a18=a18,
        ass_demand_change="Ass_A_P_other_ecrop_amount_change",
        fact_production_based_per_t="Fact_A_P_other_ecrop_ratio_CO2e_pb_to_amount_2018",
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    p_other_liming = CO2eChangeOtherLiming(
        inputs=inputs,
        what="p_other_liming",
        a18=a18,
        prod_volume=p_other_liming_calcit.prod_volume
        + p_other_liming_dolomite.prod_volume,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=p_other_liming_calcit.CO2e_production_based
        + p_other_liming_dolomite.CO2e_production_based,
    )

    p_fermen = CO2eChange(
        inputs=inputs,
        what="p_fermen",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=p_fermen_dairycow.CO2e_production_based
        + p_fermen_nondairy.CO2e_production_based
        + p_fermen_swine.CO2e_production_based
        + p_fermen_poultry.CO2e_production_based
        + p_fermen_oanimal.CO2e_production_based,
    )
    p_manure = CO2eChange(
        inputs=inputs,
        what="p_manure",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=p_manure_dairycow.CO2e_production_based
        + p_manure_nondairy.CO2e_production_based
        + p_manure_swine.CO2e_production_based
        + p_manure_poultry.CO2e_production_based
        + p_manure_oanimal.CO2e_production_based
        + p_manure_deposition.CO2e_production_based,
    )
    p_soil = CO2eChange(
        inputs=inputs,
        what="p_soil",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=p_soil_fertilizer.CO2e_production_based
        + p_soil_manure.CO2e_production_based
        + p_soil_sludge.CO2e_production_based
        + p_soil_ecrop.CO2e_production_based
        + p_soil_grazing.CO2e_production_based
        + p_soil_residue.CO2e_production_based
        + p_soil_orgfarm.CO2e_production_based
        + p_soil_orgloss.CO2e_production_based
        + p_soil_leaching.CO2e_production_based
        + p_soil_deposition.CO2e_production_based,
    )
    p_other = CO2eChange(
        inputs=inputs,
        what="p_other",
        a18=a18,
        CO2e_combustion_based=0,
        CO2e_production_based=p_other_liming.CO2e_production_based
        + p_other_urea.CO2e_production_based
        + p_other_kas.CO2e_production_based
        + p_other_ecrop.CO2e_production_based,
    )

    p_operation_heat = CO2eChangePOperationHeat(
        inputs=inputs, what="p_operation_heat", a18=a18
    )

    p_operation_elec_elcon = CO2eChangePOperationElecElcon(
        inputs=inputs, what="p_operation_elec_elcon", a18=a18
    )

    p_operation_elec_heatpump = CO2eChangePOperationElecHeatpump(
        inputs=inputs,
        what="p_operation_elec_heatpump",
        a18=a18,
        p_operation_heat=p_operation_heat,
    )

    p_operation_vehicles = CO2eChangePOperationVehicles(
        inputs=inputs, what="p_operation_vehicles", a18=a18
    )

    p_operation = CO2eChangePOperation(
        inputs=inputs,
        what="p_operation",
        a18=a18,
        p_operation_vehicles=p_operation_vehicles,
        p_operation_heat=p_operation_heat,
        p_operation_elec_elcon=p_operation_elec_elcon,
        p_operation_elec_heatpump=p_operation_elec_heatpump,
    )

    p = CO2eChangeP(
        inputs=inputs,
        what="p",
        a18=a18,
        p_operation=p_operation,
        CO2e_production_based=p_fermen.CO2e_production_based
        + p_manure.CO2e_production_based
        + p_soil.CO2e_production_based
        + p_other.CO2e_production_based,
        CO2e_total=p_fermen.CO2e_total
        + p_manure.CO2e_total
        + p_soil.CO2e_total
        + p_other.CO2e_total,
    )

    return Production(
        p=p,
        p_fermen=p_fermen,
        p_fermen_dairycow=p_fermen_dairycow,
        p_fermen_nondairy=p_fermen_nondairy,
        p_fermen_swine=p_fermen_swine,
        p_fermen_poultry=p_fermen_poultry,
        p_fermen_oanimal=p_fermen_oanimal,
        p_manure=p_manure,
        p_manure_dairycow=p_manure_dairycow,
        p_manure_nondairy=p_manure_nondairy,
        p_manure_swine=p_manure_swine,
        p_manure_poultry=p_manure_poultry,
        p_manure_oanimal=p_manure_oanimal,
        p_manure_deposition=p_manure_deposition,
        p_soil=p_soil,
        p_soil_fertilizer=p_soil_fertilizer,
        p_soil_manure=p_soil_manure,
        p_soil_sludge=p_soil_sludge,
        p_soil_ecrop=p_soil_ecrop,
        p_soil_grazing=p_soil_grazing,
        p_soil_residue=p_soil_residue,
        p_soil_orgfarm=p_soil_orgfarm,
        p_soil_orgloss=p_soil_orgloss,
        p_soil_leaching=p_soil_leaching,
        p_soil_deposition=p_soil_deposition,
        p_other=p_other,
        p_other_liming=p_other_liming,
        p_other_liming_calcit=p_other_liming_calcit,
        p_other_liming_dolomite=p_other_liming_dolomite,
        p_other_urea=p_other_urea,
        p_other_kas=p_other_kas,
        p_other_ecrop=p_other_ecrop,
        p_operation=p_operation,
        p_operation_heat=p_operation_heat,
        p_operation_elec_elcon=p_operation_elec_elcon,
        p_operation_elec_heatpump=p_operation_elec_heatpump,
        p_operation_vehicles=p_operation_vehicles,
    )
