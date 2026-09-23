from unittest.mock import patch

import pytest

from api.geocoding import geocode_destination
from utils.api_helpers import APIError


def test_geocode_destination_normalizes_result() -> None:
    payload = {"results": [{"name": "Paris", "country": "France", "latitude": 48.85, "longitude": 2.35}]}
    with patch("api.geocoding.get_json", return_value=payload):
        result = geocode_destination(" Paris ")
    assert result["city"] == "Paris"
    assert result["latitude"] == 48.85


def test_geocode_destination_rejects_empty_input() -> None:
    with pytest.raises(APIError, match="Enter a destination"):
        geocode_destination("  ")


def test_geocode_destination_handles_no_results() -> None:
    with patch("api.geocoding.get_json", return_value={"results": []}):
        with pytest.raises(APIError, match="No destination"):
            geocode_destination("Atlantis")