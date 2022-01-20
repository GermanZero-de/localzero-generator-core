from .setup import ass, entry, fact
from dataclasses import dataclass, asdict


@dataclass
class LColVars2018:
    area_ha: float = None
    CO2e_pb_per_t: float = None
    pct_x: float = None
    CO2e_pb_per_MWh: float = None
    CO2e_cb_per_t: float = None
    CO2e_cb: float = None
    CO2e_pb: float = None
    CO2e_total: float = None
    cost_certificate: float = None


@dataclass
class L18:
    # Klassenvariablen für L18
    l: LColVars2018 = LColVars2018()
    g: LColVars2018 = LColVars2018()
    g_planning: LColVars2018 = LColVars2018()
    g_forest: LColVars2018 = LColVars2018()
    g_forest_managed: LColVars2018 = LColVars2018()
    g_forest_natural: LColVars2018 = LColVars2018()
    g_crop: LColVars2018 = LColVars2018()
    g_crop_min_conv: LColVars2018 = LColVars2018()
    g_crop_min_hum: LColVars2018 = LColVars2018()
    g_crop_org_low: LColVars2018 = LColVars2018()
    g_crop_org_high: LColVars2018 = LColVars2018()
    g_grass: LColVars2018 = LColVars2018()
    g_grass_min_conv: LColVars2018 = LColVars2018()
    g_grass_org_low: LColVars2018 = LColVars2018()
    g_grass_org_high: LColVars2018 = LColVars2018()
    g_grove: LColVars2018 = LColVars2018()
    g_grove_min: LColVars2018 = LColVars2018()
    g_grove_org_low: LColVars2018 = LColVars2018()
    g_grove_org_high: LColVars2018 = LColVars2018()
    g_wet: LColVars2018 = LColVars2018()
    g_wet_min: LColVars2018 = LColVars2018()
    g_wet_org_low: LColVars2018 = LColVars2018()
    g_wet_org_high: LColVars2018 = LColVars2018()
    g_wet_org_low_r: LColVars2018 = LColVars2018()
    g_wet_org_low_rp: LColVars2018 = LColVars2018()
    g_wet_org_high_r: LColVars2018 = LColVars2018()
    g_wet_org_high_rp: LColVars2018 = LColVars2018()
    g_water: LColVars2018 = LColVars2018()
    g_water_min: LColVars2018 = LColVars2018()
    g_water_min_low: LColVars2018 = LColVars2018()
    g_water_min_high: LColVars2018 = LColVars2018()
    g_settlement: LColVars2018 = LColVars2018()
    g_settlement_min: LColVars2018 = LColVars2018()
    g_settlement_org_low: LColVars2018 = LColVars2018()
    g_settlement_org_high: LColVars2018 = LColVars2018()
    g_other: LColVars2018 = LColVars2018()
    g_wood: LColVars2018 = LColVars2018()

    # erzeuge dictionry

    def dict(self):
        return asdict(self)


