from .inputs import Inputs
from .utils import div
from dataclasses import dataclass, asdict


@dataclass
class LColVars2030:

    area_ha: float = None
    CO2e_pb_per_t: float = None
    pct_x: float = None
    CO2e_pb_per_MWh: float = None
    CO2e_cb: float = None
    CO2e_pb: float = None
    CO2e_total: float = None
    invest: float = None
    change_CO2e_t: float = None
    change_CO2e_pct: float = None
    CO2e_total_2021_estimated: float = None
    cost_climate_saved: float = None
    invest_pa: float = None
    cost_wage: float = None
    demand_emplo: float = None
    demand_emplo_new: float = None
    demand_change: float = None
    area_ha_change: float = None
    CO2e_cb_per_t: float = None
    action: float = None
    pct_of_wage: float = None
    ratio_wage_to_emplo: float = None
    emplo_existing: float = None
    invest_per_x: float = None
    area_ha_available_pct_of_action: float = None
    area_ha_available: float = None
    change_within_category: float = None
    change_wet_org_low: float = None
    change_wet_org_high: float = None
    prod_volume: float = None


@dataclass
class L30:
    # Klassenvariablen für L18
    l: LColVars2030 = LColVars2030()
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
    g_wet_org_low: LColVars2030 = LColVars2030()
    g_wet_org_high: LColVars2030 = LColVars2030()
    g_wet_org_low_r: LColVars2030 = LColVars2030()
    g_wet_org_low_rp: LColVars2030 = LColVars2030()
    g_wet_org_high_r: LColVars2030 = LColVars2030()
    g_wet_org_high_rp: LColVars2030 = LColVars2030()
    g_water: LColVars2030 = LColVars2030()
    g_water_min: LColVars2030 = LColVars2030()
    g_water_org: LColVars2030 = LColVars2030()
    g_settlement: LColVars2030 = LColVars2030()
    g_settlement_org: LColVars2030 = LColVars2030()
    g_settlement_min: LColVars2030 = LColVars2030()
    g_settlement_org_low: LColVars2030 = LColVars2030()
    g_settlement_org_high: LColVars2030 = LColVars2030()
    g_other: LColVars2030 = LColVars2030()
    g_wood: LColVars2030 = LColVars2030()
    pyr: LColVars2030 = LColVars2030()
    g_planning: LColVars2030 = LColVars2030()
    g_crop_org: LColVars2030 = LColVars2030()
    g_grass_org: LColVars2030 = LColVars2030()
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

    l18 = root.l18
    l = root.l30.l
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
    g_water_org_low = root.l30.g_water_org_low
    g_water_org_high = root.l30.g_water_org_high
    g_settlement = root.l30.g_settlement
    g_settlement_org = root.l30.g_settlement_org
    g_settlement_min = root.l30.g_settlement_min
    g_settlement_org_low = root.l30.g_settlement_org_low
    g_settlement_org_high = root.l30.g_settlement_org_high
    g_other = root.l30.g_other
    g_wood = root.l30.g_wood

    """S T A R T"""
    l.CO2e_total_2021_estimated = l18.l.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g.CO2e_total_2021_estimated = l18.g.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_settlement.invest = 0
    g_forest.CO2e_total_2021_estimated = l18.g_forest.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_forest_managed.demand_change = ass("Ass_L_G_forest_conv_pct_change")
    g_forest_managed.CO2e_pb_per_t = ass("Ass_L_G_forest_conv_CO2e_per_ha_2050")
    g_forest_managed.CO2e_cb_per_t = ass("Ass_L_G_forest_CO2e_cb_per_ha_2050")
    g_forest_managed.CO2e_total_2021_estimated = l18.g_forest_managed.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_forest_managed.invest_per_x = ass(
        "Ass_L_G_forest_afforestation_invest_per_ha_2020"
    )
    g_forest_managed.pct_of_wage = fact(
        "Fact_L_G_forest_afforestation_revenue_pct_of_wage_2018"
    )
    g_forest_managed.ratio_wage_to_emplo = fact(
        "Fact_L_G_forest_afforestation_ratio_wage_to_emplo_2018"
    )
    g_forest_managed.area_ha_available_pct_of_action = ass(
        "Ass_L_G_forest_conv_dead_pct_2018"
    ) / ass("Ass_L_G_forest_conv_pct_2050")
    g_forest_natural.demand_change = ass("Ass_L_G_forest_nature_pct_change")
    g_forest_natural.CO2e_pb_per_t = fact("Fact_L_G_forest_nature_CO2e_per_ha_2018")
    g_forest_natural.CO2e_total_2021_estimated = l18.g_forest_natural.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop.CO2e_total_2021_estimated = l18.g_crop.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop_min_conv.demand_change = ass("Ass_L_G_crop_organic_matter_pct_2050")
    g_crop_min_conv.CO2e_pb_per_t = fact(
        "Fact_L_G_crop_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_crop_min_conv.CO2e_total_2021_estimated = l18.g_crop_min_conv.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop_min_hum.CO2e_pb_per_t = fact(
        "Fact_L_G_crop_minrl_soil_sust_CO2e_per_ha_203X"
    )
    g_crop_min_hum.CO2e_total_2021_estimated = 0 * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop_org.CO2e_total_2021_estimated = l18.g_crop_org.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_crop_org_low.CO2e_pb_per_t = fact("Fact_L_G_crop_fen_CO2e_per_ha_2018")
    g_crop_org_low.CO2e_total_2021_estimated = l18.g_crop_org_low.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_crop_org_low.pct_of_wage = fact("Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018")
    g_crop_org_low.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_crop_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_crop_org_high.CO2e_pb_per_t = fact("Fact_L_G_crop_bog_CO2e_per_ha_2018")
    g_crop_org_high.CO2e_total_2021_estimated = l18.g_crop_org_high.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_crop_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_crop_org_high.pct_of_wage = fact(
        "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
    )
    g_crop_org_high.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_grass.CO2e_total_2021_estimated = l18.g_grass.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grass_min_conv.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_grass_min_conv.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_strict_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_grass_min_conv.CO2e_total_2021_estimated = l18.g_grass_min_conv.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grass_org.CO2e_total_2021_estimated = l18.g_grass_org.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grass_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_grass_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_strict_org_soil_fen_CO2e_per_ha_2018"
    )
    g_grass_org_low.CO2e_total_2021_estimated = l18.g_grass_org_low.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grass_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_grass_org_low.pct_of_wage = fact(
        "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
    )
    g_grass_org_low.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_grass_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_grass_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_strict_org_soil_bog_CO2e_per_ha_2018"
    )
    g_grass_org_high.CO2e_total_2021_estimated = l18.g_grass_org_high.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grass_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_grass_org_high.pct_of_wage = fact(
        "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
    )
    g_grass_org_high.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_grove.CO2e_total_2021_estimated = l18.g_grove.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grove_min.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_grove_min.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_woody_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_grove_min.CO2e_total_2021_estimated = l18.g_grove_min.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grove_org.CO2e_total_2021_estimated = l18.g_grove_org.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grove_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_grove_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_woody_org_soil_fen_CO2e_per_ha_2018"
    )
    g_grove_org_low.CO2e_total_2021_estimated = l18.g_grove_org_low.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grove_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_grove_org_low.pct_of_wage = fact(
        "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
    )
    g_grove_org_low.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_grove_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_grove_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_woody_org_soil_bog_CO2e_per_ha_2018"
    )
    g_grove_org_high.CO2e_total_2021_estimated = l18.g_grove_org_high.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_grove_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_grove_org_high.pct_of_wage = fact(
        "Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018"
    )
    g_grove_org_high.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_wet.CO2e_total_2021_estimated = l18.g_wet.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_min.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_wet_min.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_peat_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_wet_min.CO2e_total_2021_estimated = l18.g_wet_min.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org.CO2e_total_2021_estimated = l18.g_wet_org.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org_low.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_wet_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_peat_org_soil_fen_CO2e_per_ha_2018"
    )
    g_wet_org_low.CO2e_total_2021_estimated = l18.g_wet_org_low.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org_low.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_wet_org_low.pct_of_wage = fact("Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018")
    g_wet_org_low.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_wet_org_high.demand_change = ass("Ass_L_G_area_rewetting_2050")
    g_wet_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_peat_org_soil_bog_CO2e_per_ha_2018"
    )
    g_wet_org_high.CO2e_total_2021_estimated = l18.g_wet_org_high.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org_high.invest_per_x = ass("Ass_L_G_wet_rewetting_invest_per_ha_2016")
    g_wet_org_high.pct_of_wage = fact("Fact_L_G_wet_rewetting_revenue_pct_of_wage_2018")
    g_wet_org_high.ratio_wage_to_emplo = fact(
        "Fact_L_G_wet_rewetting_ratio_wage_to_emplo_2018"
    )
    g_wet_org_r.CO2e_total_2021_estimated = 0 * fact("Fact_M_CO2e_lulucf_2021_vs_2018")

    g_wet_org_low_r.CO2e_pb_per_t = fact("Fact_L_G_fen_wet_CO2e_per_ha_203X")
    g_wet_org_low_r.CO2e_total_2021_estimated = 0 * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )

    g_wet_org_high_r.CO2e_pb_per_t = fact("Fact_L_G_bog_wet_CO2e_per_ha_203X")
    g_wet_org_high_r.CO2e_total_2021_estimated = 0 * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org_rp.CO2e_total_2021_estimated = 0 * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
    g_wet_org_low_rp.pct_x = ass("Ass_L_G_wet_paludi_pct_2012")
    g_wet_org_low_rp.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_peat_org_soil_paludi_CO2e_per_ha_203X"
    )
    g_wet_org_low_rp.CO2e_total_2021_estimated = 0 * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org_low_rp.invest_per_x = ass("Ass_L_G_wet_paludi_invest_per_ha_2016")
    g_wet_org_high_rp.pct_x = ass("Ass_L_G_wet_paludi_pct_2012")
    g_wet_org_high_rp.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_peat_org_soil_paludi_CO2e_per_ha_203X"
    )
    g_wet_org_high_rp.CO2e_total_2021_estimated = 0 * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wet_org_high_rp.invest_per_x = ass("Ass_L_G_wet_paludi_invest_per_ha_2016")
    g_water.CO2e_total_2021_estimated = l18.g_water.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_water_org.invest = 0
    g_water_org.invest_pa = g_water_org.invest / entry("In_M_duration_target")
    g_water_org.demand_emplo_new = 0
    g_water_min.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_water_min.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_water_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_water_min.CO2e_total_2021_estimated = l18.g_water_min.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_water_org_low.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_water_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_water_org_soil_fen_CO2e_per_ha_2018"
    )
    g_water_org_low.CO2e_total_2021_estimated = l18.g_water_org_low.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_water_org_high.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_water_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_water_org_soil_bog_CO2e_per_ha_2018"
    )
    g_water_org_high.CO2e_total_2021_estimated = l18.g_water_org_high.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_settlement.CO2e_total_2021_estimated = l18.g_settlement.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_settlement_min.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_settlement_min.CO2e_pb_per_t = fact(
        "Fact_L_G_settl_minrl_soil_no_LUC_CO2e_per_ha_203X"
    )
    g_settlement_min.CO2e_total_2021_estimated = l18.g_settlement_min.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_settlement_org_low.demand_change = ass("Ass_L_G_settl_rewetting_2050")
    g_settlement_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_settl_org_soil_fen_CO2e_per_ha_2018"
    )
    g_settlement_org_low.CO2e_total_2021_estimated = (
        l18.g_settlement_org_low.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
    )
    g_settlement_org_high.demand_change = ass("Ass_L_G_settl_rewetting_2050")
    g_settlement_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_settl_org_soil_bog_CO2e_per_ha_2018"
    )
    g_settlement_org_high.CO2e_total_2021_estimated = (
        l18.g_settlement_org_high.CO2e_total * fact("Fact_M_CO2e_lulucf_2021_vs_2018")
    )
    g_other.demand_change = ass("Ass_L_G_no_LUC_203X")
    g_other.CO2e_pb_per_t = fact("Fact_L_G_other_minrl_soil_CO2e_per_ha_2018")
    g_other.CO2e_total_2021_estimated = l18.g_other.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_forest_managed.area_ha_change = (
        l18.g_forest_managed.area_ha * g_forest_managed.demand_change
    )
    g_forest_natural.area_ha_change = (
        l18.g_forest_natural.area_ha * g_forest_natural.demand_change
    )
    g_crop_min_conv.area_ha_change = l18.g_crop_min_conv.area_ha * (
        g_crop_min_conv.demand_change
    )
    g_crop_org_low.area_ha_change = (
        l18.g_crop_org_low.area_ha * g_crop_org_low.demand_change
    )
    g_crop_org_high.area_ha_change = (
        l18.g_crop_org_high.area_ha * g_crop_org_high.demand_change
    )
    g_grass_min_conv.area_ha_change = l18.g_grass_min_conv.area_ha * (
        g_grass_min_conv.demand_change
    )
    g_grass_org_low.area_ha_change = l18.g_grass_org_low.area_ha * (
        g_grass_org_low.demand_change
    )
    g_grass_org_high.area_ha_change = l18.g_grass_org_high.area_ha * (
        g_grass_org_high.demand_change
    )
    g_grove_min.area_ha_change = l18.g_grove_min.area_ha * (g_grove_min.demand_change)
    g_grove_org_low.area_ha_change = l18.g_grove_org_low.area_ha * (
        g_grove_org_low.demand_change
    )
    g_grove_org_high.area_ha_change = l18.g_grove_org_high.area_ha * (
        g_grove_org_high.demand_change
    )
    g_wet_min.area_ha_change = l18.g_wet_min.area_ha * (g_wet_min.demand_change)
    g_wet_org_low.area_ha_change = l18.g_wet_org_low.area_ha * (
        g_wet_org_low.demand_change
    )
    g_wet_org_high.area_ha_change = l18.g_wet_org_high.area_ha * (
        g_wet_org_high.demand_change
    )
    g_crop_org_low.to_wet_low = g_crop_org_low.area_ha_change
    g_grass_org_low.to_wet_low = g_grass_org_low.area_ha_change
    g_grove_org_low.to_wet_low = g_grove_org_low.area_ha_change
    g_wet_org_low.to_wet_low = g_wet_org_low.area_ha_change
    g_crop_org_high.to_wet_high = g_crop_org_high.area_ha_change
    g_grass_org_high.to_wet_high = g_grass_org_high.area_ha_change
    g_grove_org_high.to_wet_high = g_grove_org_high.area_ha_change
    g_wet_org_high.to_wet_high = g_wet_org_high.area_ha_change
    g_wet_org_low_r.area_ha_change = -(
        g_crop_org_low.to_wet_low
        + g_grass_org_low.to_wet_low
        + g_grove_org_low.to_wet_low
        + g_wet_org_low.to_wet_low
    )
    g_wet_org_high_r.area_ha_change = -(
        g_crop_org_high.to_wet_high
        + g_grass_org_high.to_wet_high
        + g_grove_org_high.to_wet_high
        + g_wet_org_high.to_wet_high
    )
    g_wet_org_low_rp.invest = -0 * g_wet_org_low_rp.invest_per_x
    g_wet_org_high_rp.invest = -0 * g_wet_org_high_rp.invest_per_x
    g_water.invest_pa = g_water_org.invest_pa
    g_water.invest = g_water_org.invest
    g_water.demand_emplo_new = g_water_org.demand_emplo_new
    g_water_min.area_ha_change = l18.g_water_min.area_ha * (g_water_min.demand_change)
    g_water_org_low.area_ha_change = l18.g_water_org_low.area_ha * (
        g_water_org_low.demand_change
    )
    g_water_org_high.area_ha_change = l18.g_water_org_high.area_ha * (
        g_water_org_high.demand_change
    )
    g_settlement_org.invest = 0
    g_settlement_org.invest_pa = g_settlement_org.invest / entry("In_M_duration_target")
    g_settlement.invest_pa = g_settlement_org.invest_pa
    g_settlement.cost_wage = g_settlement_org.cost_wage
    g_settlement.demand_emplo = g_settlement_org.demand_emplo
    g_settlement.demand_emplo_new = g_settlement_org.demand_emplo_new
    g_settlement_min.area_ha_change = l18.g_settlement_min.area_ha * (
        g_settlement_min.demand_change
    )
    g_settlement_org_low.area_ha_change = l18.g_settlement_org_low.area_ha * (
        g_settlement_org_low.demand_change
    )
    g_settlement_org_high.area_ha_change = l18.g_settlement_org_high.area_ha * (
        g_settlement_org_high.demand_change
    )
    g_other.area_ha_change = l18.g_other.area_ha * (g_other.demand_change)
    g_other.area_ha = (1 + g_other.demand_change) * l18.g_other.area_ha
    g_forest_managed.area_ha = (
        l18.g_forest_managed.area_ha + g_forest_managed.area_ha_change
    )
    g_forest_natural.area_ha = (
        l18.g_forest_natural.area_ha + g_forest_natural.area_ha_change
    )
    g_crop_min_conv.change_within_category = g_crop_min_conv.area_ha_change
    g_crop_min_conv.area_ha = (
        l18.g_crop_min_conv.area_ha + g_crop_min_conv.area_ha_change
    )
    g_crop_org_low.change_wet_org_low = g_crop_org_low.area_ha_change
    g_crop_org_low.area_ha = l18.g_crop_org_low.area_ha + g_crop_org_low.area_ha_change
    g_crop_org_low.invest = -g_crop_org_low.area_ha_change * g_crop_org_low.invest_per_x
    g_crop_org.area_ha_change = (
        g_crop_org_low.area_ha_change + g_crop_org_high.area_ha_change
    )
    g_crop_org_high.change_wet_org_high = g_crop_org_high.area_ha_change
    g_crop_org_high.area_ha = (
        l18.g_crop_org_high.area_ha + g_crop_org_high.area_ha_change
    )
    g_crop_org_high.invest = (
        -g_crop_org_high.area_ha_change * g_crop_org_high.invest_per_x
    )
    g_grass_min_conv.area_ha = (
        l18.g_grass_min_conv.area_ha + g_grass_min_conv.area_ha_change
    )
    g_grass_org_low.change_wet_org_low = g_grass_org_low.area_ha_change
    g_grass_org_low.area_ha = (
        l18.g_grass_org_low.area_ha + g_grass_org_low.area_ha_change
    )
    g_grass_org_low.invest = (
        -g_grass_org_low.area_ha_change * g_grass_org_low.invest_per_x
    )
    g_grass_org.area_ha_change = (
        g_grass_org_low.area_ha_change + g_grass_org_high.area_ha_change
    )
    g_grass_org_high.change_wet_org_high = g_grass_org_high.area_ha_change
    g_grass_org_high.area_ha = (
        l18.g_grass_org_high.area_ha + g_grass_org_high.area_ha_change
    )
    g_grass_org_high.invest = (
        -g_grass_org_high.area_ha_change * g_grass_org_high.invest_per_x
    )
    g_grove_min.area_ha = l18.g_grove_min.area_ha + g_grove_min.area_ha_change
    g_grove_org_low.change_wet_org_low = g_grove_org_low.area_ha_change
    g_grove_org_low.area_ha = (
        l18.g_grove_org_low.area_ha + g_grove_org_low.area_ha_change
    )
    g_grove_org_low.invest = (
        -g_grove_org_low.area_ha_change * g_grove_org_low.invest_per_x
    )
    g_grove_org.area_ha_change = (
        g_grove_org_low.area_ha_change + g_grove_org_high.area_ha_change
    )
    g_grove_org_high.change_wet_org_high = g_grove_org_high.area_ha_change
    g_grove_org_high.area_ha = (
        l18.g_grove_org_high.area_ha + g_grove_org_high.area_ha_change
    )
    g_grove_org_high.invest = (
        -g_grove_org_high.area_ha_change * g_grove_org_high.invest_per_x
    )
    g_wet_min.area_ha = l18.g_wet_min.area_ha + g_wet_min.area_ha_change
    g_wet_org_low.change_wet_org_low = g_wet_org_low.area_ha_change
    g_wet_org_low.area_ha = l18.g_wet_org_low.area_ha + g_wet_org_low.area_ha_change
    g_wet_org_low.invest = -g_wet_org_low.area_ha_change * g_wet_org_low.invest_per_x
    g_wet_org.area_ha_change = (
        g_wet_org_low.area_ha_change + g_wet_org_high.area_ha_change
    )
    g_wet_org_high.change_wet_org_high = g_wet_org_high.area_ha_change
    g_wet_org_high.area_ha = l18.g_wet_org_high.area_ha + g_wet_org_high.area_ha_change
    g_wet_org_high.invest = -g_wet_org_high.area_ha_change * g_wet_org_high.invest_per_x
    g_wet_org_low_r.area_ha = g_wet_org_low_r.area_ha_change
    g_wet_org_r.area_ha_change = (
        g_wet_org_low_r.area_ha_change + g_wet_org_high_r.area_ha_change
    )
    g_wet_org_high_r.area_ha = g_wet_org_high_r.area_ha_change
    g_wet_org_low_rp.invest_pa = g_wet_org_low_rp.invest / entry("In_M_duration_target")
    g_wet_org_rp.invest = g_wet_org_low_rp.invest + g_wet_org_high_rp.invest
    g_wet_org_high_rp.invest_pa = g_wet_org_high_rp.invest / entry(
        "In_M_duration_target"
    )
    g_water_min.area_ha = l18.g_water_min.area_ha + g_water_min.area_ha_change
    g_water_org_low.area_ha = (
        l18.g_water_org_low.area_ha + g_water_org_low.area_ha_change
    )
    g_water_org_high.area_ha = (
        l18.g_water_org_high.area_ha + g_water_org_high.area_ha_change
    )

    g_settlement_min.area_ha = (
        l18.g_settlement_min.area_ha + g_settlement_min.area_ha_change
    )
    g_settlement_org_low.area_ha = (
        l18.g_settlement_org_low.area_ha + g_settlement_org_low.area_ha_change
    )
    g_settlement_org_high.area_ha = (
        l18.g_settlement_org_high.area_ha + g_settlement_org_high.area_ha_change
    )
    g_other.CO2e_pb = g_other.CO2e_pb_per_t * g_other.area_ha
    g_forest_managed.CO2e_pb = g_forest_managed.CO2e_pb_per_t * g_forest_managed.area_ha
    g_forest_managed.CO2e_cb = g_forest_managed.area_ha * g_forest_managed.CO2e_cb_per_t
    g_forest_managed.area_ha_available = (
        g_forest_managed.area_ha * g_forest_managed.area_ha_available_pct_of_action
    )
    g_forest.area_ha = g_forest_managed.area_ha + g_forest_natural.area_ha
    g_forest_natural.CO2e_pb = g_forest_natural.CO2e_pb_per_t * g_forest_natural.area_ha
    g_crop_min_hum.area_ha_change = -g_crop_min_conv.change_within_category
    g_crop_min_conv.CO2e_pb = g_crop_min_conv.CO2e_pb_per_t * g_crop_min_conv.area_ha
    g_crop_org_low.CO2e_pb = g_crop_org_low.CO2e_pb_per_t * g_crop_org_low.area_ha
    g_crop_org_low.invest_pa = g_crop_org_low.invest / entry("In_M_duration_target")
    g_crop_org.area_ha = g_crop_org_low.area_ha + g_crop_org_high.area_ha
    g_crop_org_high.CO2e_pb = g_crop_org_high.CO2e_pb_per_t * g_crop_org_high.area_ha
    g_crop_org.invest = g_crop_org_low.invest + g_crop_org_high.invest
    g_crop_org_high.invest_pa = g_crop_org_high.invest / entry("In_M_duration_target")
    g_grass_min_conv.CO2e_pb = g_grass_min_conv.CO2e_pb_per_t * g_grass_min_conv.area_ha
    g_grass_org_low.CO2e_pb = g_grass_org_low.CO2e_pb_per_t * g_grass_org_low.area_ha
    g_grass_org_low.invest_pa = g_grass_org_low.invest / entry("In_M_duration_target")
    g_grass.area_ha = (
        g_grass_min_conv.area_ha + g_grass_org_low.area_ha + g_grass_org_high.area_ha
    )
    g_grass_org.area_ha = g_grass_org_low.area_ha + g_grass_org_high.area_ha
    g_grass_org_high.CO2e_pb = g_grass_org_high.CO2e_pb_per_t * g_grass_org_high.area_ha
    g_grass.invest = g_grass_org_low.invest + g_grass_org_high.invest
    g_grass_org.invest = g_grass_org_low.invest + g_grass_org_high.invest
    g_grass_org_high.invest_pa = g_grass_org_high.invest / entry("In_M_duration_target")
    g_grove_min.CO2e_pb = g_grove_min.CO2e_pb_per_t * g_grove_min.area_ha
    g_grove_org_low.CO2e_pb = g_grove_org_low.CO2e_pb_per_t * g_grove_org_low.area_ha
    g_grove_org_low.invest_pa = g_grove_org_low.invest / entry("In_M_duration_target")
    g_grove.area_ha = (
        g_grove_min.area_ha + g_grove_org_low.area_ha + g_grove_org_high.area_ha
    )
    g_grove_org.area_ha = g_grove_org_low.area_ha + g_grove_org_high.area_ha
    g_grove_org_high.CO2e_pb = g_grove_org_high.CO2e_pb_per_t * g_grove_org_high.area_ha
    g_grove.invest = g_grove_org_low.invest + g_grove_org_high.invest
    g_grove_org.invest = g_grove_org_low.invest + g_grove_org_high.invest
    g_grove_org_high.invest_pa = g_grove_org_high.invest / entry("In_M_duration_target")
    g_wet_min.CO2e_pb = g_wet_min.CO2e_pb_per_t * g_wet_min.area_ha
    g_wet_org_low.CO2e_pb = g_wet_org_low.CO2e_pb_per_t * g_wet_org_low.area_ha
    g_wet_org_low.invest_pa = g_wet_org_low.invest / entry("In_M_duration_target")
    g_wet_org.area_ha = g_wet_org_low.area_ha + g_wet_org_high.area_ha
    g_wet_org_high.CO2e_pb = g_wet_org_high.CO2e_pb_per_t * g_wet_org_high.area_ha
    g_wet_org.invest = g_wet_org_low.invest + g_wet_org_high.invest
    g_wet_org_high.invest_pa = g_wet_org_high.invest / entry("In_M_duration_target")
    g_wet_org_low_r.CO2e_pb = g_wet_org_low_r.CO2e_pb_per_t * g_wet_org_low_r.area_ha
    g_wet_org_low_rp.area_ha = g_wet_org_low_r.area_ha * g_wet_org_low_rp.pct_x
    g_wet_org_r.area_ha = g_wet_org_low_r.area_ha + g_wet_org_high_r.area_ha
    g_wet_org_high_r.CO2e_pb = g_wet_org_high_r.CO2e_pb_per_t * g_wet_org_high_r.area_ha
    g_wet_org_high_rp.area_ha = g_wet_org_high_r.area_ha * g_wet_org_high_rp.pct_x
    g_wet_org_rp.invest_pa = g_wet_org_rp.invest / entry("In_M_duration_target")

    g_water_min.CO2e_pb = g_water_min.CO2e_pb_per_t * g_water_min.area_ha
    g_water_org_low.CO2e_pb = g_water_org_low.CO2e_pb_per_t * g_water_org_low.area_ha
    g_water_org_high.CO2e_pb = g_water_org_high.CO2e_pb_per_t * g_water_org_high.area_ha
    g_water_org.area_ha = g_water_org_low.area_ha + g_water_org_high.area_ha
    g_water.area_ha = g_water_min.area_ha + g_water_org.area_ha
    g_water_org.CO2e_pb = g_water_org_low.CO2e_pb + g_water_org_high.CO2e_pb
    g_settlement_min.CO2e_pb = g_settlement_min.CO2e_pb_per_t * g_settlement_min.area_ha
    g_settlement_org_low.CO2e_pb = (
        g_settlement_org_low.CO2e_pb_per_t * g_settlement_org_low.area_ha
    )
    g_settlement.area_ha = (
        g_settlement_min.area_ha
        + g_settlement_org_low.area_ha
        + g_settlement_org_high.area_ha
    )
    g_settlement_org_high.CO2e_pb = (
        g_settlement_org_high.CO2e_pb_per_t * g_settlement_org_high.area_ha
    )
    g_other.CO2e_total = g_other.CO2e_pb
    g_forest.CO2e_cb = g_forest_managed.CO2e_cb
    g_forest_managed.CO2e_total = g_forest_managed.CO2e_pb + g_forest_managed.CO2e_cb
    g_forest_managed.invest = (
        g_forest_managed.area_ha_available * g_forest_managed.invest_per_x
    )
    g_forest.area_ha_change = g_forest.area_ha - l18.g_forest.area_ha
    g_forest.CO2e_pb = g_forest_managed.CO2e_pb + g_forest_natural.CO2e_pb
    g_forest_natural.CO2e_total = g_forest_natural.CO2e_pb
    g_crop_min_hum.area_ha = g_crop_min_hum.area_ha_change
    g_crop_min_conv.CO2e_total = g_crop_min_conv.CO2e_pb
    g_crop_org_low.CO2e_total = g_crop_org_low.CO2e_pb
    g_crop_org_low.cost_wage = g_crop_org_low.invest_pa * g_crop_org_low.pct_of_wage
    g_crop_org.CO2e_pb = g_crop_org_low.CO2e_pb + g_crop_org_high.CO2e_pb
    g_crop_org_high.CO2e_total = g_crop_org_high.CO2e_pb
    g_crop.invest = g_crop_org.invest
    g_crop_org.invest_pa = g_crop_org.invest / entry("In_M_duration_target")
    g_crop_org_high.cost_wage = g_crop_org_high.invest_pa * g_crop_org_high.pct_of_wage
    g_grass_min_conv.CO2e_total = g_grass_min_conv.CO2e_pb
    g_grass_org_low.CO2e_total = g_grass_org_low.CO2e_pb
    g_grass_org_low.cost_wage = g_grass_org_low.invest_pa * g_grass_org_low.pct_of_wage
    g_grass.area_ha_change = g_grass.area_ha - l18.g_grass.area_ha
    g_grass.CO2e_pb = (
        g_grass_min_conv.CO2e_pb + g_grass_org_low.CO2e_pb + g_grass_org_high.CO2e_pb
    )
    g_grass_org.CO2e_pb = g_grass_org_low.CO2e_pb + g_grass_org_high.CO2e_pb
    g_grass_org_high.CO2e_total = g_grass_org_high.CO2e_pb
    g_grass_org.invest_pa = g_grass_org.invest / entry("In_M_duration_target")
    g_grass_org_high.cost_wage = (
        g_grass_org_high.invest_pa * g_grass_org_high.pct_of_wage
    )
    g_grove_min.CO2e_total = g_grove_min.CO2e_pb
    g_grove_org_low.CO2e_total = g_grove_org_low.CO2e_pb
    g_grove_org_low.cost_wage = g_grove_org_low.invest_pa * g_grove_org_low.pct_of_wage
    g_grove.area_ha_change = g_grove.area_ha - l18.g_grove.area_ha
    g_grove.CO2e_pb = (
        g_grove_min.CO2e_pb + g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
    )
    g_grove_org.CO2e_pb = g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
    g_grove_org_high.CO2e_total = g_grove_org_high.CO2e_pb
    g_grove_org.invest_pa = g_grove_org.invest / entry("In_M_duration_target")
    g_grove_org_high.cost_wage = (
        g_grove_org_high.invest_pa * g_grove_org_high.pct_of_wage
    )
    g_wet_min.CO2e_total = g_wet_min.CO2e_pb
    g_wet_org_low.CO2e_total = g_wet_org_low.CO2e_pb
    g_wet_org_low.cost_wage = g_wet_org_low.invest_pa * g_wet_org_low.pct_of_wage
    g_wet_org.CO2e_pb = g_wet_org_low.CO2e_pb + g_wet_org_high.CO2e_pb
    g_wet_org_high.CO2e_total = g_wet_org_high.CO2e_pb
    g_wet.invest = g_wet_org.invest + g_wet_org_rp.invest
    g_wet_org.invest_pa = g_wet_org.invest / entry("In_M_duration_target")
    g_wet_org_high.cost_wage = g_wet_org_high.invest_pa * g_wet_org_high.pct_of_wage
    g_wet_org_low_r.CO2e_total = g_wet_org_low_r.CO2e_pb
    g_wet_org_low_rp.CO2e_pb = g_wet_org_low_rp.CO2e_pb_per_t * g_wet_org_low_rp.area_ha
    g_wet_org_low_rp.CO2e_pb = g_wet_org_low_rp.CO2e_pb_per_t * g_wet_org_low_rp.area_ha
    g_wet.area_ha = g_wet_min.area_ha + g_wet_org.area_ha + g_wet_org_r.area_ha
    g_wet_org_r.CO2e_pb = g_wet_org_low_r.CO2e_pb + g_wet_org_high_r.CO2e_pb
    g_wet_org_high_r.CO2e_total = g_wet_org_high_r.CO2e_pb
    g_wet_org_rp.area_ha = g_wet_org_low_rp.area_ha + g_wet_org_high_rp.area_ha
    g_wet_org_high_rp.CO2e_pb = (
        g_wet_org_high_rp.CO2e_pb_per_t * g_wet_org_high_rp.area_ha
    )
    g_water.area_ha_change = g_water.area_ha - l18.g_water.area_ha
    g_water.CO2e_pb = g_water_min.CO2e_pb + g_water_org.CO2e_pb
    g_water_min.CO2e_total = g_water_min.CO2e_pb
    g_water_org_low.CO2e_total = g_water_org_low.CO2e_pb
    g_water_org_high.CO2e_total = g_water_org_high.CO2e_pb
    g_settlement_min.CO2e_total = g_settlement_min.CO2e_pb
    g_settlement_org_low.CO2e_total = g_settlement_org_low.CO2e_pb
    g_settlement.area_ha_change = g_settlement.area_ha - l18.g_settlement.area_ha
    g_settlement.CO2e_pb = (
        g_settlement_min.CO2e_pb
        + g_settlement_org_low.CO2e_pb
        + g_settlement_org_high.CO2e_pb
    )
    g_settlement_org_high.CO2e_total = g_settlement_org_high.CO2e_pb
    g_other.change_CO2e_t = g_other.CO2e_total - l18.g_other.CO2e_total
    g_other.cost_climate_saved = (
        (g_other.CO2e_total_2021_estimated - g_other.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g.CO2e_cb = g_forest.CO2e_cb
    g_forest_managed.change_CO2e_t = (
        g_forest_managed.CO2e_total - l18.g_forest_managed.CO2e_total
    )
    g_forest_managed.cost_climate_saved = (
        (g_forest_managed.CO2e_total_2021_estimated - g_forest_managed.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_forest.invest = g_forest_managed.invest
    g_forest_managed.invest_pa = g_forest_managed.invest / entry("In_M_duration_target")
    g_forest.CO2e_total = g_forest.CO2e_cb + g_forest.CO2e_pb
    g_forest_natural.change_CO2e_t = (
        g_forest_natural.CO2e_total - l18.g_forest_natural.CO2e_total
    )
    g_forest_natural.cost_climate_saved = (
        (g_forest_natural.CO2e_total_2021_estimated - g_forest_natural.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop.area_ha = (
        g_crop_min_conv.area_ha
        + g_crop_min_hum.area_ha
        + g_crop_org_low.area_ha
        + g_crop_org_high.area_ha
    )
    g_crop_min_hum.CO2e_pb = g_crop_min_hum.CO2e_pb_per_t * g_crop_min_hum.area_ha
    g_crop_min_conv.change_CO2e_t = (
        g_crop_min_conv.CO2e_total - l18.g_crop_min_conv.CO2e_total
    )
    g_crop_min_conv.cost_climate_saved = (
        (g_crop_min_conv.CO2e_total_2021_estimated - g_crop_min_conv.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop_org_low.change_CO2e_t = (
        g_crop_org_low.CO2e_total - l18.g_crop_org_low.CO2e_total
    )
    g_crop_org_low.cost_climate_saved = (
        (g_crop_org_low.CO2e_total_2021_estimated - g_crop_org_low.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop_org_low.demand_emplo = div(
        g_crop_org_low.cost_wage, g_crop_org_low.ratio_wage_to_emplo
    )
    g_crop_org.CO2e_total = g_crop_org.CO2e_pb
    g_crop_org_high.change_CO2e_t = (
        g_crop_org_high.CO2e_total - l18.g_crop_org_high.CO2e_total
    )
    g_crop_org_high.cost_climate_saved = (
        (g_crop_org_high.CO2e_total_2021_estimated - g_crop_org_high.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop.invest_pa = g_crop_org.invest_pa
    g_crop_org.cost_wage = g_crop_org_low.cost_wage + g_crop_org_high.cost_wage
    g_crop_org_high.demand_emplo = div(
        g_crop_org_high.cost_wage, g_crop_org_high.ratio_wage_to_emplo
    )
    g_grass_min_conv.change_CO2e_t = (
        g_grass_min_conv.CO2e_total - l18.g_grass_min_conv.CO2e_total
    )
    g_grass_min_conv.cost_climate_saved = (
        (g_grass_min_conv.CO2e_total_2021_estimated - g_grass_min_conv.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grass_org_low.change_CO2e_t = (
        g_grass_org_low.CO2e_total - l18.g_grass_org_low.CO2e_total
    )
    g_grass_org_low.cost_climate_saved = (
        (g_grass_org_low.CO2e_total_2021_estimated - g_grass_org_low.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grass_org_low.demand_emplo = div(
        g_grass_org_low.cost_wage, g_grass_org_low.ratio_wage_to_emplo
    )
    g_grass.demand_change = div(g_grass.area_ha_change, l18.g_grass.area_ha)
    g_grass.CO2e_total = g_grass.CO2e_pb
    g_grass_org.CO2e_total = g_grass_org.CO2e_pb
    g_grass_org_high.change_CO2e_t = (
        g_grass_org_high.CO2e_total - l18.g_grass_org_high.CO2e_total
    )
    g_grass_org_high.cost_climate_saved = (
        (g_grass_org_high.CO2e_total_2021_estimated - g_grass_org_high.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grass.invest_pa = g_grass_org.invest_pa
    g_grass_org.cost_wage = g_grass_org_low.cost_wage + g_grass_org_high.cost_wage
    g_grass_org_high.demand_emplo = div(
        g_grass_org_high.cost_wage, g_grass_org_high.ratio_wage_to_emplo
    )
    g_grove_min.change_CO2e_t = g_grove_min.CO2e_total - l18.g_grove_min.CO2e_total
    g_grove_min.cost_climate_saved = (
        (g_grove_min.CO2e_total_2021_estimated - g_grove_min.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grove_org_low.change_CO2e_t = (
        g_grove_org_low.CO2e_total - l18.g_grove_org_low.CO2e_total
    )
    g_grove_org_low.cost_climate_saved = (
        (g_grove_org_low.CO2e_total_2021_estimated - g_grove_org_low.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grove_org_low.demand_emplo = div(
        g_grove_org_low.cost_wage, g_grove_org_low.ratio_wage_to_emplo
    )
    g_grove.demand_change = div(g_grove.area_ha_change, l18.g_grove.area_ha)
    g_grove.CO2e_total = g_grove.CO2e_pb
    g_grove_org.CO2e_total = g_grove_org.CO2e_pb
    g_grove_org_high.change_CO2e_t = (
        g_grove_org_high.CO2e_total - l18.g_grove_org_high.CO2e_total
    )
    g_grove_org_high.cost_climate_saved = (
        (g_grove_org_high.CO2e_total_2021_estimated - g_grove_org_high.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grove.invest_pa = g_grove_org.invest_pa
    g_grove_org.cost_wage = g_grove_org_low.cost_wage + g_grove_org_high.cost_wage
    g_grove_org_high.demand_emplo = div(
        g_grove_org_high.cost_wage, g_grove_org_high.ratio_wage_to_emplo
    )
    g_wet_min.change_CO2e_t = g_wet_min.CO2e_total - l18.g_wet_min.CO2e_total
    g_wet_min.cost_climate_saved = (
        (g_wet_min.CO2e_total_2021_estimated - g_wet_min.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet_org_low.change_CO2e_t = (
        g_wet_org_low.CO2e_total - l18.g_wet_org_low.CO2e_total
    )
    g_wet_org_low.cost_climate_saved = (
        (g_wet_org_low.CO2e_total_2021_estimated - g_wet_org_low.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet_org_low.demand_emplo = div(
        g_wet_org_low.cost_wage, g_wet_org_low.ratio_wage_to_emplo
    )
    g_wet_org.CO2e_total = g_wet_org.CO2e_pb
    g_wet_org_high.change_CO2e_t = (
        g_wet_org_high.CO2e_total - l18.g_wet_org_high.CO2e_total
    )
    g_wet_org_high.cost_climate_saved = (
        (g_wet_org_high.CO2e_total_2021_estimated - g_wet_org_high.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet.invest_pa = g_wet_org.invest_pa + g_wet_org_rp.invest_pa
    g_wet_org.cost_wage = g_wet_org_low.cost_wage + g_wet_org_high.cost_wage
    g_wet_org_high.demand_emplo = div(
        g_wet_org_high.cost_wage, g_wet_org_high.ratio_wage_to_emplo
    )
    g_wet_org_low_r.change_CO2e_t = g_wet_org_low_r.CO2e_total
    g_wet_org_low_r.cost_climate_saved = (
        (g_wet_org_low_r.CO2e_total_2021_estimated - g_wet_org_low_r.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet_org_low_rp.CO2e_total = g_wet_org_low_rp.CO2e_pb
    g_wet.area_ha_change = g_wet.area_ha - l18.g_wet.area_ha
    g_wet_org_r.CO2e_total = g_wet_org_r.CO2e_pb
    g_wet_org_high_r.change_CO2e_t = g_wet_org_high_r.CO2e_total
    g_wet_org_high_r.cost_climate_saved = (
        (g_wet_org_high_r.CO2e_total_2021_estimated - g_wet_org_high_r.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet_org_rp.CO2e_pb = g_wet_org_low_rp.CO2e_pb + g_wet_org_high_rp.CO2e_pb
    g_wet_org_high_rp.CO2e_total = g_wet_org_high_rp.CO2e_pb
    g_water.demand_change = div(g_water.area_ha_change, l18.g_water.area_ha)
    g_water.CO2e_total = g_water.CO2e_pb
    g_water_min.change_CO2e_t = g_water_min.CO2e_total - l18.g_water_min.CO2e_total
    g_water_min.cost_climate_saved = (
        (g_water_min.CO2e_total_2021_estimated - g_water_min.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_water_org_low.change_CO2e_t = (
        g_water_org_low.CO2e_total - l18.g_water_org_low.CO2e_total
    )
    g_water_org_low.cost_climate_saved = (
        (g_water_org_low.CO2e_total_2021_estimated - g_water_org_low.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_water_org_high.change_CO2e_t = (
        g_water_org_high.CO2e_total - l18.g_water_org_high.CO2e_total
    )
    g_water_org_high.cost_climate_saved = (
        (g_water_org_high.CO2e_total_2021_estimated - g_water_org_high.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_settlement_min.change_CO2e_t = (
        g_settlement_min.CO2e_total - l18.g_settlement_min.CO2e_total
    )
    g_settlement_min.cost_climate_saved = (
        (g_settlement_min.CO2e_total_2021_estimated - g_settlement_min.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_settlement_org_low.change_CO2e_t = (
        g_settlement_org_low.CO2e_total - l18.g_settlement_org_low.CO2e_total
    )
    g_settlement_org_low.cost_climate_saved = (
        (
            g_settlement_org_low.CO2e_total_2021_estimated
            - g_settlement_org_low.CO2e_total
        )
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_settlement.demand_change = div(
        g_settlement.area_ha_change, l18.g_settlement.area_ha
    )
    g_settlement.CO2e_total = g_settlement.CO2e_pb
    g_settlement_org_high.change_CO2e_t = (
        g_settlement_org_high.CO2e_total - l18.g_settlement_org_high.CO2e_total
    )
    g_settlement_org_high.cost_climate_saved = (
        (
            g_settlement_org_high.CO2e_total_2021_estimated
            - g_settlement_org_high.CO2e_total
        )
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_forest_managed.change_CO2e_pct = div(
        g_forest_managed.change_CO2e_t, l18.g_forest_managed.CO2e_total
    )
    g.invest = (
        g_forest.invest
        + g_crop.invest
        + g_grass.invest
        + g_grove.invest
        + g_wet.invest
        + g_water.invest
        + g_settlement.invest
    )
    g_forest.invest_pa = g_forest_managed.invest_pa
    g_forest_managed.cost_wage = (
        g_forest_managed.invest_pa * g_forest_managed.pct_of_wage
    )
    g_forest.change_CO2e_t = g_forest.CO2e_total - l18.g_forest.CO2e_total
    g_forest.cost_climate_saved = (
        (g_forest.CO2e_total_2021_estimated - g_forest.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_forest_natural.change_CO2e_pct = div(
        g_forest_natural.change_CO2e_t, l18.g_forest_natural.CO2e_total
    )
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
    g_crop.area_ha_change = g_crop.area_ha - l18.g_crop.area_ha
    g_crop.CO2e_pb = (
        g_crop_min_conv.CO2e_pb
        + g_crop_min_hum.CO2e_pb
        + g_crop_org_low.CO2e_pb
        + g_crop_org_high.CO2e_pb
    )
    g_crop_min_hum.CO2e_total = g_crop_min_hum.CO2e_pb
    g_crop_min_conv.change_CO2e_pct = div(
        g_crop_min_conv.change_CO2e_t, l18.g_crop_min_conv.CO2e_total
    )
    g_crop_org_low.change_CO2e_pct = div(
        g_crop_org_low.change_CO2e_t, l18.g_crop_org_low.CO2e_total
    )
    g_crop_org_low.demand_emplo_new = g_crop_org_low.demand_emplo
    g_crop_org.change_CO2e_t = g_crop_org.CO2e_total - l18.g_crop_org.CO2e_total
    g_crop_org.cost_climate_saved = (
        (g_crop_org.CO2e_total_2021_estimated - g_crop_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop_org_high.change_CO2e_pct = div(
        g_crop_org_high.change_CO2e_t, l18.g_crop_org_high.CO2e_total
    )
    g_crop.cost_wage = g_crop_org.cost_wage
    g_crop_org.demand_emplo = g_crop_org_low.demand_emplo + g_crop_org_high.demand_emplo
    g_crop_org_high.demand_emplo_new = g_crop_org_high.demand_emplo
    g_grass_min_conv.change_CO2e_pct = div(
        g_grass_min_conv.change_CO2e_t, l18.g_grass_min_conv.CO2e_total
    )
    g_grass_org_low.change_CO2e_pct = div(
        g_grass_org_low.change_CO2e_t, l18.g_grass_org_low.CO2e_total
    )
    g_grass_org_low.demand_emplo_new = g_grass_org_low.demand_emplo
    g_grass.change_CO2e_t = g_grass.CO2e_total - l18.g_grass.CO2e_total
    g_grass.cost_climate_saved = (
        (g_grass.CO2e_total_2021_estimated - g_grass.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grass_org.change_CO2e_t = g_grass_org.CO2e_total - l18.g_grass_org.CO2e_total
    g_grass_org.cost_climate_saved = (
        (g_grass_org.CO2e_total_2021_estimated - g_grass_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grass_org_high.change_CO2e_pct = div(
        g_grass_org_high.change_CO2e_t, l18.g_grass_org_high.CO2e_total
    )
    g_grass.cost_wage = g_grass_org.cost_wage
    g_grass_org.demand_emplo = (
        g_grass_org_low.demand_emplo + g_grass_org_high.demand_emplo
    )
    g_grass_org_high.demand_emplo_new = g_grass_org_high.demand_emplo
    g_grove_min.change_CO2e_pct = div(
        g_grove_min.change_CO2e_t, l18.g_grove_min.CO2e_total
    )
    g_grove_org_low.change_CO2e_pct = div(
        g_grove_org_low.change_CO2e_t, l18.g_grove_org_low.CO2e_total
    )
    g_grove_org_low.demand_emplo_new = g_grove_org_low.demand_emplo
    g_grove.change_CO2e_t = g_grove.CO2e_total - l18.g_grove.CO2e_total
    g_grove.cost_climate_saved = (
        (g_grove.CO2e_total_2021_estimated - g_grove.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grove_org.change_CO2e_t = g_grove_org.CO2e_total - l18.g_grove_org.CO2e_total
    g_grove_org.cost_climate_saved = (
        (g_grove_org.CO2e_total_2021_estimated - g_grove_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grove_org.cost_climate_saved = (
        (g_grove_org.CO2e_total_2021_estimated - g_grove_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_grove_org_high.change_CO2e_pct = div(
        g_grove_org_high.change_CO2e_t, l18.g_grove_org_high.CO2e_total
    )
    g_grove.cost_wage = g_grove_org.cost_wage
    g_water.cost_wage = g_water_org.cost_wage
    g_grove_org.demand_emplo = (
        g_grove_org_low.demand_emplo + g_grove_org_high.demand_emplo
    )
    g_grove_org_high.demand_emplo_new = g_grove_org_high.demand_emplo
    g_wet_min.change_CO2e_pct = div(g_wet_min.change_CO2e_t, l18.g_wet_min.CO2e_total)
    g_wet_org_low.change_CO2e_pct = div(
        g_wet_org_low.change_CO2e_t, l18.g_wet_org_low.CO2e_total
    )
    g_wet_org_low.demand_emplo_new = g_wet_org_low.demand_emplo
    g_wet_org.change_CO2e_t = g_wet_org.CO2e_total - l18.g_wet_org.CO2e_total
    g_wet_org.cost_climate_saved = (
        (g_wet_org.CO2e_total_2021_estimated - g_wet_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet_org_high.change_CO2e_pct = div(
        g_wet_org_high.change_CO2e_t, l18.g_wet_org_high.CO2e_total
    )
    g_wet.cost_wage = g_wet_org.cost_wage
    g_wet_org.demand_emplo = g_wet_org_low.demand_emplo + g_wet_org_high.demand_emplo
    g_wet_org_high.demand_emplo_new = g_wet_org_high.demand_emplo
    g_wet_org_low_rp.change_CO2e_t = g_wet_org_low_rp.CO2e_total
    g_wet_org_low_rp.cost_climate_saved = (
        (g_wet_org_low_rp.CO2e_total_2021_estimated - g_wet_org_low_rp.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet_org_r.change_CO2e_t = g_wet_org_r.CO2e_total
    g_wet_org_r.cost_climate_saved = (
        (g_wet_org_r.CO2e_total_2021_estimated - g_wet_org_r.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet.CO2e_pb = (
        g_wet_min.CO2e_pb
        + g_wet_org.CO2e_pb
        + g_wet_org_r.CO2e_pb
        + g_wet_org_rp.CO2e_pb
    )
    g_wet_org_rp.CO2e_total = g_wet_org_rp.CO2e_pb
    g_wet_org_high_rp.change_CO2e_t = g_wet_org_high_rp.CO2e_total
    g_wet_org_high_rp.cost_climate_saved = (
        (g_wet_org_high_rp.CO2e_total_2021_estimated - g_wet_org_high_rp.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_water.change_CO2e_t = g_water.CO2e_total - l18.g_water.CO2e_total
    g_water.cost_climate_saved = (
        (g_water.CO2e_total_2021_estimated - g_water.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_water_min.change_CO2e_pct = div(
        g_water_min.change_CO2e_t, l18.g_water_min.CO2e_total
    )
    g_water_org_low.change_CO2e_pct = div(
        g_water_org_low.change_CO2e_t, l18.g_water_org_low.CO2e_total
    )
    g_water_org_high.change_CO2e_pct = div(
        g_water_org_high.change_CO2e_t, l18.g_water_org_high.CO2e_total
    )
    g_settlement_min.change_CO2e_pct = div(
        g_settlement_min.change_CO2e_t, l18.g_settlement_min.CO2e_total
    )
    g_settlement_org_low.change_CO2e_pct = div(
        g_settlement_org_low.change_CO2e_t, l18.g_settlement_org_low.CO2e_total
    )
    g_settlement.change_CO2e_t = g_settlement.CO2e_total - l18.g_settlement.CO2e_total
    g_settlement.cost_climate_saved = (
        (g_settlement.CO2e_total_2021_estimated - g_settlement.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_settlement_org_high.change_CO2e_pct = div(
        g_settlement_org_high.change_CO2e_t, l18.g_settlement_org_high.CO2e_total
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
    g_forest.cost_wage = g_forest_managed.cost_wage
    g_forest_managed.demand_emplo = div(
        g_forest_managed.cost_wage, g_forest_managed.ratio_wage_to_emplo
    )
    g_forest.change_CO2e_pct = div(g_forest.change_CO2e_t, l18.g_forest.CO2e_total)
    g_crop.demand_change = div(g_crop.area_ha_change, l18.g_crop.area_ha)
    g_crop.CO2e_total = g_crop.CO2e_pb
    g_crop_min_hum.change_CO2e_t = g_crop_min_hum.CO2e_total
    g_crop_min_hum.cost_climate_saved = (
        (g_crop_min_hum.CO2e_total_2021_estimated - g_crop_min_hum.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop_org.change_CO2e_pct = div(
        g_crop_org.change_CO2e_t, l18.g_crop_org.CO2e_total
    )
    g_crop.demand_emplo = g_crop_org.demand_emplo
    g_crop_org.demand_emplo_new = (
        g_crop_org_low.demand_emplo_new + g_crop_org_high.demand_emplo_new
    )
    g_grass.change_CO2e_pct = div(g_grass.change_CO2e_t, l18.g_grass.CO2e_total)
    g_grass_org.change_CO2e_pct = div(
        g_grass_org.change_CO2e_t, l18.g_grass_org.CO2e_total
    )
    g_grass.demand_emplo = g_grass_org.demand_emplo
    g_grass_org.demand_emplo_new = (
        g_grass_org_low.demand_emplo_new + g_grass_org_high.demand_emplo_new
    )
    g_grove.change_CO2e_pct = div(g_grove.change_CO2e_t, l18.g_grove.CO2e_total)
    g_grove_org.change_CO2e_pct = div(
        g_grove_org.change_CO2e_t, l18.g_grove_org.CO2e_total
    )
    g_grove.demand_emplo = g_grove_org.demand_emplo
    g_water.demand_emplo = g_water_org.demand_emplo
    g_grove_org.demand_emplo_new = (
        g_grove_org_low.demand_emplo_new + g_grove_org_high.demand_emplo_new
    )
    g_wet_org.change_CO2e_pct = div(g_wet_org.change_CO2e_t, l18.g_wet_org.CO2e_total)
    g_wet.demand_emplo = g_wet_org.demand_emplo
    g_wet_org.demand_emplo_new = (
        g_wet_org_low.demand_emplo_new + g_wet_org_high.demand_emplo_new
    )
    g_wood.area_ha = g_forest_managed.area_ha
    g_wood.CO2e_pb_per_t = fact("Fact_L_G_wood_CO2e_per_ha_2018")
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
    g_wet.CO2e_total = g_wet.CO2e_pb
    g_wet_org_rp.change_CO2e_t = g_wet_org_rp.CO2e_total
    g_wet_org_rp.cost_climate_saved = (
        (g_wet_org_rp.CO2e_total_2021_estimated - g_wet_org_rp.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_water.change_CO2e_pct = div(g_water.change_CO2e_t, l18.g_water.CO2e_total)
    g_settlement.change_CO2e_pct = div(
        g_settlement.change_CO2e_t, l18.g_settlement.CO2e_total
    )

    g.cost_wage = (
        g_forest.cost_wage
        + g_crop.cost_wage
        + g_grass.cost_wage
        + g_grove.cost_wage
        + g_wet.cost_wage
    )
    g_forest.demand_emplo = g_forest_managed.demand_emplo
    g_forest_managed.demand_emplo_new = g_forest_managed.demand_emplo
    g_crop.change_CO2e_t = g_crop.CO2e_total - l18.g_crop.CO2e_total
    g_crop.cost_climate_saved = (
        (g_crop.CO2e_total_2021_estimated - g_crop.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_crop.demand_emplo_new = g_crop_org.demand_emplo_new
    g_grass.demand_emplo_new = g_grass_org.demand_emplo_new
    g_grove.demand_emplo_new = g_grove_org.demand_emplo_new
    g_wet.demand_emplo_new = g_wet_org.demand_emplo_new

    g.CO2e_total = g.CO2e_pb + g.CO2e_cb
    g_wet.change_CO2e_t = g_wet.CO2e_total - l18.g_wet.CO2e_total
    g_wet.cost_climate_saved = (
        (g_wet.CO2e_total_2021_estimated - g_wet.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g.demand_emplo = (
        g_forest.demand_emplo
        + g_crop.demand_emplo
        + g_grass.demand_emplo
        + g_grove.demand_emplo
        + g_wet.demand_emplo
    )
    g_forest.demand_emplo_new = g_forest_managed.demand_emplo_new
    g_crop.change_CO2e_pct = div(g_crop.change_CO2e_t, l18.g_crop.CO2e_total)

    g.change_CO2e_t = g.CO2e_total - l18.g.CO2e_total
    g.cost_climate_saved = (
        (g.CO2e_total_2021_estimated - g.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_wet.change_CO2e_pct = div(g_wet.change_CO2e_t, l18.g_wet.CO2e_total)

    g.demand_emplo_new = (
        g_forest.demand_emplo_new
        + g_crop.demand_emplo_new
        + g_grass.demand_emplo_new
        + g_grove.demand_emplo_new
        + g_wet.demand_emplo_new
    )

    g.change_CO2e_pct = div(g.change_CO2e_t, l18.g.CO2e_total)
    g_water.demand_emplo_new = g_water_org.demand_emplo_new
    g_water_org.area_ha_change = (
        g_water_org_low.area_ha_change + g_water_org_high.area_ha_change
    )
    g_water_org.CO2e_total = g_water_org.CO2e_pb
    g_water_org.change_CO2e_t = g_water_org.CO2e_total - l18.g_water_org.CO2e_total
    g_water_org.change_CO2e_pct = div(
        g_water_org.change_CO2e_t, l18.g_water_org.CO2e_total
    )
    g_water_org.CO2e_total_2021_estimated = l18.g_water_org.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_water_org.cost_climate_saved = (
        (g_water_org.CO2e_total_2021_estimated - g_water_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_water_org.cost_wage = 0
    g_water_org.demand_emplo = 0
    g_settlement.cost_wage = g_settlement_org.cost_wage
    g_settlement.demand_emplo = g_settlement_org.demand_emplo
    g_settlement.demand_emplo_new = g_settlement_org.demand_emplo_new
    g_settlement_org.area_ha_change = (
        g_settlement_org_low.area_ha_change + g_settlement_org_high.area_ha_change
    )
    g_settlement_org.area_ha = (
        g_settlement_org_low.area_ha + g_settlement_org_high.area_ha
    )
    g_settlement_org.CO2e_pb = (
        g_settlement_org_low.CO2e_pb + g_settlement_org_high.CO2e_pb
    )
    g_settlement_org.CO2e_total = g_settlement_org.CO2e_pb
    g_settlement_org.change_CO2e_t = (
        g_settlement_org.CO2e_total - l18.g_settlement_org.CO2e_total
    )
    g_settlement_org.change_CO2e_pct = div(
        g_settlement_org.change_CO2e_t, l18.g_settlement_org.CO2e_total
    )
    g_settlement_org.CO2e_total_2021_estimated = l18.g_settlement_org.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_settlement_org.cost_climate_saved = (
        (g_settlement_org.CO2e_total_2021_estimated - g_settlement_org.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_settlement_org.cost_wage = 0
    g_settlement_org.demand_emplo = 0
    g_settlement_org.demand_emplo_new = 0
    g_wood.CO2e_total = g_wood.CO2e_pb
    g_wood.change_CO2e_t = g_wood.CO2e_total - l18.g_wood.CO2e_total
    g_wood.change_CO2e_pct = div(g_wood.change_CO2e_t, l18.g_wood.CO2e_total)
    g_wood.CO2e_total_2021_estimated = l18.g_wood.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )
    g_wood.cost_climate_saved = (
        (g_wood.CO2e_total_2021_estimated - g_wood.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    g_settlement.cost_wage = g_settlement_org.cost_wage
    g_settlement.demand_emplo = g_settlement_org.demand_emplo
    g_settlement.demand_emplo_new = g_settlement_org.demand_emplo_new

    g_wet_org_rp.change_CO2e_pct = 0


def calcPyr(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    pyr = root.l30.pyr
    l = root.l30.l
    g = root.l30.g
    l18 = root.l18

    pyr.CO2e_total = min(
        -(
            root.h30.h.CO2e_total
            + root.e30.e.CO2e_total
            + root.f30.f.CO2e_total
            + root.r30.r.CO2e_total
            + root.b30.b.CO2e_total
            + root.i30.i.CO2e_total
            + root.t30.t.CO2e_total
            + root.a30.a.CO2e_total
            + root.l30.g.CO2e_total
        ),
        0,
    )

    pyr.CO2e_pb = pyr.CO2e_total
    pyr.CO2e_pb_per_t = fact("Fact_L_P_biochar_ratio_CO2e_pb_to_prodvol")
    pyr.prod_volume = div(pyr.CO2e_pb, pyr.CO2e_pb_per_t)

    pyr.change_CO2e_t = pyr.CO2e_pb

    pyr.change_CO2e_pct = 0
    pyr.CO2e_total_2021_estimated = 0

    pyr.cost_climate_saved = (
        (pyr.CO2e_total_2021_estimated - pyr.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )

    pyr.invest_per_x = ass("Ass_L_P_pyrolysis_plant_ratio_invest_to_biochar_pa")
    pyr.invest = pyr.prod_volume * pyr.invest_per_x
    pyr.invest_pa = div(pyr.invest, entry("In_M_duration_target"))
    pyr.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
    pyr.cost_wage = pyr.invest_pa * pyr.pct_of_wage

    pyr.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")
    pyr.demand_emplo = div(pyr.cost_wage, pyr.ratio_wage_to_emplo)
    pyr.demand_emplo_new = pyr.demand_emplo

    l.CO2e_total = g.CO2e_total + pyr.CO2e_total
    l.CO2e_pb = g.CO2e_pb + pyr.CO2e_pb
    l.CO2e_cb = g.CO2e_cb
    l.change_CO2e_t = l.CO2e_total - l18.l.CO2e_total
    l.change_CO2e_pct = div(l.change_CO2e_t, l18.l.CO2e_total)
    l.CO2e_total_2021_estimated = l18.l.CO2e_total * fact(
        "Fact_M_CO2e_lulucf_2021_vs_2018"
    )

    l.cost_climate_saved = (
        (l.CO2e_total_2021_estimated - l.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    l.invest_pa = g.invest_pa + pyr.invest_pa
    l.invest = g.invest + pyr.invest
    l.cost_wage = g.cost_wage + pyr.cost_wage
    l.demand_emplo = g.demand_emplo + pyr.demand_emplo
    l.demand_emplo_new = g.demand_emplo_new + pyr.demand_emplo_new
