# pyright: strict

from dataclasses import dataclass

from ...inputs import Inputs
from ...common.g import G, GPlanning

from .g_storage import GStorage


@dataclass(kw_only=True)
class General:
    g: G
    g_storage: GStorage
    g_planning: GPlanning


def calc_general(inputs: Inputs, p_heatnet_energy: float) -> General:

    g_planning = GPlanning.calc(inputs=inputs)
    g_storage = GStorage.calc(inputs=inputs, p_heatnet_energy=p_heatnet_energy)

    g = G.sum(g_planning, g_storage)

    return General(g=g, g_planning=g_planning, g_storage=g_storage)
