# pyright: strict

from dataclasses import dataclass

from climatevision.generator.inputs import Inputs

from ..inputs import Inputs
from ..utils import div


@dataclass(kw_only=True)
class FossilFuelsProduction:
    """This describes energy produced by fossil fuels. Which we do not do in 2030, so this
    just describes the effect of shutting those energy providers down."""

    energy: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_combustion_based: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_cost_mro: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore

    @classmethod
    def sum(
        cls,
        *ffs: "FossilFuelsProduction",
        energy_18: float,
        CO2e_total_18: float,
    ) -> "FossilFuelsProduction":
        energy = sum(ff.energy for ff in ffs)
        CO2e_total_2021_estimated = sum(ff.CO2e_total_2021_estimated for ff in ffs)
        cost_fuel = sum(ff.cost_fuel for ff in ffs)
        cost_mro = sum(ff.cost_mro for ff in ffs)
        CO2e_combustion_based = sum(ff.CO2e_combustion_based for ff in ffs)
        change_cost_energy = sum(ff.change_cost_energy for ff in ffs)
        change_cost_mro = sum(ff.change_cost_mro for ff in ffs)
        cost_climate_saved = sum(ff.cost_climate_saved for ff in ffs)
        change_CO2e_t = sum(ff.change_CO2e_t for ff in ffs)

        change_energy_MWh = energy - energy_18

        return FossilFuelsProduction(
            energy=energy,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=div(change_energy_MWh, energy_18),
            cost_fuel=cost_fuel,
            cost_mro=cost_mro,
            CO2e_combustion_based=CO2e_combustion_based,
            change_cost_energy=change_cost_energy,
            change_cost_mro=change_cost_mro,
            cost_climate_saved=cost_climate_saved,
            change_CO2e_t=change_CO2e_t,
            change_CO2e_pct=div(change_CO2e_t, CO2e_total_18),
        )


@dataclass(kw_only=True)
class Energy:
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyDemand(Energy):
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore


@dataclass(kw_only=True)
class RenewableGeothermalProduction(EnergyDemand):
    """Energy production using geothermal."""

    energy_installable: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_combustion_based: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed_pct: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    power_installable: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_cost_mro: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    pct_x: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore


@dataclass(kw_only=True)
class EnergyDemandWithCostFuel(EnergyDemand):
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore


# Definition der relevanten Spaltennamen für den Sektor E
@dataclass(kw_only=True)
class EColVars2030(EnergyDemandWithCostFuel):
    pet_sites: float = None  # type: ignore
    energy_installable: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    mro_per_MWh: float = None  # type: ignore
    mro: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_combustion_based: float = None  # type: ignore
    cost_certificate_per_MWh: float = None  # type: ignore
    cost_certificate: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_mro: float = None  # type: ignore
    cost_mro_pa_com: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_com: float = None  # type: ignore
    power_installed: float = None  # type: ignore
    power_to_be_installed_pct: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    power_installable: float = None  # type: ignore
    area_ha_available: float = None  # type: ignore
    area_ha_available_pct_of_action: float = None  # type: ignore
    ratio_power_to_area_ha: float = None  # type: ignore
    cost_mro_pa: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_cost_energy: float = None  # type: ignore
    change_cost_mro: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    pct_x: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    cost_mro_per_MWh: float = None  # type: ignore
    emplo_existing: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    lifecycle: float = None  # type: ignore


def calc_biomass(inputs: Inputs) -> EColVars2030:
    fact = inputs.fact
    ass = inputs.ass
    entries = inputs.entries

    p_local_biomass = EColVars2030()

    p_local_biomass.full_load_hour = fact("Fact_E_P_biomass_full_load_hours")

    p_local_biomass.power_installed = entries.e_PV_power_inst_biomass
    p_local_biomass.power_to_be_installed_pct = (
        entries.e_PV_power_to_be_inst_local_biomass
    )

    p_local_biomass.power_installable = entries.e_biomass_local_power_installable_sta
    p_local_biomass.power_to_be_installed = max(
        0,
        p_local_biomass.power_installable * p_local_biomass.power_to_be_installed_pct
        - p_local_biomass.power_installed,
    )
    p_local_biomass.energy = (
        (p_local_biomass.power_to_be_installed + p_local_biomass.power_installed)
        * p_local_biomass.full_load_hour
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )

    return p_local_biomass


