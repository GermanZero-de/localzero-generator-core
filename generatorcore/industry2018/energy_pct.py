from dataclasses import dataclass


@dataclass
class Energy_pct:
    # Used by s, s_fossil_gas, s_fossil_coal, s_fossil_diesel, s_fossil_fueloil, s_fossil_lpg, s_fossil_opetpro, s_fossil_ofossil, s_renew_biomass, s_renew_heatnet, s_renew_heatpump, s_renew_solarth, s_renew_elec
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
