# pyright: strict
from dataclasses import dataclass
from .co2e import CO2e
from .co2e_per_t import CO2e_per_t
from .co2e_with_pct_energy import CO2e_with_pct_energy
from .co2e_per_mwh import CO2e_per_MWh
from .co2e_basic import CO2e_basic
from .energy_sum import EnergySum, Energy_pct


@dataclass(kw_only=True)
class I18:
    i: CO2e
    p: CO2e

    p_miner: CO2e
    p_miner_cement: CO2e_per_t
    p_miner_chalk: CO2e_per_t
    p_miner_glas: CO2e_per_t
    p_miner_ceram: CO2e_per_t

    p_chem: CO2e
    p_chem_basic: CO2e_per_t
    p_chem_ammonia: CO2e_per_t
    p_chem_other: CO2e_per_t

    p_metal: CO2e
    p_metal_steel: CO2e_with_pct_energy
    p_metal_steel_primary: CO2e_per_t
    p_metal_steel_secondary: CO2e_per_t
    p_metal_nonfe: CO2e_per_t

    p_other: CO2e
    p_other_paper: CO2e_per_t
    p_other_food: CO2e_per_t
    p_other_further: CO2e_per_MWh
    p_other_2efgh: CO2e_basic

    s: Energy_pct
    s_fossil: EnergySum
    s_fossil_gas: Energy_pct
    s_fossil_coal: Energy_pct
    s_fossil_diesel: Energy_pct
    s_fossil_fueloil: Energy_pct
    s_fossil_lpg: Energy_pct
    s_fossil_opetpro: Energy_pct
    s_fossil_ofossil: Energy_pct
    s_renew: EnergySum
    s_renew_biomass: Energy_pct
    s_renew_heatnet: Energy_pct
    s_renew_heatpump: Energy_pct
    s_renew_solarth: Energy_pct
    s_renew_elec: Energy_pct
