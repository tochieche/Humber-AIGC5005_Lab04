
import requests

from .config import SOURCE_URL, TIMEOUT
from .models import HourlyRecord


class DataSourceError(Exception):
    """Raised when weather data cannot be downloaded or decoded."""


class WeatherDataSource:
    """Retrieve and parse hourly weather observations.

    This class manages communication with the weather API
    and converts valid response entries into HourlyRecord
    objects.

    Invalid hourly observations are excluded.
    """

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT):
        """Configure the weather API data source.

        Args:
            url (str): API endpoint used to retrieve data.
            timeout (int | float): Maximum request duration
                in seconds.
        """
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download and validate hourly weather observations.

        The method requests weather data, extracts the
        hourly timestamps, temperatures, and precipitation
        values, and creates HourlyRecord objects.

        Records containing missing or malformed values
        are skipped.

        Returns:
            list[HourlyRecord]: Valid hourly observations
                retrieved from the API.

        Raises:
            DataSourceError: If the API request fails or
                the response cannot be decoded, when using
                the custom error handling from the
                previous correction.
        """

        try:
            response = requests.get(
                self.url,
                timeout=self.timeout
            )
            response.raise_for_status()
            payload = response.json()

        except (requests.RequestException, ValueError) as err:
            raise DataSourceError(
                f"Unable to retrieve weather data: {err}"
            ) from err

        hourly = payload.get("hourly", {})

        timestamps = hourly.get("time", [])
        temperatures = hourly.get("temperature_2m", [])
        precipitations = hourly.get("precipitation", [])

        records = []

        for ts, temp, precip in zip(
            timestamps,
            temperatures,
            precipitations
        ):
            if ts is None or temp is None or precip is None:
                continue

            try:
                record = HourlyRecord(ts, temp, precip)
                records.append(record)
            except ValueError:
                continue

        return records
