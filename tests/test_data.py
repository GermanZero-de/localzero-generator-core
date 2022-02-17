import sys
import pandas as pd
from generatorcore.refdata import RefData

refdata = RefData.load(fix_missing_entries=True)
ags_list = list(refdata.ags_master().keys())
# ags_list.remove("DG000000")

by_ags = [
    refdata.area,
    # refdata.area_kinds,
    refdata.buildings,
    refdata.population,
    # refdata.renewable_energy,
    refdata.flats,
    # refdata.traffic,
]


def check_table(table: pd.DataFrame):
    table_name = table.__func__.__name__
    for ags in ags_list:
        try:
            table(ags)
        except Exception as e:
            assert False, "ags: " + ags + " not found in table " + table_name


def test_data_complete_by_ags():
    for table in by_ags:
        check_table(table)
