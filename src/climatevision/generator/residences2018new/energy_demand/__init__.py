# pyright: strict

from dataclasses import dataclass

from ...makeentries import Entries
from ...refdata import Facts, Assumptions

from .dataclasses import Vars1


@dataclass(kw_only=True)
class Production:
    total: float = Vars1  # type: ignore
    heating: float = None  # type: ignore
    heating_fossil: float = None  # type: ignore
    heating_fossil_gas: Vars1
    heating_fossil_lpg: Vars1
    heating_fossil_fueloil: Vars1
    heating_fossil_coal: Vars1
    heating_renew: float = None  # type: ignore
    heating_renew_heatnet: Vars1
    heating_renew_biomass: Vars1
    heating_renew_elec_heating: Vars1
    heating_renew_elec_heatpump: Vars1
    heating_renew_without_heating: Vars1


def calc_production(
    entries: Entries, facts: Facts, assumptions: Assumptions
) -> Production:
    fact = facts.fact
    
    #TODO: neue Fakten müssen noch in data facts hinzugefügt werden

    heating = 0
    heating_fossil=0 #TODO: Summe
    heating_fossil_gas=Vars1(number_of_flats = entries.r_new_flats_gas, number_of_buildings=entries.r_new_buildings_gas, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_gas_factor_adapted_to_fec"))
    heating_fossil_lpg=Vars1(number_of_flats = entries.r_new_flats_lpg, number_of_buildings=entries.r_new_buildings_lpg, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_lpg_factor_adapted_to_fec"))
    heating_fossil_fueloil=Vars1(number_of_flats = entries.r_new_flats_fueloil, number_of_buildings=entries.r_new_buildings_fueloil, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_fueloil_factor_adapted_to_fec"))
    heating_fossil_coal=Vars1(number_of_flats = entries.r_new_flats_coal, number_of_buildings=entries.r_new_buildings_coal, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_coal_factor_adapted_to_fec"))
    heating_renew=0 #TODO: Summe
    heating_renew_heatnet=Vars1(number_of_flats = entries.r_new_flats_heatnet, number_of_buildings=entries.r_new_buildings_heatnet, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_heatnet_factor_adapted_to_fec"))
    heating_renew_biomass=Vars1(number_of_flats = entries.r_new_flats_biomass, number_of_buildings=entries.r_new_buildings_biomass, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_biomass_factor_adapted_to_fec"))
    heating_renew_elec_heating=Vars1(number_of_flats = entries.r_new_flats_elec_heating, number_of_buildings=entries.r_new_buildings_elec_heating, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_elec_heating_factor_adapted_to_fec"))
    heating_renew_elec_heatpump=Vars1(number_of_flats = entries.r_new_flats_elec_heatpump, number_of_buildings=entries.r_new_buildings_elec_heatpump, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_elec_heatpump_factor_adapted_to_fec"))
    heating_renew_without_heating=Vars1(number_of_flats = entries.r_new_flats_wo_heating, number_of_buildings=entries.r_new_buildings_without_heating, ratio_area_m2_to_flat = entries.r_new_ratio_area_m2_to_flat, factor_adapted_to_fec = fact("Fact_R_P_without_heating_factor_adapted_to_fec"))

    return Production(
        heating=heating,
        heating_fossil=heating_fossil,
        heating_fossil_gas=heating_fossil_gas,
        heating_fossil_lpg=heating_fossil_lpg,
        heating_fossil_fueloil=heating_fossil_fueloil,
        heating_fossil_coal=heating_fossil_coal,
        heating_renew=heating_renew,
        heating_renew_heatnet=heating_renew_heatnet,
        heating_renew_biomass=heating_renew_biomass,
        heating_renew_elec_heating=heating_renew_elec_heating,
        heating_renew_elec_heatpump=heating_renew_elec_heatpump,
        heating_renew_without_heating=heating_renew_without_heating,
        )
