import csv
from pathlib import Path


DEFAULT_FIELDNAMES = ["id", "url", "locality", "rooms", "area_m2", "price_total_zl", "price_per_m2_zl"]


def save_csv(listings: list[dict], path: Path, fieldnames: list[str] | None = None) -> None:
    fieldnames = fieldnames or DEFAULT_FIELDNAMES
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(listings)
    print(f"Saved {len(listings)} listings to {path}")
