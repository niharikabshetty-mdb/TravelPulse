from unittest.mock import patch

from services.travel_service import get_travel_data
from utils.api_helpers import APIError


def test_get_travel_data_chains_all_clients() -> None:
    location = {
        "city": "Paris",
        "country": "France",
        "country_code": "FR",
        "latitude": 48.85,
        "longitude": 2.35,
        "timezone": "Europe/Paris",
    }
    weather = {"temperature": 20, "humidity": 55, "wind_speed": 8, "condition": "Clear", "timezone": "Europe/Paris"}
    country = {"country": "France", "currency_code": "EUR"}
    currency = {"base": "EUR", "quote": "USD", "rate": 1.1, "message": "Live rate"}
    timezone = {"timezone": "Europe/Paris", "local_time": "Monday, January 1, 2026 at 12:00 PM", "utc_offset": "UTC+0100"}

    with patch("services.travel_service.geocode_destination", return_value=location), patch(
        "services.travel_service.get_current_weather", return_value=weather
    ), patch("services.travel_service.get_country_info", return_value=country), patch(
        "services.travel_service.get_exchange_info", return_value=currency
    ), patch("services.travel_service.get_local_time", return_value=timezone):
        result = get_travel_data("Paris")

    assert result["location"]["city"] == "Paris"
    assert result["currency"]["rate"] == 1.1


def test_get_travel_data_propagates_friendly_api_failure() -> None:
    with patch("services.travel_service.geocode_destination", side_effect=APIError("No destination was found")):
        try:
            get_travel_data("Unknown")
        except APIError as error:
            assert str(error) == "No destination was found"
        else:
            raise AssertionError("Expected APIError")