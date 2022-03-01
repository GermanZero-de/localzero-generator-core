from dataclasses import dataclass, asdict, field

from . import business2018, lulucf2018
from .inputs import Inputs
from .utils import div


@dataclass
class Vars0:
    # Used by a, p_fermen, p_manure, p_soil, p_other, p_other_liming
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars1:
    # Used by p
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars2:
    # Used by g
    CO2e_total: float = None  # type: ignore


@dataclass
class Vars3:
    # Used by g_consult, g_organic, s_emethan
    pass


@dataclass
class Vars4:
    # Used by p_fermen_dairycow, p_fermen_nondairy, p_fermen_swine, p_fermen_poultry, p_fermen_oanimal, p_manure_dairycow, p_manure_nondairy, p_manure_swine, p_manure_poultry, p_manure_oanimal, p_manure_deposition
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    amount: float = None  # type: ignore


@dataclass
class Vars5:
    # Used by p_soil_fertilizer, p_soil_manure, p_soil_sludge, p_soil_ecrop, p_soil_grazing, p_soil_residue, p_soil_orgfarm, p_soil_orgloss, p_soil_leaching, p_soil_deposition
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    area_ha: float = None  # type: ignore


@dataclass
class Vars6:
    # Used by p_other_liming_dolomite, p_other_urea, p_other_ecrop, p_other_liming_calcit
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars7:
    # Used by p_other_kas
    CO2e_pb: float = None  # type: ignore
    CO2e_pb_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by p_operation, p_operation_elec_heatpump
    energy: float = None  # type: ignore


@dataclass
class Vars9:
    # Used by p_operation_heat
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars10:
    # Used by p_operation_elec_elcon, p_operation_vehicles
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars11:
    # Used by s
    CO2e_cb: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars12:
    # Used by s_petrol, s_diesel, s_fueloil, s_lpg, s_gas, s_biomass, s_elec, s_heatpump
    CO2e_cb: float = None  # type: ignore
    CO2e_cb_per_MWh: float = None  # type: ignore
    CO2e_pb: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class A18:
    a: Vars0 = field(default_factory=Vars0)
    p: Vars1 = field(default_factory=Vars1)
    g: Vars2 = field(default_factory=Vars2)
    g_consult: Vars3 = field(default_factory=Vars3)
    g_organic: Vars3 = field(default_factory=Vars3)
    p_fermen: Vars0 = field(default_factory=Vars0)
    p_fermen_dairycow: Vars4 = field(default_factory=Vars4)
    p_fermen_nondairy: Vars4 = field(default_factory=Vars4)
    p_fermen_swine: Vars4 = field(default_factory=Vars4)
    p_fermen_poultry: Vars4 = field(default_factory=Vars4)
    p_fermen_oanimal: Vars4 = field(default_factory=Vars4)
    p_manure: Vars0 = field(default_factory=Vars0)
    p_manure_dairycow: Vars4 = field(default_factory=Vars4)
    p_manure_nondairy: Vars4 = field(default_factory=Vars4)
    p_manure_swine: Vars4 = field(default_factory=Vars4)
    p_manure_poultry: Vars4 = field(default_factory=Vars4)
    p_manure_oanimal: Vars4 = field(default_factory=Vars4)
    p_manure_deposition: Vars4 = field(default_factory=Vars4)
    p_soil: Vars0 = field(default_factory=Vars0)
    p_soil_fertilizer: Vars5 = field(default_factory=Vars5)
    p_soil_manure: Vars5 = field(default_factory=Vars5)
    p_soil_sludge: Vars5 = field(default_factory=Vars5)
    p_soil_ecrop: Vars5 = field(default_factory=Vars5)
    p_soil_grazing: Vars5 = field(default_factory=Vars5)
    p_soil_residue: Vars5 = field(default_factory=Vars5)
    p_soil_orgfarm: Vars5 = field(default_factory=Vars5)
    p_soil_orgloss: Vars5 = field(default_factory=Vars5)
    p_soil_leaching: Vars5 = field(default_factory=Vars5)
    p_soil_deposition: Vars5 = field(default_factory=Vars5)
    p_other: Vars0 = field(default_factory=Vars0)
    p_other_liming_dolomite: Vars6 = field(default_factory=Vars6)
    p_other_urea: Vars6 = field(default_factory=Vars6)
    p_other_ecrop: Vars6 = field(default_factory=Vars6)
    p_other_liming: Vars0 = field(default_factory=Vars0)
    p_other_liming_calcit: Vars6 = field(default_factory=Vars6)
    p_other_kas: Vars7 = field(default_factory=Vars7)
    p_operation: Vars8 = field(default_factory=Vars8)
    p_operation_heat: Vars9 = field(default_factory=Vars9)
    p_operation_elec_elcon: Vars10 = field(default_factory=Vars10)
    p_operation_elec_heatpump: Vars8 = field(default_factory=Vars8)
    p_operation_vehicles: Vars10 = field(default_factory=Vars10)
    s: Vars11 = field(default_factory=Vars11)
    s_petrol: Vars12 = field(default_factory=Vars12)
    s_diesel: Vars12 = field(default_factory=Vars12)
    s_fueloil: Vars12 = field(default_factory=Vars12)
    s_lpg: Vars12 = field(default_factory=Vars12)
    s_gas: Vars12 = field(default_factory=Vars12)
    s_emethan: Vars3 = field(default_factory=Vars3)
    s_biomass: Vars12 = field(default_factory=Vars12)
    s_elec: Vars12 = field(default_factory=Vars12)
    s_heatpump: Vars12 = field(default_factory=Vars12)

    def dict(self):
        return asdict(self)


