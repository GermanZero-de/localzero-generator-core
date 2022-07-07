# pyright: strict
from dataclasses import dataclass
from typing import Any

from ..utils import div
from ..agri2018.a18 import A18
from ..inputs import Inputs


@dataclass
class Vars0:
    # Used by a
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


@dataclass
class Vars1:
    # Used by p
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore


@dataclass
class Vars2:
    # Used by g
    CO2e_total: float = None  # type: ignore
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


@dataclass
class Vars3:
    # Used by g_consult
    area_ha_available: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars4:
    # Used by g_organic
    area_ha_available: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    power_to_be_installed_pct: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class CO2eChange:
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        CO2e_combustion_based: float,
        CO2e_production_based: float,
    ) -> "CO2eChange":
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        change_CO2e_t = CO2e_total - getattr(a18, what).CO2e_total
        change_CO2e_pct = div(change_CO2e_t, getattr(a18, what).CO2e_total)

        CO2e_total_2021_estimated = getattr(a18, what).CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            cost_climate_saved=cost_climate_saved,
        )


@dataclass
class CO2eChangeFermentationOrManure(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    amount: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_change: float = None  # type: ignore

    @classmethod
    def calc_fermen(
        cls, inputs: Inputs, what: str, ass_demand_change: str, a18: A18
    ) -> "CO2eChangeFermentationOrManure":
        demand_change = inputs.ass(ass_demand_change)
        amount = getattr(a18, what).amount * (1 + demand_change)

        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t
        CO2e_production_based = amount * CO2e_production_based_per_t

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            amount=amount,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )

    @classmethod
    def calc_manure(
        cls, inputs: Inputs, what: str, a18: A18, amount: float
    ) -> "CO2eChangeFermentationOrManure":
        demand_change = inputs.ass("Ass_A_P_manure_ratio_CO2e_to_amount_change")

        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t * (
            1 + demand_change
        )
        CO2e_production_based = amount * CO2e_production_based_per_t

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            amount=amount,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
        )


@dataclass
class CO2eChangeSoil(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    area_ha: float = None  # type: ignore
    area_ha_change: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_change: float = None  # type: ignore

    @classmethod
    def calc_soil_grazing(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        area_ha: float,
        p_fermen_dairycow: Any,
        p_fermen_nondairy: Any,
        p_fermen_oanimal: Any,
    ) -> "CO2eChangeSoil":

        CO2e_production_based_per_t = div(
            getattr(a18, what).CO2e_production_based_per_t
            * (
                p_fermen_dairycow.amount
                + p_fermen_nondairy.amount
                + p_fermen_oanimal.amount
            ),
            a18.p_fermen_dairycow.amount
            + a18.p_fermen_nondairy.amount
            + a18.p_fermen_oanimal.amount,
        )

        demand_change = (
            div(
                CO2e_production_based_per_t,
                getattr(a18, what).CO2e_production_based_per_t,
            )
            - 1
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
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
    def calc_soil_residue(
        cls, inputs: Inputs, what: str, a18: A18, area_ha: float
    ) -> "CO2eChangeSoil":
        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t
        demand_change = (
            div(
                CO2e_production_based_per_t,
                getattr(a18, what).CO2e_production_based_per_t,
            )
            - 1
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
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
        cls, inputs: Inputs, what: str, a18: A18, area_ha: float
    ) -> "CO2eChangeSoil":
        demand_change = inputs.ass("Ass_A_P_soil_N_application_2030_change")
        CO2e_production_based_per_t = getattr(a18, what).CO2e_production_based_per_t * (
            1 + demand_change
        )

        CO2e_production_based = area_ha * CO2e_production_based_per_t

        area_ha_change = -(getattr(a18, what).area_ha - area_ha)

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
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


@dataclass
class CO2eChangeOtherLiming(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    prod_volume: float = None  # type: ignore

    @classmethod
    def calc_other_liming(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        prod_volume: float,
        CO2e_production_based: float,
    ) -> "CO2eChangeOtherLiming":

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            prod_volume=prod_volume,
        )


@dataclass
class CO2eChangeOther(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    prod_volume: float = None  # type: ignore

    @classmethod
    def calc_other(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        ass_demand_change: str,
        fact_production_based_per_t: str,
    ) -> "CO2eChangeOther":

        demand_change = inputs.ass(ass_demand_change)
        prod_volume = getattr(a18, what).prod_volume * (1 + demand_change)

        CO2e_production_based_per_t = inputs.fact(fact_production_based_per_t)
        CO2e_production_based = prod_volume * CO2e_production_based_per_t

        parent = super().calc(inputs, what, a18, 0, CO2e_production_based)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            demand_change=demand_change,
            prod_volume=prod_volume,
        )


@dataclass
class Vars10:
    # Used by p_operation
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore


@dataclass
class Vars11:
    # Used by p_operation_heat
    area_m2: float = None  # type: ignore
    area_m2_nonrehab: float = None  # type: ignore
    area_m2_rehab: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_heat_nonrehab: float = None  # type: ignore
    demand_heat_rehab: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    fec_factor_averaged: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_nonrehab: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    pct_rehab: float = None  # type: ignore
    rate_rehab_pa: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars12:
    # Used by p_operation_elec_elcon
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars13:
    # Used by p_operation_elec_heatpump
    change_energy_MWh: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars14:
    # Used by p_operation_vehicles
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    demand_biomass: float = None  # type: ignore
    demand_change: float = None  # type: ignore
    demand_ediesel: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    demand_epetrol: float = None  # type: ignore
    demand_heatpump: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars15:
    # Used by s
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
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore


@dataclass
class CO2eChangeFuel(CO2eChange):
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore

    @classmethod
    def calc_fuel(
        cls, inputs: Inputs, what: str, a18: A18, energy: float
    ) -> "CO2eChangeFuel":
        CO2e_combustion_based_per_MWh = getattr(a18, what).CO2e_combustion_based_per_MWh

        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh
        change_energy_MWh = energy - getattr(a18, what).energy
        change_energy_pct = div(change_energy_MWh, getattr(a18, what).energy)

        parent = super().calc(inputs, what, a18, CO2e_combustion_based, 0)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            energy=energy,
        )


@dataclass
class Vars17:
    # Used by s_fueloil, s_gas
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    area_m2: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars18:
    # Used by s_heatpump
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars19:
    # Used by s_emethan
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    demand_emethan: float = None  # type: ignore
    energy: float = None  # type: ignore
