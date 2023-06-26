"""
Documentation:
    - missing :-(
    - This primarily models organic waste treatment and landfilling, we do not
      model industrial waste treatment.
"""

# pyright: strict


from dataclasses import dataclass
import math

from ..makeentries import Entries
from ..refdata import Facts, Assumptions
from ..utils import div
from ..waste2018 import W18


@dataclass(kw_only=True)
class EnergySupplyDetail:
    energy: float
    CO2e_combustion_based: float
    CO2e_cb_per_MWh: float
    CO2e_total: float
    change_energy_MWh: float
    change_energy_pct: float
    change_CO2e_t: float
    change_CO2e_pct: float
    CO2e_total_2021_estimated: float
    cost_climate_saved: float

    @classmethod
    def calc(
        cls,
        entries: Entries,
        facts: Facts,
        energy: float,
        CO2e_cb_per_MWh: float,
        w18: W18,
    ):
        fact = facts.fact

        CO2e_cb = CO2e_cb_per_MWh * energy
        CO2e_total = CO2e_cb
        change_energy_MWh = energy - w18.s_elec.energy
        change_energy_pct = div(change_energy_MWh, w18.s_elec.energy)
        change_CO2e_t = CO2e_total - w18.s_elec.CO2e_total
        change_CO2e_pct = div(change_CO2e_t, w18.s_elec.CO2e_total)
        CO2e_total_2021_estimated = w18.s_elec.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            energy=energy,
            CO2e_cb_per_MWh=CO2e_cb_per_MWh,
            CO2e_combustion_based=CO2e_cb,
            CO2e_total=CO2e_total,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            change_CO2e_t=change_CO2e_t,
            change_CO2e_pct=change_CO2e_pct,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            cost_climate_saved=cost_climate_saved,
        )


@dataclass(kw_only=True)
class Landfilling:
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    cost_climate_saved: float

    @classmethod
    def calc(cls, entries: Entries, facts: Facts, assumptions: Assumptions, w18: W18):
        fact = facts.fact
        ass = assumptions.ass

        # In germany since 2005 we have stricter standards for waste separation / cover on
        # land fills. That means newer landfills produce less methan.
        # But we have lots of old landfills hence the exp function to model the decay over
        # time.  Socket value and decay are taken from various studies (see comments on the
        # assumptions)
        CO2e_pb = (
            (
                ass("Ass_W_P_landfilling_socket")
                + ass("Ass_W_P_landfilling_CO2e_pb_2005")
                * math.exp(
                    -(entries.m_year_target - 2005)
                    / ass("Ass_W_P_landfilling_methane_decay")
                )
            )
            * entries.m_population_com_2018
            / entries.m_population_nat
        )
        CO2e_total = CO2e_pb
        change_CO2e_t = CO2e_total - w18.p_landfilling.CO2e_total
        change_CO2e_pct = change_CO2e_t / w18.p_landfilling.CO2e_total

        CO2e_total_2021_estimated = w18.p_landfilling.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        return cls(
            CO2e_production_based=CO2e_pb,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            cost_climate_saved=cost_climate_saved,
        )


@dataclass(kw_only=True)
class Organic_treatment:
    """Past 2005 we have a different method of treating organic waste in germany that is more climate friendly."""

    prod_volume: float
    CO2e_pb_per_t: float
    CO2e_production_based: float
    CO2e_total: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    cost_climate_saved: float
    invest_per_x: float
    ratio_wage_to_emplo: float
    pct_of_wage: float
    invest: float
    invest_com: float
    invest_pa: float
    invest_pa_com: float
    cost_wage: float
    demand_emplo: float
    demand_emplo_new: float

    @classmethod
    def calc(cls, entries: Entries, facts: Facts, assumptions: Assumptions, w18: W18):
        fact = facts.fact
        ass = assumptions.ass

        prod_volume = entries.m_population_com_203X * ass(
            "Ass_W_P_organic_treatment_prodvol_2050_per_capita"
        )
        CO2e_pb_per_t = ass("Ass_W_P_organic_treatment_CO2e_pb_2050_per_prodvol")
        CO2e_pb = prod_volume * CO2e_pb_per_t
        CO2e_total = CO2e_pb
        change_CO2e_t = CO2e_total - w18.p_organic_treatment.CO2e_total
        change_CO2e_pct = change_CO2e_t / w18.p_organic_treatment.CO2e_total

        CO2e_total_2021_estimated = w18.p_organic_treatment.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        invest_per_x = ass(
            "Ass_W_P_organic_treatment_fermentation_stage_invest_per_prodvol"
        )
        ratio_wage_to_emplo = fact("Fact_I_P_constr_civil_ratio_wage_to_emplo_2018")
        pct_of_wage = fact("Fact_I_P_constr_civil_revenue_pct_of_wage_2018")
        invest = prod_volume * invest_per_x
        invest_com = invest
        invest_pa = invest / entries.m_duration_target
        invest_pa_com = invest_pa
        cost_wage = invest_pa * pct_of_wage
        demand_emplo = cost_wage / ratio_wage_to_emplo
        demand_emplo_new = demand_emplo

        return cls(
            prod_volume=prod_volume,
            CO2e_pb_per_t=CO2e_pb_per_t,
            CO2e_production_based=CO2e_pb,
            CO2e_total=CO2e_total,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            cost_climate_saved=cost_climate_saved,
            invest_per_x=invest_per_x,
            ratio_wage_to_emplo=ratio_wage_to_emplo,
            pct_of_wage=pct_of_wage,
            invest=invest,
            invest_com=invest_com,
            invest_pa=invest_pa,
            invest_pa_com=invest_pa_com,
            cost_wage=cost_wage,
            demand_emplo=demand_emplo,
            demand_emplo_new=demand_emplo_new,
        )


