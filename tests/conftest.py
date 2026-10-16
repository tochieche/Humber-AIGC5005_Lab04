"""Shared fixtures for the Lab 04 test suite."""

import pytest

from lab3package.models import HourlyRecord


@pytest.fixture
def sample_records() -> list[HourlyRecord]:
    """Return deterministic hourly weather observations."""
    return [
        HourlyRecord("2026-10-14T09:00", 10.0, 0.0),
        HourlyRecord("2026-10-14T10:00", 20.0, 1.5),
        HourlyRecord("2026-10-15T09:00", 5.0, 0.0),
    ]


@pytest.fixture
def sample_payload() -> dict[str, object]:
    """Return a valid Open-Meteo response without using the network."""
    return {
        "hourly": {
            "time": ["2026-10-14T09:00", "2026-10-14T10:00"],
            "temperature_2m": [10.0, 20.0],
            "precipitation": [0.0, 1.5],
        }
    }
