"""This is a simplistic regression test framework for the generator."""
import collections.abc
import json
import numbers
import os
import pytest
import typing

from generatorcore.generator import calculate_with_default_inputs
from generatorcore import refdatatools

PUBLIC_OR_PROP = typing.Literal["public", "proprietary"]


@pytest.fixture
def datadir():
    """Because the tests are not necessarily executes with cwd=<root-of-repo> we need to find
    the root of the repo first, so we know where to expect the datadir.
    """
    return refdatatools.datadir()


@pytest.fixture
def datadir_status():
    return refdatatools.DataDirStatus.get(refdatatools.datadir())


def test_datadir_proprietary_has_production_checked_out(
    datadir_status: refdatatools.DataDirStatus,
):
    assert (
        datadir_status.proprietary_status.rev == datadir_status.production.proprietary
    ), f"Expected data/proprietary to have checked out {datadir_status.production.proprietary}"


def test_datadir_public_has_production_checked_out(
    datadir_status: refdatatools.DataDirStatus,
):
    assert (
        datadir_status.public_status.rev == datadir_status.production.public
    ), f"Expected data/public to have checked out {datadir_status.production.public}"


def test_public_datadir_is_clean(datadir_status: refdatatools.DataDirStatus):
    assert (
        datadir_status.public_status.is_clean
    ), "There seem to be uncommitted / untracked files in the public data repository"


def test_proprietary_datadir_is_clean(datadir_status):
    assert (
        datadir_status.proprietary_status.is_clean
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


def end_to_end(datadir_status: refdatatools.DataDirStatus, ags):
    """This runs an end to end test. No entries are overriden, only AGS"""
    root = refdatatools.root_of_this_repo()
    fname = f"production_{ags}.json"
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


def test_end_to_end_goettingen(datadir_status):
    end_to_end(datadir_status, "03159016")
