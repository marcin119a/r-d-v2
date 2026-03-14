def filter_listings(
    listings: list[dict],
    *,
    min_price: int | None = None,
    max_price: int | None = None,
    min_area: int | None = None,
    max_area: int | None = None,
    rooms: list[int] | None = None,
    locality: str | None = None,
) -> list[dict]:
    """Filter listings by price, area, rooms, and locality."""
    result = []
    for listing in listings:
        price_str = listing.get("price_total_zl", "")
        area_str = listing.get("area_m2", "")
        rooms_str = listing.get("rooms", "")

        if min_price is not None:
            if price_str == "" or int(price_str) < min_price:
                continue
        if max_price is not None:
            if price_str == "" or int(price_str) > max_price:
                continue
        if min_area is not None:
            if area_str == "" or int(area_str) < min_area:
                continue
        if max_area is not None:
            if area_str == "" or int(area_str) > max_area:
                continue
        if rooms is not None:
            if rooms_str == "" or int(rooms_str) not in rooms:
                continue
        if locality is not None:
            if locality.lower() not in listing.get("locality", "").lower():
                continue

        result.append(listing)
    return result
