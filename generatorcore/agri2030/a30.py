from dataclasses import dataclass, field

from .dataclasses import (
    Vars0,
    Vars1,
    Vars2,
    Vars3,
    Vars4,
    Vars5,
    Vars6,
    Vars7,
    Vars8,
    Vars9,
    Vars10,
    Vars11,
    Vars12,
    Vars13,
    Vars14,
    Vars15,
    Vars16,
    Vars17,
    Vars18,
    Vars19,
)


@dataclass
class A30:
    a: Vars0 = field(default_factory=Vars0)
    p: Vars1 = field(default_factory=Vars1)
    g: Vars2 = field(default_factory=Vars2)
    g_consult: Vars3 = field(default_factory=Vars3)
    g_organic: Vars4 = field(default_factory=Vars4)
    p_fermen: Vars5 = field(default_factory=Vars5)
    p_fermen_dairycow: Vars6 = field(default_factory=Vars6)
    p_fermen_nondairy: Vars6 = field(default_factory=Vars6)
    p_fermen_swine: Vars6 = field(default_factory=Vars6)
    p_fermen_poultry: Vars6 = field(default_factory=Vars6)
    p_fermen_oanimal: Vars6 = field(default_factory=Vars6)
    p_manure: Vars5 = field(default_factory=Vars5)
    p_manure_dairycow: Vars6 = field(default_factory=Vars6)
    p_manure_nondairy: Vars6 = field(default_factory=Vars6)
    p_manure_swine: Vars6 = field(default_factory=Vars6)
    p_manure_poultry: Vars6 = field(default_factory=Vars6)
    p_manure_oanimal: Vars6 = field(default_factory=Vars6)
    p_manure_deposition: Vars6 = field(default_factory=Vars6)
    p_soil: Vars5 = field(default_factory=Vars5)
    p_soil_fertilizer: Vars7 = field(default_factory=Vars7)
    p_soil_manure: Vars7 = field(default_factory=Vars7)
    p_soil_sludge: Vars7 = field(default_factory=Vars7)
    p_soil_ecrop: Vars7 = field(default_factory=Vars7)
    p_soil_grazing: Vars7 = field(default_factory=Vars7)
    p_soil_residue: Vars7 = field(default_factory=Vars7)
    p_soil_orgfarm: Vars7 = field(default_factory=Vars7)
    p_soil_orgloss: Vars7 = field(default_factory=Vars7)
    p_soil_leaching: Vars7 = field(default_factory=Vars7)
    p_soil_deposition: Vars7 = field(default_factory=Vars7)
    p_other: Vars5 = field(default_factory=Vars5)
    p_other_liming: Vars8 = field(default_factory=Vars8)
    p_other_liming_calcit: Vars9 = field(default_factory=Vars9)
    p_other_liming_dolomite: Vars9 = field(default_factory=Vars9)
    p_other_urea: Vars9 = field(default_factory=Vars9)
    p_other_kas: Vars9 = field(default_factory=Vars9)
    p_other_ecrop: Vars9 = field(default_factory=Vars9)
    p_operation: Vars10 = field(default_factory=Vars10)
    p_operation_heat: Vars11 = field(default_factory=Vars11)
    p_operation_elec_elcon: Vars12 = field(default_factory=Vars12)
    p_operation_elec_heatpump: Vars13 = field(default_factory=Vars13)
    p_operation_vehicles: Vars14 = field(default_factory=Vars14)
    s: Vars15 = field(default_factory=Vars15)
    s_petrol: Vars16 = field(default_factory=Vars16)
    s_diesel: Vars16 = field(default_factory=Vars16)
    s_fueloil: Vars17 = field(default_factory=Vars17)
    s_lpg: Vars16 = field(default_factory=Vars16)
    s_gas: Vars17 = field(default_factory=Vars17)
    s_biomass: Vars16 = field(default_factory=Vars16)
    s_elec: Vars16 = field(default_factory=Vars16)
    s_heatpump: Vars18 = field(default_factory=Vars18)
    s_emethan: Vars19 = field(default_factory=Vars19)
