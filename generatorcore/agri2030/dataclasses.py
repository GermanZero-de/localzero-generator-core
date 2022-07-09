# pyright: strict
from dataclasses import dataclass
from typing import Any

from ..utils import div, MILLION
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
class CO2eChangeP:
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

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation: Any,
        CO2e_production_based: float,
        CO2e_total: float,
    ) -> "CO2eChangeP":

        a18_CO2e_total = getattr(a18, what).CO2e_total

        CO2e_total_2021_estimated = a18_CO2e_total * inputs.fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        change_CO2e_t = CO2e_total - a18_CO2e_total
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * inputs.entries.m_duration_neutral
            * inputs.fact("Fact_M_cost_per_CO2e_2020")
        )
        change_CO2e_pct = div(change_CO2e_t, a18_CO2e_total)
        demand_emplo = p_operation.demand_emplo

        invest = p_operation.invest
        invest_pa = invest / inputs.entries.m_duration_target

        demand_emplo_new = p_operation.demand_emplo_new
        energy = p_operation.energy
        cost_wage = p_operation.cost_wage

        return cls(
            CO2e_production_based=CO2e_production_based,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            invest=invest,
            invest_pa=invest_pa,
        )


@dataclass
class CO2eChangeG:
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

    @classmethod
    def calc(cls, g_consult: Any, g_organic: Any) -> "CO2eChangeG":
        CO2e_total = 0
        cost_wage = g_consult.cost_wage + g_organic.cost_wage

        demand_emplo = g_consult.demand_emplo + g_organic.demand_emplo
        demand_emplo_new = g_consult.demand_emplo_new + g_organic.demand_emplo_new
        demand_emplo_com = g_consult.demand_emplo_com

        invest = g_consult.invest + g_organic.invest
        invest_com = g_consult.invest_com
        invest_outside = 0

        invest_pa = g_consult.invest_pa + g_organic.invest_pa
        invest_pa_com = g_consult.invest_pa_com
        invest_pa_outside = 0

        return cls(
            CO2e_total=CO2e_total,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_outside=invest_outside,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_pa_outside=invest_pa_outside,
        )


