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

    total = EnergyDemand()
    residences = EnergyDemandWithCostFuel()
    business = EnergyDemandWithCostFuel()
    heat = EnergyDemand()
    industry = EnergyDemandWithCostFuel()
    transport = EnergyDemandWithCostFuel()
    agri = EnergyDemandWithCostFuel()
    waste = EnergyDemand()
    fuels_hydrogen_reconv = EnergyDemand()
    fuels_wo_hydrogen = EnergyDemand()

    heat.energy = h30.p.demand_electricity
    residences.energy = r30.p.demand_electricity
    business.energy = b30.p.demand_electricity
    industry.energy = i30.p.demand_electricity
    transport.energy = t30.t.transport.demand_electricity
    agri.energy = a30.p_operation.demand_electricity
    waste.energy = wastelines.s_elec.energy
    fuels_wo_hydrogen.energy = (
        f30.p_petrol.demand_electricity
        + f30.p_jetfuel.demand_electricity
        + f30.p_diesel.demand_electricity
        + f30.p_emethan.demand_electricity
        + f30.p_hydrogen.demand_electricity
    )
    fuels_hydrogen_reconv.energy = f30.p_hydrogen_reconv.demand_electricity
    total.energy = (
        heat.energy
        + residences.energy
        + business.energy
        + industry.energy
        + transport.energy
        + agri.energy
        + waste.energy
        + fuels_wo_hydrogen.energy
        + fuels_hydrogen_reconv.energy
    )

    residences.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    business.cost_fuel_per_MWh = fact("Fact_E_D_B_cost_fuel_per_MWh_2018")
    industry.cost_fuel_per_MWh = fact("Fact_E_D_I_cost_fuel_per_MWh_2018")
    transport.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")
    agri.cost_fuel_per_MWh = fact("Fact_E_D_R_cost_fuel_per_MWh_2018")

    heat.change_energy_MWh = heat.energy - e18.d_h.energy
    residences.change_energy_MWh = residences.energy - e18.d_r.energy
    business.change_energy_MWh = business.energy - e18.d_b.energy
    industry.change_energy_MWh = industry.energy - e18.d_i.energy
    transport.change_energy_MWh = transport.energy - e18.d_t.energy
    agri.change_energy_MWh = agri.energy - e18.d_a.energy
    fuels_wo_hydrogen.change_energy_MWh = fuels_wo_hydrogen.energy - 0
    fuels_hydrogen_reconv.change_energy_MWh = (
        fuels_hydrogen_reconv.energy - e18.d_f_hydrogen_reconv.energy
    )
    total.change_energy_MWh = total.energy - e18.d.energy

    heat.change_energy_pct = div(heat.change_energy_MWh, e18.d_h.energy)  # todo div0
    residences.change_energy_pct = div(
        residences.change_energy_MWh, e18.d_r.energy
    )  # todo
    business.change_energy_pct = div(business.change_energy_MWh, e18.d_b.energy)  # todo
    industry.change_energy_pct = div(industry.change_energy_MWh, e18.d_i.energy)
    transport.change_energy_pct = div(transport.change_energy_MWh, e18.d_t.energy)
    agri.change_energy_pct = div(agri.change_energy_MWh, e18.d_a.energy)  # Todo
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
