from dataclasses import dataclass, field
from .inputs import Inputs
from .utils import div
from . import (
    fuels2018,
    agri2030,
    business2030,
    heat2030,
    industry2030,
    residences2030,
    transport2030,
)


@dataclass
class F:
    # Used by f
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
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore


@dataclass
class EnergyDemand:
    # Used by d, d_r, d_b, d_i, d_t, d_a, d_e_hydrogen_reconv, p_hydrogen_total
    energy: float = None  # type: ignore


@dataclass
class TotalEFuelProduction:
    # Used by p
    CO2e_production_based: float = None  # type: ignore
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
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore


@dataclass
class EFuelProduction:
    # Used by p_petrol, p_jetfuel, p_diesel
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
    invest_pa: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore

    @classmethod
    def calc(
        cls,
        energy: float,
        inputs: Inputs,
        CO2e_emission_factor: float,
        production_2018: fuels2018.FuelProduction,
    ) -> "EFuelProduction":
        # TODO: Need better name for neg_CO2e_production_based_per_MWh
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        CO2e_total_2021_estimated = production_2018.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        # We assume that we take as much CO2e out of the air when the E-Fuel
        # is produced, as we later emit when it is burned.
        CO2e_production_based_per_MWh = -1 * CO2e_emission_factor
        pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
        ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
        invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
        full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
        demand_electricity = energy / ass("Ass_S_power_to_x_efficiency")
        change_energy_MWh = energy - production_2018.energy
        CO2e_production_based = CO2e_production_based_per_MWh * energy
        power_to_be_installed = div(demand_electricity, full_load_hour)
        change_energy_pct = div(change_energy_MWh, production_2018.energy)
        CO2e_total = CO2e_production_based
        invest = power_to_be_installed * ass("Ass_S_power_to_x_invest_per_power")
        change_CO2e_t = CO2e_total - production_2018.CO2e_total
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_pa = invest / entries.m_duration_target
        change_CO2e_pct = div(change_CO2e_t, production_2018.CO2e_total)
        cost_wage = invest_pa * pct_of_wage
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        return cls(
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_MWh=CO2e_production_based_per_MWh,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            full_load_hour=full_load_hour,
            invest=invest,
            invest_pa=invest_pa,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class Vars5:
    # Used by p_bioethanol, p_biodiesel, p_biogas
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    change_energy_pct: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by p_emethan, p_hydrogen, p_hydrogen_reconv
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_MWh: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    CO2e_total_2021_estimated: float = None  # type: ignore
    change_CO2e_pct: float = None  # type: ignore
    change_CO2e_t: float = None  # type: ignore
    change_energy_MWh: float = None  # type: ignore
    cost_climate_saved: float = None  # type: ignore
    cost_wage: float = None  # type: ignore
    demand_electricity: float = None  # type: ignore
    demand_emplo: float = None  # type: ignore
    demand_emplo_new: float = None  # type: ignore
    energy: float = None  # type: ignore
    full_load_hour: float = None  # type: ignore
    invest: float = None  # type: ignore
    invest_outside: float = None  # type: ignore
    invest_pa: float = None  # type: ignore
    invest_pa_outside: float = None  # type: ignore
    invest_per_x: float = None  # type: ignore
    pct_of_wage: float = None  # type: ignore
    power_to_be_installed: float = None  # type: ignore
    ratio_wage_to_emplo: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by p_efuels
    change_CO2e_t: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class F30:
    f: F = field(default_factory=F)
    d: EnergyDemand = field(default_factory=EnergyDemand)
    d_r: EnergyDemand = field(default_factory=EnergyDemand)
    d_b: EnergyDemand = field(default_factory=EnergyDemand)
    d_i: EnergyDemand = field(default_factory=EnergyDemand)
    d_t: EnergyDemand = field(default_factory=EnergyDemand)
    d_a: EnergyDemand = field(default_factory=EnergyDemand)
    p: TotalEFuelProduction = field(default_factory=TotalEFuelProduction)
    d_e_hydrogen_reconv: EnergyDemand = field(default_factory=EnergyDemand)
    # TODO: Rename those to p_eptrol, p_ejetfuel, ...
    p_petrol: EFuelProduction = field(default_factory=EFuelProduction)
    p_jetfuel: EFuelProduction = field(default_factory=EFuelProduction)
    p_diesel: EFuelProduction = field(default_factory=EFuelProduction)
    p_bioethanol: Vars5 = field(default_factory=Vars5)
    p_biodiesel: Vars5 = field(default_factory=Vars5)
    p_biogas: Vars5 = field(default_factory=Vars5)
    p_emethan: Vars6 = field(default_factory=Vars6)
    p_hydrogen: Vars6 = field(default_factory=Vars6)
    p_hydrogen_reconv: Vars6 = field(default_factory=Vars6)
    p_hydrogen_total: EnergyDemand = field(default_factory=EnergyDemand)
    p_efuels: Vars7 = field(default_factory=Vars7)


def calc(
    inputs: Inputs,
    *,
    f18: fuels2018.F18,
    a30: agri2030.A30,
    b30: business2030.B30,
    h30: heat2030.H30,
    i30: industry2030.I30,
    r30: residences2030.R30,
    t30: transport2030.T30,
) -> F30:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    entries = inputs.entries
    f30 = F30()
    f30.d_r = EnergyDemand(r30.p.demand_emethan)
    f30.d_b = EnergyDemand(b30.p.demand_ediesel + b30.p.demand_emethan)
    f30.d_i = EnergyDemand(i30.p.demand_emethan + i30.p.demand_hydrogen)
    f30.d_t = EnergyDemand(
        t30.t.transport.demand_epetrol
        + t30.t.transport.demand_ediesel
        + t30.t.transport.demand_ejetfuel
        + t30.t.transport.demand_hydrogen
    )
    f30.d_a = EnergyDemand(
        a30.p_operation.demand_epetrol
        + a30.p_operation.demand_ediesel
        + a30.p_operation.demand_emethan
    )
    f30.p_petrol.energy = (
        t30.t.transport.demand_epetrol + a30.p_operation.demand_epetrol
    )
    f30.p_petrol = EFuelProduction.calc(
        energy=t30.t.transport.demand_epetrol + a30.p_operation.demand_epetrol,
        CO2e_emission_factor=fact("Fact_T_S_petrol_EmFa_tank_wheel_2018"),
        inputs=inputs,
        production_2018=f18.p_petrol,
    )
    f30.p_jetfuel = EFuelProduction.calc(
        energy=t30.t.transport.demand_ejetfuel,
        CO2e_emission_factor=fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018"),
        inputs=inputs,
        production_2018=f18.p_jetfuel,
    )
    f30.p_diesel = EFuelProduction.calc(
        energy=(
            b30.p.demand_ediesel
            + t30.t.transport.demand_ediesel
            + a30.p_operation.demand_ediesel
        ),
        CO2e_emission_factor=fact("Fact_T_S_diesel_EmFa_tank_wheel_2018"),
        inputs=inputs,
        production_2018=f18.p_diesel,
    )

    f30.p_emethan.energy = (
        r30.p.demand_emethan
        + b30.p.demand_emethan
        + i30.p.demand_emethan
        + a30.p_operation.demand_emethan
    )
    f30.p_emethan.CO2e_total_2021_estimated = 0
    f30.p_emethan.CO2e_production_based_per_MWh = -1 * fact(
        "Fact_T_S_methan_EmFa_tank_wheel_2018"
    )
    f30.p_emethan.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_emethan.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f30.p_emethan.invest_per_x = ass("Ass_S_methan_invest_per_power")
    f30.p_emethan.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f30.p_emethan.demand_electricity = f30.p_emethan.energy / ass(
        "Ass_S_methan_efficiency"
    )
    f30.p_emethan.change_energy_MWh = f30.p_emethan.energy
    f30.p_emethan.CO2e_production_based = (
        f30.p_emethan.CO2e_production_based_per_MWh * f30.p_emethan.energy
    )
    f30.p_emethan.power_to_be_installed = div(
        f30.p_emethan.demand_electricity, f30.p_emethan.full_load_hour
    )
    f30.p_emethan.CO2e_total = f30.p_emethan.CO2e_production_based
    f30.p_emethan.invest = f30.p_emethan.power_to_be_installed * ass(
        "Ass_S_methan_invest_per_power"
    )
    f30.p_emethan.change_CO2e_t = f30.p_emethan.CO2e_total
    f30.p_emethan.cost_climate_saved = (
        -f30.p_emethan.CO2e_total
        * entries.m_duration_neutral
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f30.p_emethan.invest_pa = f30.p_emethan.invest / entries.m_duration_target
    f30.p_emethan.invest_outside = f30.p_emethan.invest
    f30.p_emethan.change_CO2e_pct = div(f30.p_emethan.change_CO2e_t, 0)
    f30.p_emethan.invest_pa_outside = f30.p_emethan.invest_pa
    f30.p_emethan.cost_wage = f30.p_emethan.invest_pa * f30.p_emethan.pct_of_wage
    f30.p_emethan.demand_emplo = div(
        f30.p_emethan.cost_wage, f30.p_emethan.ratio_wage_to_emplo
    )
    f30.p_emethan.demand_emplo_new = f30.p_emethan.demand_emplo
    f30.p_hydrogen.energy = i30.p.demand_hydrogen + t30.t.transport.demand_hydrogen
    f30.p_hydrogen.CO2e_total_2021_estimated = 0
    f30.p_hydrogen.CO2e_production_based_per_MWh = 0.0
    f30.p_hydrogen.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_hydrogen.ratio_wage_to_emplo = ass(
        "Ass_S_constr_renew_gas_wage_per_year_2017"
    )
    f30.p_hydrogen.invest_per_x = ass("Ass_S_electrolyses_invest_per_power")
    f30.p_hydrogen.full_load_hour = ass("Ass_F_P_electrolysis_full_load_hours")
    f30.p_hydrogen.demand_electricity = f30.p_hydrogen.energy / ass(
        "Ass_F_P_electrolysis_efficiency"
    )
    f30.p_hydrogen.change_energy_MWh = f30.p_hydrogen.energy
    f30.p_hydrogen.power_to_be_installed = f30.p_hydrogen.demand_electricity / ass(
        "Ass_F_P_electrolysis_full_load_hours"
    )
    f30.p_hydrogen.CO2e_total = 0
    f30.p_hydrogen.change_CO2e_t = 0
    f30.p_hydrogen.invest = f30.p_hydrogen.power_to_be_installed * ass(
        "Ass_S_electrolyses_invest_per_power"
    )
    f30.p_hydrogen.cost_climate_saved = 0
    f30.p_hydrogen.invest_pa = f30.p_hydrogen.invest / entries.m_duration_target
    f30.p_hydrogen.invest_outside = f30.p_hydrogen.invest
    f30.p_hydrogen.change_CO2e_pct = div(f30.p_hydrogen.change_CO2e_t, 0)
    f30.p_hydrogen.invest_pa_outside = f30.p_hydrogen.invest_pa
    f30.p_hydrogen.cost_wage = f30.p_hydrogen.invest_pa * f30.p_hydrogen.pct_of_wage
    f30.p_hydrogen.demand_emplo = div(
        f30.p_hydrogen.cost_wage, f30.p_hydrogen.ratio_wage_to_emplo
    )
    f30.p_hydrogen.demand_emplo_new = f30.p_hydrogen.demand_emplo
    f30.p_hydrogen.CO2e_production_based = 0
    f30.p_biodiesel.change_energy_MWh = -f18.p_biodiesel.energy
    f30.p_biodiesel.CO2e_total_2021_estimated = 0
    f30.p_biodiesel.change_energy_pct = div(
        f30.p_biodiesel.change_energy_MWh, f18.p_biodiesel.energy
    )
    f30.p_biodiesel.change_CO2e_t = -f18.p_biodiesel.CO2e_total
    f30.p_biodiesel.cost_climate_saved = 0
    f30.p_bioethanol.change_energy_MWh = -f18.p_bioethanol.energy
    f30.p_bioethanol.CO2e_total_2021_estimated = 0
    f30.p_bioethanol.change_energy_pct = div(
        f30.p_bioethanol.change_energy_MWh, f18.p_bioethanol.energy
    )
    f30.p_bioethanol.change_CO2e_t = f30.p_biodiesel.change_CO2e_t
    f30.p_bioethanol.cost_climate_saved = 0
    f30.p_biogas.change_energy_MWh = -f18.p_biogas.energy
    f30.p_biogas.CO2e_total_2021_estimated = 0
    f30.p_biogas.change_energy_pct = div(
        f30.p_biogas.change_energy_MWh, f18.p_biogas.energy
    )
    f30.p_biogas.change_CO2e_t = 0
    f30.p_biogas.cost_climate_saved = 0
    f30.p_hydrogen_reconv.CO2e_total_2021_estimated = 0
    f30.p_hydrogen_reconv.CO2e_production_based_per_MWh = 0
    f30.p_hydrogen_reconv.invest_per_x = ass("Ass_S_electrolyses_invest_per_power")
    f30.p_hydrogen_reconv.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_hydrogen_reconv.ratio_wage_to_emplo = ass(
        "Ass_S_constr_renew_gas_wage_per_year_2017"
    )
    f30.p_hydrogen_reconv.full_load_hour = ass("Ass_F_P_electrolysis_full_load_hours")
    f30.p_hydrogen_reconv.energy = (
        (
            h30.p.demand_electricity
            + r30.p.demand_electricity
            + b30.p.demand_electricity
            + i30.p.demand_electricity
            + t30.t.transport.demand_electricity
            + a30.p_operation.demand_electricity
            + f30.p_petrol.demand_electricity
            + f30.p_jetfuel.demand_electricity
            + f30.p_diesel.demand_electricity
            + f30.p_emethan.demand_electricity
            + f30.p_hydrogen.demand_electricity
        )
        * ass("Ass_E_P_renew_reverse_addon_to_demand_2035")
        / ass("Ass_E_P_renew_reverse_gud_efficiency")
    )
    f30.p_hydrogen_reconv.CO2e_total = 0
    f30.p_hydrogen_reconv.change_CO2e_t = 0
    f30.p_hydrogen_reconv.demand_electricity = f30.p_hydrogen_reconv.energy / ass(
        "Ass_F_P_electrolysis_efficiency"
    )
    f30.p_hydrogen_reconv.change_energy_MWh = f30.p_hydrogen_reconv.energy
    f30.p_hydrogen_reconv.cost_climate_saved = 0
    f30.p_hydrogen_reconv.power_to_be_installed = (
        f30.p_hydrogen_reconv.demand_electricity
        / ass("Ass_F_P_electrolysis_full_load_hours")
    )
    f30.p_hydrogen_reconv.change_CO2e_pct = div(f30.p_hydrogen_reconv.change_CO2e_t, 0)
    f30.p_hydrogen_reconv.invest = (
        f30.p_hydrogen_reconv.power_to_be_installed * f30.p_hydrogen_reconv.invest_per_x
    )
    f30.p_hydrogen_reconv.invest_pa = (
        f30.p_hydrogen_reconv.invest / entries.m_duration_target
    )
    f30.p_hydrogen_reconv.invest_outside = f30.p_hydrogen_reconv.invest
    f30.p_hydrogen_reconv.invest_pa_outside = f30.p_hydrogen_reconv.invest_pa
    f30.p_hydrogen_reconv.cost_wage = (
        f30.p_hydrogen_reconv.invest_pa * f30.p_hydrogen_reconv.pct_of_wage
    )
    f30.p_hydrogen_reconv.demand_emplo = div(
        f30.p_hydrogen_reconv.cost_wage, f30.p_hydrogen_reconv.ratio_wage_to_emplo
    )
    f30.p_hydrogen_reconv.demand_emplo_new = f30.p_hydrogen_reconv.demand_emplo
    f30.p_hydrogen_reconv.CO2e_production_based = 0
    f30.p_efuels.energy = (
        f30.p_petrol.energy + f30.p_diesel.energy + f30.p_jetfuel.energy
    )
    f30.p_efuels.change_CO2e_t = (
        f30.p_petrol.change_CO2e_t
        + f30.p_diesel.change_CO2e_t
        + f30.p_jetfuel.change_CO2e_t
    )
    f30.p.CO2e_total_2021_estimated = (
        f30.p_petrol.CO2e_total_2021_estimated
        + f30.p_jetfuel.CO2e_total_2021_estimated
        + f30.p_diesel.CO2e_total_2021_estimated
        + f30.p_bioethanol.CO2e_total_2021_estimated
        + f30.p_biodiesel.CO2e_total_2021_estimated
        + f30.p_biogas.CO2e_total_2021_estimated
        + f30.p_emethan.CO2e_total_2021_estimated
        + f30.p_hydrogen.CO2e_total_2021_estimated
        + f30.p_hydrogen_reconv.CO2e_total_2021_estimated
    )
    f30.p.CO2e_production_based = (
        f30.p_petrol.CO2e_production_based
        + f30.p_jetfuel.CO2e_production_based
        + f30.p_diesel.CO2e_production_based
        + f30.p_emethan.CO2e_production_based
        + f30.p_hydrogen.CO2e_production_based
        + f30.p_hydrogen_reconv.CO2e_production_based
    )
    f30.p.energy = (
        f30.p_petrol.energy
        + f30.p_jetfuel.energy
        + f30.p_diesel.energy
        + f30.p_emethan.energy
        + f30.p_hydrogen.energy
        + f30.p_hydrogen_reconv.energy
    )
    f30.p.CO2e_total = (
        f30.p_petrol.CO2e_total
        + f30.p_jetfuel.CO2e_total
        + f30.p_diesel.CO2e_total
        + f30.p_emethan.CO2e_total
        + f30.p_hydrogen.CO2e_total
        + f30.p_hydrogen_reconv.CO2e_total
    )
    f30.p.demand_electricity = (
        f30.p_petrol.demand_electricity
        + f30.p_jetfuel.demand_electricity
        + f30.p_diesel.demand_electricity
        + f30.p_emethan.demand_electricity
        + f30.p_hydrogen.demand_electricity
        + f30.p_hydrogen_reconv.demand_electricity
    )
    f30.p.change_energy_MWh = (
        f30.p_petrol.change_energy_MWh
        + f30.p_jetfuel.change_energy_MWh
        + f30.p_diesel.change_energy_MWh
        + f30.p_bioethanol.change_energy_MWh
        + f30.p_biodiesel.change_energy_MWh
        + f30.p_biogas.change_energy_MWh
        + f30.p_emethan.change_energy_MWh
        + f30.p_hydrogen.change_energy_MWh
        + f30.p_hydrogen_reconv.change_energy_MWh
    )
    f30.p.change_CO2e_t = (
        f30.p_petrol.change_CO2e_t
        + f30.p_jetfuel.change_CO2e_t
        + f30.p_diesel.change_CO2e_t
        + f30.p_bioethanol.change_CO2e_t
        + f30.p_biodiesel.change_CO2e_t
        + f30.p_biogas.change_CO2e_t
        + f30.p_emethan.change_CO2e_t
        + f30.p_hydrogen.change_CO2e_t
        + f30.p_hydrogen_reconv.change_CO2e_t
    )
    f30.p.cost_climate_saved = (
        f30.p_petrol.cost_climate_saved
        + f30.p_jetfuel.cost_climate_saved
        + f30.p_diesel.cost_climate_saved
        + f30.p_bioethanol.cost_climate_saved
        + f30.p_biodiesel.cost_climate_saved
        + f30.p_biogas.cost_climate_saved
        + f30.p_emethan.cost_climate_saved
        + f30.p_hydrogen.cost_climate_saved
        + f30.p_hydrogen_reconv.cost_climate_saved
    )
    f30.p.change_energy_pct = div(f30.p.change_energy_MWh, f18.p.energy)
    f30.p.change_CO2e_pct = div(f30.p.change_CO2e_t, f18.p.CO2e_total)
    f30.p.invest = (
        f30.p_petrol.invest
        + f30.p_jetfuel.invest
        + f30.p_diesel.invest
        + f30.p_emethan.invest
        + f30.p_hydrogen.invest
        + f30.p_hydrogen_reconv.invest
    )
    f30.p.invest_pa = (
        f30.p_petrol.invest_pa
        + f30.p_jetfuel.invest_pa
        + f30.p_diesel.invest_pa
        + f30.p_emethan.invest_pa
        + f30.p_hydrogen.invest_pa
        + f30.p_hydrogen_reconv.invest_pa
    )
    f30.p.invest_outside = (
        f30.p_emethan.invest_outside
        + f30.p_hydrogen.invest_outside
        + f30.p_hydrogen_reconv.invest_outside
    )
    f30.p.invest_pa_outside = (
        f30.p_emethan.invest_pa_outside
        + f30.p_hydrogen.invest_pa_outside
        + f30.p_hydrogen_reconv.invest_pa_outside
    )
    f30.p.cost_wage = (
        f30.p_petrol.cost_wage
        + f30.p_jetfuel.cost_wage
        + f30.p_diesel.cost_wage
        + f30.p_emethan.cost_wage
        + f30.p_hydrogen.cost_wage
        + f30.p_hydrogen_reconv.cost_wage
    )
    f30.p.demand_emplo = (
        f30.p_petrol.demand_emplo
        + f30.p_jetfuel.demand_emplo
        + f30.p_diesel.demand_emplo
        + f30.p_emethan.demand_emplo
        + f30.p_hydrogen.demand_emplo
        + f30.p_hydrogen_reconv.demand_emplo
    )
    f30.p.demand_emplo_new = (
        f30.p_petrol.demand_emplo_new
        + f30.p_jetfuel.demand_emplo_new
        + f30.p_diesel.demand_emplo_new
        + f30.p_emethan.demand_emplo_new
        + f30.p_hydrogen.demand_emplo_new
        + f30.p_hydrogen_reconv.demand_emplo_new
    )
    f30.f.CO2e_total_2021_estimated = f30.p.CO2e_total_2021_estimated
    f30.f.CO2e_production_based = f30.p.CO2e_production_based
    f30.f.CO2e_total = f30.p.CO2e_total
    f30.f.change_energy_MWh = f30.p.change_energy_MWh
    f30.f.change_CO2e_t = f30.p.change_CO2e_t
    f30.f.cost_climate_saved = f30.p.cost_climate_saved
    f30.f.change_energy_pct = f30.p.change_energy_pct
    f30.f.change_CO2e_pct = f30.p.change_CO2e_pct
    f30.f.invest = f30.p.invest
    f30.f.invest_pa = f30.p.invest_pa
    f30.f.invest_outside = f30.p.invest_outside
    f30.f.invest_pa_outside = f30.p.invest_pa_outside
    f30.f.cost_wage = f30.p.cost_wage
    f30.f.demand_emplo = f30.p.demand_emplo
    f30.f.demand_emplo_new = f30.p.demand_emplo_new
    f30.d_e_hydrogen_reconv.energy = f30.p_hydrogen_reconv.energy
    f30.d.energy = (
        f30.d_r.energy
        + f30.d_b.energy
        + f30.d_i.energy
        + f30.d_t.energy
        + f30.d_a.energy
        + f30.d_e_hydrogen_reconv.energy
    )
    f30.p_hydrogen_total.energy = f30.p_hydrogen.energy + f30.p_hydrogen_reconv.energy
    return f30
