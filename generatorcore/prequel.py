#!/usr/bin/env python
# coding: utf-8

from setup import *
from dataclasses import dataclass, asdict


# this function brings forward als calculations that are needed prior to
def Prequel_calc(root):
    try:

        # Declarations
        e30 = root.e30
        t30 = root.t30

        #real calculations

        e30.p_local_pv_roof.area_ha_available = ((4 / 3) * ((
            entry('In_R_area_m2_1flat') / 100 * ass('Ass_S_DurchschnittlichtePVFläche_Gebäude_1Wohnung') +
            entry('In_R_area_m2_2flat') / 100 * ass('Ass_S_DurchschnittlichtePVFläche_Gebäude_2Wohnungen') +
            entry('In_R_area_m2_3flat') / 100 * ass('Ass_S_DurchschnittlichtePVFläche_Gebäude_3odermehrWohnungen') +
            entry('In_R_area_m2_dorm') / 100 * ass('Ass_S_DurchschnittlichtePVFläche_Wohnheim'))) / 10000
        )

        #mock values
        t30.s_elec.demand_electricity = 103530852


    except Exception as e:
        print(e)
        raise




