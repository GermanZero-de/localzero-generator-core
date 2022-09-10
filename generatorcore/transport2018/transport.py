# pyright: strict

from dataclasses import dataclass

from ..utils import element_wise_plus

from .air import Air
from .road import Road
from .rail import Rail
from .ship import Ship
from .other import Other


@dataclass
class Transport:
    # Used by t
    CO2e_combustion_based: float
    CO2e_total: float
    demand_biodiesel: float = 0
    demand_bioethanol: float = 0
    demand_biogas: float = 0
    demand_diesel: float = 0
    demand_electricity: float = 0
    demand_fueloil: float = 0
    demand_gas: float = 0
    demand_jetfuel: float = 0
    demand_lpg: float = 0
    demand_petrol: float = 0
    energy: float = 0
    transport_capacity_pkm: float = 0
    transport_capacity_tkm: float = 0

    def __add__(self: "Transport", other: "Transport") -> "Transport":
        return element_wise_plus(self, other)

    @classmethod
    def lift_air(cls, a: Air) -> "Transport":
        return cls(
            CO2e_combustion_based=a.CO2e_combustion_based,
            CO2e_total=a.CO2e_total,
            demand_jetfuel=a.demand_jetfuel,
            demand_petrol=a.demand_petrol,
            energy=a.energy,
            transport_capacity_pkm=a.transport_capacity_pkm,
            transport_capacity_tkm=a.transport_capacity_tkm,
        )

    @classmethod
    def lift_ship(cls, s: Ship) -> "Transport":
        return cls(
            CO2e_combustion_based=s.CO2e_combustion_based,
            CO2e_total=s.CO2e_total,
            demand_diesel=s.demand_diesel,
            demand_fueloil=s.demand_fueloil,
            energy=s.energy,
            transport_capacity_tkm=s.transport_capacity_tkm,
        )

    @classmethod
    def lift_road(cls, r: Road) -> "Transport":
        return cls(
            CO2e_combustion_based=r.CO2e_combustion_based,
            CO2e_total=r.CO2e_total,
            demand_diesel=r.demand_diesel,
            demand_biodiesel=r.demand_biodiesel,
            demand_bioethanol=r.demand_bioethanol,
            demand_biogas=r.demand_biogas,
            demand_electricity=r.demand_electricity,
            demand_gas=r.demand_gas,
            demand_lpg=r.demand_lpg,
            demand_petrol=r.demand_petrol,
            energy=r.energy,
            transport_capacity_tkm=r.transport_capacity_tkm,
            transport_capacity_pkm=r.transport_capacity_pkm,
        )

    @classmethod
    def lift_rail(cls, r: Rail) -> "Transport":
        return cls(
            CO2e_combustion_based=r.CO2e_combustion_based,
            CO2e_total=r.CO2e_total,
            demand_biodiesel=r.demand_biodiesel,
            demand_diesel=r.demand_diesel,
            demand_electricity=r.demand_electricity,
            energy=r.energy,
            transport_capacity_pkm=r.transport_capacity_pkm,
            transport_capacity_tkm=r.transport_capacity_tkm,
        )

    @classmethod
    def lift_other(cls, o: Other) -> "Transport":
        return cls(
            CO2e_combustion_based=o.CO2e_combustion_based,
            CO2e_total=o.CO2e_total,
            transport_capacity_pkm=o.transport_capacity_pkm,
        )
