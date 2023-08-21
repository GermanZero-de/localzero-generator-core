# pyright: strict

from dataclasses import dataclass

from ....refdata import Facts
from ....utils import div
from ....electricity2018.e18 import E18
from ....agri2030.a30 import A30
from ....business2030.b30 import B30
from ....fuels2030.f30 import F30
from ....heat2030.h30 import H30
from ....industry2030.i30 import I30
from ....residences2030.r30 import R30
from ....transport2030.t30 import T30
from ....waste2030 import WasteLines

from ...core.energy import EnergyDemand, EnergyDemandWithCostFuel


@dataclass(kw_only=True)
class Demand:
    residences: EnergyDemandWithCostFuel
    business: EnergyDemandWithCostFuel
    heat: EnergyDemand
    industry: EnergyDemandWithCostFuel
    transport: EnergyDemandWithCostFuel
    agri: EnergyDemandWithCostFuel
    waste: EnergyDemand

    fuels_hydrogen_reconv: EnergyDemand
    fuels_wo_hydrogen: EnergyDemand

    total: EnergyDemand


def calc_demand(
    facts: Facts,
    e18: E18,
    a30: A30,
    b30: B30,
    f30: F30,
    h30: H30,
    i30: I30,
    r30: R30,
    t30: T30,
    wastelines: WasteLines,
) -> Demand:
    fact = facts.fact

    agri = EnergyDemandWithCostFuel(
        energy=a30.p_operation.demand_electricity,
        energy_18=e18.d_a.energy,
        cost_fuel_per_MWh=fact("Fact_E_D_R_cost_fuel_per_MWh_2018"),
    )
    business = EnergyDemandWithCostFuel(
        energy=b30.p.demand_electricity,
        energy_18=e18.d_b.energy,
        cost_fuel_per_MWh=fact("Fact_E_D_B_cost_fuel_per_MWh_2018"),
    )
    industry = EnergyDemandWithCostFuel(
        energy=i30.p.demand_electricity,
        energy_18=e18.d_i.energy,
        cost_fuel_per_MWh=fact("Fact_E_D_I_cost_fuel_per_MWh_2018"),
    )
    residences = EnergyDemandWithCostFuel(
        energy=r30.p.demand_electricity,
        energy_18=e18.d_r.energy,
        cost_fuel_per_MWh=fact("Fact_E_D_R_cost_fuel_per_MWh_2018"),
    )
    transport = EnergyDemandWithCostFuel(
        energy=t30.t.transport.demand_electricity,
        energy_18=e18.d_t.energy,
        cost_fuel_per_MWh=fact("Fact_E_D_R_cost_fuel_per_MWh_2018"),
    )

    waste = EnergyDemand(energy=wastelines.s_elec.energy)
    heat = EnergyDemand(energy=h30.p.demand_electricity)
    fuels_wo_hydrogen = EnergyDemand(
        energy=f30.p_petrol.demand_electricity
        + f30.p_jetfuel.demand_electricity
        + f30.p_diesel.demand_electricity
        + f30.p_emethan.demand_electricity
        + f30.p_hydrogen.demand_electricity
    )
    fuels_hydrogen_reconv = EnergyDemand(
        energy=f30.p_hydrogen_reconv.demand_electricity
    )
    total = EnergyDemand(
        energy=heat.energy
        + residences.energy
        + business.energy
        + industry.energy
        + transport.energy
        + agri.energy
        + waste.energy
        + fuels_wo_hydrogen.energy
        + fuels_hydrogen_reconv.energy
    )

    heat.change_energy_MWh = heat.energy - e18.d_h.energy
    fuels_wo_hydrogen.change_energy_MWh = fuels_wo_hydrogen.energy - 0
    fuels_hydrogen_reconv.change_energy_MWh = (
        fuels_hydrogen_reconv.energy - e18.d_f_hydrogen_reconv.energy
    )
    total.change_energy_MWh = total.energy - e18.d.energy

    heat.change_energy_pct = div(heat.change_energy_MWh, e18.d_h.energy)
    total.change_energy_pct = div(total.change_energy_MWh, e18.d.energy)

    return Demand(
        residences=residences,
        business=business,
        heat=heat,
        industry=industry,
        transport=transport,
        agri=agri,
        waste=waste,
        fuels_hydrogen_reconv=fuels_hydrogen_reconv,
        fuels_wo_hydrogen=fuels_wo_hydrogen,
        total=total,
    )
