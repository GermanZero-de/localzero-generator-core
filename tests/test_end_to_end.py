"""This is a simplistic regression test framework for the generator."""
import json
import os
import pytest
import typing

from generatorcore.generator import calculate_with_default_inputs
from generatorcore import refdatatools, diffs

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


def end_to_end(datadir_status: refdatatools.DataDirStatus, ags, year=2035):
    """This runs an end to end test. No entries are overriden, only AGS"""
    root = refdatatools.root_of_this_repo()
    fname = f"production_{ags}_{year}.json"
    with open(os.path.join(root, "tests", "end_to_end_expected", fname)) as fp:
        expected = json.load(fp)
        g = calculate_with_default_inputs(ags=ags, year=year)
        got = g.result_dict()
        ds = list(diffs.all(expected, got))
        if ds:
            # Write a diff of the json
            for (p, e, g) in ds:
                print("at", p, "expected", e, "got", g)
            assert False, "End to end test failed"


# Default year = 2035
def test_end_to_end_goettingen(datadir_status):
    end_to_end(datadir_status, "03159016")


# Default year = 2035
def test_end_to_end_germany(datadir_status):
    end_to_end(datadir_status, "DG000000")


# Min year for the generator = 2021
def test_end_to_end_goettingen_2021(datadir_status):
    end_to_end(datadir_status, ags="03159016", year=2021)


# Min year for the website = 2025
def test_end_to_end_goettingen_2025(datadir_status):
    end_to_end(datadir_status, ags="03159016", year=2025)


# Max year for the generator and website = 2050
def test_end_to_end_goettingen_2050(datadir_status):
    end_to_end(datadir_status, ags="03159016", year=2050)
