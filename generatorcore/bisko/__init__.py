# pyright: strict
from dataclasses import dataclass

from generatorcore.inputs import Inputs

from ..utils import div
from .. import (
    agri2018,
    electricity2018,
    business2018,
    fuels2018,
    heat2018,
    industry2018,
    lulucf2018,
    residences2018,
    transport2018,
)


@dataclass
class ProductionBasedEmission:
    # production based Emissions
    CO2e_pb: float

    @classmethod
    def calc_sum_pb_emission(
        cls, *args: "ProductionBasedEmission"
    ) -> "ProductionBasedEmission":
        CO2e_pb = sum([elem.CO2e_pb for elem in args])
        return cls(CO2e_pb=CO2e_pb)

    def add_production_based_emission(self, *args: "ProductionBasedEmission"):
        self.CO2e_pb = self.CO2e_pb + sum([elem.CO2e_pb for elem in args])

    def add_combustion_based_emission(self, *args: "Emissions"):
        self.CO2e_cb = self.CO2e_cb + sum([elem.CO2e_cb for elem in args])


@dataclass
class Emissions(ProductionBasedEmission):
    # combustion based Emissions
    CO2e_cb: float
    CO2e_total: float = 0

    def __post_init__(self):
        self.CO2e_total = self.CO2e_cb + self.CO2e_pb

    @classmethod
    def calc_sum_emissions(cls, *args: "Emissions") -> "Emissions":  # type: ignore
        CO2e_cb: float = sum([elem.CO2e_cb for elem in args])
        CO2e_pb: float = sum([elem.CO2e_pb for elem in args])
        return cls(CO2e_cb=CO2e_cb, CO2e_pb=CO2e_pb)

    @classmethod
    def calc_sum_from_emissions_and_pb_emissions(cls,pb_emission_summands:list[ProductionBasedEmission],emission_summands:list["Emissions"]):
        CO2e_cb: float = sum([elem.CO2e_cb for elem in emission_summands])
        CO2e_pb: float = sum([elem.CO2e_pb for elem in pb_emission_summands]) + sum([elem.CO2e_pb for elem in emission_summands])
        return cls(CO2e_cb=CO2e_cb, CO2e_pb=CO2e_pb)
    


@dataclass(kw_only=True)
class EnergyAndEmissions(Emissions):
    """
    This class contains the relevant data attributes for the Bisko greenhous gas (GHG)
    balance for a energy source like petrol/electricitiy or the data for a sub sector
    like the communal facilities.
    """

    # energy consumption
    energy: float

    @classmethod
    def calc_sum_energy_and_emissions(
        cls, *args: "EnergyAndEmissions"
    ) -> "EnergyAndEmissions":
        return cls(
            energy=sum([elem.energy for elem in args]),
            CO2e_cb=sum([elem.CO2e_cb for elem in args]),
            CO2e_pb=sum([elem.CO2e_pb for elem in args]),
        )


@dataclass
class EnergyAndEmissionsCalcIntermediate(EnergyAndEmissions):
    """
    This class is a contains all relevant parameters for the conversion calculation
    from the "Einflussbilanz" (EB) to the "BISKO Bilanz" (see Readme) for a single energy
    source like petrol or electricity. Various contributions from EB
    sectors are combined to form the new variables of the BISKO balance. EB
    attributes (eb-prefix) are saved intermediately for convenience.
    Most instances of this class do not have contributions from all possible EB sectors.
    To avoid creating classes for all occuring subsets, all attributes are initialized with 0.
    """

    # these variables are calculated by the __post_init__ function.
    energy: float = 0
    CO2e_cb: float = 0
    CO2e_pb: float = 0

    # Variables that are calculated for the Einflussbilanz (eb)
    eb_energy_from_same_sector: float = 0
    eb_energy_from_agri: float = 0
    eb_CO2e_cb_from_same_sector: float = 0
    eb_CO2e_cb_from_heat: float = 0
    eb_CO2e_cb_from_elec: float = 0
    eb_CO2e_cb_from_fuels: float = 0
    eb_CO2e_cb_from_agri: float = 0
    eb_CO2e_pb_from_heat: float = 0

    def __post_init__(self):

        self.energy = sum([self.eb_energy_from_same_sector, self.eb_energy_from_agri])
        self.CO2e_cb = sum(
            [
                self.eb_CO2e_cb_from_same_sector,
                self.eb_CO2e_cb_from_heat,
                self.eb_CO2e_cb_from_elec,
                self.eb_CO2e_cb_from_fuels,
                self.eb_CO2e_cb_from_agri,
            ]
        )
        self.CO2e_pb = sum([self.eb_CO2e_pb_from_heat])

    def to_energy_and_emissions(self) -> EnergyAndEmissions:
        return EnergyAndEmissions(
            energy=self.energy, CO2e_cb=self.CO2e_cb, CO2e_pb=self.CO2e_pb
        )


