"""Weather API access; the only package module importing requests."""

import logging

import requests

from .errors import DownloadError, ResponseFormatError
from .models import HourlyRecord

logger = logging.getLogger(__name__)
DataSourceError = DownloadError


class WeatherDataSource:
    """Download Open-Meteo hourly observations and validate records."""

    def __init__(self, url: str = "", timeout: float = 15) -> None:
        """Set the URL and HTTP timeout."""
        self.url = url
        self.timeout = timeout

    def fetch(self) -> list[HourlyRecord]:
        """Return valid observations or raise a package-specific exception."""
        logger.info("Starting weather data download")
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            raise DownloadError("Unable to download weather observations") from error
        try:
            payload = response.json()
        except ValueError as error:
            raise ResponseFormatError("Invalid JSON response") from error
        if not isinstance(payload, dict) or not isinstance(payload.get("hourly"), dict):
            raise ResponseFormatError("Missing or invalid hourly data")
        hourly = payload["hourly"]
        keys = ("time", "temperature_2m", "precipitation")
        arrays = [hourly.get(key) for key in keys]
        if not all(isinstance(values, list) for values in arrays):
            raise ResponseFormatError("Missing hourly response arrays")
        times, temperatures, precipitation = arrays
        if not len(times) == len(temperatures) == len(precipitation):
            raise ResponseFormatError("Hourly arrays must have equal lengths")
        logger.debug("Received %s hourly observations", len(times))
        records: list[HourlyRecord] = []
        for timestamp, temp, precip in zip(
            times, temperatures, precipitation, strict=True
        ):
            try:
                if not isinstance(timestamp, str):
                    raise ValueError("Invalid timestamp")
                records.append(HourlyRecord(timestamp, temp, precip))
            except (ValueError, TypeError) as error:
                logger.warning(
                    "Skipping invalid observation at %s: %s", timestamp, error
                )
        return records
