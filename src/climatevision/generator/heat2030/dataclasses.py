# pyright: strict

from dataclasses import dataclass, InitVar

from ..inputs import Inputs
from ..utils import div, MILLION
from ..heat2018.h18 import H18
from ..common.g import G
from ..common.energy import Energy
from ..common.energy_with_co2e_per_mwh import EnergyWithCO2ePerMWh
from ..common.co2_emission import CO2Emission


@dataclass(kw_only=True)
class VarsInvest:
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    invest: float = 0
    invest_com: float = 0
    invest_pa: float = 0
    invest_pa_com: float = 0


@dataclass(kw_only=True)
class VarsChange:
    CO2e_total_2021_estimated: float = 0
    change_CO2e_pct: float = 0
    change_CO2e_t: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    cost_climate_saved: float = 0


@dataclass(kw_only=True)
class VarsWage:
    pct_energy: float
    invest_per_x: float
    pct_of_wage: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact

        self.pct_of_wage = fact("Fact_B_P_constr_main_revenue_pct_of_wage_2017")
        self.ratio_wage_to_emplo = fact("Fact_B_P_constr_main_ratio_wage_to_emplo_2017")


@dataclass(kw_only=True)
class Vars9(EnergyWithCO2ePerMWh, VarsChange):
    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact
        entries = inputs.entries

        h18_p_what = getattr(h18, "p_" + what)

        self.CO2e_production_based = self.energy * self.CO2e_production_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        self.CO2e_total = self.CO2e_production_based + self.CO2e_combustion_based

        self.change_energy_MWh = self.energy - h18_p_what.energy
        self.change_energy_pct = div(self.change_energy_MWh, h18_p_what.energy)

        self.change_CO2e_t = self.CO2e_total - h18_p_what.CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, h18_p_what.CO2e_total)

        self.CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )

        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )


@dataclass(kw_only=True)
class Vars6(Vars9):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact
        ass = inputs.ass

        Vars9.__post_init__(self, inputs=inputs, what=what, h18=h18)

        if what == "biomass":
            self.cost_fuel_per_MWh = fact("Fact_R_S_wood_energy_cost_factor_2018")
        else:
            self.cost_fuel_per_MWh = ass("Ass_R_S_" + what + "_energy_cost_factor_2035")

        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION


@dataclass(kw_only=True)
class Vars11(Vars9, VarsInvest, VarsWage):
    area_ha_available: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact
        entries = inputs.entries

        Vars9.__post_init__(self, inputs=inputs, what=what, h18=h18)
        VarsWage.__post_init__(self, inputs=inputs, what=what, h18=h18)

        self.area_ha_available = self.energy / fact(
            "Fact_H_P_heatnet_solarth_park_yield_2025"
        )
        self.invest = self.invest_per_x * self.area_ha_available
        self.invest_pa = self.invest / entries.m_duration_target

        self.cost_wage = self.pct_of_wage * self.invest_pa

        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)

        self.invest_pa_com = self.invest_pa
        self.invest_com = self.invest
        self.demand_emplo_new = self.demand_emplo


@dataclass(kw_only=True)
class Vars13(Vars9, VarsInvest, VarsWage):
    full_load_hour: float
    power_to_be_installed: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        entries = inputs.entries

        Vars9.__post_init__(self, inputs=inputs, what=what, h18=h18)
        VarsWage.__post_init__(self, inputs=inputs, what=what, h18=h18)

        self.power_to_be_installed = div(self.energy, self.full_load_hour)
        self.invest = self.invest_per_x * self.power_to_be_installed
        self.invest_pa = self.invest / entries.m_duration_target

        self.cost_wage = self.pct_of_wage * self.invest_pa
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)
        self.demand_emplo_new = self.demand_emplo

        self.invest_pa_com = self.invest_pa
        self.invest_com = self.invest


@dataclass(kw_only=True)
class Vars12(Vars13):
    demand_electricity: float = 0
    full_load_hour: float = 0
    power_to_be_installed: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
    ):
        fact = inputs.fact

        Vars13.__post_init__(self, inputs=inputs, what=what, h18=h18)

        self.demand_electricity = self.energy / fact("Fact_H_P_heatnet_lheatpump_apf")


@dataclass(kw_only=True)
class Vars10(CO2Emission, Energy, VarsInvest, VarsChange):
    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]
    heatnet_cogen: InitVar[Vars9]
    heatnet_plant: InitVar[Vars11]
    heatnet_lheatpump: InitVar[Vars12]
    heatnet_geoth: InitVar[Vars13]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
        heatnet_cogen: Vars9,
        heatnet_plant: Vars11,
        heatnet_lheatpump: Vars12,
        heatnet_geoth: Vars13,
    ):
        fact = inputs.fact
        entries = inputs.entries

        h18_p_what = getattr(h18, "p_" + what)

        self.CO2e_combustion_based = heatnet_cogen.CO2e_combustion_based
        self.CO2e_production_based = (
            heatnet_cogen.CO2e_production_based
            + heatnet_plant.CO2e_production_based
            + heatnet_lheatpump.CO2e_production_based
            + heatnet_geoth.CO2e_production_based
        )
        self.CO2e_total = heatnet_cogen.CO2e_total

        self.change_energy_MWh = self.energy - h18_p_what.energy
        self.change_energy_pct = div(self.change_energy_MWh, h18_p_what.energy)

        self.change_CO2e_t = self.CO2e_total - h18_p_what.CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, h18_p_what.CO2e_total)

        self.CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        self.invest = (
            heatnet_plant.invest + heatnet_lheatpump.invest + heatnet_geoth.invest
        )
        self.invest_pa = (
            heatnet_plant.invest_pa
            + heatnet_lheatpump.invest_pa
            + heatnet_geoth.invest_pa
        )
        self.invest_pa_com = self.invest_pa
        self.demand_emplo = (
            heatnet_plant.demand_emplo
            + heatnet_lheatpump.demand_emplo
            + heatnet_geoth.demand_emplo
        )
        self.invest_com = self.invest
        self.cost_wage = (
            heatnet_plant.cost_wage
            + heatnet_lheatpump.cost_wage
            + heatnet_geoth.cost_wage
        )
        self.demand_emplo_new = (
            heatnet_plant.demand_emplo_new
            + heatnet_lheatpump.demand_emplo_new
            + heatnet_geoth.demand_emplo_new
        )


