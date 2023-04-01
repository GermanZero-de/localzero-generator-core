# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class Vars2:
    # Used by p, p_elec_elcon, p_elec_heatpump, p_vehicles, p_other
    energy: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars3:
    # Used by p_nonresi
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    number_of_buildings: float = None  # type: ignore


@dataclass(kw_only=True)
class Vars4:
    # Used by p_nonresi_com
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    pct_x: float = None  # type: ignore