@dataclass(kw_only=True)
class Sums(EnergyAndEmissions):
    """
    This class represents a sum over instances of class EnergyAndEmissionsCalcIntermediate.
    """

    # energy consumption
    energy_from_same_eb_sector: float
    energy_from_eb_agri_sector: float

    # combustion based Emissions
    eb_CO2e_from_same_sector: float
    eb_CO2e_cb_from_agri: float
    eb_CO2e_cb_from_heat: float
    eb_CO2e_cb_from_elec: float
    eb_CO2e_cb_from_fuels: float

    # production based Emissions
    eb_CO2e_pb_from_heat: float

    @classmethod
    def calc(cls, *args: EnergyAndEmissionsCalcIntermediate):
        energy = sum([elem.energy for elem in args])
        energy_from_same_eb_sector = sum(
            [elem.eb_energy_from_same_sector for elem in args]
        )
        energy_from_eb_agri_sector = sum([elem.eb_energy_from_agri for elem in args])
        CO2e_cb = sum([elem.CO2e_cb for elem in args])
        eb_CO2e_from_same_sector = sum(
            [elem.eb_CO2e_cb_from_same_sector for elem in args]
        )
        eb_CO2e_cb_from_agri = sum([elem.eb_CO2e_cb_from_agri for elem in args])
        eb_CO2e_cb_from_heat = sum([elem.eb_CO2e_cb_from_heat for elem in args])
        eb_CO2e_cb_from_elec = sum([elem.eb_CO2e_cb_from_elec for elem in args])
        eb_CO2e_cb_from_fuels = sum([elem.eb_CO2e_cb_from_fuels for elem in args])
        CO2e_pb = sum([elem.CO2e_pb for elem in args])
        eb_CO2e_pb_from_heat = sum([elem.eb_CO2e_pb_from_heat for elem in args])

        return cls(
            energy=energy,
            energy_from_same_eb_sector=energy_from_same_eb_sector,
            energy_from_eb_agri_sector=energy_from_eb_agri_sector,
            CO2e_cb=CO2e_cb,
            eb_CO2e_from_same_sector=eb_CO2e_from_same_sector,
            eb_CO2e_cb_from_agri=eb_CO2e_cb_from_agri,
            eb_CO2e_cb_from_heat=eb_CO2e_cb_from_heat,
            eb_CO2e_cb_from_elec=eb_CO2e_cb_from_elec,
            eb_CO2e_cb_from_fuels=eb_CO2e_cb_from_fuels,
            CO2e_pb=CO2e_pb,
            eb_CO2e_pb_from_heat=eb_CO2e_pb_from_heat,
        )


@dataclass
class BiskoSector:
    # shared BISKO sector variables
    total: Sums | EnergyAndEmissions

    lpg: EnergyAndEmissions
    gas: EnergyAndEmissions
    elec: EnergyAndEmissions
    fueloil: EnergyAndEmissions


@dataclass
class BiskoSectorWithExtraCommunalFacilities:
    """
    Some Bisko GHG balances also show the emissions and energy consumptions of
    communal facilities. This is only relevant for the private residences and
    the buisness sector.
    """

    communal_facilities: EnergyAndEmissions
    sector_without_communal_facilities: EnergyAndEmissions


