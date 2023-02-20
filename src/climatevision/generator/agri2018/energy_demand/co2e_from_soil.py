# pyright: strict

from dataclasses import dataclass

from ...common.co2_equivalent_emission import CO2eEmission


@dataclass(kw_only=True)
class CO2eFromSoil(CO2eEmission):
    # Used by p_soil_fertilizer, p_soil_manure, p_soil_sludge, p_soil_ecrop, p_soil_grazing, p_soil_residue, p_soil_orgfarm, p_soil_orgloss, p_soil_leaching, p_soil_deposition
    CO2e_production_based_per_t: float
    area_ha: float

    @classmethod
    def calc(cls, ratio_CO2e_to_ha: float, area_ha: float) -> "CO2eFromSoil":
        CO2e_combustion_based = 0.0
        # Huh? This line looks really odd.  Is that a we combined multiple different variables in the same spreadsheet column
        # modelling oddity?
        CO2e_production_based_per_t = ratio_CO2e_to_ha
        CO2e_production_based = area_ha * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            area_ha=area_ha,
        )
