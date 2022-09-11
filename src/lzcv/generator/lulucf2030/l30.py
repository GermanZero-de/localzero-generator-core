# pyright: strict

from dataclasses import dataclass

from .dataclasses import LColVars2030


@dataclass(kw_only=True)
class L30:
    l: LColVars2030
    g: LColVars2030
    g_forest: LColVars2030
    g_forest_managed: LColVars2030
    g_forest_natural: LColVars2030
    g_crop: LColVars2030
    g_crop_org: LColVars2030
    g_crop_min_conv: LColVars2030
    g_crop_min_hum: LColVars2030
    g_crop_org_low: LColVars2030
    g_crop_org_high: LColVars2030
    g_grass: LColVars2030
    g_grass_min_conv: LColVars2030
    g_grass_org_low: LColVars2030
    g_grass_org_high: LColVars2030
    g_grove: LColVars2030
    g_grove_min: LColVars2030
    g_grove_org: LColVars2030
    g_grove_org_low: LColVars2030
    g_grove_org_high: LColVars2030
    g_wet: LColVars2030
    g_wet_min: LColVars2030
    g_wet_org_low: LColVars2030
    g_wet_org_high: LColVars2030
    g_wet_org_low_r: LColVars2030
    g_wet_org_low_rp: LColVars2030
    g_wet_org_high_r: LColVars2030
    g_wet_org_high_rp: LColVars2030
    g_water: LColVars2030
    g_water_min: LColVars2030
    g_water_org: LColVars2030
    g_settlement: LColVars2030
    g_settlement_org: LColVars2030
    g_settlement_min: LColVars2030
    g_settlement_org_low: LColVars2030
    g_settlement_org_high: LColVars2030
    g_other: LColVars2030
    g_wood: LColVars2030
    pyr: LColVars2030
    g_planning: LColVars2030
    g_grass_org: LColVars2030
    g_wet_org: LColVars2030
    g_wet_org_r: LColVars2030
    g_wet_org_rp: LColVars2030
    g_water_org_low: LColVars2030
    g_water_org_high: LColVars2030
