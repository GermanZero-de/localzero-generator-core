# pyright: strict

from dataclasses import dataclass

from ..common.g import G
from ..common.co2_emission import CO2eEmission
from ..common.invest import InvestCommune

from .energy_production import TotalHeatProduction
from .energy_production.dataclasses import CO2eChange


@dataclass(kw_only=True)
class H(CO2eEmission, InvestCommune, CO2eChange):
    demand_emplo_com: float

    @classmethod
    def of_p_and_g(cls, p: TotalHeatProduction, g: G) -> "H":
        return cls(
            CO2e_combustion_based=p.CO2e_combustion_based,
            CO2e_production_based=p.CO2e_production_based,
            CO2e_total=p.CO2e_total,
            CO2e_total_2021_estimated=p.CO2e_total_2021_estimated,
            change_CO2e_pct=p.change_CO2e_pct,
            change_CO2e_t=p.change_CO2e_t,
            change_energy_MWh=p.change_energy_MWh,
            change_energy_pct=p.change_energy_pct,
            cost_climate_saved=p.cost_climate_saved,
            cost_wage=g.cost_wage + p.cost_wage,
            demand_emplo=g.demand_emplo + p.demand_emplo,
            demand_emplo_new=g.demand_emplo_new + p.demand_emplo_new,
            invest=g.invest + p.invest,
            invest_com=g.invest_com + p.invest_com,
            invest_pa=g.invest_pa + p.invest_pa,
            invest_pa_com=g.invest_pa_com + p.invest_pa_com,
            demand_emplo_com=g.demand_emplo_com,  # TODO: Check demand_emplo_new in Heat with Hauke
        )
