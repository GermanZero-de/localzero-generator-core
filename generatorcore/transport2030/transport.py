# pyright: strict
from typing import Callable, Protocol
from dataclasses import dataclass, InitVar
from ..utils import div


class Transport2018(Protocol):
    energy: float
    CO2e_combustion_based: float


@dataclass(frozen=True)
class ZeroEnergyAndCO2e:
    energy: float = 0
    CO2e_combustion_based: float = 0


zero_energy_and_co2e = ZeroEnergyAndCO2e()


@dataclass(kw_only=True)
class Transport:
    """Every form of transports is modelled at least in terms of the below."""

    # change_km is confusing. What does it mean when we start to aggregate
    # two transports, one that modified transport_capacity_pkm and one
    # that modified transport_capacity_tkm ?
    change_km: float
    CO2e_combustion_based: float
    CO2e_total_2021_estimated: float
    CO2e_total: float
    cost_climate_saved: float
    transport_capacity_pkm: float
    transport_capacity_tkm: float

    demand_ejetfuel: float = 0
    demand_ediesel: float = 0
    demand_electricity: float = 0
    demand_epetrol: float = 0
    demand_hydrogen: float = 0

    # Numbers we can derive from the above + 2018 values
    energy: float = 0  # always just the sum of the demands
    change_energy_MWh: float = 0
    change_CO2e_t: float = 0
    change_CO2e_pct: float = 0
    change_energy_pct: float = 0

    transport2018: InitVar[Transport2018 | None] = None

    def __post_init__(self, transport2018: Transport2018 | None = None):
        self.energy = (
            self.demand_ejetfuel
            + self.demand_ediesel
            + self.demand_electricity
            + self.demand_epetrol
            + self.demand_hydrogen
        )
        if transport2018 is not None:
            self.calc_and_set_changes(transport2018)

    def calc_and_set_changes(self, transport2018: Transport2018) -> None:
        self.change_CO2e_t = (
            self.CO2e_combustion_based - transport2018.CO2e_combustion_based
        )
        self.change_energy_MWh = self.energy - transport2018.energy
        self.change_CO2e_pct = div(
            self.change_CO2e_t, transport2018.CO2e_combustion_based
        )
        self.change_energy_pct = div(self.change_energy_MWh, transport2018.energy)

    @classmethod
    def sum(cls, *transports: "Transport", transport2018: Transport2018) -> "Transport":
        """Aggregate two transports (e.g. road_bus + road_car).  Mostly this is
        just straightforward sums. But we also compute the percentages of
        change in comparison of energy and CO2e in 2018.
        """

        def sum_of(get: Callable[["Transport"], float]):
            return sum(map(get, transports))

        res = cls(
            CO2e_total=sum_of(lambda t: t.CO2e_total),
            CO2e_combustion_based=sum_of(lambda t: t.CO2e_combustion_based),
            CO2e_total_2021_estimated=sum_of(lambda t: t.CO2e_total_2021_estimated),
            change_km=sum_of(lambda t: t.change_km),
            cost_climate_saved=sum_of(lambda t: t.cost_climate_saved),
            transport_capacity_tkm=sum_of(lambda t: t.transport_capacity_tkm),
            transport_capacity_pkm=sum_of(lambda t: t.transport_capacity_pkm),
            demand_ejetfuel=sum_of(lambda t: t.demand_ejetfuel),
            demand_ediesel=sum_of(lambda t: t.demand_ediesel),
            demand_electricity=sum_of(lambda t: t.demand_electricity),
            demand_epetrol=sum_of(lambda t: t.demand_epetrol),
            demand_hydrogen=sum_of(lambda t: t.demand_hydrogen),
            transport2018=transport2018,
        )
        return res
