# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class EnergySupply:
    total: float = None  # type: ignore
    dummy: float = None  # type: ignore


def calc_supply() -> EnergySupply:

    return EnergySupply(dummy=0)
