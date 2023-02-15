# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..common.energy import Energy, EnergyWithPercentage


@dataclass(kw_only=True)
class EnergySourceSubBranch:
    s: Energy
    s_fossil: Energy
    s_fossil_gas: Energy
    s_fossil_coal: Energy
    s_fossil_diesel: Energy
    s_fossil_fueloil: Energy
    s_fossil_lpg: Energy
    s_fossil_opetpro: Energy
    s_fossil_ofossil: Energy
    s_renew: Energy
    s_renew_biomass: Energy
    s_renew_heatnet: Energy
    s_renew_elec: Energy
    s_renew_orenew: Energy

    @classmethod
    def _get_energy_pct_fact(
        cls, inputs: Inputs, sub_branch: str, branch: str, energy_type: str
    ) -> float:
        fact = inputs.fact
        fact_name = (
            "Fact_I_S_"
            + branch
            + "_"
            + sub_branch
            + "_fec_pct_of_"
            + energy_type
            + "_2018"
        )
        # add 0% facts in table -> remove try block

        fec_pct = fact(fact_name)

        return fec_pct

    @classmethod
    def calc_energy_source_sub_branch(
        cls,
        inputs: Inputs,
        energy_demand: float,
        sub_branch: str,
        branch: str,
    ) -> "EnergySourceSubBranch":

        branch_energy_supply = energy_demand

        fec_pct_gas = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="gas"
        )
        s_fossil_gas = Energy(energy=branch_energy_supply * fec_pct_gas)
        fec_pct_coal = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="coal"
        )
        s_fossil_coal = Energy(energy=branch_energy_supply * fec_pct_coal)
        fec_pct_diesel = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="diesel"
        )
        s_fossil_diesel = Energy(energy=branch_energy_supply * fec_pct_diesel)
        fec_pct_fueloil = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="fueloil"
        )
        s_fossil_fueloil = Energy(energy=branch_energy_supply * fec_pct_fueloil)
        fec_pct_lpg = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="lpg"
        )
        s_fossil_lpg = Energy(energy=branch_energy_supply * fec_pct_lpg)
        fec_pct_opetpro = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="opetpro"
        )
        s_fossil_opetpro = Energy(energy=branch_energy_supply * fec_pct_opetpro)
        fec_pct_ofossil = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="ofossil"
        )
        s_fossil_ofossil = Energy(energy=branch_energy_supply * fec_pct_ofossil)

        s_fossil = Energy(
            energy=s_fossil_gas.energy
            + s_fossil_coal.energy
            + s_fossil_diesel.energy
            + s_fossil_fueloil.energy
            + s_fossil_lpg.energy
            + s_fossil_opetpro.energy
            + s_fossil_ofossil.energy
        )

        fec_pct_biomass = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="biomass"
        )
        s_renew_biomass = Energy(energy=branch_energy_supply * fec_pct_biomass)
        fec_pct_heatnet = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="heatnet"
        )
        s_renew_heatnet = Energy(energy=branch_energy_supply * fec_pct_heatnet)
        fec_pct_heatpump = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="heatpump"
        )
        s_renew_heatpump = Energy(energy=branch_energy_supply * fec_pct_heatpump)
        fec_pct_elec = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="elec"
        )
        s_renew_elec = Energy(energy=branch_energy_supply * fec_pct_elec)
        fec_pct_orenew = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="orenew"
        )
        s_renew_orenew = Energy(energy=branch_energy_supply * fec_pct_orenew)

        s_renew = Energy(
            energy=s_renew_biomass.energy
            + s_renew_heatnet.energy
            + s_renew_heatpump.energy
            + s_renew_orenew.energy
            + s_renew_elec.energy
        )

        s = Energy(energy=branch_energy_supply)

        return cls(
            s=s,
            s_fossil=s_fossil,
            s_fossil_gas=s_fossil_gas,
            s_fossil_coal=s_fossil_coal,
            s_fossil_diesel=s_fossil_diesel,
            s_fossil_fueloil=s_fossil_fueloil,
            s_fossil_lpg=s_fossil_lpg,
            s_fossil_opetpro=s_fossil_opetpro,
            s_fossil_ofossil=s_fossil_ofossil,
            s_renew=s_renew,
            s_renew_biomass=s_renew_biomass,
            s_renew_heatnet=s_renew_heatnet,
            s_renew_orenew=s_renew_orenew,
            s_renew_elec=s_renew_elec,
        )


