# pyright: strict

from dataclasses import dataclass

from ...common.energy import Energy

from .efuel_production import EFuelProduction


@dataclass(kw_only=True)
class EFuels(Energy):
    change_CO2e_t: float

    @classmethod
    def calc(cls, *efuels: EFuelProduction) -> "EFuels":
        change_CO2e_t = sum(e.change_CO2e_t for e in efuels)
        energy = sum(e.energy for e in efuels)
        return cls(change_CO2e_t=change_CO2e_t, energy=energy)
