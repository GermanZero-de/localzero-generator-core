# pyright: strict
from generatorcore.industry2018.co2e import CO2e
from generatorcore.industry2018.empty import Empty
from ..inputs import Inputs
from .i18 import I18
from .co2e_per_t import CO2e_per_t
from .co2e_basic import CO2e_basic
from .co2e_per_mwh import CO2e_per_MWh
from .co2e_with_pct_energy import CO2e_with_pct_energy
from .energy_pct import Energy_pct
from .energy_sum import EnergySum


# for mineral industry the energy_use_factor still needs to be added to facts
def calc(inputs: Inputs) -> I18:
    fact = inputs.fact
    entries = inputs.entries

    p_miner_energy = entries.i_fec_pct_of_miner * entries.i_energy_total
    p_miner_cement = CO2e_per_t.calc_p_miner_cement(inputs, p_miner_energy)
    p_miner_chalk = CO2e_per_t.calc_p_miner_chalk(inputs, p_miner_energy)
    p_miner_glas = CO2e_per_t.calc_p_miner_glas(inputs, p_miner_energy)
    p_miner_ceram = CO2e_per_t.calc_p_miner_ceram(inputs, p_miner_energy)
    p_miner = p_miner_cement + p_miner_chalk + p_miner_glas + p_miner_ceram

    p_chem_energy = entries.i_fec_pct_of_chem * entries.i_energy_total
    p_chem_basic = CO2e_per_t.calc_p_chem_basic(inputs, p_chem_energy)
    p_chem_ammonia = CO2e_per_t.calc_p_chem_ammonia(inputs, p_chem_energy)
    p_chem_other = CO2e_per_t.calc_p_chem_other(inputs, p_chem_energy)
    p_chem = p_chem_basic + p_chem_ammonia + p_chem_other

    p_metal_energy = entries.i_fec_pct_of_metal * entries.i_energy_total
    p_metal_steel_pct_energy = fact("Fact_I_P_metal_fec_pct_of_steel_2018")
    p_metal_steel_energy = p_metal_energy * p_metal_steel_pct_energy
    p_metal_steel_primary = CO2e_per_t.calc_p_metal_steel_primary_route(
        inputs, p_metal_steel_energy
    )
    p_metal_steel_secondary = CO2e_per_t.calc_p_metal_steel_secondary_route(
        inputs, p_metal_steel_energy
    )
    p_metal_steel = CO2e_with_pct_energy.calc_p_metal_steel(
        inputs,
        p_metal_steel_pct_energy,
        p_metal_steel_energy,
        p_metal_steel_primary,
        p_metal_steel_secondary,
    )
    p_metal_nonfe = CO2e_per_t.calc_p_metal_non_fe(inputs, p_metal_energy)
    p_metal = p_metal_steel + p_metal_nonfe
    p_metal.energy = p_metal_energy

    p_other_energy = entries.i_fec_pct_of_other * entries.i_energy_total
    p_other_paper = CO2e_per_t.calc_p_other_paper(inputs, p_other_energy)
    p_other_food = CO2e_per_t.calc_p_other_food(inputs, p_other_energy)
    p_other_further = CO2e_per_MWh.calc_p_other_further(inputs, p_other_energy)
    p_other_2efgh = CO2e_basic.calc_p_other_2efgh(inputs, p_other_further.energy)
    p_other = p_other_paper + p_other_food
    p_other.energy = p_other_energy

    p_other.CO2e_combustion_based += +p_other_further.CO2e_combustion_based
    p_other.CO2e_production_based += (
        +p_other_further.CO2e_production_based + p_other_2efgh.CO2e_production_based
    )
    p_other.CO2e_total += +p_other_further.CO2e_total + p_other_2efgh.CO2e_total

    p = p_miner + p_chem + p_metal + p_other
    p.energy = entries.i_energy_total

    s = Energy_pct(energy=entries.i_energy_total, total_energy=entries.i_energy_total)

    s_fossil_gas = Energy_pct(energy=entries.i_gas_fec, total_energy=s.energy)
    s_fossil_coal = Energy_pct(energy=entries.i_coal_fec, total_energy=s.energy)
    s_fossil_diesel = Energy_pct(energy=entries.i_diesel_fec, total_energy=s.energy)
    s_fossil_fueloil = Energy_pct(energy=entries.i_fueloil_fec, total_energy=s.energy)
    s_fossil_lpg = Energy_pct(energy=entries.i_lpg_fec, total_energy=s.energy)
    s_fossil_opetpro = Energy_pct(energy=entries.i_opetpro_fec, total_energy=s.energy)
    s_fossil_ofossil = Energy_pct(energy=entries.i_ofossil_fec, total_energy=s.energy)

    s_renew_biomass = Energy_pct(energy=entries.i_biomass_fec, total_energy=s.energy)
    s_renew_heatnet = Energy_pct(energy=entries.i_heatnet_fec, total_energy=s.energy)
    s_renew_heatpump = Energy_pct(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_heatpump_to_orenew_2018"),
        total_energy=s.energy,
    )
    s_renew_solarth = Energy_pct(
        energy=entries.i_orenew_fec * fact("Fact_R_S_ratio_solarth_to_orenew_2018"),
        total_energy=s.energy,
    )
    s_renew_elec = Energy_pct(energy=entries.i_elec_fec, total_energy=s.energy)
    s_renew_hydrogen = Empty()
    s_renew_emethan = Empty()

    s_renew = EnergySum(
        s_renew_biomass.energy
        + s_renew_heatnet.energy
        + s_renew_heatpump.energy
        + s_renew_solarth.energy
        + s_renew_elec.energy
    )

    s_fossil = EnergySum(
        s_fossil_gas.energy
        + s_fossil_coal.energy
        + s_fossil_diesel.energy
        + s_fossil_fueloil.energy
        + s_fossil_lpg.energy
        + s_fossil_opetpro.energy
        + s_fossil_ofossil.energy
    )

    i = CO2e()
    i.prod_volume = p.prod_volume
    i.CO2e_production_based = p.CO2e_production_based
    i.CO2e_combustion_based = p.CO2e_combustion_based
    i.CO2e_total = p.CO2e_total
    i.energy = p.energy

    return I18(
        i=i,
        p=p,
        p_miner=p_miner,
        p_miner_cement=p_miner_cement,
        p_miner_chalk=p_miner_chalk,
        p_miner_glas=p_miner_glas,
        p_miner_ceram=p_miner_ceram,
        p_chem=p_chem,
        p_chem_basic=p_chem_basic,
        p_chem_ammonia=p_chem_ammonia,
        p_chem_other=p_chem_other,
        p_metal=p_metal,
        p_metal_steel=p_metal_steel,
        p_metal_steel_primary=p_metal_steel_primary,
        p_metal_steel_secondary=p_metal_steel_secondary,
        p_metal_nonfe=p_metal_nonfe,
        p_other=p_other,
        p_other_paper=p_other_paper,
        p_other_food=p_other_food,
        p_other_further=p_other_further,
        p_other_2efgh=p_other_2efgh,
        s=s,
        s_fossil=s_fossil,
        s_fossil_gas=s_fossil_gas,
        s_fossil_coal=s_fossil_coal,
        s_fossil_diesel=s_fossil_diesel,
        s_fossil_fueloil=s_fossil_fueloil,
        s_fossil_lpg=s_fossil_lpg,
        s_fossil_opetpro=s_fossil_opetpro,
        s_fossil_ofossil=s_fossil_ofossil,
        s_renew=s_renew,
        s_renew_hydrogen=s_renew_hydrogen,
        s_renew_emethan=s_renew_emethan,
        s_renew_biomass=s_renew_biomass,
        s_renew_heatnet=s_renew_heatnet,
        s_renew_heatpump=s_renew_heatpump,
        s_renew_solarth=s_renew_solarth,
        s_renew_elec=s_renew_elec,
    )
