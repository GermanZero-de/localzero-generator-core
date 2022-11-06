"""This is a simplistic regression test framework for the generator."""

# pyright: strict

from dataclasses import asdict
from typing import Any, Literal
import json
import os
import pytest

from climatevision.generator import (
    refdatatools,
    diffs,
    make_entries,
    calculate_with_default_inputs,
    RefData,
)

PUBLIC_OR_PROP = Literal["public", "proprietary"]


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


def test_proprietary_datadir_is_clean(datadir_status: refdatatools.DataDirStatus):
    assert (
        datadir_status.proprietary_status.is_clean
    ), "There seem to be uncommitted / untracked files in the proprietary data repository"


def test_all_used_variables_are_populated():
    """This tests that the variables that are actually used by knud haven't changed.
    In principle this test is of course redundant, given the end to end tests. But
    As long as we are cleaning up the Result type, it is good to have an explicit
    reminder when we change that something that will need KNUD to be adjusted.
    """
    root = refdatatools.root_of_this_repo()
    g = calculate_with_default_inputs(ags="03159016", year=2035)
    result = g.result_dict()
    with open(os.path.join(root, "tests", "usage.json")) as fp:
        usage = json.load(fp)
    missing = set()  # type: ignore
    populated_with_none = set()  # type: ignore
    for path in usage["generator"]:
        next = result
        for element in path.split("."):
            if element in next:
                next = next[element]  # type: ignore
                if next is None:
                    populated_with_none.add(path)  # type: ignore
                    break
            else:
                missing.add(path)  # type: ignore
                break
    assert (
        len(missing) == 0  # type: ignore
    ), f"The following variables are used by KNUD but not populated: {missing}"
    assert (
        len(populated_with_none) == 0  # type: ignore
    ), f"The following variables are used by KNUD but populated with None: {populated_with_none}"


def end_to_end(datadir_status: refdatatools.DataDirStatus, ags: Any, year: int = 2035):
    """This runs an end to end test. No entries are overriden, only AGS"""
    root = refdatatools.root_of_this_repo()
    fname = f"production_{ags}_{year}.json"
    with open(os.path.join(root, "tests", "end_to_end_expected", fname)) as fp:
        expected = json.load(fp)
        g = calculate_with_default_inputs(ags=ags, year=year)
        got = g.result_dict()
        ds = list(diffs.all(expected=expected, actual=got))  # type: ignore
        if ds:
            # Write a diff of the json
            for d in ds:
                print(d)
            assert False, "End to end test failed"

        assert diffs.float_matches(
            actual=g.h18.d.energy, expected=g.h18.p.energy, rel=1e-9
        ), f"h18 energy demand {g.h18.d.energy} is not equal to energy production {g.h18.p.energy}"


def make_entries_test(ags: Any, year: int):
    refdata = RefData.load()
    root = refdatatools.root_of_this_repo()
    fname = f"entries_{ags}_{year}.json"
    with open(os.path.join(root, "tests", "end_to_end_expected", fname)) as fp:
        expected = json.load(fp)
        e = make_entries(refdata, ags, year)
        got = asdict(e)
        ds = list(diffs.all(expected=expected, actual=got))  # type: ignore
        if ds:
            for d in ds:
                print(d)
            assert False, "make entries test failed"


def test_entries_test():
    make_entries_test("03159016", 2035)


# Default year = 2035
def test_end_to_end_goettingen(datadir_status: refdatatools.DataDirStatus):
    end_to_end(datadir_status, "03159016")


# Default year = 2035
def test_end_to_end_germany(datadir_status: refdatatools.DataDirStatus):
    end_to_end(datadir_status, "DG000000")


# Min year for the generator = 2021
def test_end_to_end_goettingen_2021(datadir_status: refdatatools.DataDirStatus):
    end_to_end(datadir_status, ags="03159016", year=2021)


# Min year for the website = 2025
def test_end_to_end_goettingen_2025(datadir_status: refdatatools.DataDirStatus):
    end_to_end(datadir_status, ags="03159016", year=2025)


# Max year for the generator and website = 2050
def test_end_to_end_goettingen_2050(datadir_status: refdatatools.DataDirStatus):
    end_to_end(datadir_status, ags="03159016", year=2050)
