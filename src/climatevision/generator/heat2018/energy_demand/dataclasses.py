# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class Vars1:
    energy: float
