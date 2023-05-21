# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...lulucf2018.l18 import L18
from ...business2018.b18 import B18
from ...common.energy import Energy, EnergyPerM2
from ...common.co2_equivalent_emission import CO2eEmission

from ..energy_base import Energies

from .p import P
from .co2e_from_fermentation_or_manure import CO2eFromFermentationOrManure
from .co2e_from_soil import CO2eFromSoil
from .co2e_from_other import CO2eFromOther


@dataclass(kw_only=True)
class Production:

    total: P

    fermen: CO2eEmission
    fermen_dairycow: CO2eFromFermentationOrManure
    fermen_nondairy: CO2eFromFermentationOrManure
    fermen_swine: CO2eFromFermentationOrManure
    fermen_poultry: CO2eFromFermentationOrManure
    fermen_oanimal: CO2eFromFermentationOrManure

    manure: CO2eEmission
    manure_dairycow: CO2eFromFermentationOrManure
    manure_nondairy: CO2eFromFermentationOrManure
    manure_swine: CO2eFromFermentationOrManure
    manure_poultry: CO2eFromFermentationOrManure
    manure_oanimal: CO2eFromFermentationOrManure
    manure_deposition: CO2eFromFermentationOrManure

    soil: CO2eEmission
    soil_fertilizer: CO2eFromSoil
    soil_manure: CO2eFromSoil
    soil_sludge: CO2eFromSoil
    soil_ecrop: CO2eFromSoil
    soil_grazing: CO2eFromSoil
    soil_residue: CO2eFromSoil
    soil_orgfarm: CO2eFromSoil
    soil_orgloss: CO2eFromSoil
    soil_leaching: CO2eFromSoil
    soil_deposition: CO2eFromSoil

    other: CO2eEmission
    other_liming_dolomite: CO2eFromOther
    other_urea: CO2eFromOther
    other_ecrop: CO2eFromOther
    other_liming: CO2eEmission
    other_liming_calcit: CO2eFromOther
    other_kas: CO2eFromOther

    operation: Energy
    operation_heat: EnergyPerM2
    operation_elec_elcon: Energy
    operation_elec_heatpump: Energy
    operation_vehicles: Energy