def calc(inputs: Inputs, *, l18: lulucf2018.L18, b18: business2018.B18) -> A18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries

    a18 = A18()

    # Most of the "shortcuts" below should probably just die. They don't save
    # that much typing anymore and make it harder to recognize the data flow.
    a = a18.a
    p = a18.p
    g = a18.g
    p_fermen = a18.p_fermen
    p_fermen_dairycow = a18.p_fermen_dairycow
    p_fermen_nondairy = a18.p_fermen_nondairy
    p_fermen_swine = a18.p_fermen_swine
    p_fermen_poultry = a18.p_fermen_poultry
    p_fermen_oanimal = a18.p_fermen_oanimal
    p_manure = a18.p_manure
    p_manure_dairycow = a18.p_manure_dairycow
    p_manure_nondairy = a18.p_manure_nondairy
    p_manure_swine = a18.p_manure_swine
    p_manure_poultry = a18.p_manure_poultry
    p_manure_oanimal = a18.p_manure_oanimal
    p_manure_deposition = a18.p_manure_deposition
    p_soil = a18.p_soil
    p_soil_fertilizer = a18.p_soil_fertilizer
    p_soil_manure = a18.p_soil_manure
    p_soil_sludge = a18.p_soil_sludge
    p_soil_ecrop = a18.p_soil_ecrop
    p_soil_grazing = a18.p_soil_grazing
    p_soil_residue = a18.p_soil_residue
    p_soil_orgfarm = a18.p_soil_orgfarm
    p_soil_orgloss = a18.p_soil_orgloss
    p_soil_leaching = a18.p_soil_leaching
    p_soil_deposition = a18.p_soil_deposition
    p_other = a18.p_other
    p_other_kas = a18.p_other_kas
    p_other_liming = a18.p_other_liming
    p_other_liming_calcit = a18.p_other_liming_calcit
    p_other_liming_dolomite = a18.p_other_liming_dolomite
    p_other_urea = a18.p_other_urea
    p_other_ecrop = a18.p_other_ecrop
    p_operation = a18.p_operation
    p_operation_heat = a18.p_operation_heat
    p_operation_elec_elcon = a18.p_operation_elec_elcon
    p_operation_vehicles = a18.p_operation_vehicles
    s = a18.s
    s_petrol = a18.s_petrol
    s_diesel = a18.s_diesel
    s_fueloil = a18.s_fueloil
    s_lpg = a18.s_lpg
    s_gas = a18.s_gas
    s_biomass = a18.s_biomass
    s_elec = a18.s_elec
    s_heatpump = a18.s_heatpump
    p_operation_elec_heatpump = a18.p_operation_elec_heatpump

    s_heatpump.energy = 0.0
    g.CO2e_total = 0.0
    p_fermen.CO2e_cb = 0.0
    p_fermen_dairycow.CO2e_cb = 0.0
    p_fermen_nondairy.CO2e_cb = 0.0
    p_fermen_swine.CO2e_cb = 0.0
    p_fermen_poultry.CO2e_cb = 0.0
    p_fermen_oanimal.CO2e_cb = 0.0
    p_manure.CO2e_cb = 0.0
    p_manure_dairycow.CO2e_cb = 0.0
    p_manure_nondairy.CO2e_cb = 0.0
    p_manure_swine.CO2e_cb = 0.0
    p_manure_poultry.CO2e_cb = 0.0
    p_manure_oanimal.CO2e_cb = 0.0
    p_manure_deposition.CO2e_cb = 0.0
    p_soil.CO2e_cb = 0.0
    p_soil_fertilizer.CO2e_cb = 0.0
    p_soil_manure.CO2e_cb = 0.0
    p_soil_sludge.CO2e_cb = 0.0
    p_soil_ecrop.CO2e_cb = 0.0
    p_soil_grazing.CO2e_cb = 0.0
    p_soil_residue.CO2e_cb = 0.0
    p_soil_orgfarm.CO2e_cb = 0.0
    p_soil_orgloss.CO2e_cb = 0.0
    p_soil_leaching.CO2e_cb = 0.0
    p_soil_deposition.CO2e_cb = 0.0
    p_other.CO2e_cb = 0.0
    p_other_liming.CO2e_cb = 0.0
    p_other_liming_calcit.CO2e_cb = 0.0
    p_other_liming_dolomite.CO2e_cb = 0.0
    p_other_urea.CO2e_cb = 0.0
    p_other_ecrop.CO2e_cb = 0.0
    s.CO2e_pb = 0.0
    s_petrol.CO2e_pb = 0.0
    s_diesel.CO2e_pb = 0.0
    s_fueloil.CO2e_pb = 0.0
    s_lpg.CO2e_pb = 0.0
    s_gas.CO2e_pb = 0.0
    s_biomass.CO2e_pb = 0.0
    s_elec.CO2e_pb = 0.0
    s_heatpump.CO2e_pb = 0.0
    p_operation_elec_heatpump.energy = 0

    p_fermen_dairycow.CO2e_pb_per_t = fact(
        "Fact_A_P_fermen_dairycow_ratio_CO2e_to_amount_2018"
    )
    p_fermen_dairycow.amount = entries.a_fermen_dairycow_amount
    s_petrol.CO2e_cb_per_MWh = fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
    p_manure_dairycow.CO2e_pb_per_t = entries.a_manure_dairycow_ratio_CO2e_to_amount
    p_manure_dairycow.CO2e_pb = (
        p_fermen_dairycow.amount * p_manure_dairycow.CO2e_pb_per_t
    )
    p_fermen_dairycow.CO2e_pb = (
        p_fermen_dairycow.amount * p_fermen_dairycow.CO2e_pb_per_t
    )
    p_fermen_nondairy.CO2e_pb_per_t = fact(
        "Fact_A_P_fermen_nondairy_ratio_CO2e_to_amount_2018"
    )
    p_fermen_nondairy.amount = entries.a_fermen_nondairy_amount
    p_fermen_dairycow.CO2e_total = p_fermen_dairycow.CO2e_pb + p_fermen_dairycow.CO2e_cb
    p_fermen_nondairy.CO2e_pb = (
        p_fermen_nondairy.amount * p_fermen_nondairy.CO2e_pb_per_t
    )
    p_fermen_swine.CO2e_pb_per_t = fact(
        "Fact_A_P_fermen_swine_ratio_CO2e_to_amount_2018"
    )
    p_fermen_swine.amount = entries.a_fermen_pig_amount
    p_fermen_nondairy.CO2e_total = p_fermen_nondairy.CO2e_pb + p_fermen_nondairy.CO2e_cb
    p_fermen_swine.CO2e_pb = p_fermen_swine.amount * p_fermen_swine.CO2e_pb_per_t
    p_fermen_poultry.CO2e_pb_per_t = fact(
        "Fact_A_P_fermen_poultry_ratio_CO2e_to_amount_2018"
    )
    p_fermen_poultry.amount = entries.a_fermen_poultry_amount
    p_fermen_swine.CO2e_total = p_fermen_swine.CO2e_pb + p_fermen_swine.CO2e_cb
    p_fermen_poultry.CO2e_pb = p_fermen_poultry.amount * p_fermen_poultry.CO2e_pb_per_t
    p_fermen_poultry.CO2e_total = p_fermen_poultry.CO2e_pb
    p_fermen_oanimal.CO2e_pb_per_t = fact(
        "Fact_A_P_fermen_oanimal_ratio_CO2e_to_amount_2018"
    )
    p_fermen_oanimal.amount = entries.a_fermen_oanimal_amount
    p_fermen_poultry.CO2e_total = p_fermen_poultry.CO2e_pb + p_fermen_poultry.CO2e_cb
    p_fermen_oanimal.CO2e_pb = p_fermen_oanimal.amount * p_fermen_oanimal.CO2e_pb_per_t
    p_fermen.CO2e_pb = p_fermen.CO2e_pb = (
        p_fermen_dairycow.CO2e_pb
        + p_fermen_nondairy.CO2e_pb
        + p_fermen_swine.CO2e_pb
        + p_fermen_poultry.CO2e_pb
        + p_fermen_oanimal.CO2e_pb
    )
    p_fermen.CO2e_total = p_fermen.CO2e_pb + p_fermen.CO2e_cb
    p_fermen_oanimal.CO2e_total = p_fermen_oanimal.CO2e_pb + p_fermen_oanimal.CO2e_cb
    p_soil_fertilizer.CO2e_pb_per_t = entries.a_soil_fertilizer_ratio_CO2e_to_ha
    p_soil_fertilizer.area_ha = l18.g_crop.area_ha
    p_manure_dairycow.amount = p_fermen_dairycow.amount
    p_manure_nondairy.CO2e_pb_per_t = entries.a_manure_nondairy_ratio_CO2e_to_amount
    p_manure_nondairy.CO2e_pb = (
        p_fermen_nondairy.amount * p_manure_nondairy.CO2e_pb_per_t
    )
    p_manure_dairycow.CO2e_total = p_manure_dairycow.CO2e_pb + p_manure_dairycow.CO2e_cb
    p_manure_nondairy.amount = p_fermen_nondairy.amount
    p_manure_swine.CO2e_pb_per_t = entries.a_manure_swine_ratio_CO2e_to_amount
    p_manure_swine.CO2e_pb = p_fermen_swine.amount * p_manure_swine.CO2e_pb_per_t
    p_manure_nondairy.CO2e_total = p_manure_nondairy.CO2e_pb + p_manure_nondairy.CO2e_cb
    p_manure_swine.amount = p_fermen_swine.amount
    p_manure_poultry.CO2e_pb_per_t = entries.a_manure_poultry_ratio_CO2e_to_amount
    p_manure_poultry.CO2e_pb = p_fermen_poultry.amount * p_manure_poultry.CO2e_pb_per_t
    p_manure_swine.CO2e_total = p_manure_swine.CO2e_pb + p_manure_swine.CO2e_cb
    p_manure_poultry.amount = p_fermen_poultry.amount
    p_manure_oanimal.CO2e_pb_per_t = entries.a_manure_oanimal_ratio_CO2e_to_amount
    p_manure_oanimal.CO2e_pb = p_fermen_oanimal.amount * p_manure_oanimal.CO2e_pb_per_t
    p_manure_poultry.CO2e_total = p_manure_poultry.CO2e_pb + p_manure_poultry.CO2e_cb
    p_manure_oanimal.amount = p_fermen_oanimal.amount
    p_manure_deposition.CO2e_pb_per_t = entries.a_manure_deposition_ratio_CO2e_to_amount
    p_manure_deposition.amount = (
        p_fermen_dairycow.amount
        + p_fermen_nondairy.amount
        + p_fermen_swine.amount
        + p_fermen_oanimal.amount
    )
    p_manure_oanimal.CO2e_total = p_manure_oanimal.CO2e_pb + p_manure_oanimal.CO2e_cb
    p_manure_deposition.CO2e_pb = (
        p_manure_deposition.amount * p_manure_deposition.CO2e_pb_per_t
    )
    p_manure.CO2e_pb = (
        p_manure_dairycow.CO2e_pb
        + p_manure_nondairy.CO2e_pb
        + p_manure_swine.CO2e_pb
        + p_manure_poultry.CO2e_pb
        + p_manure_oanimal.CO2e_pb
        + p_manure_deposition.CO2e_pb
    )
    p_manure.CO2e_total = p_manure.CO2e_pb + p_manure.CO2e_cb
    p_manure_deposition.CO2e_total = (
        p_manure_deposition.CO2e_pb + p_manure_deposition.CO2e_cb
    )
    p_other_liming_calcit.CO2e_pb_per_t = fact(
        "Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_liming_calcit.prod_volume = entries.a_other_liming_calcit_prod_volume
    p_soil_fertilizer.CO2e_pb = (
        p_soil_fertilizer.area_ha * p_soil_fertilizer.CO2e_pb_per_t
    )
    p_soil_manure.CO2e_pb_per_t = entries.a_soil_manure_ratio_CO2e_to_ha
    p_soil_manure.area_ha = l18.g_crop.area_ha
    p_soil_fertilizer.CO2e_total = p_soil_fertilizer.CO2e_pb + p_soil_fertilizer.CO2e_cb
    p_soil_manure.CO2e_pb = p_soil_manure.area_ha * p_soil_manure.CO2e_pb_per_t
    p_soil_sludge.CO2e_pb_per_t = entries.a_soil_sludge_ratio_CO2e_to_ha
    p_soil_sludge.area_ha = l18.g_crop.area_ha
    p_soil_manure.CO2e_total = p_soil_manure.CO2e_pb + p_soil_manure.CO2e_cb
    p_soil_sludge.CO2e_pb = p_soil_sludge.area_ha * p_soil_sludge.CO2e_pb_per_t
    p_soil_ecrop.CO2e_pb_per_t = entries.a_soil_ecrop_ratio_CO2e_to_ha
    p_soil_ecrop.area_ha = l18.g_crop.area_ha
    p_soil_sludge.CO2e_total = p_soil_sludge.CO2e_pb + p_soil_sludge.CO2e_cb
    p_soil_ecrop.CO2e_pb = p_soil_ecrop.area_ha * p_soil_ecrop.CO2e_pb_per_t
    p_soil_grazing.CO2e_pb_per_t = entries.a_soil_crazing_ratio_CO2e_to_ha
    p_soil_grazing.area_ha = l18.g_grass.area_ha
    p_soil_ecrop.CO2e_total = p_soil_ecrop.CO2e_pb + p_soil_ecrop.CO2e_cb
    p_soil_grazing.CO2e_pb = p_soil_grazing.area_ha * p_soil_grazing.CO2e_pb_per_t
    p_soil_residue.CO2e_pb_per_t = entries.a_soil_residue_ratio_CO2e_to_ha
    p_soil_residue.area_ha = l18.g_crop.area_ha
    p_soil_grazing.CO2e_total = p_soil_grazing.CO2e_pb + p_soil_grazing.CO2e_cb
    p_soil_residue.CO2e_pb = p_soil_residue.area_ha * p_soil_residue.CO2e_pb_per_t
    p_soil_orgfarm.CO2e_pb_per_t = entries.a_soil_orgfarm_ratio_CO2e_to_ha
    p_soil_orgfarm.area_ha = (
        l18.g_crop_org_low.area_ha
        + l18.g_crop_org_high.area_ha
        + l18.g_grass_org_low.area_ha
        + l18.g_grass_org_high.area_ha
    )
    p_soil_residue.CO2e_total = p_soil_residue.CO2e_pb + p_soil_residue.CO2e_cb
    p_soil_orgfarm.CO2e_pb = p_soil_orgfarm.area_ha * p_soil_orgfarm.CO2e_pb_per_t
    p_soil_orgloss.CO2e_pb_per_t = entries.a_soil_orgloss_ratio_CO2e_to_ha
    p_soil_orgloss.area_ha = l18.g_crop_org_low.area_ha + l18.g_crop_org_high.area_ha
    p_soil_orgfarm.CO2e_total = p_soil_orgfarm.CO2e_pb + p_soil_orgfarm.CO2e_cb
    p_soil_orgloss.CO2e_pb = p_soil_orgloss.area_ha * p_soil_orgloss.CO2e_pb_per_t
    p_soil_leaching.CO2e_pb_per_t = entries.a_soil_leaching_ratio_CO2e_to_ha
    p_soil_leaching.area_ha = l18.g_crop.area_ha + l18.g_grass.area_ha
    p_soil_orgloss.CO2e_total = p_soil_orgloss.CO2e_pb + p_soil_orgloss.CO2e_cb
    p_soil_leaching.CO2e_pb = p_soil_leaching.area_ha * p_soil_leaching.CO2e_pb_per_t
    p_soil_deposition.CO2e_pb_per_t = entries.a_soil_deposition_ratio_CO2e_to_ha
    p_soil_deposition.area_ha = l18.g_crop.area_ha + l18.g_grass.area_ha
    p_soil_leaching.CO2e_total = p_soil_leaching.CO2e_pb + p_soil_leaching.CO2e_cb
    p_soil_deposition.CO2e_pb = (
        p_soil_deposition.area_ha * p_soil_deposition.CO2e_pb_per_t
    )
    p_soil.CO2e_pb = (
        p_soil_fertilizer.CO2e_pb
        + p_soil_manure.CO2e_pb
        + p_soil_sludge.CO2e_pb
        + p_soil_ecrop.CO2e_pb
        + p_soil_grazing.CO2e_pb
        + p_soil_residue.CO2e_pb
        + p_soil_orgfarm.CO2e_pb
        + p_soil_orgloss.CO2e_pb
        + p_soil_leaching.CO2e_pb
        + p_soil_deposition.CO2e_pb
    )
    p_soil.CO2e_total = p_soil.CO2e_pb + p_soil.CO2e_cb
    p_soil_deposition.CO2e_total = p_soil_deposition.CO2e_pb + p_soil_deposition.CO2e_cb
    p_other_liming_calcit.CO2e_pb = (
        p_other_liming_calcit.prod_volume * p_other_liming_calcit.CO2e_pb_per_t
    )
    p_other_urea.CO2e_pb_per_t = fact("Fact_A_P_other_urea_CO2e_pb_to_amount_2018")
    p_other_liming_dolomite.CO2e_pb_per_t = fact(
        "Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_liming_dolomite.prod_volume = entries.a_other_liming_dolomite_prod_volume
    p_other_liming_dolomite.CO2e_pb = (
        p_other_liming_dolomite.prod_volume * p_other_liming_dolomite.CO2e_pb_per_t
    )
    p_other_liming.CO2e_pb = (
        p_other_liming_calcit.CO2e_pb + p_other_liming_dolomite.CO2e_pb
    )
    p_other_liming_calcit.CO2e_total = p_other_liming_calcit.CO2e_pb
    p_other_liming.CO2e_total = p_other_liming.CO2e_pb
    p_other_urea.prod_volume = entries.a_other_urea_prod_volume
    p_other_urea.CO2e_pb = p_other_urea.prod_volume * p_other_urea.CO2e_pb_per_t
    p_other_liming_dolomite.CO2e_total = p_other_liming_dolomite.CO2e_pb
    p_other_urea.CO2e_total = p_other_urea.CO2e_pb + p_other_urea.CO2e_cb
    p_other_ecrop.CO2e_pb_per_t = fact(
        "Fact_A_P_other_ecrop_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_ecrop.prod_volume = entries.a_other_ecrop_prod_volume
    p_other_ecrop.CO2e_pb = p_other_ecrop.prod_volume * p_other_ecrop.CO2e_pb_per_t

    p_other_liming_calcit.prod_volume = entries.a_other_liming_calcit_prod_volume
    p_other_liming_calcit.CO2e_pb_per_t = fact(
        "Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_liming_calcit.CO2e_pb = (
        p_other_liming_calcit.prod_volume * p_other_liming_calcit.CO2e_pb_per_t
    )
    p_other_liming_dolomite.prod_volume = entries.a_other_liming_dolomite_prod_volume
    p_other_liming_dolomite.CO2e_pb_per_t = fact(
        "Fact_A_P_other_liming_dolomite_ratio_CO2e_pb_to_amount_2018"
    )
    p_other_liming_dolomite.CO2e_pb = (
        p_other_liming_dolomite.prod_volume * p_other_liming_dolomite.CO2e_pb_per_t
    )
    p_other_kas.prod_volume = entries.a_other_kas_prod_volume
    p_other_kas.CO2e_pb_per_t = fact("Fact_A_P_other_kas_ratio_CO2e_pb_to_amount_2018")
    p_other_kas.CO2e_pb = p_other_kas.prod_volume * p_other_kas.CO2e_pb_per_t
    p_other.CO2e_pb = (
        p_other_liming.CO2e_pb
        + p_other_urea.CO2e_pb
        + p_other_kas.CO2e_pb
        + p_other_ecrop.CO2e_pb
    )
    p_other_kas.CO2e_total = p_other_kas.CO2e_pb
    p_other_ecrop.CO2e_total = p_other_ecrop.CO2e_pb + p_other_ecrop.CO2e_cb
    p_other.CO2e_total = (
        p_other_liming.CO2e_total
        + p_other_urea.CO2e_total
        + p_other_kas.CO2e_total
        + p_other_ecrop.CO2e_total
    )
    p.CO2e_pb = p_fermen.CO2e_pb + p_manure.CO2e_pb + p_soil.CO2e_pb + p_other.CO2e_pb
    s_petrol.energy = entries.a_petrol_fec
    p.CO2e_total = (
        p_fermen.CO2e_total
        + p_manure.CO2e_total
        + p_soil.CO2e_total
        + p_other.CO2e_total
    )
    s_fueloil.energy = entries.a_fueloil_fec
    s_diesel.energy = entries.a_diesel_fec
    p_operation_heat.area_m2 = (
        b18.p_nonresi.area_m2
        * fact("Fact_A_P_energy_buildings_ratio_A_to_B")
        / (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
    )
    s_lpg.energy = entries.a_lpg_fec
    s_elec.energy = entries.a_elec_fec
    p_operation_elec_elcon.energy = s_elec.energy
    s_gas.energy = entries.a_gas_fec
    p_operation_vehicles.energy = s_petrol.energy + s_diesel.energy

    s_biomass.energy = entries.a_biomass_fec
    s.energy = (
        s_petrol.energy
        + s_diesel.energy
        + s_fueloil.energy
        + s_lpg.energy
        + s_gas.energy
        + s_biomass.energy
        + s_elec.energy
    )
    s_petrol.CO2e_cb = s_petrol.energy * s_petrol.CO2e_cb_per_MWh
    s_diesel.CO2e_cb_per_MWh = fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
    s_petrol.pct_energy = div(s_petrol.energy, s.energy)
    s_diesel.pct_energy = div(s_diesel.energy, s.energy)
    s_diesel.CO2e_cb = s_diesel.energy * s_diesel.CO2e_cb_per_MWh
    s_fueloil.CO2e_cb_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    s_petrol.CO2e_total = s_petrol.CO2e_pb + s_petrol.CO2e_cb
    s_fueloil.pct_energy = div(s_fueloil.energy, s.energy)
    s_fueloil.CO2e_cb = s_fueloil.energy * s_fueloil.CO2e_cb_per_MWh
    s_lpg.CO2e_cb_per_MWh = fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
    s_diesel.CO2e_total = s_diesel.CO2e_pb + s_diesel.CO2e_cb
    p_operation.energy = s.energy
    p_operation_vehicles.pct_energy = div(
        p_operation_vehicles.energy, p_operation.energy
    )
    s_lpg.pct_energy = div(s_lpg.energy, s.energy)
    s_lpg.CO2e_cb = s_lpg.energy * s_lpg.CO2e_cb_per_MWh
    s_gas.CO2e_cb_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    s_fueloil.CO2e_total = s_fueloil.CO2e_pb + s_fueloil.CO2e_cb
    p_operation_heat.energy = (
        s_fueloil.energy + s_lpg.energy + s_gas.energy + s_biomass.energy
    )
    s_gas.pct_energy = div(s_gas.energy, s.energy)
    s_gas.CO2e_cb = s_gas.energy * s_gas.CO2e_cb_per_MWh
    s_biomass.CO2e_cb_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    s_lpg.CO2e_total = s_lpg.CO2e_pb + s_lpg.CO2e_cb
    p_operation_heat.factor_adapted_to_fec = div(
        p_operation_heat.energy, p_operation_heat.area_m2
    )
    s_biomass.pct_energy = div(s_biomass.energy, s.energy)
    s_biomass.CO2e_cb = s_biomass.energy * s_biomass.CO2e_cb_per_MWh
    s.CO2e_cb = (
        s_petrol.CO2e_cb
        + s_diesel.CO2e_cb
        + s_fueloil.CO2e_cb
        + s_lpg.CO2e_cb
        + s_gas.CO2e_cb
        + s_biomass.CO2e_cb
    )
    s_gas.CO2e_total = s_gas.CO2e_pb + s_gas.CO2e_cb
    p_operation_heat.pct_energy = div(p_operation_heat.energy, p_operation.energy)
    s_elec.pct_energy = div(s_elec.energy, s.energy)
    s.CO2e_total = s.CO2e_pb + s.CO2e_cb
    a.CO2e_total = g.CO2e_total + p.CO2e_total + s.CO2e_total
    s_biomass.CO2e_total = s_biomass.CO2e_pb + s_biomass.CO2e_cb
    p_operation_elec_elcon.pct_energy = div(
        p_operation_elec_elcon.energy, p_operation.energy
    )
    s.pct_energy = (
        s_petrol.pct_energy
        + s_diesel.pct_energy
        + s_fueloil.pct_energy
        + s_lpg.pct_energy
        + s_gas.pct_energy
        + s_biomass.pct_energy
        + s_elec.pct_energy
    )
    s_elec.CO2e_cb_per_MWh = fact("Fact_RB_S_elec_ratio_CO2e_to_fec")
    s_elec.CO2e_cb = s_elec.energy * s_elec.CO2e_cb_per_MWh
    s_elec.CO2e_total = s_elec.CO2e_pb + s_elec.CO2e_cb
    s_heatpump.pct_energy = div(s_heatpump.energy, b18.s.energy)
    s_heatpump.CO2e_cb_per_MWh = fact("Fact_RB_S_heatpump_ratio_CO2e_to_fec")
    s_heatpump.CO2e_cb = s_heatpump.energy * s_heatpump.CO2e_cb_per_MWh
    s_heatpump.CO2e_total = s_heatpump.CO2e_cb

    a.CO2e_pb = p.CO2e_pb
    a.CO2e_cb = s.CO2e_cb
    p.energy = p_operation.energy

    return a18
