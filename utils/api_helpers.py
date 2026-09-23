"""Shared HTTP behavior for TravelPulse API clients."""

from __future__ import annotations

from typing import Any

import requests


class APIError(RuntimeError):
    """An expected failure while calling or decoding a public API."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def get_json(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    timeout: float = 10,
) -> dict[str, Any] | list[Any]:
    """GET a JSON endpoint with status, timeout, and decoding checks."""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
    except requests.Timeout as exc:
        raise APIError("The API request timed out.") from exc
    except requests.ConnectionError as exc:
        raise APIError("The API could not be reached.") from exc
    except requests.HTTPError as exc:
        raise APIError(
            f"The API returned HTTP {response.status_code}.",
            status_code=response.status_code,
        ) from exc
    except requests.RequestException as exc:
        raise APIError("The API request failed.") from exc

    try:
        return response.json()
    except ValueError as exc:
        raise APIError("The API returned invalid JSON.", response.status_code) from exc