"""REST Countries client."""

from typing import Any

from utils.api_helpers import APIError, get_json


COUNTRY_URL = "https://restcountries.com/v3.1/alpha"
COUNTRY_FALLBACK_URL = "https://countriesnow.space/api/v0.1/countries/info?returns=currency,flag,capital,iso2"


def _fallback_country_info(country_name: str, country_code: str) -> dict[str, Any]:
    payload = get_json(COUNTRY_FALLBACK_URL)
    records = payload.get("data", []) if isinstance(payload, dict) else []
    wanted_code = country_code.upper()
    wanted_name = country_name.casefold()
    record = next(
        (
            item
            for item in records
            if item.get("iso2", "").upper() == wanted_code
            or item.get("name", "").casefold() == wanted_name
        ),
        None,
    )
    if not record:
        raise APIError("Country information is unavailable for this destination.")
    return {
        "country": record.get("name", country_name),
        "capital": record.get("capital") or "Not available",
        "region": "Not available",
        "subregion": "Not available",
        "continent": "Not available",
        "population": 0,
        "currency_code": record.get("currency", ""),
        "currency_name": record.get("currency", "Not available"),
        "currency_symbol": "",
        "flag": record.get("flag", ""),
    }


def get_country_info(country_code: str, country_name: str = "") -> dict[str, Any]:
    """Fetch and normalize country information from an ISO alpha-2 code."""
    if not country_code:
        raise APIError("Country information is unavailable for this destination.")
    payload = get_json(f"{COUNTRY_URL}/{country_code}")
    if isinstance(payload, dict) and payload.get("success") is False:
        return _fallback_country_info(country_name, country_code)
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