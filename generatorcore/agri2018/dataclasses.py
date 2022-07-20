# pyright: strict
from dataclasses import dataclass

from .. import business2018
from ..inputs import Inputs
from ..utils import div


@dataclass
class CO2eEmissions:
    # Used by a, p_fermen, p_manure, p_soil, p_other, p_other_liming
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float

    @classmethod
    def sum(cls, *co2es: "CO2eEmissions") -> "CO2eEmissions":
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in co2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in co2es),
            CO2e_total=sum(c.CO2e_total for c in co2es),
        )


@dataclass
class P:
    # TODO: What is a good name for this?
    # Used by p
    CO2e_production_based: float
    CO2e_total: float
    energy: float


@dataclass
class CO2eFromFermentationOrManure(CO2eEmissions):
    # Used by p_fermen_dairycow, p_fermen_nondairy, p_fermen_swine, p_fermen_poultry, p_fermen_oanimal, p_manure_dairycow, p_manure_nondairy, p_manure_swine, p_manure_poultry, p_manure_oanimal, p_manure_deposition
    CO2e_production_based_per_t: float
    amount: float

    @classmethod
    def calc_fermen(
        cls, inputs: Inputs, what: str, *, alias: str | None = None
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        # This line and the next might just be a little too cute.
        # They make the callsite nice and short, but forego any type checking
        # I'll keep it like this for now, but this is one of the places where
        # a better overall design is probably lurking somewhere
        CO2e_production_based_per_t = inputs.fact(
            "Fact_A_P_fermen_" + what + "_ratio_CO2e_to_amount_2018"
        )
        # Also don't ask me why we called swine swine except when we called them pig
        amount = getattr(
            inputs.entries, "a_fermen_" + (what if alias is None else alias) + "_amount"
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )

    @classmethod
    def calc_manure(
        cls, inputs: Inputs, what: str, *, amount: float
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = getattr(
            inputs.entries, "a_manure_" + what + "_ratio_CO2e_to_amount"
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )

    @classmethod
    def calc_deposition(
        cls,
        inputs: Inputs,
        *,
        p_fermen_dairycow: "CO2eFromFermentationOrManure",
        p_fermen_nondairy: "CO2eFromFermentationOrManure",
        p_fermen_swine: "CO2eFromFermentationOrManure",
        p_fermen_oanimal: "CO2eFromFermentationOrManure",
    ) -> "CO2eFromFermentationOrManure":
        """This computes the deposition of reactive nitrogen of animals (excluding poultry)"""

        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = (
            inputs.entries.a_manure_deposition_ratio_CO2e_to_amount
        )
        amount = (
            p_fermen_dairycow.amount
            + p_fermen_nondairy.amount
            + p_fermen_swine.amount
            + p_fermen_oanimal.amount
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )


@dataclass
class CO2eFromSoil(CO2eEmissions):
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


@dataclass
class CO2eFromOther(CO2eEmissions):
    # Used by p_other_liming_dolomite, p_other_urea, p_other_ecrop, p_other_liming_calcit
    CO2e_production_based_per_t: float
    prod_volume: float

    @classmethod
    def calc(
        cls, inputs: Inputs, what: str, *, ratio_suffix: str = "_ratio"
    ) -> "CO2eFromOther":
        # No idea why we use ratio_ with
        #   Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018
        # but not with
        #   Fact_A_P_other_urea_CO2e_pb_to_amount_2018
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = inputs.fact(
            "Fact_A_P_other_" + what + ratio_suffix + "_CO2e_pb_to_amount_2018"
        )
        prod_volume = getattr(inputs.entries, "a_other_" + what + "_prod_volume")
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            prod_volume=prod_volume,
        )


@dataclass
class Energy:
    # Used by p_operation, p_operation_elec_heatpump
    energy: float


@dataclass
class EnergyWithPercentage(Energy):
    # Used by p_operation_elec_elcon, p_operation_vehicles
    pct_energy: float

    @classmethod
    def calc(cls, *, energy: float, total_energy: float) -> "EnergyWithPercentage":
        return cls(energy=energy, pct_energy=div(energy, total_energy))


@dataclass
class OperationHeatEnergy(EnergyWithPercentage):
    # Used by p_operation_heat
    area_m2: float
    factor_adapted_to_fec: float

    @classmethod
    def calc(  # type: ignore
        cls, inputs: Inputs, b18: business2018.B18, energy: float, total_energy: float
    ):
        area_m2 = (
            b18.p_nonresi.area_m2
            * inputs.fact("Fact_A_P_energy_buildings_ratio_A_to_B")
            / (1 - inputs.fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
        )
        factor_adapted_to_fec = div(energy, area_m2)
        pct_energy = div(energy, total_energy)
        return cls(
            energy=energy,
            pct_energy=pct_energy,
            factor_adapted_to_fec=factor_adapted_to_fec,
            area_m2=area_m2,
        )


@dataclass
class CO2eFromEnergyUse(CO2eEmissions):
    # Used by s
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float
    energy: float

    @classmethod
    def sum(cls, *co2es: "CO2eFromEnergyUse") -> "CO2eFromEnergyUse":  # type: ignore
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in co2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in co2es),
            CO2e_total=sum(c.CO2e_total for c in co2es),
            energy=sum(c.energy for c in co2es),
        )


@dataclass
class CO2eFromEnergyUseDetail(CO2eFromEnergyUse):
    # TODO: Why are these called s_ ?
    # Used by s_petrol, s_diesel, s_fueloil, s_lpg, s_gas, s_biomass, s_elec, s_heatpump
    CO2e_combustion_based_per_MWh: float
    pct_energy: float

    @classmethod
    def calc(
        cls, *, energy: float, total_energy: float, CO2e_combustion_based_per_MWh: float
    ) -> "CO2eFromEnergyUseDetail":
        CO2e_production_based = 0.0
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
            energy=energy,
            pct_energy=div(energy, total_energy),
        )
