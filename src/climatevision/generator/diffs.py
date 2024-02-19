"""Module diffs -- Utility module to compare to result dictionaries.

During testing and development it is often necessary to compare two result dictionaries.
"""

# pyright: strict

from dataclasses import dataclass
from typing import Any, Iterator
from collections.abc import Mapping
from math import isnan, fabs
from numbers import Number


def float_matches(actual: Any, expected: Any, rel: float):
    if isnan(actual) and isnan(expected):
        return True
    elif isnan(actual):
        return False
    elif isnan(expected):
        return False
    reltol = fabs(expected) * rel
    diff = fabs(actual - expected)
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

    def csv(self) -> list[str]:
        return [self.path, str(self.expected), str(self.actual)]


@dataclass(kw_only=True)
class FloatDiff(Diff):
    path: str

    def diff_in_percent(self) -> float:
        actual: float = float(self.actual)  # type: ignore
        expected: float = float(self.expected)  # type: ignore
        diff: float = actual - expected
        one_percent: float = expected / 100.0 if expected != 0 else 0
        if one_percent != 0:
            return diff / one_percent
        else:
            return 0

    def __str__(self) -> str:
        percent = self.diff_in_percent()
        return f"at {self.path} expected {self.expected} got {self.actual} ({percent:.2f}%)"

    def csv(self) -> list[str]:
        return [
            self.path,
            str(self.expected),
            str(self.actual),
            str(self.diff_in_percent()),
        ]


def all_helper(path: str, actual: Any, expected: Any, *, rel: float) -> Iterator[Diff]:
    if isinstance(actual, Mapping) and isinstance(expected, Mapping):
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
    elif isinstance(actual, Mapping) and expected is MISSING_SENTINEL:
        for k in actual.keys():  # type: ignore
            yield from all_helper(path + "." + k, actual[k], MISSING_SENTINEL, rel=rel)  # type: ignore
    elif isinstance(expected, Mapping) and actual is MISSING_SENTINEL:
        for k in expected.keys():  # type: ignore
            yield from all_helper(
                path + "." + k, MISSING_SENTINEL, expected[k], rel=rel  # type: ignore
            )
    elif isinstance(actual, Number) and isinstance(expected, Number):
        if not float_matches(actual=actual, expected=expected, rel=rel):
            yield FloatDiff(path=path, actual=actual, expected=expected)
    elif hasattr(actual, "__float__") and hasattr(expected, "__float__"):  # type: ignore
        f = float(actual)  # type: ignore
        e = float(expected)  # type: ignore
        if not float_matches(actual=f, expected=e, rel=rel):
            yield FloatDiff(path=path, actual=f, expected=e)  # type: ignore
    elif actual != expected:
        yield Diff(path=path, actual=actual, expected=expected)  # type: ignore


def all(*, actual: Any, expected: Any, rel: float = 1e-9):
    return all_helper("", actual, expected, rel=rel)