def Lulucf2018_calc(root):

    g = root.l18.g
    l = root.l18.l
    g_forest = root.l18.g_forest
    g_forest_managed = root.l18.g_forest_managed
    g_forest_natural = root.l18.g_forest_natural
    g_crop = root.l18.g_crop
    g_crop_min_conv = root.l18.g_crop_min_conv
    g_crop_org_low = root.l18.g_crop_org_low
    g_crop_org_high = root.l18.g_crop_org_high
    g_grass = root.l18.g_grass
    g_grass_min_conv = root.l18.g_grass_min_conv
    g_grass_org_low = root.l18.g_grass_org_low
    g_grass_org_high = root.l18.g_grass_org_high
    g_grove = root.l18.g_grove
    g_grove_min = root.l18.g_grove_min
    g_grove_org_low = root.l18.g_grove_org_low
    g_grove_org_high = root.l18.g_grove_org_high
    g_wet = root.l18.g_wet
    g_wet_min = root.l18.g_wet_min
    g_wet_org_low = root.l18.g_wet_org_low
    g_wet_org_high = root.l18.g_wet_org_high
    g_water = root.l18.g_water
    g_water_min = root.l18.g_water_min
    g_water_min_low = root.l18.g_water_min_low
    g_water_min_high = root.l18.g_water_min_high
    g_settlement = root.l18.g_settlement
    g_settlement_min = root.l18.g_settlement_min
    g_settlement_org_low = root.l18.g_settlement_org_low
    g_settlement_org_high = root.l18.g_settlement_org_high
    g_other = root.l18.g_other
    g_wood = root.l18.g_wood

    try:
        g_forest.area_ha = entry("In_M_area_wood_com")

        g_forest_managed.CO2e_pb_per_t = fact("Fact_L_G_forest_conv_CO2e_per_ha_2018")
        g_forest_managed.CO2e_cb_per_t = fact("Fact_L_G_forest_CO2e_cb_per_ha_2018")
        g_forest_managed.pct_x = fact("Fact_L_G_forest_pct_of_conv_2018")

        g_crop.area_ha = entry("In_M_area_agri_com") * fact("Fact_L_G_factor_crop")
        g_crop_min_conv.CO2e_pb_per_t = fact(
            "Fact_L_G_crop_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_forest_managed.area_ha = g_forest.area_ha * g_forest_managed.pct_x
        g_crop_min_conv.pct_x = fact("Fact_L_G_fraction_minrl_soil_crop")

        g_forest_managed.CO2e_cb = (
            g_forest_managed.CO2e_cb_per_t * g_forest_managed.area_ha
        )
        g_forest_managed.CO2e_pb = (
            g_forest_managed.area_ha * g_forest_managed.CO2e_pb_per_t
        )
        g_forest_natural.CO2e_pb_per_t = fact("Fact_L_G_forest_nature_CO2e_per_ha_2018")
        g_forest_natural.pct_x = fact("Fact_L_G_forest_pct_of_nature_2018")

        g_forest.CO2e_cb = g_forest_managed.CO2e_cb

        g.CO2e_cb = g_forest.CO2e_cb

        g_forest_natural.area_ha = g_forest.area_ha * g_forest_natural.pct_x

        g_forest_natural.CO2e_pb = (
            g_forest_natural.area_ha * g_forest_natural.CO2e_pb_per_t
        )
        g_forest.CO2e_pb = g_forest_managed.CO2e_pb + g_forest_natural.CO2e_pb
        g_forest.CO2e_total = g_forest.CO2e_pb + g_forest.CO2e_cb

        g_crop_min_conv.area_ha = g_crop.area_ha * g_crop_min_conv.pct_x

        g_grass.area_ha = (
            entry("In_M_area_agri_com") * fact("Fact_L_G_factor_crop_to_grass")
            + entry("In_M_area_veg_plant_uncover_com")
            * fact("Fact_L_G_factor_grass_strict")
            + entry("In_M_area_veg_heath_com")
            + entry("In_M_area_veg_marsh_com")
        )
        g_grass_min_conv.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_strict_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_grass_min_conv.pct_x = fact("Fact_L_G_fraction_minrl_soil_grass_strict")
        g_crop_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_crop")

        g_crop_min_conv.CO2e_pb = (
            g_crop_min_conv.CO2e_pb_per_t * g_crop_min_conv.area_ha
        )
        g_crop_org_low.CO2e_pb_per_t = fact("Fact_L_G_crop_fen_CO2e_per_ha_2018")
        g_crop_org_low.area_ha = g_crop.area_ha * g_crop_org_low.pct_x

        g_crop_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_crop")

        g_crop_org_low.CO2e_pb = g_crop_org_low.CO2e_pb_per_t * g_crop_org_low.area_ha
        g_crop_org_high.CO2e_pb_per_t = fact("Fact_L_G_crop_bog_CO2e_per_ha_2018")
        g_crop_org_high.area_ha = g_crop.area_ha * g_crop_org_high.pct_x

        g_crop.pct_x = (
            g_crop_min_conv.pct_x
            +
            # g_crop_min_hum.pct_x +
            g_crop_org_low.pct_x
            + g_crop_org_high.pct_x
        )
        g_crop_org_high.CO2e_pb = (
            g_crop_org_high.CO2e_pb_per_t * g_crop_org_high.area_ha
        )
        g_crop.CO2e_pb = (
            g_crop_min_conv.CO2e_pb
            +
            # g_crop_min_hum.CO2e_pb +
            g_crop_org_low.CO2e_pb
            + g_crop_org_high.CO2e_pb
        )
        g_crop.CO2e_total = g_crop.CO2e_pb

        g_grass_min_conv.area_ha = g_grass.area_ha * g_grass_min_conv.pct_x

        g_grove.area_ha = entry("In_M_area_veg_wood_com")

        g_grove_min.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_woody_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_grove_min.pct_x = fact("Fact_L_G_fraction_minrl_soil_grass_woody")

        g_grass_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_grass_strict")
        g_grass_min_conv.CO2e_pb = (
            g_grass_min_conv.CO2e_pb_per_t * g_grass_min_conv.area_ha
        )
        g_grass_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_strict_org_soil_fen_CO2e_per_ha_2018"
        )
        g_grass_org_low.area_ha = g_grass.area_ha * g_grass_org_low.pct_x

        g_grass_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_grass_strict")
        g_grass_org_low.CO2e_pb = (
            g_grass_org_low.CO2e_pb_per_t * g_grass_org_low.area_ha
        )
        g_grass_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_strict_org_soil_bog_CO2e_per_ha_2018"
        )
        g_grass_org_high.area_ha = g_grass.area_ha * g_grass_org_high.pct_x

        g_grass.pct_x = (
            g_grass_min_conv.pct_x + g_grass_org_low.pct_x + g_grass_org_high.pct_x
        )
        g_grass_org_high.CO2e_pb = (
            g_grass_org_high.CO2e_pb_per_t * g_grass_org_high.area_ha
        )
        g_grass.CO2e_pb = (
            g_grass_min_conv.CO2e_pb
            + g_grass_org_low.CO2e_pb
            + g_grass_org_high.CO2e_pb
        )
        g_grass.CO2e_total = g_grass.CO2e_pb

        g_grove_min.area_ha = g_grove.area_ha * g_grove_min.pct_x
        g_wet.area_ha = entry("In_M_area_veg_moor_com") + entry(
            "In_M_area_water_com"
        ) * fact("Fact_L_G_factor_wetland_peat")
        g_wet_min.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_wet_min.pct_x = fact("Fact_L_G_fraction_minrl_soil_wetland_peat")

        g_grove_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_grass_woody")
        g_grove_min.CO2e_pb = g_grove_min.CO2e_pb_per_t * g_grove_min.area_ha

        g_grove_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_woody_org_soil_fen_CO2e_per_ha_2018"
        )
        g_grove_org_low.area_ha = g_grove.area_ha * g_grove_org_low.pct_x

        g_grove_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_grass_woody")
        g_grove_org_low.CO2e_pb = (
            g_grove_org_low.CO2e_pb_per_t * g_grove_org_low.area_ha
        )
        g_grove_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_grass_woody_org_soil_bog_CO2e_per_ha_2018"
        )
        g_grove_org_high.area_ha = g_grove.area_ha * g_grove_org_high.pct_x
        g_grove.pct_x = (
            g_grove_min.pct_x + g_grove_org_low.pct_x + g_grove_org_high.pct_x
        )
        g_grove_org_high.CO2e_pb = (
            g_grove_org_high.CO2e_pb_per_t * g_grove_org_high.area_ha
        )
        g_grove.CO2e_pb = (
            g_grove_min.CO2e_pb + g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
        )
        g_grove.CO2e_total = g_grove.CO2e_pb

        g_wet_min.area_ha = g_wet.area_ha * g_wet_min.pct_x

        g_water.area_ha = entry("In_M_area_water_com") * fact(
            "Fact_L_G_factor_wetland_water"
        )
        g_water_min.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_minrl_soil_ord_CO2e_per_ha_2018"
        )
        g_water_min.pct_x = fact("Fact_L_G_fraction_minrl_soil_wetland_water")
        g_wet_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_wetland_peat")
        g_wet_min.CO2e_pb = g_wet_min.CO2e_pb_per_t * g_wet_min.area_ha

        g_wet_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_org_soil_fen_CO2e_per_ha_2018"
        )
        g_wet_org_low.area_ha = g_wet.area_ha * g_wet_org_low.pct_x

        g_wet_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_wetland_peat")
        g_wet_org_low.CO2e_pb = g_wet_org_low.CO2e_pb_per_t * g_wet_org_low.area_ha
        g_wet_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_peat_org_soil_bog_CO2e_per_ha_2018"
        )
        g_wet_org_high.area_ha = g_wet.area_ha * g_wet_org_high.pct_x

        g_wet.pct_x = g_wet_min.pct_x + g_wet_org_low.pct_x + g_wet_org_high.pct_x
        g_wet_org_high.CO2e_pb = g_wet_org_high.CO2e_pb_per_t * g_wet_org_high.area_ha
        g_wet.CO2e_pb = (
            g_wet_min.CO2e_pb + g_wet_org_low.CO2e_pb + g_wet_org_high.CO2e_pb
        )
        g_wet.CO2e_total = g_wet.CO2e_pb

        g_water_min.area_ha = g_water.area_ha * g_water_min.pct_x

        g_settlement.area_ha = entry("In_M_area_settlement_com") + entry(
            "In_M_area_transport_com"
        )
        g_settlement_min.CO2e_pb_per_t = fact(
            "Fact_L_G_settl_minrl_soil_CO2e_per_ha_2018"
        )
        g_settlement_min.pct_x = fact("Fact_L_G_fraction_minrl_soil_settl")

        g_water_min_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_wetland_water")
        g_water_min.CO2e_pb = g_water_min.CO2e_pb_per_t * g_water_min.area_ha

        g_water_min_high.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_org_soil_bog_CO2e_per_ha_2018"
        )
        g_water_min_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_wetland_water")
        g_water_min_high.area_ha = g_water.area_ha * g_water_min_high.pct_x

        g_water_min_low.area_ha = g_water.area_ha * g_water_min_low.pct_x

        g_water_min_low.CO2e_pb_per_t = fact(
            "Fact_L_G_wetland_water_org_soil_fen_CO2e_per_ha_2018"
        )
        g_water_min_low.CO2e_pb = (
            g_water_min_low.CO2e_pb_per_t * g_water_min_low.area_ha
        )
        g_water.pct_x = (
            g_water_min.pct_x + g_water_min_low.pct_x + g_water_min_high.pct_x
        )
        g_water_min_high.CO2e_pb = (
            g_water_min_high.CO2e_pb_per_t * g_water_min_high.area_ha
        )
        g_water.CO2e_pb = (
            g_water_min.CO2e_pb + g_water_min_low.CO2e_pb + g_water_min_high.CO2e_pb
        )
        g_water.CO2e_total = g_water.CO2e_pb

        g_settlement_min.area_ha = g_settlement.area_ha * g_settlement_min.pct_x
        g_other.area_ha = entry("In_M_area_veg_plant_uncover_com") * fact(
            "Fact_L_G_factor_other"
        )
        g_other.CO2e_pb_per_t = fact("Fact_L_G_other_minrl_soil_CO2e_per_ha_2018")
        g_other.CO2e_pb = g_other.CO2e_pb_per_t * g_other.area_ha

        g_settlement_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_settl")
        g_settlement_min.CO2e_pb = (
            g_settlement_min.CO2e_pb_per_t * g_settlement_min.area_ha
        )
        g_settlement_org_low.CO2e_pb_per_t = fact(
            "Fact_L_G_settl_org_soil_fen_CO2e_per_ha_2018"
        )
        g_settlement_org_low.area_ha = g_settlement.area_ha * g_settlement_org_low.pct_x
        g_settlement_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_settl")
        g_settlement_org_low.CO2e_pb = (
            g_settlement_org_low.CO2e_pb_per_t * g_settlement_org_low.area_ha
        )
        g_settlement_org_high.CO2e_pb_per_t = fact(
            "Fact_L_G_settl_org_soil_bog_CO2e_per_ha_2018"
        )
        g_settlement_org_high.area_ha = (
            g_settlement.area_ha * g_settlement_org_high.pct_x
        )
        g_settlement.pct_x = (
            g_settlement_min.pct_x
            + g_settlement_org_low.pct_x
            + g_settlement_org_high.pct_x
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
        g_wood.CO2e_pb_per_t = -0.313283  # Todo(fact('Fact_L_G_wood_CO2e_per_ha_2018'))

        g_other.CO2e_total = g_other.CO2e_pb

        g_wood.area_ha = g_forest_managed.area_ha

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
        g_wood.CO2e_total = g_wood.CO2e_pb

        g.CO2e_total = (
            g_forest.CO2e_total
            + g_crop.CO2e_total
            + g_grass.CO2e_total
            + g_grove.CO2e_total
            + g_wet.CO2e_total
            + g_water.CO2e_total
            + g_settlement.CO2e_total
            + g_other.CO2e_total
            + g_wood.CO2e_total
        )

        l.CO2e_pb = g.CO2e_pb
        l.CO2e_cb = g.CO2e_cb
        l.CO2e_total = g.CO2e_total
        g_forest.pct_x = 1.0
        g_forest_managed.CO2e_total = (
            g_forest_managed.CO2e_pb + g_forest_managed.CO2e_cb
        )
        g_forest_natural.CO2e_total = g_forest_natural.CO2e_pb
        g_crop_min_conv.CO2e_total = g_crop_min_conv.CO2e_pb
        g_crop_org_low.CO2e_total = g_crop_org_low.CO2e_pb
        g_crop_org_high.CO2e_total = g_crop_org_high.CO2e_pb
        g_grass_min_conv.CO2e_total = g_grass_min_conv.CO2e_pb
        g_grass_org_low.CO2e_total = g_grass_org_low.CO2e_pb
        g_grass_org_high.CO2e_total = g_grass_org_high.CO2e_pb
        g_grove_min.CO2e_total = g_grove_min.CO2e_pb
        g_grove_org_low.CO2e_total = g_grove_org_low.CO2e_pb
        g_grove_org_high.CO2e_total = g_grove_org_high.CO2e_pb
        g_wet_min.CO2e_total = g_wet_min.CO2e_pb
        g_wet_org_low.CO2e_total = g_wet_org_low.CO2e_pb
        g_wet_org_high.CO2e_total = g_wet_org_high.CO2e_pb
        g_water_min.CO2e_total = g_water_min.CO2e_pb
        g_water_min_low.CO2e_total = g_water_min_low.CO2e_pb
        g_water_min_high.CO2e_total = g_water_min_high.CO2e_pb
        g_settlement_min.CO2e_total = g_settlement_min.CO2e_pb
        g_settlement_org_low.CO2e_total = g_settlement_org_low.CO2e_pb
        g_settlement_org_high.CO2e_total = g_settlement_org_high.CO2e_pb

    except Exception as e:
        print(e)
        raise
