"""Frankfurter currency conversion client."""

from typing import Any

from utils.api_helpers import APIError, get_json


CURRENCY_URL = "https://api.frankfurter.app/latest"


def get_exchange_info(base_currency: str, quote_currency: str = "USD") -> dict[str, Any]:
    base = base_currency.upper().strip()
    quote = quote_currency.upper().strip()
    if not base:
        return {"base": "", "quote": quote, "rate": None, "message": "Currency unavailable"}
    if base == quote:
        return {"base": base, "quote": quote, "rate": 1.0, "message": "Same currency"}

    try:
        payload = get_json(CURRENCY_URL, params={"from": base, "to": quote})
        rate = payload.get("rates", {}).get(quote) if isinstance(payload, dict) else None
        if rate is None:
            return {"base": base, "quote": quote, "rate": None, "message": "Conversion unavailable"}
        return {"base": base, "quote": quote, "rate": float(rate), "message": "Live rate"}
    except APIError as exc:
        if exc.status_code in {400, 404}:
            return {"base": base, "quote": quote, "rate": None, "message": "Currency unsupported"}
        raise