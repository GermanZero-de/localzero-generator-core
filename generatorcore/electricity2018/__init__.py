from ..inputs import Inputs
from ..utils import div
from .. import transport2018
from .e18 import E18


def calc(inputs: Inputs, *, t18: transport2018.T18) -> E18:
    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    Million = 1000000

    e18 = E18()

    """variable abbrevations"""
    e = e18.e
    d = e18.d
    d_r = e18.d_r
    d_b = e18.d_b
    d_i = e18.d_i
    d_t = e18.d_t
    d_a = e18.d_a
    d_h = e18.d_h
    d_f_hydrogen_reconv = e18.d_f_hydrogen_reconv
    p = e18.p
    p_fossil = e18.p_fossil
    p_fossil_nuclear = e18.p_fossil_nuclear
    p_fossil_coal_brown = e18.p_fossil_coal_brown
    p_fossil_coal_brown_cogen = e18.p_fossil_coal_brown_cogen
    p_fossil_coal_black = e18.p_fossil_coal_black
    p_fossil_coal_black_cogen = e18.p_fossil_coal_black_cogen
    p_fossil_gas = e18.p_fossil_gas
    p_fossil_gas_cogen = e18.p_fossil_gas_cogen
    p_fossil_ofossil = e18.p_fossil_ofossil
    p_fossil_ofossil_cogen = e18.p_fossil_ofossil_cogen
    p_renew = e18.p_renew
    p_renew_geoth = e18.p_renew_geoth
    p_renew_hydro = e18.p_renew_hydro
    p_renew_pv = e18.p_renew_pv
    p_renew_pv_roof = e18.p_renew_pv_roof
    p_renew_pv_facade = e18.p_renew_pv_facade
    p_renew_pv_park = e18.p_renew_pv_park
    p_renew_wind = e18.p_renew_wind
    p_renew_wind_onshore = e18.p_renew_wind_onshore
    p_renew_wind_offshore = e18.p_renew_wind_offshore
    p_renew_biomass = e18.p_renew_biomass
    p_renew_biomass_waste = e18.p_renew_biomass_waste
    p_renew_biomass_solid = e18.p_renew_biomass_solid
    p_renew_biomass_gaseous = e18.p_renew_biomass_gaseous
    p_renew_biomass_cogen = e18.p_renew_biomass_cogen
    p_renew_pv_agri = e18.p_renew_pv_agri
    p_renew_reverse = e18.p_renew_reverse
    p_fossil_and_renew = e18.p_fossil_and_renew
    p_local_pv_roof = e18.p_local_pv_roof
    p_local_pv_facade = e18.p_local_pv_facade
    p_local_pv_park = e18.p_local_pv_park
    p_local_pv_agri = e18.p_local_pv_agri
    p_local_pv = e18.p_local_pv
    p_local_wind_onshore = e18.p_local_wind_onshore
    p_local_biomass = e18.p_local_biomass
    p_local_biomass_cogen = e18.p_local_biomass_cogen
    p_local_hydro = e18.p_local_hydro
    p_local = e18.p_local

    d_h.energy = 0
    d_f_hydrogen_reconv.energy = 0
    d_r.energy = entries.r_elec_fec
    d_r.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    d_r.cost_fuel = d_r.cost_fuel_per_MWh * d_r.energy / Million
    d_b.energy = entries.b_elec_fec
    d_b.cost_fuel_per_MWh = fact("Fact_E_D_B_cost_fuel_per_MWh_2018")
    d_b.cost_fuel = d_b.cost_fuel_per_MWh * d_b.energy / 1000000
    d_i.energy = entries.i_elec_fec
    d_i.cost_fuel_per_MWh = fact("Fact_E_D_I_cost_fuel_per_MWh_2018")
    d_i.cost_fuel = d_i.energy * d_i.cost_fuel_per_MWh / 1000000
    d_t.energy = t18.t.demand_electricity
    d_t.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    d_t.cost_fuel = d_t.energy * d_t.cost_fuel_per_MWh / 1000000
    d_a.energy = entries.a_elec_fec
    d.energy = d_r.energy + d_b.energy + d_i.energy + d_t.energy + d_a.energy
    d.cost_fuel = d_r.cost_fuel + d_b.cost_fuel + d_i.cost_fuel + d_t.cost_fuel
    p.energy = d.energy

    p_renew_wind_onshore.CO2e_combustion_based = 0.0
    p_renew_wind_onshore.CO2e_combustion_based_per_MWh = 0.0
    p_renew_wind_onshore.CO2e_total = 0.0
    p_renew_wind_onshore.pct_energy = fact("Fact_E_P_wind_onshore_pct_of_gep_2018")
    p_renew_wind_onshore.energy = p_renew_wind_onshore.pct_energy * p.energy
    p_renew_wind_onshore.cost_mro_per_MWh = (
        ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_wind_onshore_mro_per_year")
        / fact("Fact_E_P_wind_onshore_full_load_hours")
        * 1000
    )
    p_renew_wind_onshore.cost_mro = (
        p_renew_wind_onshore.cost_mro_per_MWh
        * p_renew_wind_onshore.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_renew_wind_offshore.CO2e_combustion_based = 0.0
    p_renew_wind_offshore.CO2e_combustion_based_per_MWh = 0.0
    p_renew_wind_offshore.CO2e_total = 0.0
    p_renew_wind_offshore.pct_energy = fact("Fact_E_P_wind_offshore_pct_of_gep_2018")
    p_renew_wind_offshore.energy = p_renew_wind_offshore.pct_energy * p.energy
    p_renew_wind_offshore.cost_mro_per_MWh = (
        ass("Ass_E_P_renew_wind_offshore_ratio_invest_to_power_2020")
        * ass("Ass_E_P_renew_wind_offshore_mro_per_year")
        / fact("Fact_E_P_wind_offshore_full_load_hours")
        * 1000
    )
    p_renew_wind_offshore.cost_mro = (
        p_renew_wind_offshore.cost_mro_per_MWh
        * p_renew_wind_offshore.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_renew_wind.CO2e_combustion_based = 0.0
    p_renew_wind.pct_energy = fact("Fact_E_P_wind_pct_of_gep_2018")
    p_renew_wind.energy = d.energy * p_renew_wind.pct_energy
    p_renew_wind.cost_mro = (
        p_renew_wind_onshore.cost_mro + p_renew_wind_offshore.cost_mro
    )
    p_renew_wind.CO2e_total = 0

    p_renew_reverse.energy = 0.0

    p_local_wind_onshore.CO2e_combustion_based = 0.0
    p_local_wind_onshore.CO2e_combustion_based_per_MWh = 0.0
    p_local_wind_onshore.CO2e_total = 0.0
    p_local_wind_onshore.energy = (
        entries.e_PV_power_inst_wind_on
        * fact("Fact_E_P_wind_onshore_full_load_hours")
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_wind_onshore.cost_mro_per_MWh = (
        ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_wind_onshore_mro_per_year")
        / fact("Fact_E_P_wind_onshore_full_load_hours")
        * 1000
    )
    p_local_wind_onshore.cost_mro = (
        p_local_wind_onshore.energy * p_local_wind_onshore.cost_mro_per_MWh / Million
    )

    p_local_biomass.CO2e_total = 0.0
    p_local_biomass.energy = (
        entries.e_PV_power_inst_biomass
        * fact("Fact_E_P_biomass_full_load_hours")
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_biomass.cost_mro_per_MWh = ass("Ass_E_P_local_biomass_mro_per_MWh")
    p_local_biomass.cost_mro = (
        p_local_biomass.energy * p_local_biomass.cost_mro_per_MWh / Million
    )
    p_local_biomass.cost_fuel_per_MWh = ass(
        "Ass_E_P_local_biomass_material_costs"
    ) / ass("Ass_E_P_local_biomass_efficiency")
    p_local_biomass.cost_fuel = (
        p_local_biomass.cost_fuel_per_MWh * p_local_biomass.energy / 1000000
    )
    p_local_biomass.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_local_biomass.CO2e_combustion_based = (
        p_local_biomass.CO2e_combustion_based_per_MWh * p_local_biomass.energy
    )

    p_local_hydro.CO2e_combustion_based = 0.0
    p_local_hydro.CO2e_combustion_based_per_MWh = 0.0
    p_local_hydro.CO2e_total = 0.0
    p_local_hydro.energy = (
        entries.e_PV_power_inst_water
        * fact("Fact_E_P_hydro_full_load_hours")
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")
    p_local_hydro.cost_mro = (
        p_local_hydro.energy * p_local_hydro.cost_mro_per_MWh / Million
    )

    p.energy = d.energy

    p_fossil_nuclear.pct_energy = fact("Fact_E_P_nuclear_pct_of_gep_2018")
    p_fossil_nuclear.energy = p.energy * p_fossil_nuclear.pct_energy
    p_fossil_nuclear.cost_fuel_per_MWh = ass(
        "Ass_E_P_fossil_nuclear_cost_fuel_per_MWh"
    ) / ass("Ass_E_P_fossil_nuclear_efficiency")
    p_fossil_nuclear.cost_fuel = (
        p_fossil_nuclear.cost_fuel_per_MWh
        * p_fossil_nuclear.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_nuclear.CO2e_combustion_based_per_MWh = 0
    p_fossil_nuclear.CO2e_combustion_based = (
        p_fossil_nuclear.CO2e_combustion_based_per_MWh
        * p_fossil_nuclear.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    )
    p_fossil_nuclear.cost_mro_per_MWh = ass("Ass_E_P_fossil_nuclear_mro_per_MW") / fact(
        "Fact_E_P_nuclear_full_load_hours"
    )
    p_fossil_nuclear.cost_mro = (
        p_fossil_nuclear.cost_mro_per_MWh
        * p_fossil_nuclear.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_nuclear.cost_certificate_per_MWh = 0
    p_fossil_nuclear.cost_certificate = (
        p_fossil_nuclear.cost_certificate_per_MWh * p_fossil_nuclear.energy / 1000000
    )
    p_fossil_nuclear.CO2e_total = p_fossil_nuclear.CO2e_combustion_based
    p_fossil_coal_brown.pct_energy = fact("Fact_E_P_coal_brown_pct_of_gep_2018")
    p_fossil_coal_brown.energy = p.energy * p_fossil_coal_brown.pct_energy
    p_fossil_coal_brown.cost_fuel_per_MWh = ass(
        "Ass_E_P_fossil_coal_brown_cost_fuel_per_MWh"
    ) / ass("Ass_E_P_fossil_coal_black_efficiency")
    p_fossil_coal_brown.cost_fuel = (
        p_fossil_coal_brown.cost_fuel_per_MWh
        * p_fossil_coal_brown.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_coal_brown.cost_certificate_per_MWh = (
        fact("Fact_E_P_coal_brown_ratio_CO2e_cb_to_gep_2018")
        * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
        * 1000
    )
    p_fossil_coal_brown.cost_certificate = (
        p_fossil_coal_brown.cost_certificate_per_MWh
        * p_fossil_coal_brown.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_coal_brown.cost_mro_per_MWh = ass(
        "Ass_E_P_fossil_coal_brown_mro_per_MW"
    ) / fact("Fact_E_P_coal_brown_full_load_hours")
    p_fossil_coal_brown.cost_mro = (
        p_fossil_coal_brown.cost_mro_per_MWh
        * p_fossil_coal_brown.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_coal_brown.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_coal_brown_ratio_CO2e_cb_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_fossil_coal_brown.CO2e_combustion_based = (
        p_fossil_coal_brown.CO2e_combustion_based_per_MWh * p_fossil_coal_brown.energy
    )
    p_fossil_coal_brown.CO2e_total = p_fossil_coal_brown.CO2e_combustion_based
    p_fossil_coal_brown_cogen.pct_energy = fact("Fact_E_P_coal_brown_cogen_ratio_2018")
    p_fossil_coal_brown_cogen.energy = (
        p_fossil_coal_brown.energy * p_fossil_coal_brown_cogen.pct_energy
    )
    p_fossil_coal_black.pct_energy = fact("Fact_E_P_coal_black_pct_of_gep_2018")
    p_fossil_coal_black.energy = p.energy * p_fossil_coal_black.pct_energy
    p_fossil_coal_black.cost_fuel_per_MWh = ass(
        "Ass_E_P_fossil_coal_black_cost_fuel_per_MWh"
    ) / ass("Ass_E_P_fossil_coal_black_efficiency")
    p_fossil_coal_black.cost_fuel = (
        p_fossil_coal_black.cost_fuel_per_MWh
        * p_fossil_coal_black.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_coal_black.cost_certificate_per_MWh = (
        fact("Fact_E_P_coal_black_ratio_CO2e_cb_to_gep_2018")
        * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
        * 1000
    )
    p_fossil_coal_black.cost_certificate = (
        p_fossil_coal_black.cost_certificate_per_MWh
        * p_fossil_coal_black.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_coal_black.cost_mro_per_MWh = ass(
        "Ass_E_P_fossil_coal_black_mro_per_MW"
    ) / fact("Fact_E_P_coal_black_full_load_hours")
    p_fossil_coal_black.cost_mro = (
        p_fossil_coal_black.cost_mro_per_MWh
        * p_fossil_coal_black.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_coal_black.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_coal_black_ratio_CO2e_cb_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_fossil_coal_black.CO2e_combustion_based = (
        p_fossil_coal_black.CO2e_combustion_based_per_MWh * p_fossil_coal_black.energy
    )
    p_fossil_coal_black.CO2e_total = p_fossil_coal_black.CO2e_combustion_based
    p_fossil_coal_black_cogen.pct_energy = fact("Fact_E_P_coal_black_cogen_ratio_2018")
    p_fossil_coal_black_cogen.energy = (
        p_fossil_coal_black.energy * p_fossil_coal_black_cogen.pct_energy
    )
    p_fossil_gas.pct_energy = fact("Fact_E_P_gas_pct_of_gep_2018")
    p_fossil_gas.energy = p.energy * p_fossil_gas.pct_energy
    p_fossil_gas.cost_fuel_per_MWh = ass(
        "Ass_E_P_renew_reverse_gud_cost_fuel_per_MWh"
    ) / ass("Ass_E_P_renew_reverse_gud_efficiency")
    p_fossil_gas.cost_fuel = (
        p_fossil_gas.cost_fuel_per_MWh
        * p_fossil_gas.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_gas.cost_certificate_per_MWh = (
        fact("Fact_E_P_gas_ratio_CO2e_cb_to_gep_2018")
        * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
        * 1000
    )
    p_fossil_gas.cost_certificate = (
        p_fossil_gas.cost_certificate_per_MWh
        * p_fossil_gas.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_gas.cost_mro_per_MWh = ass(
        "Ass_E_P_renew_reverse_gud_cost_mro_per_MW"
    ) / fact("Fact_E_P_gas_full_load_hours")
    p_fossil_gas.cost_mro = (
        p_fossil_gas.cost_mro_per_MWh
        * p_fossil_gas.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_gas.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_gas_ratio_CO2e_cb_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_fossil_gas.CO2e_combustion_based = (
        p_fossil_gas.CO2e_combustion_based_per_MWh * p_fossil_gas.energy
    )
    p_fossil_gas.CO2e_total = p_fossil_gas.CO2e_combustion_based
    p_fossil_gas_cogen.pct_energy = fact("Fact_E_P_gas_cogen_ratio_2018")
    p_fossil_gas_cogen.energy = p_fossil_gas.energy * p_fossil_gas_cogen.pct_energy
    p_fossil_ofossil.pct_energy = fact("Fact_E_P_ofossil_pct_of_gep_2018")
    p_fossil_ofossil.energy = p.energy * p_fossil_ofossil.pct_energy
    p_fossil_ofossil.cost_fuel_per_MWh = p_fossil_coal_brown.cost_fuel_per_MWh
    p_fossil_ofossil.cost_fuel = (
        p_fossil_ofossil.cost_fuel_per_MWh
        * p_fossil_ofossil.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_ofossil.cost_certificate_per_MWh = (
        fact("Fact_E_P_ofossil_ratio_CO2e_cb_to_gep_2018")
        * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
        * 1000
    )
    p_fossil_ofossil.cost_certificate = (
        p_fossil_ofossil.cost_certificate_per_MWh
        * p_fossil_ofossil.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_ofossil.cost_mro_per_MWh = p_fossil_coal_brown.cost_mro_per_MWh
    p_fossil_ofossil.cost_mro = (
        p_fossil_ofossil.cost_mro_per_MWh
        * p_fossil_ofossil.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_fossil_ofossil.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_ofossil_ratio_CO2e_cb_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_fossil_ofossil.CO2e_combustion_based = (
        p_fossil_ofossil.CO2e_combustion_based_per_MWh * p_fossil_ofossil.energy
    )
    p_fossil_ofossil.CO2e_total = 0
    p_fossil_ofossil.CO2e_total = p_fossil_ofossil.CO2e_combustion_based
    p_fossil_ofossil_cogen.pct_energy = fact("Fact_E_P_ofossil_cogen_ratio_2018")
    p_fossil_ofossil_cogen.energy = (
        p_fossil_ofossil.energy * p_fossil_ofossil_cogen.pct_energy
    )
    p_fossil.energy = (
        p_fossil_nuclear.energy
        + p_fossil_coal_brown.energy
        + p_fossil_coal_black.energy
        + p_fossil_gas.energy
        + p_fossil_ofossil.energy
    )
    p_fossil.pct_energy = div(p_fossil.energy, p.energy)
    p_fossil.cost_fuel = (
        p_fossil_nuclear.cost_fuel
        + p_fossil_coal_brown.cost_fuel
        + p_fossil_coal_black.cost_fuel
        + p_fossil_gas.cost_fuel
        + p_fossil_ofossil.cost_fuel
    )
    p_fossil.cost_certificate = (
        p_fossil_nuclear.cost_certificate
        + p_fossil_coal_brown.cost_certificate
        + p_fossil_coal_black.cost_certificate
        + p_fossil_gas.cost_certificate
        + p_fossil_ofossil.cost_certificate
    )
    p_fossil.cost_mro = (
        p_fossil_nuclear.cost_mro
        + p_fossil_coal_brown.cost_mro
        + p_fossil_coal_black.cost_mro
        + p_fossil_gas.cost_mro
        + p_fossil_ofossil.cost_mro
    )
    p_fossil.CO2e_combustion_based = (
        p_fossil_nuclear.CO2e_combustion_based
        + p_fossil_coal_brown.CO2e_combustion_based
        + p_fossil_coal_black.CO2e_combustion_based
        + p_fossil_gas.CO2e_combustion_based
        + p_fossil_ofossil.CO2e_combustion_based
    )
    p_fossil.CO2e_combustion_based_per_MWh = div(
        p_fossil.CO2e_combustion_based, p_fossil.energy
    )
    p_fossil.CO2e_total = (
        p_fossil_nuclear.CO2e_total
        + p_fossil_coal_brown.CO2e_total
        + p_fossil_coal_black.CO2e_total
        + p_fossil_gas.CO2e_total
        + p_fossil_ofossil.CO2e_total
    )

    p_renew_pv.pct_energy = fact("Fact_E_P_pv_pct_of_gep_2018")
    p_renew_pv.energy = d.energy * p_renew_pv.pct_energy

    p_renew_pv_roof.pct_energy = fact("Fact_E_P_pv_roof_pct_of_gep_pv_2017")
    p_renew_pv_roof.energy = p_renew_pv.energy * p_renew_pv_roof.pct_energy
    p_renew_pv_roof.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / entries.e_pv_full_load_hours_sta
        * 1000
    )
    p_renew_pv_roof.cost_mro = (
        p_renew_pv_roof.energy
        * p_renew_pv_roof.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_pv_roof.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_pv_roof.CO2e_combustion_based = (
        p_renew_pv_roof.CO2e_combustion_based_per_MWh * p_renew_pv_roof.energy
    )
    p_renew_pv_roof.CO2e_total = p_renew_pv_roof.CO2e_combustion_based
    p_renew_pv_facade.pct_energy = fact("Fact_E_P_pv_rest_pct_of_gep_pv_2017") / 2
    p_renew_pv_facade.energy = p_renew_pv.energy * p_renew_pv_facade.pct_energy
    p_renew_pv_facade.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / ass("Ass_E_P_local_pv_facade_full_load_hours")
        * 1000
    )
    p_renew_pv_facade.cost_mro = (
        p_renew_pv_facade.energy
        * p_renew_pv_facade.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_pv_facade.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_pv_facade.CO2e_combustion_based = (
        p_renew_pv_facade.CO2e_combustion_based_per_MWh * p_renew_pv_facade.energy
    )
    p_renew_pv_facade.CO2e_total = p_renew_pv_facade.CO2e_combustion_based
    p_renew_pv_park.pct_energy = fact("Fact_E_P_pv_park_pct_of_gep_pv_2017")
    p_renew_pv_park.energy = p_renew_pv.energy * p_renew_pv_park.pct_energy
    p_renew_pv_park.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2020")
        * ass("Ass_E_P_local_pv_park_mro_per_year")
        / entries.e_pv_full_load_hours_sta
        * 1000
    )
    p_renew_pv_park.cost_mro = (
        p_renew_pv_park.energy
        * p_renew_pv_park.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_pv_park.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_pv_park.CO2e_combustion_based = (
        p_renew_pv_park.CO2e_combustion_based_per_MWh * p_renew_pv_park.energy
    )
    p_renew_pv_park.CO2e_total = p_renew_pv_park.CO2e_combustion_based
    p_renew_pv_agri.pct_energy = fact("Fact_E_P_pv_rest_pct_of_gep_pv_2017") / 2
    p_renew_pv_agri.energy = p_renew_pv.energy * p_renew_pv_agri.pct_energy
    p_renew_pv_agri.cost_mro_per_MWh = (
        ass("Ass_E_P_local_pv_agri_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / entries.e_pv_full_load_hours_sta
        * 1000
    )
    p_renew_pv_agri.cost_mro = (
        p_renew_pv_agri.energy
        * p_renew_pv_agri.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_pv_agri.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_pv_agri.CO2e_combustion_based = (
        p_renew_pv_agri.CO2e_combustion_based_per_MWh * p_renew_pv_agri.energy
    )
    p_renew_pv_agri.CO2e_total = p_renew_pv_agri.CO2e_combustion_based
    p_renew_pv_agri.CO2e_total = p_renew_pv_agri.CO2e_combustion_based

    p_renew_pv.CO2e_combustion_based = 0.0
    p_renew_pv.cost_mro = (
        p_renew_pv_roof.cost_mro
        + p_renew_pv_facade.cost_mro
        + p_renew_pv_park.cost_mro
        + p_renew_pv_agri.cost_mro
    )
    p_renew_pv.CO2e_total = (
        p_renew_pv_roof.CO2e_total
        + p_renew_pv_facade.CO2e_total
        + p_renew_pv_park.CO2e_total
        + p_renew_pv_agri.CO2e_total
    )

    p_renew_biomass_waste.pct_energy = fact("Fact_E_P_biomass_waste_pct_of_gep_2018")
    p_renew_biomass_waste.energy = p.energy * p_renew_biomass_waste.pct_energy
    p_renew_biomass_waste.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_biomass_waste_ratio_CO2e_cb_nonCO2_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_biomass_waste.CO2e_combustion_based = (
        p_renew_biomass_waste.CO2e_combustion_based_per_MWh
        * p_renew_biomass_waste.energy
    )
    p_renew_biomass_waste.CO2e_total = p_renew_biomass_waste.CO2e_combustion_based

    p_renew_biomass_solid.pct_energy = fact("Fact_E_P_biomass_solid_pct_of_gep_2018")
    p_renew_biomass_solid.energy = p.energy * p_renew_biomass_solid.pct_energy
    p_renew_biomass_solid.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_biomass_solid_ratio_CO2e_cb_nonCO2_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_biomass_solid.CO2e_combustion_based = (
        p_renew_biomass_solid.CO2e_combustion_based_per_MWh
        * p_renew_biomass_solid.energy
    )
    p_renew_biomass_solid.CO2e_total = p_renew_biomass_solid.CO2e_combustion_based

    p_renew_biomass_gaseous.pct_energy = fact(
        "Fact_E_P_biomass_gaseous_pct_of_gep_2018"
    )
    p_renew_biomass_gaseous.energy = p.energy * p_renew_biomass_gaseous.pct_energy
    p_renew_biomass_gaseous.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_biomass_gaseous_ratio_CO2e_cb_nonCO2_to_gep_2018"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_biomass_gaseous.CO2e_combustion_based = (
        p_renew_biomass_gaseous.CO2e_combustion_based_per_MWh
        * p_renew_biomass_gaseous.energy
    )
    p_renew_biomass_gaseous.CO2e_total = p_renew_biomass_gaseous.CO2e_combustion_based

    p_renew_biomass.pct_energy = fact("Fact_E_P_biomass_pct_of_gep_2018")
    p_renew_biomass.energy = p.energy * p_renew_biomass.pct_energy
    p_renew_biomass.cost_fuel_per_MWh = ass(
        "Ass_E_P_local_biomass_material_costs"
    ) / ass("Ass_E_P_local_biomass_efficiency")
    p_renew_biomass.cost_fuel = (
        p_renew_biomass.cost_fuel_per_MWh
        * p_renew_biomass.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / 1000000
    )
    p_renew_biomass.cost_mro_per_MWh = ass("Ass_E_P_local_biomass_mro_per_MWh")
    p_renew_biomass.cost_mro = (
        p_renew_biomass.energy
        * p_renew_biomass.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_biomass.CO2e_combustion_based = (
        p_renew_biomass_waste.CO2e_combustion_based
        + p_renew_biomass_solid.CO2e_combustion_based
        + p_renew_biomass_gaseous.CO2e_combustion_based
    )
    p_renew_biomass.CO2e_combustion_based_per_MWh = div(
        p_renew_biomass.CO2e_combustion_based, p_renew_biomass.energy
    )
    p_renew_biomass.CO2e_total = (
        p_renew_biomass_waste.CO2e_total
        + p_renew_biomass_solid.CO2e_total
        + p_renew_biomass_gaseous.CO2e_total
    )
    p_renew_biomass_cogen.pct_energy = fact("Fact_E_P_renew_cogen_ratio_2018")
    p_renew_biomass_cogen.energy = (
        p_renew_biomass.energy * p_renew_biomass_cogen.pct_energy
    )
    p_renew_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")
    p_renew_hydro.pct_energy = fact("Fact_E_P_hydro_pct_of_gep_2018")
    p_renew_hydro.energy = p.energy * p_renew_hydro.pct_energy
    p_renew_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")
    p_renew_hydro.cost_mro = (
        p_renew_hydro.energy
        * p_renew_hydro.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_hydro.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_hydro.CO2e_combustion_based = (
        p_renew_hydro.CO2e_combustion_based_per_MWh
        * p_renew_hydro.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    )
    p_renew_hydro.CO2e_total = p_renew_hydro.CO2e_combustion_based
    p_renew_geoth.pct_energy = fact("Fact_E_P_geothermal_pct_of_gep_2018")
    p_renew_geoth.energy = p.energy * p_renew_geoth.pct_energy
    p_renew_geoth.cost_mro_per_MWh = ass("Ass_E_P_renew_geoth_mro_per_MWh")
    p_renew_geoth.cost_mro = (
        p_renew_geoth.energy
        * p_renew_geoth.cost_mro_per_MWh
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        / Million
    )
    p_renew_geoth.CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    p_renew_geoth.CO2e_combustion_based = (
        p_renew_geoth.CO2e_combustion_based_per_MWh
        * p_renew_geoth.energy
        * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
    )
    p_renew_geoth.CO2e_total = p_renew_geoth.CO2e_combustion_based
    p_renew.energy = (
        p_renew_pv.energy
        + p_renew_wind.energy
        + p_renew_biomass.energy
        + p_renew_geoth.energy
        + p_renew_hydro.energy
    )
    p_renew.pct_energy = div(p_renew.energy, p.energy)
    p_renew.cost_fuel = p_renew_biomass.cost_fuel
    p_renew.cost_mro = (
        p_renew_pv.cost_mro
        + p_renew_wind.cost_mro
        + p_renew_biomass.cost_mro
        + p_renew_geoth.cost_mro
        + p_renew_hydro.cost_mro
    )
    p_renew.CO2e_combustion_based = p_renew_biomass.CO2e_combustion_based
    p_renew.CO2e_total = (
        p_renew_pv.CO2e_total
        + p_renew_wind.CO2e_total
        + p_renew_biomass.CO2e_total
        + p_renew_geoth.CO2e_total
        + p_renew_hydro.CO2e_total
    )
    p_renew.CO2e_combustion_based_per_MWh = div(
        p_renew.CO2e_combustion_based, p_renew.energy
    )

    p_local_pv_roof.energy = (
        entries.e_PV_power_inst_roof
        * entries.e_pv_full_load_hours_sta
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_roof.cost_mro_per_MWh = p_renew_pv_roof.cost_mro_per_MWh
    p_local_pv_roof.cost_mro = (
        p_local_pv_roof.energy * p_local_pv_roof.cost_mro_per_MWh / Million
    )
    p_local_pv_facade.energy = (
        entries.e_PV_power_inst_facade
        * ass("Ass_E_P_local_pv_facade_full_load_hours")
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_facade.cost_mro_per_MWh = (
        ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
        * ass("Ass_E_P_local_pv_roof_mro_per_year")
        / ass("Ass_E_P_local_pv_facade_full_load_hours")
        * 1000
    )
    p_local_pv_facade.cost_mro = (
        p_local_pv_facade.energy * p_local_pv_facade.cost_mro_per_MWh / Million
    )
    p_local_pv_park.energy = (
        entries.e_PV_power_inst_park
        * entries.e_pv_full_load_hours_sta
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_park.cost_mro_per_MWh = p_renew_pv_park.cost_mro_per_MWh
    p_local_pv_park.cost_mro = (
        p_local_pv_park.energy * p_local_pv_park.cost_mro_per_MWh / Million
    )
    p_local_pv_agri.energy = (
        entries.e_PV_power_inst_agripv
        * entries.e_pv_full_load_hours_sta
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    p_local_pv_agri.cost_mro_per_MWh = p_renew_pv_agri.cost_mro_per_MWh
    p_local_pv_agri.cost_mro = (
        p_local_pv_agri.energy * p_local_pv_agri.cost_mro_per_MWh / Million
    )

    p_local_pv.CO2e_combustion_based = 0.0
    p_local_pv.CO2e_combustion_based_per_MWh = 0.0
    p_local_pv.CO2e_total = 0.0
    p_local_pv.energy = (
        p_local_pv_roof.energy
        + p_local_pv_facade.energy
        + p_local_pv_park.energy
        + p_local_pv_agri.energy
    )
    p_local_pv.cost_mro = (
        p_local_pv_roof.cost_mro
        + p_local_pv_facade.cost_mro
        + p_local_pv_park.cost_mro
        + p_local_pv_agri.cost_mro
    )

    p_local.CO2e_total = 0.0
    p_local.energy = (
        p_local_pv.energy
        + p_local_wind_onshore.energy
        + p_local_biomass.energy
        + p_local_hydro.energy
    )
    p_local.cost_fuel = p_local_biomass.cost_fuel
    p_local.cost_mro = (
        p_local_pv.cost_mro
        + p_local_wind_onshore.cost_mro
        + p_local_biomass.cost_mro
        + p_local_hydro.cost_mro
    )
    p_local.CO2e_combustion_based = p_local_biomass.CO2e_combustion_based
    p_local.pct_energy = div(p_local.energy, p.energy)

    p.cost_fuel = p_fossil.cost_fuel + p_renew.cost_fuel
    p.cost_certificate = p_fossil.cost_certificate
    p.cost_mro = p_fossil.cost_mro + p_renew.cost_mro
    p.CO2e_combustion_based = (
        p_fossil.CO2e_combustion_based + p_renew.CO2e_combustion_based
    )
    p.CO2e_combustion_based_per_MWh = div(p.CO2e_combustion_based, p.energy)
    p.CO2e_total = p_fossil.CO2e_total + p_renew.CO2e_total

    e.CO2e_production_based = 0.0
    e.CO2e_combustion_based = p.CO2e_combustion_based
    e.CO2e_total = p.CO2e_total

    p_local_biomass_cogen.pct_energy = fact("Fact_E_P_renew_cogen_ratio_2018")
    p_local_biomass_cogen.energy = (
        p_local_biomass.energy * p_local_biomass_cogen.pct_energy
    )
    p_fossil_and_renew.energy = p.energy
    p_fossil_and_renew.CO2e_combustion_based = (
        p_fossil.CO2e_combustion_based + p_renew.CO2e_combustion_based
    )
    p_fossil_and_renew.CO2e_combustion_based_per_MWh = div(
        p_fossil_and_renew.CO2e_combustion_based, p_fossil_and_renew.energy
    )
    p_fossil_and_renew.CO2e_total = p_fossil.CO2e_total + p_renew.CO2e_total
    p_fossil_and_renew.pct_energy = p_fossil.pct_energy + p_renew.pct_energy
    return e18