@dataclass(kw_only=True)
class EnergySourceBranch:
    s: Energy
    s_fossil: Energy
    s_fossil_gas: Energy
    s_fossil_coal: Energy
    s_fossil_diesel: Energy
    s_fossil_fueloil: Energy
    s_fossil_lpg: Energy
    s_fossil_opetpro: Energy
    s_fossil_ofossil: Energy
    s_renew: Energy
    s_renew_biomass: Energy
    s_renew_heatnet: Energy
    s_renew_elec: Energy
    s_renew_orenew: Energy

    @classmethod
    def calc_energy_source_sum(
        cls, sub_branch_list: list[EnergySourceSubBranch]
    ) -> "EnergySourceBranch":
        s = 0
        s_fossil = 0
        s_fossil_gas = 0
        s_fossil_coal = 0
        s_fossil_diesel = 0
        s_fossil_fueloil = 0
        s_fossil_lpg = 0
        s_fossil_opetpro = 0
        s_fossil_ofossil = 0
        s_renew = 0
        s_renew_biomass = 0
        s_renew_heatnet = 0
        s_renew_elec = 0
        s_renew_orenew = 0

        for sub_branch in sub_branch_list:
            s += sub_branch.s.energy
            s_fossil += sub_branch.s_fossil.energy
            s_fossil_gas += sub_branch.s_fossil_gas.energy
            s_fossil_coal += sub_branch.s_fossil_coal.energy
            s_fossil_diesel += sub_branch.s_fossil_diesel.energy
            s_fossil_fueloil += sub_branch.s_fossil_fueloil.energy
            s_fossil_lpg += sub_branch.s_fossil_lpg.energy
            s_fossil_opetpro += sub_branch.s_fossil_opetpro.energy
            s_fossil_ofossil += sub_branch.s_fossil_ofossil.energy
            s_renew += sub_branch.s_renew.energy
            s_renew_biomass += sub_branch.s_renew_biomass.energy
            s_renew_heatnet += sub_branch.s_renew_heatnet.energy
            s_renew_elec += sub_branch.s_renew_elec.energy
            s_renew_orenew += sub_branch.s_renew_orenew.energy

        s = Energy(energy=s)
        s_fossil = Energy(energy=s_fossil)
        s_fossil_gas = Energy(energy=s_fossil_gas)
        s_fossil_coal = Energy(energy=s_fossil_coal)
        s_fossil_diesel = Energy(energy=s_fossil_diesel)
        s_fossil_fueloil = Energy(energy=s_fossil_fueloil)
        s_fossil_lpg = Energy(energy=s_fossil_lpg)
        s_fossil_opetpro = Energy(energy=s_fossil_opetpro)
        s_fossil_ofossil = Energy(energy=s_fossil_ofossil)
        s_renew = Energy(energy=s_renew)
        s_renew_biomass = Energy(energy=s_renew_biomass)
        s_renew_heatnet = Energy(energy=s_renew_heatnet)
        s_renew_elec = Energy(energy=s_renew_elec)
        s_renew_orenew = Energy(energy=s_renew_orenew)

        return cls(
            s=s,
            s_fossil=s_fossil,
            s_fossil_gas=s_fossil_gas,
            s_fossil_coal=s_fossil_coal,
            s_fossil_diesel=s_fossil_diesel,
            s_fossil_fueloil=s_fossil_fueloil,
            s_fossil_lpg=s_fossil_lpg,
            s_fossil_opetpro=s_fossil_opetpro,
            s_fossil_ofossil=s_fossil_ofossil,
            s_renew=s_renew,
            s_renew_biomass=s_renew_biomass,
            s_renew_heatnet=s_renew_heatnet,
            s_renew_elec=s_renew_elec,
            s_renew_orenew=s_renew_orenew,
        )


