# pyright: strict
from typing import Any
from devtool import Devtool
import os

filePath = "test.txt"


def check_cmd(argv1: Any, subcmd: str, run: bool):
    args = Devtool().parse_args(argv1)
    assert args.subcmd is subcmd
    if run:
        args.func(args)


def test_cmd_run_with_defaults():
    check_cmd(["run"], "run", True)


def test_cmd_run_with_parameters():
    if os.path.exists(filePath):
        assert False, "file " + filePath + " already exists"

    check_cmd(
        ["run", "-ags", "10000000", "-year", "2040", "-o", filePath],
        "run",
        True,
    )

    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        assert False, "file " + filePath + " was not created"


def test_cmd_make_entries_with_defaults():
    check_cmd(["make"], "make", True)


def test_cmd_make_entries_with_parameters():
    if os.path.exists(filePath):
        assert False, "file " + filePath + " already exists"

    check_cmd(
        ["make", "-ags", "10000000", "-year", "2040", "-o", filePath],
        "make",
        True,
    )

    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        assert False, "file " + filePath + " was not created"


def test_cmd_explorer():
    check_cmd(
        ["explorer"],
        "explorer",
        False,  # You can't run this command here, because it won't return.
    )


def test_cmd_ready_to_rock():
    check_cmd(
        ["ready_to_rock"],
        "ready_to_rock",
        False,  # You can't run this command here otherwise it will call the tests and create an infinite loop.
    )


def test_cmd_data_is_production():
    check_cmd(["data", "is-production"], "is-production", True)


def test_cmd_data_checkout():
    check_cmd(["data", "checkout"], "checkout", True)


def test_cmd_data_lookup_ags():
    check_cmd(
        ["data", "lookup", "10000000"],
        "lookup",
        True,
    )


"""
def test_cmd_data_lookup_fact():
    check_cmd(
        ["data", "lookup", "Fact_M_CO2e_wo_lulucf_2015_vs_2018"],
        "lookup",
        True,
    )
"""


def test_cmd_data_lookup_assumption():
    check_cmd(
        ["data", "lookup", "Ass_E_P_renew_nep_total_2035"],
        "lookup",
        True,
    )


def test_cmd_data_entries_user_overrides_generate_defaults():
    check_cmd(
        ["data", "entries-user-overrides-generate-defaults"],
        "entries-user-overrides-generate-defaults",
        False,  # You shouldn't run this function here. It will need too much time.
    )


def test_cmd_test_end_to_end_run_all_ags():
    check_cmd(
        ["test_end_to_end", "run_all_ags"],
        "run_all_ags",
        False,  # You shouldn't run this function here. It will need too much time.
    )


def test_cmd_test_end_to_end_update_expectations():
    check_cmd(
        ["test_end_to_end", "update_expectations"],
        "update_expectations",
        False  # You shouldn't run this as it will update expectations.
        # We only want people to do so when they have thought about it first.
    )


def test_cmd_test_end_to_end_create_expectations_with_defaults():
    check_cmd(
        ["test_end_to_end", "create_expectation"],
        "create_expectation",
        False,  # Same rationale as above
    )
