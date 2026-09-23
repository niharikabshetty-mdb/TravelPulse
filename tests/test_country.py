from unittest.mock import patch

from api.country import get_country_info


def test_get_country_info_handles_optional_fields() -> None:
    payload = [{"name": {"common": "France"}, "region": "Europe", "currencies": {"EUR": {"name": "Euro", "symbol": "€"}}}]
    with patch("api.country.get_json", return_value=payload):
        result = get_country_info("FR", "France")
    assert result["country"] == "France"
    assert result["capital"] == "Not available"
    assert result["currency_code"] == "EUR"