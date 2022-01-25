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
from generatorcore.refdata import Version

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


def is_repo_clean(path_to_repo: str) -> bool:
    # the output of git status --porcelain is guaranteed to be empty if the repository is clean
    porcelain = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        check=True,
        text=True,
        cwd=path_to_repo,
    ).stdout.strip()
    print(porcelain)
    return porcelain == ""


@pytest.fixture
def datadir():
    """Because the tests are not necessarily executes with cwd=<root-of-repo> we need to find
    the root of the repo first, so we know where to expect the datadir.
    """
    return os.path.normpath(os.path.join(root_of_this_repo(), "data"))


def get_hash_of_data_repo(r: PUBLIC_OR_PROP) -> str:
    root = root_of_this_repo()
    return get_git_hash(os.path.join(root, "data", r))


def head_of_repo_is(repo: PUBLIC_OR_PROP, expected_hash: str) -> bool:
    hash = get_hash_of_data_repo(repo)
    return hash == expected_hash


def test_datadir_contains_production_repos(datadir):
    version = Version.load("production", datadir=datadir)
    assert head_of_repo_is(
        "public", version.public
    ), f"Expected data/public to have checked out {version.public}"
    assert head_of_repo_is(
        "proprietary", version.proprietary
    ), f"Expected data/proprietary to have checked out {version.proprietary}"


def test_public_datadir_is_clean(datadir):
    assert is_repo_clean(
        os.path.join(datadir, "public")
    ), "There seem to be uncommitted / untracked files in the public data repository"


def test_proprietary_datadir_is_clean(datadir):
    assert is_repo_clean(
        os.path.join(datadir, "proprietary")
    ), "There seem to be uncommitted / untracked files in the proprietary data repository"


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
    """This runs an end to end test. No entries are overriden, only AGS"""
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
