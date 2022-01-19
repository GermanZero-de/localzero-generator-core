from setup import *
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


@dataclass
class L30:
    # Klassenvariablen für L18
    L: LColVars2030 = LColVars2030()
    e: LColVars2030 = LColVars2030()
    g: LColVars2030 = LColVars2030()
    g_forest: LColVars2030 = LColVars2030()
    g_forest_managed: LColVars2030 = LColVars2030()
    g_forest_natural: LColVars2030 = LColVars2030()
    g_crop: LColVars2030 = LColVars2030()
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
    g_water_min_low: LColVars2030 = LColVars2030()
    g_water_min_high: LColVars2030 = LColVars2030()
    g_settlement: LColVars2030 = LColVars2030()
    g_settlement_min: LColVars2030 = LColVars2030()
    g_settlement_org_low: LColVars2030 = LColVars2030()
    g_settlement_org_high: LColVars2030 = LColVars2030()
    g_other: LColVars2030 = LColVars2030()
    g_wood: LColVars2030 = LColVars2030()
    pyrolysis: LColVars2030 = LColVars2030()
    g_planning: LColVars2030 = LColVars2030()
    # erzeuge dictionry

    def dict(self):
        return asdict(self)


def Lulucf2030_calc(root):
    l18 = root.l18
    L = root.l30.L
    e = root.l30.e
    g = root.l30.g
    g_forest = root.l30.g_forest
    g_forest_managed = root.l30.g_forest_managed
    g_forest_natural = root.l30.g_forest_natural
    g_crop = root.l30.g_crop
    g_crop_min_conv = root.l30.g_crop_min_conv
    g_crop_min_hum = root.l30.g_crop_min_hum
    g_crop_org_low = root.l30.g_crop_org_low
    g_crop_org_high = root.l30.g_crop_org_high
    g_grass = root.l30.g_grass
    g_grass_min_conv = root.l30.g_grass_min_conv
    g_grass_org_low = root.l30.g_grass_org_low
    g_grass_org_high = root.l30.g_grass_org_high
    g_grove = root.l30.g_grove
    g_grove_min = root.l30.g_grove_min
    g_grove_org_low = root.l30.g_grove_org_low
    g_grove_org_high = root.l30.g_grove_org_high
    g_wet = root.l30.g_wet
    g_wet_min = root.l30.g_wet_min
    g_wet_org_low = root.l30.g_wet_org_low
    g_wet_org_high = root.l30.g_wet_org_high
    g_wet_org_low_r = root.l30.g_wet_org_low_r
    g_wet_org_low_rp = root.l30.g_wet_org_low_rp
    g_wet_org_high_r = root.l30.g_wet_org_high_r
    g_wet_org_high_rp = root.l30.g_wet_org_high_rp
    g_water = root.l30.g_water
    g_water_min = root.l30.g_water_min
    g_water_min_low = root.l30.g_water_min_low
    g_water_min_high = root.l30.g_water_min_high
    g_settlement = root.l30.g_settlement
    g_settlement_min = root.l30.g_settlement_min
    g_settlement_org_low = root.l30.g_settlement_org_low
    g_settlement_org_high = root.l30.g_settlement_org_high
    g_other = root.l30.g_other
    g_wood = root.l30.g_wood
    pyrolysis = root.l30.pyrolysis

    try:

        g_forest_managed.CO2e_pb_per_t = (
            ass('Ass_L_G_forest_conv_CO2e_per_ha_2050')
        )
        g_forest_managed.demand_change = ass('Ass_L_G_forest_conv_pct_change')
        g_forest_managed.area_ha_change = (
            l18.g_forest_managed.area_ha *
            g_forest_managed.demand_change
        )
        g_forest.CO2e_cb_per_t = (fact('Fact_L_G_forest_CO2e_cb_per_ha_203X'))

        g_forest_managed.area_ha = (
            l18.g_forest_managed.area_ha +
            g_forest_managed.area_ha_change
        )
        g_forest_managed.CO2e_pb = (
            g_forest_managed.CO2e_pb_per_t *
            g_forest_managed.area_ha
        )
        g_forest_managed.invest_per_x = (
            ass('Ass_L_G_forest_afforestation_invest_per_ha_2020')
        )
        g_crop_min_conv.demand_change = (
            ass('Ass_L_G_crop_organic_matter_pct_2050')
        )
        g_crop_min_conv.CO2e_pb_per_t = (
            fact('Fact_L_G_crop_minrl_soil_ord_CO2e_per_ha_2018')
        )
        g_forest_natural.CO2e_pb_per_t = (
            fact('Fact_L_G_forest_nature_CO2e_per_ha_2018')
        )
        g_forest.CO2e_cb = (g_forest_managed.area_ha * g_forest.CO2e_cb_per_t)
        g_forest_natural.demand_change = (
            ass('Ass_L_G_forest_nature_pct_change')
        )
        g_forest_natural.area_ha_change = (
            l18.g_forest_natural.area_ha *
            g_forest_natural.demand_change
        )
        g_crop_org_low.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_forest_natural.area_ha = (
            l18.g_forest_natural.area_ha +
            g_forest_natural.area_ha_change
        )
        g.CO2e_cb = g_forest.CO2e_cb
        g_forest_natural.CO2e_pb = (
            g_forest_natural.CO2e_pb_per_t *
            g_forest_natural.area_ha
        )
        g_forest.CO2e_pb = (
            g_forest_managed.CO2e_pb +
            g_forest_natural.CO2e_pb
        )
        g_forest.CO2e_total = (g_forest.CO2e_cb + g_forest.CO2e_pb)
        g_forest_managed.area_ha_available_pct_of_action = (
            ass('Ass_L_G_forest_conv_dead_pct_2018') /
            ass('Ass_L_G_forest_conv_pct_2050')
        )
        g_forest_managed.area_ha_available = (
            g_forest_managed.area_ha *
            g_forest_managed.area_ha_available_pct_of_action
        )
        g_forest_managed.invest = (
            g_forest_managed.area_ha_available *
            g_forest_managed.invest_per_x
        )
        g_forest.invest = g_forest_managed.invest
        g_forest.change_CO2e_t = (
            g_forest.CO2e_total -
            l18.g_forest.CO2e_total
        )
        g_crop_min_conv.area_ha_change = (
            l18.g_crop_min_conv.area_ha * (g_crop_min_conv.demand_change)
        )
        g_forest.area_ha = (
            g_forest_managed.area_ha +
            g_forest_natural.area_ha
        )
        g_crop_min_conv.area_ha = (
            l18.g_crop_min_conv.area_ha +
            g_crop_min_conv.area_ha_change
        )
        g_crop_min_conv.CO2e_pb = (
            g_crop_min_conv.CO2e_pb_per_t *
            g_crop_min_conv.area_ha
        )
        g_crop_min_hum.CO2e_pb_per_t = (
            fact('Fact_L_G_crop_minrl_soil_sust_CO2e_per_ha_203X')
        )
        g_crop_min_hum.area_ha_change = 0

        g_grass_min_conv.demand_change = (ass('Ass_L_G_no_LUC_203X')
                                          )
        g_grass_min_conv.CO2e_pb_per_t = (
            fact('Fact_L_G_grass_strict_minrl_soil_ord_CO2e_per_ha_2018')
        )
        g_crop_min_hum.area_ha = g_crop_min_hum.area_ha_change
        g_crop_min_hum.CO2e_pb = (
            g_crop_min_hum.CO2e_pb_per_t *
            g_crop_min_hum.area_ha
        )
        g_grass_org_low.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_crop_org_low.CO2e_pb_per_t = (
            fact('Fact_L_G_crop_fen_CO2e_per_ha_2018')
        )
        g_crop_org_low.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_crop_org_low.area_ha_change = (
            l18.g_crop_org_low.area_ha *
            g_crop_org_low.demand_change
        )
        g_crop_org_low.area_ha = (
            l18.g_crop_org_low.area_ha +
            g_crop_org_low.area_ha_change
        )
        g_crop_org_low.CO2e_pb = (
            g_crop_org_low.CO2e_pb_per_t *
            g_crop_org_low.area_ha
        )
        g_crop_org_high.CO2e_pb_per_t = (
            fact('Fact_L_G_crop_bog_CO2e_per_ha_2018')
        )
        g_crop_org_high.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_crop_org_high.area_ha_change = (
            l18.g_crop_org_high.area_ha *
            g_crop_org_high.demand_change
        )
        g_crop_org_high.area_ha = (
            l18.g_crop_org_high.area_ha +
            g_crop_org_high.area_ha_change
        )
        g_crop_org_high.CO2e_pb = (
            g_crop_org_high.CO2e_pb_per_t *
            g_crop_org_high.area_ha
        )
        g_crop.CO2e_pb = (
            g_crop_min_conv.CO2e_pb +
            g_crop_min_hum.CO2e_pb +
            g_crop_org_low.CO2e_pb +
            g_crop_org_high.CO2e_pb
        )
        g_crop_org_low.to_wet_low = g_crop_org_low.area_ha_change

        g_crop.CO2e_total = g_crop.CO2e_pb

        g_crop.change_CO2e_t = (g_crop.CO2e_total - l18.g_crop.CO2e_total)

        g_grass_min_conv.area_ha_change = (
            l18.g_grass_min_conv.area_ha * (g_grass_min_conv.demand_change)
        )
        g_crop_org_high.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_crop_org_low.invest = (
            - g_crop_org_low.area_ha_change *
            g_crop_org_low.invest_per_x
        )
        g_crop.area_ha = (
            g_crop_min_conv.area_ha +
            g_crop_min_hum.area_ha +
            g_crop_org_low.area_ha +
            g_crop_org_high.area_ha
        )
        g_crop.area_ha_change = (g_crop.area_ha - l18.g_crop.area_ha)

        g_crop_org_high.to_wet_high = g_crop_org_high.area_ha_change

        g_crop.demand_change = (g_crop.area_ha_change / l18.g_crop.area_ha)

        g_grass_min_conv.area_ha = (
            l18.g_grass_min_conv.area_ha +
            g_grass_min_conv.area_ha_change
        )
        g_grass_min_conv.CO2e_pb = (
            g_grass_min_conv.CO2e_pb_per_t *
            g_grass_min_conv.area_ha
        )
        g_crop_org_high.invest = (
            - g_crop_org_high.area_ha_change *
            g_crop_org_high.invest_per_x
        )
        g_crop.invest = (
            g_crop_org_low.invest +
            g_crop_org_high.invest +
            g_crop_org_high.invest
        )
        g_grass_org_low.CO2e_pb_per_t = (
            fact('Fact_L_G_grass_strict_org_soil_fen_CO2e_per_ha_2018')
        )
        g_grass_org_low.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_grove_min.demand_change = (ass('Ass_L_G_no_LUC_203X'))

        g_grove_min.CO2e_pb_per_t = (
            fact('Fact_L_G_grass_woody_minrl_soil_ord_CO2e_per_ha_2018')
        )
        g_grass_org_low.area_ha_change = (
            l18.g_grass_org_low.area_ha * (g_grass_org_low.demand_change)
        )
        g_grass_org_low.area_ha = (
            l18.g_grass_org_low.area_ha +
            g_grass_org_low.area_ha_change
        )
        g_grove_org_low.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_grass_org_low.CO2e_pb = (
            g_grass_org_low.CO2e_pb_per_t *
            g_grass_org_low.area_ha
        )
        g_grass_org_high.CO2e_pb_per_t = (
            fact('Fact_L_G_grass_strict_org_soil_bog_CO2e_per_ha_2018')
        )
        g_grass_org_high.demand_change = (ass('Ass_L_G_area_rewetting_2050'))
        g_grass_org_high.area_ha_change = (
            l18.g_grass_org_high.area_ha * (g_grass_org_high.demand_change)
        )
        g_grass_org_high.area_ha = (
            l18.g_grass_org_high.area_ha +
            g_grass_org_high.area_ha_change
        )
        g_grass_org_high.CO2e_pb = (
            g_grass_org_high.CO2e_pb_per_t *
            g_grass_org_high.area_ha
        )
        g_grass.CO2e_pb = (
            g_grass_min_conv.CO2e_pb +
            g_grass_org_low.CO2e_pb +
            g_grass_org_high.CO2e_pb
        )
        g_grass_org_low.to_wet_low = g_grass_org_low.area_ha_change

        g_grass.CO2e_total = g_grass.CO2e_pb

        g_grass.change_CO2e_t = (g_grass.CO2e_total - l18.g_grass.CO2e_total)

        g_grove_min.area_ha_change = (
            l18.g_grove_min.area_ha * (g_grove_min.demand_change)
        )
        g_grass_org_high.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_grass_org_low.invest = (
            - g_grass_org_low.area_ha_change *
            g_grass_org_low.invest_per_x
        )
        g_grass.area_ha = (
            g_grass_min_conv.area_ha +
            g_grass_org_low.area_ha +
            g_grass_org_high.area_ha
        )
        g_grass.area_ha_change = (g_grass.area_ha - l18.g_grass.area_ha)

        g_grass_org_high.to_wet_high = g_grass_org_high.area_ha_change

        g_grass.demand_change = (g_grass.area_ha_change / l18.g_grass.area_ha)

        g_grove_min.area_ha = (
            l18.g_grove_min.area_ha +
            g_grove_min.area_ha_change
        )
        g_grove_min.CO2e_pb = (g_grove_min.CO2e_pb_per_t * g_grove_min.area_ha)

        g_grass_org_high.invest = (
            - g_grass_org_high.area_ha_change *
            g_grass_org_high.invest_per_x
        )
        g_grass.invest = (g_grass_org_low.invest + g_grass_org_high.invest)

        g_wet_min.demand_change = (ass('Ass_L_G_no_LUC_203X'))

        g_wet_min.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_peat_minrl_soil_ord_CO2e_per_ha_2018')
        )
        g_grove_org_high.CO2e_pb_per_t = (
            fact('Fact_L_G_grass_woody_org_soil_bog_CO2e_per_ha_2018')
        )
        g_grove_org_high.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_wet_org_high.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_grove_org_high.area_ha_change = (
            l18.g_grove_org_high.area_ha * (g_grove_org_high.demand_change)
        )
        g_grove_org_high.area_ha = (
            l18.g_grove_org_high.area_ha +
            g_grove_org_high.area_ha_change
        )
        g_grove_org_low.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_grove_org_high.CO2e_pb = (
            g_grove_org_high.CO2e_pb_per_t *
            g_grove_org_high.area_ha
        )
        g_grove_org_low.area_ha_change = (
            l18.g_grove_org_low.area_ha * (g_grove_org_low.demand_change)
        )
        g_grove_org_low.area_ha = (
            l18.g_grove_org_low.area_ha +
            g_grove_org_low.area_ha_change
        )
        g_grove_org_low.CO2e_pb_per_t = (
            fact('Fact_L_G_grass_woody_org_soil_fen_CO2e_per_ha_2018')
        )
        g_grove_org_low.to_wet_low = g_grove_org_low.area_ha_change

        g_grove_org_low.CO2e_pb = (
            g_grove_org_low.CO2e_pb_per_t *
            g_grove_org_low.area_ha
        )
        g_grove.CO2e_pb = (
            g_grove_min.CO2e_pb +
            g_grove_org_low.CO2e_pb +
            g_grove_org_high.CO2e_pb
        )
        g_grove.CO2e_total = g_grove.CO2e_pb

        g_grove_org_high.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_grove_org_low.invest = (
            - g_grove_org_low.area_ha_change *
            g_grove_org_low.invest_per_x
        )
        g_grove.change_CO2e_t = (g_grove.CO2e_total - l18.g_grove.CO2e_total)

        g_wet_min.area_ha_change = (
            l18.g_wet_min.area_ha * (g_wet_min.demand_change)
        )
        g_grove_org_high.to_wet_high = g_grove_org_high.area_ha_change

        g_grove.area_ha = (
            g_grove_min.area_ha +
            g_grove_org_low.area_ha +
            g_grove_org_high.area_ha
        )
        g_wet_min.area_ha = (l18.g_wet_min.area_ha + g_wet_min.area_ha_change)

        g_wet_min.CO2e_pb = (g_wet_min.CO2e_pb_per_t * g_wet_min.area_ha)

        g_grove_org_high.invest = (
            - g_grove_org_high.area_ha_change *
            g_grove_org_high.invest_per_x
        )
        g_grove.invest = (g_grove_org_low.invest + g_grove_org_high.invest)
        g_water_min.demand_change = (ass('Ass_L_G_no_LUC_203X'))
        g_water_min.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_water_minrl_soil_ord_CO2e_per_ha_2018')
        )
        g_wet_org_low_r.CO2e_pb_per_t = (
            fact('Fact_L_G_fen_wet_CO2e_per_ha_203X')
        )
        g_wet_org_low.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_wet_org_high.demand_change = (ass('Ass_L_G_area_rewetting_2050'))

        g_wet_org_low.area_ha_change = (
            l18.g_wet_org_low.area_ha * (g_wet_org_low.demand_change)
        )
        g_wet_org_low.to_wet_low = g_wet_org_low.area_ha_change
        g_wet_org_low_r.area_ha_change = (
            - (g_crop_org_low.to_wet_low + g_grass_org_low.to_wet_low +
               g_grove_org_low.to_wet_low + g_wet_org_low.to_wet_low)
        )
        g_wet_org_low_r.area_ha = g_wet_org_low_r.area_ha_change

        g_wet_org_low_r.CO2e_pb = (
            g_wet_org_low_r.CO2e_pb_per_t *
            g_wet_org_low_r.area_ha
        )
        g_wet_org_high_r.CO2e_pb_per_t = (
            fact('Fact_L_G_bog_wet_CO2e_per_ha_203X')
        )
        g_wet_org_high.area_ha_change = (
            l18.g_wet_org_high.area_ha * (g_wet_org_high.demand_change)
        )
        g_wet_org_high.to_wet_high = g_wet_org_high.area_ha_change

        g_wet_org_low.area_ha = (
            l18.g_wet_org_low.area_ha +
            g_wet_org_low.area_ha_change
        )
        g_wet_org_low.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_peat_org_soil_fen_CO2e_per_ha_2018')
        )
        g_wet_org_low.CO2e_pb = (
            g_wet_org_low.CO2e_pb_per_t *
            g_wet_org_low.area_ha
        )
        g_wet_org_low.invest_per_x = (
            ass('Ass_L_G_wet_rewetting_invest_per_ha_2016')
        )
        g_wet_org_low.invest = (
            - g_wet_org_low.area_ha_change *
            g_wet_org_low.invest_per_x
        )
        g_wet_org_high_r.area_ha_change = (
            - (g_crop_org_high.to_wet_high + g_grass_org_high.to_wet_high +
               g_grove_org_high.to_wet_high + g_wet_org_high.to_wet_high)
        )
        g_wet_org_high.invest = (
            - g_wet_org_high.area_ha_change *
            g_wet_org_high.invest_per_x
        )
        g_wet_org_high_r.area_ha = g_wet_org_high_r.area_ha_change

        g_wet_org_high.area_ha = (
            l18.g_wet_org_high.area_ha +
            g_wet_org_high.area_ha_change
        )
        g_wet_org_high.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_peat_org_soil_bog_CO2e_per_ha_2018')
        )
        g_wet_org_high.CO2e_pb = (
            g_wet_org_high.CO2e_pb_per_t *
            g_wet_org_high.area_ha)
        g_wet_org_low_rp.invest_per_x = (
            ass('Ass_L_G_wet_paludi_invest_per_ha_2016')
        )
        g_wet_org_low_rp.invest = (- 0 * g_wet_org_low_rp.invest_per_x)

        g_wet_org_high_r.CO2e_pb = (
            g_wet_org_high_r.CO2e_pb_per_t *
            g_wet_org_high_r.area_ha
        )
        g_wet.CO2e_pb = (
            g_wet_min.CO2e_pb +
            g_wet_org_low_r.CO2e_pb +
            g_wet_org_high_r.CO2e_pb
        )
        g_wet.CO2e_total = g_wet.CO2e_pb

        g_wet.change_CO2e_t = (g_wet.CO2e_total - l18.g_wet.CO2e_total)

        g_wet_org_low_rp.pct_x = (ass('Ass_L_G_wet_paludi_pct_2012'))

        g_wet_org_low_rp.area_ha = (
            g_wet_org_low_r.area_ha *
            g_wet_org_low_rp.pct_x
        )
        g_wet_org_low_rp.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_peat_org_soil_paludi_CO2e_per_ha_203X')
        )
        g_wet_org_low_rp.CO2e_pb = (
            g_wet_org_low_rp.CO2e_pb_per_t *
            g_wet_org_low_rp.area_ha
        )
        g_wet_org_high_rp.invest_per_x = (
            ass('Ass_L_G_wet_paludi_invest_per_ha_2016')
        )
        g_wet_org_high_rp.invest = (- 0 * g_wet_org_high_rp.invest_per_x)

        g_water_min.area_ha_change = (
            l18.g_water_min.area_ha * (g_water_min.demand_change)
        )
        g_wet.area_ha = (
            g_wet_min.area_ha +
            g_wet_org_low_r.area_ha +
            g_wet_org_high_r.area_ha
        )
        g_water_min.area_ha = (
            l18.g_water_min.area_ha +
            g_water_min.area_ha_change
        )
        g_water_min.CO2e_pb = (g_water_min.CO2e_pb_per_t * g_water_min.area_ha)

        g_wet_org_high_rp.pct_x = (ass('Ass_L_G_wet_paludi_pct_2012'))

        g_wet_org_high_rp.area_ha = (
            g_wet_org_high_r.area_ha *
            g_wet_org_high_rp.pct_x
        )
        g_wet_org_high_rp.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_peat_org_soil_paludi_CO2e_per_ha_203X')
        )
        g_wet_org_high_rp.CO2e_pb = (
            g_wet_org_high_rp.CO2e_pb_per_t *
            g_wet_org_high_rp.area_ha
        )
        g_wet.invest = (
            g_wet_org_high.invest +
            g_wet_org_low_rp.invest +
            g_wet_org_high_rp.invest
        )
        g.invest = (
            g_forest.invest +
            g_crop.invest +
            g_grass.invest +
            g_grove.invest +
            g_wet.invest
        )
        g_settlement_min.demand_change = (ass('Ass_L_G_no_LUC_203X'))

        g_settlement_min.CO2e_pb_per_t = (
            fact('Fact_L_G_settl_minrl_soil_no_LUC_CO2e_per_ha_203X')
        )
        g_water_min_low.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_water_org_soil_fen_CO2e_per_ha_2018')
        )
        g_water_min_low.demand_change = (ass('Ass_L_G_no_LUC_203X'))

        g_water_min_low.area_ha_change = (
            l18.g_water_min_low.area_ha * (g_water_min_low.demand_change)
        )
        g_water_min_low.area_ha = (
            l18.g_water_min_low.area_ha +
            g_water_min_low.area_ha_change)
        g_water_min_low.CO2e_pb = (
            g_water_min_low.CO2e_pb_per_t *
            g_water_min_low.area_ha
        )
        g_water_min_high.CO2e_pb_per_t = (
            fact('Fact_L_G_wetland_water_org_soil_bog_CO2e_per_ha_2018')
        )
        g_water_min_high.demand_change = ass('Ass_L_G_no_LUC_203X')

        g_water_min_high.area_ha_change = (
            l18.g_water_min_high.area_ha * (g_water_min_high.demand_change)
        )
        g_water_min_high.area_ha = (
            l18.g_water_min_high.area_ha +
            g_water_min_high.area_ha_change
        )
        g_water_min_high.CO2e_pb = (
            g_water_min_high.CO2e_pb_per_t *
            g_water_min_high.area_ha
        )
        g_water.CO2e_pb = (
            g_water_min.CO2e_pb +
            g_water_min_low.CO2e_pb +
            g_water_min_high.CO2e_pb
        )
        g_water.CO2e_total = g_water.CO2e_pb

        g_water.change_CO2e_t = (g_water.CO2e_total - l18.g_water.CO2e_total)

        g_settlement_min.area_ha_change = (
            l18.g_settlement_min.area_ha * (g_settlement_min.demand_change)
        )
        g_water.area_ha = (
            g_water_min.area_ha +
            g_water_min_low.area_ha +
            g_water_min_high.area_ha
        )
        g_settlement_min.area_ha = (
            l18.g_settlement_min.area_ha +
            g_settlement_min.area_ha_change
        )
        g_settlement_min.CO2e_pb = (
            g_settlement_min.CO2e_pb_per_t *
            g_settlement_min.area_ha
        )
        g_other.demand_change = (ass('Ass_L_G_no_LUC_203X')
                                 )
        g_other.CO2e_pb_per_t = (
            fact('Fact_L_G_other_minrl_soil_CO2e_per_ha_2018')
        )
        g_settlement_org_low.CO2e_pb_per_t = (
            fact('Fact_L_G_settl_org_soil_fen_CO2e_per_ha_2018')
        )
        g_settlement_org_low.demand_change = (
            ass('Ass_L_G_settl_rewetting_2050')
        )
        g_settlement_org_low.area_ha_change = (
            l18.g_settlement_org_low.area_ha * (g_settlement_org_low.demand_change)
        )
        g_settlement_org_low.area_ha = (
            l18.g_settlement_org_low.area_ha +
            g_settlement_org_low.area_ha_change
        )
        g_settlement_org_low.CO2e_pb = (
            g_settlement_org_low.CO2e_pb_per_t *
            g_settlement_org_low.area_ha
        )
        g_settlement_org_high.CO2e_pb_per_t = (
            fact('Fact_L_G_settl_org_soil_bog_CO2e_per_ha_2018')
        )
        g_settlement_org_high.demand_change = (
            ass('Ass_L_G_settl_rewetting_2050')
        )
        g_settlement_org_high.area_ha_change = (
            l18.g_settlement_org_high.area_ha * (g_settlement_org_high.demand_change)
        )
        g_settlement_org_high.area_ha = (
            l18.g_settlement_org_high.area_ha +
            g_settlement_org_high.area_ha_change
        )
        g_settlement_org_high.CO2e_pb = (
            g_settlement_org_high.CO2e_pb_per_t *
            g_settlement_org_high.area_ha
        )
        g_settlement.CO2e_pb = (
            g_settlement_min.CO2e_pb +
            g_settlement_org_low.CO2e_pb +
            g_settlement_org_high.CO2e_pb
        )
        g_settlement.CO2e_total = g_settlement.CO2e_pb

        g_settlement.change_CO2e_t = (
            g_settlement.CO2e_total -
            l18.g_settlement.CO2e_total
        )
        g_other.area_ha = ((1 + g_other.demand_change) * l18.g_other.area_ha)

        g_settlement.area_ha = (
            g_settlement_min.area_ha +
            g_settlement_org_low.area_ha +
            g_settlement_org_high.area_ha
        )
        g_other.CO2e_pb = (g_other.CO2e_pb_per_t * g_other.area_ha)

        g_wood.CO2e_pb_per_t = (fact('Fact_L_G_wood_CO2e_per_ha_2018'))

        g_wood.area_ha = g_forest_managed.area_ha

        g_other.area_ha_change = (
            l18.g_other.area_ha * (g_other.demand_change)
        )
        g.area_ha = (
            g_forest.area_ha +
            g_crop.area_ha +
            g_grass.area_ha +
            g_grove.area_ha +
            g_wet.area_ha +
            g_water.area_ha +
            g_settlement.area_ha +
            g_other.area_ha
        )
        g_wood.CO2e_pb = (g_wood.CO2e_pb_per_t * g_wood.area_ha)

        g.CO2e_pb = (
            g_forest.CO2e_pb +
            g_crop.CO2e_pb +
            g_grass.CO2e_pb +
            g_grove.CO2e_pb +
            g_wet.CO2e_pb +
            g_water.CO2e_pb +
            g_settlement.CO2e_pb +
            g_other.CO2e_pb +
            g_wood.CO2e_pb
        )
        g_other.CO2e_total = g_other.CO2e_pb

        g_other.change_CO2e_t = (g_other.CO2e_total - l18.g_other.CO2e_total)

        g.CO2e_total = (g.CO2e_pb + g.CO2e_cb)

        pyrolysis.CO2e_total = 0  # Todo: not defined in Excel

        L.CO2e_total = (g.CO2e_total + pyrolysis.CO2e_total)

        g.change_CO2e_t = (g.CO2e_total - l18.g.CO2e_total)

        g_wood.CO2e_total = g_wood.CO2e_pb

        g_wood.change_CO2e_t = (g_wood.CO2e_total - l18.g_wood.CO2e_total)

    except Exception as e:
        print(e)
        raise
