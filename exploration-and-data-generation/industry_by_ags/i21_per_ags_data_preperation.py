import pandas as pd
import numpy as np

PATH_I21_VALUES = "i21_values_germany.csv"  # all i18 from an export of the current cenerator
PATH_FILE_EXPORT = "i21_ratio_x_to_co2e_total.csv"

AGS_FILE_PATH = "./data/2021.csv"
DEHST_FILE_PATH = "Anlagenliste_2022_de_Excel.xlsx"
AGS_MATCH_EXPORT_PATH = "industry_ags_match_reduced_export.csv"

AGS_TO_STATE = {
    "01": "SH",
    "02": "HH",
    "03": "NI",
    "04": "HB",
    "05": "NW",
    "06": "HE",
    "07": "RP",
    "08": "BW",
    "09": "BY",
    "10": "SL",
    "11": "BE",
    "12": "BB",
    "13": "MV",
    "14": "SN",
    "15": "ST",
    "16": "TH",
}

# only usable for 2018 VET as not all NACE identifiers are added (only the ones present in the excel sheet)
MAPPER_NACE_WZ = {
    "miner_cement": ["23.51", "23.65"],
    "miner_chalk": ["23.52", "23.62"],
    "miner_glas": ["23.1"],
    "miner_ceram": ["23.2", "23.3", "23.4"],
    "chem_basic": ["20.11", "20.12", "20.13", "20.14", "20.16"],
    "chem_ammonia": ["20.15"],
    "chem_other": ["20.2", "20.3", "20.4", "20.5", "20.6", "21."],
    "metal_steel": [
        "24.1",
        "25.5",
        "25.61",
    ],  # primary and secondary is sorted by cities later
    "metal_nonfe": ["24.4", "24.53", "24.54"],
    "other_paper": ["17."],
    "other_food": ["10.8", "10.6", "10.5", "10.4", "10.3", "11.05", "12.00"],
    # "other_further": ["8.", "22.", "24.2", "24.3", "25.", "28.1", "29.", "30."],
    "other_further": [
        "13.",
        "14.",
        "15.",
        "16.",
        "18.",
        "22.",
        "23.61",
        "23.64",
        "23.69",
        "23.7",
        "23.9" "24.2",
        "24.3",
        "25.1",
        "25.2",
        "25.3",
        "25.4",
        "25.62",
        "25.7",
        "25.8",
        "26.9",
        "27.",
        "28.1",
        "29.",
        "30.",
        "31.",
        "32.",
        "33.",
    ],
}

IDS_PRIMARY_STEEL = [
    56,
    70,
    52,
    1086,
    59,
    53,
    69,
    206009,
    60,
    1228,
    43,
]  # manual selection of steel primary facilities


def add_zeros(ags):
    if not pd.isna(ags):
        ags = str(ags)
        length_ags = len(ags)
        if length_ags < 8:
            ags = "0" * (8 - length_ags) + ags
    return ags


