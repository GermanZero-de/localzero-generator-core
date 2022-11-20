# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import div
from ..common.g import G


@dataclass(kw_only=True)
class GConsult(G):
    emplo_existing: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(cls, inputs: Inputs) -> "GConsult":
        ass = inputs.ass
        entries = inputs.entries

        invest_pa = (
            ass("Ass_I_G_advice_invest_pa_per_capita") * entries.m_population_com_2018
        )
        invest_pa_com = invest_pa
        invest = invest_pa * entries.m_duration_target
        invest_com = invest

        pct_of_wage = ass("Ass_I_G_advice_invest_pct_of_wage")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = ass("Ass_T_C_yearly_costs_per_planer")

        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        emplo_existing = 0

        demand_emplo_new = demand_emplo - emplo_existing
        demand_emplo_com = demand_emplo_new

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            emplo_existing=emplo_existing,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass(kw_only=True)
class Vars2:
    # Used by i
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars3:
    # Used by p
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_heatnet: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4:
    # Used by p_miner
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
    # Used by p_miner_cement, p_miner_chalk, p_chem_basic, p_chem_other
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6:
    # Used by p_miner_glas, p_chem_ammonia, p_metal_steel_secondary
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars7:
    # Used by p_miner_ceram, p_metal_nonfe
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars8:
    # Used by p_chem
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9:
    # Used by p_metal
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars10:
    # Used by p_metal_steel
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars11:
    # Used by p_metal_steel_primary
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_hydrogen: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars12:
    # Used by p_other
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_heatnet: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars13:
    # Used by p_other_paper, p_other_food
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_t: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_heatnet: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars14:
    # Used by p_other_further
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_heatnet: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    prod_volume: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars15:
    # Used by p_other_2efgh
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars16:
    # Used by s, s_fossil_gas, s_fossil_coal, s_fossil_diesel, s_fossil_fueloil, s_fossil_lpg, s_fossil_opetpro, s_fossil_ofossil, s_renew, s_renew_hydrogen, s_renew_emethan, s_renew_biomass, s_renew_heatnet, s_renew_heatpump, s_renew_solarth, s_renew_elec
    energy: float
