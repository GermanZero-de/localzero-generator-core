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
class EnergyDemand:
    # Used by d, d_r, d_b, d_i, d_t, d_a, d_e_hydrogen_reconv, p_hydrogen_total
    energy: float


@dataclass
class EFuelProduction:
    """This computes the replacement of fossil fuels by corresponding E-fuels.
    (e.g. petrol -> epetrol).
    """

    # Used by p_petrol, p_jetfuel, p_diesel
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_wage: float
    demand_electricity: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    full_load_hour: float
    invest: float
    invest_pa: float
    invest_per_x: float
    pct_of_wage: float
    power_to_be_installed: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        energy: float,
        inputs: Inputs,
        CO2e_emission_factor: float,
        production_2018: fuels2018.FuelProduction,
    ) -> "EFuelProduction":
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
class FuelWithoutDirectReplacement:
    """This computes the effect on our CO2e and energy budget of us totally stopping
    to produce some fuels without a direct replacement."""

    # Used by p_bioethanol, p_biodiesel, p_biogas
    CO2e_total_2021_estimated: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float

    @classmethod
    def calc(cls, energy2018: float) -> "FuelWithoutDirectReplacement":
        # Possible future work marker:
        # We simplified bio{ethonal,diesel,gas} to have 0 emission at
        # production and when burned.  This is not fully correct. But
        # if we didn't do that we would also have to account for growth
        # of the bio component in lulucf.
        return cls(
            change_energy_MWh=-energy2018,
            change_energy_pct=-1,
            CO2e_total_2021_estimated=0,
            change_CO2e_t=0,
            cost_climate_saved=0,
        )


@dataclass
class NewEFuelProduction:
    """Production of new style of efuels that are not yet used (at an industrial scale)."""

    # Used by p_emethan, p_hydrogen, p_hydrogen_reconv
    CO2e_production_based: float
    CO2e_production_based_per_MWh: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    cost_climate_saved: float
    cost_wage: float
    demand_electricity: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    full_load_hour: float
    invest: float
    invest_outside: float
    invest_pa: float
    invest_pa_outside: float
    invest_per_x: float
    pct_of_wage: float
    power_to_be_installed: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        energy: float,
        CO2e_emission_factor: float,
        invest_per_power: float,
        full_load_hour: float,
        fuel_efficiency: float,
    ) -> "NewEFuelProduction":
        fact = inputs.fact
        ass = inputs.ass
        entries = inputs.entries

        CO2e_total_2021_estimated = 0
        # We assume that we take as much CO2e out of the air when the E-Fuel
        # is produced, as we later emit when it is burned.
        CO2e_production_based_per_MWh = -1 * CO2e_emission_factor
        CO2e_production_based = CO2e_production_based_per_MWh * energy
        CO2e_total = CO2e_production_based
        change_CO2e_t = CO2e_total
        change_CO2e_pct = 0

        pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
        ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
        demand_electricity = energy / fuel_efficiency
        change_energy_MWh = energy
        power_to_be_installed = demand_electricity / full_load_hour
        invest = power_to_be_installed * invest_per_power
        cost_climate_saved = (
            -CO2e_total * entries.m_duration_neutral * fact("Fact_M_cost_per_CO2e_2020")
        )
        invest_pa = invest / entries.m_duration_target
        invest_outside = invest
        invest_pa_outside = invest_pa
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
            cost_climate_saved=cost_climate_saved,
            cost_wage=cost_wage,
            demand_electricity=demand_electricity,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            energy=energy,
            full_load_hour=full_load_hour,
            invest=invest,
            invest_outside=invest_outside,
            invest_pa=invest_pa,
            invest_pa_outside=invest_pa_outside,
            invest_per_x=invest_per_power,
            pct_of_wage=pct_of_wage,
            power_to_be_installed=power_to_be_installed,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class TotalEFuelProduction:
    # Used by p
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_wage: float
    demand_electricity: float
    demand_emplo: float
    demand_emplo_new: float
    energy: float
    invest: float
    invest_outside: float
    invest_pa: float
    invest_pa_outside: float

    @classmethod
    def calc(
        cls,
        f18: fuels2018.F18,
        new_efuels: list[NewEFuelProduction],
        efuels: list[EFuelProduction],
        fuels_without_repl: list[FuelWithoutDirectReplacement],
    ) -> "TotalEFuelProduction":

        res = cls(
            CO2e_production_based=sum(x.CO2e_production_based for x in new_efuels)
            + sum(x.CO2e_production_based for x in efuels),
            CO2e_total=sum(x.CO2e_total for x in new_efuels)
            + sum(x.CO2e_total for x in efuels),
            CO2e_total_2021_estimated=sum(
                x.CO2e_total_2021_estimated for x in new_efuels
            )
            + sum(x.CO2e_total_2021_estimated for x in efuels)
            + sum(x.CO2e_total_2021_estimated for x in fuels_without_repl),
            change_CO2e_pct=0,
            change_CO2e_t=sum(x.change_CO2e_t for x in new_efuels)
            + sum(x.change_CO2e_t for x in efuels)
            + sum(x.change_CO2e_t for x in fuels_without_repl),
            change_energy_MWh=sum(x.change_energy_MWh for x in new_efuels)
            + sum(x.change_energy_MWh for x in efuels)
            + sum(x.change_energy_MWh for x in fuels_without_repl),
            change_energy_pct=0,
            cost_climate_saved=sum(x.cost_climate_saved for x in new_efuels)
            + sum(x.cost_climate_saved for x in efuels)
            + sum(x.cost_climate_saved for x in fuels_without_repl),
            cost_wage=sum(x.cost_wage for x in new_efuels)
            + sum(x.cost_wage for x in efuels),
            demand_electricity=sum(x.demand_electricity for x in new_efuels)
            + sum(x.demand_electricity for x in efuels),
            demand_emplo=sum(x.demand_emplo for x in new_efuels)
            + sum(x.demand_emplo for x in efuels),
            demand_emplo_new=sum(x.demand_emplo_new for x in new_efuels)
            + sum(x.demand_emplo_new for x in efuels),
            energy=sum(x.energy for x in new_efuels) + sum(x.energy for x in efuels),
            invest=sum(x.invest for x in new_efuels) + sum(x.invest for x in efuels),
            invest_outside=sum(x.invest_outside for x in new_efuels),
            invest_pa=sum(x.invest_pa for x in new_efuels)
            + sum(x.invest_pa for x in efuels),
            invest_pa_outside=sum(x.invest_pa_outside for x in new_efuels),
        )
        res.change_energy_pct = div(res.change_energy_MWh, f18.p.energy)
        res.change_CO2e_pct = div(res.change_CO2e_t, f18.p.CO2e_total)
        return res


