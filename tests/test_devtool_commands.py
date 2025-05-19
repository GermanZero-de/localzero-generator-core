# pyright: strict

import os

import pytest

from devtool import Devtool

filePath = "test.txt"


def check_cmd(argv1: object, subcmd: str, run: bool):
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
        [
            "run",
            "-ags",
            "10000000",
            "-year_target",
            "2040",
            "-year_ref",
            "2021",
            "-year_baseline",
            "2022",
            "-o",
            filePath,
        ],
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
        [
            "make",
            "-ags",
            "10000000",
            "-year_target",
            "2040",
            "-year_ref",
            "2021",
            "-year_baseline",
            "2022",
            "-o",
            filePath,
        ],
        "make",
        True,
    )

    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        assert False, "file " + filePath + " was not created"


def test_cmd_make_entries_with_invalid_ags():
    with pytest.raises(SystemExit) as excinfo:
        check_cmd(
            [
                "make",
                "-ags",
                "12345678",  # Invalid AGS value
                "-year_target",
                "2040",
                "-year_ref",
                "2018",
                "-o",
                "dummy_output_path",
            ],
            "make",
            False,
        )

    assert excinfo.value.code == 2


def test_cmd_make_entries_with_invalid_target_year():
    with pytest.raises(SystemExit) as excinfo:
        check_cmd(
            [
                "make",
                "-ags",
                "10000000",
                "-year_target",
                "2100",  # Invalid target year
                "-year_ref",
                "2018",
                "-o",
                filePath,
            ],
            "make",
            False,
        )

    assert excinfo.value.code == 2


def test_cmd_make_entries_with_invalid_ref_year():
    with pytest.raises(SystemExit) as excinfo:
        check_cmd(
            [
                "make",
                "-ags",
                "10000000",
                "-year_target",
                "2040",
                "-year_ref",
                "1999",  # Invalid ref year
                "-o",
                filePath,
            ],
            "make",
            False,
        )

    assert excinfo.value.code == 2


def test_cmd_make_entries_with_invalid_baseline_year():
    with pytest.raises(SystemExit) as excinfo:
        check_cmd(
            [
                "make",
                "-ags",
                "10000000",
                "-year_target",
                "2040",
                "-year_ref",
                "2018",
                "-year_baseline",
                "1999",  # Invalid baseline year
                "-o",
                filePath,
            ],
            "make",
            False,
        )

    assert excinfo.value.code == 2


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
    check_cmd(["data", "checkout"], "checkout", False)


def test_cmd_data_lookup_ags():
    check_cmd(
        ["data", "lookup", "10000000"],
        "lookup",
        True,
    )


def test_cmd_data_lookup_fact():
    check_cmd(
        ["data", "lookup", "Fact_M_CO2e_wo_lulucf_2016_vs_year_ref"],
        "lookup",
        True,
    )


def test_cmd_data_lookup_assumption():
    check_cmd(
        ["data", "lookup", "Ass_E_P_renew_nep_total_2035"],
        "lookup",
        True,
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
        False,  # You shouldn't run this as it will update expectations.
        # We only want people to do so when they have thought about it first.
    )


def test_cmd_test_end_to_end_create_expectations_with_defaults():
    check_cmd(
        ["test_end_to_end", "create_expectation"],
        "create_expectation",
        False,  # Same rationale as above
    )
