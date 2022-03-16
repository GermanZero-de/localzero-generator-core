from dataclasses import dataclass
from ..inputs import Inputs
from ..utils import div


@dataclass
class InvestmentAction:
    """For some transport mechanism additional investments are needed."""

    # Used by road_gds_mhd_action_wire, other_foot_action_infra, other_cycl_action_infra, rail_action_invest_infra, rail_action_invest_station, road_bus_action_infra
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    invest_per_x: float
    pct_of_wage: float
    ratio_wage_to_emplo: float

    @classmethod
    def calc_rail_action_invest_infra(cls, inputs: Inputs) -> "InvestmentAction":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_rail_infrstrctr")
        invest = invest_per_x * entries.m_population_com_203X
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        demand_emplo = div(
            cost_wage,
            ratio_wage_to_emplo,
        )
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        demand_emplo_new = demand_emplo
        invest_pa_com = invest_com / entries.m_duration_target

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_rail_action_invest_station(cls, inputs: Inputs) -> "InvestmentAction":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_rail_train station")
        invest = invest_per_x * entries.m_population_com_203X
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_com = invest_com / entries.m_duration_target
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        demand_emplo = div(
            cost_wage,
            ratio_wage_to_emplo,
        )
        demand_emplo_new = demand_emplo

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_other_foot_action_infra(cls, inputs: Inputs) -> "InvestmentAction":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        invest_per_x = ass("Ass_T_D_invest_pedestrians")
        invest_pa = invest_per_x * entries.m_population_com_203X
        invest = invest_pa * entries.m_duration_target
        invest_com = invest
        invest_pa_com = invest_pa
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        demand_emplo_new = demand_emplo

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )

    @classmethod
    def calc_other_cycl_action_infra(
        cls, inputs: Inputs, cycle_transport_capacity_pkm: float
    ) -> "InvestmentAction":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        invest_per_x = ass("Ass_T_C_cost_per_trnsprt_ppl_cycle")
        invest = cycle_transport_capacity_pkm * invest_per_x
        invest_com = invest * ass("Ass_T_C_ratio_public_sector_100")
        invest_pa_com = invest_com / entries.m_duration_target
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        invest_pa = invest / entries.m_duration_target
        cost_wage = invest_pa * pct_of_wage
        demand_emplo = div(
            cost_wage,
            ratio_wage_to_emplo,
        )
        demand_emplo_new = demand_emplo

        return cls(
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )


@dataclass
class RoadInvestmentAction(InvestmentAction):
    # Used by road_action_charger
    base_unit: float

    @classmethod
    def calc_car_action_charger(
        cls, inputs: Inputs, car_base_unit: float
    ) -> "RoadInvestmentAction":
        ass = inputs.ass
        fact = inputs.fact
        entries = inputs.entries

        # Divide cars by chargers/car => chargers
        base_unit = car_base_unit / (
            ass("Ass_S_ratio_bev_car_per_charge_point_city")
            if entries.t_rt3 == "city"
            else ass("Ass_S_ratio_bev_car_per_charge_point_smcity_rural")
            if entries.t_rt3 == "smcty"
            else ass("Ass_S_ratio_bev_car_per_charge_point_smcity_rural")
            if entries.t_rt3 == "rural"
            else ass("Ass_S_ratio_bev_car_per_charge_point_nat")
        )
        invest_per_x = ass("Ass_T_C_cost_per_charge_point")
        invest = base_unit * invest_per_x
        invest_pa = invest / entries.m_duration_target
        pct_of_wage = fact("Fact_T_D_constr_roadrail_revenue_pct_of_wage_2018")
        invest_com = invest * ass("Ass_T_C_invest_state_charge_point_prctg")
        cost_wage = invest_pa * pct_of_wage
        ratio_wage_to_emplo = fact("Fact_T_D_constr_roadrail_ratio_wage_to_emplo_2018")
        demand_emplo = div(cost_wage, ratio_wage_to_emplo)
        invest_pa_com = invest_com / entries.m_duration_target
        demand_emplo_new = demand_emplo
        return cls(
            base_unit=base_unit,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            invest_per_x=invest_per_x,
            pct_of_wage=pct_of_wage,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
        )
