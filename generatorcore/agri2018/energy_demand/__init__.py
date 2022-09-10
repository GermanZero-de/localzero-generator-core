# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...lulucf2018.l18 import L18
from ...business2018.b18 import B18
from ...commonDataclasses.energy import Energy, EnergyWithPercentage
from ...commonDataclasses.co2eEmissions import CO2eEmissions

from .p import P
from .co2eFromFermentationOrManure import CO2eFromFermentationOrManure
from .co2eFromSoil import CO2eFromSoil
from .co2eFromOther import CO2eFromOther
from .operationHeatEnergy import OperationHeatEnergy


@dataclass(kw_only=True)
class Production:

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


def calc_production(
    inputs: Inputs,
    l18: L18,
    b18: B18,
    total_energy: float,
    s_elec_energy: float,
    s_petrol_energy: float,
    s_diesel_energy: float,
    s_fueloil_energy: float,
    s_lpg_energy: float,
    s_gas_energy: float,
    s_biomass_energy: float,
) -> Production:

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
        entries.a_soil_fertilizer_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_manure = CO2eFromSoil.calc(
        entries.a_soil_manure_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_sludge = CO2eFromSoil.calc(
        entries.a_soil_sludge_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_ecrop = CO2eFromSoil.calc(
        entries.a_soil_ecrop_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_residue = CO2eFromSoil.calc(
        entries.a_soil_residue_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )

    # grass land soil emissions
    # TODO: Fix spelling of grazing in entries
    p_soil_grazing = CO2eFromSoil.calc(
        entries.a_soil_crazing_ratio_CO2e_to_ha, area_ha=l18.g_grass.area_ha
    )

    # organic soil emissions
    p_soil_orgfarm = CO2eFromSoil.calc(
        entries.a_soil_orgfarm_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha
        + l18.g_crop_org_high.area_ha
        + l18.g_grass_org_low.area_ha
        + l18.g_grass_org_high.area_ha,
    )
    p_soil_orgloss = CO2eFromSoil.calc(
        entries.a_soil_orgloss_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha + l18.g_crop_org_high.area_ha,
    )

    # other soil emissions
    p_soil_leaching = CO2eFromSoil.calc(
        entries.a_soil_leaching_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    p_soil_deposition = CO2eFromSoil.calc(
        entries.a_soil_deposition_ratio_CO2e_to_ha,
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

    p_operation_elec_heatpump = Energy(energy=0)
    p_operation = Energy(energy=total_energy)
    p_operation_elec_elcon = EnergyWithPercentage.calc(
        energy=s_elec_energy, total_energy=p_operation.energy
    )
    p_operation_vehicles = EnergyWithPercentage.calc(
        energy=s_petrol_energy + s_diesel_energy, total_energy=p_operation.energy
    )
    p_operation_heat = OperationHeatEnergy.calc(
        inputs,
        b18,
        energy=s_fueloil_energy + s_lpg_energy + s_gas_energy + s_biomass_energy,
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
