# pyright: strict

from ...refdata import Facts, Assumptions


def from_demands(
    facts: Facts,
    assumptions: Assumptions,
    *,
    demand_biodiesel: float = 0,
    demand_bioethanol: float = 0,
    demand_biogas: float = 0,
    demand_diesel: float = 0,
    demand_electricity: float = 0,
    demand_fueloil: float = 0,
    demand_gas: float = 0,
    demand_jetfuel: float = 0,
    demand_lpg: float = 0,
    demand_petrol: float = 0,
    demand_jetpetrol: float = 0,
) -> float:
    fact = facts.fact
    ass = assumptions.ass

    return (
        demand_biodiesel * ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
        + demand_bioethanol * ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
        + demand_biogas * ass("Ass_T_S_biogas_EmFa_tank_wheel")
        + demand_diesel * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
        + demand_electricity * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        + demand_fueloil * fact("Fact_T_S_fueloil_EmFa_tank_wheel_2018")
        + demand_gas * fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        + demand_jetfuel * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
        + demand_lpg * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        + demand_petrol * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
        + demand_jetpetrol * fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")
    )
