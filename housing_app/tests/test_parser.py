from pathlib import Path

import pytest

from housing_app.scraper.parser import parse_listings

SAMPLE_HTML = Path(__file__).parent / "fixtures" / "sample_page.html"

EXPECTED = [
    {
        "id": "3920246",
        "locality": "Łódź Bałuty",
        "rooms": "3",
        "area_m2": "44",
        "price_total_zl": "383000",
        "url_ends_with": "l7f5y5",
    },
    {
        "id": "3845120",
        "locality": "Łódź Widzew",
        "rooms": "2",
        "area_m2": "52",
        "price_total_zl": "520000",
        "url_ends_with": "a3b2c1",
    },
    {
        "id": "3901337",
        "locality": "Łódź Górna",
        "rooms": "4",
        "area_m2": "75",
        "price_total_zl": "680000",
        "url_ends_with": "x9y8z7",
    },
]


@pytest.fixture(scope="module")
def listings():
    html = SAMPLE_HTML.read_text(encoding="utf-8")
    return parse_listings(html)


@pytest.fixture(scope="module")
def listings_by_id(listings):
    return {l["id"]: l for l in listings}


def test_listing_count(listings):
    assert len(listings) == 3


def test_all_have_required_fields(listings):
    required = {"id", "url", "locality", "rooms", "area_m2", "price_total_zl", "price_per_m2_zl"}
    for listing in listings:
        assert set(listing.keys()) == required
        assert listing["id"] != ""
        assert listing["url"].startswith("https://")


@pytest.mark.parametrize("expected", EXPECTED, ids=[e["id"] for e in EXPECTED])
def test_listing_fields(listings_by_id, expected):
    listing = listings_by_id[expected["id"]]
    assert listing["locality"] == expected["locality"]
    assert listing["rooms"] == expected["rooms"]
    assert listing["area_m2"] == expected["area_m2"]
    assert listing["price_total_zl"] == expected["price_total_zl"]
    assert listing["url"].endswith(expected["url_ends_with"])
    expected_per_m2 = str(round(int(expected["price_total_zl"]) / int(expected["area_m2"])))
    assert listing["price_per_m2_zl"] == expected_per_m2
