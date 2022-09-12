# pyright: strict

"""This module provides optional facility to generate a trace of the calculation as the
calculation is done. Used by the explorer. Not used by the Klimavision website.
"""

from .monkeypatch import maybe_enable_tracing as maybe_enable

__all__ = ["maybe_enable"]
