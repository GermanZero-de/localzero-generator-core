End to end test expected results
================================

This directory contains one file per ags it ran for. Those are encoded in the filename: `production_<ags>.json`

If you want to generate a fresh version of all expected results call 'python devtool.py test_end_to_end update_expectations'.
If you want to create a new expectation file for a new ags call 'python devtool.py test_end_to_end create_expectation -ags <ags>'.

    TODO: This currently doesn't handle any other inputs (e.g. year=...) or any of the others
    and indeed just adding those to the filename will eventually not scale anymore ;-) But
    again a problem for another day.
