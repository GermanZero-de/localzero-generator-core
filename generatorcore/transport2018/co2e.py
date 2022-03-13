from ..inputs import Inputs


def from_demands(
    inputs: Inputs,
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
    return (
        demand_biodiesel * inputs.ass("Ass_T_S_biodiesel_EmFa_tank_wheel")
        + demand_bioethanol * inputs.ass("Ass_T_S_bioethanol_EmFa_tank_wheel")
        + demand_biogas * inputs.ass("Ass_T_S_biogas_EmFa_tank_wheel")
        + demand_diesel * inputs.fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
        + demand_electricity * inputs.fact("Fact_T_S_electricity_EmFa_tank_wheel_2018")
        + demand_fueloil * inputs.fact("Fact_T_S_fueloil_EmFa_tank_wheel_2018")
        + demand_gas * inputs.fact("Fact_T_S_cng_EmFa_tank_wheel_2018")
        + demand_jetfuel * inputs.fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018")
        + demand_lpg * inputs.fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
        + demand_petrol * inputs.fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
        + demand_jetpetrol * inputs.fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")
    )
