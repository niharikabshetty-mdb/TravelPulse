from unittest.mock import patch

from api.currency import get_exchange_info
from api.timezone import get_local_time


def test_same_currency_does_not_call_api() -> None:
    assert get_exchange_info("EUR", "EUR")["rate"] == 1.0


def test_currency_normalizes_rate() -> None:
    with patch("api.currency.get_json", return_value={"rates": {"USD": 1.08}}):
        result = get_exchange_info("EUR")
    assert result["rate"] == 1.08


def test_timezone_returns_local_time() -> None:
    result = get_local_time("Europe/Paris")
    assert result["timezone"] == "Europe/Paris"
    assert "at" in result["local_time"]