"""Tests for expected data-source failures."""

from unittest.mock import Mock

import pytest
import requests

from lab3package.errors import DownloadError, ResponseFormatError
from lab3package.sources import WeatherDataSource


def test_download_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Translate a connection failure into DownloadError."""

    def fail(*args: object, **kwargs: object) -> None:
        raise requests.ConnectionError("offline")

    monkeypatch.setattr("lab3package.sources.requests.get", fail)

    source = WeatherDataSource(
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=43.65&longitude=-79.38"
        "&hourly=temperature_2m,precipitation"
        "&past_days=7&forecast_days=0"
        "&timezone=America%2FToronto"
    )

    with pytest.raises(DownloadError, match="Unable to download"):
        source.fetch()


def test_malformed_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reject an API response without hourly data."""
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"unexpected": "data"}

    monkeypatch.setattr(
        "lab3package.sources.requests.get",
        lambda *args, **kwargs: response,
    )

    source = WeatherDataSource(
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=43.65&longitude=-79.38"
        "&hourly=temperature_2m,precipitation"
        "&past_days=7&forecast_days=0"
        "&timezone=America%2FToronto"
    )

    with pytest.raises(ResponseFormatError, match="hourly"):
        source.fetch()
