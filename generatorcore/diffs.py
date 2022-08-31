"""Module diffs -- Utility module to compare to result dictionaries.

During testing and development it is often necessary to compare two result dictionaries.
"""
# pyright: strict
from dataclasses import dataclass
import collections.abc
import math
import numbers
from typing import Any, Iterator

from . import tracednumber


def float_matches(actual: Any, expected: Any, rel: Any):
    if math.isnan(actual) and math.isnan(expected):
        return True
    elif math.isnan(actual):
        return False
    elif math.isnan(expected):
        return False
    reltol = math.fabs(expected) * rel
    diff = math.fabs(actual - expected)
    if diff < reltol:
        return True
    if diff < 1e-12:
        return True
    return False


@dataclass(kw_only=True)
class MissingSentinel:
    def __str__(self):
        return "nothing"


MISSING_SENTINEL = MissingSentinel()


@dataclass(kw_only=True)
class Diff:
    path: str
    actual: object
    expected: object

    def __str__(self) -> str:
        return f"at {self.path} expected {self.expected} got {self.actual}"


def all_helper(path: str, actual: Any, expected: Any, *, rel: Any) -> Iterator[Diff]:
    if isinstance(actual, collections.abc.Mapping) and isinstance(
        expected, collections.abc.Mapping
    ):
        keys1: Any = frozenset(actual.keys())  # type: ignore
        keys2: Any = frozenset(expected.keys())  # type: ignore
        shared_keys = keys1.intersection(keys2)
        for k in shared_keys:
            yield from all_helper(path + "." + k, actual[k], expected[k], rel=rel)
        for k in keys1 - shared_keys:
            yield from all_helper(path + "." + k, actual[k], MISSING_SENTINEL, rel=rel)
        for k in keys2 - shared_keys:
            yield from all_helper(
                path + "." + k, MISSING_SENTINEL, expected[k], rel=rel
            )
    elif isinstance(actual, collections.abc.Mapping) and expected is MISSING_SENTINEL:
        for k in actual.keys():  # type: ignore
            yield from all_helper(path + "." + k, actual[k], MISSING_SENTINEL, rel=rel)  # type: ignore
    elif isinstance(expected, collections.abc.Mapping) and actual is MISSING_SENTINEL:
        for k in expected.keys():  # type: ignore
            yield from all_helper(
                path + "." + k, MISSING_SENTINEL, expected[k], rel=rel  # type: ignore
            )
    elif isinstance(actual, numbers.Number) and isinstance(expected, numbers.Number):
        if not float_matches(actual=actual, expected=expected, rel=rel):
            yield Diff(path=path, actual=actual, expected=expected)
    elif isinstance(actual, tracednumber.TracedNumber):
        if not float_matches(actual=actual.value, expected=expected, rel=rel):
            yield Diff(path=path, actual=actual, expected=expected)
    elif actual != expected:
        yield Diff(path=path, actual=actual, expected=expected)  # type: ignore


def all(*, actual, expected, rel=1e-9):  # type: ignore
    return all_helper("", actual, expected, rel=rel)
