import requests

BASE_URL = "https://adresowo.pl"
LISTING_URL = "https://adresowo.pl/mieszkania/{city}/_l{page}"
DELAY_SECONDS = 0.25


def city_page_url(city: str, page: int) -> str:
    return LISTING_URL.format(city=city, page=page)


def fetch_html(url: str, timeout: int = 20) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8",
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text
