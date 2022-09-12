# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class Energy:
    # Used by p_operation, p_operation_elec_heatpump
    energy: float
