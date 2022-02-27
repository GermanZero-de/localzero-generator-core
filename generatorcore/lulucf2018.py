from dataclasses import dataclass, asdict, field

from .inputs import Inputs


@dataclass
class LColVars2018:
    area_ha: float = None  # type: ignore
    CO2e_pb_per_t: float = None  # type: ignore
    pct_x: float = None  # type: ignore
    CO2e_pb_per_MWh: float = None  # type: ignore
    CO2e_cb_per_t: float = None  # type: ignore
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    cost_certificate: float = None  # type: ignore


@dataclass
class L18:
    # Klassenvariablen für L18
    l: LColVars2018 = field(default_factory=LColVars2018)
    g: LColVars2018 = field(default_factory=LColVars2018)
    g_planning: LColVars2018 = field(default_factory=LColVars2018)
    g_forest: LColVars2018 = field(default_factory=LColVars2018)
    g_forest_managed: LColVars2018 = field(default_factory=LColVars2018)
    g_forest_natural: LColVars2018 = field(default_factory=LColVars2018)
    g_crop: LColVars2018 = field(default_factory=LColVars2018)
    g_crop_org: LColVars2018 = field(default_factory=LColVars2018)
    g_crop_min_conv: LColVars2018 = field(default_factory=LColVars2018)
    g_crop_min_hum: LColVars2018 = field(default_factory=LColVars2018)
    g_crop_org_low: LColVars2018 = field(default_factory=LColVars2018)
    g_crop_org_high: LColVars2018 = field(default_factory=LColVars2018)
    g_grass: LColVars2018 = field(default_factory=LColVars2018)
    g_grass_min_conv: LColVars2018 = field(default_factory=LColVars2018)
    g_grass_org: LColVars2018 = field(default_factory=LColVars2018)
    g_grass_org_low: LColVars2018 = field(default_factory=LColVars2018)
    g_grass_org_high: LColVars2018 = field(default_factory=LColVars2018)
    g_grove: LColVars2018 = field(default_factory=LColVars2018)
    g_grove_min: LColVars2018 = field(default_factory=LColVars2018)
    g_grove_org: LColVars2018 = field(default_factory=LColVars2018)
    g_grove_org_low: LColVars2018 = field(default_factory=LColVars2018)
    g_grove_org_high: LColVars2018 = field(default_factory=LColVars2018)
    g_wet: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_min: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_r: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_rp: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_low: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_high: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_low_r: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_low_rp: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_high_r: LColVars2018 = field(default_factory=LColVars2018)
    g_wet_org_high_rp: LColVars2018 = field(default_factory=LColVars2018)
    g_water: LColVars2018 = field(default_factory=LColVars2018)
    g_water_org: LColVars2018 = field(default_factory=LColVars2018)
    g_water_min: LColVars2018 = field(default_factory=LColVars2018)
    g_water_org_low: LColVars2018 = field(default_factory=LColVars2018)
    g_water_org_high: LColVars2018 = field(default_factory=LColVars2018)
    g_settlement: LColVars2018 = field(default_factory=LColVars2018)
    g_settlement_org: LColVars2018 = field(default_factory=LColVars2018)
    g_settlement_min: LColVars2018 = field(default_factory=LColVars2018)
    g_settlement_org_low: LColVars2018 = field(default_factory=LColVars2018)
    g_settlement_org_high: LColVars2018 = field(default_factory=LColVars2018)
    g_other: LColVars2018 = field(default_factory=LColVars2018)
    g_wood: LColVars2018 = field(default_factory=LColVars2018)
    pyrolysis: LColVars2018 = field(default_factory=LColVars2018)

    def dict(self):
        return asdict(self)


