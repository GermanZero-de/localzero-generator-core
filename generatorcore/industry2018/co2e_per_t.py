# pyright: strict
from dataclasses import InitVar, dataclass
from ..inputs import Inputs
from .co2e import CO2e


@dataclass
class CO2e_per_t(CO2e):
    # Used by p_miner_cement, p_miner_chalk, p_miner_glas, p_miner_ceram, p_chem_basic, p_chem_ammonia, p_chem_other, p_metal_steel_primary, p_metal_steel_secondary, p_metal_nonfe, p_other_paper, p_other_food
    CO2e_combustion_based_per_t: float = 0
    CO2e_production_based_per_t: float = 0
    energy_use_factor: float = 0
    pct_energy: float = 0

    inputs: InitVar[Inputs] = None  # type: ignore
    category_energy: InitVar[float] = 0
    fact_pct_energy: InitVar[str] = ""
    fact_CO2e_production_based_per_t: InitVar[str] = ""
    fact_CO2e_combustion_based_per_t: InitVar[str] = ""

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        category_energy: float,
        fact_pct_energy: str,
        fact_CO2e_production_based_per_t: str,
        fact_CO2e_combustion_based_per_t: str,
    ):
        self.pct_energy = inputs.fact(fact_pct_energy)
        self.energy = self.pct_energy * category_energy

        self.prod_volume = self.energy * self.energy_use_factor

        self.CO2e_production_based_per_t = inputs.fact(fact_CO2e_production_based_per_t)
        self.CO2e_combustion_based_per_t = inputs.fact(fact_CO2e_combustion_based_per_t)

        self.CO2e_production_based = self.prod_volume * self.CO2e_production_based_per_t
        self.CO2e_combustion_based = self.prod_volume * self.CO2e_combustion_based_per_t

        super().__post_init__()

    @classmethod
    def calc_p_miner_cement(
        cls, inputs: Inputs, category_energy: float
    ) -> "CO2e_per_t":
        energy_use_factor = inputs.fact("Fact_I_P_miner_cement_energy_use_factor_2017")

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_miner_fec_pct_of_cement_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_miner_cement_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_miner_cement_ratio_CO2e_cb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_miner_chalk(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = inputs.fact("Fact_I_P_miner_chalk_energy_use_factor_2017")

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_miner_fec_pct_of_chalk_2017",
            fact_CO2e_production_based_per_t="Fact_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_miner_glas(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = inputs.fact("Fact_I_P_miner_glas_energy_use_factor_2017")

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_miner_fec_pct_of_glas_2017",
            fact_CO2e_production_based_per_t="Fact_I_P_miner_glas_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_miner_glas_ratio_CO2e_cb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_miner_ceram(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = inputs.fact("Fact_I_P_miner_ceram_energy_use_factor_2017")

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_miner_fec_pct_of_ceram_2017",
            fact_CO2e_production_based_per_t="Fact_I_P_miner_ceram_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_miner_ceram_ratio_CO2e_cb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_chem_basic(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = inputs.fact(
            "Fact_I_P_chem_basic_wo_ammonia_ratio_prodvol_to_fec_2018"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_S_chem_basic_wo_ammonia_fec_ratio_to_chem_all_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_chem_basic_wo_ammonia_CO2e_pb_ratio_per_t_product_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_chem_basic_wo_ammonia_CO2e_eb_ratio_per_t_product_2018",
        )

    @classmethod
    def calc_p_chem_ammonia(
        cls, inputs: Inputs, category_energy: float
    ) -> "CO2e_per_t":
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_chem_ammonia_fec_ratio_per_t_product_2013"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_S_chem_ammonia_fec_ratio_to_chem_all_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_chem_ammonia_CO2e_pb_ratio_per_t_product_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_chem_ammonia_CO2e_eb_ratio_per_t_product_2018",
        )

    @classmethod
    def calc_p_chem_other(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = inputs.fact("Fact_I_P_chem_other_ratio_prodvol_to_fec_2018")

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_S_chem_other_fec_ratio_to_chem_all_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_chem_other_CO2e_pb_ratio_per_t_product_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_chem_other_CO2e_eb_ratio_per_t_product_2018",
        )

    @classmethod
    def calc_p_metal_steel_primary_route(
        cls, inputs: Inputs, category_energy: float
    ) -> "CO2e_per_t":
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_metal_steel_primary_ratio_fec_to_prodvol_2018"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fakt_I_N_metallh_Primaerroute_EEV_2018_Anteil",
            fact_CO2e_production_based_per_t="Fact_I_P_metal_steel_primary_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_metal_steel_primary_ratio_CO2e_eb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_metal_steel_secondary_route(
        cls, inputs: Inputs, category_energy: float
    ) -> "CO2e_per_t":
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_metal_steel_secondary_ratio_fec_to_prodvol_2018"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fakt_I_N_metallh_Sekundaerroute_EEV_2018_Anteil",
            fact_CO2e_production_based_per_t="Fact_I_P_metal_steel_secondary_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_metal_steel_secondary_ratio_CO2e_eb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_metal_non_fe(
        cls, inputs: Inputs, category_energy: float
    ) -> "CO2e_per_t":
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_metal_nonfe_ratio_fec_to_prodvol_2018"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_metal_fec_pct_of_nonfe_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_metal_nonfe_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_metal_nonfe_ratio_CO2e_cb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_other_paper(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_other_paper_ratio_fec_to_prodvol_2018"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_other_fec_pct_of_paper_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_other_paper_ratio_CO2e_cb_to_prodvol_2018",
        )

    @classmethod
    def calc_p_other_food(cls, inputs: Inputs, category_energy: float) -> "CO2e_per_t":
        energy_use_factor = 1 / inputs.fact(
            "Fact_I_P_other_food_ratio_fec_to_prodvol_2018"
        )

        return cls(
            energy_use_factor=energy_use_factor,
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_other_fec_pct_of_food_2018",
            fact_CO2e_production_based_per_t="Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol_2018",
            fact_CO2e_combustion_based_per_t="Fact_I_P_other_food_ratio_CO2e_cb_to_prodvol_2018",
        )
