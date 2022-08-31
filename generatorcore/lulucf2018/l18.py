# pyright: strict
from dataclasses import dataclass

from .dataclasses import (
    Vars0,
    Vars1,
    Vars3,
    Vars4,
    Vars5,
    Vars6,
    Vars7,
    Vars8,
)


@dataclass(kw_only=True)
class L18:
    l: Vars0
    g: Vars1
    g_forest: Vars3
    g_forest_managed: Vars4
    g_forest_natural: Vars5
    g_crop: Vars6
    g_crop_org: Vars6
    g_crop_min_conv: Vars5
    g_crop_min_hum: Vars7
    g_crop_org_low: Vars5
    g_crop_org_high: Vars5
    g_grass: Vars6
    g_grass_min_conv: Vars5
    g_grass_org: Vars6
    g_grass_org_low: Vars5
    g_grass_org_high: Vars5
    g_grove: Vars6
    g_grove_min: Vars5
    g_grove_org: Vars6
    g_grove_org_low: Vars5
    g_grove_org_high: Vars5
    g_wet: Vars6
    g_wet_min: Vars5
    g_wet_org: Vars6
    g_wet_org_r: Vars7
    g_wet_org_low: Vars5
    g_wet_org_high: Vars5
    g_water: Vars6
    g_water_org: Vars6
    g_water_min: Vars5
    g_water_org_low: Vars5
    g_water_org_high: Vars5
    g_settlement: Vars6
    g_settlement_org: Vars6
    g_settlement_min: Vars5
    g_settlement_org_low: Vars5
    g_settlement_org_high: Vars5
    g_other: Vars8
    g_wood: Vars8
    pyrolysis: Vars7
