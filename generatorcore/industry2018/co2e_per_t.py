# pyright: strict
from dataclasses import dataclass
from ..inputs import Inputs
from .co2e import CO2e


@dataclass
class CO2e_per_t(CO2e):
    # Used by p_miner_cement, p_miner_chalk, p_miner_glas, p_miner_ceram, p_chem_basic, p_chem_ammonia, p_chem_other, p_metal_steel_primary, p_metal_steel_secondary, p_metal_nonfe, p_other_paper, p_other_food
    CO2e_combustion_based_per_t: float = 0
    CO2e_production_based_per_t: float = 0
    energy_use_factor: float = 0
    pct_energy: float = 0

    @classmethod
    def calc_p_miner_cement(cls, inputs: Inputs, p_miner_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact("Fact_I_P_miner_fec_pct_of_cement_2018")
        energy = pct_energy * p_miner_energy
        energy_use_factor = inputs.fact("Fact_I_P_miner_cement_energy_use_factor_2017")
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_miner_cement_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_miner_cement_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_miner_chalk(cls, inputs: Inputs, p_miner_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact("Fact_I_P_miner_fec_pct_of_chalk_2017")
        energy = p_miner_energy * pct_energy
        energy_use_factor = inputs.fact("Fact_I_P_miner_chalk_energy_use_factor_2017")
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_miner_glas(cls, inputs: Inputs, p_miner_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact("Fact_I_P_miner_fec_pct_of_glas_2017")
        energy = p_miner_energy * pct_energy
        energy_use_factor = inputs.fact("Fact_I_P_miner_glas_energy_use_factor_2017")
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_miner_glas_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_miner_glas_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_miner_ceram(cls, inputs: Inputs, p_miner_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact("Fact_I_P_miner_fec_pct_of_ceram_2017")
        energy = p_miner_energy * pct_energy
        energy_use_factor = inputs.fact("Fact_I_P_miner_ceram_energy_use_factor_2017")
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_miner_ceram_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_miner_ceram_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_chem_basic(cls, inputs: Inputs, p_chem_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact(
            "Fact_I_S_chem_basic_wo_ammonia_fec_ratio_to_chem_all_2018"
        )
        energy = p_chem_energy * pct_energy
        energy_use_factor = inputs.fact(
            "Fact_I_P_chem_basic_wo_ammonia_ratio_prodvol_to_fec_2018"
        )
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_chem_basic_wo_ammonia_CO2e_pb_ratio_per_t_product_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_chem_basic_wo_ammonia_CO2e_eb_ratio_per_t_product_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_chem_ammonia(cls, inputs: Inputs, p_chem_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact("Fact_I_S_chem_ammonia_fec_ratio_to_chem_all_2018")
        energy = p_chem_energy * pct_energy
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_chem_ammonia_fec_ratio_per_t_product_2013"
        )
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_chem_ammonia_CO2e_pb_ratio_per_t_product_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_chem_ammonia_CO2e_eb_ratio_per_t_product_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_chem_other(cls, inputs: Inputs, p_chem_energy: float) -> "CO2e_per_t":
        pct_energy = inputs.fact("Fact_I_S_chem_other_fec_ratio_to_chem_all_2018")
        energy = p_chem_energy * pct_energy
        energy_use_factor = inputs.fact("Fact_I_P_chem_other_ratio_prodvol_to_fec_2018")
        prod_volume = energy * energy_use_factor
        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_chem_other_CO2e_pb_ratio_per_t_product_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_chem_other_CO2e_eb_ratio_per_t_product_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_metal_steel_primary_route(
        cls, inputs: Inputs, p_metal_steel_energy: float
    ) -> "CO2e_per_t":

        pct_energy = inputs.fact("Fakt_I_N_metallh_Primaerroute_EEV_2018_Anteil")
        energy = p_metal_steel_energy * pct_energy

        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_metal_steel_primary_ratio_fec_to_prodvol_2018"
        )
        prod_volume = energy * energy_use_factor

        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_metal_steel_primary_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t

        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_metal_steel_primary_ratio_CO2e_eb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_metal_steel_secondary_route(
        cls, inputs: Inputs, p_metal_steel_energy: float
    ) -> "CO2e_per_t":

        pct_energy = inputs.fact("Fakt_I_N_metallh_Sekundaerroute_EEV_2018_Anteil")
        energy = p_metal_steel_energy * pct_energy

        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_metal_steel_secondary_ratio_fec_to_prodvol_2018"
        )
        prod_volume = energy * energy_use_factor

        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_metal_steel_secondary_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t

        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_metal_steel_secondary_ratio_CO2e_eb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_metal_non_fe(cls, inputs: Inputs, p_metal_energy: float) -> "CO2e_per_t":

        pct_energy = inputs.fact("Fact_I_P_metal_fec_pct_of_nonfe_2018")
        energy = p_metal_energy * pct_energy

        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_metal_nonfe_ratio_fec_to_prodvol_2018"
        )
        prod_volume = energy * energy_use_factor

        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_metal_nonfe_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t

        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_metal_nonfe_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_other_paper(cls, inputs: Inputs, p_other_energy: float) -> "CO2e_per_t":

        pct_energy = inputs.fact("Fact_I_P_other_fec_pct_of_paper_2018")

        energy = p_other_energy * pct_energy
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_other_paper_ratio_fec_to_prodvol_2018"
        )
        prod_volume = energy * energy_use_factor

        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = CO2e_production_based_per_t * prod_volume

        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_other_paper_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )

    @classmethod
    def calc_p_other_food(cls, inputs: Inputs, p_other_energy: float) -> "CO2e_per_t":

        pct_energy = inputs.fact("Fact_I_P_other_fec_pct_of_food_2018")
        energy = p_other_energy * pct_energy
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_other_food_ratio_fec_to_prodvol_2018"
        )
        prod_volume = energy * energy_use_factor

        CO2e_production_based_per_t = inputs.fact(
            "Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol_2018"
        )
        CO2e_production_based = prod_volume * CO2e_production_based_per_t

        CO2e_combustion_based_per_t = inputs.fact(
            "Fact_I_P_other_food_ratio_CO2e_cb_to_prodvol_2018"
        )
        CO2e_combustion_based = prod_volume * CO2e_combustion_based_per_t

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_t=CO2e_combustion_based_per_t,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            energy=energy,
            energy_use_factor=energy_use_factor,
            pct_energy=pct_energy,
            prod_volume=prod_volume,
        )
