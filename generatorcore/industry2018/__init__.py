from ..inputs import Inputs
from ..utils import div
from .i18 import I18
from .co2e_per_t import CO2e_per_t


# for mineral industry the energy_use_factor still needs to be added to facts
def calc(inputs: Inputs) -> I18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries

    i18 = I18()

    i18.p_miner.energy = entries.i_fec_pct_of_miner * entries.i_energy_total
    i18.p_miner_cement = CO2e_per_t.calc_p_miner_cement(inputs, i18.p_miner.energy)  # type: ignore
    i18.p_miner_chalk = CO2e_per_t.calc_p_miner_chalk(inputs, i18.p_miner.energy)  # type: ignore
    i18.p_miner_glas = CO2e_per_t.calc_p_miner_glas(inputs, i18.p_miner.energy)  # type: ignore
    i18.p_miner_ceram = CO2e_per_t.calc_p_miner_ceram(inputs, i18.p_miner.energy)  # type: ignore

    i18.p_chem.energy = entries.i_fec_pct_of_chem * entries.i_energy_total
    i18.p_chem_basic = CO2e_per_t.calc_p_chem_basic(inputs, i18.p_chem.energy)  # type: ignore
    i18.p_chem_ammonia = CO2e_per_t.calc_p_chem_ammonia(inputs, i18.p_chem.energy)  # type: ignore
    i18.p_chem_other = CO2e_per_t.calc_p_chem_other(inputs, i18.p_chem.energy)  # type: ignore

    # metal
    i18.p_metal.energy = entries.i_fec_pct_of_metal * entries.i_energy_total

    # steel total (primary and secondary)
    i18.p_metal_steel.pct_energy = fact("Fact_I_P_metal_fec_pct_of_steel_2018")
    i18.p_metal_steel.energy = i18.p_metal.energy * i18.p_metal_steel.pct_energy

    # primary and secondary route
    i18.p_metal_steel_primary = CO2e_per_t.calc_p_metal_steel_primary(inputs, i18.p_metal_steel.energy)  # type: ignore
    i18.p_metal_steel_secondary = CO2e_per_t.calc_p_metal_steel_secondary(inputs, i18.p_metal_steel.energy)  # type: ignore

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

    # non fe metals
    i18.p_metal_nonfe = CO2e_per_t.calc_p_metal_nonfe(inputs, i18.p_metal.energy)  # type: ignore

    # p_other
    i18.p_other.energy = entries.i_fec_pct_of_other * entries.i_energy_total
    i18.p_other_paper = CO2e_per_t.calc_p_other_paper(inputs, i18.p_other.energy)  # type: ignore
    i18.p_other_food = CO2e_per_t.calc_p_other_food(inputs, i18.p_other.energy)  # type: ignore

    # p_other_further
    i18.p_other_further.pct_energy = fact("Fact_I_P_other_fec_pct_of_further_2018")
    i18.p_other_further.energy = i18.p_other.energy * i18.p_other_further.pct_energy
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

    i18.s_fossil_gas.pct_energy = div(i18.s_fossil_gas.energy, i18.s.energy)
    i18.s_fossil_coal.pct_energy = div(i18.s_fossil_coal.energy, i18.s.energy)
    i18.s_fossil_diesel.pct_energy = div(i18.s_fossil_diesel.energy, i18.s.energy)
    i18.s_fossil_fueloil.pct_energy = div(i18.s_fossil_fueloil.energy, i18.s.energy)
    i18.s_fossil_lpg.pct_energy = div(i18.s_fossil_lpg.energy, i18.s.energy)
    i18.s_fossil_opetpro.pct_energy = div(i18.s_fossil_opetpro.energy, i18.s.energy)
    i18.s_fossil_ofossil.pct_energy = div(i18.s_fossil_ofossil.energy, i18.s.energy)

    i18.s_renew_biomass.pct_energy = div(i18.s_renew_biomass.energy, i18.s.energy)
    i18.s_renew_heatnet.pct_energy = div(i18.s_renew_heatnet.energy, i18.s.energy)
    i18.s_renew_heatpump.pct_energy = div(i18.s_renew_heatpump.energy, i18.s.energy)
    i18.s_renew_solarth.pct_energy = div(i18.s_renew_solarth.energy, i18.s.energy)
    i18.s_renew_elec.pct_energy = div(i18.s_renew_elec.energy, i18.s.energy)

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
        + i18.s_renew_heatpump.pct_energy
        + i18.s_renew_solarth.pct_energy
        + i18.s_renew_elec.pct_energy
    )

    i18.i.prod_volume = i18.p.prod_volume
    i18.i.CO2e_production_based = i18.p.CO2e_production_based
    i18.i.CO2e_combustion_based = i18.p.CO2e_combustion_based
    i18.i.CO2e_total = i18.p.CO2e_total
    i18.i.energy = i18.p.energy

    return i18
