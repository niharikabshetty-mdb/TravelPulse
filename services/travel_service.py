"""Coordinate TravelPulse API calls into one dashboard-ready payload."""

from typing import Any

from api.country import get_country_info
from api.currency import get_exchange_info
from api.geocoding import geocode_destination
from api.timezone import get_local_time
from api.weather import get_current_weather


def get_travel_data(destination: str) -> dict[str, Any]:
    """Run the destination -> weather/country/currency/time API chain."""
    location = geocode_destination(destination)
    weather = get_current_weather(location["latitude"], location["longitude"])
    country = get_country_info(location["country_code"], location["country"])
    currency = get_exchange_info(country["currency_code"])
    timezone = get_local_time(weather.get("timezone") or location.get("timezone", "UTC"))

    return {
        "location": location,
        "weather": weather,
        "country": country,
        "currency": currency,
        "timezone": timezone,
    }