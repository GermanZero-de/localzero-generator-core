"""This is a simplistic regression test framework for the generator."""
import collections.abc
import difflib
import json
import numbers
import os
import pytest
import subprocess
import sys
import typing

from generatorcore.generator import calculate_with_default_inputs

CURRENT_PUBLIC_DATA_HASH = "c64c73ff852777ba0fdab2e9a6d7b44eca847af6"

CURRENT_PROPRIETARY_DATA_HASH = "b8dc6c23d1bf7372693887ea0856cd74d8bfc263"

PUBLIC_OR_PROP = typing.Literal["public", "proprietary"]


def get_git_hash(path_to_repo: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
        cwd=path_to_repo,
    ).stdout.strip()


def root_of_this_repo() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip()


def get_hash_of_data_repo(r: PUBLIC_OR_PROP) -> str:
    root = root_of_this_repo()
    return get_git_hash(os.path.join(root, "data", r))


def assert_repo_is_unchanged(repo: PUBLIC_OR_PROP, expected: str):
    hash = get_hash_of_data_repo(repo)
    assert (
        hash == expected
    ), f"Have you changed the {repo} repository on purpose? If so update the hash above."


def test_public_repo_has_not_been_changed():
    assert_repo_is_unchanged("public", CURRENT_PUBLIC_DATA_HASH)


def test_proprietary_repo_has_not_changed():
    assert_repo_is_unchanged("proprietary", CURRENT_PROPRIETARY_DATA_HASH)


def find_diffs(path: str, d1, d2) -> list[tuple[str, typing.Any, typing.Any]]:
    if d1 is None and d2 is None:
        return []
    elif type(d1) is str and type(d2) is str:
        if d1 == d2:
            return []
        else:
            return [(path, d1, d2)]
    elif isinstance(d1, numbers.Number) and isinstance(d2, numbers.Number):
        if d1 == pytest.approx(d2, nan_ok=True):
            return []
        else:
            return [(path, d1, d2)]
    elif isinstance(d1, collections.abc.Mapping) and isinstance(
        d2, collections.abc.Mapping
    ):
        if d1.keys() != d2.keys():
            return [(path, d1, d2)]
        else:
            diffs = []
            for k in d1.keys():
                diffs.extend(
                    find_diffs(("" if path == "" else path + ".") + k, d1[k], d2[k])
                )
            return diffs
    else:
        return [(path, d1, d2)]


def end_to_end(ags):
    public_hash = get_hash_of_data_repo("public")
    proprietary_hash = get_hash_of_data_repo("proprietary")
    root = root_of_this_repo()
    fname = f"{public_hash}_{proprietary_hash}_{ags}.json"
    with open(os.path.join(root, "tests", "end_to_end_expected", fname)) as fp:
        expected = json.load(fp)
        g = calculate_with_default_inputs(ags=ags, year=2035)
        got = g.result_dict()
        diffs = find_diffs("", expected, got)
        if diffs:
            # Write a diff of the json
            for (p, e, g) in diffs:
                print("at", p, "expected", e, "got", g)
            assert False, "End to end test failed"


def test_end_to_end_goettingen():
    end_to_end("03159016")
