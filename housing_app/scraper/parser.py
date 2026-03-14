import re
from bs4 import BeautifulSoup


BASE_URL = "https://adresowo.pl"


def _clean_number(text: str) -> str:
    """Remove non-digit characters except dot/comma, normalize to int string."""
    return re.sub(r"[^\d]", "", text)


def parse_listings(html: str) -> list[dict]:
    """Parse apartment listing cards from HTML and return list of dicts."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", attrs={"data-offer-card": True})

    results = []
    for card in cards:
        offer_id = card.get("data-id", "")

        # URL
        anchor = card.find("a", href=True)
        url = BASE_URL + anchor["href"] if anchor else ""

        # Locality (bold span inside h2 > a)
        locality_tag = card.find("span", class_=lambda c: c and "font-bold" in c and "tracking-wide" in c)
        locality = locality_tag.get_text(strip=True) if locality_tag else ""

        # Price, area, rooms — the three <p class="flex-auto"> blocks
        stat_paragraphs = card.find_all("p", class_=lambda c: c and "flex-auto" in c and "text-base" in c)

        price_total_zl = ""
        area_m2 = ""
        rooms = ""

        if len(stat_paragraphs) >= 3:
            price_raw = stat_paragraphs[0].find("span", class_="font-bold")
            area_raw = stat_paragraphs[1].find("span", class_="font-bold")
            rooms_raw = stat_paragraphs[2].find("span", class_="font-bold")

            price_total_zl = _clean_number(price_raw.get_text()) if price_raw else ""
            area_m2 = _clean_number(area_raw.get_text()) if area_raw else ""
            rooms = _clean_number(rooms_raw.get_text()) if rooms_raw else ""

        # price per m²
        price_per_m2_zl = ""
        if price_total_zl and area_m2 and int(area_m2) > 0:
            price_per_m2_zl = str(round(int(price_total_zl) / int(area_m2)))

        results.append({
            "id": offer_id,
            "url": url,
            "locality": locality,
            "rooms": rooms,
            "area_m2": area_m2,
            "price_total_zl": price_total_zl,
            "price_per_m2_zl": price_per_m2_zl,
        })

    return results
