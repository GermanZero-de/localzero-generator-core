from dataclasses import dataclass, asdict
from .inputs import Inputs
from .utils import div

#  Definition der relevanten Spaltennamen für den Sektor F (30)


@dataclass
class FColVars2030:
    demand_electricity: float = None
    demand_hydrogen: float = None
    energy: float = None
    CO2e_cb: float = None
    CO2e_pb: float = None
    CO2e_pb_per_MWh: float = None
    CO2e_total: float = None
    change_energy_MWh: float = None
    change_energy_pct: float = None
    change_CO2e_t: float = None
    CO2e_total_2021_estimated: float = None
    cost_climate_saved: float = None
    invest_pa: float = None
    invest_per_x: float = None
    invest: float = None
    pct_of_wage: float = None
    cost_wage: float = None
    ratio_wage_to_emplo: float = None
    demand_emplo: float = None
    power_to_be_installed: float = None
    full_load_hour: float = None
    change_CO2e_pct: float = None
    action: float = None
    emplo_existing: float = None
    demand_emplo_new: float = None
    invest_pa_outside: float = None
    invest_outside: float = None
    cost_mro_pa: float = None


@dataclass
class F30:
    f: FColVars2030 = FColVars2030()
    g: FColVars2030 = FColVars2030()
    d: FColVars2030 = FColVars2030()
    d_r: FColVars2030 = FColVars2030()
    d_b: FColVars2030 = FColVars2030()
    d_i: FColVars2030 = FColVars2030()
    d_t: FColVars2030 = FColVars2030()
    d_a: FColVars2030 = FColVars2030()
    p: FColVars2030 = FColVars2030()

    d_e_hydrogen_reconv: FColVars2030 = FColVars2030()
    p_petrol: FColVars2030 = FColVars2030()
    p_jetfuel: FColVars2030 = FColVars2030()
    p_diesel: FColVars2030 = FColVars2030()
    p_bioethanol: FColVars2030 = FColVars2030()
    p_biodiesel: FColVars2030 = FColVars2030()
    p_biogas: FColVars2030 = FColVars2030()
    p_emethan: FColVars2030 = FColVars2030()
    p_hydrogen: FColVars2030 = FColVars2030()
    p_hydrogen_reconv: FColVars2030 = FColVars2030()

    #only medded for fuels pdf text
    p_hydrogen_total: FColVars2030 = FColVars2030()
    p_efuels: FColVars2030 = FColVars2030()

    # erzeuge dictionry
    def dict(self):
        return asdict(self)