def calc_biomass_cogen(
    inputs: Inputs, *, p_local_biomass: EColVars2030
) -> EColVars2030:
    fact = inputs.fact

    p_local_biomass_cogen = EColVars2030()

    p_local_biomass_cogen.energy = p_local_biomass.energy * fact(
        "Fact_E_P_renew_cogen_ratio_2018"
    )

    return p_local_biomass_cogen


def calc_production_renewable_geothermal(
    inputs: Inputs,
    *,
    d_energy: float,
) -> RenewableGeothermalProduction:
    ass = inputs.ass
    fact = inputs.fact
    entries = inputs.entries

    Kalkulationszeitraum = entries.m_duration_target

    CO2e_total = 0
    invest = 0
    demand_emplo = 0
    cost_mro_per_MWh = ass("Ass_E_P_renew_geoth_mro_per_MWh")
    CO2e_combustion_based_per_MWh = fact(
        "Fact_E_P_climate_neutral_ratio_CO2e_cb_to_fec"
    )
    invest_per_x = ass("Ass_E_P_renew_geoth_invest") * 1000
    pct_of_wage = ass("Ass_E_P_constr_plant_invest_pct_of_wage_2017")
    ratio_wage_to_emplo = ass("Ass_E_P_constr_elec_ratio_wage_to_emplo_2017")
    emplo_existing = 0
    power_installable = ass("Ass_E_P_renew_geoth_power_installable")
    power_to_be_installed_pct = ass("Ass_E_P_renew_geoth_power_to_be_installed_2035")
    power_installed = fact("Fact_E_P_geoth_power_installed_2018")
    full_load_hour = fact("Fact_E_P_geoth_full_load_hours")

    invest_pa = invest / Kalkulationszeitraum
    demand_emplo_new = max(0, demand_emplo - emplo_existing)
    power_to_be_installed = max(
        0,
        power_installable * power_to_be_installed_pct - power_installed,
    )
    energy_installable = (
        full_load_hour
        * power_installable
        * (1 - ass("Ass_E_P_renew_loss_brutto_to_netto"))
    )
    invest_outside = invest * d_energy / ass("Ass_E_P_renew_nep_total_2035")
    cost_wage = invest_pa * pct_of_wage
    invest_pa_outside = (
        power_to_be_installed
        * invest_per_x
        / Kalkulationszeitraum
        * d_energy
        / ass("Ass_E_P_renew_nep_total_2035")
    )
    change_CO2e_pct = 0
    cost_climate_saved = 0

    # For now the below are actually computed at a later stage
    # TODO: Figure out if we can move the calculations up
    energy = 0
    CO2e_combustion_based = 0
    cost_mro = 0
    change_energy_MWh = 0
    change_energy_pct = 0
    change_CO2e_t = 0
    change_cost_mro = 0
    pct_x = 0
    return RenewableGeothermalProduction(
        energy=energy,
        energy_installable=energy_installable,
        CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
        CO2e_combustion_based=CO2e_combustion_based,
        cost_climate_saved=cost_climate_saved,
        cost_mro=cost_mro,
        CO2e_total=CO2e_total,
        demand_emplo=demand_emplo,
        power_installed=power_installed,
        power_to_be_installed_pct=power_to_be_installed_pct,
        power_to_be_installed=power_to_be_installed,
        power_installable=power_installable,
        change_energy_MWh=change_energy_MWh,
        change_energy_pct=change_energy_pct,
        change_CO2e_t=change_CO2e_t,
        change_CO2e_pct=change_CO2e_pct,
        change_cost_mro=change_cost_mro,
        invest=invest,
        invest_pa=invest_pa,
        invest_outside=invest_outside,
        invest_pa_outside=invest_pa_outside,
        invest_per_x=invest_per_x,
        pct_of_wage=pct_of_wage,
        pct_x=pct_x,
        ratio_wage_to_emplo=ratio_wage_to_emplo,
        cost_wage=cost_wage,
        cost_mro_per_MWh=cost_mro_per_MWh,
        emplo_existing=emplo_existing,
        demand_emplo_new=demand_emplo_new,
        full_load_hour=full_load_hour,
    )
