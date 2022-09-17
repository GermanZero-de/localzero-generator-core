# pyright: strict

from climatevision.generator import RefData
from climatevision.server.overridables import populate_defaults


def test_populate_defaults():
    """This tests that calling populate_defaults does not raise an exception. We particularly
    want to protect against a incorrect name of a overridable field."""
    refdata = RefData.load()
    populate_defaults(refdata, "08416041", 2035)
