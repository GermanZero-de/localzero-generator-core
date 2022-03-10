"""Module utils -- some useful classes or functions.

div
Percentage calculations usually imply a division. For some municipalities, however,
the data may be incomplete or irrelevant and the denominator happens to be zero.
In this case, a result of 0 is returned, also to avoid an exception.
"""
import typing
from dataclasses import fields


def div(a: float, b: float) -> float:
    return 0.0 if b == 0.0 else a / b


T = typing.TypeVar("T")


def element_wise_plus(a: T, b: T) -> T:
    return type(a)(*(getattr(a, f.name) + getattr(b, f.name) for f in fields(a)))