@dataclass(kw_only=True)
class Wastewater:
    """Wastewater treatment."""

    energy: float
    prod_volume: float
    CO2e_pb_per_t: float
    CO2e_production_based: float
    CO2e_total: float
    change_energy_MWh: float
    change_energy_pct: float
    CO2e_total_2021_estimated: float
    change_CO2e_pct: float
    change_CO2e_t: float
    cost_climate_saved: float
    demand_electricity: float

    @classmethod
    def calc(cls, entries: Entries, facts: Facts, assumptions: Assumptions, w18: W18):
        fact = facts.fact
        ass = assumptions.ass

        prod_volume = entries.m_population_com_203X * ass(
            "Ass_W_P_wastewater_prodvol_2050_per_capita"
        )
        energy = w18.p_wastewater.energy * (prod_volume / w18.p_wastewater.prod_volume)

        CO2e_pb_per_t = ass("Ass_W_P_wastewater_CO2e_pb_2050_per_prodvol")
        CO2e_pb = prod_volume * CO2e_pb_per_t
        CO2e_total = CO2e_pb

        change_energy_MWh = energy - w18.p_wastewater.energy
        change_energy_pct = change_energy_MWh / w18.p_wastewater.energy

        change_CO2e_t = CO2e_total - w18.p_organic_treatment.CO2e_total
        change_CO2e_pct = div(change_CO2e_t, w18.p_organic_treatment.CO2e_total)

        CO2e_total_2021_estimated = w18.p_organic_treatment.CO2e_total * fact(
            "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
        )
        cost_climate_saved = (
            (CO2e_total_2021_estimated - CO2e_total)
            * entries.m_duration_neutral
            * fact("Fact_M_cost_per_CO2e_2020")
        )

        demand_electricity = w18.p_wastewater.demand_electricity * div(
            prod_volume, w18.p_wastewater.prod_volume
        )

        return cls(
            prod_volume=prod_volume,
            energy=energy,
            CO2e_pb_per_t=CO2e_pb_per_t,
            CO2e_production_based=CO2e_pb,
            CO2e_total=CO2e_total,
            change_energy_MWh=change_energy_MWh,
            change_energy_pct=change_energy_pct,
            CO2e_total_2021_estimated=CO2e_total_2021_estimated,
            change_CO2e_pct=change_CO2e_pct,
            change_CO2e_t=change_CO2e_t,
            cost_climate_saved=cost_climate_saved,
            demand_electricity=demand_electricity,
        )


@dataclass(kw_only=True)
class WasteLines:
    p_landfilling: Landfilling
    p_organic_treatment: Organic_treatment
    p_wastewater: Wastewater

    s_elec: EnergySupplyDetail

    @classmethod
    def calc_waste_lines(
        cls, entries: Entries, facts: Facts, assumptions: Assumptions, w18: W18
    ):
        p_landfilling = Landfilling.calc(entries, facts, assumptions, w18=w18)
        p_organic_treatment = Organic_treatment.calc(
            entries, facts, assumptions, w18=w18
        )
        p_wastewater = Wastewater.calc(entries, facts, assumptions, w18=w18)

        electricity_demand = p_wastewater.demand_electricity

        s_elec = EnergySupplyDetail.calc(
            entries, facts, w18=w18, energy=electricity_demand, CO2e_cb_per_MWh=0
        )

        return cls(
            p_landfilling=p_landfilling,
            p_organic_treatment=p_organic_treatment,
            p_wastewater=p_wastewater,
            s_elec=s_elec,
        )
