import argparse
import csv
import time
from pathlib import Path

import requests

from housing_app.scraper.downloader import fetch_html, city_page_url, DELAY_SECONDS
from housing_app.scraper.parser import parse_listings
from housing_app.scraper.detail_parser import parse_listing_detail, DETAIL_FIELDNAMES
from housing_app.export.csv_export import save_csv


def scrape_all_pages(city: str, max_pages: int = 50) -> list[dict]:
    all_listings: list[dict] = []
    seen_ids: set[str] = set()

    for page in range(1, max_pages + 1):
        url = city_page_url(city, page)
        print(f"Fetching page {page}: {url}")
        try:
            html = fetch_html(url)
        except requests.HTTPError as e:
            print(f"  HTTP error {e.response.status_code}, stopping.")
            break
        except requests.RequestException as e:
            print(f"  Request failed: {e}, stopping.")
            break

        listings = parse_listings(html)
        new = [l for l in listings if l["id"] not in seen_ids]
        seen_ids.update(l["id"] for l in new)
        all_listings.extend(new)
        print(f"  Parsed {len(listings)} listings, {len(new)} new (total: {len(all_listings)})")

        if not new:
            break

        time.sleep(DELAY_SECONDS)

    return all_listings


def enrich_with_details(listings: list[dict]) -> list[dict]:
    """Fetch each listing's detail page and merge fields into the listing dict."""
    enriched = []
    total = len(listings)
    for i, listing in enumerate(listings, 1):
        url = listing.get("url", "")
        print(f"  Detail {i}/{total}: {url}")
        try:
            html = fetch_html(url)
            detail = parse_listing_detail(html)
            enriched.append({**listing, **detail})
        except requests.RequestException as e:
            print(f"    Failed: {e}")
            enriched.append(listing)
        time.sleep(DELAY_SECONDS)
    return enriched


def save_detailed_csv(listings: list[dict], path: Path) -> None:
    base_fields = ["id", "url", "locality", "rooms", "area_m2", "price_total_zl", "price_per_m2_zl"]
    fieldnames = base_fields + [f for f in DETAIL_FIELDNAMES if f not in base_fields]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(listings)
    print(f"Saved {len(listings)} listings to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape apartment listings from adresowo.pl")
    parser.add_argument("city", help="City slug, e.g. lodz, mielec, krakow")
    parser.add_argument("--output", help="Output CSV path (default: adresowo_<city>.csv)")
    parser.add_argument("--details", action="store_true",
                        help="Also fetch each listing's detail page for extended data")
    args = parser.parse_args()

    output = Path(args.output) if args.output else Path.cwd() / f"adresowo_{args.city}.csv"

    listings = scrape_all_pages(args.city)
    if not listings:
        print("No listings found.")
        return

    if args.details:
        print(f"\nFetching details for {len(listings)} listings...")
        listings = enrich_with_details(listings)
        save_detailed_csv(listings, output)
    else:
        save_csv(listings, output)
        print(f"Saved {len(listings)} listings to {output}")


if __name__ == "__main__":
    main()
