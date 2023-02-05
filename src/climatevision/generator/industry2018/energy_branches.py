# pyright: strict

from dataclasses import dataclass

from ..inputs import Inputs
from ..common.energy import Energy, EnergyWithPercentage


@dataclass(kw_only=True)
class EnergySourceSubBranch:
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
    def _get_energy_pct_fact(
        cls, inputs: Inputs, sub_branch: str, branch: str, energy_type: str
    ) -> float:
        fact = inputs.fact
        fact_name = "Fact_I_P_" + branch + "_" + sub_branch + "_fec_pct_of_coal_2018"
        try:
            fec_pct = fact(fact_name)
        except:  # add error type
            fec_pct = 0.0

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

        # add calculation with new facts here:

        fec_pct_gas = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="gas"
        )
        i_gas_fec = branch_energy_supply * fec_pct_gas
        s_fossil_gas = EnergyWithPercentage(
            energy=i_gas_fec, total_energy=branch_energy_supply
        )
        fec_pct_coal = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="coal"
        )
        i_coal_fec = branch_energy_supply * fec_pct_coal
        s_fossil_coal = EnergyWithPercentage(
            energy=i_coal_fec, total_energy=branch_energy_supply
        )
        fec_pct_diesel = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="diesel"
        )
        i_diesel_fec = branch_energy_supply * fec_pct_diesel
        s_fossil_diesel = EnergyWithPercentage(
            energy=i_diesel_fec, total_energy=branch_energy_supply
        )
        fec_pct_fueloil = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="fueloil"
        )
        i_fueloil_fec = branch_energy_supply * fec_pct_fueloil
        s_fossil_fueloil = EnergyWithPercentage(
            energy=i_fueloil_fec, total_energy=branch_energy_supply
        )
        fec_pct_lpg = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="lpg"
        )
        i_lpg_fec = branch_energy_supply * fec_pct_lpg
        s_fossil_lpg = EnergyWithPercentage(
            energy=i_lpg_fec, total_energy=branch_energy_supply
        )
        fec_pct_opetpro = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="opetpro"
        )
        i_opetpro_fec = branch_energy_supply * fec_pct_opetpro
        s_fossil_opetpro = EnergyWithPercentage(
            energy=i_opetpro_fec, total_energy=branch_energy_supply
        )
        fec_pct_ofossil = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="ofossil"
        )
        i_ofossil_fec = branch_energy_supply * fec_pct_ofossil
        s_fossil_ofossil = EnergyWithPercentage(
            energy=i_ofossil_fec, total_energy=branch_energy_supply
        )

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
        i_biomass_fec = branch_energy_supply * fec_pct_biomass
        s_renew_biomass = EnergyWithPercentage(
            energy=i_biomass_fec, total_energy=branch_energy_supply
        )
        fec_pct_heatnet = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="heatnet"
        )
        i_heatnet_fec = branch_energy_supply * fec_pct_heatnet
        s_renew_heatnet = EnergyWithPercentage(
            energy=i_heatnet_fec, total_energy=branch_energy_supply
        )
        fec_pct_heatpump = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="heatpump"
        )
        i_heatpump_fec = branch_energy_supply * fec_pct_heatpump
        s_renew_heatpump = EnergyWithPercentage(
            energy=i_heatpump_fec, total_energy=branch_energy_supply
        )
        fec_pct_elec = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="elec"
        )
        i_elec_fec = branch_energy_supply * fec_pct_elec
        s_renew_elec = EnergyWithPercentage(
            energy=i_elec_fec, total_energy=branch_energy_supply
        )
        fec_pct_orenew = cls._get_energy_pct_fact(
            inputs=inputs, sub_branch=sub_branch, branch=branch, energy_type="orenew"
        )
        i_orenew_fec = branch_energy_supply * fec_pct_orenew
        s_renew_orenew = EnergyWithPercentage(
            energy=i_orenew_fec, total_energy=branch_energy_supply
        )

        s_renew = Energy(
            energy=s_renew_biomass.energy
            + s_renew_heatnet.energy
            + s_renew_heatpump.energy
            + s_renew_orenew.energy
            + s_renew_elec.energy
        )

        s = EnergyWithPercentage(
            energy=branch_energy_supply, total_energy=branch_energy_supply
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
            s_renew_orenew=s_renew_orenew,
            s_renew_elec=s_renew_elec,
        )