@dataclass
class BiskoPrivResidences(BiskoSector, BiskoSectorWithExtraCommunalFacilities):
    """
    Bisko Sector for private residences.
    """

    petrol: EnergyAndEmissions
    coal: EnergyAndEmissions
    heatnet: EnergyAndEmissions
    biomass: EnergyAndEmissions
    solarth: EnergyAndEmissions
    heatpump: EnergyAndEmissions

    @classmethod
    def calc_priv_residences_bisko(
        cls,
        inputs: Inputs,
        r18: residences2018.R18,
        h18: heat2018.H18,
        f18: fuels2018.F18,
        e18: electricity2018.E18,
    ) -> "BiskoPrivResidences":

        fact = inputs.fact
        # ass = inputs.ass

        petrol = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_petrol.energy,
            eb_CO2e_cb_from_same_sector=r18.s_petrol.CO2e_total,
            eb_CO2e_cb_from_fuels=r18.s_petrol.energy* fact("Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018"),
        )
        fueloil = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_fueloil.energy,
            eb_CO2e_cb_from_same_sector=r18.s_fueloil.CO2e_total,
            eb_CO2e_cb_from_heat=r18.s_fueloil.energy * fact("Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"),
        )
        coal = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_coal.energy,
            eb_CO2e_cb_from_same_sector=r18.s_coal.CO2e_total,
            eb_CO2e_cb_from_heat=r18.s_coal.energy * fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=r18.s_coal.energy * fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"),
        )
        lpg = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_lpg.energy,
            eb_CO2e_cb_from_same_sector=r18.s_lpg.CO2e_total,
            eb_CO2e_cb_from_heat=r18.s_lpg.energy * fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018"),
        )
        gas = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_gas.energy,
            eb_CO2e_cb_from_same_sector=r18.s_gas.CO2e_total,
            eb_CO2e_cb_from_heat=r18.s_gas.energy * fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=r18.s_gas.energy * fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        )
        heatnet = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_heatnet.energy,
            eb_CO2e_cb_from_same_sector=r18.s_heatnet.CO2e_total,
            eb_CO2e_cb_from_heat=r18.s_heatnet.energy * fact("Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"),
        )
        biomass = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_biomass.energy,
            eb_CO2e_cb_from_same_sector=r18.s_biomass.CO2e_total,
            eb_CO2e_pb_from_heat=r18.s_biomass.energy * fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"),
        )
        solarth = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_solarth.energy,
            eb_CO2e_cb_from_same_sector=r18.s_solarth.CO2e_total,
            eb_CO2e_pb_from_heat=r18.s_solarth.energy * fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        )
        heatpump = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_heatpump.energy,
            eb_CO2e_cb_from_same_sector=r18.s_heatpump.CO2e_total,
            eb_CO2e_pb_from_heat=r18.s_heatpump.energy * fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        )
        elec = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=r18.s_elec.energy,
            eb_CO2e_cb_from_same_sector=r18.s_elec.CO2e_total,
            eb_CO2e_cb_from_elec=r18.s_elec.energy * e18.p.CO2e_combustion_based_per_MWh,
        )

        total = Sums.calc(
            petrol, fueloil, coal, lpg, gas, heatnet, biomass, solarth, heatpump, elec
        )

        communal_facilities = EnergyAndEmissions(
            energy=r18.p_buildings_area_m2_com.energy,
            CO2e_cb=total.CO2e_cb
            * div(r18.p_buildings_area_m2_com.energy, total.energy),
            CO2e_pb=total.CO2e_pb
            * div(r18.p_buildings_area_m2_com.energy, total.energy),
        )
        sector_without_communal_facilities = EnergyAndEmissions(
            energy=total.energy - communal_facilities.energy,
            CO2e_cb=total.CO2e_cb
            * div(total.energy - communal_facilities.energy, total.energy),
            CO2e_pb=total.CO2e_pb
            * div(total.energy - communal_facilities.energy, total.energy),
        )

        return cls(
            petrol=petrol.to_energy_and_emissions(),
            fueloil=fueloil.to_energy_and_emissions(),
            coal=coal.to_energy_and_emissions(),
            lpg=lpg.to_energy_and_emissions(),
            gas=gas.to_energy_and_emissions(),
            heatnet=heatnet.to_energy_and_emissions(),
            biomass=biomass.to_energy_and_emissions(),
            solarth=solarth.to_energy_and_emissions(),
            heatpump=heatpump.to_energy_and_emissions(),
            elec=elec.to_energy_and_emissions(),
            total=total,
            communal_facilities=communal_facilities,
            sector_without_communal_facilities=sector_without_communal_facilities,
        )


