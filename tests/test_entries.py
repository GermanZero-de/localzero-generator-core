# pyright: strict

from climatevision.generator import RefData
from climatevision.server import overridables


def test_sections_with_defaults():
    """This tests that calling populate_defaults does not raise an exception. We particularly
    want to protect against a incorrect name of a overridable field."""
    refdata = RefData.load(year_ref=2018)
    overridables.sections_with_defaults(refdata, "08416041", 2022, 2035)