@dataclass
class F:
    # Used by f
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_energy_pct: float
    cost_climate_saved: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    invest: float
    invest_outside: float
    invest_pa: float
    invest_pa_outside: float

    @classmethod
    def of_p(cls, p: TotalEFuelProduction) -> "F":
        return cls(
            CO2e_total_2021_estimated=p.CO2e_total_2021_estimated,
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


@dataclass
class EFuels:
    # Used by p_efuels
    change_CO2e_t: float
    energy: float

    @classmethod
    def calc(cls, *efuels: EFuelProduction) -> "EFuels":
        change_CO2e_t = sum(e.change_CO2e_t for e in efuels)
        energy = sum(e.energy for e in efuels)
        return cls(change_CO2e_t=change_CO2e_t, energy=energy)


@dataclass
class F30:
    d: EnergyDemand
    d_r: EnergyDemand
    d_b: EnergyDemand
    d_i: EnergyDemand
    d_t: EnergyDemand
    d_a: EnergyDemand
    d_e_hydrogen_reconv: EnergyDemand
    # TODO: Rename those to p_eptrol, p_ejetfuel, ...
    p_petrol: EFuelProduction
    p_jetfuel: EFuelProduction
    p_diesel: EFuelProduction
    p_bioethanol: FuelWithoutDirectReplacement
    p_biodiesel: FuelWithoutDirectReplacement
    p_biogas: FuelWithoutDirectReplacement
    p_emethan: NewEFuelProduction
    p_hydrogen: NewEFuelProduction
    p_hydrogen_reconv: NewEFuelProduction
    p_hydrogen_total: EnergyDemand  # Actually this is total hydrogen production
    p_efuels: EFuels
    f: F
    p: TotalEFuelProduction


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
    fact = inputs.fact
    ass = inputs.ass

    d_r = EnergyDemand(r30.p.demand_emethan)
    d_b = EnergyDemand(b30.p.demand_ediesel + b30.p.demand_emethan)
    d_i = EnergyDemand(i30.p.demand_emethan + i30.p.demand_hydrogen)
    d_t = EnergyDemand(
        t30.t.transport.demand_epetrol
        + t30.t.transport.demand_ediesel
        + t30.t.transport.demand_ejetfuel
        + t30.t.transport.demand_hydrogen
    )
    d_a = EnergyDemand(
        a30.p_operation.demand_epetrol
        + a30.p_operation.demand_ediesel
        + a30.p_operation.demand_emethan
    )
    p_petrol = EFuelProduction.calc(
        energy=t30.t.transport.demand_epetrol + a30.p_operation.demand_epetrol,
        CO2e_emission_factor=fact("Fact_T_S_petrol_EmFa_tank_wheel_2018"),
        inputs=inputs,
        production_2018=f18.p_petrol,
    )
    p_jetfuel = EFuelProduction.calc(
        energy=t30.t.transport.demand_ejetfuel,
        CO2e_emission_factor=fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018"),
        inputs=inputs,
        production_2018=f18.p_jetfuel,
    )
    p_diesel = EFuelProduction.calc(
        energy=(
            b30.p.demand_ediesel
            + t30.t.transport.demand_ediesel
            + a30.p_operation.demand_ediesel
        ),
        CO2e_emission_factor=fact("Fact_T_S_diesel_EmFa_tank_wheel_2018"),
        inputs=inputs,
        production_2018=f18.p_diesel,
    )
    p_biogas = FuelWithoutDirectReplacement.calc(energy2018=f18.p_biogas.energy)
    p_biodiesel = FuelWithoutDirectReplacement.calc(energy2018=f18.p_biodiesel.energy)
    p_bioethanol = FuelWithoutDirectReplacement.calc(energy2018=f18.p_bioethanol.energy)

    p_emethan = NewEFuelProduction.calc(
        inputs,
        energy=r30.p.demand_emethan
        + b30.p.demand_emethan
        + i30.p.demand_emethan
        + a30.p_operation.demand_emethan,
        CO2e_emission_factor=fact("Fact_T_S_methan_EmFa_tank_wheel_2018"),
        invest_per_power=ass("Ass_S_methan_invest_per_power"),
        full_load_hour=ass("Ass_S_power_to_x_full_load_hours2"),
        fuel_efficiency=ass("Ass_S_methan_efficiency"),
    )
    p_hydrogen = NewEFuelProduction.calc(
        inputs,
        energy=i30.p.demand_hydrogen + t30.t.transport.demand_hydrogen,
        CO2e_emission_factor=0,
        invest_per_power=ass("Ass_S_electrolyses_invest_per_power"),
        full_load_hour=ass("Ass_F_P_electrolysis_full_load_hours"),
        fuel_efficiency=ass("Ass_F_P_electrolysis_efficiency"),
    )
    p_hydrogen_reconv = NewEFuelProduction.calc(
        inputs,
        energy=(
            (
                h30.p.demand_electricity
                + r30.p.demand_electricity
                + b30.p.demand_electricity
                + i30.p.demand_electricity
                + t30.t.transport.demand_electricity
                + a30.p_operation.demand_electricity
                + p_petrol.demand_electricity
                + p_jetfuel.demand_electricity
                + p_diesel.demand_electricity
                + p_emethan.demand_electricity
                + p_hydrogen.demand_electricity
            )
            * ass("Ass_E_P_renew_reverse_addon_to_demand_2035")
            / ass("Ass_E_P_renew_reverse_gud_efficiency")
        ),
        CO2e_emission_factor=0,
        invest_per_power=ass("Ass_S_electrolyses_invest_per_power"),
        full_load_hour=ass("Ass_F_P_electrolysis_full_load_hours"),
        fuel_efficiency=ass("Ass_F_P_electrolysis_efficiency"),
    )
    d_e_hydrogen_reconv = EnergyDemand(p_hydrogen_reconv.energy)
    d = EnergyDemand(
        d_r.energy
        + d_b.energy
        + d_i.energy
        + d_t.energy
        + d_a.energy
        + d_e_hydrogen_reconv.energy
    )
    p_efuels = EFuels.calc(p_petrol, p_diesel, p_jetfuel)

    p = TotalEFuelProduction.calc(
        f18,
        new_efuels=[p_emethan, p_hydrogen, p_hydrogen_reconv],
        efuels=[p_petrol, p_jetfuel, p_diesel],
        fuels_without_repl=[p_biogas, p_biodiesel, p_bioethanol],
    )

    f30 = F30(
        d=d,
        d_r=d_r,
        d_b=d_b,
        d_i=d_i,
        d_t=d_t,
        d_a=d_a,
        d_e_hydrogen_reconv=d_e_hydrogen_reconv,
        p_petrol=p_petrol,
        p_jetfuel=p_jetfuel,
        p_diesel=p_diesel,
        p_biogas=p_biogas,
        p_biodiesel=p_biodiesel,
        p_bioethanol=p_bioethanol,
        p_emethan=p_emethan,
        p_hydrogen=p_hydrogen,
        p_hydrogen_reconv=p_hydrogen_reconv,
        p_efuels=p_efuels,
        p_hydrogen_total=EnergyDemand(p_hydrogen.energy + p_hydrogen_reconv.energy),
        p=p,
        f=F.of_p(p),
    )

    return f30
