import json
import collections.abc
import typing
import numbers
import math


def sanitize_excel(e):
    """We are not interested in string values and some odd keys can be thrown away too"""
    if isinstance(e, dict):
        return {
            k: sanitize_excel(v)
            for k, v in e.items()
            if k != "\u00a0" and not isinstance(v, str)
        }
    else:
        return e


def remove_null_values(r):
    """Because of the way we have declared types we produce too many values."""
    if isinstance(r, dict):
        return {k: v for k, v in r.items() if v is not None}
    else:
        return r


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


def find_diffs(
    path: str, d1, d2, *, rel
) -> typing.Iterator[tuple[str, typing.Any, typing.Any]]:
    if isinstance(d1, collections.abc.Mapping) and isinstance(
        d2, collections.abc.Mapping
    ):
        keys1 = frozenset(d1.keys())
        keys2 = frozenset(d2.keys())
        shared_keys = keys1.intersection(keys2)
        for k in shared_keys:
            yield from find_diffs(path + "." + k, d1[k], d2[k], rel=rel)
        for k in keys1 - shared_keys:
            yield from find_diffs(path + "." + k, d1[k], None, rel=rel)
        for k in keys2 - shared_keys:
            yield from find_diffs(path + "." + k, None, d2[k], rel=rel)
    elif isinstance(d1, collections.abc.Mapping) and d2 is None:
        for k in d1.keys():
            yield from find_diffs(path + "." + k, d1[k], None, rel=rel)
    elif isinstance(d2, collections.abc.Mapping) and d1 is None:
        for k in d2.keys():
            yield from find_diffs(path + "." + k, None, d2[k], rel=rel)
    elif isinstance(d1, numbers.Number) and isinstance(d2, numbers.Number):
        if not float_matches(actual=d1, expected=d2, rel=rel):
            yield (path, d1, d2)
    elif d1 != d2:
        yield (path, d1, d2)


def cmd_compare_to_excel(args):
    def pr3(a, b, c):
        if b is None:
            b = "MISSING"
        elif b == {}:
            b = "{}"
        if c is None:
            c = "MISSING"
        elif c == {}:
            c = "{}"
        print(f"{a:<50}{b:>25}{c:>25}")

    with open(args.result_file) as fp:
        result = remove_null_values(json.load(fp))
    with open(args.excel_file) as fp:
        excel = sanitize_excel(json.load(fp))
    diffs = find_diffs("", result, excel, rel=float(args.relative_tolerance))
    if diffs:
        pr3("PATH", "RESULT", "EXCEL")
        for (p, r, x) in diffs:
            if args.show_missing_in_excel or x != None:
                pr3(p, r, x)