def calc(root, inputs: Inputs):
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    Million = 1000000

    f = root.f30

    """ Start"""
    f.d_r.energy = root.r30.p.demand_emethan
    f.d_b.energy = root.b30.p.demand_ediesel + root.b30.p.demand_emethan
    f.d_i.energy = root.i30.p.demand_emethan + root.i30.p.demand_hydrogen
    f.d_t.energy = (
        root.t30.t.demand_epetrol
        + root.t30.t.demand_ediesel
        + root.t30.t.demand_ejetfuel
        + root.t30.t.demand_hydrogen
    )
    f.d_a.energy = (
        root.a30.p_operation.demand_epetrol
        + root.a30.p_operation.demand_ediesel
        + root.a30.p_operation.demand_emethan
    )
    f.p_petrol.energy = root.t30.t.demand_epetrol + root.a30.p_operation.demand_epetrol
    f.p_jetfuel.energy = root.t30.t.demand_ejetfuel
    f.p_diesel.energy = (
        root.b30.p.demand_ediesel
        + root.t30.t.demand_ediesel
        + root.a30.p_operation.demand_ediesel
    )
    f.p_emethan.energy = (
        root.r30.p.demand_emethan
        + root.b30.p.demand_emethan
        + root.i30.p.demand_emethan
        + root.a30.p_operation.demand_emethan
    )
    f.p_hydrogen.energy = root.i30.p.demand_hydrogen + root.t30.t.demand_hydrogen
    # ---------------------------
    f.p_bioethanol.change_energy_MWh = -root.f18.p_bioethanol.energy
    f.p_biodiesel.change_energy_MWh = -root.f18.p_biodiesel.energy
    f.p_biogas.change_energy_MWh = -root.f18.p_biogas.energy
    f.p_petrol.CO2e_total_2021_estimated = root.f18.p_petrol.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    f.p_jetfuel.CO2e_total_2021_estimated = root.f18.p_jetfuel.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    f.p_diesel.CO2e_total_2021_estimated = root.f18.p_diesel.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    f.p_bioethanol.CO2e_total_2021_estimated = (
        f.p_biodiesel.CO2e_total_2021_estimated
    ) = (
        f.p_biogas.CO2e_total_2021_estimated
    ) = (
        f.p_emethan.CO2e_total_2021_estimated
    ) = (
        f.p_hydrogen.CO2e_total_2021_estimated
    ) = f.p_hydrogen_reconv.CO2e_total_2021_estimated = 0

    # ---------------------------------------
    f.p_petrol.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
    f.p_petrol.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f.p_petrol.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f.p_petrol.invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
    f.p_petrol.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f.p_jetfuel.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")
    f.p_jetfuel.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f.p_jetfuel.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f.p_jetfuel.invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
    f.p_jetfuel.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f.p_diesel.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
    f.p_diesel.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f.p_diesel.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f.p_diesel.invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
    f.p_diesel.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f.p_emethan.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_methan_EmFa_tank_wheel_2018")
    f.p_hydrogen.CO2e_pb_per_MWh = 0.0
    f.p_hydrogen_reconv.CO2e_pb_per_MWh = 0
    # --------------------------------
    f.p_emethan.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f.p_emethan.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f.p_emethan.invest_per_x = ass("Ass_S_methan_invest_per_power")
    f.p_emethan.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f.p_hydrogen.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f.p_hydrogen.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f.p_hydrogen.invest_per_x = ass("Ass_S_electrolyses_invest_per_power")
    f.p_hydrogen.full_load_hour = ass("Ass_F_P_electrolysis_full_load_hours")
    f.p_hydrogen_reconv.invest_per_x = ass("Ass_S_electrolyses_invest_per_power")
    # ---------------------------------------
    f.p_hydrogen_reconv.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    # --------------------------------------
    f.p_hydrogen_reconv.ratio_wage_to_emplo = ass(
        "Ass_S_constr_renew_gas_wage_per_year_2017"
    )
    # --------------------------------------
    f.p_hydrogen_reconv.full_load_hour = ass("Ass_F_P_electrolysis_full_load_hours")
    # --------------------------------------
    f.p_petrol.demand_electricity = f.p_petrol.energy / ass(
        "Ass_S_power_to_x_efficiency"
    )
    f.p_petrol.change_energy_MWh = f.p_petrol.energy - root.f18.p_petrol.energy
    f.p_jetfuel.demand_electricity = f.p_jetfuel.energy / ass(
        "Ass_S_power_to_x_efficiency"
    )
    f.p_jetfuel.change_energy_MWh = f.p_jetfuel.energy - root.f18.p_jetfuel.energy
    f.p_diesel.demand_electricity = f.p_diesel.energy / ass(
        "Ass_S_power_to_x_efficiency"
    )
    f.p_diesel.change_energy_MWh = f.p_diesel.energy - root.f18.p_diesel.energy
    f.p_emethan.demand_electricity = f.p_emethan.energy / ass(
        "Ass_S_methan_efficiency"
    )  # -----------------------
    f.p_emethan.change_energy_MWh = f.p_emethan.energy
    f.p_hydrogen.demand_electricity = f.p_hydrogen.energy / ass(
        "Ass_F_P_electrolysis_efficiency"
    )

    f.p_hydrogen.change_energy_MWh = f.p_hydrogen.energy
    f.p_bioethanol.change_energy_pct = div(
        f.p_bioethanol.change_energy_MWh, root.f18.p_bioethanol.energy
    )
    f.p_biodiesel.change_energy_pct = div(
        f.p_biodiesel.change_energy_MWh, root.f18.p_biodiesel.energy
    )
    f.p_biogas.change_energy_pct = div(
        f.p_biogas.change_energy_MWh, root.f18.p_biogas.energy
    )
    # -------------------------------------
    f.p.CO2e_total_2021_estimated = (
        f.p_petrol.CO2e_total_2021_estimated
        + f.p_jetfuel.CO2e_total_2021_estimated
        + f.p_diesel.CO2e_total_2021_estimated
        + f.p_bioethanol.CO2e_total_2021_estimated
        + f.p_biodiesel.CO2e_total_2021_estimated
        + f.p_biogas.CO2e_total_2021_estimated
        + f.p_emethan.CO2e_total_2021_estimated
        + f.p_hydrogen.CO2e_total_2021_estimated
        + f.p_hydrogen_reconv.CO2e_total_2021_estimated
    )  # SUM(p_petrol.CO2e_total_2021_estimated:p_hydrogen_reconv.CO2e_total_2021_estimated)
    f.p_petrol.CO2e_pb = f.p_petrol.CO2e_pb_per_MWh * f.p_petrol.energy
    f.p_jetfuel.CO2e_pb = f.p_jetfuel.CO2e_pb_per_MWh * f.p_jetfuel.energy
    f.p_diesel.CO2e_pb = f.p_diesel.CO2e_pb_per_MWh * f.p_diesel.energy
    f.p_emethan.CO2e_pb = f.p_emethan.CO2e_pb_per_MWh * f.p_emethan.energy
    f.p_hydrogen.CO2e_pb = f.p_hydrogen_reconv.CO2e_pb = 0
    # --------------------------------
    f.p_petrol.power_to_be_installed = div(
        f.p_petrol.demand_electricity, f.p_petrol.full_load_hour
    )
    f.p_petrol.change_energy_pct = div(
        f.p_petrol.change_energy_MWh, root.f18.p_petrol.energy
    )
    f.p_jetfuel.power_to_be_installed = div(
        f.p_jetfuel.demand_electricity, f.p_jetfuel.full_load_hour
    )
    f.p_jetfuel.change_energy_pct = div(
        f.p_jetfuel.change_energy_MWh, root.f18.p_jetfuel.energy
    )
    f.p_diesel.power_to_be_installed = f.p_diesel.demand_electricity / ass(
        "Ass_S_power_to_x_full_load_hours2"
    )
    f.p_diesel.change_energy_pct = div(
        f.p_diesel.change_energy_MWh, root.f18.p_diesel.energy
    )
    f.p_emethan.power_to_be_installed = div(
        f.p_emethan.demand_electricity, f.p_emethan.full_load_hour
    )
    # ---------------------------------------
    f.p_hydrogen.power_to_be_installed = f.p_hydrogen.demand_electricity / ass(
        "Ass_F_P_electrolysis_full_load_hours"
    )
    f.p_hydrogen_reconv.energy = (
        (
            root.h30.p.demand_electricity
            + root.r30.p.demand_electricity
            + root.b30.p.demand_electricity
            + root.i30.p.demand_electricity
            + root.t30.t.demand_electricity
            + root.a30.p_operation.demand_electricity
            + f.p_petrol.demand_electricity
            + f.p_jetfuel.demand_electricity
            + f.p_diesel.demand_electricity
            + f.p_emethan.demand_electricity
            + f.p_hydrogen.demand_electricity
        )
        * ass("Ass_E_P_renew_reverse_addon_to_demand_2035")
        / ass("Ass_E_P_renew_reverse_gud_efficiency")
    )
    f.f.CO2e_total_2021_estimated = f.p.CO2e_total_2021_estimated
    f.p_petrol.CO2e_total = f.p_petrol.CO2e_pb
    f.p_jetfuel.CO2e_total = f.p_jetfuel.CO2e_pb
    f.p_diesel.CO2e_total = f.p_diesel.CO2e_pb
    f.p_hydrogen.CO2e_total = f.p_hydrogen_reconv.CO2e_total = 0
    f.p_biodiesel.change_CO2e_t = -root.f18.p_biodiesel.CO2e_total
    f.p_bioethanol.change_CO2e_t = f.p_biodiesel.change_CO2e_t
    f.p_hydrogen.change_CO2e_t = (
        f.p_hydrogen_reconv.change_CO2e_t
    ) = f.p_biogas.change_CO2e_t = 0
    f.p.CO2e_pb = (
        f.p_petrol.CO2e_pb
        + f.p_jetfuel.CO2e_pb
        + f.p_diesel.CO2e_pb
        + f.p_emethan.CO2e_pb
        + f.p_hydrogen.CO2e_pb
        + f.p_hydrogen_reconv.CO2e_pb
    )  # SUM(p_petrol.CO2e_pb:p_hydrogen_reconv.CO2e_pb)

    f.p_emethan.CO2e_total = f.p_emethan.CO2e_pb
    # ---------------------------------
    f.p_petrol.invest = f.p_petrol.power_to_be_installed * ass(
        "Ass_S_power_to_x_invest_per_power"
    )
    f.p_jetfuel.invest = f.p_jetfuel.power_to_be_installed * ass(
        "Ass_S_power_to_x_invest_per_power"
    )
    f.p_diesel.invest = f.p_diesel.power_to_be_installed * ass(
        "Ass_S_power_to_x_invest_per_power"
    )
    f.p_emethan.invest = f.p_emethan.power_to_be_installed * ass(
        "Ass_S_methan_invest_per_power"
    )
    # ---------------------------------------
    f.p_hydrogen.invest = f.p_hydrogen.power_to_be_installed * ass(
        "Ass_S_electrolyses_invest_per_power"
    )
    f.d_e_hydrogen_reconv.energy = f.p_hydrogen_reconv.energy
    f.p.energy = (
        f.p_petrol.energy
        + f.p_jetfuel.energy
        + f.p_diesel.energy
        + f.p_emethan.energy
        + f.p_hydrogen.energy
        + f.p_hydrogen_reconv.energy
    )  # SUM(p_petrol.energy:p_hydrogen_reconv.energy)
    f.p_hydrogen_reconv.demand_electricity = f.p_hydrogen_reconv.energy / ass(
        "Ass_F_P_electrolysis_efficiency"
    )
    f.p_hydrogen_reconv.change_energy_MWh = f.p_hydrogen_reconv.energy
    # ---------------------------------
    f.p_petrol.change_CO2e_t = f.p_petrol.CO2e_total - root.f18.p_petrol.CO2e_total
    f.p_petrol.cost_climate_saved = (
        (f.p_petrol.CO2e_total_2021_estimated - f.p_petrol.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f.p_jetfuel.change_CO2e_t = f.p_jetfuel.CO2e_total - root.f18.p_jetfuel.CO2e_total
    f.p_jetfuel.cost_climate_saved = (
        (f.p_jetfuel.CO2e_total_2021_estimated - f.p_jetfuel.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f.p_diesel.change_CO2e_t = f.p_diesel.CO2e_total - root.f18.p_diesel.CO2e_total
    f.p_diesel.cost_climate_saved = (
        (f.p_diesel.CO2e_total_2021_estimated - f.p_diesel.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f.f.CO2e_pb = f.p.CO2e_pb
    f.p.CO2e_total = (
        f.p_petrol.CO2e_total
        + f.p_jetfuel.CO2e_total
        + f.p_diesel.CO2e_total
        + f.p_emethan.CO2e_total
        + f.p_hydrogen.CO2e_total
        + f.p_hydrogen_reconv.CO2e_total
    )  # SUM(p_petrol.CO2e_total:p_hydrogen_reconv.CO2e_total)
    f.p_emethan.change_CO2e_t = f.p_emethan.CO2e_total
    # --------------------------------------
    f.p_emethan.cost_climate_saved = (
        -f.p_emethan.CO2e_total
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f.p_bioethanol.cost_climate_saved = (
        f.p_biodiesel.cost_climate_saved
    ) = (
        f.p_biogas.cost_climate_saved
    ) = f.p_hydrogen.cost_climate_saved = f.p_hydrogen_reconv.cost_climate_saved = 0
    f.p_petrol.invest_pa = f.p_petrol.invest / entry("In_M_duration_target")
    f.p_jetfuel.invest_pa = f.p_jetfuel.invest / entry("In_M_duration_target")
    f.p_diesel.invest_pa = f.p_diesel.invest / entry("In_M_duration_target")
    f.p_emethan.invest_pa = f.p_emethan.invest / entry("In_M_duration_target")
    # --------------------------------------
    f.p_emethan.invest_outside = f.p_emethan.invest
    f.p_hydrogen.invest_pa = f.p_hydrogen.invest / entry("In_M_duration_target")
    f.p_hydrogen.invest_outside = f.p_hydrogen.invest
    f.d.energy = (
        f.d_r.energy
        + f.d_b.energy
        + f.d_i.energy
        + f.d_t.energy
        + f.d_a.energy
        + f.d_e_hydrogen_reconv.energy
    )  # SUM(d_r.energy:d_e_hydrogen_reconv.energy)
    f.p.demand_electricity = (
        f.p_petrol.demand_electricity
        + f.p_jetfuel.demand_electricity
        + f.p_diesel.demand_electricity
        + f.p_emethan.demand_electricity
        + f.p_hydrogen.demand_electricity
        + f.p_hydrogen_reconv.demand_electricity
    )  # (SUM(p_petrol.demand_electricity:p_hydrogen_reconv.demand_electricity))
    f.p_hydrogen_reconv.power_to_be_installed = (
        f.p_hydrogen_reconv.demand_electricity
        / ass("Ass_F_P_electrolysis_full_load_hours")
    )
    f.p.change_energy_MWh = (
        f.p_petrol.change_energy_MWh
        + f.p_jetfuel.change_energy_MWh
        + f.p_diesel.change_energy_MWh
        + f.p_bioethanol.change_energy_MWh
        + f.p_biodiesel.change_energy_MWh
        + f.p_biogas.change_energy_MWh
        + f.p_emethan.change_energy_MWh
        + f.p_hydrogen.change_energy_MWh
        + f.p_hydrogen_reconv.change_energy_MWh
    )  # SUM(p_petrol.change_energy_MWh:p_hydrogen_reconv.change_energy_MWh)
    f.p_petrol.change_CO2e_pct = div(
        f.p_petrol.change_CO2e_t, root.f18.p_petrol.CO2e_total
    )
    f.p_jetfuel.change_CO2e_pct = div(
        f.p_jetfuel.change_CO2e_t, root.f18.p_jetfuel.CO2e_total
    )
    f.p_diesel.change_CO2e_pct = div(
        f.p_diesel.change_CO2e_t, root.f18.p_diesel.CO2e_total
    )
    f.f.CO2e_total = f.p.CO2e_total
    f.p.change_CO2e_t = (
        f.p_petrol.change_CO2e_t
        + f.p_jetfuel.change_CO2e_t
        + f.p_diesel.change_CO2e_t
        + f.p_bioethanol.change_CO2e_t
        + f.p_biodiesel.change_CO2e_t
        + f.p_biogas.change_CO2e_t
        + f.p_emethan.change_CO2e_t
        + f.p_hydrogen.change_CO2e_t
        + f.p_hydrogen_reconv.change_CO2e_t
    )  # SUM(p_petrol.change_CO2e_t:p_hydrogen_reconv.change_CO2e_t)
    # SUM(p_petrol.change_CO2e_t:p_hydrogen_reconv.change_CO2e_t)
    f.p.cost_climate_saved = (
        f.p_petrol.cost_climate_saved
        + f.p_jetfuel.cost_climate_saved
        + f.p_diesel.cost_climate_saved
        + f.p_bioethanol.cost_climate_saved
        + f.p_biodiesel.cost_climate_saved
        + f.p_biogas.cost_climate_saved
        + f.p_emethan.cost_climate_saved
        + f.p_hydrogen.cost_climate_saved
        + f.p_hydrogen_reconv.cost_climate_saved
    )  # SUM(p_petrol.cost_climate_saved:p_emethan.cost_climate_saved)
    f.p_petrol.cost_wage = f.p_petrol.invest_pa * f.p_petrol.pct_of_wage
    f.p_jetfuel.cost_wage = f.p_jetfuel.invest_pa * f.p_jetfuel.pct_of_wage
    f.p_diesel.cost_wage = f.p_diesel.invest_pa * f.p_diesel.pct_of_wage
    f.p_emethan.invest_pa_outside = f.p_emethan.invest_pa
    f.p_emethan.cost_wage = f.p_emethan.invest_pa * f.p_emethan.pct_of_wage
    # --------------------------------------
    f.p_hydrogen.invest_pa_outside = f.p_hydrogen.invest_pa
    f.p_hydrogen.cost_wage = f.p_hydrogen.invest_pa * f.p_hydrogen.pct_of_wage
    f.p_hydrogen_reconv.invest = (
        f.p_hydrogen_reconv.power_to_be_installed * f.p_hydrogen_reconv.invest_per_x
    )
    f.f.change_energy_MWh = f.p.change_energy_MWh
    f.p.change_energy_pct = div(f.p.change_energy_MWh, root.f18.p.energy)
    f.f.change_CO2e_t = f.p.change_CO2e_t
    f.p.change_CO2e_pct = div(f.p.change_CO2e_t, root.f18.p.CO2e_total)
    f.f.cost_climate_saved = f.p.cost_climate_saved
    f.p_petrol.demand_emplo = div(f.p_petrol.cost_wage, f.p_petrol.ratio_wage_to_emplo)
    f.p_jetfuel.demand_emplo = div(
        f.p_jetfuel.cost_wage, f.p_jetfuel.ratio_wage_to_emplo
    )
    f.p_diesel.demand_emplo = div(f.p_diesel.cost_wage, f.p_diesel.ratio_wage_to_emplo)
    f.p_emethan.demand_emplo = div(
        f.p_emethan.cost_wage, f.p_emethan.ratio_wage_to_emplo
    )
    f.p_hydrogen.demand_emplo = (
        div(f.p_hydrogen.cost_wage, f.p_hydrogen.ratio_wage_to_emplo)
        if entry("In_M_AGS_com") == "DG000000"
        else 0
    )
    f.p.invest = (
        f.p_petrol.invest
        + f.p_jetfuel.invest
        + f.p_diesel.invest
        + f.p_emethan.invest
        + f.p_hydrogen.invest
        + f.p_hydrogen_reconv.invest
    )  # SUM(p_petrol.invest:p_hydrogen_reconv.invest)
    f.p_hydrogen_reconv.invest_pa = f.p_hydrogen_reconv.invest / entry(
        "In_M_duration_target"
    )
    f.p_hydrogen_reconv.invest_outside = f.p_hydrogen_reconv.invest
    f.f.change_energy_pct = f.p.change_energy_pct
    f.f.change_CO2e_pct = f.p.change_CO2e_pct
    f.p_petrol.demand_emplo_new = f.p_petrol.demand_emplo
    f.p_jetfuel.demand_emplo_new = f.p_jetfuel.demand_emplo
    f.p_diesel.demand_emplo_new = f.p_diesel.demand_emplo
    f.p_emethan.demand_emplo_new = f.p_emethan.demand_emplo
    f.p_hydrogen.demand_emplo_new = f.p_hydrogen.demand_emplo
    f.f.invest = f.p.invest
    f.p.invest_pa = (
        f.p_petrol.invest_pa
        + f.p_jetfuel.invest_pa
        + f.p_diesel.invest_pa
        + f.p_emethan.invest_pa
        + f.p_hydrogen.invest_pa
        + f.p_hydrogen_reconv.invest_pa
    )  # SUM(p_petrol.invest_pa:p_hydrogen_reconv.invest_pa)
    f.p_hydrogen_reconv.invest_pa_outside = f.p_hydrogen_reconv.invest_pa
    f.p_hydrogen_reconv.cost_wage = (
        f.p_hydrogen_reconv.invest_pa * f.p_hydrogen_reconv.pct_of_wage
    )
    f.p.invest_outside = (
        f.p_emethan.invest_outside
        + f.p_hydrogen.invest_outside
        + f.p_hydrogen_reconv.invest_outside
    )
    f.f.invest_pa = f.p.invest_pa
    f.p.invest_pa_outside = (
        f.p_emethan.invest_pa_outside
        + f.p_hydrogen.invest_pa_outside
        + f.p_hydrogen_reconv.invest_pa_outside
    )
    f.p.cost_wage = (
        f.p_petrol.cost_wage
        + f.p_jetfuel.cost_wage
        + f.p_diesel.cost_wage
        + f.p_emethan.cost_wage
        + f.p_hydrogen.cost_wage
        + f.p_hydrogen_reconv.cost_wage
    )  # SUM(p_petrol.cost_wage:p_hydrogen_reconv.cost_wage)
    f.p_hydrogen_reconv.demand_emplo = (
        div(f.p_hydrogen_reconv.cost_wage, f.p_hydrogen_reconv.ratio_wage_to_emplo)
        if entry("In_M_AGS_com") == "DG000000"
        else 0
    )
    f.f.invest_outside = f.p.invest_outside
    f.f.invest_pa_outside = f.p.invest_pa_outside
    f.f.cost_wage = f.p.cost_wage
    f.p.demand_emplo = (
        f.p_petrol.demand_emplo
        + f.p_jetfuel.demand_emplo
        + f.p_diesel.demand_emplo
        + f.p_emethan.demand_emplo
        + f.p_hydrogen.demand_emplo
        + f.p_hydrogen_reconv.demand_emplo
    )  # SUM(p_petrol.demand_emplo:p_hydrogen_reconv.demand_emplo)
    f.p_hydrogen_reconv.demand_emplo_new = f.p_hydrogen_reconv.demand_emplo
    f.f.demand_emplo = f.p.demand_emplo
    f.p.demand_emplo_new = (
        f.p_petrol.demand_emplo_new
        + f.p_jetfuel.demand_emplo_new
        + f.p_diesel.demand_emplo_new
        + f.p_emethan.demand_emplo_new
        + f.p_hydrogen.demand_emplo_new
        + f.p_hydrogen_reconv.demand_emplo_new
    )  # SUM(p_petrol.demand_emplo_new:p_hydrogen_reconv.demand_emplo_new)
    f.f.demand_emplo_new = f.p.demand_emplo_new

    #only for fuel pdf text
    f.p_hydrogen_total.energy = f.p_hydrogen.energy + f.p_hydrogen_reconv.energy
    f.p_efuels.energy = f.p_petrol.energy + f.p_diesel.energy + f.p_jetfuel.energy
    f.p_efuels.change_CO2e_t = f.p_petrol.change_CO2e_t + f.p_diesel.change_CO2e_t + f.p_jetfuel.change_CO2e_t
    #------------
