# pyright: strict
from dataclasses import dataclass, InitVar

from ..utils import div, MILLION
from ..agri2018.a18 import A18
from ..inputs import Inputs
from .energy_demand import CO2eChange, Production


@dataclass(kw_only=True)
class CO2eChangeEnergyPerMWh(CO2eChange):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    change_energy_pct: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_production_based = 0
        self.CO2e_combustion_based_per_MWh = getattr(
            a18, what
        ).CO2e_combustion_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved


@dataclass(kw_only=True)
class CO2eChangeFuelOilGas(CO2eChangeEnergyPerMWh):
    area_m2: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0
        self.area_m2 = 0

        parent = CO2eChangeEnergyPerMWh(
            inputs=inputs,
            what=what,
            a18=a18,
            energy=self.energy,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_combustion_based_per_MWh = parent.CO2e_combustion_based_per_MWh
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved
        self.change_energy_MWh = parent.change_energy_MWh
        self.change_energy_pct = parent.change_energy_pct


@dataclass(kw_only=True)
class CO2eChangeFuelHeatpump(CO2eChangeEnergyPerMWh):
    cost_fuel: float = 0
    cost_fuel_per_MWh: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    emplo_existing: float = 0
    full_load_hour: float = 0
    invest: float = 0
    invest_pa: float = 0
    invest_per_x: float = 0
    pct_of_wage: float = 0
    power_installed: float = 0
    power_to_be_installed: float = 0
    ratio_wage_to_emplo: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        self.CO2e_combustion_based = 0
        self.CO2e_production_based = 0

        self.cost_fuel_per_MWh = inputs.fact("Fact_R_S_gas_energy_cost_factor_2018")
        self.cost_fuel = self.energy * self.cost_fuel_per_MWh / MILLION

        self.full_load_hour = inputs.fact("Fact_B_S_full_usage_hours_buildings")
        self.power_installed = div(getattr(a18, what).energy, self.full_load_hour)
        self.power_to_be_installed = max(
            div(self.energy, self.full_load_hour) - self.power_installed, 0
        )

        self.invest_per_x = inputs.fact("Fact_R_S_heatpump_cost")
        self.invest = self.invest_per_x * self.power_to_be_installed * 1000
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.pct_of_wage = inputs.fact(
            "Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017"
        )
        self.cost_wage = self.invest_pa * self.pct_of_wage
        self.ratio_wage_to_emplo = inputs.fact(
            "Fact_B_P_heating_wage_per_person_per_year"
        )
        self.demand_emplo = div(self.cost_wage, self.ratio_wage_to_emplo)

        self.emplo_existing = (
            inputs.fact("Fact_B_P_install_heating_emplo_2017")
            * inputs.entries.m_population_com_2018
            / inputs.entries.m_population_nat
            * inputs.ass("Ass_B_D_install_heating_emplo_pct_of_A_heatpump")
        )

        self.demand_emplo_new = max(0, self.demand_emplo - self.emplo_existing)

        parent = CO2eChangeEnergyPerMWh(
            inputs=inputs,
            what=what,
            a18=a18,
            energy=self.energy,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_combustion_based_per_MWh = parent.CO2e_combustion_based_per_MWh
        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.cost_climate_saved = parent.cost_climate_saved
        self.change_energy_MWh = parent.change_energy_MWh

        # override value from parent!
        self.change_CO2e_pct = div(
            parent.change_CO2e_t, 1.0  # always 0
        )  # getattr(a18, what).CO2e_total)


@dataclass(kw_only=True)
class CO2eChangeFuelEmethan(CO2eChange):
    energy: float

    CO2e_combustion_based_per_MWh: float = 0
    change_energy_MWh: float = 0
    demand_emethan: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]

    def __post_init__(self, inputs: Inputs, what: str, a18: A18):

        what = ""

        self.CO2e_production_based = 0
        self.CO2e_combustion_based = 0
        self.CO2e_combustion_based_per_MWh = inputs.fact(
            "Fact_T_S_methan_EmFa_tank_wheel_2018"
        )

        self.change_energy_MWh = self.energy
        self.demand_emethan = self.energy

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved


@dataclass(kw_only=True)
class CO2eChangeS(CO2eChange):
    change_energy_MWh: float = 0
    change_energy_pct: float = 0
    cost_wage: float = 0
    demand_emplo: float = 0
    demand_emplo_new: float = 0
    energy: float = 0
    invest: float = 0
    invest_pa: float = 0

    inputs: InitVar[Inputs]
    what: InitVar[str]
    a18: InitVar[A18]
    s_petrol: InitVar[CO2eChangeEnergyPerMWh]
    s_diesel: InitVar[CO2eChangeEnergyPerMWh]
    s_fueloil: InitVar[CO2eChangeFuelOilGas]
    s_lpg: InitVar[CO2eChangeEnergyPerMWh]
    s_gas: InitVar[CO2eChangeFuelOilGas]
    s_emethan: InitVar[CO2eChangeFuelEmethan]
    s_biomass: InitVar[CO2eChangeEnergyPerMWh]
    s_elec: InitVar[CO2eChangeEnergyPerMWh]
    s_heatpump: InitVar[CO2eChangeFuelHeatpump]

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        what: str,
        a18: A18,
        s_petrol: CO2eChangeEnergyPerMWh,
        s_diesel: CO2eChangeEnergyPerMWh,
        s_fueloil: CO2eChangeFuelOilGas,
        s_lpg: CO2eChangeEnergyPerMWh,
        s_gas: CO2eChangeFuelOilGas,
        s_emethan: CO2eChangeFuelEmethan,
        s_biomass: CO2eChangeEnergyPerMWh,
        s_elec: CO2eChangeEnergyPerMWh,
        s_heatpump: CO2eChangeFuelHeatpump,
    ):

        self.CO2e_production_based = 0
        self.CO2e_combustion_based = (
            s_petrol.CO2e_combustion_based
            + s_diesel.CO2e_combustion_based
            + s_fueloil.CO2e_combustion_based
            + s_lpg.CO2e_combustion_based
            + s_gas.CO2e_combustion_based
            + s_emethan.CO2e_combustion_based
            + s_biomass.CO2e_combustion_based
            + s_elec.CO2e_combustion_based
            + s_heatpump.CO2e_combustion_based
        )

        self.invest = s_heatpump.invest
        self.invest_pa = self.invest / inputs.entries.m_duration_target

        self.energy = (
            s_petrol.energy
            + s_diesel.energy
            + s_fueloil.energy
            + s_lpg.energy
            + s_gas.energy
            + s_emethan.energy
            + s_biomass.energy
            + s_elec.energy
            + s_heatpump.energy
        )
        self.change_energy_MWh = self.energy - getattr(a18, what).energy
        self.change_energy_pct = div(self.change_energy_MWh, getattr(a18, what).energy)

        self.demand_emplo = s_heatpump.demand_emplo
        self.demand_emplo_new = s_heatpump.demand_emplo_new

        self.cost_wage = s_heatpump.cost_wage

        parent = CO2eChange(
            inputs=inputs,
            what=what,
            a18=a18,
            CO2e_combustion_based=self.CO2e_combustion_based,
            CO2e_production_based=self.CO2e_production_based,
        )

        self.CO2e_total = parent.CO2e_total
        self.CO2e_total_2021_estimated = parent.CO2e_total_2021_estimated
        self.change_CO2e_pct = parent.change_CO2e_pct
        self.change_CO2e_t = parent.change_CO2e_t
        self.cost_climate_saved = parent.cost_climate_saved


