# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.energy import Energy


@dataclass(kw_only=True)
class EnergySupplySubBranch:
    total: Energy
    fossil: Energy
    fossil_gas: Energy
    fossil_coal: Energy
    fossil_diesel: Energy
    fossil_fueloil: Energy
    fossil_lpg: Energy
    fossil_opetpro: Energy
    fossil_ofossil: Energy
    renew: Energy
    renew_biomass: Energy
    renew_heatnet: Energy
    renew_elec: Energy
    renew_orenew: Energy

    @classmethod
    def calc_energy_supply_sub_branch(
        cls,
        inputs: Inputs,
        energy_demand: float,
        sub_branch: str,
        branch: str,
    ) -> "EnergySupplySubBranch":

        fact = inputs.fact

        branch_energy_supply = energy_demand

        fact_prefix = "Fact_I_S_" + branch + "_" + sub_branch + "_fec_pct_of_"

        fec_pct_gas = fact(fact_prefix + "gas" + "_2018")
        fossil_gas = Energy(energy=branch_energy_supply * fec_pct_gas)

        fec_pct_coal = fact(fact_prefix + "coal" + "_2018")
        fossil_coal = Energy(energy=branch_energy_supply * fec_pct_coal)

        fec_pct_diesel = fact(fact_prefix + "diesel" + "_2018")
        fossil_diesel = Energy(energy=branch_energy_supply * fec_pct_diesel)

        fec_pct_fueloil = fact(fact_prefix + "fueloil" + "_2018")
        fossil_fueloil = Energy(energy=branch_energy_supply * fec_pct_fueloil)

        fec_pct_lpg = fact(fact_prefix + "lpg" + "_2018")
        fossil_lpg = Energy(energy=branch_energy_supply * fec_pct_lpg)

        fec_pct_opetpro = fact(fact_prefix + "opetpro" + "_2018")
        fossil_opetpro = Energy(energy=branch_energy_supply * fec_pct_opetpro)

        fec_pct_ofossil = fact(fact_prefix + "ofossil" + "_2018")
        fossil_ofossil = Energy(energy=branch_energy_supply * fec_pct_ofossil)

        fossil = Energy(
            energy=fossil_gas.energy
            + fossil_coal.energy
            + fossil_diesel.energy
            + fossil_fueloil.energy
            + fossil_lpg.energy
            + fossil_opetpro.energy
            + fossil_ofossil.energy
        )

        fec_pct_biomass = fact(fact_prefix + "biomass" + "_2018")
        renew_biomass = Energy(energy=branch_energy_supply * fec_pct_biomass)

        fec_pct_heatnet = fact(fact_prefix + "heatnet" + "_2018")
        renew_heatnet = Energy(energy=branch_energy_supply * fec_pct_heatnet)

        fec_pct_elec = fact(fact_prefix + "elec" + "_2018")
        renew_elec = Energy(energy=branch_energy_supply * fec_pct_elec)

        fec_pct_orenew = fact(fact_prefix + "orenew" + "_2018")
        renew_orenew = Energy(energy=branch_energy_supply * fec_pct_orenew)

        renew = Energy(
            energy=renew_biomass.energy
            + renew_heatnet.energy
            + renew_orenew.energy
            + renew_elec.energy
        )

        total = Energy(energy=branch_energy_supply)

        return cls(
            total=total,
            fossil=fossil,
            fossil_gas=fossil_gas,
            fossil_coal=fossil_coal,
            fossil_diesel=fossil_diesel,
            fossil_fueloil=fossil_fueloil,
            fossil_lpg=fossil_lpg,
            fossil_opetpro=fossil_opetpro,
            fossil_ofossil=fossil_ofossil,
            renew=renew,
            renew_biomass=renew_biomass,
            renew_heatnet=renew_heatnet,
            renew_orenew=renew_orenew,
            renew_elec=renew_elec,
        )


