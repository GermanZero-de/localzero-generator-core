from .inputs import Inputs
from dataclasses import dataclass, asdict


@dataclass
class LColVars2030:

    area_ha: float = -1
    CO2e_pb_per_t: float = -1
    pct_x: float = -1
    CO2e_pb_per_MWh: float = -1
    CO2e_cb: float = -1
    CO2e_pb: float = -1
    CO2e_total: float = -1
    invest: float = -1
    change_CO2e_t: float = -1
    change_CO2e_pct: float = -1
    CO2e_total_2021_estimated: float = -1
    cost_climate_saved: float = -1
    invest_pa: float = -1
    cost_wage: float = -1
    demand_emplo: float = -1
    demand_emplo_new: float = -1
    demand_change: float = -1
    area_ha_change: float = -1
    CO2e_cb_per_t: float = -1
    action: float = -1
    pct_of_wage: float = -1
    ratio_wage_to_emplo: float = -1
    emplo_existing: float = -1
    invest_per_x: float = -1
    area_ha_available_pct_of_action: float = -1
    area_ha_available: float = -1
    change_within_category: float = -1
    change_wet_org_low: float = -1
    change_wet_org_high: float = -1


@dataclass
class L30:
    # Klassenvariablen für L18
    l: LColVars2030 = LColVars2030()
    e: LColVars2030 = LColVars2030()
    g: LColVars2030 = LColVars2030()
    g_forest: LColVars2030 = LColVars2030()
    g_forest_managed: LColVars2030 = LColVars2030()
    g_forest_natural: LColVars2030 = LColVars2030()
    g_crop: LColVars2030 = LColVars2030()
    g_crop_org: LColVars2030 = LColVars2030()
    g_crop_min_conv: LColVars2030 = LColVars2030()
    g_crop_min_hum: LColVars2030 = LColVars2030()
    g_crop_org_low: LColVars2030 = LColVars2030()
    g_crop_org_high: LColVars2030 = LColVars2030()
    g_grass: LColVars2030 = LColVars2030()
    g_grass_min_conv: LColVars2030 = LColVars2030()
    g_grass_org_low: LColVars2030 = LColVars2030()
    g_grass_org_high: LColVars2030 = LColVars2030()
    g_grove: LColVars2030 = LColVars2030()
    g_grove_min: LColVars2030 = LColVars2030()
    g_grove_org: LColVars2030 = LColVars2030()
    g_grove_org_low: LColVars2030 = LColVars2030()
    g_grove_org_high: LColVars2030 = LColVars2030()
    g_wet: LColVars2030 = LColVars2030()
    g_wet_min: LColVars2030 = LColVars2030()
    g_wet_org_rp: LColVars2030 = LColVars2030()
    g_wet_org_low: LColVars2030 = LColVars2030()
    g_wet_org_high: LColVars2030 = LColVars2030()
    g_wet_org_low_r: LColVars2030 = LColVars2030()
    g_wet_org_low_rp: LColVars2030 = LColVars2030()
    g_wet_org_high_r: LColVars2030 = LColVars2030()
    g_wet_org_high_rp: LColVars2030 = LColVars2030()
    g_water: LColVars2030 = LColVars2030()
    g_water_min: LColVars2030 = LColVars2030()
    g_water_org: LColVars2030 = LColVars2030()
    g_water_min_low: LColVars2030 = LColVars2030()
    g_water_min_high: LColVars2030 = LColVars2030()
    g_settlement: LColVars2030 = LColVars2030()
    g_settlement_org: LColVars2030 = LColVars2030()
    g_settlement_min: LColVars2030 = LColVars2030()
    g_settlement_org_low: LColVars2030 = LColVars2030()
    g_settlement_org_high: LColVars2030 = LColVars2030()
    g_other: LColVars2030 = LColVars2030()
    g_wood: LColVars2030 = LColVars2030()
    pyrolysis: LColVars2030 = LColVars2030()
    g_planning: LColVars2030 = LColVars2030()
    g_crop_org: LColVars2030 = LColVars2030()
    g_grass_org: LColVars2030 = LColVars2030()
    g_grove_org: LColVars2030 = LColVars2030()
    g_wet_org: LColVars2030 = LColVars2030()
    g_wet_org_r: LColVars2030 = LColVars2030()
    g_wet_org_rp: LColVars2030 = LColVars2030()
    g_water_org_low: LColVars2030 = LColVars2030()
    g_water_org_high: LColVars2030 = LColVars2030()

    # erzeuge dictionry

    def dict(self):
        return asdict(self)


