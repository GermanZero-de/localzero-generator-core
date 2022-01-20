from dataclasses import dataclass, field, InitVar, asdict
from .setup import ass, entry, fact


@dataclass
class IColVars:
    energy: float = None
    pct_energy: float = None
    prod_volume: float = None
    energy_use_factor: float = None
    CO2e_pb: float = None
    CO2e_pb_per_MWh: float = None
    CO2e_pb_per_t: float = None
    CO2e_cb: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_cb_per_t: float = None
    CO2e_total: float = None


@dataclass
class I18:
    g: IColVars = IColVars()
    p: IColVars = IColVars()
    p_miner: IColVars = IColVars()
    p_miner_cement: IColVars = IColVars()
    p_miner_chalk: IColVars = IColVars()
    p_miner_glas: IColVars = IColVars()
    p_miner_ceram: IColVars = IColVars()
    p_chem: IColVars = IColVars()
    p_chem_basic: IColVars = IColVars()
    p_chem_ammonia: IColVars = IColVars()
    p_chem_other: IColVars = IColVars()
    p_metal: IColVars = IColVars()
    p_metal_steel: IColVars = IColVars()
    p_metal_steel_primary: IColVars = IColVars()
    p_metal_steel_secondary: IColVars = IColVars()
    p_metal_nonfe: IColVars = IColVars()
    p_other: IColVars = IColVars()
    p_other_paper: IColVars = IColVars()
    p_other_food: IColVars = IColVars()
    p_other_further: IColVars = IColVars()
    p_other_2efgh: IColVars = IColVars()
    s: IColVars = IColVars()
    s_fossil: IColVars = IColVars()
    s_fossil_gas: IColVars = IColVars()
    s_fossil_coal: IColVars = IColVars()
    s_fossil_diesel: IColVars = IColVars()
    s_fossil_fueloil: IColVars = IColVars()
    s_fossil_lpg: IColVars = IColVars()
    s_fossil_opetpro: IColVars = IColVars()
    s_fossil_ofossil: IColVars = IColVars()
    s_renew: IColVars = IColVars()
    s_renew_hydrogen: IColVars = IColVars()
    s_renew_emethan: IColVars = IColVars()
    s_renew_biomass: IColVars = IColVars()
    s_renew_heatnet: IColVars = IColVars()
    s_renew_orenew: IColVars = IColVars()
    s_renew_solarth: IColVars = IColVars()
    s_renew_elec: IColVars = IColVars()

    def dict(self):
        return asdict(self)