@dataclass(kw_only=True)
class EnergySourceSubSum:
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
    def calc_energy_supply_sub_sum(
        cls,
        sub_branch_list: list[EnergySourceSubBranch]
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
            s += sub_branch.s.total_energy
            s_fossil += sub_branch.s_fossil
            s_fossil_gas += sub_branch.s_fossil_gas
            s_fossil_coal += sub_branch.s_fossil_coal
            s_fossil_diesel += sub_branch.s_fossil_diesel
            s_fossil_fueloil += sub_branch.s_fossil_fueloil
            s_fossil_lpg += sub_branch.s_fossil_lpg
            s_fossil_opetpro += sub_branch.s_fossil_opetpro
            s_fossil_ofossil += sub_branch.s_fossil_ofossil
            s_renew += sub_branch.s_renew.energy
            s_renew_biomass += sub_branch.s_renew_biomass
            s_renew_heatnet += sub_branch.s_renew_heatnet
            s_renew_elec += sub_branch.s_renew_elec
            s_renew_orenew += sub_branch.s_renew_orenew

        return cls(
            s = s
            s_fossil = s_fossil
            s_fossil_gas = s_fossil_gas
            s_fossil_coal = s_fossil_coal
            s_fossil_diesel = s_fossil_diesel
            s_fossil_fueloil = s_fossil_fueloil
            s_fossil_lpg = s_fossil_lpg
            s_fossil_opetpro = s_fossil_opetpro
            s_fossil_ofossil = s_fossil_ofossil
            s_renew = s_renew
            s_renew_biomass = s_renew_biomass
            s_renew_heatnet = s_renew_heatnet
            s_renew_elec = s_renew_elec
            s_renew_orenew = s_renew_orenew
        )

@dataclass(kw_only=True)
class EnergySourceBranch:
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
        cls,
        sub_branch_list: list[EnergySourceSubBranch | EnergySourceSubSum]
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
            s += sub_branch.s
            s_fossil += sub_branch.s_fossil
            s_fossil_gas += sub_branch.s_fossil_gas
            s_fossil_coal += sub_branch.s_fossil_coal
            s_fossil_diesel += sub_branch.s_fossil_diesel
            s_fossil_fueloil += sub_branch.s_fossil_fueloil
            s_fossil_lpg += sub_branch.s_fossil_lpg
            s_fossil_opetpro += sub_branch.s_fossil_opetpro
            s_fossil_ofossil += sub_branch.s_fossil_ofossil
            s_renew += sub_branch.s_renew
            s_renew_biomass += sub_branch.s_renew_biomass
            s_renew_heatnet += sub_branch.s_renew_heatnet
            s_renew_elec += sub_branch.s_renew_elec
            s_renew_orenew += sub_branch.s_renew_orenew

        return cls(
            s = s
            s_fossil = s_fossil
            s_fossil_gas = s_fossil_gas
            s_fossil_coal = s_fossil_coal
            s_fossil_diesel = s_fossil_diesel
            s_fossil_fueloil = s_fossil_fueloil
            s_fossil_lpg = s_fossil_lpg
            s_fossil_opetpro = s_fossil_opetpro
            s_fossil_ofossil = s_fossil_ofossil
            s_renew = s_renew
            s_renew_biomass = s_renew_biomass
            s_renew_heatnet = s_renew_heatnet
            s_renew_elec = s_renew_elec
            s_renew_orenew = s_renew_orenew
        )

@dataclass
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
    def calc_energy_source_sum(cls,) -> "EnergySourceSum":
        
        return cls(
            s = s
            s_fossil = s_fossil
            s_fossil_gas = s_fossil_gas
            s_fossil_coal = s_fossil_coal
            s_fossil_diesel = s_fossil_diesel
            s_fossil_fueloil = s_fossil_fueloil
            s_fossil_lpg = s_fossil_lpg
            s_fossil_opetpro = s_fossil_opetpro
            s_fossil_ofossil = s_fossil_ofossil
            s_renew = s_renew
            s_renew_biomass = s_renew_biomass
            s_renew_heatnet = s_renew_heatnet
            s_renew_elec = s_renew_elec
            s_renew_orenew = s_renew_orenew
        )