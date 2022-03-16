# pyright: strict
from typing import Callable
from dataclasses import dataclass
from ..utils import div


@dataclass
class Transport:
    """Every form of transports is modelled at least in terms of the below."""

    change_CO2e_t: float
    change_energy_MWh: float
    change_km: float
    CO2e_combustion_based: float
    CO2e_total_2021_estimated: float
    CO2e_total: float
    cost_climate_saved: float
    energy: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    change_CO2e_pct: float
    change_energy_pct: float

    @classmethod
    def sum(
        cls,
        *transports: "Transport",
        energy_2018: float,
        co2e_2018: float,
    ) -> "Transport":
        """Aggregate two transports (e.g. road_bus + road_car).  Mostly this is
        just straightforward sums. But we also compute the percentages of
        change in comparison of energy and CO2e in 2018.
        """

        def sum_of(get: Callable[["Transport"], float]):
            return sum(map(get, transports))

        change_CO2e_t = sum_of(lambda t: t.change_CO2e_t)
        change_energy_MWh = sum_of(lambda t: t.change_energy_MWh)
        return cls(
            CO2e_total=sum_of(lambda t: t.CO2e_total),
            CO2e_combustion_based=sum_of(lambda t: t.CO2e_combustion_based),
            CO2e_total_2021_estimated=sum_of(lambda t: t.CO2e_total_2021_estimated),
            change_CO2e_t=change_CO2e_t,
            change_energy_MWh=change_energy_MWh,
            change_km=sum_of(lambda t: t.change_km),
            energy=sum_of(lambda t: t.energy),
            cost_climate_saved=sum_of(lambda t: t.cost_climate_saved),
            transport_capacity_tkm=sum_of(lambda t: t.transport_capacity_tkm),
            transport_capacity_pkm=sum_of(lambda t: t.transport_capacity_pkm),
            change_CO2e_pct=div(change_CO2e_t, co2e_2018),
            change_energy_pct=div(change_energy_MWh, energy_2018),
        )
