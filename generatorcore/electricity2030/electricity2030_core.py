from dataclasses import dataclass, field

from ..inputs import Inputs


@dataclass
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


@dataclass
class EnergyDemand:
    energy: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore


@dataclass
class RenewableGeothermalProduction:
    """Energy production using geothermal."""

    energy: float = None  # type: ignore
    energy_installable: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
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
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
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


@dataclass
class EnergyDemandWithCostFuel(EnergyDemand):
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore


# Definition der relevanten Spaltennamen für den Sektor E
@dataclass
class EColVars2030:
    energy: float = None  # type: ignore
    pet_sites: float = None  # type: ignore
    energy_installable: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
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
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
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


# Definition der Zeilennamen für den Sektor E
@dataclass
class E30:
    # Klassenvariablen für E
    e: EColVars2030 = field(default_factory=EColVars2030)
    g: EColVars2030 = field(default_factory=EColVars2030)
    g_grid_offshore: EColVars2030 = field(default_factory=EColVars2030)
    g_grid_onshore: EColVars2030 = field(default_factory=EColVars2030)
    g_grid_pv: EColVars2030 = field(default_factory=EColVars2030)
    d: EnergyDemand = field(default_factory=EnergyDemand)
    d_r: EnergyDemandWithCostFuel = field(default_factory=EnergyDemandWithCostFuel)
    d_b: EnergyDemandWithCostFuel = field(default_factory=EnergyDemandWithCostFuel)
    d_h: EnergyDemand = field(default_factory=EnergyDemand)
    d_i: EnergyDemandWithCostFuel = field(default_factory=EnergyDemandWithCostFuel)
    d_t: EnergyDemandWithCostFuel = field(default_factory=EnergyDemandWithCostFuel)
    d_a: EnergyDemandWithCostFuel = field(default_factory=EnergyDemandWithCostFuel)
    d_f_hydrogen_reconv: EColVars2030 = field(default_factory=EColVars2030)
    d_e_hydrogen: EColVars2030 = field(default_factory=EColVars2030)
    d_e_hydrogen_local: EColVars2030 = field(default_factory=EColVars2030)
    d_f_wo_hydrogen: EColVars2030 = field(default_factory=EColVars2030)
    p: EColVars2030 = field(default_factory=EColVars2030)
    p_fossil_and_renew: EColVars2030 = field(default_factory=EColVars2030)
    p_fossil: EColVars2030 = field(default_factory=EColVars2030)
    # We treat nuclear like another fossil fuel (that is a energy source we should stop
    # using). Different countries have made other decisions but for Germany this seems
    # like the only solution currently plausible to be actually implemented (because
    # the political consensus to exit nuclear is very very high).
    p_fossil_nuclear: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_coal_brown: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_coal_brown_cogen: EColVars2030 = field(default_factory=EColVars2030)
    p_fossil_coal_black: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_coal_black_cogen: EColVars2030 = field(default_factory=EColVars2030)
    p_fossil_gas: FossilFuelsProduction = field(default_factory=FossilFuelsProduction)
    p_fossil_gas_cogen: EColVars2030 = field(default_factory=EColVars2030)
    p_fossil_ofossil: FossilFuelsProduction = field(
        default_factory=FossilFuelsProduction
    )
    p_fossil_ofossil_cogen: EColVars2030 = field(default_factory=EColVars2030)
    p_renew: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_pv: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_pv_roof: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_pv_facade: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_pv_park: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_pv_agri: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_wind: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_wind_onshore: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_wind_offshore: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_biomass: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_biomass_waste: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_biomass_solid: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_biomass_gaseous: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_biomass_cogen: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_geoth: RenewableGeothermalProduction = field(
        default_factory=RenewableGeothermalProduction
    )
    p_renew_hydro: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_geoth_local: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_hydro_local: EColVars2030 = field(default_factory=EColVars2030)
    p_renew_reverse: EColVars2030 = field(default_factory=EColVars2030)

    p_local: EColVars2030 = field(default_factory=EColVars2030)
    p_local_pv: EColVars2030 = field(default_factory=EColVars2030)
    p_local_pv_roof: EColVars2030 = field(default_factory=EColVars2030)
    p_local_pv_facade: EColVars2030 = field(default_factory=EColVars2030)
    p_local_pv_park: EColVars2030 = field(default_factory=EColVars2030)
    p_local_pv_agri: EColVars2030 = field(default_factory=EColVars2030)
    p_local_wind_onshore: EColVars2030 = field(default_factory=EColVars2030)
    p_local_biomass: EColVars2030 = field(default_factory=EColVars2030)
    p_local_biomass_solid: EColVars2030 = field(default_factory=EColVars2030)
    p_local_biomass_gaseous: EColVars2030 = field(default_factory=EColVars2030)
    p_local_biomass_cogen: EColVars2030 = field(default_factory=EColVars2030)
    p_local_hydro: EColVars2030 = field(default_factory=EColVars2030)
    p_local_surplus: EColVars2030 = field(default_factory=EColVars2030)


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

    p_local_biomass_cogen.pct_energy = fact("Fact_E_P_renew_cogen_ratio_2018")
    p_local_biomass_cogen.energy = (
        p_local_biomass.energy * p_local_biomass_cogen.pct_energy
    )

    return p_local_biomass_cogen
