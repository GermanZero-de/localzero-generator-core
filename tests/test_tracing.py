from climatevision.tracing.number import TracedNumber
from climatevision.generator import calculate_with_default_inputs
from climatevision.tracing import with_tracing


def test_literal():
    assert str(TracedNumber.lift(1)) == "1 : 1"


def test_binops():
    assert (
        str(TracedNumber.lift(1) / 2)
        == "0.5 : {'binary': '/', 'a': 1, 'b': 2, 'value': 0.5}"
    )
    assert (
        str(TracedNumber.lift(2) * 3)
        == "6 : {'binary': '*', 'a': 2, 'b': 3, 'value': 6}"
    )
    assert (
        str(TracedNumber.lift(2) * TracedNumber.lift(3))
        == "6 : {'binary': '*', 'a': 2, 'b': 3, 'value': 6}"
    )
    assert (
        str(TracedNumber.lift(1) + 2)
        == "3 : {'binary': '+', 'a': 1, 'b': 2, 'value': 3}"
    )
    assert (
        str(TracedNumber.lift(1) + TracedNumber.lift(2))
        == "3 : {'binary': '+', 'a': 1, 'b': 2, 'value': 3}"
    )
    assert (
        str(TracedNumber.lift(1) - TracedNumber.lift(2))
        == "-1 : {'binary': '-', 'a': 1, 'b': 2, 'value': -1}"
    )
    assert (
        str(TracedNumber.lift(1) - 2)
        == "-1 : {'binary': '-', 'a': 1, 'b': 2, 'value': -1}"
    )
    assert (
        str(3 - TracedNumber.lift(1))
        == "2 : {'binary': '-', 'a': 3, 'b': 1, 'value': 2}"
    )
    assert (
        str(3 + TracedNumber.lift(1))
        == "4 : {'binary': '+', 'a': 3, 'b': 1, 'value': 4}"
    )
    assert (
        str(6 / TracedNumber.lift(2))
        == "3.0 : {'binary': '/', 'a': 6, 'b': 2, 'value': 3.0}"
    )


def test_unary():
    assert str(-TracedNumber.lift(1)) == "-1 : {'unary': '-', 'a': 1}"


def test_is_integer():
    assert TracedNumber.lift(3).is_integer()
    assert TracedNumber.lift(3.0).is_integer()
    assert not TracedNumber.lift(3.4).is_integer()


def test_float():
    assert float(TracedNumber.lift(3)) == 3.0


def test_data():
    assert (
        str(TracedNumber.data(TracedNumber.lift(3), source="a", key="b", attr="c"))
    ) == "3 : {'source': 'a', 'key': 'b', 'attr': 'c', 'value': 3}"


def test_fact_or_ass():
    assert (
        str(TracedNumber.fact_or_ass("hello", 3))
        == "3 : {'fact_or_ass': 'hello', 'value': 3}"
    )


def test_comparisons():
    assert TracedNumber.lift(1) == 1
    assert TracedNumber.lift(1) == TracedNumber.lift(1)
    assert TracedNumber.lift(1) != TracedNumber.lift(2)  # type: ignore
    assert 1 == TracedNumber.lift(1)
    assert 1 < TracedNumber.lift(2)  # type: ignore
    assert TracedNumber.lift(1) < 2  # type: ignore


def test_enable_disable_tracing():
    """Here we do not care about the value computed nor do we care about the exact trace.
    What we do want is that the value stays the same across each run and that the trace
    can be disabled and enabled as expected."""

    # We check ENABLE -> DISABLE -> ENABLE to make sure that there are no
    # leftovers that only break on multiple runs
    expected_value = "55229.174057478296"
    expected_trace = (
        "{'binary': '+', 'a': {'name': 'a30.g_consult.cost_wage'}, 'b': {'name': 'a30.g_organic.cost_wage'}, 'value': "
        + expected_value
        + "}"
    )

    result = with_tracing(
        enabled=True,
        f=lambda: calculate_with_default_inputs(
            2018, "08416041", 2025, 2035
        ).result_dict(),
    )
    assert (
        str(result["a30"]["g"]["cost_wage"])  # type: ignore
        == "{'value': " + expected_value + ", 'trace': " + expected_trace + "}"
    )

    result = with_tracing(
        enabled=False,
        f=lambda: calculate_with_default_inputs(
            2018, "08416041", 2025, 2035
        ).result_dict(),
    )
    assert str(result["a30"]["g"]["cost_wage"]) == expected_value  # type: ignore

    result = with_tracing(
        enabled=True,
        f=lambda: calculate_with_default_inputs(
            2018, "08416041", 2025, 2035
        ).result_dict(),
    )
    assert (
        str(result["a30"]["g"]["cost_wage"])  # type: ignore
        == "{'value': " + expected_value + ", 'trace': " + expected_trace + "}"
    )