@dataclass
class BiskoBusiness(BiskoSector, BiskoSectorWithExtraCommunalFacilities):
    petrol: EnergyAndEmissions
    diesel: EnergyAndEmissions
    jetfuel: EnergyAndEmissions
    coal: EnergyAndEmissions
    heatnet: EnergyAndEmissions
    biomass: EnergyAndEmissions
    solarth: EnergyAndEmissions
    heatpump: EnergyAndEmissions

    @classmethod
    def calc_business_bisko(
        cls,
        inputs: Inputs,
        b18: business2018.B18,
        h18: heat2018.H18,
        f18: fuels2018.F18,
        e18: electricity2018.E18,
        a18: agri2018.A18,
    ) -> "BiskoBusiness":

        fact = inputs.fact

        petrol = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_petrol.energy,
            eb_energy_from_agri=a18.s_petrol.energy,
            eb_CO2e_cb_from_same_sector=b18.s_petrol.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_petrol.CO2e_total,
            eb_CO2e_cb_from_fuels= (b18.s_petrol.energy + a18.s_petrol.energy) * fact("Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018"),
        )
        diesel = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_diesel.energy,
            eb_energy_from_agri=a18.s_diesel.energy,
            eb_CO2e_cb_from_same_sector=b18.s_diesel.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_diesel.CO2e_total,
            eb_CO2e_cb_from_fuels= (b18.s_diesel.energy + a18.s_diesel.energy) * fact("Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018"),
        )
        jetfuel = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_jetfuel.energy,
            eb_CO2e_cb_from_same_sector=b18.s_jetfuel.CO2e_total,
            eb_CO2e_cb_from_fuels= b18.s_jetfuel.energy * fact("Fact_F_P_jetfuel_ratio_CO2e_cb_to_fec_2018"),
        )
        fueloil = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_fueloil.energy,
            eb_energy_from_agri=a18.s_fueloil.energy,
            eb_CO2e_cb_from_same_sector=b18.s_fueloil.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_fueloil.CO2e_total,
            eb_CO2e_cb_from_heat= (b18.s_fueloil.energy + a18.s_fueloil.energy) * fact("Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"),
        )
        coal = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_coal.energy,
            eb_CO2e_cb_from_same_sector=b18.s_coal.CO2e_total,
            eb_CO2e_cb_from_heat= b18.s_coal.energy * fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat= b18.s_coal.energy * fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"),
        )
        lpg = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_lpg.energy,
            eb_energy_from_agri=a18.s_lpg.energy,
            eb_CO2e_cb_from_same_sector=b18.s_lpg.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_lpg.CO2e_total,
            eb_CO2e_cb_from_heat= (b18.s_lpg.energy + a18.s_lpg.energy) * fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018"),
        )
        gas = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_gas.energy,
            eb_energy_from_agri=a18.s_gas.energy,
            eb_CO2e_cb_from_same_sector=b18.s_gas.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_gas.CO2e_total,
            eb_CO2e_cb_from_heat=(b18.s_gas.energy + a18.s_gas.energy) * fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=(b18.s_gas.energy + a18.s_gas.energy) * fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        )
        heatnet = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_heatnet.energy,
            eb_CO2e_cb_from_same_sector=b18.s_heatnet.CO2e_total,
            eb_CO2e_cb_from_heat = b18.s_heatnet.energy  * fact("Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"),
        )
        biomass = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_biomass.energy,
            eb_energy_from_agri=a18.s_biomass.energy,
            eb_CO2e_cb_from_same_sector=b18.s_biomass.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_biomass.CO2e_total,
            eb_CO2e_pb_from_heat= (b18.s_biomass.energy + a18.s_biomass.energy) * fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"),
        )
        solarth = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_solarth.energy,
            eb_CO2e_cb_from_same_sector=b18.s_solarth.CO2e_total,
            eb_CO2e_pb_from_heat= b18.s_solarth.energy * fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        )
        heatpump = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_heatpump.energy,
            eb_CO2e_cb_from_same_sector=b18.s_heatpump.CO2e_total,
            eb_CO2e_pb_from_heat= b18.s_heatpump.energy * fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        )
        elec = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=b18.s_elec.energy,
            eb_energy_from_agri=a18.s_elec.energy,
            eb_CO2e_cb_from_same_sector=b18.s_elec.CO2e_total,
            eb_CO2e_cb_from_agri=a18.s_elec.CO2e_total,
            eb_CO2e_cb_from_elec=(b18.s_elec.energy + a18.s_elec.energy) * e18.p.CO2e_combustion_based_per_MWh,
        )

        total = Sums.calc(
            petrol,
            diesel,
            jetfuel,
            fueloil,
            coal,
            lpg,
            gas,
            heatnet,
            biomass,
            solarth,
            heatpump,
            elec,
        )

        communal_facilities = EnergyAndEmissions(
            energy=b18.p_nonresi_com.energy,
            CO2e_cb=total.CO2e_cb * div(b18.p_nonresi_com.energy, total.energy),
            CO2e_pb=total.CO2e_pb * div(b18.p_nonresi_com.energy, total.energy),
        )
        sector_without_communal_facilities = EnergyAndEmissions(
            energy=total.energy - communal_facilities.energy,
            CO2e_cb=total.CO2e_cb
            * div(total.energy - communal_facilities.energy, total.energy),
            CO2e_pb=total.CO2e_pb
            * div(total.energy - communal_facilities.energy, total.energy),
        )

        return cls(
            petrol=petrol.to_energy_and_emissions(),
            diesel=diesel.to_energy_and_emissions(),
            jetfuel=jetfuel.to_energy_and_emissions(),
            fueloil=fueloil.to_energy_and_emissions(),
            coal=coal.to_energy_and_emissions(),
            lpg=lpg.to_energy_and_emissions(),
            gas=gas.to_energy_and_emissions(),
            heatnet=heatnet.to_energy_and_emissions(),
            biomass=biomass.to_energy_and_emissions(),
            solarth=solarth.to_energy_and_emissions(),
            heatpump=heatpump.to_energy_and_emissions(),
            elec=elec.to_energy_and_emissions(),
            total=total,
            communal_facilities=communal_facilities,
            sector_without_communal_facilities=sector_without_communal_facilities,
        )


