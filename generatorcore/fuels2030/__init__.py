"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/fuel.html
"""

# pyright: strict
from ..inputs import Inputs
from .. import (
    fuels2018,
    agri2030,
    business2030,
    heat2030,
    industry2030,
    residences2030,
    transport2030,
)
from .f30 import F30
from .dataclasses import (
    EnergyDemand,
    EFuelProduction,
    FuelWithoutDirectReplacement,
    NewEFuelProduction,
    EFuels,
    F,
    TotalEFuelProduction,
)


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
