import re
from bs4 import BeautifulSoup


def _clean_number(text: str) -> str:
    return re.sub(r"[^\d]", "", text)


def _clean_decimal(text: str) -> str:
    """Keep digits and comma/dot, return as string with dot separator."""
    cleaned = re.sub(r"[^\d,.]", "", text).replace(",", ".")
    return cleaned


def parse_listing_detail(html: str) -> dict:
    """Parse a single listing detail page. Returns a flat dict of all fields."""
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # --- Stats bar: price, area, rooms, floor, elevator, year_built ---
    # Price block: <span class="block">360 000 <span>zł</span></span>
    price_block = soup.find("span", class_=lambda c: c and "block" in c,
                            string=lambda t: False)
    # Find by looking for the zł child span inside a block span
    for span in soup.find_all("span", class_="block"):
        child = span.find("span", class_=lambda c: c and "text-neutral-600" in c)
        if child and child.get_text(strip=True) in ("zł",):
            raw = re.sub(r"\s", "", span.get_text(strip=True).replace("zł", ""))
            result["price_total_zl"] = _clean_number(raw)
            break

    # Price per m²
    for span in soup.find_all("span"):
        t = span.get_text(strip=True)
        if "zł / m²" in t and "text-neutral-600" in " ".join(span.get("class") or []):
            result["price_per_m2_zl"] = _clean_number(t)
            break

    # Area: <span class="block">42,42 <span>m²</span></span>
    for span in soup.find_all("span", class_="block"):
        child = span.find("span")
        if child and child.get_text(strip=True) == "m²":
            raw = span.get_text(strip=True).replace("m²", "").strip()
            result["area_m2"] = _clean_decimal(raw)
            break

    # Rooms: <span class="block ..."><b>2</b> <span>pokoje</span></span>
    for span in soup.find_all("span", class_=lambda c: c and "block" in c):
        child = span.find("span", class_=lambda c: c and "text-neutral-600" in c)
        if child and child.get_text(strip=True) in ("pokoje", "pokój", "pok."):
            b = span.find("b")
            result["rooms"] = b.get_text(strip=True) if b else _clean_number(
                span.get_text(strip=True).replace(child.get_text(strip=True), ""))
            break

    # Floor: <span class="block">3 <span>piętro</span></span>
    for span in soup.find_all("span", class_="block"):
        child = span.find("span")
        if child and child.get_text(strip=True) == "piętro":
            result["floor"] = _clean_number(
                span.get_text(strip=True).replace("piętro", ""))
            # Elevator: sibling span with "brak windy" / "winda"
            parent_div = span.find_parent("div")
            if parent_div:
                for sib in parent_div.find_all("span"):
                    t = sib.get_text(strip=True)
                    if "winda" in t.lower():
                        result["elevator"] = "nie" if "brak" in t.lower() else "tak"
                        break
            break

    # Year built: <span class="block">1976</span> followed by <span>rok budowy</span>
    for span in soup.find_all("span", class_=lambda c: c and "text-neutral-600" in c):
        if span.get_text(strip=True) == "rok budowy":
            prev = span.find_previous_sibling("span", class_="block")
            if prev:
                result["year_built"] = prev.get_text(strip=True)
            break

    # --- Structured UL detail items ---
    detail_ul = soup.find(
        "ul",
        class_=lambda c: c and "mt-6" in c and "px-4" in c and "text-neutral-800" in c,
    )
    if detail_ul:
        for li in detail_ul.find_all("li", recursive=False):
            spans = li.find_all("span", class_="block")
            if len(spans) < 2:
                continue
            main_text = spans[0].get_text(strip=True)
            sub_text = spans[1].get_text(strip=True)

            if "Na sprzedaż" in main_text or "m²" in main_text:
                result["listing_summary"] = main_text
                result["features"] = sub_text
            elif "piętro" in main_text and "blok" in main_text:
                result["building_info"] = main_text
                result["building_details"] = sub_text
            elif re.search(r"(Łódź|Warszawa|Kraków|Mielec|Wrocław|Poznań|miasto)", main_text, re.I):
                result["locality"] = main_text
                result["street"] = sub_text
            elif "stan" in main_text.lower() or "odświeżenia" in main_text.lower() or "deweloperski" in main_text.lower():
                result["condition"] = main_text
                result["windows"] = sub_text
            elif "własność" in main_text.lower() or "spółdzielcze" in main_text.lower():
                result["ownership"] = main_text
            elif "Wyposażenie" in main_text:
                result["equipment"] = sub_text
            elif "Cena do negocjacji" in main_text:
                result["price_negotiable"] = "tak"
            elif "właściciela" in main_text.lower() or "agenta" in main_text.lower() or "agencj" in main_text.lower():
                result["offer_type"] = main_text.strip()
                result["added"] = sub_text

    if "price_negotiable" not in result:
        result["price_negotiable"] = "nie"

    # --- Description ---
    section = soup.find("section")
    if section:
        result["description"] = section.get_text(" ", strip=True)

    return result


DETAIL_FIELDNAMES = [
    "price_total_zl",
    "price_per_m2_zl",
    "area_m2",
    "rooms",
    "floor",
    "elevator",
    "year_built",
    "listing_summary",
    "features",
    "building_info",
    "building_details",
    "locality",
    "street",
    "condition",
    "windows",
    "ownership",
    "equipment",
    "price_negotiable",
    "offer_type",
    "added",
    "description",
]