@dataclass(kw_only=True)
class Vars5(CO2Emission, VarsInvest, VarsChange):
    cost_fuel: float = 0
    demand_electricity: float = 0
    energy: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    h18: InitVar[H18]
    gas: InitVar[Vars6]
    lpg: InitVar[Vars9]
    fueloil: InitVar[Vars6]
    opetpro: InitVar[Vars9]
    coal: InitVar[Vars6]
    heatnet: InitVar[Vars10]
    heatnet_lheatpump: InitVar[Vars12]
    biomass: InitVar[Vars6]
    ofossil: InitVar[Vars9]
    orenew: InitVar[Vars9]

    def __post_init__(
        self,
        inputs: Inputs,
        what: str,
        h18: H18,
        gas: Vars6,
        lpg: Vars9,
        fueloil: Vars6,
        opetpro: Vars9,
        coal: Vars6,
        heatnet: Vars10,
        heatnet_lheatpump: Vars12,
        biomass: Vars6,
        ofossil: Vars9,
        orenew: Vars9,
    ):
        fact = inputs.fact
        entries = inputs.entries

        h18_p_what = getattr(h18, "p" + what)

        self.demand_electricity = heatnet_lheatpump.demand_electricity
        self.CO2e_total_2021_estimated = h18_p_what.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        self.energy = (
            gas.energy
            + lpg.energy
            + fueloil.energy
            + opetpro.energy
            + coal.energy
            + heatnet.energy
            + biomass.energy
            + ofossil.energy
            + orenew.energy
        )
        self.change_energy_MWh = self.energy - h18_p_what.energy
        self.CO2e_combustion_based = (
            gas.CO2e_combustion_based
            + lpg.CO2e_combustion_based
            + fueloil.CO2e_combustion_based
            + opetpro.CO2e_combustion_based
            + coal.CO2e_combustion_based
            + heatnet.CO2e_combustion_based
        )
        self.invest = heatnet.invest
        self.demand_emplo = heatnet.demand_emplo
        self.demand_emplo_new = heatnet.demand_emplo_new
        self.invest_pa_com = heatnet.invest_pa_com
        self.invest_pa = heatnet.invest_pa
        self.invest_com = heatnet.invest_com
        self.CO2e_total = (
            gas.CO2e_total
            + lpg.CO2e_total
            + fueloil.CO2e_total
            + opetpro.CO2e_total
            + coal.CO2e_total
            + heatnet.CO2e_total
            + biomass.CO2e_total
            + ofossil.CO2e_total
            + orenew.CO2e_total
        )
        self.cost_wage = heatnet.cost_wage
        self.change_energy_pct = div(self.change_energy_MWh, h18_p_what.energy)
        self.cost_fuel = (
            gas.cost_fuel + fueloil.cost_fuel + coal.cost_fuel + biomass.cost_fuel
        )
        self.cost_climate_saved = (
            (self.CO2e_total_2021_estimated - self.CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        self.change_CO2e_t = self.CO2e_total - h18_p_what.CO2e_total
        self.change_CO2e_pct = div(self.change_CO2e_t, h18_p_what.CO2e_total)
        self.CO2e_production_based = (
            gas.CO2e_production_based
            + opetpro.CO2e_production_based
            + coal.CO2e_production_based
            + heatnet.CO2e_production_based
            + biomass.CO2e_production_based
            + ofossil.CO2e_production_based
            + orenew.CO2e_production_based
        )


@dataclass(kw_only=True)
class H(CO2Emission, VarsInvest, VarsChange):
    demand_emplo_com: float

    @classmethod
    def of_p_and_g(cls, p: Vars5, g: G) -> "H":
        return cls(
            CO2e_total_2021_estimated=p.CO2e_total_2021_estimated,
            CO2e_combustion_based=p.CO2e_combustion_based,
            invest_pa=g.invest_pa + p.invest_pa,
            invest_pa_com=g.invest_pa_com + p.invest_pa_com,
            CO2e_total=p.CO2e_total,
            change_energy_MWh=p.change_energy_MWh,
            change_CO2e_t=p.change_CO2e_t,
            cost_climate_saved=p.cost_climate_saved,
            cost_wage=g.cost_wage + p.cost_wage,
            change_energy_pct=p.change_energy_pct,
            change_CO2e_pct=p.change_CO2e_pct,
            invest=g.invest + p.invest,
            demand_emplo=g.demand_emplo + p.demand_emplo,
            demand_emplo_new=g.demand_emplo_new + p.demand_emplo_new,
            invest_com=g.invest_com + p.invest_com,
            CO2e_production_based=p.CO2e_production_based,
            demand_emplo_com=g.demand_emplo_com,  # TODO: Check demand_emplo_new in Heat with Hauke
        )
