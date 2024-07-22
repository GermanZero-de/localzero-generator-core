End to end test expected results
================================

This directory contains one file per ags and year combination it ran for. Those are encoded in the filename: `production_<ags>_<year_baseline>_<year_target>.json`
The year of the reference data is encoded in the foldername.

If you want to generate a fresh version of all expected results call 'python devtool.py test_end_to_end update_expectations'.
If you want to create a new expectation file for a new ags call 'python devtool.py test_end_to_end create_expectation -ags <ags> -year_baseline <year_baseline> -year_target <year_target>'.