def calc(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    """"""
    """ import external values"""
    import json

    if entry("In_M_AGS_com") == "DG000000":
        excel_path = "excel/germany_values.json"
    elif entry("In_M_AGS_com") == "03159016":
        excel_path = "excel/goettingen_values.json"

    with open(excel_path, "r") as fp:
        exl = json.load(fp)
    fp.close()
    """end"""

    root.h30.h.CO2e_total = exl["h30"]["h"]["CO2e_total"]
    root.e30.e.CO2e_total = exl["e30"]["e"]["CO2e_total"]
    root.f30.f.CO2e_total = exl["f30"]["f"]["CO2e_total"]
    root.r30.r.CO2e_total = exl["r30"]["r"]["CO2e_total"]
    # root.b30.b.CO2e_total = exl["b30"]["b"]["CO2e_total"]
    # root.i30.i.CO2e_total = exl["i30"]["i"]["CO2e_total"]
    # root.t30.t.CO2e_total = exl["t30"]["t"]["CO2e_total"]
    root.a30.a.CO2e_total = exl["a30"]["a"]["CO2e_total"]

    l18 = root.l18
    l = root.l30.l
    e = root.l30.e
    g = root.l30.g
    g_forest = root.l30.g_forest
    g_forest_managed = root.l30.g_forest_managed
    g_forest_natural = root.l30.g_forest_natural
    g_crop = root.l30.g_crop
    g_crop_org = root.l30.g_crop_org
    g_crop_min_conv = root.l30.g_crop_min_conv
    g_crop_min_hum = root.l30.g_crop_min_hum
    g_crop_org_low = root.l30.g_crop_org_low
    g_crop_org_high = root.l30.g_crop_org_high
    g_grass = root.l30.g_grass
    g_grass_org = root.l30.g_grass_org
    g_grass_min_conv = root.l30.g_grass_min_conv
    g_grass_org_low = root.l30.g_grass_org_low
    g_grass_org_high = root.l30.g_grass_org_high
    g_grove = root.l30.g_grove
    g_grove_min = root.l30.g_grove_min
    g_grove_org = root.l30.g_grove_org
    g_grove_org_low = root.l30.g_grove_org_low
    g_grove_org_high = root.l30.g_grove_org_high
    g_wet = root.l30.g_wet
    g_wet_min = root.l30.g_wet_min
    g_wet_org = root.l30.g_wet_org
    g_wet_org_rp = root.l30.g_wet_org_rp
    g_wet_org_r = root.l30.g_wet_org_r
    g_wet_org_low = root.l30.g_wet_org_low
    g_wet_org_high = root.l30.g_wet_org_high
    g_wet_org_low_r = root.l30.g_wet_org_low_r
    g_wet_org_low_rp = root.l30.g_wet_org_low_rp
    g_wet_org_high_r = root.l30.g_wet_org_high_r
    g_wet_org_high_rp = root.l30.g_wet_org_high_rp
    g_water = root.l30.g_water
    g_water_org = root.l30.g_water_org
    g_water_min = root.l30.g_water_min
    g_water_min_low = root.l30.g_water_min_low
    g_water_min_high = root.l30.g_water_min_high
    g_water_org_low = root.l30.g_water_org_low
    g_water_org_high = root.l30.g_water_org_high
    g_settlement = root.l30.g_settlement
    g_settlement_org = root.l30.g_settlement_org
    g_settlement_min = root.l30.g_settlement_min
    g_settlement_org_low = root.l30.g_settlement_org_low
    g_settlement_org_high = root.l30.g_settlement_org_high
    g_other = root.l30.g_other
    g_wood = root.l30.g_wood
    pyrolysis = root.l30.pyrolysis

    h30 = root.h30
    e30 = root.e30
    f30 = root.f30
    r30 = root.r30
    b30 = root.b30
    i30 = root.i30
    t30 = root.t30
    a30 = root.a30

    l30_dict = {}
    for i in range(20):
        if l30_dict == root.l30.dict():
            break
        l30_dict = root.l30.dict()
        g_forest_managed.CO2e_pb_per_t = ass("Ass_L_G_forest_conv_CO2e_per_ha_2050")
        g_forest_managed.demand_change = ass("Ass_L_G_forest_conv_pct_change")
        g_forest_managed.area_ha_change = (
            l18.g_forest_managed.area_ha * g_forest_managed.demand_change
        )
        # g_forest.CO2e_cb_per_t = fact("Fact_L_G_forest_CO2e_cb_per_ha_203X")

        g_forest_managed.area_ha = (
            l18.g_forest_managed.area_ha + g_forest_managed.area_ha_change
        )
        g_forest_managed.CO2e_pb = (
            g_forest_managed.CO2e_pb_per_t * g_forest_managed.area_ha
        )
        g_forest_managed.invest_per_x = ass(
            "Ass_L_G_forest_afforestation_invest_per_ha_2020"
        )
        g_crop_min_conv.demand_change = ass("Ass_L_G_crop_organic_matter_pct_2050")
        g_crop_min_conv.CO2e_pb_per_t = fact(
            "Fact_L_G_crop_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_forest_natural.CO2e_pb_per_t = fact("Fact_L_G_forest_nature_CO2e_per_ha_2018")
        g_forest_managed.CO2e_cb_per_t = ass("Ass_L_G_forest_CO2e_cb_per_ha_2050")
        g_forest_managed.CO2e_cb = (
            g_forest_managed.area_ha * g_forest_managed.CO2e_cb_per_t
        )
        g_forest.CO2e_cb = g_forest_managed.CO2e_cb
        g_forest_natural.demand_change = ass("Ass_L_G_forest_nature_pct_change")
        g_forest_natural.area_ha_change = (
            l18.g_forest_natural.area_ha * g_forest_natural.demand_change
        )
        g_crop_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_forest_natural.area_ha = (
            l18.g_forest_natural.area_ha + g_forest_natural.area_ha_change
        )
        g.CO2e_cb = g_forest.CO2e_cb
        g_forest_natural.CO2e_pb = (
            g_forest_natural.CO2e_pb_per_t * g_forest_natural.area_ha
        )
        g_forest.CO2e_pb = g_forest_managed.CO2e_pb + g_forest_natural.CO2e_pb
        g_forest.CO2e_total = g_forest.CO2e_cb + g_forest.CO2e_pb
        g_forest_managed.area_ha_available_pct_of_action = ass(
            "Ass_L_G_forest_conv_dead_pct_2018"
        ) / ass("Ass_L_G_forest_conv_pct_2050")
        g_forest_managed.area_ha_available = (
            g_forest_managed.area_ha * g_forest_managed.area_ha_available_pct_of_action
        )
        g_forest_managed.invest = (
            g_forest_managed.area_ha_available * g_forest_managed.invest_per_x
        )
        g_forest.invest = g_forest_managed.invest
        g_forest.change_CO2e_t = g_forest.CO2e_total - l18.g_forest.CO2e_total
        g_crop_min_conv.area_ha_change = l18.g_crop_min_conv.area_ha * (
            g_crop_min_conv.demand_change
        )
        g_forest.area_ha = g_forest_managed.area_ha + g_forest_natural.area_ha
        g_crop_min_conv.area_ha = (
            l18.g_crop_min_conv.area_ha + g_crop_min_conv.area_ha_change
        )
        g_crop_min_conv.CO2e_pb = (
            g_crop_min_conv.CO2e_pb_per_t * g_crop_min_conv.area_ha
        )
        g_crop_min_hum.CO2e_pb_per_t = fact(
            "Fact_L_G_crop_minrl_soil_sust_CO2e_per_ha_203X"
        )
        g_crop_min_conv.change_within_category = g_crop_min_conv.area_ha_change
        g_crop_min_hum.area_ha_change = -g_crop_min_conv.change_within_category

        g_grass_min_conv.demand_change = ass("Ass_L_G_no_LUC_203X")
        g_grass_min_conv.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_strict_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_crop_min_hum.area_ha = g_crop_min_hum.area_ha_change
        g_crop_min_hum.CO2e_pb = g_crop_min_hum.CO2e_pb_per_t * g_crop_min_hum.area_ha
        g_grass_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_crop_org_low.CO2e_pb_per_t = fact("Fact_L_G_crop_fen_CO2e_per_ha_2018")
        g_crop_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_crop_org_low.area_ha_change = (
            l18.g_crop_org_low.area_ha * g_crop_org_low.demand_change
        )
        g_crop_org_low.area_ha = (
            l18.g_crop_org_low.area_ha + g_crop_org_low.area_ha_change
        )
        g_crop_org_low.CO2e_pb = g_crop_org_low.CO2e_pb_per_t * g_crop_org_low.area_ha
        g_crop_org_high.CO2e_pb_per_t = fact("Fact_L_G_crop_bog_CO2e_per_ha_2018")
        g_crop_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_crop_org_high.area_ha_change = (
            l18.g_crop_org_high.area_ha * g_crop_org_high.demand_change
        )
        g_crop_org_high.area_ha = (
            l18.g_crop_org_high.area_ha + g_crop_org_high.area_ha_change
        )
        g_crop_org_high.CO2e_pb = (
            g_crop_org_high.CO2e_pb_per_t * g_crop_org_high.area_ha
        )
        g_crop.CO2e_pb = (
            g_crop_min_conv.CO2e_pb
            + g_crop_min_hum.CO2e_pb
            + g_crop_org_low.CO2e_pb
            + g_crop_org_high.CO2e_pb
        )
        g_crop_org_low.to_wet_low = g_crop_org_low.area_ha_change

        g_crop.CO2e_total = g_crop.CO2e_pb

        g_crop.change_CO2e_t = g_crop.CO2e_total - l18.g_crop.CO2e_total

        g_grass_min_conv.area_ha_change = l18.g_grass_min_conv.area_ha * (
            g_grass_min_conv.demand_change
        )
        g_crop_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_crop_org_low.invest = (
            -g_crop_org_low.area_ha_change * g_crop_org_low.invest_per_x
        )
        g_crop.area_ha = (
            g_crop_min_conv.area_ha
            + g_crop_min_hum.area_ha
            + g_crop_org_low.area_ha
            + g_crop_org_high.area_ha
        )
        g_crop.area_ha_change = g_crop.area_ha - l18.g_crop.area_ha

        g_crop_org_high.to_wet_high = g_crop_org_high.area_ha_change

        g_crop.demand_change = g_crop.area_ha_change / l18.g_crop.area_ha

        g_grass_min_conv.area_ha = (
            l18.g_grass_min_conv.area_ha + g_grass_min_conv.area_ha_change
        )
        g_grass_min_conv.CO2e_pb = (
            g_grass_min_conv.CO2e_pb_per_t * g_grass_min_conv.area_ha
        )
        g_crop_org_high.invest = (
            -g_crop_org_high.area_ha_change * g_crop_org_high.invest_per_x
        )
        g_crop_org.invest = g_crop_org_low.invest + g_crop_org_high.invest
        g_crop.invest = g_crop_org.invest
        g_grass_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_strict_org_soil_fen_CO2e_per_ha_2018"
        )
        g_grass_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_grove_min.demand_change = ass("Ass_L_G_no_LUC_203X")

        g_grove_min.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_woody_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_grass_org_low.area_ha_change = l18.g_grass_org_low.area_ha * (
            g_grass_org_low.demand_change
        )
        g_grass_org_low.area_ha = (
            l18.g_grass_org_low.area_ha + g_grass_org_low.area_ha_change
        )
        g_grove_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_grass_org_low.CO2e_pb = (
            g_grass_org_low.CO2e_pb_per_t * g_grass_org_low.area_ha
        )
        g_grass_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_strict_org_soil_bog_CO2e_per_ha_2018"
        )
        g_grass_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")
        g_grass_org_high.area_ha_change = l18.g_grass_org_high.area_ha * (
            g_grass_org_high.demand_change
        )
        g_grass_org_high.area_ha = (
            l18.g_grass_org_high.area_ha + g_grass_org_high.area_ha_change
        )
        g_grass_org_high.CO2e_pb = (
            g_grass_org_high.CO2e_pb_per_t * g_grass_org_high.area_ha
        )
        g_grass.CO2e_pb = (
            g_grass_min_conv.CO2e_pb
            + g_grass_org_low.CO2e_pb
            + g_grass_org_high.CO2e_pb
        )
        g_grass_org_low.to_wet_low = g_grass_org_low.area_ha_change

        g_grass.CO2e_total = g_grass.CO2e_pb

        g_grass.change_CO2e_t = g_grass.CO2e_total - l18.g_grass.CO2e_total

        g_grove_min.area_ha_change = l18.g_grove_min.area_ha * (
            g_grove_min.demand_change
        )
        g_grass_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_grass_org_low.invest = (
            -g_grass_org_low.area_ha_change * g_grass_org_low.invest_per_x
        )
        g_grass.area_ha = (
            g_grass_min_conv.area_ha
            + g_grass_org_low.area_ha
            + g_grass_org_high.area_ha
        )
        g_grass.area_ha_change = g_grass.area_ha - l18.g_grass.area_ha

        g_grass_org_high.to_wet_high = g_grass_org_high.area_ha_change

        g_grass.demand_change = g_grass.area_ha_change / l18.g_grass.area_ha

        g_grove_min.area_ha = l18.g_grove_min.area_ha + g_grove_min.area_ha_change
        g_grove_min.CO2e_pb = g_grove_min.CO2e_pb_per_t * g_grove_min.area_ha

        g_grass_org_high.invest = (
            -g_grass_org_high.area_ha_change * g_grass_org_high.invest_per_x
        )
        g_grass.invest = g_grass_org_low.invest + g_grass_org_high.invest

        g_wet_min.demand_change = ass("Ass_L_G_no_LUC_203X")

        g_wet_min.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_grove_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_woody_org_soil_bog_CO2e_per_ha_2018"
        )
        g_grove_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_wet_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_grove_org_high.area_ha_change = l18.g_grove_org_high.area_ha * (
            g_grove_org_high.demand_change
        )
        g_grove_org_high.area_ha = (
            l18.g_grove_org_high.area_ha + g_grove_org_high.area_ha_change
        )
        g_grove_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_grove_org_high.CO2e_pb = (
            g_grove_org_high.CO2e_pb_per_t * g_grove_org_high.area_ha
        )
        g_grove_org_low.area_ha_change = l18.g_grove_org_low.area_ha * (
            g_grove_org_low.demand_change
        )
        g_grove_org_low.area_ha = (
            l18.g_grove_org_low.area_ha + g_grove_org_low.area_ha_change
        )
        g_grove_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_woody_org_soil_fen_CO2e_per_ha_2018"
        )
        g_grove_org_low.to_wet_low = g_grove_org_low.area_ha_change

        g_grove_org_low.CO2e_pb = (
            g_grove_org_low.CO2e_pb_per_t * g_grove_org_low.area_ha
        )
        g_grove.CO2e_pb = (
            g_grove_min.CO2e_pb + g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
        )
        g_grove.CO2e_total = g_grove.CO2e_pb

        g_grove_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_grove_org_low.invest = (
            -g_grove_org_low.area_ha_change * g_grove_org_low.invest_per_x
        )
        g_grove.change_CO2e_t = g_grove.CO2e_total - l18.g_grove.CO2e_total

        g_wet_min.area_ha_change = l18.g_wet_min.area_ha * (g_wet_min.demand_change)
        g_grove_org_high.to_wet_high = g_grove_org_high.area_ha_change

        g_grove.area_ha = (
            g_grove_min.area_ha + g_grove_org_low.area_ha + g_grove_org_high.area_ha
        )
        g_wet_min.area_ha = l18.g_wet_min.area_ha + g_wet_min.area_ha_change

        g_wet_min.CO2e_pb = g_wet_min.CO2e_pb_per_t * g_wet_min.area_ha

        g_grove_org_high.invest = (
            -g_grove_org_high.area_ha_change * g_grove_org_high.invest_per_x
        )
        g_grove.invest = g_grove_org_low.invest + g_grove_org_high.invest
        g_water_min.demand_change = ass("Ass_L_G_no_LUC_203X")
        g_water_min.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_wet_org_low_r.CO2e_pb_per_t = fact("Fact_L_G_fen_wet_CO2e_per_ha_203X")
        g_wet_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_wet_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")

        g_wet_org_low.area_ha_change = l18.g_wet_org_low.area_ha * (
            g_wet_org_low.demand_change
        )
        g_wet_org_low.to_wet_low = g_wet_org_low.area_ha_change
        g_wet_org_low_r.area_ha_change = -(
            g_crop_org_low.to_wet_low
            + g_grass_org_low.to_wet_low
            + g_grove_org_low.to_wet_low
            + g_wet_org_low.to_wet_low
        )
        g_wet_org_low_r.area_ha = g_wet_org_low_r.area_ha_change

        g_wet_org_low_r.CO2e_pb = (
            g_wet_org_low_r.CO2e_pb_per_t * g_wet_org_low_r.area_ha
        )
        g_wet_org_high_r.CO2e_pb_per_t = fact("Fact_L_G_bog_wet_CO2e_per_ha_203X")
        g_wet_org_high.area_ha_change = l18.g_wet_org_high.area_ha * (
            g_wet_org_high.demand_change
        )
        g_wet_org_high.to_wet_high = g_wet_org_high.area_ha_change

        g_wet_org_low.area_ha = l18.g_wet_org_low.area_ha + g_wet_org_low.area_ha_change
        g_wet_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_org_soil_fen_CO2e_per_ha_2018"
        )
        g_wet_org_low.CO2e_pb = g_wet_org_low.CO2e_pb_per_t * g_wet_org_low.area_ha
        g_wet_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
        g_wet_org_low.invest = (
            -g_wet_org_low.area_ha_change * g_wet_org_low.invest_per_x
        )
        g_wet_org_high_r.area_ha_change = -(
            g_crop_org_high.to_wet_high
            + g_grass_org_high.to_wet_high
            + g_grove_org_high.to_wet_high
            + g_wet_org_high.to_wet_high
        )
        g_wet_org_high.invest = (
            -g_wet_org_high.area_ha_change * g_wet_org_high.invest_per_x
        )
        g_wet_org_high_r.area_ha = g_wet_org_high_r.area_ha_change

        g_wet_org_high.area_ha = (
            l18.g_wet_org_high.area_ha + g_wet_org_high.area_ha_change
        )
        g_wet_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_org_soil_bog_CO2e_per_ha_2018"
        )
        g_wet_org_high.CO2e_pb = g_wet_org_high.CO2e_pb_per_t * g_wet_org_high.area_ha
        g_wet_org_low_rp.invest_per_x = ass("Ass_L_G_wet_paludi_invest_per_ha_2016")
        g_wet_org_low_rp.invest = -0 * g_wet_org_low_rp.invest_per_x

        g_wet_org_high_r.CO2e_pb = (
            g_wet_org_high_r.CO2e_pb_per_t * g_wet_org_high_r.area_ha
        )
        g_wet_org.CO2e_pb = g_wet_org_low.CO2e_pb + g_wet_org_high.CO2e_pb
        g_wet_org_r.CO2e_pb = g_wet_org_low_r.CO2e_pb + g_wet_org_high_r.CO2e_pb
        g_wet_org_low_rp.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_org_soil_paludi_CO2e_per_ha_203X"
        )
        g_wet_org_high_rp.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_org_soil_paludi_CO2e_per_ha_203X"
        )
        g_wet_org_high_rp.pct_x = ass("Ass_L_G_wet_paludi_pct_2012")
        g_wet_org_high_rp.area_ha = g_wet_org_high_r.area_ha * g_wet_org_high_rp.pct_x
        g_wet_org_high_rp.CO2e_pb = (
            g_wet_org_high_rp.CO2e_pb_per_t * g_wet_org_high_rp.area_ha
        )
        g_wet_org_low_rp.pct_x = ass("Ass_L_G_wet_paludi_pct_2012")
        g_wet_org_low_rp.area_ha = g_wet_org_low_r.area_ha * g_wet_org_low_rp.pct_x
        g_wet_org_low_rp.CO2e_pb = (
            g_wet_org_low_rp.CO2e_pb_per_t * g_wet_org_low_rp.area_ha
        )
        g_wet_org_rp.CO2e_pb = g_wet_org_low_rp.CO2e_pb + g_wet_org_high_rp.CO2e_pb
        g_wet.CO2e_pb = (
            g_wet_min.CO2e_pb
            + g_wet_org.CO2e_pb
            + g_wet_org_r.CO2e_pb
            + g_wet_org_rp.CO2e_pb
        )
        g_wet.CO2e_total = g_wet.CO2e_pb

        g_wet.change_CO2e_t = g_wet.CO2e_total - l18.g_wet.CO2e_total

        g_wet_org_low_rp.CO2e_pb = (
            g_wet_org_low_rp.CO2e_pb_per_t * g_wet_org_low_rp.area_ha
        )
        g_wet_org_high_rp.invest_per_x = ass("Ass_L_G_wet_paludi_invest_per_ha_2016")
        g_wet_org_high_rp.invest = -0 * g_wet_org_high_rp.invest_per_x

        g_water_min.area_ha_change = l18.g_water_min.area_ha * (
            g_water_min.demand_change
        )
        g_wet_org.area_ha = g_wet_org_low.area_ha + g_wet_org_high.area_ha
        g_wet_org_r.area_ha = g_wet_org_low_r.area_ha + g_wet_org_high_r.area_ha
        g_wet.area_ha = g_wet_min.area_ha + g_wet_org.area_ha + g_wet_org_r.area_ha
        g_water_min.area_ha = l18.g_water_min.area_ha + g_water_min.area_ha_change
        g_water_min.CO2e_pb = g_water_min.CO2e_pb_per_t * g_water_min.area_ha

        g_wet_org.invest = g_wet_org_low.invest + g_wet_org_high.invest
        g_wet_org_rp.invest = g_wet_org_low_rp.invest + g_wet_org_high_rp.invest
        g_wet.invest = g_wet_org.invest + g_wet_org_rp.invest
        g_grove_org.invest = g_grove_org_low.invest + g_grove_org_high.invest
        g_water.invest = g_water_org.invest
        g_settlement.invest = 0
        g.invest = (
            g_forest.invest
            + g_crop.invest
            + g_grass.invest
            + g_grove.invest
            + g_wet.invest
            + g_water.invest
            + g_settlement.invest
        )
        g_settlement_min.demand_change = ass("Ass_L_G_no_LUC_203X")

        g_settlement_min.CO2e_pb_per_t = fact(
            "Fact_L_G_settl_minrl_soil_no_LUC_CO2e_per_ha_203X"
        )
        g_water_min_low.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_org_soil_fen_CO2e_per_ha_2018"
        )
        g_water_min_low.demand_change = ass("Ass_L_G_no_LUC_203X")

        g_water_min_low.CO2e_pb = (
            g_water_min_low.CO2e_pb_per_t * g_water_min_low.area_ha
        )
        g_water_min_high.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_org_soil_bog_CO2e_per_ha_2018"
        )
        g_water_min_high.demand_change = ass("Ass_L_G_no_LUC_203X")

        g_water_min_high.CO2e_pb = (
            g_water_min_high.CO2e_pb_per_t * g_water_min_high.area_ha
        )
        g_water.CO2e_pb = g_water_min.CO2e_pb + g_water_org.CO2e_pb
        g_water.CO2e_total = g_water.CO2e_pb

        g_water.change_CO2e_t = g_water.CO2e_total - l18.g_water.CO2e_total

        g_settlement_min.area_ha_change = l18.g_settlement_min.area_ha * (
            g_settlement_min.demand_change
        )
        g_water.area_ha = g_water_min.area_ha + g_water_org.area_ha
        g_settlement_min.area_ha = (
            l18.g_settlement_min.area_ha + g_settlement_min.area_ha_change
        )
        g_settlement_min.CO2e_pb = (
            g_settlement_min.CO2e_pb_per_t * g_settlement_min.area_ha
        )
        g_other.demand_change = ass("Ass_L_G_no_LUC_203X")
        g_other.CO2e_pb_per_t = fact("Fact_L_G_other_minrl_soil_CO2e_per_ha_2018")
        g_settlement_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_settl_org_soil_fen_CO2e_per_ha_2018"
        )
        g_settlement_org_low.demand_change = ass("Ass_L_G_settl_rewetting_2050")
        g_settlement_org_low.area_ha_change = l18.g_settlement_org_low.area_ha * (
            g_settlement_org_low.demand_change
        )
        g_settlement_org_low.area_ha = (
            l18.g_settlement_org_low.area_ha + g_settlement_org_low.area_ha_change
        )
        g_settlement_org_low.CO2e_pb = (
            g_settlement_org_low.CO2e_pb_per_t * g_settlement_org_low.area_ha
        )
        g_settlement_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_settl_org_soil_bog_CO2e_per_ha_2018"
        )
        g_settlement_org_high.demand_change = ass("Ass_L_G_settl_rewetting_2050")
        g_settlement_org_high.area_ha_change = l18.g_settlement_org_high.area_ha * (
            g_settlement_org_high.demand_change
        )
        g_settlement_org_high.area_ha = (
            l18.g_settlement_org_high.area_ha + g_settlement_org_high.area_ha_change
        )
        g_settlement_org_high.CO2e_pb = (
            g_settlement_org_high.CO2e_pb_per_t * g_settlement_org_high.area_ha
        )
        g_settlement.CO2e_pb = (
            g_settlement_min.CO2e_pb
            + g_settlement_org_low.CO2e_pb
            + g_settlement_org_high.CO2e_pb
        )
        g_settlement.CO2e_total = g_settlement.CO2e_pb

        g_settlement.change_CO2e_t = (
            g_settlement.CO2e_total - l18.g_settlement.CO2e_total
        )
        g_other.area_ha = (1 + g_other.demand_change) * l18.g_other.area_ha

        g_settlement.area_ha = (
            g_settlement_min.area_ha
            + g_settlement_org_low.area_ha
            + g_settlement_org_high.area_ha
        )
        g_other.CO2e_pb = g_other.CO2e_pb_per_t * g_other.area_ha

        g_wood.CO2e_pb_per_t = fact("Fact_L_G_wood_CO2e_per_ha_2018")

        g_wood.area_ha = g_forest_managed.area_ha

        g_other.area_ha_change = l18.g_other.area_ha * (g_other.demand_change)
        g.area_ha = (
            g_forest.area_ha
            + g_crop.area_ha
            + g_grass.area_ha
            + g_grove.area_ha
            + g_wet.area_ha
            + g_water.area_ha
            + g_settlement.area_ha
            + g_other.area_ha
        )
        g_wood.CO2e_pb = g_wood.CO2e_pb_per_t * g_wood.area_ha

        g.CO2e_pb = (
            g_forest.CO2e_pb
            + g_crop.CO2e_pb
            + g_grass.CO2e_pb
            + g_grove.CO2e_pb
            + g_wet.CO2e_pb
            + g_water.CO2e_pb
            + g_settlement.CO2e_pb
            + g_other.CO2e_pb
            + g_wood.CO2e_pb
        )
        g_other.CO2e_total = g_other.CO2e_pb

        g_other.change_CO2e_t = g_other.CO2e_total - l18.g_other.CO2e_total

        g.CO2e_total = g.CO2e_pb + g.CO2e_cb

        pyrolysis.CO2e_total = 0  # Todo: not defined in Excel

        l.CO2e_total = g.CO2e_total + pyrolysis.CO2e_total

        g.change_CO2e_t = g.CO2e_total - l18.g.CO2e_total

        g_wood.CO2e_total = g_wood.CO2e_pb

        g_wood.change_CO2e_t = g_wood.CO2e_total - l18.g_wood.CO2e_total

        pyrolysis.CO2e_pb = pyrolysis.CO2e_total
        pyrolysis.CO2e_pb_per_t = fact("Fact_L_P_biochar_ratio_CO2e_pb_to_prodvol")
        pyrolysis.prod_volume = pyrolysis.CO2e_pb / pyrolysis.CO2e_pb_per_t

        pyrolysis.CO2e_total = min(
            -h30.h.CO2e_total
            + e30.e.CO2e_total
            + f30.f.CO2e_total
            + r30.r.CO2e_total
            + b30.b.CO2e_total
            + i30.i.CO2e_total
            + t30.t.CO2e_total
            + a30.a.CO2e_total
            + g.CO2e_total,
            0,
        )
        pyrolysis.change_CO2e_t = pyrolysis.CO2e_total - l18.pyrolysis.CO2e_total
        # div 0 pyrolysis.change_CO2e_pct = (pyrolysis.change_CO2e_t / AV395)
        pyrolysis.CO2e_total_2021_estimated = l18.pyrolysis.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        pyrolysis.cost_climate_saved = (
            (pyrolysis.CO2e_total_2021_estimated - pyrolysis.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        pyrolysis.invest_pa = pyrolysis.invest / entry("In_M_duration_target")
        pyrolysis.invest = pyrolysis.prod_volume * pyrolysis.invest_per_x
        pyrolysis.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        pyrolysis.cost_wage = pyrolysis.invest_pa * pyrolysis.pct_of_wage
        pyrolysis.ratio_wage_to_emplo = fact(
            "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
        )
        pyrolysis.demand_emplo = pyrolysis.cost_wage / pyrolysis.ratio_wage_to_emplo
        pyrolysis.demand_emplo_new = pyrolysis.demand_emplo
        pyrolysis.invest_per_x = ass(
            "Ass_L_P_pyrolysis_plant_ratio_invest_to_biochar_pa"
        )

        l.CO2e_pb = g.CO2e_pb + pyrolysis.CO2e_pb
        l.CO2e_cb = g.CO2e_cb
        l.change_CO2e_t = l.CO2e_total - l18.l.CO2e_total
        l.change_CO2e_pct = l.change_CO2e_t / l18.l.CO2e_total
        l.CO2e_total_2021_estimated = l18.l.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        l.cost_climate_saved = (
            (l.CO2e_total_2021_estimated - l.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        l.invest_pa = g.invest_pa + pyrolysis.invest_pa
        l.invest = g.invest + pyrolysis.invest
        l.demand_emplo = g.demand_emplo + pyrolysis.demand_emplo
        l.demand_emplo_new = g.demand_emplo_new + pyrolysis.demand_emplo_new
        g.change_CO2e_pct = g.change_CO2e_t / l18.g.CO2e_total
        g.CO2e_total_2021_estimated = l18.g.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g.cost_climate_saved = (
            (g.CO2e_total_2021_estimated - g.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g.invest_pa = (
            g_forest.invest_pa
            + g_crop.invest_pa
            + g_grass.invest_pa
            + g_grove.invest_pa
            + g_wet.invest_pa
            + g_water.invest_pa
            + g_settlement.invest_pa
        )
        g.cost_wage = (
            g_forest.cost_wage
            + g_crop.cost_wage
            + g_grass.cost_wage
            + g_grove.cost_wage
            + g_wet.cost_wage
        )
        g.demand_emplo = (
            g_forest.demand_emplo
            + g_crop.demand_emplo
            + g_grass.demand_emplo
            + g_grove.demand_emplo
            + g_wet.demand_emplo
        )
        g.demand_emplo_new = (
            g_forest.demand_emplo_new
            + g_crop.demand_emplo_new
            + g_grass.demand_emplo_new
            + g_grove.demand_emplo_new
            + g_wet.demand_emplo_new
        )
        g_forest.area_ha_change = g_forest.area_ha - l18.g_forest.area_ha
        g_forest.change_CO2e_pct = g_forest.change_CO2e_t / l18.g_forest.CO2e_total
        g_forest.CO2e_total_2021_estimated = l18.g_forest.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_forest.cost_climate_saved = (
            (g_forest.CO2e_total_2021_estimated - g_forest.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_forest.invest_pa = g_forest_managed.invest_pa
        g_forest.cost_wage = g_forest_managed.cost_wage
        g_forest.demand_emplo = g_forest_managed.demand_emplo
        g_forest.demand_emplo_new = g_forest_managed.demand_emplo_new
        g_forest_managed.CO2e_total = (
            g_forest_managed.CO2e_pb + g_forest_managed.CO2e_cb
        )
        g_forest_managed.change_CO2e_t = (
            g_forest_managed.CO2e_total - l18.g_forest_managed.CO2e_total
        )
        g_forest_managed.change_CO2e_pct = (
            g_forest_managed.change_CO2e_t / l18.g_forest_managed.CO2e_total
        )
        g_forest_managed.CO2e_total_2021_estimated = (
            l18.g_forest_managed.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_forest_managed.cost_climate_saved = (
            (g_forest_managed.CO2e_total_2021_estimated - g_forest_managed.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_forest_managed.invest_pa = g_forest_managed.invest / entry(
            "In_M_duration_target"
        )
        g_forest_managed.pct_of_wage = fact(
            "Fact_L_G_forest_afforestation_revenue_pct_of_wage_2018"
        )
        g_forest_managed.cost_wage = (
            g_forest_managed.invest_pa * g_forest_managed.pct_of_wage
        )
        g_forest_managed.ratio_wage_to_emplo = fact(
            "Fact_L_G_forest_afforestation_ratio_wage_to_emplo_2018"
        )
        g_forest_managed.demand_emplo = (
            g_forest_managed.cost_wage / g_forest_managed.ratio_wage_to_emplo
        )
        g_forest_managed.demand_emplo_new = g_forest_managed.demand_emplo
        g_forest_natural.CO2e_total = g_forest_natural.CO2e_pb
        g_forest_natural.change_CO2e_t = (
            g_forest_natural.CO2e_total - l18.g_forest_natural.CO2e_total
        )
        g_forest_natural.change_CO2e_pct = (
            g_forest_natural.change_CO2e_t / l18.g_forest_natural.CO2e_total
        )
        g_forest_natural.CO2e_total_2021_estimated = (
            l18.g_forest_natural.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_forest_natural.cost_climate_saved = (
            (g_forest_natural.CO2e_total_2021_estimated - g_forest_natural.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop.change_CO2e_pct = g_crop.change_CO2e_t / l18.g_crop.CO2e_total
        g_crop.CO2e_total_2021_estimated = l18.g_crop.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_crop.cost_climate_saved = (
            (g_crop.CO2e_total_2021_estimated - g_crop.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop.invest_pa = g_crop_org.invest_pa
        g_crop.cost_wage = g_crop_org.cost_wage
        g_crop.demand_emplo = g_crop_org.demand_emplo
        g_crop.demand_emplo_new = g_crop_org.demand_emplo_new
        g_crop_min_conv.CO2e_total = g_crop_min_conv.CO2e_pb
        g_crop_min_conv.change_CO2e_t = (
            g_crop_min_conv.CO2e_total - l18.g_crop_min_conv.CO2e_total
        )
        g_crop_min_conv.change_CO2e_pct = (
            g_crop_min_conv.change_CO2e_t / l18.g_crop_min_conv.CO2e_total
        )
        g_crop_min_conv.CO2e_total_2021_estimated = (
            l18.g_crop_min_conv.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_crop_min_conv.cost_climate_saved = (
            (g_crop_min_conv.CO2e_total_2021_estimated - g_crop_min_conv.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop_min_hum.CO2e_total = g_crop_min_hum.CO2e_pb
        g_crop_min_hum.change_CO2e_t = g_crop_min_hum.CO2e_total
        g_crop_min_hum.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_crop_min_hum.cost_climate_saved = (
            (g_crop_min_hum.CO2e_total_2021_estimated - g_crop_min_hum.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop_org.area_ha_change = (
            g_crop_org_low.area_ha_change + g_crop_org_high.area_ha_change
        )
        g_crop_org.area_ha = g_crop_org_low.area_ha + g_crop_org_high.area_ha
        g_crop_org.CO2e_pb = g_crop_org_low.CO2e_pb + g_crop_org_high.CO2e_pb
        g_crop_org.CO2e_total = g_crop_org.CO2e_pb
        g_crop_org.change_CO2e_t = g_crop_org.CO2e_total - l18.g_crop_org.CO2e_total
        g_crop_org.change_CO2e_pct = (
            g_crop_org.change_CO2e_t / l18.g_crop_org.CO2e_total
        )
        g_crop_org.CO2e_total_2021_estimated = l18.g_crop_org.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_crop_org.cost_climate_saved = (
            (g_crop_org.CO2e_total_2021_estimated - g_crop_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop_org.invest_pa = g_crop_org.invest / entry("In_M_duration_target")
        g_crop_org.cost_wage = g_crop_org_low.cost_wage + g_crop_org_high.cost_wage
        g_crop_org.demand_emplo = (
            g_crop_org_low.demand_emplo + g_crop_org_high.demand_emplo
        )
        g_crop_org.demand_emplo_new = (
            g_crop_org_low.demand_emplo_new + g_crop_org_high.demand_emplo_new
        )
        g_crop_org_low.change_wet_org_low = g_crop_org_low.area_ha_change
        g_crop_org_low.CO2e_total = g_crop_org_low.CO2e_pb
        g_crop_org_low.change_CO2e_t = (
            g_crop_org_low.CO2e_total - l18.g_crop_org_low.CO2e_total
        )
        g_crop_org_low.change_CO2e_pct = (
            g_crop_org_low.change_CO2e_t / l18.g_crop_org_low.CO2e_total
        )
        g_crop_org_low.CO2e_total_2021_estimated = l18.g_crop_org_low.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_crop_org_low.cost_climate_saved = (
            (g_crop_org_low.CO2e_total_2021_estimated - g_crop_org_low.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop_org_low.invest_pa = g_crop_org_low.invest / entry("In_M_duration_target")
        g_crop_org_low.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_crop_org_low.cost_wage = g_crop_org_low.invest_pa * g_crop_org_low.pct_of_wage
        g_crop_org_low.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_crop_org_low.demand_emplo = (
            g_crop_org_low.cost_wage / g_crop_org_low.ratio_wage_to_emplo
        )
        g_crop_org_low.demand_emplo_new = g_crop_org_low.demand_emplo
        g_crop_org_high.change_wet_org_high = g_crop_org_high.area_ha_change
        g_crop_org_high.CO2e_total = g_crop_org_high.CO2e_pb
        g_crop_org_high.change_CO2e_t = (
            g_crop_org_high.CO2e_total - l18.g_crop_org_high.CO2e_total
        )
        g_crop_org_high.change_CO2e_pct = (
            g_crop_org_high.change_CO2e_t / l18.g_crop_org_high.CO2e_total
        )
        g_crop_org_high.CO2e_total_2021_estimated = (
            l18.g_crop_org_high.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_crop_org_high.cost_climate_saved = (
            (g_crop_org_high.CO2e_total_2021_estimated - g_crop_org_high.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_crop_org_high.invest_pa = g_crop_org_high.invest / entry(
            "In_M_duration_target"
        )
        g_crop_org_high.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_crop_org_high.cost_wage = (
            g_crop_org_high.invest_pa * g_crop_org_high.pct_of_wage
        )
        g_crop_org_high.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_crop_org_high.demand_emplo = (
            g_crop_org_high.cost_wage / g_crop_org_high.ratio_wage_to_emplo
        )
        g_crop_org_high.demand_emplo_new = g_crop_org_high.demand_emplo
        g_grass.change_CO2e_pct = g_grass.change_CO2e_t / l18.g_grass.CO2e_total
        g_grass.CO2e_total_2021_estimated = l18.g_grass.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_grass.cost_climate_saved = (
            (g_grass.CO2e_total_2021_estimated - g_grass.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grass.invest_pa = g_grass_org.invest_pa
        g_grass.cost_wage = g_grass_org.cost_wage
        g_grass.demand_emplo = g_grass_org.demand_emplo
        g_grass.demand_emplo_new = g_grass_org.demand_emplo_new
        g_grass_min_conv.CO2e_total = g_grass_min_conv.CO2e_pb
        g_grass_min_conv.change_CO2e_t = (
            g_grass_min_conv.CO2e_total - l18.g_grass_min_conv.CO2e_total
        )
        g_grass_min_conv.change_CO2e_pct = (
            g_grass_min_conv.change_CO2e_t / l18.g_grass_min_conv.CO2e_total
        )
        g_grass_min_conv.CO2e_total_2021_estimated = (
            l18.g_grass_min_conv.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_grass_min_conv.cost_climate_saved = (
            (g_grass_min_conv.CO2e_total_2021_estimated - g_grass_min_conv.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grass_org.area_ha_change = (
            g_grass_org_low.area_ha_change + g_grass_org_high.area_ha_change
        )
        g_grass_org.area_ha = g_grass_org_low.area_ha + g_grass_org_high.area_ha
        g_grass_org.CO2e_pb = g_grass_org_low.CO2e_pb + g_grass_org_high.CO2e_pb
        g_grass_org.CO2e_total = g_grass_org.CO2e_pb
        g_grass_org.change_CO2e_t = g_grass_org.CO2e_total - l18.g_grass_org.CO2e_total
        g_grass_org.change_CO2e_pct = (
            g_grass_org.change_CO2e_t / l18.g_grass_org.CO2e_total
        )
        g_grass_org.CO2e_total_2021_estimated = l18.g_grass_org.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_grass_org.cost_climate_saved = (
            (g_grass_org.CO2e_total_2021_estimated - g_grass_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grass_org.invest_pa = g_grass_org.invest / entry("In_M_duration_target")
        g_grass_org.invest = g_grass_org_low.invest + g_grass_org_high.invest
        g_grass_org.cost_wage = g_grass_org_low.cost_wage + g_grass_org_high.cost_wage
        g_grass_org.demand_emplo = (
            g_grass_org_low.demand_emplo + g_grass_org_high.demand_emplo
        )
        g_grass_org.demand_emplo_new = (
            g_grass_org_low.demand_emplo_new + g_grass_org_high.demand_emplo_new
        )
        g_grass_org_low.change_wet_org_low = g_grass_org_low.area_ha_change
        g_grass_org_low.CO2e_total = g_grass_org_low.CO2e_pb
        g_grass_org_low.change_CO2e_t = (
            g_grass_org_low.CO2e_total - l18.g_grass_org_low.CO2e_total
        )
        g_grass_org_low.change_CO2e_pct = (
            g_grass_org_low.change_CO2e_t / l18.g_grass_org_low.CO2e_total
        )
        g_grass_org_low.CO2e_total_2021_estimated = (
            l18.g_grass_org_low.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_grass_org_low.cost_climate_saved = (
            (g_grass_org_low.CO2e_total_2021_estimated - g_grass_org_low.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grass_org_low.invest_pa = g_grass_org_low.invest / entry(
            "In_M_duration_target"
        )
        g_grass_org_low.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_grass_org_low.cost_wage = (
            g_grass_org_low.invest_pa * g_grass_org_low.pct_of_wage
        )
        g_grass_org_low.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_grass_org_low.demand_emplo = (
            g_grass_org_low.cost_wage / g_grass_org_low.ratio_wage_to_emplo
        )
        g_grass_org_low.demand_emplo_new = g_grass_org_low.demand_emplo
        g_grass_org_high.change_wet_org_high = g_grass_org_high.area_ha_change
        g_grass_org_high.CO2e_total = g_grass_org_high.CO2e_pb
        g_grass_org_high.change_CO2e_t = (
            g_grass_org_high.CO2e_total - l18.g_grass_org_high.CO2e_total
        )
        g_grass_org_high.change_CO2e_pct = (
            g_grass_org_high.change_CO2e_t / l18.g_grass_org_high.CO2e_total
        )
        g_grass_org_high.CO2e_total_2021_estimated = (
            l18.g_grass_org_high.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_grass_org_high.cost_climate_saved = (
            (g_grass_org_high.CO2e_total_2021_estimated - g_grass_org_high.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grass_org_high.invest_pa = g_grass_org_high.invest / entry(
            "In_M_duration_target"
        )
        g_grass_org_high.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_grass_org_high.cost_wage = (
            g_grass_org_high.invest_pa * g_grass_org_high.pct_of_wage
        )
        g_grass_org_high.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_grass_org_high.demand_emplo = (
            g_grass_org_high.cost_wage / g_grass_org_high.ratio_wage_to_emplo
        )
        g_grass_org_high.demand_emplo_new = g_grass_org_high.demand_emplo
        g_grove.demand_change = g_grove.area_ha_change / l18.g_grove.area_ha
        g_grove.area_ha_change = g_grove.area_ha - l18.g_grove.area_ha
        g_grove.change_CO2e_pct = g_grove.change_CO2e_t / l18.g_grove.CO2e_total
        g_grove.CO2e_total_2021_estimated = l18.g_grove.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_grove.cost_climate_saved = (
            (g_grove.CO2e_total_2021_estimated - g_grove.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grove.invest_pa = g_grove_org.invest_pa
        g_grove.cost_wage = g_grove_org.cost_wage
        g_grove.demand_emplo = g_grove_org.demand_emplo
        g_grove.demand_emplo_new = g_grove_org.demand_emplo_new
        g_grove_min.CO2e_total = g_grove_min.CO2e_pb
        g_grove_min.change_CO2e_t = g_grove_min.CO2e_total - l18.g_grove_min.CO2e_total
        g_grove_min.change_CO2e_pct = (
            g_grove_min.change_CO2e_t / l18.g_grove_min.CO2e_total
        )
        g_grove_min.CO2e_total_2021_estimated = l18.g_grove_min.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_grove_min.cost_climate_saved = (
            (g_grove_min.CO2e_total_2021_estimated - g_grove_min.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grove_org.area_ha_change = (
            g_grove_org_low.area_ha_change + g_grove_org_high.area_ha_change
        )
        g_grove_org.area_ha = g_grove_org_low.area_ha + g_grove_org_high.area_ha
        g_grove_org.cost_climate_saved = (
            (g_grove_org.CO2e_total_2021_estimated - g_grove_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grove_org.CO2e_pb = g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
        g_grove_org.CO2e_total = g_grove_org.CO2e_pb
        g_grove_org.change_CO2e_t = g_grove_org.CO2e_total - l18.g_grove_org.CO2e_total
        g_grove_org.change_CO2e_pct = (
            g_grove_org.change_CO2e_t / l18.g_grove_org.CO2e_total
        )
        g_grove_org.CO2e_total_2021_estimated = l18.g_grove_org.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_grove_org.cost_climate_saved = (
            (g_grove_org.CO2e_total_2021_estimated - g_grove_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grove_org.invest_pa = g_grove_org.invest / entry("In_M_duration_target")
        g_grove_org.cost_wage = g_grove_org_low.cost_wage + g_grove_org_high.cost_wage
        g_grove_org.demand_emplo = (
            g_grove_org_low.demand_emplo + g_grove_org_high.demand_emplo
        )
        g_grove_org.demand_emplo_new = (
            g_grove_org_low.demand_emplo_new + g_grove_org_high.demand_emplo_new
        )
        g_grove_org_low.change_wet_org_low = g_grove_org_low.area_ha_change
        g_grove_org_low.CO2e_total = g_grove_org_low.CO2e_pb
        g_grove_org_low.change_CO2e_t = (
            g_grove_org_low.CO2e_total - l18.g_grove_org_low.CO2e_total
        )
        g_grove_org_low.change_CO2e_pct = (
            g_grove_org_low.change_CO2e_t / l18.g_grove_org_low.CO2e_total
        )
        g_grove_org_low.CO2e_total_2021_estimated = (
            l18.g_grove_org_low.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_grove_org_low.cost_climate_saved = (
            (g_grove_org_low.CO2e_total_2021_estimated - g_grove_org_low.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grove_org_low.invest_pa = g_grove_org_low.invest / entry(
            "In_M_duration_target"
        )
        g_grove_org_low.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_grove_org_low.cost_wage = (
            g_grove_org_low.invest_pa * g_grove_org_low.pct_of_wage
        )
        g_grove_org_low.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_grove_org_low.demand_emplo = (
            g_grove_org_low.cost_wage / g_grove_org_low.ratio_wage_to_emplo
        )
        g_grove_org_low.demand_emplo_new = g_grove_org_low.demand_emplo
        g_grove_org_high.change_wet_org_high = g_grove_org_high.area_ha_change
        g_grove_org_high.CO2e_total = g_grove_org_high.CO2e_pb
        g_grove_org_high.change_CO2e_t = (
            g_grove_org_high.CO2e_total - l18.g_grove_org_high.CO2e_total
        )
        g_grove_org_high.change_CO2e_pct = (
            g_grove_org_high.change_CO2e_t / l18.g_grove_org_high.CO2e_total
        )
        g_grove_org_high.CO2e_total_2021_estimated = (
            l18.g_grove_org_high.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_grove_org_high.cost_climate_saved = (
            (g_grove_org_high.CO2e_total_2021_estimated - g_grove_org_high.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_grove_org_high.invest_pa = g_grove_org_high.invest / entry(
            "In_M_duration_target"
        )
        g_grove_org_high.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_grove_org_high.cost_wage = (
            g_grove_org_high.invest_pa * g_grove_org_high.pct_of_wage
        )
        g_grove_org_high.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_grove_org_high.demand_emplo = (
            g_grove_org_high.cost_wage / g_grove_org_high.ratio_wage_to_emplo
        )
        g_grove_org_high.demand_emplo_new = g_grove_org_high.demand_emplo
        g_wet.area_ha_change = g_wet.area_ha - l18.g_wet.area_ha
        g_wet.change_CO2e_pct = g_wet.change_CO2e_t / l18.g_wet.CO2e_total
        g_wet.CO2e_total_2021_estimated = l18.g_wet.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet.cost_climate_saved = (
            (g_wet.CO2e_total_2021_estimated - g_wet.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet.invest_pa = g_wet_org.invest_pa + g_wet_org_rp.invest_pa
        g_wet.cost_wage = g_wet_org.cost_wage
        g_wet.demand_emplo = g_wet_org.demand_emplo
        g_wet.demand_emplo_new = g_wet_org.demand_emplo_new
        g_wet_min.CO2e_total = g_wet_min.CO2e_pb
        g_wet_min.change_CO2e_t = g_wet_min.CO2e_total - l18.g_wet_min.CO2e_total
        g_wet_min.change_CO2e_pct = g_wet_min.change_CO2e_t / l18.g_wet_min.CO2e_total
        g_wet_min.CO2e_total_2021_estimated = l18.g_wet_min.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_min.cost_climate_saved = (
            (g_wet_min.CO2e_total_2021_estimated - g_wet_min.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org.area_ha_change = (
            g_wet_org_low.area_ha_change + g_wet_org_high.area_ha_change
        )
        g_wet_org.CO2e_total = g_wet_org.CO2e_pb
        g_wet_org.change_CO2e_t = g_wet_org.CO2e_total - l18.g_wet_org.CO2e_total
        g_wet_org.change_CO2e_pct = g_wet_org.change_CO2e_t / l18.g_wet_org.CO2e_total
        g_wet_org.CO2e_total_2021_estimated = l18.g_wet_org.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org.cost_climate_saved = (
            (g_wet_org.CO2e_total_2021_estimated - g_wet_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org.invest_pa = g_wet_org.invest / entry("In_M_duration_target")
        g_wet_org.cost_wage = g_wet_org_low.cost_wage + g_wet_org_high.cost_wage
        g_wet_org.demand_emplo = (
            g_wet_org_low.demand_emplo + g_wet_org_high.demand_emplo
        )
        g_wet_org.demand_emplo_new = (
            g_wet_org_low.demand_emplo_new + g_wet_org_high.demand_emplo_new
        )
        g_wet_org_low.change_wet_org_low = g_wet_org_low.area_ha_change
        g_wet_org_low.CO2e_total = g_wet_org_low.CO2e_pb
        g_wet_org_low.change_CO2e_t = (
            g_wet_org_low.CO2e_total - l18.g_wet_org_low.CO2e_total
        )
        g_wet_org_low.change_CO2e_pct = (
            g_wet_org_low.change_CO2e_t / l18.g_wet_org_low.CO2e_total
        )
        g_wet_org_low.CO2e_total_2021_estimated = l18.g_wet_org_low.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_low.cost_climate_saved = (
            (g_wet_org_low.CO2e_total_2021_estimated - g_wet_org_low.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_low.invest_pa = g_wet_org_low.invest / entry("In_M_duration_target")
        g_wet_org_low.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_wet_org_low.cost_wage = g_wet_org_low.invest_pa * g_wet_org_low.pct_of_wage
        g_wet_org_low.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_wet_org_low.demand_emplo = (
            g_wet_org_low.cost_wage / g_wet_org_low.ratio_wage_to_emplo
        )
        g_wet_org_low.demand_emplo_new = g_wet_org_low.demand_emplo
        g_wet_org_high.change_wet_org_high = g_wet_org_high.area_ha_change
        g_wet_org_high.CO2e_total = g_wet_org_high.CO2e_pb
        g_wet_org_high.change_CO2e_t = (
            g_wet_org_high.CO2e_total - l18.g_wet_org_high.CO2e_total
        )
        g_wet_org_high.change_CO2e_pct = (
            g_wet_org_high.change_CO2e_t / l18.g_wet_org_high.CO2e_total
        )
        g_wet_org_high.CO2e_total_2021_estimated = l18.g_wet_org_high.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_high.cost_climate_saved = (
            (g_wet_org_high.CO2e_total_2021_estimated - g_wet_org_high.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_high.invest_pa = g_wet_org_high.invest / entry("In_M_duration_target")
        g_wet_org_high.pct_of_wage = fact(
            "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
        )
        g_wet_org_high.cost_wage = g_wet_org_high.invest_pa * g_wet_org_high.pct_of_wage
        g_wet_org_high.ratio_wage_to_emplo = fact(
            "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
        )
        g_wet_org_high.demand_emplo = (
            g_wet_org_high.cost_wage / g_wet_org_high.ratio_wage_to_emplo
        )
        g_wet_org_high.demand_emplo_new = g_wet_org_high.demand_emplo
        g_wet_org_r.area_ha_change = (
            g_wet_org_low_r.area_ha_change + g_wet_org_high_r.area_ha_change
        )
        g_wet_org_r.CO2e_total = g_wet_org_r.CO2e_pb
        g_wet_org_r.change_CO2e_t = g_wet_org_r.CO2e_total
        g_wet_org_r.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_r.cost_climate_saved = (
            (g_wet_org_r.CO2e_total_2021_estimated - g_wet_org_r.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_low_r.CO2e_total = g_wet_org_low_r.CO2e_pb
        g_wet_org_low_r.change_CO2e_t = g_wet_org_low_r.CO2e_total
        g_wet_org_low_r.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_low_r.cost_climate_saved = (
            (g_wet_org_low_r.CO2e_total_2021_estimated - g_wet_org_low_r.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_high_r.CO2e_total = g_wet_org_high_r.CO2e_pb
        g_wet_org_high_r.change_CO2e_t = g_wet_org_high_r.CO2e_total
        g_wet_org_high_r.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_high_r.cost_climate_saved = (
            (g_wet_org_high_r.CO2e_total_2021_estimated - g_wet_org_high_r.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_rp.area_ha = g_wet_org_low_rp.area_ha + g_wet_org_high_rp.area_ha
        g_wet_org_rp.CO2e_total = g_wet_org_rp.CO2e_pb
        g_wet_org_rp.change_CO2e_t = g_wet_org_rp.CO2e_total
        g_wet_org_rp.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_rp.cost_climate_saved = (
            (g_wet_org_rp.CO2e_total_2021_estimated - g_wet_org_rp.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_rp.invest_pa = g_wet_org_rp.invest / entry("In_M_duration_target")
        g_wet_org_low_rp.CO2e_total = g_wet_org_low_rp.CO2e_pb
        g_wet_org_low_rp.change_CO2e_t = g_wet_org_low_rp.CO2e_total
        g_wet_org_low_rp.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_low_rp.cost_climate_saved = (
            (g_wet_org_low_rp.CO2e_total_2021_estimated - g_wet_org_low_rp.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_low_rp.invest_pa = g_wet_org_low_rp.invest / entry(
            "In_M_duration_target"
        )
        g_wet_org_high_rp.CO2e_total = g_wet_org_high_rp.CO2e_pb
        g_wet_org_high_rp.change_CO2e_t = g_wet_org_high_rp.CO2e_total
        g_wet_org_high_rp.CO2e_total_2021_estimated = 0 * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wet_org_high_rp.cost_climate_saved = (
            (g_wet_org_high_rp.CO2e_total_2021_estimated - g_wet_org_high_rp.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wet_org_high_rp.invest_pa = g_wet_org_high_rp.invest / entry(
            "In_M_duration_target"
        )
        g_water.demand_change = g_water.area_ha_change / l18.g_water.area_ha
        g_water.area_ha_change = g_water.area_ha - l18.g_water.area_ha
        g_water.change_CO2e_pct = g_water.change_CO2e_t / l18.g_water.CO2e_total
        g_water.CO2e_total_2021_estimated = l18.g_water.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_water.cost_climate_saved = (
            (g_water.CO2e_total_2021_estimated - g_water.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_water.invest_pa = g_water_org.invest_pa
        g_water.cost_wage = g_grove_org.cost_wage
        g_water.demand_emplo = g_grove_org.demand_emplo
        g_water.demand_emplo_new = g_grove_org.demand_emplo_new
        g_water_min.CO2e_total = g_water_min.CO2e_pb
        g_water_min.change_CO2e_t = g_water_min.CO2e_total - l18.g_water_min.CO2e_total
        g_water_min.change_CO2e_pct = (
            g_water_min.change_CO2e_t / l18.g_water_min.CO2e_total
        )
        g_water_min.CO2e_total_2021_estimated = l18.g_water_min.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_water_min.cost_climate_saved = (
            (g_water_min.CO2e_total_2021_estimated - g_water_min.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_water_org.CO2e_pb = g_water_org_low.CO2e_pb + g_water_org_high.CO2e_pb
        g_water_org.CO2e_total = g_water_org.CO2e_pb
        g_water_org.CO2e_total_2021_estimated = l18.g_water_org.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_water_org.cost_climate_saved = (
            (g_water_org.CO2e_total_2021_estimated - g_water_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_water_org.invest_pa = g_water_org.invest / entry("In_M_duration_target")
        g_water_org.invest = 0
        g_water_org.cost_wage = 0
        g_water_org.demand_emplo = 0
        g_water_org.demand_emplo_new = 0
        g_water_org.area_ha = g_water_org_low.area_ha + g_water_org_high.area_ha
        g_water_org_low.demand_change = ass("Ass_L_G_no_LUC_203X")
        g_water_org_low.area_ha_change = l18.g_water_org_low.area_ha * (
            g_water_org_low.demand_change
        )
        g_water_org_low.area_ha = (
            l18.g_water_org_low.area_ha + g_water_org_low.area_ha_change
        )
        g_water_org_low.CO2e_pb = (
            g_water_org_low.CO2e_pb_per_t * g_water_org_low.area_ha
        )
        g_water_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_org_soil_fen_CO2e_per_ha_2018"
        )
        g_water_org_low.CO2e_total = g_water_org_low.CO2e_pb
        g_water_org_low.change_CO2e_t = (
            g_water_org_low.CO2e_total - l18.g_water_org_low.CO2e_total
        )
        g_water_org_low.change_CO2e_pct = (
            g_water_org_low.change_CO2e_t / l18.g_water_org_low.CO2e_total
        )
        g_water_org_low.CO2e_total_2021_estimated = (
            l18.g_water_org_low.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_water_org_low.cost_climate_saved = (
            (g_water_org_low.CO2e_total_2021_estimated - g_water_org_low.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_water_org_high.demand_change = ass("Ass_L_G_no_LUC_203X")
        g_water_org_high.area_ha_change = l18.g_water_org_high.area_ha * (
            g_water_org_high.demand_change
        )
        g_water_org_high.area_ha = (
            l18.g_water_org_high.area_ha + g_water_org_high.area_ha_change
        )
        g_water_org_high.CO2e_pb = (
            g_water_org_high.CO2e_pb_per_t * g_water_org_high.area_ha
        )
        g_water_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_org_soil_bog_CO2e_per_ha_2018"
        )
        g_water_org_high.CO2e_total = g_water_org_high.CO2e_pb
        g_water_org_high.change_CO2e_t = (
            g_water_org_high.CO2e_total - l18.g_water_org_high.CO2e_total
        )
        g_water_org_high.change_CO2e_pct = (
            g_water_org_high.change_CO2e_t / l18.g_water_org_high.CO2e_total
        )
        g_water_org_high.CO2e_total_2021_estimated = (
            l18.g_water_org_high.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_water_org_high.cost_climate_saved = (
            (g_water_org_high.CO2e_total_2021_estimated - g_water_org_high.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_settlement.demand_change = (
            g_settlement.area_ha_change / l18.g_settlement.area_ha
        )
        g_settlement.area_ha_change = g_settlement.area_ha - l18.g_settlement.area_ha
        g_settlement.change_CO2e_pct = (
            g_settlement.change_CO2e_t / l18.g_settlement.CO2e_total
        )
        g_settlement.CO2e_total_2021_estimated = l18.g_settlement.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_settlement.cost_climate_saved = (
            (g_settlement.CO2e_total_2021_estimated - g_settlement.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_settlement.invest_pa = g_settlement_org.invest_pa
        g_settlement.cost_wage = g_settlement_org.cost_wage
        g_settlement.demand_emplo = g_settlement_org.demand_emplo
        g_settlement.demand_emplo_new = g_settlement_org.demand_emplo_new
        g_settlement_min.CO2e_total = g_settlement_min.CO2e_pb
        g_settlement_min.change_CO2e_t = (
            g_settlement_min.CO2e_total - l18.g_settlement_min.CO2e_total
        )
        g_settlement_min.change_CO2e_pct = (
            g_settlement_min.change_CO2e_t / l18.g_settlement_min.CO2e_total
        )
        g_settlement_min.CO2e_total_2021_estimated = (
            l18.g_settlement_min.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_settlement_min.cost_climate_saved = (
            (g_settlement_min.CO2e_total_2021_estimated - g_settlement_min.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_settlement_org_low.CO2e_total = g_settlement_org_low.CO2e_pb
        g_settlement_org_low.change_CO2e_t = (
            g_settlement_org_low.CO2e_total - l18.g_settlement_org_low.CO2e_total
        )
        g_settlement_org_low.change_CO2e_pct = (
            g_settlement_org_low.change_CO2e_t / l18.g_settlement_org_low.CO2e_total
        )
        g_settlement_org_low.CO2e_total_2021_estimated = (
            l18.g_settlement_org_low.CO2e_total
            * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_settlement_org_low.cost_climate_saved = (
            (
                g_settlement_org_low.CO2e_total_2021_estimated
                - g_settlement_org_low.CO2e_total
            )
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_settlement_org_high.CO2e_total = g_settlement_org_high.CO2e_pb
        g_settlement_org_high.change_CO2e_t = (
            g_settlement_org_high.CO2e_total - l18.g_settlement_org_high.CO2e_total
        )
        g_settlement_org_high.change_CO2e_pct = (
            g_settlement_org_high.change_CO2e_t / l18.g_settlement_org_high.CO2e_total
        )
        g_settlement_org_high.CO2e_total_2021_estimated = (
            l18.g_settlement_org_high.CO2e_total
            * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_settlement_org_high.cost_climate_saved = (
            (
                g_settlement_org_high.CO2e_total_2021_estimated
                - g_settlement_org_high.CO2e_total
            )
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_other.CO2e_total_2021_estimated = l18.g_other.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_other.cost_climate_saved = (
            (g_other.CO2e_total_2021_estimated - g_other.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_wood.change_CO2e_pct = g_wood.change_CO2e_t / l18.g_wood.CO2e_total
        g_wood.CO2e_total_2021_estimated = l18.g_wood.CO2e_total * fact(
            "Fact_M_CO2e_lulucf_2021_vs_2018"
        )
        g_wood.cost_climate_saved = (
            (g_wood.CO2e_total_2021_estimated - g_wood.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_settlement_org.cost_climate_saved = (
            (g_settlement_org.CO2e_total_2021_estimated - g_settlement_org.CO2e_total)
            * entry("In_M_duration_neutral")
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        g_settlement_org.CO2e_total_2021_estimated = (
            l18.g_settlement_org.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
        )
        g_settlement_org.CO2e_total = g_settlement_org.CO2e_pb
        g_settlement_org.CO2e_pb = (
            g_settlement_org_low.CO2e_pb + g_settlement_org_high.CO2e_pb
        )
        g_settlement_org.area_ha = (
            g_settlement_org_low.area_ha + g_settlement_org_high.area_ha
        )