@dataclass(kw_only=True)
class EnergySupply:
    s: CO2eChangeS
    s_petrol: CO2eChangeEnergyPerMWh
    s_diesel: CO2eChangeEnergyPerMWh
    s_fueloil: CO2eChangeFuelOilGas
    s_lpg: CO2eChangeEnergyPerMWh
    s_gas: CO2eChangeFuelOilGas
    s_biomass: CO2eChangeEnergyPerMWh
    s_elec: CO2eChangeEnergyPerMWh
    s_heatpump: CO2eChangeFuelHeatpump
    s_emethan: CO2eChangeFuelEmethan


def calc_supply(inputs: Inputs, a18: A18, production: Production) -> EnergySupply:

    s_petrol = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_petrol",
        a18=a18,
        energy=production.p_operation_vehicles.demand_epetrol,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_diesel = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_diesel",
        a18=a18,
        energy=production.p_operation_vehicles.demand_ediesel,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_lpg = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_lpg",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_biomass = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_biomass",
        a18=a18,
        energy=production.p_operation.demand_biomass,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_elec = CO2eChangeEnergyPerMWh(
        inputs=inputs,
        what="s_elec",
        a18=a18,
        energy=production.p_operation.demand_electricity,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_fueloil = CO2eChangeFuelOilGas(
        inputs=inputs,
        what="s_fueloil",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_gas = CO2eChangeFuelOilGas(
        inputs=inputs,
        what="s_gas",
        a18=a18,
        energy=0,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_heatpump = CO2eChangeFuelHeatpump(
        inputs=inputs,
        what="s_heatpump",
        a18=a18,
        energy=production.p_operation.demand_heatpump,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )
    s_emethan = CO2eChangeFuelEmethan(
        inputs=inputs,
        what="",
        a18=a18,
        energy=production.p_operation_heat.demand_emethan,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )

    s = CO2eChangeS(
        inputs=inputs,
        what="s",
        a18=a18,
        s_petrol=s_petrol,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_emethan=s_emethan,
        s_biomass=s_biomass,
        s_elec=s_elec,
        s_heatpump=s_heatpump,
        CO2e_combustion_based=None,  # type: ignore
        CO2e_production_based=None,  # type: ignore
    )

    return EnergySupply(
        s=s,
        s_petrol=s_petrol,
        s_diesel=s_diesel,
        s_fueloil=s_fueloil,
        s_lpg=s_lpg,
        s_gas=s_gas,
        s_biomass=s_biomass,
        s_elec=s_elec,
        s_heatpump=s_heatpump,
        s_emethan=s_emethan,
    )
