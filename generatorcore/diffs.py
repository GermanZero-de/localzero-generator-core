"""Module diffs -- Utility module to compare to result dictionaries.

During testing and development it is often necessary to compare two result dictionaries.
"""
import collections.abc
import math
import numbers
import typing


def float_matches(actual, expected, rel):
    if math.isnan(actual) and math.isnan(expected):
        return True
    elif math.isnan(actual):
        return False
    elif math.isnan(expected):
        return False
    diff = math.fabs(actual - expected)
    reltol = math.fabs(expected) * rel
    if diff < reltol:
        return True
    if diff < 1e-12:
        return True
    return False


class MissingSentinel:
    def __str__(self):
        return "nothing"


MISSING_SENTINEL = MissingSentinel()


def all_helper(
    path: str, d1, d2, *, rel
) -> typing.Iterator[tuple[str, typing.Any, typing.Any]]:
    if isinstance(d1, collections.abc.Mapping) and isinstance(
        d2, collections.abc.Mapping
    ):
        keys1 = frozenset(d1.keys())
        keys2 = frozenset(d2.keys())
        shared_keys = keys1.intersection(keys2)
        for k in shared_keys:
            yield from all_helper(path + "." + k, d1[k], d2[k], rel=rel)
        for k in keys1 - shared_keys:
            yield from all_helper(path + "." + k, d1[k], MISSING_SENTINEL, rel=rel)
        for k in keys2 - shared_keys:
            yield from all_helper(path + "." + k, MISSING_SENTINEL, d2[k], rel=rel)
    elif isinstance(d1, collections.abc.Mapping) and d2 is MISSING_SENTINEL:
        for k in d1.keys():
            yield from all_helper(path + "." + k, d1[k], MISSING_SENTINEL, rel=rel)
    elif isinstance(d2, collections.abc.Mapping) and d1 is MISSING_SENTINEL:
        for k in d2.keys():
            yield from all_helper(path + "." + k, MISSING_SENTINEL, d2[k], rel=rel)
    elif isinstance(d1, numbers.Number) and isinstance(d2, numbers.Number):
        if not float_matches(actual=d1, expected=d2, rel=rel):
            yield (path, d1, d2)
    elif d1 != d2:
        yield (path, d1, d2)


def all(d1, d2, *, rel=1e6):
    return all_helper("", d1, d2, rel=rel)
