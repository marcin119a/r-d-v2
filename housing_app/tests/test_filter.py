import pytest

from housing_app.processing.filters import filter_listings


@pytest.fixture
def sample_listings():
    return [
        {"id": "1", "locality": "Bałuty", "rooms": "2", "area_m2": "45", "price_total_zl": "300000", "price_per_m2_zl": "6667"},
        {"id": "2", "locality": "Śródmieście", "rooms": "3", "area_m2": "65", "price_total_zl": "500000", "price_per_m2_zl": "7692"},
        {"id": "3", "locality": "Widzew", "rooms": "1", "area_m2": "30", "price_total_zl": "200000", "price_per_m2_zl": "6667"},
        {"id": "4", "locality": "Polesie", "rooms": "4", "area_m2": "90", "price_total_zl": "700000", "price_per_m2_zl": "7778"},
        {"id": "5", "locality": "Bałuty", "rooms": "2", "area_m2": "50", "price_total_zl": "350000", "price_per_m2_zl": "7000"},
        {"id": "6", "locality": "Górna", "rooms": "", "area_m2": "", "price_total_zl": "", "price_per_m2_zl": ""},
    ]


def test_no_filters_returns_all(sample_listings):
    result = filter_listings(sample_listings)
    assert len(result) == 6


def test_min_price(sample_listings):
    result = filter_listings(sample_listings, min_price=350000)
    assert all(int(l["price_total_zl"]) >= 350000 for l in result)
    assert len(result) == 3


def test_max_price(sample_listings):
    result = filter_listings(sample_listings, max_price=300000)
    ids = [l["id"] for l in result]
    assert ids == ["1", "3"]


def test_price_range(sample_listings):
    result = filter_listings(sample_listings, min_price=300000, max_price=500000)
    ids = [l["id"] for l in result]
    assert ids == ["1", "2", "5"]


def test_min_area(sample_listings):
    result = filter_listings(sample_listings, min_area=50)
    ids = [l["id"] for l in result]
    assert ids == ["2", "4", "5"]


def test_max_area(sample_listings):
    result = filter_listings(sample_listings, max_area=45)
    ids = [l["id"] for l in result]
    assert ids == ["1", "3"]


def test_single_room(sample_listings):
    result = filter_listings(sample_listings, rooms=[2])
    ids = [l["id"] for l in result]
    assert ids == ["1", "5"]


def test_multiple_rooms(sample_listings):
    result = filter_listings(sample_listings, rooms=[2, 3])
    ids = [l["id"] for l in result]
    assert ids == ["1", "2", "5"]


def test_locality_substring(sample_listings):
    result = filter_listings(sample_listings, locality="bałuty")
    ids = [l["id"] for l in result]
    assert ids == ["1", "5"]


def test_combined_filters(sample_listings):
    result = filter_listings(sample_listings, rooms=[2, 3], min_area=40, max_price=400000)
    ids = [l["id"] for l in result]
    assert ids == ["1", "5"]


def test_empty_numeric_excluded_by_price_filter(sample_listings):
    result = filter_listings(sample_listings, min_price=0)
    assert all(l["id"] != "6" for l in result)


def test_empty_numeric_excluded_by_area_filter(sample_listings):
    result = filter_listings(sample_listings, min_area=0)
    assert all(l["id"] != "6" for l in result)


def test_empty_numeric_excluded_by_rooms_filter(sample_listings):
    result = filter_listings(sample_listings, rooms=[1, 2, 3, 4])
    assert all(l["id"] != "6" for l in result)