@dataclass
class CO2eChangeGConsult:
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

    @classmethod
    def calc(cls, inputs: Inputs) -> "CO2eChangeGConsult":
        area_ha_available = inputs.entries.a_farm_amount

        invest_per_x = inputs.ass("Ass_A_G_consult_invest_per_farm")
        invest = area_ha_available * invest_per_x
        invest_com = invest * inputs.ass("Ass_A_G_consult_invest_pct_of_public")
        invest_pa = invest / inputs.entries.m_duration_target
        invest_pa_com = invest_pa * inputs.ass("Ass_A_G_consult_invest_pct_of_public")

        pct_of_wage = inputs.ass("Ass_A_G_consult_invest_pct_of_wage")
        cost_wage = invest_pa * pct_of_wage

        ratio_wage_to_emplo = inputs.ass("Ass_A_G_consult_ratio_wage_to_emplo")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo
        demand_emplo_com = demand_emplo_new

        return cls(
            area_ha_available=area_ha_available,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_com=demand_emplo_com,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class CO2eChangeGOrganic:
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

    @classmethod
    def calc(cls, inputs: Inputs) -> "CO2eChangeGOrganic":
        area_ha_available = inputs.entries.m_area_agri_com

        power_installed = inputs.entries.a_area_agri_com_pct_of_organic
        power_to_be_installed_pct = inputs.ass("Ass_A_G_area_agri_pct_of_organic_2050")
        power_to_be_installed = area_ha_available * (
            power_to_be_installed_pct - power_installed
        )

        invest_per_x = inputs.ass("Ass_A_G_area_agri_organic_ratio_invest_to_ha")
        invest = power_to_be_installed * invest_per_x
        invest_pa = invest / inputs.entries.m_duration_target

        pct_of_wage = inputs.fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        cost_wage = invest_pa * pct_of_wage

        ratio_wage_to_emplo = inputs.fact(
            "Fact_B_P_constr_main_ratio_wage_to_emplo_2017"
        )
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        return cls(
            area_ha_available=area_ha_available,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            power_installed=power_installed,
            power_to_be_installed=power_to_be_installed,
            power_to_be_installed_pct=power_to_be_installed_pct,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


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

        if not what:
            a18_CO2e_total = 0
        else:
            a18_CO2e_total = getattr(a18, what).CO2e_total

        CO2e_total = CO2e_production_based + CO2e_combustion_based
        change_CO2e_t = CO2e_total - a18_CO2e_total
        change_CO2e_pct = div(change_CO2e_t, a18_CO2e_total)

        CO2e_total_2021_estimated = a18_CO2e_total * inputs.fact(
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
class CO2eChangePOperation:
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

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        what: str,
        a18: A18,
        p_operation_vehicles: Any,
        p_operation_heat: Any,
        p_operation_elec_elcon: Any,
        p_operation_elec_heatpump: Any,
    ) -> "CO2eChangePOperation":
        demand_epetrol = p_operation_vehicles.demand_epetrol
        demand_ediesel = p_operation_vehicles.demand_ediesel
        demand_heatpump = p_operation_heat.demand_heatpump
        demand_emplo = p_operation_heat.demand_emplo
        demand_emplo_new = p_operation_heat.demand_emplo_new
        demand_biomass = p_operation_heat.demand_biomass
        demand_electricity = (
            p_operation_elec_elcon.demand_electricity
            + p_operation_elec_heatpump.demand_electricity
        )
        demand_emethan = p_operation_heat.demand_emethan

        energy = (
            p_operation_heat.energy
            + p_operation_elec_elcon.energy
            + p_operation_elec_heatpump.energy
            + p_operation_vehicles.energy
        )

        invest = p_operation_heat.invest
        invest_pa = invest / inputs.entries.m_duration_target
        cost_wage = p_operation_heat.cost_wage

        change_energy_MWh = energy - getattr(a18, what).energy
        change_energy_pct = div(change_energy_MWh, getattr(a18, what).energy)

        return cls(
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_wage=cost_wage,
            demand_biomass=demand_biomass,
            demand_ediesel=demand_ediesel,
            demand_electricity=demand_electricity,
            demand_emethan=demand_emethan,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            demand_epetrol=demand_epetrol,
            demand_heatpump=demand_heatpump,
            energy=energy,
            invest=invest,
            invest_pa=invest_pa,
        )


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
class CO2eChangeFuelOilGas(CO2eChange):
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

    @classmethod
    def calc_fuel(
        cls, inputs: Inputs, what: str, a18: A18, energy: float
    ) -> "CO2eChangeFuelOilGas":
        area_m2 = 0
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
            area_m2=area_m2,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            energy=energy,
        )


@dataclass
class CO2eChangeFuelHeatpump(CO2eChange):
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

    @classmethod
    def calc_fuel(
        cls, inputs: Inputs, what: str, a18: A18, energy: float
    ) -> "CO2eChangeFuelHeatpump":
        CO2e_combustion_based_per_MWh = getattr(a18, what).CO2e_combustion_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        change_energy_MWh = energy - getattr(a18, what).energy

        cost_fuel_per_MWh = inputs.fact("Fact_R_S_gas_energy_cost_factor_2018")
        cost_fuel = energy * cost_fuel_per_MWh / MILLION

        full_load_hour = inputs.fact("Fact_B_S_full_usage_hours_buildings")
        power_installed = div(getattr(a18, what).energy, full_load_hour)
        power_to_be_installed = max(div(energy, full_load_hour) - power_installed, 0)

        invest_per_x = inputs.fact("Fact_R_S_heatpump_cost")
        invest = invest_per_x * power_to_be_installed * 1000
        invest_pa = invest / inputs.entries.m_duration_target

        pct_of_wage = inputs.fact("Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = inputs.fact("Fact_B_P_heating_wage_per_person_per_year")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)

        emplo_existing = (
            inputs.fact("Fact_B_P_install_heating_emplo_2017")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
            * inputs.ass("Ass_B_D_install_heating_emplo_pct_of_A_heatpump")
        )

        demand_emplo_new = max(0, demand_emplo - emplo_existing)

        parent = super().calc(inputs, what, a18, CO2e_combustion_based, 0)

        # override value from parent!
        change_CO2e_pct = div(
            parent.change_CO2e_t, 1.0
        )  # getattr(a18, what).CO2e_total)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            cost_climate_saved=parent.cost_climate_saved,
            change_energy_MWh=change_energy_MWh,
            cost_fuel=cost_fuel,
            cost_fuel_per_MWh=cost_fuel_per_MWh,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            emplo_existing=emplo_existing,
            energy=energy,
            full_load_hour=full_load_hour,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            power_installed=power_installed,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class CO2eChangeFuelEmethan(CO2eChange):
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

    @classmethod
    def calc_fuel(
        cls, inputs: Inputs, a18: A18, energy: float
    ) -> "CO2eChangeFuelEmethan":
        CO2e_combustion_based = 0
        CO2e_combustion_based_per_MWh = inputs.fact(
            "Fact_T_S_methan_EmFa_tank_wheel_2018"
        )

        change_energy_MWh = energy
        demand_emethan = energy

        parent = super().calc(inputs, "", a18, CO2e_combustion_based, 0)

        return cls(
            CO2e_combustion_based=parent.CO2e_combustion_based,
            CO2e_production_based=parent.CO2e_production_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_total=parent.CO2e_total,
            CO2e_total_2021_estimated=parent.CO2e_total_2021_estimated,
            change_CO2e_pct=parent.change_CO2e_pct,
            change_CO2e_t=parent.change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            cost_climate_saved=parent.cost_climate_saved,
            demand_emethan=demand_emethan,
            energy=energy,
        )
