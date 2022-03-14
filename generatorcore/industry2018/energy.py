from dataclasses import dataclass


@dataclass
class Energy:
    # Used by s_fossil, s_renew
    energy: float = None  # type: ignore
