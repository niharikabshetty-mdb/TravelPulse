"""REST Countries client."""

from typing import Any

from utils.api_helpers import APIError, get_json


COUNTRY_URL = "https://restcountries.com/v3.1/alpha"


def get_country_info(country_code: str, country_name: str = "") -> dict[str, Any]:
    """Fetch and normalize country information from an ISO alpha-2 code."""
    if not country_code:
        raise APIError("Country information is unavailable for this destination.")
    payload = get_json(f"{COUNTRY_URL}/{country_code}")
    record = payload[0] if isinstance(payload, list) and payload else payload
    if not isinstance(record, dict):
        raise APIError("The country response did not contain country details.")

    currencies = record.get("currencies") or {}
    currency_code, currency_data = next(iter(currencies.items()), ("", {}))
    capitals = record.get("capital") or []
    return {
        "country": record.get("name", {}).get("common", country_name),
        "capital": capitals[0] if capitals else "Not available",
        "region": record.get("region", "Not available"),
        "subregion": record.get("subregion", "Not available"),
        "continent": (record.get("continents") or ["Not available"])[0],
        "population": record.get("population", 0),
        "currency_code": currency_code,
        "currency_name": currency_data.get("name", "Not available"),
        "currency_symbol": currency_data.get("symbol", ""),
        "flag": record.get("flags", {}).get("svg", record.get("flags", {}).get("png", "")),
    }