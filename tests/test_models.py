
"""Tests for weather record validation."""

import pytest
from lab3package.models import HourlyRecord
from lab3package.models import ShowRecord


def test_valid_record() -> None:
    """Accept a valid weather observation."""
    record = HourlyRecord("2026-10-14T09:00", 12.5, 0.0)
    assert record.temperature == 12.5


@pytest.mark.parametrize(
    ("temperature", "expected"),
    [
        ("10.5", 10.5),
        (0, 0.0),
        (-5, -5.0),
    ],
)
def test_temperature_conversion(
    temperature: str | int,
    expected: float,
) -> None:
    """Convert supported temperatures to floating-point values."""
    record = HourlyRecord("2026-10-14T09:00", temperature, 0)
    assert record.temperature == expected


def test_missing_temperature() -> None:
    """Reject missing temperatures with an explanatory error."""
    with pytest.raises(ValueError, match="cannot be None"):
        HourlyRecord("2026-10-14T09:00", None, 0.0)


def test_missing_timestamp() -> None:
    """Reject records without timestamps."""
    with pytest.raises(ValueError, match="Timestamp"):
        HourlyRecord(None, 10.0, 0.0)


def test_invalid_temperature() -> None:
    """Reject nonnumeric temperatures."""
    with pytest.raises(ValueError, match="Invalid"):
        HourlyRecord("2026-10-14T09:00", "invalid", 0.0)



def test_missing_genre_list() -> None:
    """Reject a show without genres."""
    with pytest.raises(ValueError, match="Genre list"):
        ShowRecord("Sample Show", (), 8.0)


def test_missing_rating() -> None:
    """Reject a show without a rating."""
    with pytest.raises(
        (TypeError, ValueError),
        match="Rating|NoneType|not supported",
    ):
        ShowRecord("Sample Show", ("Drama",), None)
