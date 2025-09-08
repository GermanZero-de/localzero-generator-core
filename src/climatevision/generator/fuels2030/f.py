# pyright: strict

from dataclasses import dataclass

from ..common.invest import Invest

from .energy_production import TotalEFuelProduction


@dataclass(kw_only=True)
class F(Invest):
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_year_before_baseline_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    invest_outside: float
    invest_pa_outside: float

    @classmethod
    def of_p(cls, p: TotalEFuelProduction) -> "F":
        return cls(
            CO2e_total_year_before_baseline_estimated=p.CO2e_total_year_before_baseline_estimated,
            CO2e_production_based=p.CO2e_production_based,
            CO2e_total=p.CO2e_total,
            change_energy_MWh=p.change_energy_MWh,
            change_CO2e_t=p.change_CO2e_t,
            cost_climate_saved=p.cost_climate_saved,
            change_energy_pct=p.change_energy_pct,
            change_CO2e_pct=p.change_CO2e_pct,
            invest=p.invest,
            invest_pa=p.invest_pa,
            invest_outside=p.invest_outside,
            invest_pa_outside=p.invest_pa_outside,
            cost_wage=p.cost_wage,
            demand_emplo=p.demand_emplo,
            demand_emplo_new=p.demand_emplo_new,
        )
