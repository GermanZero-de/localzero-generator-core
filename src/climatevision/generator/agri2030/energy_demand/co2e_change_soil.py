# pyright: strict

from dataclasses import dataclass

from ...agri2018.a18 import A18
from ...entries import Entries
from ...refdata import Assumptions, Facts
from ...utils import div
from .co2e_change_agri import CO2eChangeAgri


@dataclass(kw_only=True)
class CO2eChangeSoil(CO2eChangeAgri):
    CO2e_production_based_per_t: float = 0
    area_ha: float = 0
    area_ha_change: float = 0
    demand_change: float = 0

    @classmethod
    def calc_soil_special(
        cls,
        facts: Facts,
        entries: Entries,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
        area_ha: float,
        CO2e_production_based_per_t: float,
    ) -> "CO2eChangeSoil":
        CO2e_combustion_based = 0

        demand_change = (
            div(
                CO2e_production_based_per_t,
                getattr(a18, what).CO2e_production_based_per_t,
            )
            - 1
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = CO2eChangeAgri(
            facts=facts,
            entries=entries,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
        )

        return cls(
            facts=facts,
            entries=entries,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            area_ha=area_ha,
            area_ha_change=area_ha_change,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )

    @classmethod
    def calc_soil(
        cls,
        facts: Facts,
        entries: Entries,
        assumptions: Assumptions,
        duration_CO2e_neutral_years: float,
        what: str,
        a18: A18,
        area_ha: float,
    ) -> "CO2eChangeSoil":
        ass = assumptions.ass

        CO2e_combustion_based = 0

        demand_change = ass("Ass_A_P_soil_N_application_2030_change")
        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t * (
            1 + demand_change
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = CO2eChangeAgri(
            facts=facts,
            entries=entries,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
        )

        return cls(
            facts=facts,
            entries=entries,
            duration_CO2e_neutral_years=duration_CO2e_neutral_years,
            what=what,
            a18=a18,
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            area_ha=area_ha,
            area_ha_change=area_ha_change,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )
