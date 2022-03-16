from ..inputs import Inputs
from ..utils import div
from .i18 import I18
from .co2e_per_t import CO2e_per_t
from .co2e_basic import CO2e_basic
from .co2e_per_mwh import CO2e_per_MWh
from .co2e_with_pct_energy import CO2e_with_pct_energy


# for mineral industry the energy_use_factor still needs to be added to facts
def calc(inputs: Inputs) -> I18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries

    i18 = I18()

    p_miner_energy = entries.i_fec_pct_of_miner * entries.i_energy_total
    i18.p_miner_cement = CO2e_per_t.calc_p_miner_cement(inputs, p_miner_energy)  # type: ignore
    i18.p_miner_chalk = CO2e_per_t.calc_p_miner_chalk(inputs, p_miner_energy)  # type: ignore
    i18.p_miner_glas = CO2e_per_t.calc_p_miner_glas(inputs, p_miner_energy)  # type: ignore
    i18.p_miner_ceram = CO2e_per_t.calc_p_miner_ceram(inputs, p_miner_energy)  # type: ignore
    i18.p_miner = (
        i18.p_miner_cement + i18.p_miner_chalk + i18.p_miner_glas + i18.p_miner_ceram
    )

    p_chem_energy = entries.i_fec_pct_of_chem * entries.i_energy_total
    i18.p_chem_basic = CO2e_per_t.calc_p_chem_basic(inputs, p_chem_energy)  # type: ignore
    i18.p_chem_ammonia = CO2e_per_t.calc_p_chem_ammonia(inputs, p_chem_energy)  # type: ignore
    i18.p_chem_other = CO2e_per_t.calc_p_chem_other(inputs, p_chem_energy)  # type: ignore
    i18.p_chem = i18.p_chem_basic + i18.p_chem_ammonia + i18.p_chem_other

    p_metal_energy = entries.i_fec_pct_of_metal * entries.i_energy_total
    p_metal_steel_pct_energy = fact("Fact_I_P_metal_fec_pct_of_steel_2018")
    p_metal_steel_energy = p_metal_energy * p_metal_steel_pct_energy
    i18.p_metal_steel_primary = CO2e_per_t.calc_p_metal_steel_primary_route(inputs, p_metal_steel_energy)  # type: ignore
    i18.p_metal_steel_secondary = CO2e_per_t.calc_p_metal_steel_secondary_route(inputs, p_metal_steel_energy)  # type: ignore
    i18.p_metal_steel = CO2e_with_pct_energy.calc_p_metal_steel(inputs, p_metal_steel_pct_energy, p_metal_steel_energy, i18.p_metal_steel_primary, i18.p_metal_steel_secondary)  # type: ignore
    i18.p_metal_nonfe = CO2e_per_t.calc_p_metal_non_fe(inputs, p_metal_energy)  # type: ignore
    i18.p_metal = i18.p_metal_steel + i18.p_metal_nonfe
    i18.p_metal.energy = p_metal_energy

    p_other_energy = entries.i_fec_pct_of_other * entries.i_energy_total
    i18.p_other_paper = CO2e_per_t.calc_p_other_paper(inputs, p_other_energy)  # type: ignore
    i18.p_other_food = CO2e_per_t.calc_p_other_food(inputs, p_other_energy)  # type: ignore
    i18.p_other_further = CO2e_per_MWh.calc_p_other_further(inputs, p_other_energy)  # type: ignore
    i18.p_other_2efgh = CO2e_basic.calc_p_other_2efgh(inputs, i18.p_other_further.energy)  # type: ignore
    i18.p_other = i18.p_other_paper + i18.p_other_food
    i18.p_other.energy = p_other_energy

    i18.p_other.CO2e_combustion_based += +i18.p_other_further.CO2e_combustion_based
    i18.p_other.CO2e_production_based += (
        +i18.p_other_further.CO2e_production_based
        + i18.p_other_2efgh.CO2e_production_based
    )
    i18.p_other.CO2e_total += (
        +i18.p_other_further.CO2e_total + i18.p_other_2efgh.CO2e_total
    )

    i18.p = i18.p_miner + i18.p_chem + i18.p_metal + i18.p_other
    i18.p.energy = entries.i_energy_total

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
