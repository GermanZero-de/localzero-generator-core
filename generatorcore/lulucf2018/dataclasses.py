# pyright: strict
from dataclasses import dataclass


@dataclass(kw_only=True)
class Vars0:
    # Used by l
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars1:
    # Used by g
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars3:
    # Used by g_forest
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4:
    # Used by g_forest_managed
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by g_forest_natural, g_crop_min_conv, g_crop_org_low, g_crop_org_high, g_grass_min_conv, g_grass_org_low, g_grass_org_high, g_grove_min, g_grove_org_low, g_grove_org_high, g_wet_min, g_wet_org_low, g_wet_org_high, g_water_min, g_water_org_low, g_water_org_high, g_settlement_min, g_settlement_org_low, g_settlement_org_high
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6:
    # Used by g_crop, g_crop_org, g_grass, g_grass_org, g_grove, g_grove_org, g_wet, g_wet_org, g_water, g_water_org, g_settlement, g_settlement_org
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore
    pct_x: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7:
    # Used by g_crop_min_hum, g_wet_org_r, pyrolysis
    CO2e_total: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8:
    # Used by g_other, g_wood
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore
