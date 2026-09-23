from unittest.mock import Mock, patch

import pytest
import requests

from utils.api_helpers import APIError, get_json


def test_get_json_passes_query_parameters_and_returns_json() -> None:
    response = Mock(status_code=200)
    response.json.return_value = {"ok": True}

    with patch("utils.api_helpers.requests.get", return_value=response) as request:
        assert get_json("https://example.test/data", params={"city": "Paris"}) == {"ok": True}

    request.assert_called_once_with(
        "https://example.test/data", params={"city": "Paris"}, timeout=10
    )


def test_get_json_translates_http_error() -> None:
    response = Mock(status_code=404)
    response.raise_for_status.side_effect = requests.HTTPError("missing")

    with patch("utils.api_helpers.requests.get", return_value=response):
        with pytest.raises(APIError, match="HTTP 404") as error:
            get_json("https://example.test/missing")

    assert error.value.status_code == 404


def test_get_json_translates_timeout() -> None:
    with patch("utils.api_helpers.requests.get", side_effect=requests.Timeout):
        with pytest.raises(APIError, match="timed out"):
            get_json("https://example.test/slow")