def preprocess_dehst_data(ags_file_path, dehst_file_path, export_path):
    df_ags = pd.read_csv(ags_file_path)

    df_anlagen = pd.read_excel(
        dehst_file_path,
        sheet_name="Anlagen_Liste",
        decimal=",",
        thousands=".",
        converters={
            "Bundesland": "str",
            "AGS_manual": "str",
            "VET 2018 [t CO2 Äq]": "int",
            "ID": "int",
        },  # type: ignore
    )

    df_anlagen.rename(
        columns={
            "Standort der Anlage": "Ort",
            "AGS": "AGS_xls",
            "VET 2018 [t CO2 Äq]": "VET2018_t",
            "Haupttätigkeit nach TEHG": "TEHG_Nr",
            "Bezeichnung Haupttätigkeit nach TEHG": "TEHG_name",
            "NACE WZ2008": "nace_wz",
        },
        inplace=True,
    )
    df_anlagen = df_anlagen[
        [
            "ID",
            "Nummer",
            "Betreiber",
            "Anlagenname",
            "Bundesland",
            "Ort Original",
            "Ort",
            "VET2018_t",
            "TEHG_Nr",
            "TEHG_name",
            "nace_wz",
            "AGS_manual",
        ]
    ]
    df_anlagen["AGS_manual"] = df_anlagen["AGS_manual"].apply(add_zeros)
    df_anlagen.dropna(subset=["nace_wz"], inplace=True)

    df_anlagen["i_category"] = "No category"
    for key, item in MAPPER_NACE_WZ.items():
        if len(item) > 0:
            for name in item:
                df_anlagen.loc[
                    df_anlagen["nace_wz"].str.contains(name), "i_category"
                ] = key

    df_anlagen.loc[
        (df_anlagen["i_category"] == "metal_steel")
        & (df_anlagen["ID"].isin(IDS_PRIMARY_STEEL)),
        "i_category",
    ] = "metal_steel_primary"
    df_anlagen.loc[
        df_anlagen["i_category"] == "metal_steel", "i_category"
    ] = "metal_steel_secondary"
    df_anlagen = df_anlagen[df_anlagen["i_category"] != "No category"]

    df_ags["ags_state_digits"] = [x[:2] for x in df_ags["ags"]]
    df_ags["state"] = df_ags["ags_state_digits"].map(AGS_TO_STATE)
    # remove everything behind a , (for example `, Stadt` or `, Landkreis`)
    df_ags["name"] = df_ags["description"].str.split(",").str[0]

    # select duplicates in AGS list
    df_ags_duplicates = df_ags[df_ags.duplicated(subset="name", keep=False)]
    df_ags_duplicates = df_ags_duplicates.sort_values("name")
    df_ags_no_duplicates = df_ags.drop_duplicates(subset="name", keep=False)
    n = 0
    mask_duplicates_state_unique = [False] * len(df_ags_duplicates)
    while True:
        row = df_ags_duplicates.iloc[n]
        ort_count = df_ags_duplicates[df_ags_duplicates["name"] == row["name"]].shape[0]

        if ort_count == 2:
            if row["state"] != df_ags_duplicates.iloc[n + 1]["state"]:
                mask_duplicates_state_unique[n] = True
                mask_duplicates_state_unique[n + 1] = True

        elif ort_count == 3:
            if (
                (row["state"] != df_ags_duplicates.iloc[n + 1]["state"])
                & (row["state"] != df_ags_duplicates.loc[:, "state"].iloc[n + 2])
                & (
                    df_ags_duplicates.loc[:, "state"].iloc[n + 1]
                    != df_ags_duplicates.loc[:, "state"].iloc[n + 2]
                )
            ):
                mask_duplicates_state_unique[n] = True
                mask_duplicates_state_unique[n + 1] = True
                mask_duplicates_state_unique[n + 2] = True

        n += ort_count
        if n >= len(df_ags_duplicates):
            break
    df_ags_duplicates_state_unique = df_ags_duplicates[mask_duplicates_state_unique]

    # Find AGS for "Ort"
    # This is a multi step process iterating over every entry in df_anlagen terminating at the earliest match
    # 1. if column AGS_manual has an entry this entry is used as AGS
    # 2. search for a match of "Ort" inside the dg_ags_no_duplicates list
    # 3. search for a match inside the df_ags_duplicates_state_unique for a match of "Ort" and "State"
    # 4. For all not matched entries of df_anlagen check if the df_ags_no_duplicates "Ort" does start with the location of the "Anlage" (also check if the state matches)

    for index, row in df_anlagen.iterrows():
        state_anlage = row.loc["Bundesland"]
        location_anlage = row.loc["Ort"]
        if ~df_anlagen.loc[:, "AGS_manual"].isna().loc[index]:
            # print(df_anlagen.loc[index, "AGS_manual"])
            df_anlagen.loc[index, "AGS"] = df_anlagen.loc[index, "AGS_manual"]
            df_anlagen.loc[index, "match_type"] = "manual_entry"
        else:
            temp_ags_match = df_ags_no_duplicates.loc[
                (df_ags_no_duplicates["name"] == location_anlage)
            ]
            # select entries with only one match
            if temp_ags_match.shape[0] == 1:
                if temp_ags_match["state"].values[0] == state_anlage:
                    df_anlagen.loc[index, "AGS"] = temp_ags_match["ags"].values[0]
                    df_anlagen.loc[index, "match_type"] = "direct"
            else:
                temp_ags_match_dup = df_ags_duplicates_state_unique.loc[
                    (df_ags_duplicates_state_unique["name"] == location_anlage)
                ]
                if temp_ags_match_dup.shape[0] == 1:
                    raise ValueError(
                        "Duplicate entry selection wrong. Single entry found in AGS list"
                    )
                elif temp_ags_match_dup.shape[0] > 1:
                    for index_match, match in temp_ags_match_dup.iterrows():
                        if match["state"] == state_anlage:
                            df_anlagen.loc[index, "AGS"] = match["ags"]
                            df_anlagen.loc[
                                index, "match_type"
                            ] = "dublicate_match_state_unique"

    for index, row in df_anlagen[df_anlagen["match_type"].isna()].iterrows():
        state_anlage = row.loc["Bundesland"]
        location_anlage = row.loc["Ort"]
        temp_ags_match = df_ags_no_duplicates[
            df_ags_no_duplicates["name"].str.startswith(location_anlage) == True
        ]
        if temp_ags_match.shape[0] == 1:
            if temp_ags_match["state"].values[0] == state_anlage:
                df_anlagen.loc[index, "AGS"] = temp_ags_match["ags"].values[0]
                df_anlagen.loc[index, "match_type"] = "starts_with_only_one_match"
    df_anlagen = df_anlagen[~pd.isna(df_anlagen["match_type"])]
    df_anlagen[["Ort Original", "VET2018_t", "i_category", "AGS"]].to_csv(
        export_path, index=False
    )
    # df_anlagen.to_csv("industry_ags_match_full_export.csv")


def calcualate_factors_to_co2e_total(file_path, export_path):
    """Calculate the factors to calculate the i18 values from CO2e_total per category
    and export the factors to csv."""
    # TODO add "Energieträger" (research for ratios necessary)
    df = pd.read_csv(
        file_path,
        decimal=",",
        thousands=".",
        sep=";",
    )
    df[["cat", "type"]] = df["description"].str.split(pat=".", expand=True)[[2, 3]]

    for categorie in df["cat"].unique():
        co2e_total = df[
            np.logical_and(df["cat"] == categorie, df["type"] == "CO2e_total")
        ]["value"].values[0]
        df.loc[df["cat"] == categorie, "raito_CO2_total"] = (
            df[df["cat"] == categorie]["value"] / co2e_total
        )

    df[["cat", "type", "raito_CO2_total"]].to_csv(export_path, index=False)


def main():
    calcualate_factors_to_co2e_total(PATH_I21_VALUES, PATH_FILE_EXPORT)


if __name__ == "__main__":
    main()
