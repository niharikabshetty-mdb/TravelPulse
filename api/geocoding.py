"""Open-Meteo geocoding client."""

from typing import Any

from utils.api_helpers import APIError, get_json


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode_destination(destination: str) -> dict[str, Any]:
    """Return the best matching city and coordinates for a destination."""
    query = destination.strip()
    if not query:
        raise APIError("Enter a destination before searching.")

    payload = get_json(
        GEOCODING_URL,
        params={"name": query, "count": 1, "language": "en", "format": "json"},
    )
    results = payload.get("results", []) if isinstance(payload, dict) else []
    if not results:
        raise APIError(f"No destination was found for '{query}'.")

    result = results[0]
    try:
        return {
            "city": result["name"],
            "country": result["country"],
            "country_code": result.get("country_code", ""),
            "latitude": float(result["latitude"]),
            "longitude": float(result["longitude"]),
            "timezone": result.get("timezone", "UTC"),
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise APIError("The geocoding response was missing location details.") from exc