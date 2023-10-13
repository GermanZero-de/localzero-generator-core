"""
This module was auto generated from an annotated version of the 2018 facts file, which
contained explicit formulas for every derived fact. This way we could simplify updating
the facts, without changing a lot of the actual code.
"""

from . import refdata


def calculate_derived_facts(rd: refdata.RefData):
    f = rd.facts()

    f.add_derived_fact(
        "Fact_H_P_heatnet_prodvol_brutto_2018",
        f.fact("Fact_H_P_heatnet_cogen_prodvol_2018")
        + f.fact("Fact_H_P_heatnet_plant_prodvol_2018"),
        {
            "group": "ui",
            "description": "BruttofernwÃ¤rmeerzeugung Deutschland 2018",
            "unit": "MWh/a",
            "rationale": "UmwandlungsausstroÃŸ insgesamt gibt die BruttofernwÃ¤rmeerzeugung aus Heizkraftwerken der allg. Versorgung (Teilmenge der WÃ¤rmekraftwerke, nÃ¤mlich die mit KWK) und Fernheizwerken an",
            "reference": "AG EB 2018 Zeile 32, Spalte AF",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_heatnet_ratio_netto_to_brutto_2018",
        f.fact("Fact_H_P_heatnet_fec_2018")
        / f.fact("Fact_H_P_heatnet_prodvol_brutto_2018"),
        {
            "group": "ui",
            "description": "VerhÃ¤ltnis NettofernwÃ¤rmeerzeugung zu BruttofernwÃ¤rmeerzeugung Deutschland 2018",
            "unit": "MWh/a",
            "rationale": "Division von Fact_H_P_heatnet_fec_2018/Fact_H_P_heatnet_prodvol_brutto_2018",
            "reference": "AG EB 2018 Zeile 32+45, Spalte AF",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_coal_CO2e_cb_2018") / f.fact("Fact_H_P_coal_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor verbrennungsbedingte CO2e Herstellung fester Brennstoffe/Kohle (CRF 1.A.1.c) vs. EEV Kohle 2018",
            "unit": "",
            "rationale": "Fact_H_P_coal_CO2e_cb_2018/Fact_H_P_coal_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018",
        f.fact("Fact_H_P_coal_CO2e_pb_2018") / f.fact("Fact_H_P_coal_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor produktionsbedingte CO2e (Diffuse Emissionen) Kohlebergbau und -umwandlung 2018 (CRF 1.B.1) vs. EEV Kohle 2018",
            "unit": "",
            "rationale": "Fact_H_P_coal_CO2e_pb_2018/Fact_H_P_coal_fec_2018",
            "reference": "NIR S.182ff",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_gas_CO2e_cb_2018") / f.fact("Fact_H_P_gas_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor verbrennungsbedingte CO2e Erdgas(netz) 2018 (CRF 1.A.3.e) vs. EEV Erdgas 2018",
            "unit": "",
            "rationale": "Fact_H_P_gas_CO2e_cb_2018/Fact_H_P_gas_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018",
        f.fact("Fact_H_P_gas_CO2e_pb_2018") / f.fact("Fact_H_P_gas_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor prozesssbedingte CO2e (Diffuse Emissionen) Gas 2018 (CRF 1.B.2.b) vs. EEV Erdgas 2018",
            "unit": "",
            "rationale": "Fact_H_P_gas_CO2e_pb_2018/Fact_H_P_gas_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_opetpro_CO2e_pb_2018",
        f.fact("Fact_H_P_opetpro_CO2e_1B2a_2018")
        + f.fact("Fact_H_P_opetpro_CO2e_1B2c_2018"),
        {
            "group": "ui",
            "description": "Prozessbedingte CO2e sonstige MineralÃ¶lprodukte 2018",
            "unit": "",
            "rationale": "Summe aus CRF 1.B.2.a und CRF 1.B.2.c",
            "reference": "NIR S 265, 289",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018",
        f.fact("Fact_H_P_opetpro_CO2e_pb_2018") / f.fact("Fact_H_P_opetpro_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor prozesssbedingte CO2e (Roh)Ã–l Lagerung etc. 2018 (CRF 1.B.2.a) vs. EEV Sonstige MineralÃ¶lprodukte 2018",
            "unit": "",
            "rationale": "Fact_H_P_opetpro_CO2e_pb_2018/Fact_H_P_opetpro_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018",
        f.fact("Fact_H_P_orenew_CO2e_pb_2018") / f.fact("Fact_H_P_orenew_fec_2018"),
        {
            "group": "ui",
            "description": "Emissionsfaktor prozesssbedingte CO2e sonstige EE (Geothermie) 2018 (CRF 1.B.2.d) vs. EEV Sonstige EE 2018",
            "unit": "",
            "rationale": "Fact_H_P_orenew_CO2e_pb_2018/Fact_H_P_orenew_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018",
        f.fact("Fact_H_P_biomass_CO2e_pb_2018") / f.fact("Fact_H_P_biomass_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor prozesssbedingte CO2e Biomasse und erneuerbare AbfÃ¤lle vs. EEV Biomasse 2018",
            "unit": "",
            "rationale": "Fact_H_P_biomass_CO2e_pb_2018/Fact_H_P_biomass_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018",
        f.fact("Fact_H_P_ofossil_CO2e_pb_2018") / f.fact("Fact_H_P_ofossil_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor prozesssbedingte CO2e Sonstige (fossile) EnergietrÃ¤ger (Nichterneuerbare AbfÃ¤lle, AbwÃ¤rme) vs. EEV Sonstige EE 2018",
            "unit": "",
            "rationale": "Fact_H_P_ofossil_CO2e_pb_2018/Fact_H_P_ofossil_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_fueloil_CO2e_cb_2018") / f.fact("Fact_H_P_fueloil_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor verbrennungsbedingte CO2e MineralÃ¶lwirtschaft 2018 HeizÃ¶l (leicht) (Teil CRF 1.A.1.b) vs. EEV HeizÃ¶l 2018",
            "unit": "",
            "rationale": "Fact_H_P_fueloil_CO2e_cb_2018/Fact_H_P_fueloil_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_lpg_CO2e_cb_2018") / f.fact("Fact_H_P_lpg_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor verbrennungsbedingte CO2e MineralÃ¶lwirtschaft 2018 LPG (Teil CRF 1.A.1.b) vs. EEV LPG 2018",
            "unit": "",
            "rationale": "Fact_H_P_lpg_CO2e_cb_2018/Fact_H_P_lpg_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_opetpro_CO2e_cb_2018") / f.fact("Fact_H_P_opetpro_fec_2018"),
        {
            "group": "ud",
            "description": "Emissionsfaktor verbrennungsbedingte CO2e MineralÃ¶lwirtschaft 2018 sonstige MineralÃ¶lprodukte (Teil CRF 1.A.1.b) vs. EEV Sonstige MineralÃ¶lprodukte 2018",
            "unit": "",
            "rationale": "Fact_H_P_opetpro_CO2e_cb_2018/Fact_H_P_opetpro_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_heatnet_cogen_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_heatnet_cogen_CO2e_cb_2018")
        / (
            f.fact("Fact_H_P_heatnet_cogen_prodvol_2018")
            * f.fact("Fact_H_P_heatnet_ratio_netto_to_brutto_2018")
        ),
        {
            "group": "ud",
            "description": "Mittlerer Emissionsfaktor CO2e KWK-WÃ¤rme aus Heizkraftwerken der allgemeinen Versorgung 2018 (Teil aus 1.A.1.a)",
            "unit": "t CO2e/MWh",
            "rationale": "Gesamtemissionen aus der KWK-FernwÃ¤rmeerzeugung geteilt durch deren netto FernwÃ¤rmebereitstellung: Fact_H_P_heatnet_cogen_CO2e_cb_2018/(Fact_H_P_heatnet_cogen_prodvol_2018*Fact_H_P_heatnet_ratio_netto_to_brutto_2018)",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_heatnet_plant_CO2e_cb_2018")
        / (
            f.fact("Fact_H_P_heatnet_plant_prodvol_2018")
            * f.fact("Fact_H_P_heatnet_ratio_netto_to_brutto_2018")
        ),
        {
            "group": "ud",
            "description": "Mittlerer Emissionsfaktor CO2e FernwÃ¤rme aus Fernheizwerken der allgemeinen Versorgung 2018 (Teil aus CRF 1.A.1.a)",
            "unit": "t CO2e/MWh",
            "rationale": "Gesamtemissionen aus der Fernheizwerk-FernwÃ¤rmeerzeugung geteilt durch deren netto FernwÃ¤rmebereitstellung: Fact_H_P_heatnet_plant_CO2e_cb_2018/(Fact_H_P_heatnet_plant_prodvol_2018*Fact_H_P_heatnet_ratio_netto_to_brutto_2018)",
            "reference": "",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_H_P_heatnet_biomass_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_H_P_heatnet_biomass_CO2e_cb_2018")
        / f.fact("Fact_H_P_heatnet_biomass_fec_2018"),
        {
            "group": "ud",
            "description": "Mittlerer Emissionsfaktor verbrennungsbedingte CO2e aus non-CO2-THG der Biomasse-KWK-WÃ¤rme aus Heizkraftwerken der allgemeinen Versorgung 2018 (Teil aus 1.A.1.a)",
            "unit": "t CO2e/MWh",
            "rationale": "Berechnung =Fact_H_P_heatnet_biomass_CO2e_cb_2018/Fact_H_P_heatnet_biomass_fec_2018 ,\nDieser ist ein gewichteter Mittelwert aller eingesetzter BiomassetrÃ¤ger fÃ¼r die WÃ¤rmeproduktion der allgemeinen Versorgung nach UBA 2019.",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_E_P_ratio_gross_electricity_prod_to_fec_electricity_2018",
        f.fact("Fact_E_P_elec_prodvol_brutto_2018")
        / f.fact("Fact_E_P_elec_prodvol_netto_2018"),
        {
            "group": "ud",
            "description": "VerhÃ¤ltnis Bruttostromerzeugung/Endenergieverbrauch Strom 2018",
            "unit": "",
            "rationale": "Emissionsfaktoren werden auf die Bruttostromerzeugung BSE (gross energy production = gep) (643,451 TWh in 2018) bezogen. Wir arbeiten aber mit dem Endenergieverbrauch EEV (513,327 TWh in 2018). Um auf den richtigen Bundeswert der THG-Emissionen 2018 zu kommen, mÃ¼ssen wir die Berechnung also mit BSE/EEV skalieren. Berechnung =Fact_E_P_elec_prodvol_brutto_2018/E_P_elec_prodvol_netto_2018",
            "reference": "AG EB 2018 Zeile 32+45, Spalte AD",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_E_P_coal_black_cogen_ratio_2018",
        f.fact("Fact_H_P_heatnet_cogen_coal_black_prodvol_2018")
        * f.fact("Fact_H_P_heatnet_ratio_netto_to_brutto_2018")
        / (
            f.fact("Fact_E_P_elec_prodvol_netto_2018")
            * f.fact("Fact_E_P_coal_black_pct_of_gep_2018")
        ),
        {
            "group": "ud",
            "description": "Prozentualer Aufschlag Netto(EEV)-KWK-FernwÃ¤rmeerzeugung auf Nettostromerzeugung aus Steinkohle 2018",
            "unit": "%",
            "rationale": "Netto(EEV)-KWK-FernwÃ¤rme aus Steinkohle geteilt durch Nettostromerzeugung aus Steinkohle: Fact_H_P_heatnet_cogen_coal_black_prodvol_2018*Fact_H_P_heatnet_ratio_netto_to_brutto_2018/(Fact_E_P_elec_prodvol_netto_2018*Fakt_S_B_Steinkohle_Anteil2018)",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_E_P_coal_brown_cogen_ratio_2018",
        f.fact("Fact_H_P_heatnet_cogen_coal_brown_prodvol_2018")
        * f.fact("Fact_H_P_heatnet_ratio_netto_to_brutto_2018")
        / (
            f.fact("Fact_E_P_elec_prodvol_netto_2018")
            * f.fact("Fact_E_P_coal_brown_pct_of_gep_2018")
        ),
        {
            "group": "ud",
            "description": "Prozentualer Aufschlag Netto(EEV)-KWK-FernwÃ¤rmeerzeugung auf Nettostromerzeugung aus Braunkohle 2018",
            "unit": "%",
            "rationale": "Netto(EEV)-KWK-FernwÃ¤rme aus Braunkohle geteilt durch Nettostromerzeugung aus Braunkohle: Fact_H_P_heatnet_cogen_coal_brown_prodvol_2018*Fact_H_P_heatnet_ratio_netto_to_brutto_2018/(Fact_E_P_elec_prodvol_netto_2018*Fakt_S_B_Braunkohle_Anteil2018)",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_E_P_gas_cogen_ratio_2018",
        f.fact("Fact_H_P_heatnet_cogen_gas_prodvol_2018")
        * f.fact("Fact_H_P_heatnet_ratio_netto_to_brutto_2018")
        / (
            f.fact("Fact_E_P_elec_prodvol_netto_2018")
            * f.fact("Fact_E_P_gas_pct_of_gep_2018")
        ),
        {
            "group": "ud",
            "description": "Prozentualer Aufschlag Netto(EEV)-KWK-FernwÃ¤rmeerzeugung auf Nettostromerzeugung aus Erdgas 2018",
            "unit": "%",
            "rationale": "Netto(EEV)-KWK-FernwÃ¤rme aus Erdgas geteilt durch Nettostromerzeugung aus Erdgas: Fact_H_P_heatnet_cogen_gas_prodvol_2018*Fact_H_P_heatnet_ratio_netto_to_brutto_2018/(Fact_E_P_elec_prodvol_netto_2018*Fakt_S_B_Gas_Anteil2018)",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_E_P_ofossil_cogen_ratio_2018",
        f.fact("Fact_H_P_heatnet_cogen_ofossil_prodvol_2018")
        * f.fact("Fact_H_P_heatnet_ratio_netto_to_brutto_2018")
        / (
            f.fact("Fact_E_P_elec_prodvol_netto_2018")
            * f.fact("Fact_E_P_ofossil_pct_of_gep_2018")
        ),
        {
            "group": "ud",
            "description": "Prozentualer Aufschlag Netto(EEV)-KWK-FernwÃ¤rmeerzeugung auf Nettostromerzeugung aus sonstigen EnergietrÃ¤gern (inkl. MineralÃ¶l) 2018",
            "unit": "%",
            "rationale": "Netto(EEV)-KWK-FernwÃ¤rme aus sonstigen EnergietrÃ¤gern (inkl. MineralÃ¶l) geteilt durch Nettostromerzeugung aus sonstigen EnergietrÃ¤gern (inkl. MineralÃ¶l): Fact_H_P_heatnet_cogen_ofossil_prodvol_2018*Fact_H_P_heatnet_ratio_netto_to_brutto_2018/(Fact_E_P_elec_prodvol_netto_2018*Fakt_S_B_sonst.konv_Anteil2018)",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_E_P_pv_rest_pct_of_gep_pv_2017",
        1
        - f.fact("Fact_E_P_pv_roof_pct_of_gep_pv_2017")
        - f.fact("Fact_E_P_pv_park_pct_of_gep_pv_2017"),
        {
            "group": "ud",
            "description": "Anteil Rest (Fassade + Agri) an PV D-Land 2017",
            "unit": "%",
            "rationale": 'Auswertung foerderal Erneuerbar, Alle "Sonstige" jeweils zur Hälfte der Fassaden-PV und der Agrar-PV zugerechnet',
            "reference": "foerderal Erneuerbar",
            "link": "https://www.foederal-erneuerbar.de/uebersicht/bundeslaender/BW%7CBY%7CB%7CBB%7CHB%7CHH%7CHE%7CMV%7CNI%7CNRW%7CRLP%7CSL%7CSN%7CST%7CSH%7CTH%7CD/kategorie/solar/auswahl/991-anteil_freiflaechena/#goto_993",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2018",
        f.fact("Fact_F_P_petindus_CO2e_cb_2018")
        / f.fact("Fact_F_P_petindus_prodvol_2018"),
        {
            "group": "ui",
            "description": "Faktor CO2e MineralÃ¶lraffinerien pro t 2018",
            "unit": "CO2e/t",
            "rationale": "NIR CO2e Wert fÃ¼r MineralÃ¶lraffinerien (CRF 1.A.1.b) wird auf die komplette MineralÃ¶lwirtschaftsprodukton gleichverteilt nach Produktionsmengen laut MVW Jahresbericht 2019 umgelegt, Berechnung: Fact_F_P_petindus_CO2e_cb_2018/Fact_F_P_petindus_prodvol_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_petrol_CO2e_cb_2018",
        f.fact("Fact_F_P_petrol_prodvol_2018")
        * f.fact("Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2018"),
        {
            "group": "ui",
            "description": "CO2e MineralÃ¶lwirtschaft 2018 Benzin",
            "unit": "t",
            "rationale": "CO2e aus CRF 1.A.1.b anteilig nach Produktionsmenge laut MWV Jahresbericht 2019, berechnet aus Fact_F_P_petrol_prodvol_2018, Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_jetfuel_CO2e_cb_2018",
        f.fact("Fact_F_P_jetfuel_prodvol_2018")
        * f.fact("Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2018"),
        {
            "group": "ui",
            "description": "CO2e MineralÃ¶lwirtschaft 2018 Kerosin",
            "unit": "t",
            "rationale": "CO2e aus CRF 1.A.1.b anteilig nach Produktionsmenge laut MWV Jahresbericht 2019, berechnet aus Fact_F_P_jetfuel_prodvol_2018, Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2020",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_diesel_CO2e_cb_2018",
        f.fact("Fact_F_P_diesel_prodvol_2018")
        * f.fact("Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2018"),
        {
            "group": "ui",
            "description": "CO2e MineralÃ¶lwirtschaft 2018 Diesel",
            "unit": "t",
            "rationale": "CO2e aus CRF 1.A.1.b anteilig nach Produktionsmenge laut MWV Jahresbericht 2019, berechnet aus Fact_F_P_diesel_prodvol_2018, Fact_F_P_petindus_ratio_CO2e_cb_to_prodvol_2019",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_F_P_petrol_CO2e_cb_2018") / f.fact("Fact_F_P_petrol_fec_2018"),
        {
            "group": "ud",
            "description": "Faktor CO2e zu EEV Benzin 2018",
            "unit": "",
            "rationale": "Dieser Faktor gibt an, wie viele CO2e bei der Benzinproduktion in Deutschland entstehen, geteilt jedoch durch den Endenergieverbrauch, in dem auch die Einfuhr enthalten ist. Berechnung =Fact_F_P_petrol_CO2e_cb_2018/Fact_F_P_petrol_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_F_P_diesel_CO2e_cb_2018") / f.fact("Fact_F_P_diesel_fec_2018"),
        {
            "group": "ud",
            "description": "Faktor CO2e zu EEV Diesel 2018",
            "unit": "",
            "rationale": "Dieser Faktor gibt an, wie viele CO2e bei der Dieselproduktion in Deutschland entstehen, geteilt jedoch durch den Endenergieverbrauch, in dem auch die Einfuhr enthalten ist. Berechnung =Fact_F_P_diesel_CO2e_cb_2018/Fact_F_P_diesel_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
    f.add_derived_fact(
        "Fact_F_P_jetfuel_ratio_CO2e_cb_to_fec_2018",
        f.fact("Fact_F_P_jetfuel_CO2e_cb_2018") / f.fact("Fact_F_P_jetfuel_fec_2018"),
        {
            "group": "ud",
            "description": "Faktor CO2e zu EEV Kerosin 2018",
            "unit": "",
            "rationale": "Dieser Faktor gibt an, wie viele CO2e bei der Kerosinproduktion in Deutschland entstehen, geteilt jedoch durch den Endenergieverbrauch, in dem auch die Einfuhr enthalten ist. Berechnung =Fact_F_P_jetfuel_CO2e_cb_2018/Fact_F_P_jetfuel_fec_2018",
            "reference": "Berechnung",
            "link": "",
        },
    )
