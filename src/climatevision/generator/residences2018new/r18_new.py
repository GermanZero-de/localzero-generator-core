# pyright: strict

from dataclasses import dataclass


@dataclass(kw_only=True)
class R18New:
    dummy: float = None  # type: ignore
    r: float = None  # type: ignore
    p: float = None  # type: ignore
    p_dummy: float = None  # type: ignore
    s: float = None  # type: ignore
    s_dummy: float = None  # type: ignore
