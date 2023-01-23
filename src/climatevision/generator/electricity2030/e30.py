# pyright: strict

from dataclasses import dataclass

from .electricity2030_core import (
    EColVars2030,
    EnergyDemand,
    EnergyDemandWithCostFuel,
    FossilFuelsProduction,
    RenewableGeothermalProduction,
    Energy,
)


@dataclass(kw_only=True)
class E30:
    e: EColVars2030
    g: EColVars2030
    g_grid_offshore: EColVars2030
    g_grid_onshore: EColVars2030
    g_grid_pv: EColVars2030
    d: EnergyDemand
    d_r: EnergyDemandWithCostFuel
    d_b: EnergyDemandWithCostFuel
    d_h: EnergyDemand
    d_i: EnergyDemandWithCostFuel
    d_t: EnergyDemandWithCostFuel
    d_a: EnergyDemandWithCostFuel
    d_w: EnergyDemand
    d_f_hydrogen_reconv: EnergyDemand
    d_f_wo_hydrogen: EnergyDemand
    p: EColVars2030
    p_fossil_and_renew: EColVars2030
    p_fossil: FossilFuelsProduction
    # We treat nuclear like another fossil fuel (that is a energy source we should stop
    # using). Different countries have made other decisions but for Germany this seems
    # like the only solution currently plausible to be actually implemented (because
    # the political consensus to exit nuclear is very very high).
    p_fossil_nuclear: FossilFuelsProduction
    p_fossil_coal_brown: FossilFuelsProduction
    p_fossil_coal_black: FossilFuelsProduction
    p_fossil_gas: FossilFuelsProduction
    p_fossil_ofossil: FossilFuelsProduction
    p_renew: EColVars2030
    p_renew_pv: EColVars2030
    p_renew_pv_roof: EColVars2030
    p_renew_pv_facade: EColVars2030
    p_renew_pv_park: EColVars2030
    p_renew_pv_agri: EColVars2030
    p_renew_wind: EColVars2030
    p_renew_wind_onshore: EColVars2030
    p_renew_wind_offshore: EColVars2030
    p_renew_biomass: EColVars2030
    p_renew_geoth: RenewableGeothermalProduction
    p_renew_hydro: EColVars2030
    p_renew_reverse: EColVars2030

    p_local: EColVars2030
    p_local_pv: EColVars2030
    p_local_pv_roof: EColVars2030
    p_local_pv_facade: EColVars2030
    p_local_pv_park: EColVars2030
    p_local_pv_agri: EColVars2030
    p_local_wind_onshore: EColVars2030
    p_local_biomass: EColVars2030
    p_local_biomass_cogen: EColVars2030
    p_local_hydro: EColVars2030
    p_local_surplus: Energy
