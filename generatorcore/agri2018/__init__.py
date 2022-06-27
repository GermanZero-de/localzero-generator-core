# pyright: strict
from .. import business2018, lulucf2018
from ..inputs import Inputs

from .dataclasses import (
    CO2eEmissions,
    P,
    CO2eFromFermentationOrManure,
    CO2eFromSoil,
    CO2eFromOther,
    Energy,
    EnergyWithPercentage,
    OperationHeatEnergy,
    CO2eFromEnergyUse,
    CO2eFromEnergyUseDetail,
)
from .a18 import A18


def calc(inputs: Inputs, *, l18: lulucf2018.L18, b18: business2018.B18) -> A18:
    fact = inputs.fact
    entries = inputs.entries

    # Fermen
    p_fermen_dairycow = CO2eFromFermentationOrManure.calc_fermen(inputs, "dairycow")
    p_fermen_nondairy = CO2eFromFermentationOrManure.calc_fermen(inputs, "nondairy")
    p_fermen_swine = CO2eFromFermentationOrManure.calc_fermen(
        inputs, "swine", alias="pig"
    )
    p_fermen_poultry = CO2eFromFermentationOrManure.calc_fermen(inputs, "poultry")
    p_fermen_oanimal = CO2eFromFermentationOrManure.calc_fermen(inputs, "oanimal")

    p_fermen = CO2eEmissions.sum(
        p_fermen_dairycow,
        p_fermen_nondairy,
        p_fermen_swine,
        p_fermen_poultry,
        p_fermen_oanimal,
    )

    # Manure
    p_manure_dairycow = CO2eFromFermentationOrManure.calc_manure(
        inputs, "dairycow", amount=p_fermen_dairycow.amount
    )
    p_manure_nondairy = CO2eFromFermentationOrManure.calc_manure(
        inputs, "nondairy", amount=p_fermen_nondairy.amount
    )
    p_manure_swine = CO2eFromFermentationOrManure.calc_manure(
        inputs, "swine", amount=p_fermen_swine.amount
    )
    p_manure_poultry = CO2eFromFermentationOrManure.calc_manure(
        inputs, "poultry", amount=p_fermen_poultry.amount
    )
    p_manure_oanimal = CO2eFromFermentationOrManure.calc_manure(
        inputs, "oanimal", amount=p_fermen_oanimal.amount
    )
    p_manure_deposition = CO2eFromFermentationOrManure.calc_deposition(
        inputs,
        p_fermen_dairycow=p_fermen_dairycow,
        p_fermen_nondairy=p_fermen_nondairy,
        p_fermen_swine=p_fermen_swine,
        p_fermen_oanimal=p_fermen_oanimal,
    )
    p_manure = CO2eEmissions.sum(
        p_manure_dairycow,
        p_manure_nondairy,
        p_manure_swine,
        p_manure_poultry,
        p_manure_oanimal,
        p_manure_deposition,
    )

    # crop land soil emissions
    p_soil_fertilizer = CO2eFromSoil.calc(
        inputs.entries.a_soil_fertilizer_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_manure = CO2eFromSoil.calc(
        inputs.entries.a_soil_manure_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_sludge = CO2eFromSoil.calc(
        inputs.entries.a_soil_sludge_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_ecrop = CO2eFromSoil.calc(
        inputs.entries.a_soil_ecrop_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_residue = CO2eFromSoil.calc(
        inputs.entries.a_soil_residue_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )

    # grass land soil emissions
    # TODO: Fix spelling of grazing in entries
    p_soil_grazing = CO2eFromSoil.calc(
        inputs.entries.a_soil_crazing_ratio_CO2e_to_ha, area_ha=l18.g_grass.area_ha
    )

    # organic soil emissions
    p_soil_orgfarm = CO2eFromSoil.calc(
        inputs.entries.a_soil_orgfarm_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha
        + l18.g_crop_org_high.area_ha
        + l18.g_grass_org_low.area_ha
        + l18.g_grass_org_high.area_ha,
    )
    p_soil_orgloss = CO2eFromSoil.calc(
        inputs.entries.a_soil_orgloss_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha + l18.g_crop_org_high.area_ha,
    )

    # other soil emissions
    p_soil_leaching = CO2eFromSoil.calc(
        inputs.entries.a_soil_leaching_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    p_soil_deposition = CO2eFromSoil.calc(
        inputs.entries.a_soil_deposition_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    p_soil = CO2eEmissions.sum(
        p_soil_fertilizer,
        p_soil_manure,
        p_soil_sludge,
        p_soil_ecrop,
        p_soil_grazing,
        p_soil_residue,
        p_soil_orgfarm,
        p_soil_orgloss,
        p_soil_leaching,
        p_soil_deposition,
    )

    # Other
    p_other_liming_calcit = CO2eFromOther.calc(inputs, "liming_calcit")
    p_other_liming_dolomite = CO2eFromOther.calc(inputs, "liming_dolomite")
    p_other_liming = CO2eEmissions.sum(p_other_liming_calcit, p_other_liming_dolomite)

    p_other_urea = CO2eFromOther.calc(inputs, "urea", ratio_suffix="")
    p_other_ecrop = CO2eFromOther.calc(inputs, "ecrop")
    p_other_kas = CO2eFromOther.calc(inputs, "kas")

    p_other = CO2eEmissions.sum(
        p_other_liming, p_other_urea, p_other_kas, p_other_ecrop
    )

    # Energy
    total_energy = (
        entries.a_petrol_fec
        + entries.a_diesel_fec
        + entries.a_fueloil_fec
        + entries.a_lpg_fec
        + entries.a_gas_fec
        + entries.a_biomass_fec
        + entries.a_elec_fec
    )
    s_heatpump = CO2eFromEnergyUseDetail.calc(
        energy=0,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_heatpump_ratio_CO2e_to_fec"),
    )
    s_petrol = CO2eFromEnergyUseDetail.calc(
        energy=inputs.entries.a_petrol_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_T_S_petrol_EmFa_tank_wheel_2018"),
    )
    s_diesel = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_diesel_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_T_S_diesel_EmFa_tank_wheel_2018"),
    )
    s_fueloil = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_fueloil_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_fueloil_cb_EF"),
    )
    s_lpg = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_lpg_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_T_S_lpg_EmFa_tank_wheel_2018"),
    )
    s_gas = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_gas_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_H_P_ngas_cb_EF"),
    )
    s_biomass = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_biomass_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_biomass_CO2e_EF"),
    )
    s_elec = CO2eFromEnergyUseDetail.calc(
        energy=entries.a_elec_fec,
        total_energy=total_energy,
        CO2e_combustion_based_per_MWh=fact("Fact_RB_S_elec_ratio_CO2e_to_fec"),
    )
    s = CO2eFromEnergyUse.sum(
        s_petrol, s_diesel, s_fueloil, s_lpg, s_gas, s_biomass, s_elec
    )
    p_operation_elec_heatpump = Energy(0)
    p_operation = Energy(total_energy)
    p_operation_elec_elcon = EnergyWithPercentage.calc(
        energy=s_elec.energy, total_energy=p_operation.energy
    )
    p_operation_vehicles = EnergyWithPercentage.calc(
        energy=s_petrol.energy + s_diesel.energy, total_energy=p_operation.energy
    )
    p_operation_heat = OperationHeatEnergy.calc(
        inputs,
        b18,
        energy=s_fueloil.energy + s_lpg.energy + s_gas.energy + s_biomass.energy,
        total_energy=p_operation.energy,
    )
    p = P(
        CO2e_production_based=(
            p_fermen.CO2e_production_based
            + p_manure.CO2e_production_based
            + p_soil.CO2e_production_based
            + p_other.CO2e_production_based
        ),
        CO2e_total=(
            p_fermen.CO2e_total
            + p_manure.CO2e_total
            + p_soil.CO2e_total
            + p_other.CO2e_total
        ),
        energy=p_operation.energy,
    )
    a = CO2eEmissions(
        CO2e_total=p.CO2e_total + s.CO2e_total,
        CO2e_production_based=p.CO2e_production_based,
        CO2e_combustion_based=s.CO2e_combustion_based,
    )

    return A18(
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
        s=s,
        a=a,
    )