def calc(inputs: Inputs) -> L18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries

    l18 = L18()

    g = l18.g
    l = l18.l
    g_forest = l18.g_forest
    g_forest_managed = l18.g_forest_managed
    g_forest_natural = l18.g_forest_natural
    g_crop = l18.g_crop
    g_crop_min_conv = l18.g_crop_min_conv
    g_crop_org_low = l18.g_crop_org_low
    g_crop_org_high = l18.g_crop_org_high
    g_grass = l18.g_grass
    g_grass_min_conv = l18.g_grass_min_conv
    g_grass_org_low = l18.g_grass_org_low
    g_grass_org_high = l18.g_grass_org_high
    g_grove = l18.g_grove
    g_grove_min = l18.g_grove_min
    g_grove_org_low = l18.g_grove_org_low
    g_grove_org_high = l18.g_grove_org_high
    g_wet = l18.g_wet
    g_wet_min = l18.g_wet_min
    g_wet_org_low = l18.g_wet_org_low
    g_wet_org_high = l18.g_wet_org_high
    g_wet_org_r = l18.g_wet_org_r
    g_water = l18.g_water
    g_water_org = l18.g_water_org
    g_water_min = l18.g_water_min
    g_settlement = l18.g_settlement
    g_settlement_org = l18.g_settlement_org
    g_settlement_min = l18.g_settlement_min
    g_settlement_org_low = l18.g_settlement_org_low
    g_settlement_org_high = l18.g_settlement_org_high
    g_other = l18.g_other
    g_wood = l18.g_wood
    g_crop_org = l18.g_crop_org
    g_grass_org = l18.g_grass_org
    g_grove_org = l18.g_grove_org
    g_wet_org = l18.g_wet_org
    g_water_org_low = l18.g_water_org_low
    g_water_org_high = l18.g_water_org_high
    pyrolysis = l18.pyrolysis

    g_forest.area_ha = entries.m_area_wood_com

    g_forest_managed.CO2e_pb_per_t = fact("Fact_L_G_forest_conv_CO2e_per_ha_2018")
    g_forest_managed.CO2e_cb_per_t = fact("Fact_L_G_forest_CO2e_cb_per_ha_2018")
    g_forest_managed.pct_x = fact("Fact_L_G_forest_pct_of_conv_2018")

    g_crop.area_ha = entries.m_area_agri_com * fact("Fact_L_G_factor_crop")
    g_crop_min_conv.CO2e_pb_per_t = fact(
        "Fact_L_G_crop_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_forest_managed.area_ha = g_forest.area_ha * g_forest_managed.pct_x
    g_crop_min_conv.pct_x = fact("Fact_L_G_fraction_minrl_soil_crop")

    g_forest_managed.CO2e_cb = g_forest_managed.CO2e_cb_per_t * g_forest_managed.area_ha
    g_forest_managed.CO2e_pb = g_forest_managed.area_ha * g_forest_managed.CO2e_pb_per_t
    g_forest_natural.CO2e_pb_per_t = fact("Fact_L_G_forest_nature_CO2e_per_ha_2018")
    g_forest_natural.pct_x = fact("Fact_L_G_forest_pct_of_nature_2018")

    g_forest.CO2e_cb = g_forest_managed.CO2e_cb

    g.CO2e_cb = g_forest.CO2e_cb

    g_forest_natural.area_ha = g_forest.area_ha * g_forest_natural.pct_x

    g_forest_natural.CO2e_pb = g_forest_natural.area_ha * g_forest_natural.CO2e_pb_per_t
    g_forest.CO2e_pb = g_forest_managed.CO2e_pb + g_forest_natural.CO2e_pb
    g_forest.CO2e_total = g_forest.CO2e_pb + g_forest.CO2e_cb

    g_crop_min_conv.area_ha = g_crop.area_ha * g_crop_min_conv.pct_x

    g_grass.area_ha = (
        entries.m_area_agri_com * fact("Fact_L_G_factor_crop_to_grass")
        + entries.m_area_veg_plant_uncover_com * fact("Fact_L_G_factor_grass_strict")
        + entries.m_area_veg_heath_com
        + entries.m_area_veg_marsh_com
    )
    g_grass_min_conv.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_strict_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_grass_min_conv.pct_x = fact("Fact_L_G_fraction_minrl_soil_grass_strict")
    g_crop_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_crop")

    g_crop_min_conv.CO2e_pb = g_crop_min_conv.CO2e_pb_per_t * g_crop_min_conv.area_ha
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
    g_crop_org_high.CO2e_pb = g_crop_org_high.CO2e_pb_per_t * g_crop_org_high.area_ha
    g_crop.CO2e_pb = (
        g_crop_min_conv.CO2e_pb
        +
        # g_crop_min_hum.CO2e_pb +
        g_crop_org_low.CO2e_pb
        + g_crop_org_high.CO2e_pb
    )
    g_crop.CO2e_total = g_crop.CO2e_pb
    g_crop_org.CO2e_pb = g_crop_org_low.CO2e_pb + g_crop_org_high.CO2e_pb
    g_crop_org.CO2e_total = g_crop_org.CO2e_pb
    g_crop_org.pct_x = g_crop_org_low.pct_x + g_crop_org_high.pct_x
    g_crop_org.area_ha = g_crop_org_low.area_ha + g_crop_org_high.area_ha
    g_grass_min_conv.area_ha = g_grass.area_ha * g_grass_min_conv.pct_x

    g_grove.area_ha = entries.m_area_veg_wood_com
    # g_grove.area_ha = (
    #    entries.m_area_agri_com * fact("Fact_L_G_factor_crop_to_grass")
    #    + entries.m_area_veg_plant_uncover_com * fact("Fact_L_G_factor_grass_strict")
    #    + entries.m_area_veg_heath_com
    #    + entries.m_area_veg_marsh_com
    # )

    g_grove_min.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_woody_minrl_soil_ord_CO2e_per_ha_2018"
    )
    g_grove_min.pct_x = fact("Fact_L_G_fraction_minrl_soil_grass_woody")
    g_grass_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_grass_strict")
    g_grass_min_conv.CO2e_pb = g_grass_min_conv.CO2e_pb_per_t * g_grass_min_conv.area_ha
    g_grass_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_strict_org_soil_fen_CO2e_per_ha_2018"
    )
    g_grass_org_low.area_ha = g_grass.area_ha * g_grass_org_low.pct_x

    g_grass_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_grass_strict")
    g_grass_org_low.CO2e_pb = g_grass_org_low.CO2e_pb_per_t * g_grass_org_low.area_ha
    g_grass_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_strict_org_soil_bog_CO2e_per_ha_2018"
    )
    g_grass_org_high.area_ha = g_grass.area_ha * g_grass_org_high.pct_x

    g_grass.pct_x = (
        g_grass_min_conv.pct_x + g_grass_org_low.pct_x + g_grass_org_high.pct_x
    )
    g_grass_org_high.CO2e_pb = g_grass_org_high.CO2e_pb_per_t * g_grass_org_high.area_ha
    g_grass.CO2e_pb = (
        g_grass_min_conv.CO2e_pb + g_grass_org_low.CO2e_pb + g_grass_org_high.CO2e_pb
    )
    g_grass_org.CO2e_pb = g_grass_org_low.CO2e_pb + g_grass_org_high.CO2e_pb
    g_grass_org.CO2e_total = g_grass_org.CO2e_pb
    g_grass.CO2e_total = g_grass.CO2e_pb
    g_grass_org.pct_x = g_grass_org_low.pct_x + g_grass_org_high.pct_x
    g_grass_org.area_ha = g_grass_org_low.area_ha + g_grass_org_high.area_ha
    g_grove_min.area_ha = g_grove.area_ha * g_grove_min.pct_x
    g_wet.area_ha = entries.m_area_veg_moor_com + entries.m_area_water_com * fact(
        "Fact_L_G_factor_wetland_peat"
    )
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
    g_grove_org_low.CO2e_pb = g_grove_org_low.CO2e_pb_per_t * g_grove_org_low.area_ha
    g_grove_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_grass_woody_org_soil_bog_CO2e_per_ha_2018"
    )
    g_grove_org_high.area_ha = g_grove.area_ha * g_grove_org_high.pct_x
    g_grove.pct_x = g_grove_min.pct_x + g_grove_org_low.pct_x + g_grove_org_high.pct_x
    g_grove_org_high.CO2e_pb = g_grove_org_high.CO2e_pb_per_t * g_grove_org_high.area_ha
    g_grove.CO2e_pb = (
        g_grove_min.CO2e_pb + g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
    )
    g_grove.CO2e_total = g_grove.CO2e_pb
    g_grove_org.pct_x = g_grove_org_low.pct_x + g_grove_org_high.pct_x
    g_grove_org.area_ha = g_grove_org_low.area_ha + g_grove_org_high.area_ha
    g_wet_min.area_ha = g_wet.area_ha * g_wet_min.pct_x

    g_water.area_ha = (
        entries.m_area_agri_com * fact("Fact_L_G_factor_crop_to_grass")
        + entries.m_area_veg_plant_uncover_com * fact("Fact_L_G_factor_grass_strict")
        + entries.m_area_veg_heath_com
        + entries.m_area_veg_marsh_com
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
    g_wet_org.CO2e_pb = g_wet_org_low.CO2e_pb + g_wet_org_high.CO2e_pb
    g_wet_org.CO2e_total = g_wet_org.CO2e_pb
    g_wet.CO2e_pb = g_wet_min.CO2e_pb + g_wet_org_low.CO2e_pb + g_wet_org_high.CO2e_pb
    g_wet.CO2e_total = g_wet.CO2e_pb
    g_wet_org.pct_x = g_wet_org_low.pct_x + g_wet_org_high.pct_x
    g_wet_org.area_ha = g_wet_org_low.area_ha + g_wet_org_high.area_ha
    g_water_min.area_ha = g_water.area_ha * g_water_min.pct_x

    g_settlement.area_ha = (
        entries.m_area_agri_com * fact("Fact_L_G_factor_crop_to_grass")
        + entries.m_area_veg_plant_uncover_com * fact("Fact_L_G_factor_grass_strict")
        + entries.m_area_veg_heath_com
        + entries.m_area_veg_marsh_com
    )
    g_settlement_min.CO2e_pb_per_t = fact("Fact_L_G_settl_minrl_soil_CO2e_per_ha_2018")
    g_settlement_min.pct_x = fact("Fact_L_G_fraction_minrl_soil_settl")
    g_water_min.CO2e_pb = g_water_min.CO2e_pb_per_t * g_water_min.area_ha

    g_water_org_low.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_water_org_soil_fen_CO2e_per_ha_2018"
    )
    g_water_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_wetland_water")
    g_water_org_high.pct_x = fact("Fact_L_G_fraction_org_soil_bog_wetland_water")
    g_water_org.pct_x = g_water_org_low.pct_x + g_water_org_high.pct_x
    g_water.pct_x = g_water_min.pct_x + g_water_org.pct_x
    g_water_org_low.area_ha = g_water.area_ha * g_water_org_low.pct_x
    g_water_org_low.CO2e_pb = g_water_org_low.CO2e_pb_per_t * g_water_org_low.area_ha
    g_water_org_high.CO2e_pb_per_t = fact(
        "Fact_L_G_wetland_water_org_soil_bog_CO2e_per_ha_2018"
    )

    g_water_org_high.area_ha = g_water.area_ha * g_water_org_high.pct_x
    g_water_org_high.CO2e_pb = g_water_org_high.CO2e_pb_per_t * g_water_org_high.area_ha
    g_water_org.CO2e_pb = g_water_org_low.CO2e_pb + g_water_org_high.CO2e_pb
    g_water.CO2e_pb = g_water_min.CO2e_pb + g_water_org.CO2e_pb
    g_water.CO2e_total = g_water.CO2e_pb
    g_water_org.area_ha = g_water_org_low.area_ha + g_water_org_high.area_ha

    g_water_org.CO2e_total = g_water_org.CO2e_pb
    g_settlement_min.area_ha = g_settlement.area_ha * g_settlement_min.pct_x
    g_other.area_ha = entries.m_area_veg_plant_uncover_com * fact(
        "Fact_L_G_factor_other"
    )
    g_other.CO2e_pb_per_t = fact("Fact_L_G_other_minrl_soil_CO2e_per_ha_2018")
    g_other.CO2e_pb = g_other.CO2e_pb_per_t * g_other.area_ha

    g_settlement_org_low.pct_x = fact("Fact_L_G_fraction_org_soil_fen_settl")
    g_settlement_min.CO2e_pb = g_settlement_min.CO2e_pb_per_t * g_settlement_min.area_ha
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
    g_settlement_org_high.area_ha = g_settlement.area_ha * g_settlement_org_high.pct_x
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
    g_settlement_org.pct_x = g_settlement_org_low.pct_x + g_settlement_org_high.pct_x
    g_settlement_org.area_ha = (
        g_settlement_org_low.area_ha + g_settlement_org_high.area_ha
    )
    g_settlement_org.CO2e_pb = (
        g_settlement_org_low.CO2e_pb + g_settlement_org_high.CO2e_pb
    )
    g_settlement_org.CO2e_total = g_settlement_org.CO2e_pb

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
    g_wood.CO2e_pb_per_t = fact("Fact_L_G_wood_CO2e_per_ha_2018")

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
    g_forest_managed.CO2e_total = g_forest_managed.CO2e_pb + g_forest_managed.CO2e_cb
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
    g_water_org_low.CO2e_total = g_water_org_low.CO2e_pb
    g_grove_org.CO2e_pb = g_grove_org_low.CO2e_pb + g_grove_org_high.CO2e_pb
    g_grove_org.CO2e_total = g_grove_org.CO2e_pb
    g_water_org_high.CO2e_total = g_water_org_high.CO2e_pb
    g_settlement_min.CO2e_total = g_settlement_min.CO2e_pb
    g_settlement_org_low.CO2e_total = g_settlement_org_low.CO2e_pb
    g_settlement_org_high.CO2e_total = g_settlement_org_high.CO2e_pb
    pyrolysis.CO2e_total = 0

    g_wet_org_r.CO2e_total = 0
    l18.g_crop_min_hum.CO2e_total = 0

    return l18
