# pyright: strict

import inspect
import pytest

from climatevision.generator import Entries
from climatevision.generator import RefData
from climatevision.server import overridables


def create_valid_entries_values() -> dict[str, object]:
    """Creates a dictionary with default valid values for all Entries fields."""
    entries_values = {}
    signature = inspect.signature(Entries)

    for name, param in signature.parameters.items():
        if param.annotation == float or param.annotation == int:
            entries_values[name] = 0.0
        elif param.annotation == str:
            entries_values[name] = "test"

    return entries_values  # type: ignore


def test_sections_with_defaults():
    """This tests that calling populate_defaults does not raise an exception. We particularly
    want to protect against a incorrect name of a overridable field."""
    refdata = RefData.load(year_ref=2018)
    overridables.sections_with_defaults(refdata, "08416041", 2022, 2035)


def test_when_all_values_are_positive_then_assert_is_valid_is_successful():
    """Tests that assert_is_valid passes with non-negative numeric values."""
    valid_data = create_valid_entries_values()
    entry = Entries(**valid_data)  # type: ignore
    try:
        entry.assert_is_valid()
    except AssertionError as e:
        pytest.fail(f"assert_is_valid failed unexpectedly: {e}")


def test_when_float_value_is_negative_then_assert_is_valid_throws_exception():
    """Tests that assert_is_valid fails if a float field is negative."""
    invalid_data = create_valid_entries_values()
    invalid_data["a_biomass_fec"] = -10.5

    entry = Entries(**invalid_data)  # type: ignore
    with pytest.raises(AssertionError, match="a_biomass_fec should be 0 or positive"):
        entry.assert_is_valid()


def test_when_int_value_is_negative_then_assert_is_valid_throws_exception():
    """Tests that assert_is_valid fails if an int field is negative."""
    invalid_data = create_valid_entries_values()
    invalid_data["m_population_com_2018"] = -50

    entry = Entries(**invalid_data)  # type: ignore
    with pytest.raises(
        AssertionError, match="m_population_com_2018 should be 0 or positive"
    ):
        entry.assert_is_valid()