# for mineral industry the energy_use_factor still needs to be added to facts
def Industry2018_calc(root):

    i18 = root.i18

    i18.p_miner.energy = entry("In_I_miner_fec")

    i18.p_miner_cement.pct_energy = fact("Fact_I_P_miner_fec_pct_of_cement_2018")
    i18.p_miner_cement.energy = i18.p_miner_cement.pct_energy * i18.p_miner.energy
    i18.p_miner_cement.energy_use_factor = fact(
        "Fact_I_P_miner_cement_energy_use_factor_2017"
    )
    i18.p_miner_cement.prod_volume = (
        i18.p_miner_cement.energy * i18.p_miner_cement.energy_use_factor
    )
    i18.p_miner_cement.CO2e_pb_per_t = fact(
        "Fact_I_P_miner_cement_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_cement.CO2e_pb = (
        i18.p_miner_cement.prod_volume * i18.p_miner_cement.CO2e_pb_per_t
    )
    i18.p_miner_cement.CO2e_cb_per_t = fact(
        "Fact_I_P_miner_cement_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_cement.CO2e_cb = (
        i18.p_miner_cement.prod_volume * i18.p_miner_cement.CO2e_cb_per_t
    )
    i18.p_miner_cement.CO2e_total = (
        i18.p_miner_cement.CO2e_pb + i18.p_miner_cement.CO2e_cb
    )

    # chalk
    i18.p_miner_chalk.pct_energy = fact("Fact_I_P_miner_fec_pct_of_chalk_2017")
    i18.p_miner_chalk.energy = i18.p_miner.energy * i18.p_miner_chalk.pct_energy
    i18.p_miner_chalk.energy_use_factor = fact(
        "Fact_I_P_miner_chalk_energy_use_factor_2017"
    )
    i18.p_miner_chalk.prod_volume = (
        i18.p_miner_chalk.energy * i18.p_miner_chalk.energy_use_factor
    )
    i18.p_miner_chalk.CO2e_pb_per_t = fact(
        "Fact_I_P_miner_chalk_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_chalk.CO2e_pb = (
        i18.p_miner_chalk.prod_volume * i18.p_miner_chalk.CO2e_pb_per_t
    )
    i18.p_miner_chalk.CO2e_cb_per_t = fact(
        "Fact_I_P_miner_chalk_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_chalk.CO2e_cb = (
        i18.p_miner_chalk.prod_volume * i18.p_miner_chalk.CO2e_cb_per_t
    )
    i18.p_miner_chalk.CO2e_total = i18.p_miner_chalk.CO2e_pb + i18.p_miner_chalk.CO2e_cb

    # glas
    i18.p_miner_glas.pct_energy = fact("Fact_I_P_miner_fec_pct_of_glas_2017")
    i18.p_miner_glas.energy = i18.p_miner.energy * i18.p_miner_glas.pct_energy
    i18.p_miner_glas.energy_use_factor = fact(
        "Fact_I_P_miner_glas_energy_use_factor_2017"
    )
    i18.p_miner_glas.prod_volume = (
        i18.p_miner_glas.energy * i18.p_miner_glas.energy_use_factor
    )
    i18.p_miner_glas.CO2e_pb_per_t = fact(
        "Fact_I_P_miner_glas_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_glas.CO2e_pb = (
        i18.p_miner_glas.prod_volume * i18.p_miner_glas.CO2e_pb_per_t
    )
    i18.p_miner_glas.CO2e_cb_per_t = fact(
        "Fact_I_P_miner_glas_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_glas.CO2e_cb = (
        i18.p_miner_glas.prod_volume * i18.p_miner_glas.CO2e_cb_per_t
    )
    i18.p_miner_glas.CO2e_total = i18.p_miner_glas.CO2e_pb + i18.p_miner_glas.CO2e_cb

    # cream
    i18.p_miner_ceram.pct_energy = fact("Fact_I_P_miner_fec_pct_of_ceram_2017")
    i18.p_miner_ceram.energy = i18.p_miner.energy * i18.p_miner_ceram.pct_energy
    i18.p_miner_ceram.energy_use_factor = fact(
        "Fact_I_P_miner_ceram_energy_use_factor_2017"
    )
    i18.p_miner_ceram.prod_volume = (
        i18.p_miner_ceram.energy * i18.p_miner_ceram.energy_use_factor
    )
    i18.p_miner_ceram.CO2e_pb_per_t = fact(
        "Fact_I_P_miner_ceram_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_miner_ceram.CO2e_pb = (
        i18.p_miner_ceram.prod_volume * i18.p_miner_ceram.CO2e_pb_per_t
    )
    i18.p_miner_ceram.CO2e_cb_per_t = fact(
        "Fact_I_P_miner_ceram_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_miner_ceram.CO2e_cb = (
        i18.p_miner_ceram.prod_volume * i18.p_miner_ceram.CO2e_cb_per_t
    )
    i18.p_miner_ceram.CO2e_total = i18.p_miner_ceram.CO2e_pb + i18.p_miner_ceram.CO2e_cb

    # p_chem_basic
    i18.p_chem_basic.pct_energy = fact(
        "Fact_I_S_chem_basic_wo_ammonia_fec_ratio_to_chem_all_2018"
    )

    i18.p_chem.energy = entry("In_I_chem_fec")
    i18.p_chem_basic.energy = entry("In_I_chem_fec") * i18.p_chem_basic.pct_energy
    i18.p_chem_basic.energy_use_factor = fact(
        "Fact_I_P_chem_basic_wo_ammonia_ratio_prodvol_to_fec_2018"
    )
    i18.p_chem_basic.prod_volume = (
        i18.p_chem_basic.energy * i18.p_chem_basic.energy_use_factor
    )
    i18.p_chem_basic.CO2e_pb_per_t = fact(
        "Fact_I_P_chem_basic_wo_ammonia_CO2e_pb_ratio_per_t_product_2018"
    )
    i18.p_chem_basic.CO2e_pb = (
        i18.p_chem_basic.prod_volume * i18.p_chem_basic.CO2e_pb_per_t
    )
    i18.p_chem_basic.CO2e_cb_per_t = fact(
        "Fact_I_P_chem_basic_wo_ammonia_CO2e_eb_ratio_per_t_product_2018"
    )
    i18.p_chem_basic.CO2e_cb = (
        i18.p_chem_basic.prod_volume * i18.p_chem_basic.CO2e_cb_per_t
    )
    i18.p_chem_basic.CO2e_total = i18.p_chem_basic.CO2e_pb + i18.p_chem_basic.CO2e_cb

    # chem ammonia
    i18.p_chem_ammonia.pct_energy = fact(
        "Fact_I_S_chem_ammonia_fec_ratio_to_chem_all_2018"
    )
    i18.p_chem_ammonia.energy = entry("In_I_chem_fec") * i18.p_chem_ammonia.pct_energy
    i18.p_chem_ammonia.energy_use_factor = 1 / fact(
        "Fact_I_P_chem_ammonia_fec_ratio_per_t_product_2013"
    )
    i18.p_chem_ammonia.prod_volume = (
        i18.p_chem_ammonia.energy * i18.p_chem_ammonia.energy_use_factor
    )
    i18.p_chem_ammonia.CO2e_pb_per_t = fact(
        "Fact_I_P_chem_ammonia_CO2e_pb_ratio_per_t_product_2018"
    )
    i18.p_chem_ammonia.CO2e_pb = (
        i18.p_chem_ammonia.prod_volume * i18.p_chem_ammonia.CO2e_pb_per_t
    )
    i18.p_chem_ammonia.CO2e_cb_per_t = fact(
        "Fact_I_P_chem_ammonia_CO2e_eb_ratio_per_t_product_2018"
    )
    i18.p_chem_ammonia.CO2e_cb = (
        i18.p_chem_ammonia.prod_volume * i18.p_chem_ammonia.CO2e_cb_per_t
    )
    i18.p_chem_ammonia.CO2e_total = (
        i18.p_chem_ammonia.CO2e_pb + i18.p_chem_ammonia.CO2e_cb
    )

    # chem other
    i18.p_chem_other.pct_energy = fact("Fact_I_S_chem_other_fec_ratio_to_chem_all_2018")
    i18.p_chem_other.energy = entry("In_I_chem_fec") * i18.p_chem_other.pct_energy
    i18.p_chem_other.energy_use_factor = fact(
        "Fact_I_P_chem_other_ratio_prodvol_to_fec_2018"
    )
    i18.p_chem_other.prod_volume = (
        i18.p_chem_other.energy * i18.p_chem_other.energy_use_factor
    )
    i18.p_chem_other.CO2e_pb_per_t = fact(
        "Fact_I_P_chem_other_CO2e_pb_ratio_per_t_product_2018"
    )
    i18.p_chem_other.CO2e_pb = (
        i18.p_chem_other.prod_volume * i18.p_chem_other.CO2e_pb_per_t
    )
    i18.p_chem_other.CO2e_cb_per_t = fact(
        "Fact_I_P_chem_other_CO2e_eb_ratio_per_t_product_2018"
    )
    i18.p_chem_other.CO2e_cb = (
        i18.p_chem_other.prod_volume * i18.p_chem_other.CO2e_cb_per_t
    )
    i18.p_chem_other.CO2e_total = i18.p_chem_other.CO2e_pb + i18.p_chem_other.CO2e_cb

    # Funktioniert erst mit aktualisierter Fakten pki (24.08.21)
    # metal
    i18.p_metal.energy = entry("In_I_metal_fec")

    # steel total (primary and secondary)
    i18.p_metal_steel.pct_energy = fact("Fact_I_P_metal_fec_pct_of_steel_2018")
    i18.p_metal_steel.energy = i18.p_metal.energy * i18.p_metal_steel.pct_energy

    # primary route -----------------------------------------------------------------------
    i18.p_metal_steel_primary.pct_energy = fact(
        "Fakt_I_N_metallh_Primaerroute_EEV_2018_Anteil"
    )
    i18.p_metal_steel_primary.energy = (
        i18.p_metal_steel.energy * i18.p_metal_steel_primary.pct_energy
    )

    i18.p_metal_steel_primary.energy_use_factor = 1 / fact(
        "Fact_I_P_metal_steel_primary_ratio_fec_to_prodvol_2018"
    )
    i18.p_metal_steel_primary.prod_volume = (
        i18.p_metal_steel_primary.energy * i18.p_metal_steel_primary.energy_use_factor
    )

    i18.p_metal_steel_primary.CO2e_pb_per_t = fact(
        "Fact_I_P_metal_steel_primary_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_metal_steel_primary.CO2e_pb = (
        i18.p_metal_steel_primary.prod_volume * i18.p_metal_steel_primary.CO2e_pb_per_t
    )

    i18.p_metal_steel_primary.CO2e_cb_per_t = fact(
        "Fact_I_P_metal_steel_primary_ratio_CO2e_eb_to_prodvol_2018"
    )
    i18.p_metal_steel_primary.CO2e_cb = (
        i18.p_metal_steel_primary.prod_volume * i18.p_metal_steel_primary.CO2e_cb_per_t
    )

    i18.p_metal_steel_primary.CO2e_total = (
        i18.p_metal_steel_primary.CO2e_pb + i18.p_metal_steel_primary.CO2e_cb
    )

    # secondary route ----------------------------------------------------------------
    i18.p_metal_steel_secondary.pct_energy = fact(
        "Fakt_I_N_metallh_Sekundaerroute_EEV_2018_Anteil"
    )
    i18.p_metal_steel_secondary.energy = (
        i18.p_metal_steel.energy * i18.p_metal_steel_secondary.pct_energy
    )

    i18.p_metal_steel_secondary.energy_use_factor = 1 / fact(
        "Fact_I_P_metal_steel_secondary_ratio_fec_to_prodvol_2018"
    )
    i18.p_metal_steel_secondary.prod_volume = (
        i18.p_metal_steel_secondary.energy
        * i18.p_metal_steel_secondary.energy_use_factor
    )

    i18.p_metal_steel_secondary.CO2e_pb_per_t = fact(
        "Fact_I_P_metal_steel_secondary_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_metal_steel_secondary.CO2e_pb = (
        i18.p_metal_steel_secondary.prod_volume
        * i18.p_metal_steel_secondary.CO2e_pb_per_t
    )

    i18.p_metal_steel_secondary.CO2e_cb_per_t = fact(
        "Fact_I_P_metal_steel_secondary_ratio_CO2e_eb_to_prodvol_2018"
    )
    i18.p_metal_steel_secondary.CO2e_cb = (
        i18.p_metal_steel_secondary.prod_volume
        * i18.p_metal_steel_secondary.CO2e_cb_per_t
    )

    i18.p_metal_steel_secondary.CO2e_total = (
        i18.p_metal_steel_secondary.CO2e_pb + i18.p_metal_steel_secondary.CO2e_cb
    )

    # steel total (primary and secondary) - continiued -----------------------------
    i18.p_metal_steel.prod_volume = (
        i18.p_metal_steel_primary.prod_volume + i18.p_metal_steel_secondary.prod_volume
    )

    i18.p_metal_steel.CO2e_pb = (
        i18.p_metal_steel_primary.CO2e_pb + i18.p_metal_steel_secondary.CO2e_pb
    )
    i18.p_metal_steel.CO2e_cb = (
        i18.p_metal_steel_primary.CO2e_cb + i18.p_metal_steel_secondary.CO2e_cb
    )
    i18.p_metal_steel.CO2e_total = (
        i18.p_metal_steel_primary.CO2e_total + i18.p_metal_steel_secondary.CO2e_total
    )

    # non fe metals ------------------------------------------------------------------
    i18.p_metal_nonfe.pct_energy = fact("Fact_I_P_metal_fec_pct_of_nonfe_2018")
    i18.p_metal_nonfe.energy = i18.p_metal.energy * i18.p_metal_nonfe.pct_energy

    i18.p_metal_nonfe.energy_use_factor = 1 / fact(
        "Fact_I_P_metal_nonfe_ratio_fec_to_prodvol_2018"
    )
    i18.p_metal_nonfe.prod_volume = (
        i18.p_metal_nonfe.energy * i18.p_metal_nonfe.energy_use_factor
    )

    i18.p_metal_nonfe.CO2e_pb_per_t = fact(
        "Fact_I_P_metal_nonfe_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_metal_nonfe.CO2e_pb = (
        i18.p_metal_nonfe.prod_volume * i18.p_metal_nonfe.CO2e_pb_per_t
    )

    i18.p_metal_nonfe.CO2e_cb_per_t = fact(
        "Fact_I_P_metal_nonfe_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_metal_nonfe.CO2e_cb = (
        i18.p_metal_nonfe.prod_volume * i18.p_metal_nonfe.CO2e_cb_per_t
    )

    i18.p_metal_nonfe.CO2e_total = i18.p_metal_nonfe.CO2e_pb + i18.p_metal_nonfe.CO2e_cb

    # p_other_paper
    i18.p_other_paper.pct_energy = fact("Fact_I_P_other_fec_pct_of_paper_2018")

    i18.p_other_paper.energy = entry("In_I_other_fec") * i18.p_other_paper.pct_energy
    i18.p_other_paper.energy_use_factor = 1 / fact(
        "Fact_I_P_other_paper_ratio_fec_to_prodvol_2018"
    )
    i18.p_other_paper.prod_volume = (
        i18.p_other_paper.energy * i18.p_other_paper.energy_use_factor
    )

    i18.p_other_paper.CO2e_pb_per_t = fact(
        "Fact_I_P_other_paper_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_other_paper.CO2e_pb = (
        i18.p_other_paper.CO2e_pb_per_t * i18.p_other_paper.prod_volume
    )

    i18.p_other_paper.CO2e_cb_per_t = fact(
        "Fact_I_P_other_paper_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_other_paper.CO2e_cb = (
        i18.p_other_paper.prod_volume * i18.p_other_paper.CO2e_cb_per_t
    )

    i18.p_other_paper.CO2e_total = i18.p_other_paper.CO2e_pb + i18.p_other_paper.CO2e_cb

    # p_other_food
    i18.p_other_food.pct_energy = fact("Fact_I_P_other_fec_pct_of_food_2018")
    i18.p_other_food.energy = entry("In_I_other_fec") * i18.p_other_food.pct_energy
    i18.p_other_food.energy_use_factor = 1 / fact(
        "Fact_I_P_other_food_ratio_fec_to_prodvol_2018"
    )
    i18.p_other_food.prod_volume = (
        i18.p_other_food.energy * i18.p_other_food.energy_use_factor
    )

    i18.p_other_food.CO2e_pb_per_t = fact(
        "Fact_I_P_other_food_ratio_CO2e_pb_to_prodvol_2018"
    )
    i18.p_other_food.CO2e_pb = (
        i18.p_other_food.prod_volume * i18.p_other_food.CO2e_pb_per_t
    )

    i18.p_other_food.CO2e_cb_per_t = fact(
        "Fact_I_P_other_food_ratio_CO2e_cb_to_prodvol_2018"
    )
    i18.p_other_food.CO2e_cb = (
        i18.p_other_food.prod_volume * i18.p_other_food.CO2e_cb_per_t
    )

    i18.p_other_food.CO2e_total = i18.p_other_food.CO2e_cb + i18.p_other_food.CO2e_pb

    # p_other_further
    i18.p_other_further.pct_energy = fact("Fact_I_P_other_fec_pct_of_further_2018")
    i18.p_other_further.energy = (
        entry("In_I_other_fec") * i18.p_other_further.pct_energy
    )
    # no prodvolume for other industries
    # i18.p_other_further.energy_use_factor =
    # i18.p_other_further.prod_volume = i18.p_other_further.energy * i18.p_other_further.energy_use_factor
    i18.p_other_further.CO2e_pb_per_MWh = fact(
        "Fact_I_P_other_2d_ratio_CO2e_pb_to_fec_2018"
    )
    i18.p_other_further.CO2e_pb = (
        i18.p_other_further.energy * i18.p_other_further.CO2e_pb_per_MWh
    )
    i18.p_other_further.CO2e_cb_per_MWh = fact(
        "Fact_I_P_other_further_ratio_CO2e_cb_to_fec_2018"
    )
    i18.p_other_further.CO2e_cb = (
        i18.p_other_further.energy * i18.p_other_further.CO2e_cb_per_MWh
    )
    i18.p_other_further.CO2e_total = (
        i18.p_other_further.CO2e_pb + i18.p_other_further.CO2e_cb
    )
    i18.p_other_further.prod_volume = fact("Fact_I_P_other_further_prodvol_2018")

    # energy of further_other_industries

    i18.p_other_2efgh.CO2e_pb_per_MWh = fact(
        "Fact_I_P_other_2efgh_ratio_CO2e_pb_to_fec_2018"
    )
    i18.p_other_2efgh.CO2e_pb = (
        i18.p_other_further.energy * i18.p_other_2efgh.CO2e_pb_per_MWh
    )
    i18.p_other_2efgh.CO2e_total = i18.p_other_2efgh.CO2e_pb

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
    i18.p_miner.CO2e_pb = (
        i18.p_miner_cement.CO2e_pb
        + i18.p_miner_chalk.CO2e_pb
        + i18.p_miner_glas.CO2e_pb
        + i18.p_miner_ceram.CO2e_pb
    )

    i18.p_chem.CO2e_pb = (
        i18.p_chem_basic.CO2e_pb + i18.p_chem_ammonia.CO2e_pb + i18.p_chem_other.CO2e_pb
    )
    i18.p_metal.CO2e_pb = i18.p_metal_steel.CO2e_pb + i18.p_metal_nonfe.CO2e_pb
    i18.p_other.energy = entry("In_I_other_fec")

    i18.p_other.CO2e_pb = (
        i18.p_other_paper.CO2e_pb
        + i18.p_other_food.CO2e_pb
        + i18.p_other_further.CO2e_pb
        + i18.p_other_2efgh.CO2e_pb
    )

    i18.p_miner.CO2e_cb = (
        i18.p_miner_cement.CO2e_cb
        + i18.p_miner_chalk.CO2e_cb
        + i18.p_miner_glas.CO2e_cb
        + i18.p_miner_ceram.CO2e_cb
    )

    i18.p_chem.CO2e_cb = (
        i18.p_chem_basic.CO2e_cb + i18.p_chem_ammonia.CO2e_cb + i18.p_chem_other.CO2e_cb
    )

    i18.p_metal.CO2e_cb = i18.p_metal_steel.CO2e_cb + i18.p_metal_nonfe.CO2e_cb

    i18.p_other.CO2e_cb = (
        i18.p_other_paper.CO2e_cb
        + i18.p_other_food.CO2e_cb
        + i18.p_other_further.CO2e_cb
    )

    i18.p.CO2e_cb = (
        i18.p_miner.CO2e_cb
        + i18.p_chem.CO2e_cb
        + i18.p_metal.CO2e_cb
        + i18.p_other.CO2e_cb
    )

    i18.p_metal.prod_volume = (
        i18.p_metal_steel.prod_volume + i18.p_metal_nonfe.prod_volume
    )

    i18.p_other.prod_volume = (
        i18.p_other_paper.prod_volume + i18.p_other_food.prod_volume
    )

    i18.p.energy = entry("In_I_energy_total")
    i18.p.prod_volume = (
        i18.p_miner.prod_volume
        + i18.p_chem.prod_volume
        + i18.p_metal.prod_volume
        + i18.p_other.prod_volume
    )

    i18.p.CO2e_pb = (
        i18.p_miner.CO2e_pb
        + i18.p_chem.CO2e_pb
        + i18.p_metal.CO2e_pb
        + i18.p_other.CO2e_pb
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

    i18.s.energy = entry("In_I_energy_total")

    i18.s_fossil_gas.energy = entry("In_I_gas_fec")
    i18.s_fossil_coal.energy = entry("In_I_coal_fec")
    i18.s_fossil_diesel.energy = entry("In_I_diesel_fec")
    i18.s_fossil_fueloil.energy = entry("In_I_fueloil_fec")
    i18.s_fossil_lpg.energy = entry("In_I_lpg_fec")
    i18.s_fossil_opetpro.energy = entry("In_I_opetpro_fec")
    i18.s_fossil_ofossil.energy = entry("In_I_ofossil_fec")

    i18.s_renew_biomass.energy = entry("In_I_biomass_fec")
    i18.s_renew_heatnet.energy = entry("In_I_heatnet_fec")
    i18.s_renew_orenew.energy = entry("In_I_orenew_fec") * fact(
        "Fact_R_S_ratio_heatpump_to_orenew_2018"
    )
    i18.s_renew_solarth.energy = entry("In_I_orenew_fec") * fact(
        "Fact_R_S_ratio_solarth_to_orenew_2018"
    )
    i18.s_renew_elec.energy = entry("In_I_elec_fec")

    i18.s_renew.energy = (
        i18.s_renew_biomass.energy
        + i18.s_renew_heatnet.energy
        + i18.s_renew_orenew.energy
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

    i18.s_fossil_gas.pct_energy = i18.s_fossil_gas.energy / i18.s.energy
    i18.s_fossil_coal.pct_energy = i18.s_fossil_coal.energy / i18.s.energy
    i18.s_fossil_diesel.pct_energy = i18.s_fossil_diesel.energy / i18.s.energy
    i18.s_fossil_fueloil.pct_energy = i18.s_fossil_fueloil.energy / i18.s.energy
    i18.s_fossil_lpg.pct_energy = i18.s_fossil_lpg.energy / i18.s.energy
    i18.s_fossil_opetpro.pct_energy = i18.s_fossil_opetpro.energy / i18.s.energy
    i18.s_fossil_ofossil.pct_energy = i18.s_fossil_ofossil.energy / i18.s.energy

    i18.s_renew_biomass.pct_energy = i18.s_renew_biomass.energy / i18.s.energy
    i18.s_renew_heatnet.pct_energy = i18.s_renew_heatnet.energy / i18.s.energy
    i18.s_renew_orenew.pct_energy = i18.s_renew_orenew.energy / i18.s.energy
    i18.s_renew_solarth.pct_energy = i18.s_renew_solarth.energy / i18.s.energy
    i18.s_renew_elec.pct_energy = i18.s_renew_elec.energy / i18.s.energy

    i18.s.pct_energy = (
        i18.s_fossil_gas.pct_energy
        + i18.s_fossil_coal.pct_energy
        + i18.s_fossil_diesel.pct_energy
        + i18.s_fossil_fueloil.pct_energy
        + i18.s_fossil_lpg.pct_energy
        + i18.s_fossil_opetpro.pct_energy
        + i18.s_fossil_ofossil.pct_energy
        + i18.s_renew_biomass.pct_energy
        + i18.s_renew_heatnet.pct_energy
        + i18.s_renew_orenew.pct_energy
        + i18.s_renew_solarth.pct_energy
        + i18.s_renew_elec.pct_energy
    )
