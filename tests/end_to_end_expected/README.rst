End to end test expected results
================================

This directory contains one file per version of the reference data and ags it ran for. Those
three things are encoded in the filename: `<hash-of-data/public>_<hash-of-data/proprietary>_<ags>.json`

If you want to generate a fresh version of such a file `python devtool.py run` is your friend.

    TODO: This currently doesn't handle any other inputs (e.g. year=...) or any of the others
    and indeed just adding those to the filename will eventually not scale anymore ;-) But
    again a problem for another day.
