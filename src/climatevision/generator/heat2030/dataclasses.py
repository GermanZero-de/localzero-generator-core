# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..utils import div, MILLION
from ..heat2018.h18 import H18
from ..residences2030.r30 import R30
from ..business2030.b30 import B30
from ..common.energyWithCO2ePerMWh import EnergyWithCO2ePerMWh


@dataclass(kw_only=True)
class Vars0:
    # Used by h
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
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars5:
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
    cost_fuel: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars6(EnergyWithCO2ePerMWh):
    # Used by p_gas, p_coal
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_fuel: float
    cost_fuel_per_MWh: float

    @classmethod
    def calc(cls, inputs: Inputs, what: str, h18: H18, r30: R30, b30: B30) -> "Vars6":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        h18_p_what = getattr(h18, "p_" + what)
        r30_s_what = getattr(r30, "s_" + what)
        b30_s_what = getattr(b30, "s_" + what)

        CO2e_production_based_per_MWh = h18_p_what.CO2e_production_based_per_MWh
        CO2e_combustion_based_per_MWh = h18_p_what.CO2e_combustion_based_per_MWh

        energy = r30_s_what.energy + b30_s_what.energy

        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        cost_fuel_per_MWh = ass("Ass_R_S_" + what + "_energy_cost_factor_2035")
        cost_fuel = energy * cost_fuel_per_MWh / MILLION

        change_energy_MWh = energy - h18_p_what.energy
        change_energy_pct = div(change_energy_MWh, h18_p_what.energy)

        change_CO2e_t = CO2e_total - h18_p_what.CO2e_total
        change_CO2e_pct = div(change_CO2e_t, h18_p_what.CO2e_total)

        CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            cost_fuel=cost_fuel,
            cost_fuel_per_MWh=cost_fuel_per_MWh,
            energy=energy,
        )


@dataclass(kw_only=True)
class Vars7:
    # Used by p_lpg
    CO2e_combustion_based: float
    CO2e_combustion_based_per_MWh: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    energy: float

    @classmethod
    def calc(cls, inputs: Inputs, what: str, h18: H18, r30: R30, b30: B30) -> "Vars7":
        fact = inputs.fact
        entries = inputs.entries

        h18_p_what = getattr(h18, "p_" + what)
        r30_s_what = getattr(r30, "s_" + what)
        b30_s_what = getattr(b30, "s_" + what)

        CO2e_combustion_based_per_MWh = h18_p_what.CO2e_combustion_based_per_MWh

        energy = r30_s_what.energy + b30_s_what.energy

        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_combustion_based

        change_energy_MWh = energy - h18_p_what.energy
        change_energy_pct = div(change_energy_MWh, h18_p_what.energy)

        change_CO2e_t = CO2e_total - h18_p_what.CO2e_total
        change_CO2e_pct = div(change_CO2e_t, h18_p_what.CO2e_total)

        CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            energy=energy,
        )


@dataclass(kw_only=True)
class Vars8:
    # Used by p_fueloil
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars9(EnergyWithCO2ePerMWh):
    # Used by p_opetpro, p_heatnet_cogen
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        what: str,
        h18: H18,
        energy: float,
        CO2e_production_based_per_MWh: float,
        CO2e_combustion_based_per_MWh: float,
    ) -> "Vars9":
        fact = inputs.fact
        entries = inputs.entries

        h18_p_what = getattr(h18, "p_" + what)

        CO2e_production_based = energy * CO2e_production_based_per_MWh
        CO2e_combustion_based = energy * CO2e_combustion_based_per_MWh

        CO2e_total = CO2e_production_based + CO2e_combustion_based

        change_energy_MWh = energy - h18_p_what.energy
        change_energy_pct = div(change_energy_MWh, h18_p_what.energy)

        change_CO2e_t = CO2e_total - h18_p_what.CO2e_total
        change_CO2e_pct = div(change_CO2e_t, h18_p_what.CO2e_total)

        CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_combustion_based_per_MWh=CO2e_combustion_based_per_MWh,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            energy=energy,
        )


@dataclass(kw_only=True)
class Vars10:
    # Used by p_heatnet
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
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars11:
    # Used by p_heatnet_plant
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    area_ha_available: float = None  # type: ignore
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
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars12:
    # Used by p_heatnet_lheatpump
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
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars13:
    # Used by p_heatnet_geoth
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
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_com: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_com: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_energy: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars14:
    # Used by p_biomass
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_fuel: float = None  # type: ignore
    cost_fuel_per_MWh: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars15:
    # Used by p_ofossil, p_orenew, p_solarth, p_heatpump
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    energy: float = None  # type: ignore