def calc_production(
    inputs: Inputs, l18: L18, b18: B18, energies: Energies
) -> Production:

    entries = inputs.entries

    # Fermen
    fermen_dairycow = CO2eFromFermentationOrManure.calc_fermen(inputs, "dairycow")
    fermen_nondairy = CO2eFromFermentationOrManure.calc_fermen(inputs, "nondairy")
    fermen_swine = CO2eFromFermentationOrManure.calc_fermen(
        inputs, "swine", alias="pig"
    )
    fermen_poultry = CO2eFromFermentationOrManure.calc_fermen(inputs, "poultry")
    fermen_oanimal = CO2eFromFermentationOrManure.calc_fermen(inputs, "oanimal")

    fermen = CO2eEmission.sum(
        fermen_dairycow,
        fermen_nondairy,
        fermen_swine,
        fermen_poultry,
        fermen_oanimal,
    )

    # Manure
    manure_dairycow = CO2eFromFermentationOrManure.calc_manure(
        inputs, "dairycow", amount=fermen_dairycow.amount
    )
    manure_nondairy = CO2eFromFermentationOrManure.calc_manure(
        inputs, "nondairy", amount=fermen_nondairy.amount
    )
    manure_swine = CO2eFromFermentationOrManure.calc_manure(
        inputs, "swine", amount=fermen_swine.amount
    )
    manure_poultry = CO2eFromFermentationOrManure.calc_manure(
        inputs, "poultry", amount=fermen_poultry.amount
    )
    manure_oanimal = CO2eFromFermentationOrManure.calc_manure(
        inputs, "oanimal", amount=fermen_oanimal.amount
    )
    manure_deposition = CO2eFromFermentationOrManure.calc_deposition(
        inputs,
        fermen_dairycow=fermen_dairycow,
        fermen_nondairy=fermen_nondairy,
        fermen_swine=fermen_swine,
        fermen_oanimal=fermen_oanimal,
    )
    manure = CO2eEmission.sum(
        manure_dairycow,
        manure_nondairy,
        manure_swine,
        manure_poultry,
        manure_oanimal,
        manure_deposition,
    )

    # crop land soil emissions
    soil_fertilizer = CO2eFromSoil.calc(
        entries.a_soil_fertilizer_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    soil_manure = CO2eFromSoil.calc(
        entries.a_soil_manure_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    soil_sludge = CO2eFromSoil.calc(
        entries.a_soil_sludge_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    soil_ecrop = CO2eFromSoil.calc(
        entries.a_soil_ecrop_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    soil_residue = CO2eFromSoil.calc(
        entries.a_soil_residue_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )

    # grass land soil emissions
    # TODO: Fix spelling of grazing in entries
    soil_grazing = CO2eFromSoil.calc(
        entries.a_soil_crazing_ratio_CO2e_to_ha, area_ha=l18.g_grass.area_ha
    )

    # organic soil emissions
    soil_orgfarm = CO2eFromSoil.calc(
        entries.a_soil_orgfarm_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha
        + l18.g_crop_org_high.area_ha
        + l18.g_grass_org_low.area_ha
        + l18.g_grass_org_high.area_ha,
    )
    soil_orgloss = CO2eFromSoil.calc(
        entries.a_soil_orgloss_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha + l18.g_crop_org_high.area_ha,
    )

    # other soil emissions
    soil_leaching = CO2eFromSoil.calc(
        entries.a_soil_leaching_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    soil_deposition = CO2eFromSoil.calc(
        entries.a_soil_deposition_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    soil = CO2eEmission.sum(
        soil_fertilizer,
        soil_manure,
        soil_sludge,
        soil_ecrop,
        soil_grazing,
        soil_residue,
        soil_orgfarm,
        soil_orgloss,
        soil_leaching,
        soil_deposition,
    )

    # Other
    other_liming_calcit = CO2eFromOther.calc(inputs, "liming_calcit")
    other_liming_dolomite = CO2eFromOther.calc(inputs, "liming_dolomite")
    other_liming = CO2eEmission.sum(other_liming_calcit, other_liming_dolomite)

    other_urea = CO2eFromOther.calc(inputs, "urea", ratio_suffix="")
    other_ecrop = CO2eFromOther.calc(inputs, "ecrop")
    other_kas = CO2eFromOther.calc(inputs, "kas")

    other = CO2eEmission.sum(other_liming, other_urea, other_kas, other_ecrop)

    operation_elec_heatpump = Energy(energy=0)
    operation_elec_elcon = Energy(energy=energies.elec.energy)
    operation_vehicles = Energy(energy=energies.petrol.energy + energies.diesel.energy)
    operation_heat = EnergyPerM2(
        energy=energies.fueloil.energy
        + energies.lpg.energy
        + energies.gas.energy
        + energies.biomass.energy,
        area_m2=(
            b18.p_nonresi.area_m2
            * inputs.fact("Fact_A_P_energy_buildings_ratio_A_to_B")
            / (1 - inputs.fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
        ),
    )

    operation = Energy(
        energy=energies.petrol.energy
        + energies.diesel.energy
        + energies.fueloil.energy
        + energies.lpg.energy
        + energies.gas.energy
        + energies.biomass.energy
        + energies.elec.energy
    )

    total = P(
        CO2e_production_based=(
            fermen.CO2e_production_based
            + manure.CO2e_production_based
            + soil.CO2e_production_based
            + other.CO2e_production_based
        ),
        CO2e_total=(
            fermen.CO2e_total + manure.CO2e_total + soil.CO2e_total + other.CO2e_total
        ),
        energy=operation.energy,
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
