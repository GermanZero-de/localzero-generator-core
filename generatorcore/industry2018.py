from dataclasses import dataclass, field, asdict
from .inputs import Inputs
from .utils import div


@dataclass
class Vars0:
    # Used by i, p, p_miner, p_chem, p_metal, p_other
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars1:
    # Used s_renew_hydrogen, s_renew_emethan
    pass


@dataclass
class Vars2:
    # Used by p_miner_cement, p_miner_chalk, p_miner_glas, p_miner_ceram, p_chem_basic, p_chem_ammonia, p_chem_other, p_metal_steel_primary, p_metal_steel_secondary, p_metal_nonfe, p_other_paper, p_other_food
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    energy_use_factor: float = None  # type: ignore
    percentage_of_energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by p_metal_steel
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    percentage_of_energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by p_other_further
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    percentage_of_energy: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars5:
    # Used by p_other_2efgh
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by s, s_fossil_gas, s_fossil_coal, s_fossil_diesel, s_fossil_fueloil, s_fossil_lpg, s_fossil_opetpro, s_fossil_ofossil, s_renew_biomass, s_renew_heatnet, s_renew_heatpump, s_renew_solarth, s_renew_elec
    energy: float = None  # type: ignore
    percentage_of_energy: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by s_fossil, s_renew
    energy: float = None  # type: ignore


@dataclass
class I18:
    i: Vars0 = field(default_factory=Vars0)
    p: Vars0 = field(default_factory=Vars0)
    p_miner: Vars0 = field(default_factory=Vars0)
    p_miner_cement: Vars2 = field(default_factory=Vars2)
    p_miner_chalk: Vars2 = field(default_factory=Vars2)
    p_miner_glas: Vars2 = field(default_factory=Vars2)
    p_miner_ceram: Vars2 = field(default_factory=Vars2)
    p_chem: Vars0 = field(default_factory=Vars0)
    p_chem_basic: Vars2 = field(default_factory=Vars2)
    p_chem_ammonia: Vars2 = field(default_factory=Vars2)
    p_chem_other: Vars2 = field(default_factory=Vars2)
    p_metal: Vars0 = field(default_factory=Vars0)
    p_metal_steel: Vars3 = field(default_factory=Vars3)
    p_metal_steel_primary: Vars2 = field(default_factory=Vars2)
    p_metal_steel_secondary: Vars2 = field(default_factory=Vars2)
    p_metal_nonfe: Vars2 = field(default_factory=Vars2)
    p_other: Vars0 = field(default_factory=Vars0)
    p_other_paper: Vars2 = field(default_factory=Vars2)
    p_other_food: Vars2 = field(default_factory=Vars2)
    p_other_further: Vars4 = field(default_factory=Vars4)
    p_other_2efgh: Vars5 = field(default_factory=Vars5)
    s: Vars6 = field(default_factory=Vars6)
    s_fossil: Vars7 = field(default_factory=Vars7)
    s_fossil_gas: Vars6 = field(default_factory=Vars6)
    s_fossil_coal: Vars6 = field(default_factory=Vars6)
    s_fossil_diesel: Vars6 = field(default_factory=Vars6)
    s_fossil_fueloil: Vars6 = field(default_factory=Vars6)
    s_fossil_lpg: Vars6 = field(default_factory=Vars6)
    s_fossil_opetpro: Vars6 = field(default_factory=Vars6)
    s_fossil_ofossil: Vars6 = field(default_factory=Vars6)
    s_renew: Vars7 = field(default_factory=Vars7)
    s_renew_hydrogen: Vars1 = field(default_factory=Vars1)
    s_renew_emethan: Vars1 = field(default_factory=Vars1)
    s_renew_biomass: Vars6 = field(default_factory=Vars6)
    s_renew_heatnet: Vars6 = field(default_factory=Vars6)
    s_renew_heatpump: Vars6 = field(default_factory=Vars6)
    s_renew_solarth: Vars6 = field(default_factory=Vars6)
    s_renew_elec: Vars6 = field(default_factory=Vars6)

    def dict(self):
        return asdict(self)


