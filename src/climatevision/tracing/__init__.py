# pyright: strict

"""This module provides optional facility to generate a trace of the calculation as the
calculation is done. Used by the explorer. Not used by the Klimavision website.
"""

from .monkeypatch import with_tracing, enable_tracing

__all__ = ["with_tracing", "enable_tracing"]
