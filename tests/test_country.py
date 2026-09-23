from unittest.mock import patch

from api.country import get_country_info


def test_get_country_info_handles_optional_fields() -> None:
    payload = [{"name": {"common": "France"}, "region": "Europe", "currencies": {"EUR": {"name": "Euro", "symbol": "€"}}}]
    with patch("api.country.get_json", return_value=payload):
        result = get_country_info("FR", "France")
    assert result["country"] == "France"
    assert result["capital"] == "Not available"
    assert result["currency_code"] == "EUR"


def test_get_country_info_uses_fallback_when_provider_is_deprecated() -> None:
    deprecated = {"success": False, "data": None, "errors": [{"message": "deprecated"}]}
    fallback = {"data": [{"name": "France", "capital": "Paris", "currency": "EUR", "iso2": "FR"}]}
    with patch("api.country.get_json", side_effect=[deprecated, fallback]):
        result = get_country_info("FR", "France")
    assert result["capital"] == "Paris"
    assert result["currency_code"] == "EUR"