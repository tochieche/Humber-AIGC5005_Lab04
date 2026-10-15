
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
    """Verify that an empty genre list raises ValueError."""
    with pytest.raises(ValueError, match="Genre list is required"):
        ShowRecord(
            name="Sample Show",
            genres=(),
            rating=8.0,
        )


def test_missing_rating() -> None:
    """Verify that a missing rating raises ValueError."""
    with pytest.raises(ValueError, match="Rating is required"):
        ShowRecord(
            name="Sample Show",
            genres=("Drama",),
            rating=None,
        )

def test_valid_show_record() -> None:
    """Verify that valid show information is accepted."""
    show = ShowRecord(
        name="Sample Show",
        genres=("Drama", "Comedy"),
        rating=8.5,
    )

    assert show.name == "Sample Show"
    assert show.rating == 8.5
    assert show.genres == ("Drama", "Comedy")
