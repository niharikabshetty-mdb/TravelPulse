"""Open-Meteo current weather client."""

from typing import Any

from utils.api_helpers import APIError, get_json


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


def weather_condition(code: int | None) -> str:
    return WEATHER_CODES.get(code, "Unknown conditions")


def get_current_weather(latitude: float, longitude: float) -> dict[str, Any]:
    payload = get_json(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "auto",
        },
    )
    current = payload.get("current", {}) if isinstance(payload, dict) else {}
    try:
        code = int(current["weather_code"])
        return {
            "temperature": float(current["temperature_2m"]),
            "humidity": int(current["relative_humidity_2m"]),
            "wind_speed": float(current["wind_speed_10m"]),
            "weather_code": code,
            "condition": weather_condition(code),
            "timezone": payload.get("timezone", "UTC"),
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise APIError("The weather response was missing current conditions.") from exc