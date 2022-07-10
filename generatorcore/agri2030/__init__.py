"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from .dataclasses import (
    CO2eChangeA,
    CO2eChangeG,
    CO2eChangeGConsult,
    CO2eChangeGOrganic,
)
from .energy_demand import (
    CO2eChangeP,
    CO2eChange,
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
from ..inputs import Inputs
from ..utils import div
from .. import agri2018, lulucf2030
from .a30 import A30


def calc(inputs: Inputs, *, a18: agri2018.A18, l30: lulucf2030.L30) -> A30:
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

    p_other_liming_calcit = CO2eChangeOther.calc_other(
        inputs,
        "p_other_liming_calcit",
        a18,
        "Ass_A_P_other_liming_calcit_amount_change",
        "Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018",
    )
    p_other_liming_dolomite = CO2eChangeOther.calc_other(
        inputs,
        "p_other_liming_dolomite",
        a18,
        "Ass_A_P_other_liming_dolomit_amount_change",
        "Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018",
    )
    p_other_urea = CO2eChangeOther.calc_other(
        inputs,
        "p_other_urea",
        a18,
        "Ass_A_P_other_urea_amount_change",
        "Fact_A_P_other_urea_CO2e_pb_to_amount_2018",
    )
    p_other_kas = CO2eChangeOther.calc_other(
        inputs,
        "p_other_kas",
        a18,
        "Ass_A_P_other_kas_amount_change",
        "Fact_A_P_other_kas_ratio_CO2e_pb_to_amount_2018",
    )
    p_other_ecrop = CO2eChangeOther.calc_other(
        inputs,
        "p_other_ecrop",
        a18,
        "Ass_A_P_other_ecrop_amount_change",
        "Fact_A_P_other_ecrop_ratio_CO2e_pb_to_amount_2018",
    )
    p_other_liming = CO2eChangeOtherLiming.calc_other_liming(
        inputs,
        "p_other_liming",
        a18,
        p_other_liming_calcit.prod_volume + p_other_liming_dolomite.prod_volume,
        p_other_liming_calcit.CO2e_production_based
        + p_other_liming_dolomite.CO2e_production_based,
    )

    p_fermen = CO2eChange.calc(
        inputs,
        "p_fermen",
        a18,
        0,
        p_fermen_dairycow.CO2e_production_based
        + p_fermen_nondairy.CO2e_production_based
        + p_fermen_swine.CO2e_production_based
        + p_fermen_poultry.CO2e_production_based
        + p_fermen_oanimal.CO2e_production_based,
    )
    p_manure = CO2eChange.calc(
        inputs,
        "p_manure",
        a18,
        0,
        p_manure_dairycow.CO2e_production_based
        + p_manure_nondairy.CO2e_production_based
        + p_manure_swine.CO2e_production_based
        + p_manure_poultry.CO2e_production_based
        + p_manure_oanimal.CO2e_production_based
        + p_manure_deposition.CO2e_production_based,
    )
    p_soil = CO2eChange.calc(
        inputs,
        "p_soil",
        a18,
        0,
        p_soil_fertilizer.CO2e_production_based
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
    p_other = CO2eChange.calc(
        inputs,
        "p_other",
        a18,
        0,
        p_other_liming.CO2e_production_based
        + p_other_urea.CO2e_production_based
        + p_other_kas.CO2e_production_based
        + p_other_ecrop.CO2e_production_based,
    )

    p_operation_heat = CO2eChangePOperationHeat.calc(inputs, "p_operation_heat", a18)

    p_operation_elec_elcon = CO2eChangePOperationElecElcon.calc(
        inputs, "p_operation_elec_elcon", a18
    )

    p_operation_elec_heatpump = CO2eChangePOperationElecHeatpump.calc(
        inputs, "p_operation_elec_heatpump", a18, p_operation_heat
    )

    p_operation_vehicles = CO2eChangePOperationVehicles.calc(
        inputs, "p_operation_vehicles", a18
    )

    p_operation = CO2eChangePOperation.calc(
        inputs,
        "p_operation",
        a18,
        p_operation_vehicles,
        p_operation_heat,
        p_operation_elec_elcon,
        p_operation_elec_heatpump,
    )

    p = CO2eChangeP.calc(
        inputs,
        "p",
        a18,
        p_operation,
        p_fermen.CO2e_production_based
        + p_manure.CO2e_production_based
        + p_soil.CO2e_production_based
        + p_other.CO2e_production_based,
        p_fermen.CO2e_total
        + p_manure.CO2e_total
        + p_soil.CO2e_total
        + p_other.CO2e_total,
    )

    s_petrol = CO2eChangeEnergyPerMWh.calc_energy(
        inputs, "s_petrol", a18, p_operation_vehicles.demand_epetrol
    )
    s_diesel = CO2eChangeEnergyPerMWh.calc_energy(
        inputs, "s_diesel", a18, p_operation_vehicles.demand_ediesel
    )
    s_lpg = CO2eChangeEnergyPerMWh.calc_energy(inputs, "s_lpg", a18, 0)
    s_biomass = CO2eChangeEnergyPerMWh.calc_energy(
        inputs, "s_biomass", a18, p_operation.demand_biomass
    )
    s_elec = CO2eChangeEnergyPerMWh.calc_energy(
        inputs, "s_elec", a18, p_operation.demand_electricity
    )
    s_fueloil = CO2eChangeFuelOilGas.calc_energy(inputs, "s_fueloil", a18, 0)
    s_gas = CO2eChangeFuelOilGas.calc_energy(inputs, "s_gas", a18, 0)
    s_heatpump = CO2eChangeFuelHeatpump.calc_energy(
        inputs, "s_heatpump", a18, p_operation.demand_heatpump
    )
    s_emethan = CO2eChangeFuelEmethan.calc_energy(
        inputs, a18, p_operation_heat.demand_emethan
    )

    g_consult = CO2eChangeGConsult.calc(inputs)
    g_organic = CO2eChangeGOrganic.calc(inputs)
    g = CO2eChangeG.calc(g_consult, g_organic)

    s = CO2eChangeS.calc_s(
        inputs,
        "s",
        a18,
        s_petrol,
        s_diesel,
        s_fueloil,
        s_lpg,
        s_gas,
        s_emethan,
        s_biomass,
        s_elec,
        s_heatpump,
    )

    a = CO2eChangeA.calc(inputs, "a", a18, p_operation, p, g, s)

    return A30(
        p_fermen_dairycow=p_fermen_dairycow,
        p_fermen_nondairy=p_fermen_nondairy,
        p_fermen_swine=p_fermen_swine,
        p_fermen_poultry=p_fermen_poultry,
        p_fermen_oanimal=p_fermen_oanimal,
        p_fermen=p_fermen,
        p_manure_dairycow=p_manure_dairycow,
        p_manure_nondairy=p_manure_nondairy,
        p_manure_swine=p_manure_swine,
        p_manure_poultry=p_manure_poultry,
        p_manure_oanimal=p_manure_oanimal,
        p_manure_deposition=p_manure_deposition,
        p_manure=p_manure,
        p_soil_fertilizer=p_soil_fertilizer,
        p_soil_manure=p_soil_manure,
        p_soil_sludge=p_soil_sludge,
        p_soil_ecrop=p_soil_ecrop,
        p_soil_residue=p_soil_residue,
        p_soil_grazing=p_soil_grazing,
        p_soil_orgfarm=p_soil_orgfarm,
        p_soil_orgloss=p_soil_orgloss,
        p_soil_leaching=p_soil_leaching,
        p_soil_deposition=p_soil_deposition,
        p_soil=p_soil,
        p_other_liming_calcit=p_other_liming_calcit,
        p_other_liming_dolomite=p_other_liming_dolomite,
        p_other_liming=p_other_liming,
        p_other_urea=p_other_urea,
        p_other_ecrop=p_other_ecrop,
        p_other_kas=p_other_kas,
        p_other=p_other,
        p_operation_elec_heatpump=p_operation_elec_heatpump,
        p_operation=p_operation,
        p_operation_elec_elcon=p_operation_elec_elcon,
        p_operation_vehicles=p_operation_vehicles,
        p_operation_heat=p_operation_heat,
        p=p,
        s_petrol=s_petrol,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biomass=s_biomass,
        s_elec=s_elec,
        s_heatpump=s_heatpump,
        s_emethan=s_emethan,
        s=s,
        a=a,
        g=g,
        g_consult=g_consult,
        g_organic=g_organic,
    )