@dataclass(kw_only=True)
class EnergySupplyBranch:
    total: Energy
    fossil: Energy
    fossil_gas: Energy
    fossil_coal: Energy
    fossil_diesel: Energy
    fossil_fueloil: Energy
    fossil_lpg: Energy
    fossil_opetpro: Energy
    fossil_ofossil: Energy
    renew: Energy
    renew_biomass: Energy
    renew_heatnet: Energy
    renew_elec: Energy
    renew_orenew: Energy

    @classmethod
    def calc_energy_supply_sum(
        cls, sub_branch_list: list[EnergySupplySubBranch]
    ) -> "EnergySupplyBranch":
        total = 0
        fossil = 0
        fossil_gas = 0
        fossil_coal = 0
        fossil_diesel = 0
        fossil_fueloil = 0
        fossil_lpg = 0
        fossil_opetpro = 0
        fossil_ofossil = 0
        renew = 0
        renew_biomass = 0
        renew_heatnet = 0
        renew_elec = 0
        renew_orenew = 0

        for sub_branch in sub_branch_list:
            total += sub_branch.total.energy
            fossil += sub_branch.fossil.energy
            fossil_gas += sub_branch.fossil_gas.energy
            fossil_coal += sub_branch.fossil_coal.energy
            fossil_diesel += sub_branch.fossil_diesel.energy
            fossil_fueloil += sub_branch.fossil_fueloil.energy
            fossil_lpg += sub_branch.fossil_lpg.energy
            fossil_opetpro += sub_branch.fossil_opetpro.energy
            fossil_ofossil += sub_branch.fossil_ofossil.energy
            renew += sub_branch.renew.energy
            renew_biomass += sub_branch.renew_biomass.energy
            renew_heatnet += sub_branch.renew_heatnet.energy
            renew_elec += sub_branch.renew_elec.energy
            renew_orenew += sub_branch.renew_orenew.energy

        total = Energy(energy=total)
        fossil = Energy(energy=fossil)
        fossil_gas = Energy(energy=fossil_gas)
        fossil_coal = Energy(energy=fossil_coal)
        fossil_diesel = Energy(energy=fossil_diesel)
        fossil_fueloil = Energy(energy=fossil_fueloil)
        fossil_lpg = Energy(energy=fossil_lpg)
        fossil_opetpro = Energy(energy=fossil_opetpro)
        fossil_ofossil = Energy(energy=fossil_ofossil)
        renew = Energy(energy=renew)
        renew_biomass = Energy(energy=renew_biomass)
        renew_heatnet = Energy(energy=renew_heatnet)
        renew_elec = Energy(energy=renew_elec)
        renew_orenew = Energy(energy=renew_orenew)

        return cls(
            total=total,
            fossil=fossil,
            fossil_gas=fossil_gas,
            fossil_coal=fossil_coal,
            fossil_diesel=fossil_diesel,
            fossil_fueloil=fossil_fueloil,
            fossil_lpg=fossil_lpg,
            fossil_opetpro=fossil_opetpro,
            fossil_ofossil=fossil_ofossil,
            renew=renew,
            renew_biomass=renew_biomass,
            renew_heatnet=renew_heatnet,
            renew_elec=renew_elec,
            renew_orenew=renew_orenew,
        )


@dataclass(kw_only=True)
class EnergySupplySum:
    total: Energy
    fossil: Energy
    fossil_gas: Energy
    fossil_coal: Energy
    fossil_diesel: Energy
    fossil_fueloil: Energy
    fossil_lpg: Energy
    fossil_opetpro: Energy
    fossil_ofossil: Energy
    renew: Energy
    renew_biomass: Energy
    renew_heatnet: Energy
    renew_elec: Energy
    renew_orenew: Energy

    @classmethod
    def calc_energy_supply_sum(
        cls, branch_list: list[EnergySupplyBranch]
    ) -> "EnergySupplySum":

        total = 0
        fossil = 0
        fossil_gas = 0
        fossil_coal = 0
        fossil_diesel = 0
        fossil_fueloil = 0
        fossil_lpg = 0
        fossil_opetpro = 0
        fossil_ofossil = 0
        renew = 0
        renew_biomass = 0
        renew_heatnet = 0
        renew_elec = 0
        renew_orenew = 0

        for branch in branch_list:
            total += branch.total.energy
            fossil += branch.fossil.energy
            fossil_gas += branch.fossil_gas.energy
            fossil_coal += branch.fossil_coal.energy
            fossil_diesel += branch.fossil_diesel.energy
            fossil_fueloil += branch.fossil_fueloil.energy
            fossil_lpg += branch.fossil_lpg.energy
            fossil_opetpro += branch.fossil_opetpro.energy
            fossil_ofossil += branch.fossil_ofossil.energy
            renew += branch.renew.energy
            renew_biomass += branch.renew_biomass.energy
            renew_heatnet += branch.renew_heatnet.energy
            renew_elec += branch.renew_elec.energy
            renew_orenew += branch.renew_orenew.energy

        total = Energy(energy=total)
        fossil = Energy(energy=fossil)
        fossil_gas = Energy(energy=fossil_gas)
        fossil_coal = Energy(energy=fossil_coal)
        fossil_diesel = Energy(energy=fossil_diesel)
        fossil_fueloil = Energy(energy=fossil_fueloil)
        fossil_lpg = Energy(energy=fossil_lpg)
        fossil_opetpro = Energy(energy=fossil_opetpro)
        fossil_ofossil = Energy(energy=fossil_ofossil)
        renew = Energy(energy=renew)
        renew_biomass = Energy(energy=renew_biomass)
        renew_heatnet = Energy(energy=renew_heatnet)
        renew_elec = Energy(energy=renew_elec)
        renew_orenew = Energy(energy=renew_orenew)

        return cls(
            total=total,
            fossil=fossil,
            fossil_gas=fossil_gas,
            fossil_coal=fossil_coal,
            fossil_diesel=fossil_diesel,
            fossil_fueloil=fossil_fueloil,
            fossil_lpg=fossil_lpg,
            fossil_opetpro=fossil_opetpro,
            fossil_ofossil=fossil_ofossil,
            renew=renew,
            renew_biomass=renew_biomass,
            renew_heatnet=renew_heatnet,
            renew_elec=renew_elec,
            renew_orenew=renew_orenew,
        )
