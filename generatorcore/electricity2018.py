from dataclasses import dataclass, field, InitVar, asdict
from .setup import ass, entry, fact

# Definition der relevanten Spaltennamen für den Sektor E


@dataclass
class EColVars:
    energy: float = field(default=None)
    cost_fuel_per_MWh: float = None
    cost_fuel: float = None
    pct_energy: float = None
    mro_per_MWh: float = None
    cost_mro: float = None
    CO2e_cb: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_pb: float = None
    CO2e_total: float = None
    cost_certificate_per_MWh: float = None
    cost_certificate: float = None
    cost_mro_per_MWh: float = None
    demand_electricity: float = None
    area_ha_available: float = None
    factor_adapted_to_fec: float = None


# Definition der Zeilennamen für den Sektor E
@dataclass
class E18:
    # Klassenvariablen für E
    e: EColVars = field(default=EColVars())
    g: EColVars = field(default=EColVars())
    g_grid_offshore: EColVars = EColVars()
    g_grid_onshore: EColVars = EColVars()
    g_grid_pv: EColVars = EColVars()
    d: EColVars = EColVars()
    d_r: EColVars = EColVars()
    d_b: EColVars = EColVars()
    d_i: EColVars = EColVars()
    d_t: EColVars = EColVars()
    d_a: EColVars = EColVars()
    d_h: EColVars = EColVars()
    d_f_wo_hydrogen: EColVars = EColVars()
    d_f_hydrogen_reconv: EColVars = EColVars()
    p: EColVars = EColVars()
    p_fossil: EColVars = EColVars()
    p_fossil_nuclear: EColVars = EColVars()
    p_fossil_coal_brown: EColVars = EColVars()
    p_fossil_coal_brown_cogen: EColVars = EColVars()
    p_fossil_coal_black: EColVars = EColVars()
    p_fossil_coal_black_cogen: EColVars = EColVars()
    p_fossil_gas: EColVars = EColVars()
    p_fossil_gas_cogen: EColVars = EColVars()
    p_fossil_ofossil: EColVars = EColVars()
    p_fossil_ofossil_cogen: EColVars = EColVars()
    p_renew: EColVars = EColVars()
    p_renew_pv: EColVars = EColVars()
    p_renew_pv_roof: EColVars = EColVars()
    p_renew_pv_facade: EColVars = EColVars()
    p_renew_pv_park: EColVars = EColVars()
    p_renew_pv_agri: EColVars = EColVars()
    p_renew_wind: EColVars = EColVars()
    p_renew_wind_onshore: EColVars = EColVars()
    p_renew_wind_offshore: EColVars = EColVars()
    p_renew_biomass: EColVars = EColVars()
    p_renew_biomass_waste: EColVars = EColVars()
    p_renew_biomass_solid: EColVars = EColVars()
    p_renew_biomass_gaseous: EColVars = EColVars()
    p_renew_biomass_cogen: EColVars = EColVars()
    p_renew_geoth: EColVars = EColVars()
    p_renew_hydro: EColVars = EColVars()
    p_renew_pv_agri: EColVars = EColVars()
    p_renew_reverse: EColVars = EColVars()
    p_fossil_and_renew: EColVars = EColVars()
    p_local_pv_roof: EColVars = EColVars()
    p_local_pv_facade: EColVars = EColVars()
    p_local_pv_park: EColVars = EColVars()
    p_local_pv_agri: EColVars = EColVars()
    p_local_pv: EColVars = EColVars()
    p_local_wind_onshore: EColVars = EColVars()
    p_local_biomass: EColVars = EColVars()
    p_local_biomass_cogen: EColVars = EColVars()
    p_local_biomass_gaseous: EColVars = EColVars()
    p_local_biomass_solid: EColVars = EColVars()
    p_local_surplus: EColVars = EColVars()
    p_local_hydro: EColVars = EColVars()
    p_local: EColVars = EColVars()

    # erzeuge dictionry

    def dict(self):
        return asdict(self)


# Berechnungsfunktion im Sektor E für 2018
# Parameter root: oberste Generator Instanz