@dataclass
class BiskoTransport(BiskoSector):
    """
    Bisko sector for transportation.
    """

    petrol: EnergyAndEmissions
    diesel: EnergyAndEmissions
    jetfuel: EnergyAndEmissions
    bioethanol: EnergyAndEmissions
    biodiesel: EnergyAndEmissions
    biogas: EnergyAndEmissions

    @classmethod
    def calc_transport_bisko(
        cls,
        inputs: Inputs,
        t18: transport2018.T18,
        h18: heat2018.H18,
        f18: fuels2018.F18,
        e18: electricity2018.E18,
    ) -> "BiskoTransport":

        fact = inputs.fact
        ass = inputs.ass

        petrol = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_petrol.energy,
            eb_CO2e_cb_from_same_sector=t18.s_petrol.energy
            * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_fuels=t18.s_petrol.energy * fact("Fact_F_P_petrol_ratio_CO2e_cb_to_fec_2018"),
        )
        diesel = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_diesel.energy,
            eb_CO2e_cb_from_same_sector=t18.s_diesel.energy
            * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_fuels=t18.s_diesel.energy * fact("Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018"),
        )
        jetfuel = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_jetfuel.energy,
            eb_CO2e_cb_from_same_sector=t18.s_jetfuel.energy
            * fact("Fact_T_S_jetfuel_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_fuels=t18.s_jetfuel.energy * fact("Fact_F_P_jetfuel_ratio_CO2e_cb_to_fec_2018"),
        )

        bioethanol = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_bioethanol.energy,
            eb_CO2e_cb_from_same_sector=t18.s_bioethanol.energy
            * ass("Ass_T_S_bioethanol_EmFa_tank_wheel"),
            eb_CO2e_cb_from_fuels=t18.s_bioethanol.energy * fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"),
        )
        biodiesel = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_biodiesel.energy,
            eb_CO2e_cb_from_same_sector=t18.s_biodiesel.energy
            * ass("Ass_T_S_biodiesel_EmFa_tank_wheel"),
            eb_CO2e_cb_from_fuels=t18.s_biodiesel.energy * fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"),
        )
        biogas = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_biogas.energy,
            eb_CO2e_cb_from_same_sector=t18.s_biogas.energy
            * ass("Ass_T_S_biogas_EmFa_tank_wheel"),
            eb_CO2e_cb_from_fuels= t18.s_biogas.energy * fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"),
        )

        fueloil = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_fueloil.energy,
            eb_CO2e_cb_from_same_sector=t18.s_fueloil.energy
            * fact("Fact_T_S_fueloil_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_heat=t18.s_fueloil.energy * fact("Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"),
        )

        lpg = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_lpg.energy,
            eb_CO2e_cb_from_same_sector=t18.s_lpg.energy
            * fact("Fact_T_S_lpg_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_heat=t18.s_lpg.energy * fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018"),
        )
        gas = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_gas.energy,
            eb_CO2e_cb_from_same_sector=t18.s_gas.energy
            * fact("Fact_T_S_cng_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_heat=t18.s_gas.energy * fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=t18.s_gas.energy * fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        )
        elec = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=t18.s_elec.energy,
            eb_CO2e_cb_from_same_sector=t18.s_elec.energy
            * fact("Fact_T_S_electricity_EmFa_tank_wheel_2018"),
            eb_CO2e_cb_from_elec=t18.s_elec.energy * e18.p.CO2e_combustion_based_per_MWh,
        )

        total = Sums.calc(
            petrol,
            diesel,
            jetfuel,
            bioethanol,
            biodiesel,
            biogas,
            fueloil,
            lpg,
            gas,
            elec,
        )

        return cls(
            petrol=petrol.to_energy_and_emissions(),
            diesel=diesel.to_energy_and_emissions(),
            jetfuel=jetfuel.to_energy_and_emissions(),
            bioethanol=bioethanol.to_energy_and_emissions(),
            biodiesel=biodiesel.to_energy_and_emissions(),
            biogas=biogas.to_energy_and_emissions(),
            fueloil=fueloil.to_energy_and_emissions(),
            lpg=lpg.to_energy_and_emissions(),
            gas=gas.to_energy_and_emissions(),
            elec=elec.to_energy_and_emissions(),
            total=total,
        )


