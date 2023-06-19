# pyright: strict

from dataclasses import dataclass

from ...refdata import Facts


@dataclass(kw_only=True)
class BasicProductionBranch:
    energy: float
    prod_volume: float
    CO2e_combustion_based: float
    CO2e_production_based: float
    CO2e_total: float


@dataclass(kw_only=True)
class ProductionSubBranch(BasicProductionBranch):
    energy_use_factor: float
    CO2e_combustion_based_per_t: float
    CO2e_production_based_per_t: float

    @classmethod
    def calc_sub_branch_by_co2e(
        cls,
        facts: Facts,
        sub_branch: str,
        branch: str,
        co2e_sub_branch: float,
    ) -> "ProductionSubBranch":

        fact = facts.fact

        CO2e_total = co2e_sub_branch
        # calculate production volume from CO2e (with CO2e cb as this factor is > 0 for all industries)
        CO2e_combustion_based_per_t = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_cb_to_prodvol"
        )
        CO2e_production_based_per_t = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_pb_to_prodvol"
        )
        ratio_co2e_combustion_to_production_based = CO2e_combustion_based_per_t / (
            CO2e_combustion_based_per_t + CO2e_production_based_per_t
        )
        CO2e_combustion_based = CO2e_total * ratio_co2e_combustion_to_production_based
        CO2e_production_based = CO2e_total * (
            1 - ratio_co2e_combustion_to_production_based
        )
        production_volume = CO2e_combustion_based / CO2e_combustion_based_per_t

        energy_use_factor = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_prodvol_to_fec"
        )

        energy = production_volume / energy_use_factor

        return cls(
            energy=energy,
            prod_volume=production_volume,
            energy_use_factor=energy_use_factor,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
        )

    @classmethod
    def calc_sub_branch_by_energy(
        cls,
        facts: Facts,
        sub_branch: str,
        branch: str,
        energy_consumption_branch: float,
    ) -> "ProductionSubBranch":

        fact = facts.fact

        pct_energy = fact("Fact_I_P_" + branch + "_fec_pct_of_" + sub_branch)
        energy = energy_consumption_branch * pct_energy

        energy_use_factor = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_prodvol_to_fec"
        )
        production_volume = energy * energy_use_factor

        CO2e_combustion_based_per_t = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_cb_to_prodvol"
        )
        CO2e_combustion_based = production_volume * CO2e_combustion_based_per_t

        CO2e_production_based_per_t = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_pb_to_prodvol"
        )
        CO2e_production_based = production_volume * CO2e_production_based_per_t

        CO2e_total = CO2e_combustion_based + CO2e_production_based

        return cls(
            energy=energy,
            prod_volume=production_volume,
            energy_use_factor=energy_use_factor,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
        )


@dataclass(kw_only=True)
class ProductionSubBranchCO2viaFEC(BasicProductionBranch):
    """This class is only used by p_other_further as we were not able to determine a production volume for this quantitiy
    Therefore we set the prod_volume to 100% an and calculate the CO2e Emissiones via a Emmissions/Energy_consumption - Factor"""

    CO2e_combustion_based_per_MWh: float
    CO2e_production_based_per_MWh: float

    @classmethod
    def calc_sub_branch(
        cls,
        facts: Facts,
        sub_branch: str,
        branch: str,
        energy_consumption_branch: float,
    ) -> "ProductionSubBranchCO2viaFEC":

        fact = facts.fact

        pct_energy = fact("Fact_I_P_" + branch + "_fec_pct_of_" + sub_branch)
        energy = energy_consumption_branch * pct_energy

        production_volume = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_prodvol"
        )  # =1, meaning 100% see descritpion of Fact_I_P_other_further_prodvol this Fact for explanation

        CO2e_combustion_based_per_MWh = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_cb_to_fec"
        )
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_production_based_per_MWh = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_pb_to_fec"
        )
        CO2e_production_based = energy * CO2e_production_based_per_MWh

        CO2e_total = CO2e_combustion_based + CO2e_production_based

        return cls(
            energy=energy,
            prod_volume=production_volume,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )


@dataclass(kw_only=True)
class ExtraEmission:
    """This is only used by p_other_2efgh. We are adding some additional prouction based emissions as we so not include them in p_other_further."""

    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float

    @classmethod
    def calc_extra_emission(
        cls, facts: Facts, energy_consumption: float, branch: str, sub_branch: str
    ) -> "ExtraEmission":

        fact = facts.fact

        CO2e_production_based_per_MWh = fact(
            "Fact_I_P_" + branch + "_" + sub_branch + "_ratio_CO2e_pb_to_fec"
        )
        CO2e_production_based = energy_consumption * CO2e_production_based_per_MWh
        CO2e_total = CO2e_production_based

        return cls(
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
        )


@dataclass(kw_only=True)
class ProductionSum(BasicProductionBranch):
    @classmethod
    def sum(cls, *branches: BasicProductionBranch) -> "ProductionSum":

        energy = sum(branch.energy for branch in branches)
        prod_volume = sum(branch.prod_volume for branch in branches)
        CO2e_combustion_based = sum(branch.CO2e_combustion_based for branch in branches)
        CO2e_production_based = sum(branch.CO2e_production_based for branch in branches)
        CO2e_total = sum(branch.CO2e_total for branch in branches)

        return cls(
            energy=energy,
            prod_volume=prod_volume,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
        )


@dataclass(kw_only=True)
class ProductionBranch(BasicProductionBranch):
    @classmethod
    def sum(
        cls,
        sub_branch_list: list[ProductionSubBranch | ProductionSum],
        sub_branch_via_FEC_list: list[ProductionSubBranchCO2viaFEC] = [],
        extra_emission_list: list[ExtraEmission] = [],
    ) -> "ProductionBranch":

        energy = 0
        production_volume = 0
        CO2e_combustion_based = 0
        CO2e_production_based = 0
        CO2e_total = 0

        for sub_branch in sub_branch_list:
            energy += sub_branch.energy
            production_volume += sub_branch.prod_volume
            CO2e_combustion_based += sub_branch.CO2e_combustion_based
            CO2e_production_based += sub_branch.CO2e_production_based
            CO2e_total += sub_branch.CO2e_total

        if sub_branch_via_FEC_list is not []:
            for sub_branch in sub_branch_via_FEC_list:
                energy += sub_branch.energy
                CO2e_combustion_based += sub_branch.CO2e_combustion_based
                CO2e_production_based += sub_branch.CO2e_production_based
                CO2e_total += sub_branch.CO2e_total

        if extra_emission_list is not []:
            for extra_emission in extra_emission_list:
                CO2e_production_based += extra_emission.CO2e_production_based
                CO2e_total += extra_emission.CO2e_total

        return cls(
            energy=energy,
            prod_volume=production_volume,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
        )