def Electricity2018_calc(root):
    try:
        Million = 1000000

        r18 = root.r18

        """variable abbrevations"""
        e = root.e18.e
        d = root.e18.d
        d_r = root.e18.d_r
        d_b = root.e18.d_b
        d_i = root.e18.d_i
        d_t = root.e18.d_t
        d_a = root.e18.d_a
        d_h = root.e18.d_h
        d_f_hydrogen_reconv = root.e18.d_f_hydrogen_reconv
        p = root.e18.p
        p_fossil = root.e18.p_fossil
        p_fossil_nuclear = root.e18.p_fossil_nuclear
        p_fossil_coal_brown = root.e18.p_fossil_coal_brown
        p_fossil_coal_brown_cogen = root.e18.p_fossil_coal_brown_cogen
        p_fossil_coal_black = root.e18.p_fossil_coal_black
        p_fossil_coal_black_cogen = root.e18.p_fossil_coal_black_cogen
        p_fossil_gas = root.e18.p_fossil_gas
        p_fossil_gas_cogen = root.e18.p_fossil_gas_cogen
        p_fossil_ofossil = root.e18.p_fossil_ofossil
        p_fossil_ofossil_cogen = root.e18.p_fossil_ofossil_cogen
        p_renew = root.e18.p_renew
        p_renew_geoth = root.e18.p_renew_geoth
        p_renew_hydro = root.e18.p_renew_hydro
        p_renew_pv = root.e18.p_renew_pv
        p_renew_pv_roof = root.e18.p_renew_pv_roof
        p_renew_pv_facade = root.e18.p_renew_pv_facade
        p_renew_pv_park = root.e18.p_renew_pv_park
        p_renew_wind = root.e18.p_renew_wind
        p_renew_wind_onshore = root.e18.p_renew_wind_onshore
        p_renew_wind_offshore = root.e18.p_renew_wind_offshore
        p_renew_biomass = root.e18.p_renew_biomass
        p_renew_biomass_waste = root.e18.p_renew_biomass_waste
        p_renew_biomass_solid = root.e18.p_renew_biomass_solid
        p_renew_biomass_gaseous = root.e18.p_renew_biomass_gaseous
        p_renew_biomass_cogen = root.e18.p_renew_biomass_cogen
        p_renew_pv_agri = root.e18.p_renew_pv_agri
        p_renew_reverse = root.e18.p_renew_reverse
        p_fossil_and_renew = root.e18.p_fossil_and_renew
        p_local_pv_roof = root.e18.p_local_pv_roof
        p_local_pv_facade = root.e18.p_local_pv_facade
        p_local_pv_park = root.e18.p_local_pv_park
        p_local_pv_agri = root.e18.p_local_pv_agri
        p_local_pv = root.e18.p_local_pv
        p_local_wind_onshore = root.e18.p_local_wind_onshore
        p_local_biomass = root.e18.p_local_biomass
        p_local_biomass_cogen = root.e18.p_local_biomass_cogen
        p_local_hydro = root.e18.p_local_hydro
        p_local = root.e18.p_local

        e.CO2e_pb = 0.
        p_renew_pv.CO2e_cb = 0.
        p_renew_wind.CO2e_cb = 0.
        p_renew_wind_onshore.CO2e_cb = 0.
        p_renew_wind_onshore.CO2e_cb_per_MWh = 0.
        p_renew_wind_onshore.CO2e_total = 0.
        p_renew_wind_offshore.CO2e_cb = 0.
        p_renew_wind_offshore.CO2e_cb_per_MWh = 0.
        p_renew_wind_offshore.CO2e_total = 0.
        p_renew_reverse.energy = 0.
        p_local.CO2e_total = 0.
        p_local_pv.CO2e_cb = 0.
        p_local_pv.CO2e_cb_per_MWh = 0.
        p_local_pv.CO2e_total = 0.
        p_local_wind_onshore.CO2e_cb = 0.
        p_local_wind_onshore.CO2e_cb_per_MWh = 0.
        p_local_wind_onshore.CO2e_total = 0.
        p_local_biomass.CO2e_total = 0.
        p_local_hydro.CO2e_cb = 0.
        p_local_hydro.CO2e_cb_per_MWh = 0.
        p_local_hydro.CO2e_total  = 0.

        # NACHFRAGE:
        d_h.energy = 0
        d_f_hydrogen_reconv.energy = 0
        # Zeile Haushalte:

        # 1
        d_r.energy = (
            entry("In_R_elec_fec")
            # result: 126.600.000 MWh
        )
        # 2
        d_r.cost_fuel_per_MWh = (
            fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
            # 298.80
            # result: 298,80 €/MWh
        )

        # 3
        d_r.cost_fuel = (
            d_r.cost_fuel_per_MWh
            * d_r.energy
            / Million
            # result: 37.828,08 Mio €/d_a
        )
        # Zeile GHD+sonstiges
        # 1
        d_b.energy = (
            entry("In_B_elec_fec")
            # result: 143.690.000 MWh
        )
        # 2
        d_b.cost_fuel_per_MWh = (
            fact("Fact_E_D_B_cost_fuel_per_MWh_2018")
            # resulut: 215,60 €/MWh
        )
        # 3
        d_b.cost_fuel = (
            d_b.cost_fuel_per_MWh
            * d_b.energy
            / 1000000
            # result: 30.979,56 Mio €/d_a
        )
        # Zeile Industrie

        # 1
        d_i.energy = (
            entry("In_I_elec_fec")
            # result: 226.095.000 MWh
        )
        # 2
        d_i.cost_fuel_per_MWh = (
            fact("Fact_E_D_I_cost_fuel_per_MWh_2018")
            # result: 153,00 €/MWh
        )
        # 3
        d_i.cost_fuel = (
            d_i.energy
            * d_i.cost_fuel_per_MWh
            / 1000000
            # result: 334.592,54 Mio €/d_a
        )
        # Zeile Verkehr

        # root.t18.t.demand_electricity = 11857547.31 #Todo set in traffic
        d_t.energy = root.t18.t.demand_electricity
        # 2
        d_t.cost_fuel_per_MWh = (
            fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
            # result: 298,80 €/MWh
        )
        # 3
        d_t.cost_fuel = (
            d_t.energy
            * d_t.cost_fuel_per_MWh
            / 1000000
            # result: 3.543,04 Mio €/d_a
        )
        # Zeile Landwirtschaft

        # 1
        d_a.energy = (
            entry("In_A_elec_fec")
            # result: 3.570.000 MWh
        )

        # Zeile Nachfrage Strom

        # 1
        d.energy = (
            d_r.energy
            + d_b.energy
            + d_i.energy
            + d_t.energy
            + d_a.energy
            # result: 511.812.547 MWh
        )
        # 2
        d.cost_fuel = d_r.cost_fuel + d_b.cost_fuel + d_i.cost_fuel + d_t.cost_fuel

        # BEREITSTELLUNG:

        # Zeile Bereitstellung

        # 1
        p.energy = d.energy

        # Zeile Kernenergie

        # 1
        p_fossil_nuclear.pct_energy = (
            fact("Fact_E_P_nuclear_pct_of_gep_2018")
            # result: 11,9%
        )
        # 2
        p_fossil_nuclear.energy = (
            p.energy
            * p_fossil_nuclear.pct_energy
            # result: 60.905.693 MWh
        )
        # 3
        p_fossil_nuclear.cost_fuel_per_MWh = (
            ass("Ass_E_P_fossil_nuclear_cost_fuel_per_MWh")
            / ass("Ass_E_P_fossil_nuclear_efficiency")
            # result: 21,7 €/MWh
        )
        # 4
        p_fossil_nuclear.cost_fuel = (
            p_fossil_nuclear.cost_fuel_per_MWh
            * p_fossil_nuclear.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 1.659,67 Mio €/d_a
        )

        p_fossil_nuclear.CO2e_cb_per_MWh = 0
        p_fossil_nuclear.CO2e_cb = (
            p_fossil_nuclear.CO2e_cb_per_MWh
            * p_fossil_nuclear.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )

        # 6
        p_fossil_nuclear.cost_mro_per_MWh = (
            ass("Ass_E_P_fossil_nuclear_mro_per_MW")
            / fact("Fact_E_P_nuclear_full_load_hours")
            # result: 5,3 €/MWh
        )
        # 5
        p_fossil_nuclear.cost_mro = (
            p_fossil_nuclear.cost_mro_per_MWh
            * p_fossil_nuclear.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 407,17 Mio €/d_a
        )
        # Zeile Braunkohle

        # 1
        p_fossil_coal_brown.pct_energy = (
            fact("Fact_E_P_coal_brown_pct_of_gep_2018")
            # result: 22,8%
        )
        # 2
        p_fossil_coal_brown.energy = (
            p.energy
            * p_fossil_coal_brown.pct_energy
            # result: 116.693.261 MWh
        )
        # 3

        p_fossil_coal_brown.cost_fuel_per_MWh = (
            ass("Ass_E_P_fossil_coal_brown_cost_fuel_per_MWh")
            / ass("Ass_E_P_fossil_coal_black_efficiency")
            # result: 11,9 €/MWh
        )
        # 4
        p_fossil_coal_brown.cost_fuel = (
            p_fossil_coal_brown.cost_fuel_per_MWh
            * p_fossil_coal_brown.energy
            * fact(  # check
                "Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018"
            )
            / 1000000
            # result: 1.741,36 Mio €/d_a
        )
        # 5
        p_fossil_coal_brown.cost_certificate_per_MWh = (fact('Fact_E_P_coal_brown_ratio_CO2e_cb_to_gep_2018') * fact('Fact_M_cost_certificate_per_t_CO2_ETS_2018') * 1000)
            # result: 20,9 €/MWh
        # 6
        p_fossil_coal_brown.cost_certificate = (
            p_fossil_coal_brown.cost_certificate_per_MWh
            * p_fossil_coal_brown.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 3.054,91 Mio €/d_a
        )
        # 7
        p_fossil_coal_brown.cost_mro_per_MWh = (
            ass("Ass_E_P_fossil_coal_brown_mro_per_MW")
            / fact("Fact_E_P_coal_brown_full_load_hours")
            # result: 7,8 €/MWh
        )
        # 8
        p_fossil_coal_brown.cost_mro = (
            p_fossil_coal_brown.cost_mro_per_MWh
            * p_fossil_coal_brown.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 1.140,94 Mio €/d_a
        )
        # 9
        p_fossil_coal_brown.CO2e_cb_per_MWh = (
            fact("Fact_E_P_coal_brown_ratio_CO2e_cb_to_gep_2018")
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            # result: 1,006  d_t/MWh
        )
        # 10
        p_fossil_coal_brown.CO2e_cb = (
            p_fossil_coal_brown.CO2e_cb_per_MWh
            * p_fossil_coal_brown.energy
            # result: 147.082.899 d_t/d_a
        )

        # Zeile Braunkohle, davon KWK-Wärme für Braunkohle

        # 1
        p_fossil_coal_brown_cogen.pct_energy = (
            fact("Fact_E_P_coal_brown_cogen_ratio_2018")
            # result: 5,8%
        )
        # 2
        p_fossil_coal_brown_cogen.energy = (
            p_fossil_coal_brown.energy
            * p_fossil_coal_brown_cogen.pct_energy
            # result: 6.726.064 MWh
        )

        # Zeile Steinkohle

        # 1
        p_fossil_coal_black.pct_energy = (
            fact("Fact_E_P_coal_black_pct_of_gep_2018")
            # result: 13,0%
        )
        # 2
        p_fossil_coal_black.energy = (
            p.energy
            * p_fossil_coal_black.pct_energy
            # result: 66.535.631 MWh
        )
        # 3
        p_fossil_coal_black.cost_fuel_per_MWh = (
            ass("Ass_E_P_fossil_coal_black_cost_fuel_per_MWh")
            / ass("Ass_E_P_fossil_coal_black_efficiency")
            # result: 20,0 €/MWh
        )
        # 4
        p_fossil_coal_black.cost_fuel = (
            p_fossil_coal_black.cost_fuel_per_MWh
            * p_fossil_coal_black.energy
            * fact(  # check
                "Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018"
            )
            / 1000000
            # result: 1.668,04 Mio €/d_a
        )
        # 5
        p_fossil_coal_black.cost_certificate_per_MWh = (
            fact("Fact_E_P_coal_black_ratio_CO2e_cb_to_gep_2018")
            * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
            * 1000
            # result: 15,5 €/MWh
        )
        # 6
        p_fossil_coal_black.cost_certificate = (
            p_fossil_coal_black.cost_certificate_per_MWh
            * p_fossil_coal_black.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 1.291,03 Mio €/d_a
        )
        # 7
        p_fossil_coal_black.cost_mro_per_MWh = (
            ass("Ass_E_P_fossil_coal_black_mro_per_MW")
            / fact("Fact_E_P_coal_black_full_load_hours")
            # result: 10,9 €/MWh
        )
        # 8
        p_fossil_coal_black.cost_mro = (
            p_fossil_coal_black.cost_mro_per_MWh
            * p_fossil_coal_black.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 911,00 Mio €/d_a
        )
        # 9
        p_fossil_coal_black.CO2e_cb_per_MWh = (
            fact("Fact_E_P_coal_black_ratio_CO2e_cb_to_gep_2018")
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            # result: 0,745  d_t/MWh
        )
        # 10
        p_fossil_coal_black.CO2e_cb = (
            p_fossil_coal_black.CO2e_cb_per_MWh
            * p_fossil_coal_black.energy
            # result: 62.158.560 d_t/d_a
        )

        # Zeile Steinkohle, davon KWK-Wärme für Steinkohle

        # 1
        p_fossil_coal_black_cogen.pct_energy = (
            fact("Fact_E_P_coal_black_cogen_ratio_2018")
            # result: 33,9%
        )
        # 2
        p_fossil_coal_black_cogen.energy = (
            p_fossil_coal_black.energy
            * p_fossil_coal_black_cogen.pct_energy
            # result: 22.562.112 MWh
        )

        # Zeile Erdgas

        # 1
        p_fossil_gas.pct_energy = (
            fact("Fact_E_P_gas_pct_of_gep_2018")
            # result: 12,9%
        )
        # 2
        p_fossil_gas.energy = (
            p.energy
            * p_fossil_gas.pct_energy
            # result: 66.023.819 MWh
        )
        # 3
        p_fossil_gas.cost_fuel_per_MWh = (
            ass("Ass_E_P_renew_reverse_gud_cost_fuel_per_MWh")
            / ass("Ass_E_P_renew_reverse_gud_efficiency")
            # result: 40,5 €/MWh
        )
        # 4
        p_fossil_gas.cost_fuel = (
            p_fossil_gas.cost_fuel_per_MWh
            * p_fossil_gas.energy
            * fact(  # check
                "Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018"
            )
            / 1000000
            # result: 3.353,22 Mio €/d_a
        )
        # 5
        p_fossil_gas.cost_certificate_per_MWh = (
            fact("Fact_E_P_gas_ratio_CO2e_cb_to_gep_2018")
            * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
            * 1000
            # result: 7,6 €/MWh
        )
        # 6
        p_fossil_gas.cost_certificate = (
            p_fossil_gas.cost_certificate_per_MWh
            * p_fossil_gas.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 628,87 Mio €/d_a
        )
        # 7
        p_fossil_gas.cost_mro_per_MWh = (
            ass("Ass_E_P_renew_reverse_gud_cost_mro_per_MW")
            / fact("Fact_E_P_gas_full_load_hours")
            # result: 12,9 €/MWh
        )
        # 8
        p_fossil_gas.cost_mro = (
            p_fossil_gas.cost_mro_per_MWh
            * p_fossil_gas.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 1.069,52 Mio €/d_a
        )
        # 9
        p_fossil_gas.CO2e_cb_per_MWh = fact(
            "Fact_E_P_gas_ratio_CO2e_cb_to_gep_2018"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        # 10
        p_fossil_gas.CO2e_cb = (
            p_fossil_gas.CO2e_cb_per_MWh
            * p_fossil_gas.energy
            # result: 30.277.853 d_t/d_a
        )
        # Zeile Erdgas, davon KWK-Wärme Erdgas

        # 1
        p_fossil_gas_cogen.pct_energy = (
            fact("Fact_E_P_gas_cogen_ratio_2018")
            # result: 49,6%
        )
        # 2
        p_fossil_gas_cogen.energy = (
            p_fossil_gas.energy
            * p_fossil_gas_cogen.pct_energy
            # result: 32.778.918 MWh
        )
        # Zeile sonstige koventionelle (Heizöl, Abfälle)

        # 1
        p_fossil_ofossil.pct_energy = (
            fact("Fact_E_P_ofossil_pct_of_gep_2018")
            # result: 4,0%
        )
        # 2
        p_fossil_ofossil.energy = (
            p.energy
            * p_fossil_ofossil.pct_energy
            # result: 20.472.502 MWh
        )
        # 3
        p_fossil_ofossil.cost_fuel_per_MWh = p_fossil_coal_brown.cost_fuel_per_MWh

        # 4
        p_fossil_ofossil.cost_fuel = (
            p_fossil_ofossil.cost_fuel_per_MWh
            * p_fossil_ofossil.energy
            * fact(  # check
                "Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018"
            )
            / 1000000
            # result: 10,78 Mio €/d_a
        )
        # 5
        p_fossil_ofossil.cost_certificate_per_MWh = (
            fact("Fact_E_P_ofossil_ratio_CO2e_cb_to_gep_2018")
            * fact("Fact_M_cost_certificate_per_t_CO2_ETS_2018")
            * 1000
            # result: 23,3 €/MWh
        )
        # 6
        p_fossil_ofossil.cost_certificate = (
            p_fossil_ofossil.cost_certificate_per_MWh
            * p_fossil_ofossil.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 598,31 Mio €/d_a
        )
        # 7
        p_fossil_ofossil.cost_mro_per_MWh = p_fossil_coal_brown.cost_mro_per_MWh

        # 8

        p_fossil_ofossil.cost_mro = (
            p_fossil_ofossil.cost_mro_per_MWh
            * p_fossil_ofossil.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 83.401,84 Mio €/d_a
        )
        # 9
        p_fossil_ofossil.CO2e_cb_per_MWh = fact(
            "Fact_E_P_ofossil_ratio_CO2e_cb_to_gep_2018"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        # 10
        p_fossil_ofossil.CO2e_cb = (
            p_fossil_ofossil.CO2e_cb_per_MWh
            * p_fossil_ofossil.energy
            # result: 28.806.227 d_t/d_a
        )
        # Zeile sonstige Konventionelle, davon KWK-Wärme

        # 1
        p_fossil_ofossil_cogen.pct_energy = (
            fact("Fact_E_P_ofossil_cogen_ratio_2018")
            # result: 39,9%
        )
        # 2
        p_fossil_ofossil_cogen.energy = (
            p_fossil_ofossil.energy
            * p_fossil_ofossil_cogen.pct_energy
            # result: 8.173.444 MWh
        )
        # Zeile Fossile Eneergieträger

        # 1
        p_fossil.energy = (
            p_fossil_nuclear.energy
            + p_fossil_coal_brown.energy
            + p_fossil_coal_black.energy
            + p_fossil_gas.energy
            + p_fossil_ofossil.energy
            # result: 330.630.906 MWh
        )
        # 2
        p_fossil.pct_energy = (
            p_fossil.energy
            / p.energy
            # result: 64,6%
        )

        # Zeile Photovoltaik 1

        # 1
        p_renew_pv.pct_energy = (
            fact("Fact_E_P_pv_pct_of_gep_2018")
            # result: 7,3%
        )
        # 2
        p_renew_pv.energy = (
            p.energy
            * p_renew_pv.pct_energy
            # result: 37.362.316 MWh
        )
        # Zeile Photovoltaik Dach

        # 1
        p_renew_pv_roof.pct_energy = (
            fact("Fact_E_P_pv_roof_pct_of_gep_pv_2017")
            # result: 73,2%
        )
        # 2
        p_renew_pv_roof.energy = (
            p_renew_pv.energy
            * p_renew_pv_roof.pct_energy
            # result: 27.349.215 MWh
        )
        # 7
        p_renew_pv_roof.cost_mro_per_MWh = (
            ass("Ass_E_P_local_pv_roof_ratio_invest_to_power_2020")
            * ass("Ass_E_P_local_pv_roof_mro_per_year")
            / entry("In_E_pv_full_load_hours_sta")
            * 1000
            # result: 18,4 €/MWh
        )
        # 8
        p_renew_pv_roof.cost_mro = (
            p_renew_pv_roof.energy
            * p_renew_pv_roof.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
            # result: 502,77 Mio €/d_a
        )
        # Zeile PV Fassade

        # 1
        p_renew_pv_facade.pct_energy = (
            fact("Fact_E_P_pv_rest_pct_of_gep_pv_2017")
            / 2
            # result: 0,7%
        )
        # 2
        p_renew_pv_facade.energy = (
            p_renew_pv.energy
            * p_renew_pv_facade.pct_energy
            # result: 242.855 MWh
        )
        # 7
        p_renew_pv_facade.cost_mro_per_MWh = (
            ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
            * ass("Ass_E_P_local_pv_roof_mro_per_year")
            / ass("Ass_E_P_local_pv_facade_full_load_hours")
            * 1000
            # result: 100,0 €/MWh
        )
        # 8
        p_renew_pv_facade.cost_mro = (
            p_renew_pv_facade.energy
            * p_renew_pv_facade.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
        )
        # Zeile PV Freifläche

        # 1
        p_renew_pv_park.pct_energy = (
            fact("Fact_E_P_pv_park_pct_of_gep_pv_2017")
            # result: 25,5%
        )
        # 2
        p_renew_pv_park.energy = (
            p_renew_pv.energy
            * p_renew_pv_park.pct_energy
            # result: 9.527.391 MWh
        )
        # 7
        p_renew_pv_park.cost_mro_per_MWh = (
            ass("Ass_E_S_local_pv_park_ratio_invest_to_power_2020")
            * ass("Ass_E_P_local_pv_park_mro_per_year")
            / entry("In_E_pv_full_load_hours_sta")
            * 1000
        )
        # 8
        p_renew_pv_park.cost_mro = (
            p_renew_pv_park.energy
            * p_renew_pv_park.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
            # result: 125,10 Mio €/d_a
        )
        # Zeile PV Agrar

        # 1
        p_renew_pv_agri.pct_energy = (
            fact("Fact_E_P_pv_rest_pct_of_gep_pv_2017")
            / 2
            # result: 0,7%
        )
        # 2
        p_renew_pv_agri.energy = (
            p_renew_pv.energy
            * p_renew_pv_agri.pct_energy
            # result: 242.855 MWh
        )
        # 7
        p_renew_pv_agri.cost_mro_per_MWh = (
            ass("Ass_E_P_local_pv_agri_ratio_invest_to_power")
            * ass("Ass_E_P_local_pv_roof_mro_per_year")
            / entry("In_E_pv_full_load_hours_sta")
            * 1000
            # result: 28,3 €/MWh
        )
        # 8
        p_renew_pv_agri.cost_mro = (
            p_renew_pv_agri.energy
            * p_renew_pv_agri.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
            # result: 6,88 Mio €/d_a
        )
        # Zeile Photovoltaik 2

        # 8
        p_renew_pv.cost_mro = (
            p_renew_pv_roof.cost_mro
            + p_renew_pv_facade.cost_mro
            + p_renew_pv_park.cost_mro
            + p_renew_pv_agri.cost_mro
            # result: 659,03 Mio €/d_a
        )

        # Zeile Windkraft 1

        # 1
        p_renew_wind.pct_energy = (
            fact("Fact_E_P_wind_pct_of_gep_2018")
            # result: 17,3%
        )
        # 2
        p_renew_wind.energy = (
            p.energy
            * p_renew_wind.pct_energy
            # result: 88.543.571 MWh
        )

        # Zeile Wind onshore

        # 1
        p_renew_wind_onshore.pct_energy = (
            fact("Fact_E_P_wind_onshore_pct_of_gep_2018")
            # result: 14,2%
        )
        # 2
        p_renew_wind_onshore.energy = p_renew_wind_onshore.pct_energy * p.energy
        # 7
        p_renew_wind_onshore.cost_mro_per_MWh = (
            ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2020")
            * ass("Ass_E_P_local_wind_onshore_mro_per_year")
            / fact("Fact_E_P_wind_onshore_full_load_hours")
            * 1000
            # result: 25,0 €/MWh
        )
        # 8
        p_renew_wind_onshore.cost_mro = (
            p_renew_wind_onshore.cost_mro_per_MWh
            * p_renew_wind_onshore.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 1.816,18 Mio €/d_a
        )

        # Zeile Wind offshore

        # 1
        p_renew_wind_offshore.pct_energy = (
            fact("Fact_E_P_wind_offshore_pct_of_gep_2018")
            # result: 3,1%
        )
        # 2
        p_renew_wind_offshore.energy = p_renew_wind_offshore.pct_energy * p.energy

        # 7
        p_renew_wind_offshore.cost_mro_per_MWh = (
            ass("Ass_E_P_renew_wind_offshore_ratio_invest_to_power_2020")
            * ass("Ass_E_P_renew_wind_offshore_mro_per_year")
            / fact("Fact_E_P_wind_offshore_full_load_hours")
            * 1000
            # result: 32,8 €/MWh
        )
        # 8
        p_renew_wind_offshore.cost_mro = (
            p_renew_wind_offshore.cost_mro_per_MWh
            * p_renew_wind_offshore.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
        )
        # Zeile p_renew_wind 2

        # 8
        p_renew_wind.cost_mro = (
            p_renew_wind_onshore.cost_mro
            + p_renew_wind_offshore.cost_mro  # Todo Check
            # result: 2.336,47 Mio €/d_a
        )
        # Zeile Biomasse 1

        # 1
        p_renew_biomass.pct_energy = (
            fact("Fact_E_P_biomass_pct_of_gep_2018")
            # result: 8,0%
        )
        # 2
        p_renew_biomass.energy = (
            p.energy
            * p_renew_biomass.pct_energy
            # result: 40.945.004 MWh
        )
        # 3
        p_renew_biomass.cost_fuel_per_MWh = (
            ass("Ass_E_P_local_biomass_material_costs")
            / ass("Ass_E_P_local_biomass_efficiency")
            # result: 75,8 €/MWh
        )
        # 4
        p_renew_biomass.cost_fuel = (
            p_renew_biomass.cost_fuel_per_MWh
            * p_renew_biomass.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / 1000000
            # result: 3.887,81 Mio €/d_a
        )
        # 5
        p_renew_biomass.cost_mro_per_MWh = (
            ass("Ass_E_P_local_biomass_mro_per_MWh")
            # result: 18,9 €/MWh
        )
        # 6
        p_renew_biomass.cost_mro = (
            p_renew_biomass.energy
            * p_renew_biomass.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
        )

        # Zeile Biomüll

        # 1
        p_renew_biomass_waste.pct_energy = (
            fact("Fact_E_P_biomass_waste_pct_of_gep_2018")
            # result: 1,0%
        )
        # 2
        p_renew_biomass_waste.energy = (
            p.energy
            * p_renew_biomass_waste.pct_energy
            # result: 5.118.125 MWh
        )
        # 9
        p_renew_biomass_waste.CO2e_cb_per_MWh = (
            fact("Fact_E_P_biomass_waste_ratio_CO2e_cb_nonCO2_to_gep_2018")
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            # result: 0,005  d_t/MWh
        )
        # 10
        p_renew_biomass_waste.CO2e_cb = (
            p_renew_biomass_waste.CO2e_cb_per_MWh
            * p_renew_biomass_waste.energy
            # result: 30.474 d_t/d_a
        )
        # Zeile Biomasse fest

        # 1
        p_renew_biomass_solid.pct_energy = (
            fact("Fact_E_P_biomass_solid_pct_of_gep_2018")
            # result: 1,8%
        )
        # 2
        p_renew_biomass_solid.energy = (
            p.energy
            * p_renew_biomass_solid.pct_energy
            # result: 9.212.626 MWh
        )
        # 9
        p_renew_biomass_solid.CO2e_cb_per_MWh = (
            fact("Fact_E_P_biomass_solid_ratio_CO2e_cb_nonCO2_to_gep_2018")
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            # result: 0,012  d_t/MWh
        )
        # 10
        p_renew_biomass_solid.CO2e_cb = (
            p_renew_biomass_solid.CO2e_cb_per_MWh
            * p_renew_biomass_solid.energy
            # result: 140.885 d_t/d_a
        )
        # Zeile Biogas

        # 1
        p_renew_biomass_gaseous.pct_energy = (
            fact("Fact_E_P_biomass_gaseous_pct_of_gep_2018")
            # result: 5,2%
        )
        # 2
        p_renew_biomass_gaseous.energy = (
            p.energy
            * p_renew_biomass_gaseous.pct_energy
            # result: 26.614.252 MWh
        )
        # 9
        p_renew_biomass_gaseous.CO2e_cb_per_MWh = (
            fact("Fact_E_P_biomass_gaseous_ratio_CO2e_cb_nonCO2_to_gep_2018")
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            # result: 0,100  d_t/MWh
        )
        # 10
        p_renew_biomass_gaseous.CO2e_cb = (
            p_renew_biomass_gaseous.CO2e_cb_per_MWh
            * p_renew_biomass_gaseous.energy
            # result: 3.346.082 d_t/d_a
        )
        # Zeile Biomasse KWK

        # 1
        p_renew_biomass_cogen.pct_energy = (
            fact("Fact_E_P_renew_cogen_ratio_2018")
            # result: 29,7%
        )
        # 2
        p_renew_biomass_cogen.energy = (
            p_renew_biomass.energy
            * p_renew_biomass_cogen.pct_energy
            # result: 12.175.027 MWh
        )

        p_renew_hydro.cost_mro_per_MWh = ass("Ass_E_P_local_hydro_mro_per_MWh")

        # Zeile Biomasse 2

        # 10
        p_renew_biomass.CO2e_cb = (
            p_renew_biomass_waste.CO2e_cb
            + p_renew_biomass_solid.CO2e_cb
            + p_renew_biomass_gaseous.CO2e_cb
            # result: 3.517.441 d_t/d_a
        )  # SUM(p_renew_biomass_waste.CO2e_cb:p_renew_biomass_gaseous.CO2e_cb)
        # Zeile Geothermie
        p_renew_biomass.CO2e_cb_per_MWh = (
            p_renew_biomass.CO2e_cb / p_renew_biomass.energy
        )
        # 1
        p_renew_geoth.pct_energy = (
            fact("Fact_E_P_geothermal_pct_of_gep_2018")
            # result: 0,03%
        )
        # 2
        p_renew_geoth.energy = (
            p.energy
            * p_renew_geoth.pct_energy
            # result: 153.544 MWh
        )
        # 9
        p_renew_geoth.cost_mro_per_MWh = (
            ass("Ass_E_P_renew_geoth_mro_per_MWh")
            # result: 18 €/MWh
        )
        # 10
        p_renew_geoth.cost_mro = (
            p_renew_geoth.energy
            * p_renew_geoth.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
            # result: 2,76 Mio €/d_a
        )
        # Zeile Laufwasser

        # 1
        p_renew_hydro.pct_energy = (
            fact("Fact_E_P_hydro_pct_of_gep_2018")
            # result: 2,8%
        )
        # 2
        p_renew_hydro.energy = (
            p.energy
            * p_renew_hydro.pct_energy
            # result: 14.330.751 MWh
        )
        # 9
        p_renew_hydro.cost_mro_per_MWh = (
            ass("Ass_E_P_local_hydro_mro_per_MWh")
            # result: 23,8 €/MWh
        )
        # 10

        p_renew_hydro.cost_mro = (
            p_renew_hydro.energy
            * p_renew_hydro.cost_mro_per_MWh
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
            / Million
        )

        # Zeile Erneuerbare

        # 1
        p_renew.energy = (
            p_renew_pv.energy
            + p_renew_wind.energy
            + p_renew_biomass.energy
            + p_renew_geoth.energy
            + p_renew_hydro.energy
            # result: 181.335.186 MWh
        )
        # 2
        p_renew.pct_energy = (
            p_renew.energy
            / p.energy
            # result: 35,4%
        )
        # 3
        p_renew.cost_fuel = (
            p_renew_biomass.cost_fuel
            # result: 3.887,81 Mio €/d_a
        )
        # 4
        p_renew.cost_mro = (
            p_renew_pv.cost_mro
            + p_renew_wind.cost_mro
            + p_renew_biomass.cost_mro
            + p_renew_geoth.cost_mro
            + p_renew_hydro.cost_mro
            # result: 4.114,02 Mio €/d_a
        )

        # 5
        p_renew.CO2e_cb = (
            p_renew_biomass.CO2e_cb
            # result: 3.517.441 d_t/d_a
        )

        p_renew_pv_agri = p_renew_pv_agri
        p_renew_pv_park = p_renew_pv_park

        # Lokale Erneuerbare

        e18 = root.e18
        p_local_pv_roof = p_local_pv_roof
        p_local_pv_facade = p_local_pv_facade
        p_local_pv_park = p_local_pv_park
        p_local_pv_agri = p_local_pv_agri
        p_local_pv = p_local_pv
        p_local_wind_onshore = p_local_wind_onshore
        p_local_biomass = p_local_biomass
        p_local_biomass_cogen = p_local_biomass_cogen
        p_local_hydro = p_local_hydro
        p_local = p_local

        # PV Lokal Dach
        p_local_pv_roof.energy = (
            entry("In_E_PV_power_inst_roof")
            * entry("In_E_pv_full_load_hours_sta")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 34.951.317 MWh

        p_local_pv_roof.cost_mro_per_MWh = (
            p_renew_pv_roof.cost_mro_per_MWh
            # result: 18,4 €/MWh
        )

        p_local_pv_roof.cost_mro = (
            p_local_pv_roof.energy * p_local_pv_roof.cost_mro_per_MWh / Million
        )
        # result: 642,52 Mio €/a

        # PV Lokal Fassade
        p_local_pv_facade.energy = (
            entry("In_E_PV_power_inst_facade")
            * ass("Ass_E_P_local_pv_facade_full_load_hours")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 203.765 MWh

        p_local_pv_facade.cost_mro_per_MWh = (
            ass("Ass_E_S_local_pv_facade_ratio_invest_to_power")
            * ass("Ass_E_P_local_pv_roof_mro_per_year")
            / ass("Ass_E_P_local_pv_facade_full_load_hours")
            * 1000
            # result: 100,0 €/MWh
        )

        p_local_pv_facade.cost_mro = (
            p_local_pv_facade.energy * p_local_pv_facade.cost_mro_per_MWh / Million
        )
        # result: 20,38 Mio €/a

        # PV Lokal Freifläche
        p_local_pv_park.energy = (
            entry("In_E_PV_power_inst_park")
            * entry("In_E_pv_full_load_hours_sta")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 12.175.664 MWh

        p_local_pv_park.cost_mro_per_MWh = (
            p_renew_pv_park.cost_mro_per_MWh
            # result: 13,1 €/MWh
        )

        p_local_pv_park.cost_mro = (
            p_local_pv_park.energy * p_local_pv_park.cost_mro_per_MWh / Million
        )
        # result: 159,88 Mio €/a

        # PV Lokal Agrar
        p_local_pv_agri.energy = (
            entry("In_E_PV_power_inst_agripv")
            * entry("In_E_pv_full_load_hours_sta")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 310.360 MWh

        p_local_pv_agri.cost_mro_per_MWh = p_renew_pv_agri.cost_mro_per_MWh

        p_local_pv_agri.cost_mro = (
            p_local_pv_agri.energy * p_local_pv_agri.cost_mro_per_MWh / Million
        )
        # result: 8,79 Mio €/a

        # PV Local
        p_local_pv.energy = (
            p_local_pv_roof.energy
            + p_local_pv_facade.energy
            + p_local_pv_park.energy
            + p_local_pv_agri.energy
        )
        # result: 47.641.106 MWh

        p_local_pv.cost_mro = (
            p_local_pv_roof.cost_mro
            + p_local_pv_facade.cost_mro
            + p_local_pv_park.cost_mro
            + p_local_pv_agri.cost_mro
        )
        # result: 831,56 Mio €/a

        # Wind Lokal Onshore
        p_local_wind_onshore.energy = (
            entry("In_E_PV_power_inst_wind_on")
            * fact("Fact_E_P_wind_onshore_full_load_hours")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 108.502.605 MWh

        p_local_wind_onshore.cost_mro_per_MWh = (
            ass("Ass_E_P_local_wind_onshore_ratio_invest_to_power_2020")
            * ass("Ass_E_P_local_wind_onshore_mro_per_year")
            / fact("Fact_E_P_wind_onshore_full_load_hours")
            * 1000
            # result: 20,6 €/MWh
        )

        p_local_wind_onshore.cost_mro = (
            p_local_wind_onshore.energy
            * p_local_wind_onshore.cost_mro_per_MWh
            / Million
        )
        # result: 2.236,59 Mio €/a

        # Biomasse Lokal
        p_local_biomass.energy = (
            entry("In_E_PV_power_inst_biomass")
            * fact("Fact_E_P_biomass_full_load_hours")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 51.476.856 MWh

        p_local_biomass.cost_mro_per_MWh = (
            ass("Ass_E_P_local_biomass_mro_per_MWh")
            # result: 18,9 €/MWh
        )

        p_local_biomass.cost_mro = (
            p_local_biomass.energy * p_local_biomass.cost_mro_per_MWh / Million
        )
        # result: 973,94 Mio €/a

        p_local_biomass.cost_fuel_per_MWh = (
            ass("Ass_E_P_local_biomass_material_costs")
            / ass("Ass_E_P_local_biomass_efficiency")
            # result: 75,8 €/MWh
        )

        p_local_biomass.cost_fuel = (
            p_local_biomass.cost_fuel_per_MWh
            * p_local_biomass.energy
            / 1000000
            # result: 3.899,37 Mio €/a
        )
        p_local_biomass.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_local_biomass.CO2e_cb = (
            p_local_biomass.CO2e_cb_per_MWh * p_local_biomass.energy
        )
        # Biomasse KWK Wärme

        p_local_biomass_cogen.pct_energy = fact("Fact_E_P_renew_cogen_ratio_2018")
        # result: 29,7%

        p_local_biomass_cogen.energy = (
            p_local_biomass.energy * p_local_biomass_cogen.pct_energy
        )
        # result: 15.306.680 MWh

        # Laufwasser

        p_local_hydro.energy = (
            entry("In_E_PV_power_inst_water")
            * fact("Fact_E_P_hydro_full_load_hours")
            * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
        )
        # result: 18.019.262 MWh

        p_local_hydro.cost_mro_per_MWh = (
            ass("Ass_E_P_local_hydro_mro_per_MWh")
            # result: 23,8 €/MWh
        )

        p_local_hydro.cost_mro = (
            p_local_hydro.energy * p_local_hydro.cost_mro_per_MWh / Million
        )
        # result: 428,86 Mio €/a

        # Lokale Bruttostromerzeugung
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

        p_fossil.cost_fuel = (
            p_fossil_nuclear.cost_fuel
            + p_fossil_coal_brown.cost_fuel
            + p_fossil_coal_black.cost_fuel
            + p_fossil_gas.cost_fuel
            + p_fossil_ofossil.cost_fuel
        )
        p.cost_fuel = p_fossil.cost_fuel + p_renew.cost_fuel
        p_fossil_nuclear.cost_certificate_per_MWh = 0
        p_fossil_nuclear.cost_certificate = (
            p_fossil_nuclear.cost_certificate_per_MWh
            * p_fossil_nuclear.energy
            / 1000000
        )

        p_fossil.cost_certificate = (
            p_fossil_nuclear.cost_certificate
            + p_fossil_coal_brown.cost_certificate
            + p_fossil_coal_black.cost_certificate
            + p_fossil_gas.cost_certificate
            + p_fossil_ofossil.cost_certificate
        )  # SUM(p_fossil_nuclear.cost_certificate:AM74)

        p.cost_certificate = p_fossil.cost_certificate
        p_fossil.cost_mro = (
            p_fossil_nuclear.cost_mro
            + p_fossil_coal_brown.cost_mro
            + p_fossil_coal_black.cost_mro
            + p_fossil_gas.cost_mro
            + p_fossil_ofossil.cost_mro
        )
        p.cost_mro = p_fossil.cost_mro + p_renew.cost_mro

        p_fossil.CO2e_cb = (
            p_fossil_nuclear.CO2e_cb
            + p_fossil_coal_brown.CO2e_cb
            + p_fossil_coal_black.CO2e_cb
            + p_fossil_gas.CO2e_cb
            + p_fossil_ofossil.CO2e_cb
        )
        p_fossil.CO2e_cb_per_MWh = p_fossil.CO2e_cb / p_fossil.energy
        p.CO2e_cb = p_fossil.CO2e_cb + p_renew.CO2e_cb
        p.CO2e_cb_per_MWh = p.CO2e_cb / p.energy

        p_renew_geoth.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_renew_geoth.CO2e_cb = (
            p_renew_geoth.CO2e_cb_per_MWh
            * p_renew_geoth.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_renew_hydro.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_renew_hydro.CO2e_cb = (
            p_renew_hydro.CO2e_cb_per_MWh
            * p_renew_hydro.energy
            * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        )
        p_local.CO2e_cb = p_local_biomass.CO2e_cb

        e.CO2e_cb = p.CO2e_cb
        p_fossil_nuclear.CO2e_total = p_fossil_nuclear.CO2e_cb
        p_fossil_coal_brown.CO2e_total = p_fossil_coal_brown.CO2e_cb
        p_fossil_ofossil.CO2e_total = 0
        p_fossil_coal_black.CO2e_total = p_fossil_coal_black.CO2e_cb
        p_fossil_gas.CO2e_total = p_fossil_gas.CO2e_cb
        p_fossil_ofossil.CO2e_total = p_fossil_ofossil.CO2e_cb
        p_fossil.CO2e_total = (
            p_fossil_nuclear.CO2e_total
            + p_fossil_coal_brown.CO2e_total
            + p_fossil_coal_black.CO2e_total
            + p_fossil_gas.CO2e_total
            + p_fossil_ofossil.CO2e_total
        )
        p_renew_wind.CO2e_total = 0
        p_renew_biomass_waste.CO2e_total = p_renew_biomass_waste.CO2e_cb
        p_renew_biomass_solid.CO2e_total = p_renew_biomass_solid.CO2e_cb
        p_renew_biomass_gaseous.CO2e_total = p_renew_biomass_gaseous.CO2e_cb
        p_renew_biomass.CO2e_total = (
            p_renew_biomass_waste.CO2e_total
            + p_renew_biomass_solid.CO2e_total
            + p_renew_biomass_gaseous.CO2e_total
        )  # SUM(p_renew_biomass_waste.CO2e_total:p_renew_biomass_gaseous.CO2e_total)

        p_renew_pv_roof.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_renew_pv_facade.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_renew_pv_park.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_renew_pv_agri.CO2e_cb_per_MWh = fact(
            "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
        ) * fact("Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018")
        p_renew_pv_roof.CO2e_cb = (
            p_renew_pv_roof.CO2e_cb_per_MWh * p_renew_pv_roof.energy
        )
        p_renew_pv_facade.CO2e_cb = (
            p_renew_pv_facade.CO2e_cb_per_MWh * p_renew_pv_facade.energy
        )
        p_renew_pv_park.CO2e_cb = (
            p_renew_pv_park.CO2e_cb_per_MWh * p_renew_pv_park.energy
        )
        p_renew_pv_agri.CO2e_cb = (
            p_renew_pv_agri.CO2e_cb_per_MWh * p_renew_pv_agri.energy
        )
        p_renew_pv_agri.CO2e_total = p_renew_pv_agri.CO2e_cb
        p_renew_geoth.CO2e_total = p_renew_geoth.CO2e_cb
        p_renew_hydro.CO2e_total = p_renew_hydro.CO2e_cb
        p_renew_pv_roof.CO2e_total = p_renew_pv_roof.CO2e_cb
        p_renew_pv_facade.CO2e_total = p_renew_pv_facade.CO2e_cb
        p_renew_pv_park.CO2e_total = p_renew_pv_park.CO2e_cb
        p_renew_pv_agri.CO2e_total = p_renew_pv_agri.CO2e_cb

        p_renew_pv.CO2e_total = (
            p_renew_pv_roof.CO2e_total
            + p_renew_pv_facade.CO2e_total
            + p_renew_pv_park.CO2e_total
            + p_renew_pv_agri.CO2e_total
        )  # SUM(p_renew_pv_roof.CO2e_total:p_renew_pv_agri.CO2e_total)

        p_renew.CO2e_total = (
            p_renew_pv.CO2e_total
            + p_renew_wind.CO2e_total
            + p_renew_biomass.CO2e_total
            + p_renew_geoth.CO2e_total
            + p_renew_hydro.CO2e_total
        )

        p.CO2e_total = p_fossil.CO2e_total + p_renew.CO2e_total
        e.CO2e_total = p.CO2e_total

        p_fossil_and_renew.energy = p.energy
        p_fossil_and_renew.CO2e_cb = p_fossil.CO2e_cb + p_renew.CO2e_cb
        p_fossil_and_renew.CO2e_cb_per_MWh = (
            p_fossil_and_renew.CO2e_cb / p_fossil_and_renew.energy
        )
        p_fossil_and_renew.CO2e_total = p_fossil.CO2e_total + p_renew.CO2e_total

        p_fossil_and_renew.pct_energy = p_fossil.pct_energy + p_renew.pct_energy
        p_renew.CO2e_cb_per_MWh = p_renew.CO2e_cb / p_renew.energy
        p_local.pct_energy = p_local.energy / p.energy

    except Exception as e:
        print(e)
        raise