# for mineral industry the energy_use_factor still needs to be added to facts
def calc(inputs: Inputs) -> I18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries

    i18 = I18()

    i18.p_miner.energy = entries.i_fec_pct_of_miner * entries.i_energy_total

    i18.p_miner_cement.percentage_of_energy = fact(
        "Fact_I_P_miner_fec_pct_of_cement_2018"
    )
    i18.p_miner_cement.energy = (
        i18.p_miner_cement.percentage_of_energy * i18.p_miner.energy
    )
    i18.p_miner_cement.energy_use_factor = fact(
        "Fact_I_P_miner_cement_energy_use_factor_2017"
    )
    i18.p_miner_cement.prod_volume = (
        i18.p_miner_cement.energy * i18.p_miner_cement.energy_use_factor
    )
    i18.p_miner_cement.CO2e_production_based_per_t = fact(
        "Fact_I_P_miner_cement_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_cement.CO2e_production_based = (
        i18.p_miner_cement.prod_volume * i18.p_miner_cement.CO2e_production_based_per_t
    )
    i18.p_miner_cement.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_miner_cement_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_cement.CO2e_combustion_based = (
        i18.p_miner_cement.prod_volume * i18.p_miner_cement.CO2e_combustion_based_per_t
    )
    i18.p_miner_cement.CO2e_total = (
        i18.p_miner_cement.CO2e_production_based
        + i18.p_miner_cement.CO2e_combustion_based
    )

    # chalk
    i18.p_miner_chalk.percentage_of_energy = fact(
        "Fact_I_P_miner_fec_pct_of_chalk_2017"
    )
    i18.p_miner_chalk.energy = (
        i18.p_miner.energy * i18.p_miner_chalk.percentage_of_energy
    )
    i18.p_miner_chalk.energy_use_factor = fact(
        "Fact_I_P_miner_chalk_energy_use_factor_2017"
    )
    i18.p_miner_chalk.prod_volume = (
        i18.p_miner_chalk.energy * i18.p_miner_chalk.energy_use_factor
    )
    i18.p_miner_chalk.CO2e_production_based_per_t = fact(
        "Fact_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_chalk.CO2e_production_based = (
        i18.p_miner_chalk.prod_volume * i18.p_miner_chalk.CO2e_production_based_per_t
    )
    i18.p_miner_chalk.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_chalk.CO2e_combustion_based = (
        i18.p_miner_chalk.prod_volume * i18.p_miner_chalk.CO2e_combustion_based_per_t
    )
    i18.p_miner_chalk.CO2e_total = (
        i18.p_miner_chalk.CO2e_production_based
        + i18.p_miner_chalk.CO2e_combustion_based
    )

    # glas
    i18.p_miner_glas.percentage_of_energy = fact("Fact_I_P_miner_fec_pct_of_glas_2017")
    i18.p_miner_glas.energy = i18.p_miner.energy * i18.p_miner_glas.percentage_of_energy
    i18.p_miner_glas.energy_use_factor = fact(
        "Fact_I_P_miner_glas_energy_use_factor_2017"
    )
    i18.p_miner_glas.prod_volume = (
        i18.p_miner_glas.energy * i18.p_miner_glas.energy_use_factor
    )
    i18.p_miner_glas.CO2e_production_based_per_t = fact(
        "Fact_I_P_miner_glas_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_glas.CO2e_production_based = (
        i18.p_miner_glas.prod_volume * i18.p_miner_glas.CO2e_production_based_per_t
    )
    i18.p_miner_glas.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_miner_glas_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_glas.CO2e_combustion_based = (
        i18.p_miner_glas.prod_volume * i18.p_miner_glas.CO2e_combustion_based_per_t
    )
    i18.p_miner_glas.CO2e_total = (
        i18.p_miner_glas.CO2e_production_based + i18.p_miner_glas.CO2e_combustion_based
    )

    # cream
    i18.p_miner_ceram.percentage_of_energy = fact(
        "Fact_I_P_miner_fec_pct_of_ceram_2017"
    )
    i18.p_miner_ceram.energy = (
        i18.p_miner.energy * i18.p_miner_ceram.percentage_of_energy
    )
    i18.p_miner_ceram.energy_use_factor = fact(
        "Fact_I_P_miner_ceram_energy_use_factor_2017"
    )
    i18.p_miner_ceram.prod_volume = (
        i18.p_miner_ceram.energy * i18.p_miner_ceram.energy_use_factor
    )
    i18.p_miner_ceram.CO2e_production_based_per_t = fact(
        "Fact_I_P_miner_ceram_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_ceram.CO2e_production_based = (
        i18.p_miner_ceram.prod_volume * i18.p_miner_ceram.CO2e_production_based_per_t
    )
    i18.p_miner_ceram.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_miner_ceram_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_ceram.CO2e_combustion_based = (
        i18.p_miner_ceram.prod_volume * i18.p_miner_ceram.CO2e_combustion_based_per_t
    )
    i18.p_miner_ceram.CO2e_total = (
        i18.p_miner_ceram.CO2e_production_based
        + i18.p_miner_ceram.CO2e_combustion_based
    )

    # p_chem_basic
    i18.p_chem_basic.percentage_of_energy = fact(
        "Fact_I_S_chem_basic_wo_ammonia_fec_ratio_to_chem_all_2018"
    )

    i18.p_chem.energy = entries.i_fec_pct_of_chem * entries.i_energy_total
    i18.p_chem_basic.energy = i18.p_chem.energy * i18.p_chem_basic.percentage_of_energy
    i18.p_chem_basic.energy_use_factor = fact(
        "Fact_I_P_chem_basic_wo_ammonia_ratio_prodvol_to_fec_2018"
    )
    i18.p_chem_basic.prod_volume = (
        i18.p_chem_basic.energy * i18.p_chem_basic.energy_use_factor
    )
    i18.p_chem_basic.CO2e_production_based_per_t = fact(
        "Fact_I_P_chem_basic_wo_ammonia_CO2e_pb_ratio_per_t_product_2018"
    )
    i18.p_chem_basic.CO2e_production_based = (
        i18.p_chem_basic.prod_volume * i18.p_chem_basic.CO2e_production_based_per_t
    )
    i18.p_chem_basic.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_chem_basic_wo_ammonia_CO2e_eb_ratio_per_t_product_2018"
    )
    i18.p_chem_basic.CO2e_combustion_based = (
        i18.p_chem_basic.prod_volume * i18.p_chem_basic.CO2e_combustion_based_per_t
    )
    i18.p_chem_basic.CO2e_total = (
        i18.p_chem_basic.CO2e_production_based + i18.p_chem_basic.CO2e_combustion_based
    )

    # chem ammonia
    i18.p_chem_ammonia.percentage_of_energy = fact(
        "Fact_I_S_chem_ammonia_fec_ratio_to_chem_all_2018"
    )
    i18.p_chem_ammonia.energy = (
        i18.p_chem.energy * i18.p_chem_ammonia.percentage_of_energy
    )
    i18.p_chem_ammonia.energy_use_factor = 1 / fact(
        "Fact_I_P_chem_ammonia_fec_ratio_per_t_product_2013"
    )
    i18.p_chem_ammonia.prod_volume = (
        i18.p_chem_ammonia.energy * i18.p_chem_ammonia.energy_use_factor
    )
    i18.p_chem_ammonia.CO2e_production_based_per_t = fact(
        "Fact_I_P_chem_ammonia_CO2e_pb_ratio_per_t_product_2018"
    )
    i18.p_chem_ammonia.CO2e_production_based = (
        i18.p_chem_ammonia.prod_volume * i18.p_chem_ammonia.CO2e_production_based_per_t
    )
    i18.p_chem_ammonia.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_chem_ammonia_CO2e_eb_ratio_per_t_product_2018"
    )
    i18.p_chem_ammonia.CO2e_combustion_based = (
        i18.p_chem_ammonia.prod_volume * i18.p_chem_ammonia.CO2e_combustion_based_per_t
    )
    i18.p_chem_ammonia.CO2e_total = (
        i18.p_chem_ammonia.CO2e_production_based
        + i18.p_chem_ammonia.CO2e_combustion_based
    )

    # chem other
    i18.p_chem_other.percentage_of_energy = fact(
        "Fact_I_S_chem_other_fec_ratio_to_chem_all_2018"
    )
    i18.p_chem_other.energy = i18.p_chem.energy * i18.p_chem_other.percentage_of_energy
    i18.p_chem_other.energy_use_factor = fact(
        "Fact_I_P_chem_other_ratio_prodvol_to_fec_2018"
    )
    i18.p_chem_other.prod_volume = (
        i18.p_chem_other.energy * i18.p_chem_other.energy_use_factor
    )
    i18.p_chem_other.CO2e_production_based_per_t = fact(
        "Fact_I_P_chem_other_CO2e_pb_ratio_per_t_product_2018"
    )
    i18.p_chem_other.CO2e_production_based = (
        i18.p_chem_other.prod_volume * i18.p_chem_other.CO2e_production_based_per_t
    )
    i18.p_chem_other.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_chem_other_CO2e_eb_ratio_per_t_product_2018"
    )
    i18.p_chem_other.CO2e_combustion_based = (
        i18.p_chem_other.prod_volume * i18.p_chem_other.CO2e_combustion_based_per_t
    )
    i18.p_chem_other.CO2e_total = (
        i18.p_chem_other.CO2e_production_based + i18.p_chem_other.CO2e_combustion_based
    )

    # Funktioniert erst mit aktualisierter Fakten pki (24.08.21)
    # metal
    i18.p_metal.energy = entries.i_fec_pct_of_metal * entries.i_energy_total

    # steel total (primary and secondary)
    i18.p_metal_steel.percentage_of_energy = fact(
        "Fact_I_P_metal_fec_pct_of_steel_2018"
    )
    i18.p_metal_steel.energy = (
        i18.p_metal.energy * i18.p_metal_steel.percentage_of_energy
    )

    # primary route -----------------------------------------------------------------------
    i18.p_metal_steel_primary.percentage_of_energy = fact(
        "Fakt_I_N_metallh_Primaerroute_EEV_2018_Anteil"
    )
    i18.p_metal_steel_primary.energy = (
        i18.p_metal_steel.energy * i18.p_metal_steel_primary.percentage_of_energy
    )

    i18.p_metal_steel_primary.energy_use_factor = 1 / fact(
        "Fact_I_P_metal_steel_primary_ratio_fec_to_prodvol_2018"
    )
    i18.p_metal_steel_primary.prod_volume = (
        i18.p_metal_steel_primary.energy * i18.p_metal_steel_primary.energy_use_factor
    )

    i18.p_metal_steel_primary.CO2e_production_based_per_t = fact(
        "Fact_I_P_metal_steel_primary_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_metal_steel_primary.CO2e_production_based = (
        i18.p_metal_steel_primary.prod_volume
        * i18.p_metal_steel_primary.CO2e_production_based_per_t
    )

    i18.p_metal_steel_primary.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_metal_steel_primary_ratio_CO2e_eb_to_prodvol_2018"
    )
    i18.p_metal_steel_primary.CO2e_combustion_based = (
        i18.p_metal_steel_primary.prod_volume
        * i18.p_metal_steel_primary.CO2e_combustion_based_per_t
    )

    i18.p_metal_steel_primary.CO2e_total = (
        i18.p_metal_steel_primary.CO2e_production_based
        + i18.p_metal_steel_primary.CO2e_combustion_based
    )

    # secondary route ----------------------------------------------------------------
    i18.p_metal_steel_secondary.percentage_of_energy = fact(
        "Fakt_I_N_metallh_Sekundaerroute_EEV_2018_Anteil"
    )
    i18.p_metal_steel_secondary.energy = (
        i18.p_metal_steel.energy * i18.p_metal_steel_secondary.percentage_of_energy
    )

    i18.p_metal_steel_secondary.energy_use_factor = 1 / fact(
        "Fact_I_P_metal_steel_secondary_ratio_fec_to_prodvol_2018"
    )
    i18.p_metal_steel_secondary.prod_volume = (
        i18.p_metal_steel_secondary.energy
        * i18.p_metal_steel_secondary.energy_use_factor
    )

    i18.p_metal_steel_secondary.CO2e_production_based_per_t = fact(
        "Fact_I_P_metal_steel_secondary_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_metal_steel_secondary.CO2e_production_based = (
        i18.p_metal_steel_secondary.prod_volume
        * i18.p_metal_steel_secondary.CO2e_production_based_per_t
    )

    i18.p_metal_steel_secondary.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_metal_steel_secondary_ratio_CO2e_eb_to_prodvol_2018"
    )
    i18.p_metal_steel_secondary.CO2e_combustion_based = (
        i18.p_metal_steel_secondary.prod_volume
        * i18.p_metal_steel_secondary.CO2e_combustion_based_per_t
    )

    i18.p_metal_steel_secondary.CO2e_total = (
        i18.p_metal_steel_secondary.CO2e_production_based
        + i18.p_metal_steel_secondary.CO2e_combustion_based
    )

    # steel total (primary and secondary) - continiued -----------------------------
    i18.p_metal_steel.prod_volume = (
        i18.p_metal_steel_primary.prod_volume + i18.p_metal_steel_secondary.prod_volume
    )

    i18.p_metal_steel.CO2e_production_based = (
        i18.p_metal_steel_primary.CO2e_production_based
        + i18.p_metal_steel_secondary.CO2e_production_based
    )
    i18.p_metal_steel.CO2e_combustion_based = (
        i18.p_metal_steel_primary.CO2e_combustion_based
        + i18.p_metal_steel_secondary.CO2e_combustion_based
    )
    i18.p_metal_steel.CO2e_total = (
        i18.p_metal_steel_primary.CO2e_total + i18.p_metal_steel_secondary.CO2e_total
    )

    # non fe metals ------------------------------------------------------------------
    i18.p_metal_nonfe.percentage_of_energy = fact(
        "Fact_I_P_metal_fec_pct_of_nonfe_2018"
    )
    i18.p_metal_nonfe.energy = (
        i18.p_metal.energy * i18.p_metal_nonfe.percentage_of_energy
    )

    i18.p_metal_nonfe.energy_use_factor = 1 / fact(
        "Fact_I_P_metal_nonfe_ratio_fec_to_prodvol_2018"
    )
    i18.p_metal_nonfe.prod_volume = (
        i18.p_metal_nonfe.energy * i18.p_metal_nonfe.energy_use_factor
    )

    i18.p_metal_nonfe.CO2e_production_based_per_t = fact(
        "Fact_I_P_metal_nonfe_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_metal_nonfe.CO2e_production_based = (
        i18.p_metal_nonfe.prod_volume * i18.p_metal_nonfe.CO2e_production_based_per_t
    )

    i18.p_metal_nonfe.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_metal_nonfe_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_metal_nonfe.CO2e_combustion_based = (
        i18.p_metal_nonfe.prod_volume * i18.p_metal_nonfe.CO2e_combustion_based_per_t
    )

    i18.p_metal_nonfe.CO2e_total = (
        i18.p_metal_nonfe.CO2e_production_based
        + i18.p_metal_nonfe.CO2e_combustion_based
    )

    # p_other
    i18.p_other.energy = entries.i_fec_pct_of_other * entries.i_energy_total

    # p_other_paper
    i18.p_other_paper.percentage_of_energy = fact(
        "Fact_I_P_other_fec_pct_of_paper_2018"
    )

    i18.p_other_paper.energy = (
        i18.p_other.energy * i18.p_other_paper.percentage_of_energy
    )
    i18.p_other_paper.energy_use_factor = 1 / fact(
        "Fact_I_P_other_paper_ratio_fec_to_prodvol_2018"
    )
    i18.p_other_paper.prod_volume = (
        i18.p_other_paper.energy * i18.p_other_paper.energy_use_factor
    )

    i18.p_other_paper.CO2e_production_based_per_t = fact(
        "Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_other_paper.CO2e_production_based = (
        i18.p_other_paper.CO2e_production_based_per_t * i18.p_other_paper.prod_volume
    )

    i18.p_other_paper.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_other_paper_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_other_paper.CO2e_combustion_based = (
        i18.p_other_paper.prod_volume * i18.p_other_paper.CO2e_combustion_based_per_t
    )

    i18.p_other_paper.CO2e_total = (
        i18.p_other_paper.CO2e_production_based
        + i18.p_other_paper.CO2e_combustion_based
    )

    # p_other_food
    i18.p_other_food.percentage_of_energy = fact("Fact_I_P_other_fec_pct_of_food_2018")
    i18.p_other_food.energy = i18.p_other.energy * i18.p_other_food.percentage_of_energy
    i18.p_other_food.energy_use_factor = 1 / fact(
        "Fact_I_P_other_food_ratio_fec_to_prodvol_2018"
    )
    i18.p_other_food.prod_volume = (
        i18.p_other_food.energy * i18.p_other_food.energy_use_factor
    )

    i18.p_other_food.CO2e_production_based_per_t = fact(
        "Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_other_food.CO2e_production_based = (
        i18.p_other_food.prod_volume * i18.p_other_food.CO2e_production_based_per_t
    )

    i18.p_other_food.CO2e_combustion_based_per_t = fact(
        "Fact_I_P_other_food_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_other_food.CO2e_combustion_based = (
        i18.p_other_food.prod_volume * i18.p_other_food.CO2e_combustion_based_per_t
    )

    i18.p_other_food.CO2e_total = (
        i18.p_other_food.CO2e_combustion_based + i18.p_other_food.CO2e_production_based
    )

    # p_other_further
    i18.p_other_further.percentage_of_energy = fact(
        "Fact_I_P_other_fec_pct_of_further_2018"
    )
    i18.p_other_further.energy = (
        i18.p_other.energy * i18.p_other_further.percentage_of_energy
    )
    # no prodvolume for other industries
    # i18.p_other_further.energy_use_factor =
    # i18.p_other_further.prod_volume = i18.p_other_further.energy * i18.p_other_further.energy_use_factor
    i18.p_other_further.CO2e_production_based_per_MWh = fact(
        "Fact_I_P_other_2d_ratio_CO2e_pb_to_fec_2018"
    )
    i18.p_other_further.CO2e_production_based = (
        i18.p_other_further.energy * i18.p_other_further.CO2e_production_based_per_MWh
    )
    i18.p_other_further.CO2e_combustion_based_per_MWh = fact(
        "Fact_I_P_other_further_ratio_CO2e_cb_to_fec_2018"
    )
    i18.p_other_further.CO2e_combustion_based = (
        i18.p_other_further.energy * i18.p_other_further.CO2e_combustion_based_per_MWh
    )
    i18.p_other_further.CO2e_total = (
        i18.p_other_further.CO2e_production_based
        + i18.p_other_further.CO2e_combustion_based
    )
    i18.p_other_further.prod_volume = fact("Fact_I_P_other_further_prodvol_2018")

    # energy of further_other_industries

    i18.p_other_2efgh.CO2e_production_based_per_MWh = fact(
        "Fact_I_P_other_2efgh_ratio_CO2e_pb_to_fec_2018"
    )
    i18.p_other_2efgh.CO2e_production_based = (
        i18.p_other_further.energy * i18.p_other_2efgh.CO2e_production_based_per_MWh
    )
    i18.p_other_2efgh.CO2e_total = i18.p_other_2efgh.CO2e_production_based

    i18.p_miner.prod_volume = (
        i18.p_miner_cement.prod_volume
        + i18.p_miner_chalk.prod_volume
        + i18.p_miner_glas.prod_volume
        + i18.p_miner_ceram.prod_volume
    )

    i18.p_chem.prod_volume = (
        i18.p_chem_basic.prod_volume
        + i18.p_chem_ammonia.prod_volume
        + i18.p_chem_other.prod_volume
    )
    i18.p_miner.CO2e_production_based = (
        i18.p_miner_cement.CO2e_production_based
        + i18.p_miner_chalk.CO2e_production_based
        + i18.p_miner_glas.CO2e_production_based
        + i18.p_miner_ceram.CO2e_production_based
    )

    i18.p_chem.CO2e_production_based = (
        i18.p_chem_basic.CO2e_production_based
        + i18.p_chem_ammonia.CO2e_production_based
        + i18.p_chem_other.CO2e_production_based
    )
    i18.p_metal.CO2e_production_based = (
        i18.p_metal_steel.CO2e_production_based
        + i18.p_metal_nonfe.CO2e_production_based
    )

    i18.p_other.CO2e_production_based = (
        i18.p_other_paper.CO2e_production_based
        + i18.p_other_food.CO2e_production_based
        + i18.p_other_further.CO2e_production_based
        + i18.p_other_2efgh.CO2e_production_based
    )

    i18.p_miner.CO2e_combustion_based = (
        i18.p_miner_cement.CO2e_combustion_based
        + i18.p_miner_chalk.CO2e_combustion_based
        + i18.p_miner_glas.CO2e_combustion_based
        + i18.p_miner_ceram.CO2e_combustion_based
    )

    i18.p_chem.CO2e_combustion_based = (
        i18.p_chem_basic.CO2e_combustion_based
        + i18.p_chem_ammonia.CO2e_combustion_based
        + i18.p_chem_other.CO2e_combustion_based
    )

    i18.p_metal.CO2e_combustion_based = (
        i18.p_metal_steel.CO2e_combustion_based
        + i18.p_metal_nonfe.CO2e_combustion_based
    )

    i18.p_other.CO2e_combustion_based = (
        i18.p_other_paper.CO2e_combustion_based
        + i18.p_other_food.CO2e_combustion_based
        + i18.p_other_further.CO2e_combustion_based
    )

    i18.p.CO2e_combustion_based = (
        i18.p_miner.CO2e_combustion_based
        + i18.p_chem.CO2e_combustion_based
        + i18.p_metal.CO2e_combustion_based
        + i18.p_other.CO2e_combustion_based
    )

    i18.p_metal.prod_volume = (
        i18.p_metal_steel.prod_volume + i18.p_metal_nonfe.prod_volume
    )

    i18.p_other.prod_volume = (
        i18.p_other_paper.prod_volume + i18.p_other_food.prod_volume
    )

    i18.p.energy = entries.i_energy_total
    i18.p.prod_volume = (
        i18.p_miner.prod_volume
        + i18.p_chem.prod_volume
        + i18.p_metal.prod_volume
        + i18.p_other.prod_volume
    )

    i18.p.CO2e_production_based = (
        i18.p_miner.CO2e_production_based
        + i18.p_chem.CO2e_production_based
        + i18.p_metal.CO2e_production_based
        + i18.p_other.CO2e_production_based
    )

    i18.p_miner.CO2e_total = (
        i18.p_miner_cement.CO2e_total
        + i18.p_miner_chalk.CO2e_total
        + i18.p_miner_glas.CO2e_total
        + i18.p_miner_ceram.CO2e_total
    )

    i18.p_chem.CO2e_total = (
        i18.p_chem_basic.CO2e_total
        + i18.p_chem_ammonia.CO2e_total
        + i18.p_chem_other.CO2e_total
    )

    i18.p_metal.CO2e_total = i18.p_metal_steel.CO2e_total + i18.p_metal_nonfe.CO2e_total

    i18.p_other.CO2e_total = (
        i18.p_other_paper.CO2e_total
        + i18.p_other_food.CO2e_total
        + i18.p_other_further.CO2e_total
        + i18.p_other_2efgh.CO2e_total
    )

    i18.p.CO2e_total = (
        i18.p_miner.CO2e_total
        + i18.p_chem.CO2e_total
        + i18.p_metal.CO2e_total
        + i18.p_other.CO2e_total
    )

    i18.s.energy = entries.i_energy_total

    i18.s_fossil_gas.energy = entries.i_gas_fec
    i18.s_fossil_coal.energy = entries.i_coal_fec
    i18.s_fossil_diesel.energy = entries.i_diesel_fec
    i18.s_fossil_fueloil.energy = entries.i_fueloil_fec
    i18.s_fossil_lpg.energy = entries.i_lpg_fec
    i18.s_fossil_opetpro.energy = entries.i_opetpro_fec
    i18.s_fossil_ofossil.energy = entries.i_ofossil_fec

    i18.s_renew_biomass.energy = entries.i_biomass_fec
    i18.s_renew_heatnet.energy = entries.i_heatnet_fec
    i18.s_renew_heatpump.energy = entries.i_orenew_fec * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    i18.s_renew_solarth.energy = entries.i_orenew_fec * fact(
        "Fact_R_S_ratio_solarth_to_orenew_2018"
    )
    i18.s_renew_elec.energy = entries.i_elec_fec

    i18.s_renew.energy = (
        i18.s_renew_biomass.energy
        + i18.s_renew_heatnet.energy
        + i18.s_renew_heatpump.energy
        + i18.s_renew_solarth.energy
        + i18.s_renew_elec.energy
    )

    i18.s_fossil.energy = (
        i18.s_fossil_gas.energy
        + i18.s_fossil_coal.energy
        + i18.s_fossil_diesel.energy
        + i18.s_fossil_fueloil.energy
        + i18.s_fossil_lpg.energy
        + i18.s_fossil_opetpro.energy
        + i18.s_fossil_ofossil.energy
    )

    i18.s_fossil_gas.percentage_of_energy = div(i18.s_fossil_gas.energy, i18.s.energy)
    i18.s_fossil_coal.percentage_of_energy = div(i18.s_fossil_coal.energy, i18.s.energy)
    i18.s_fossil_diesel.percentage_of_energy = div(
        i18.s_fossil_diesel.energy, i18.s.energy
    )
    i18.s_fossil_fueloil.percentage_of_energy = div(
        i18.s_fossil_fueloil.energy, i18.s.energy
    )
    i18.s_fossil_lpg.percentage_of_energy = div(i18.s_fossil_lpg.energy, i18.s.energy)
    i18.s_fossil_opetpro.percentage_of_energy = div(
        i18.s_fossil_opetpro.energy, i18.s.energy
    )
    i18.s_fossil_ofossil.percentage_of_energy = div(
        i18.s_fossil_ofossil.energy, i18.s.energy
    )

    i18.s_renew_biomass.percentage_of_energy = div(
        i18.s_renew_biomass.energy, i18.s.energy
    )
    i18.s_renew_heatnet.percentage_of_energy = div(
        i18.s_renew_heatnet.energy, i18.s.energy
    )
    i18.s_renew_heatpump.percentage_of_energy = div(
        i18.s_renew_heatpump.energy, i18.s.energy
    )
    i18.s_renew_solarth.percentage_of_energy = div(
        i18.s_renew_solarth.energy, i18.s.energy
    )
    i18.s_renew_elec.percentage_of_energy = div(i18.s_renew_elec.energy, i18.s.energy)

    i18.s.percentage_of_energy = (
        i18.s_fossil_gas.percentage_of_energy
        + i18.s_fossil_coal.percentage_of_energy
        + i18.s_fossil_diesel.percentage_of_energy
        + i18.s_fossil_fueloil.percentage_of_energy
        + i18.s_fossil_lpg.percentage_of_energy
        + i18.s_fossil_opetpro.percentage_of_energy
        + i18.s_fossil_ofossil.percentage_of_energy
        + i18.s_renew_biomass.percentage_of_energy
        + i18.s_renew_heatnet.percentage_of_energy
        + i18.s_renew_heatpump.percentage_of_energy
        + i18.s_renew_solarth.percentage_of_energy
        + i18.s_renew_elec.percentage_of_energy
    )

    i18.i.prod_volume = i18.p.prod_volume
    i18.i.CO2e_production_based = i18.p.CO2e_production_based
    i18.i.CO2e_combustion_based = i18.p.CO2e_combustion_based
    i18.i.CO2e_total = i18.p.CO2e_total
    i18.i.energy = i18.p.energy

    return i18