@dataclass(kw_only=True)
class EnergySourceSum:
    s: EnergyWithPercentage
    s_fossil: Energy
    s_fossil_gas: EnergyWithPercentage
    s_fossil_coal: EnergyWithPercentage
    s_fossil_diesel: EnergyWithPercentage
    s_fossil_fueloil: EnergyWithPercentage
    s_fossil_lpg: EnergyWithPercentage
    s_fossil_opetpro: EnergyWithPercentage
    s_fossil_ofossil: EnergyWithPercentage
    s_renew: Energy
    s_renew_biomass: EnergyWithPercentage
    s_renew_heatnet: EnergyWithPercentage
    s_renew_elec: EnergyWithPercentage
    s_renew_orenew: EnergyWithPercentage

    @classmethod
    def calc_energy_source_sum(
        cls, branch_list: list[EnergySourceBranch]
    ) -> "EnergySourceSum":
        energy_sum = 0
        s = 0
        s_fossil = 0
        s_fossil_gas = 0
        s_fossil_coal = 0
        s_fossil_diesel = 0
        s_fossil_fueloil = 0
        s_fossil_lpg = 0
        s_fossil_opetpro = 0
        s_fossil_ofossil = 0
        s_renew = 0
        s_renew_biomass = 0
        s_renew_heatnet = 0
        s_renew_elec = 0
        s_renew_orenew = 0

        for branch in branch_list:
            energy_sum += branch.s.energy
            s += branch.s.energy
            s_fossil += branch.s_fossil.energy
            s_fossil_gas += branch.s_fossil_gas.energy
            s_fossil_coal += branch.s_fossil_coal.energy
            s_fossil_diesel += branch.s_fossil_diesel.energy
            s_fossil_fueloil += branch.s_fossil_fueloil.energy
            s_fossil_lpg += branch.s_fossil_lpg.energy
            s_fossil_opetpro += branch.s_fossil_opetpro.energy
            s_fossil_ofossil += branch.s_fossil_ofossil.energy
            s_renew += branch.s_renew.energy
            s_renew_biomass += branch.s_renew_biomass.energy
            s_renew_heatnet += branch.s_renew_heatnet.energy
            s_renew_elec += branch.s_renew_elec.energy
            s_renew_orenew += branch.s_renew_orenew.energy

        s = EnergyWithPercentage(energy=s, total_energy=energy_sum)
        s_fossil = Energy(energy=s_fossil)
        s_fossil_gas = EnergyWithPercentage(
            energy=s_fossil_gas, total_energy=energy_sum
        )
        s_fossil_coal = EnergyWithPercentage(
            energy=s_fossil_coal, total_energy=energy_sum
        )
        s_fossil_diesel = EnergyWithPercentage(
            energy=s_fossil_diesel, total_energy=energy_sum
        )
        s_fossil_fueloil = EnergyWithPercentage(
            energy=s_fossil_fueloil, total_energy=energy_sum
        )
        s_fossil_lpg = EnergyWithPercentage(
            energy=s_fossil_lpg, total_energy=energy_sum
        )
        s_fossil_opetpro = EnergyWithPercentage(
            energy=s_fossil_opetpro, total_energy=energy_sum
        )
        s_fossil_ofossil = EnergyWithPercentage(
            energy=s_fossil_ofossil, total_energy=energy_sum
        )
        s_renew = Energy(energy=s_renew)
        s_renew_biomass = EnergyWithPercentage(
            energy=s_renew_biomass, total_energy=energy_sum
        )
        s_renew_heatnet = EnergyWithPercentage(
            energy=s_renew_heatnet, total_energy=energy_sum
        )
        s_renew_elec = EnergyWithPercentage(
            energy=s_renew_elec, total_energy=energy_sum
        )
        s_renew_orenew = EnergyWithPercentage(
            energy=s_renew_orenew, total_energy=energy_sum
        )

        return cls(
            s=s,
            s_fossil=s_fossil,
            s_fossil_gas=s_fossil_gas,
            s_fossil_coal=s_fossil_coal,
            s_fossil_diesel=s_fossil_diesel,
            s_fossil_fueloil=s_fossil_fueloil,
            s_fossil_lpg=s_fossil_lpg,
            s_fossil_opetpro=s_fossil_opetpro,
            s_fossil_ofossil=s_fossil_ofossil,
            s_renew=s_renew,
            s_renew_biomass=s_renew_biomass,
            s_renew_heatnet=s_renew_heatnet,
            s_renew_elec=s_renew_elec,
            s_renew_orenew=s_renew_orenew,
        )