@dataclass
class BiskoIndustry(BiskoSector):
    """
    Bisko sector for industry. We are currently not able to calculate any
    single energy source emissions in the eb_industry sector. Therefore
    it is not possible to calculate bisko single energy source emissions,
    except from single energy source emissions coming from other "Einflussbilanz"
    sectors. Instead the emissions are only calculated for the industry sub sectors.
    """

    diesel: EnergyAndEmissions
    coal: EnergyAndEmissions
    other_fossil: EnergyAndEmissions
    heatnet: EnergyAndEmissions
    biomass: EnergyAndEmissions
    solarth: EnergyAndEmissions
    heatpump: EnergyAndEmissions

    miner: Emissions
    chemistry: Emissions
    metal: Emissions
    other: Emissions

    total_supply: Sums
    total_production: Emissions

    @classmethod
    def calc_industry_bisko(
        cls,
        inputs: Inputs,
        i18: industry2018.I18,
        h18: heat2018.H18,
        f18: fuels2018.F18,
        e18: electricity2018.E18,
    ) -> "BiskoIndustry":

        fact = inputs.fact

        # Bereitstellung
        diesel = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_fossil_diesel.energy,
            eb_CO2e_cb_from_fuels=i18.s_fossil_diesel.energy * fact("Fact_F_P_diesel_ratio_CO2e_cb_to_fec_2018"),
        )
        fueloil = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_fossil_fueloil.energy,
            eb_CO2e_cb_from_heat=i18.s_fossil_fueloil.energy * fact("Fact_H_P_fueloil_ratio_CO2e_cb_to_fec_2018"),
        )
        coal = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_fossil_coal.energy,
            eb_CO2e_cb_from_heat=i18.s_fossil_coal.energy * fact("Fact_H_P_coal_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=i18.s_fossil_coal.energy * fact("Fact_H_P_coal_ratio_CO2e_pb_to_fec_2018"),
        )
        lpg = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_fossil_lpg.energy,
            eb_CO2e_cb_from_heat=i18.s_fossil_lpg.energy * fact("Fact_H_P_lpg_ratio_CO2e_cb_to_fec_2018"),
        )
        gas = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_fossil_gas.energy,
            eb_CO2e_cb_from_heat=i18.s_fossil_gas.energy * fact("Fact_H_P_gas_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=i18.s_fossil_gas.energy * fact("Fact_H_P_gas_ratio_CO2e_pb_to_fec_2018"),
        )
        other_fossil = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_fossil_ofossil.energy
            + i18.s_fossil_opetpro.energy,
            eb_CO2e_cb_from_heat=i18.s_fossil_opetpro.energy * fact("Fact_H_P_opetpro_ratio_CO2e_cb_to_fec_2018"),
            eb_CO2e_pb_from_heat=i18.s_fossil_opetpro.energy * fact("Fact_H_P_opetpro_ratio_CO2e_pb_to_fec_2018") + i18.s_fossil_ofossil.energy * fact("Fact_H_P_ofossil_ratio_CO2e_pb_to_fec_2018"),
        )

        heatnet = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_renew_heatnet.energy,
            eb_CO2e_cb_from_heat=i18.s_renew_heatnet.energy * fact("Fact_H_P_heatnet_plant_ratio_CO2e_cb_to_fec_2018"),
        )
        biomass = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_renew_biomass.energy,
            eb_CO2e_pb_from_heat=i18.s_renew_biomass.energy * fact("Fact_H_P_biomass_ratio_CO2e_pb_to_fec_2018"),
        )
        solarth = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_renew_solarth.energy,
            eb_CO2e_pb_from_heat=i18.s_renew_solarth.energy * fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        )
        heatpump = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_renew_heatpump.energy,
            eb_CO2e_pb_from_heat=i18.s_renew_heatpump.energy * fact("Fact_H_P_orenew_ratio_CO2e_pb_to_fec_2018"),
        )
        elec = EnergyAndEmissionsCalcIntermediate(
            eb_energy_from_same_sector=i18.s_renew_elec.energy,
            eb_CO2e_cb_from_elec=i18.s_renew_elec.energy * e18.p.CO2e_combustion_based_per_MWh,
        )
        # total Bereitstellung
        total_supply = Sums.calc(
            diesel,
            fueloil,
            coal,
            lpg,
            gas,
            other_fossil,
            heatnet,
            biomass,
            solarth,
            heatpump,
            elec,
        )

        miner = Emissions(
            CO2e_cb=i18.p_miner.CO2e_combustion_based,
            CO2e_pb=i18.p_miner.CO2e_production_based,
        )
        chem = Emissions(
            CO2e_cb=i18.p_chem.CO2e_combustion_based,
            CO2e_pb=i18.p_chem.CO2e_production_based,
        )
        metal = Emissions(
            CO2e_cb=i18.p_metal.CO2e_combustion_based,
            CO2e_pb=i18.p_metal.CO2e_production_based,
        )
        other = Emissions(
            CO2e_cb=i18.p_other.CO2e_combustion_based,
            CO2e_pb=i18.p_other.CO2e_production_based,
        )

        total_production = Emissions.calc_sum_emissions(miner, chem, metal, other)
        total = EnergyAndEmissions(
            energy=total_supply.energy,
            CO2e_cb=total_supply.CO2e_cb + total_production.CO2e_cb,
            CO2e_pb=total_supply.CO2e_pb + total_production.CO2e_pb,
        )

        return cls(
            diesel=diesel.to_energy_and_emissions(),
            fueloil=fueloil.to_energy_and_emissions(),
            coal=coal.to_energy_and_emissions(),
            lpg=lpg.to_energy_and_emissions(),
            gas=gas.to_energy_and_emissions(),
            other_fossil=other_fossil.to_energy_and_emissions(),
            heatnet=heatnet.to_energy_and_emissions(),
            biomass=biomass.to_energy_and_emissions(),
            solarth=solarth.to_energy_and_emissions(),
            heatpump=heatpump.to_energy_and_emissions(),
            elec=elec.to_energy_and_emissions(),
            total_supply=total_supply,
            miner=miner,
            chemistry=chem,
            metal=metal,
            other=other,
            total_production=total_production,
            total=total,
        )



