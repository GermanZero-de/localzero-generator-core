"""This is a simplistic regression test framework for the generator."""

# pyright: strict

import json
import os
from dataclasses import asdict
from typing import Literal

import pytest

from climatevision.generator import (
    RefData,
    calculate_with_default_inputs,
    diffs,
    make_entries,
    refdatatools,
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


@pytest.fixture(
    params=[2018, 2021],
    ids=["year_ref_2018", "year_ref_2021"],
)
def year_ref(request):  # type: ignore
    return request.param  # type: ignore


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
    g = calculate_with_default_inputs(
        2018, ags="03159016", year_baseline=2025, year_target=2035
    )
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


def end_to_end(
    year_ref: int, ags: str, year_baseline: int = 2025, year_target: int = 2035
):
    """This runs an end to end test. No entries are overriden, only AGS"""
    root = refdatatools.root_of_this_repo()
    fname = f"production_{ags}_{year_baseline}_{year_target}.json"
    with open(
        os.path.join(root, "tests", "end_to_end_expected", f"{year_ref}", fname)
    ) as fp:
        expected = json.load(fp)
        g = calculate_with_default_inputs(
            year_ref=year_ref,
            ags=ags,
            year_baseline=year_baseline,
            year_target=year_target,
        )
        got = g.result_dict()
        ds = list(diffs.all(expected=expected, actual=got))  # type: ignore
        if ds:
            # Write a diff of the json
            for d in ds:
                print(d)
            assert False, "End to end test failed"

        assert diffs.float_matches(
            actual=g.f18.d.energy, expected=g.f18.p.energy, rel=1e-9
        ), f"f18 energy demand {g.f18.d.energy} is not equal to energy production {g.f18.p.energy}"
        assert diffs.float_matches(
            actual=g.h18.d.energy, expected=g.h18.p.energy, rel=1e-9
        ), f"h18 energy demand {g.h18.d.energy} is not equal to energy production {g.h18.p.energy}"


def make_entries_test(year_ref: int, ags: str, year_baseline: int, year_target: int):
    refdata = RefData.load(year_ref=year_ref)
    root = refdatatools.root_of_this_repo()
    fname = f"entries_{ags}_{year_baseline}_{year_target}.json"
    with open(
        os.path.join(root, "tests", "end_to_end_expected", f"{year_ref}", fname)
    ) as fp:
        expected = json.load(fp)
        e = make_entries(refdata, ags, year_baseline, year_target)
        got = asdict(e)
        ds = list(diffs.all(expected=expected, actual=got))  # type: ignore
        if ds:
            for d in ds:
                print(d)
            assert False, "make entries test failed"


def test_entries_test(year_ref: int):
    make_entries_test(year_ref, "03159016", 2025, 2035)


# Default year_baseline = 2025, default year_target = 2035
def test_end_to_end_goettingen(year_ref: int):
    end_to_end(year_ref, "03159016")


# Default year_baseline = 2025, default year_target = 2035
def test_end_to_end_germany(year_ref: int):
    end_to_end(year_ref, "DG000000")


# Min year_target for the generator = 2030
def test_end_to_end_goettingen_2030(year_ref: int):
    end_to_end(year_ref, ags="03159016", year_target=2030)


# Max year_target for the generator = 2050
def test_end_to_end_goettingen_2050(year_ref: int):
    end_to_end(year_ref, ags="03159016", year_target=2050)
