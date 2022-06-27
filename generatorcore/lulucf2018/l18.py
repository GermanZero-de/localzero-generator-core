from dataclasses import dataclass, field

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


@dataclass
class L18:
    l: Vars0 = field(default_factory=Vars0)
    g: Vars1 = field(default_factory=Vars1)
    g_forest: Vars3 = field(default_factory=Vars3)
    g_forest_managed: Vars4 = field(default_factory=Vars4)
    g_forest_natural: Vars5 = field(default_factory=Vars5)
    g_crop: Vars6 = field(default_factory=Vars6)
    g_crop_org: Vars6 = field(default_factory=Vars6)
    g_crop_min_conv: Vars5 = field(default_factory=Vars5)
    g_crop_min_hum: Vars7 = field(default_factory=Vars7)
    g_crop_org_low: Vars5 = field(default_factory=Vars5)
    g_crop_org_high: Vars5 = field(default_factory=Vars5)
    g_grass: Vars6 = field(default_factory=Vars6)
    g_grass_min_conv: Vars5 = field(default_factory=Vars5)
    g_grass_org: Vars6 = field(default_factory=Vars6)
    g_grass_org_low: Vars5 = field(default_factory=Vars5)
    g_grass_org_high: Vars5 = field(default_factory=Vars5)
    g_grove: Vars6 = field(default_factory=Vars6)
    g_grove_min: Vars5 = field(default_factory=Vars5)
    g_grove_org: Vars6 = field(default_factory=Vars6)
    g_grove_org_low: Vars5 = field(default_factory=Vars5)
    g_grove_org_high: Vars5 = field(default_factory=Vars5)
    g_wet: Vars6 = field(default_factory=Vars6)
    g_wet_min: Vars5 = field(default_factory=Vars5)
    g_wet_org: Vars6 = field(default_factory=Vars6)
    g_wet_org_r: Vars7 = field(default_factory=Vars7)
    g_wet_org_low: Vars5 = field(default_factory=Vars5)
    g_wet_org_high: Vars5 = field(default_factory=Vars5)
    g_water: Vars6 = field(default_factory=Vars6)
    g_water_org: Vars6 = field(default_factory=Vars6)
    g_water_min: Vars5 = field(default_factory=Vars5)
    g_water_org_low: Vars5 = field(default_factory=Vars5)
    g_water_org_high: Vars5 = field(default_factory=Vars5)
    g_settlement: Vars6 = field(default_factory=Vars6)
    g_settlement_org: Vars6 = field(default_factory=Vars6)
    g_settlement_min: Vars5 = field(default_factory=Vars5)
    g_settlement_org_low: Vars5 = field(default_factory=Vars5)
    g_settlement_org_high: Vars5 = field(default_factory=Vars5)
    g_other: Vars8 = field(default_factory=Vars8)
    g_wood: Vars8 = field(default_factory=Vars8)
    pyrolysis: Vars7 = field(default_factory=Vars7)