@dataclass
class BiskoAgriculture():
    total : ProductionBasedEmission 
    forest: ProductionBasedEmission
    manure: ProductionBasedEmission
    soil: ProductionBasedEmission
    other: ProductionBasedEmission

    @classmethod
    def calc_bisko_agri(cls, a18: agri2018.A18) -> "BiskoAgriculture":
        forest = ProductionBasedEmission(CO2e_pb=a18.p_fermen.CO2e_production_based)
        manure = ProductionBasedEmission(CO2e_pb=a18.p_manure.CO2e_production_based)
        soil = ProductionBasedEmission(CO2e_pb=a18.p_soil.CO2e_production_based)
        other = ProductionBasedEmission(CO2e_pb=a18.p_other.CO2e_production_based)

        total = ProductionBasedEmission.calc_sum_pb_emission(
            forest, manure, soil, other
        )

        return cls(forest=forest, manure=manure, soil=soil, other=other, total=total)


@dataclass
class BiskoLULUCF():
    total: Emissions 
    forest: Emissions
    crop: ProductionBasedEmission
    grass: ProductionBasedEmission
    grove: ProductionBasedEmission
    wet: ProductionBasedEmission
    water: ProductionBasedEmission
    settlement: ProductionBasedEmission
    other: ProductionBasedEmission
    wood: ProductionBasedEmission

    @classmethod
    def calc_bisko_lulucf(cls, l18: lulucf2018.L18) -> "BiskoLULUCF":
        forest = Emissions(CO2e_pb=l18.g_forest.CO2e_production_based,CO2e_cb=l18.g_forest.CO2e_combustion_based) #forest has cb emission because of biomass use
        crop = ProductionBasedEmission(CO2e_pb=l18.g_crop.CO2e_total)
        grass = ProductionBasedEmission(CO2e_pb=l18.g_grass.CO2e_total)
        grove = ProductionBasedEmission(CO2e_pb=l18.g_grove.CO2e_total)
        wet = ProductionBasedEmission(CO2e_pb=l18.g_wet.CO2e_total)
        water = ProductionBasedEmission(CO2e_pb=l18.g_water.CO2e_total)
        settlement = ProductionBasedEmission(CO2e_pb=l18.g_settlement.CO2e_total)
        other = ProductionBasedEmission(CO2e_pb=l18.g_other.CO2e_total)
        wood = ProductionBasedEmission(CO2e_pb=l18.g_wood.CO2e_total)

        total = Emissions.calc_sum_from_emissions_and_pb_emissions(pb_emission_summands=
            [crop, grass, grove, wet, water, settlement, other, wood],emission_summands=[forest])
        

        return cls(
            forest=forest,
            crop=crop,
            grass=grass,
            grove=grove,
            wet=wet,
            water=water,
            settlement=settlement,
            other=other,
            wood=wood,
            total=total,
        )


