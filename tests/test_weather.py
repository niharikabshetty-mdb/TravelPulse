from unittest.mock import patch

from api.weather import get_current_weather


def test_get_current_weather_normalizes_current_conditions() -> None:
    payload = {
        "timezone": "Europe/Paris",
        "current": {
            "temperature_2m": 21.5,
            "relative_humidity_2m": 60,
            "wind_speed_10m": 12.0,
            "weather_code": 1,
        },
    }
    with patch("api.weather.get_json", return_value=payload):
        result = get_current_weather(48.85, 2.35)
    assert result["temperature"] == 21.5
    assert result["condition"] == "Mainly clear"
    assert result["timezone"] == "Europe/Paris"