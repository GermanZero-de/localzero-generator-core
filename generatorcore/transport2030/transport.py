from dataclasses import dataclass
from ..utils import div


@dataclass
class Transport:
    CO2e_total: float
    CO2e_combustion_based: float
    CO2e_total_2021_estimated: float
    change_CO2e_t: float
    change_energy_MWh: float
    change_km: float
    energy: float
    cost_climate_saved: float
    transport_capacity_tkm: float
    transport_capacity_pkm: float
    change_CO2e_pct: float
    change_energy_pct: float

    @classmethod
    def sum(
        cls, a: "Transport", b: "Transport", energy_2018: float, co2e_2018: float
    ) -> "Transport":
        change_CO2e_t = a.change_CO2e_t + b.change_CO2e_t
        change_energy_MWh = a.change_energy_MWh + b.change_energy_MWh
        return cls(
            CO2e_total=a.CO2e_total + b.CO2e_total,
            CO2e_combustion_based=a.CO2e_combustion_based + b.CO2e_combustion_based,
            CO2e_total_2021_estimated=a.CO2e_total_2021_estimated
            + b.CO2e_total_2021_estimated,
            change_CO2e_t=a.change_CO2e_t + b.change_CO2e_t,
            change_energy_MWh=a.change_energy_MWh + b.change_energy_MWh,
            change_km=a.change_km + b.change_km,
            energy=a.energy + b.energy,
            cost_climate_saved=a.cost_climate_saved + b.cost_climate_saved,
            transport_capacity_tkm=a.transport_capacity_tkm + b.transport_capacity_tkm,
            transport_capacity_pkm=a.transport_capacity_pkm + b.transport_capacity_pkm,
            change_CO2e_pct=div(change_CO2e_t, co2e_2018),
            change_energy_pct=div(change_energy_MWh, energy_2018),
        )
