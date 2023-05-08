"""
Documentation:
https://localzero-generator.readthedocs.io/de/latest/sectors/agriculture.html
"""

# pyright: strict

from dataclasses import dataclass
from ..inputs import Inputs


@dataclass(kw_only=True)
class WasteBranch:
    energy: float
    prod_volume: float
    demand_electricity: float
    CO2e_production_based: float
    CO2e_production_based_per_t: float
    CO2e_total: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        use_prod_vol: bool,
        CO2e_pb_per_t: float,
        prod_vol_per_cap: float = 0,
        energy: float = 0,
    ):
        entries = inputs.entries
        prod_vol = entries.m_population_com_2018 * prod_vol_per_cap
        if use_prod_vol:
            CO2e_pb = CO2e_pb_per_t * prod_vol
        else:
            CO2e_pb = CO2e_pb_per_t * entries.m_population_com_2018

        CO2e_total = CO2e_pb
        demand_electricity = energy
        return cls(
            energy=energy,
            prod_volume=prod_vol,
            demand_electricity=demand_electricity,
            CO2e_production_based_per_t=CO2e_pb_per_t,
            CO2e_production_based=CO2e_pb,
            CO2e_total=CO2e_total,
        )


@dataclass(kw_only=True)
class EnergyProduction:
    energy: float
    prod_volume: float
    CO2e_production_based: float
    CO2e_total: float

    @classmethod
    def calc(cls, *waste_lines: WasteBranch):

        energy = sum([line.energy for line in waste_lines])
        prod_vol = sum([line.prod_volume for line in waste_lines])
        CO2e_pb = sum([line.CO2e_production_based for line in waste_lines])
        CO2e_total = sum([line.CO2e_total for line in waste_lines])

        return cls(
            energy=energy,
            prod_volume=prod_vol,
            CO2e_production_based=CO2e_pb,
            CO2e_total=CO2e_total,
        )


@dataclass(kw_only=True)
class EnergySupplyDetail:
    energy: float
    CO2e_combustion_based: float
    CO2e_cb_per_MWh: float
    CO2e_total: float

    @classmethod
    def calc(cls, energy: float, CO2e_cb_per_MWh: float):
        CO2e_cb = CO2e_cb_per_MWh * energy
        return cls(
            energy=energy,
            CO2e_cb_per_MWh=CO2e_cb_per_MWh,
            CO2e_combustion_based=CO2e_cb,
            CO2e_total=CO2e_cb,
        )


@dataclass(kw_only=True)
class EnergySupply:
    energy: float
    CO2e_combustion_based: float
    CO2e_total: float

    @classmethod
    def calc(cls, *energy_supplies: EnergySupplyDetail):

        energy = sum([supply.energy for supply in energy_supplies])
        CO2e_cb = sum([supply.CO2e_combustion_based for supply in energy_supplies])
        CO2e_total = sum([supply.CO2e_total for supply in energy_supplies])

        return cls(energy=energy, CO2e_combustion_based=CO2e_cb, CO2e_total=CO2e_total)


@dataclass(kw_only=True)
class W18:
    w: EnergyProduction
    p: EnergyProduction
    p_landfilling: WasteBranch
    p_organic_treatment: WasteBranch
    p_wastewater: WasteBranch

    s: EnergySupply
    s_elec: EnergySupplyDetail

    @classmethod
    def calc(cls, inputs: Inputs):

        entries = inputs.entries
        fact = inputs.fact

        s_elec = EnergySupplyDetail.calc(energy=entries.w_elec_fec, CO2e_cb_per_MWh=0)
        s = EnergySupply.calc(s_elec)

        p_landfilling = WasteBranch.calc(
            inputs=inputs,
            energy=0,
            use_prod_vol=False,
            CO2e_pb_per_t=fact("Fact_W_P_landfilling_CO2e_pb_2018_per_capita"),
        )
        p_organic_treatment = WasteBranch.calc(
            inputs=inputs,
            energy=0,
            use_prod_vol=True,
            prod_vol_per_cap=fact("Fact_W_P_organic_treatment_prodvol_2018_per_capita"),
            CO2e_pb_per_t=fact("Fact_W_P_organic_treatment_CO2e_pb_2018_per_prodvol"),
        )
        p_wastewater = WasteBranch.calc(
            inputs=inputs,
            energy=entries.w_elec_fec,
            use_prod_vol=True,
            prod_vol_per_cap=fact("Fact_W_P_wastewater_prodvol_2018_per_capita"),
            CO2e_pb_per_t=fact("Fact_W_P_wastewater_CO2e_pb_2018_per_prodvol"),
        )

        p = EnergyProduction.calc(p_landfilling, p_organic_treatment, p_wastewater)
        w = p
        return cls(
            w=w,
            p=p,
            p_landfilling=p_landfilling,
            p_organic_treatment=p_organic_treatment,
            p_wastewater=p_wastewater,
            s=s,
            s_elec=s_elec,
        )
