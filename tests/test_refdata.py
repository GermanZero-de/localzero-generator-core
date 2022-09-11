"""Tests of the reference data.
   Note as we test some values derived from the reference data, these tests might need to
   be adapted when our reference data changes.  This is by design. Our reference data
   changes seldomly and when it does it is normally on purpose and thereby having to
   adjust some tests that e.g. check that loading the reference / computing derived
   values / fixing holes in the data works, is an ok tradeoff, to spending a long
   time trying to figure out a bug in the generator when it is actually in the loading
   of the reference data module.
"""
import pytest

from lzcv.generator import RefData

FEDERAL_STATES = ["%02i000000" % i for i in range(1, 17)]


@pytest.fixture
def refdata():
    return RefData.load()


def test_traffic_has_an_entry_for_every_federal_state(refdata: RefData):
    for ags in FEDERAL_STATES:
        refdata.traffic(ags)


def test_traffic_agg_for_baden_wuerttemberg(refdata: RefData):
    """Test one aggregation (assuming that if one works it's unlikely that the others fail)"""
    t = refdata.traffic("08000000")
    assert t.float("car_it_ot") == pytest.approx(68352.911991)
    assert t.float("car_ab") == pytest.approx(21371.105574)
    assert t.float("ldt_it_ot") == pytest.approx(5176.741946)
    assert t.float("ldt_ab") == pytest.approx(1238.013404)
    assert t.float("mhd_it_ot") == pytest.approx(4297.24258)
    assert t.float("mhd_ab") == pytest.approx(3756.971882)
    assert t.float("rail_ppl_elec") == pytest.approx(723089.115148)
    assert t.float("rail_ppl_diesel") == pytest.approx(548120.18989)
    assert t.float("gds_elec") == pytest.approx(430495.602542)
    assert t.float("gds_diesel") == pytest.approx(62133.032561)


def test_traffic_agg_for_tuebingen_administrative_district(refdata: RefData):
    """Test one aggregation on the administrative district level (as opposed to municipality)"""
    t = refdata.traffic("08416000")
    assert t.float("car_it_ot") == pytest.approx(1482.892553)
    assert t.float("car_ab") == pytest.approx(218.22056)
    assert t.float("ldt_it_ot") == pytest.approx(113.231857)
    assert t.float("ldt_ab") == pytest.approx(14.24184)
    assert t.float("mhd_it_ot") == pytest.approx(85.360104)
    assert t.float("mhd_ab") == pytest.approx(27.324456)
    assert t.float("rail_ppl_elec") == pytest.approx(2663.7081)
    assert t.float("rail_ppl_diesel") == pytest.approx(16807.108653)
    assert t.float("gds_elec") == pytest.approx(212.596949)
    assert t.float("gds_diesel") == pytest.approx(39.325871)


def test_co2path(refdata: RefData):
    """co2path is the only refdata with an integer key. So check at least one lookup in there."""
    p = refdata.co2path(2035)
    assert p.float("GHG_budget_2016_to_year") == pytest.approx(7923139996.0)
    assert p.float("nonCO2_budget_2016_to_year") == pytest.approx(1586688275)
