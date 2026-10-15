
"""Tests for weather aggregation strategies."""

from lab3package.aggregations import (
    ConditionCountAggregation,
    DailyTemperatureAggregation,
    RecentReadingsAggregation,
)
from lab3package.models import HourlyRecord


def test_daily_temperature(sample_records: list[HourlyRecord]) -> None:
    """Calculate the daily maximum correctly."""
    result = DailyTemperatureAggregation().compute(sample_records)

    assert result["2026-10-14"]["max_temp_c"] == 20.0


def test_daily_precipitation(sample_records: list[HourlyRecord]) -> None:
    """Calculate daily precipitation totals."""
    result = DailyTemperatureAggregation().compute(sample_records)

    assert result["2026-10-14"]["total_precip_mm"] == 1.5


def test_condition_counts(sample_records: list[HourlyRecord]) -> None:
    """Count weather conditions correctly."""
    result = ConditionCountAggregation().compute(sample_records)

    assert result["Precipitation"] == 1
    assert result["Cool Dry"] == 2


def test_recent_readings(sample_records: list[HourlyRecord]) -> None:
    """Return the requested number of latest observations."""
    result = RecentReadingsAggregation(count=2).compute(sample_records)

    assert len(result) == 2
    assert result[-1]["temperature_c"] == 5.0