@dataclass
class Bisko:
    priv_residences: BiskoPrivResidences
    business: BiskoBusiness
    transport: BiskoTransport
    industry: BiskoIndustry

    agri: BiskoAgriculture
    lulucf: BiskoLULUCF

    total: EnergyAndEmissions
    communal_facilities: EnergyAndEmissions

    bisko_quality: float

    @classmethod
    def calc(
        cls,
        inputs: Inputs,
        *,
        a18: agri2018.A18,
        b18: business2018.B18,
        e18: electricity2018.E18,
        f18: fuels2018.F18,
        h18: heat2018.H18,
        i18: industry2018.I18,
        l18: lulucf2018.L18,
        r18: residences2018.R18,
        t18: transport2018.T18,
    ) -> "Bisko":

        priv_residences_bisko = BiskoPrivResidences.calc_priv_residences_bisko(
            inputs=inputs, r18=r18, h18=h18, f18=f18, e18=e18
        )
        business_bisko = BiskoBusiness.calc_business_bisko(
            inputs=inputs,b18=b18, h18=h18, f18=f18, e18=e18, a18=a18
        )
        transport_bisko = BiskoTransport.calc_transport_bisko(
            inputs=inputs, t18=t18, h18=h18, f18=f18, e18=e18
        )
        industry_bisko = BiskoIndustry.calc_industry_bisko(
            inputs=inputs, i18=i18, h18=h18, f18=f18, e18=e18
        )
        agri_bisko = BiskoAgriculture.calc_bisko_agri(a18=a18)
        lulucf_bisko = BiskoLULUCF.calc_bisko_lulucf(l18=l18)

        total = EnergyAndEmissions.calc_sum_energy_and_emissions(
            priv_residences_bisko.total,
            business_bisko.total,
            transport_bisko.total,
            industry_bisko.total,
        )

        total.add_production_based_emission(agri_bisko.total, lulucf_bisko.total)
        total.add_combustion_based_emission(lulucf_bisko.total)

        communal_facilities = EnergyAndEmissions.calc_sum_energy_and_emissions(
            priv_residences_bisko.communal_facilities,
            business_bisko.communal_facilities,
        )
        bisko_quality = transport_bisko.total.energy * div(0.5, total.energy)

        return cls(
            priv_residences=priv_residences_bisko,
            business=business_bisko,
            transport=transport_bisko,
            industry=industry_bisko,
            agri=agri_bisko,
            lulucf=lulucf_bisko,
            total=total,
            communal_facilities=communal_facilities,
            bisko_quality=bisko_quality,
        )
