"""Polymorphism tests exercising actual aggregation implementations."""

from unittest.mock import patch

from lab3package.aggregations import (
    Aggregation,
    ConditionCountAggregation,
    DailyTemperatureAggregation,
    RecentReadingsAggregation,
)
from lab3package.models import HourlyRecord
from lab3package.report import ReportBuilder


def test_aggregation_list(sample_records: list[HourlyRecord]) -> None:
    """Store three strategies via the shared interface."""
    builder = ReportBuilder(sample_records)
    assert len(builder.aggregations) == 3
    assert all(isinstance(a, Aggregation) for a in builder.aggregations)


def test_each_compute_called(sample_records: list[HourlyRecord]) -> None:
    """Execute each override exactly once."""
    builder = ReportBuilder(sample_records)
    with (
        patch.object(
            DailyTemperatureAggregation,
            "compute",
            wraps=builder.aggregations[0].compute,
        ) as daily,
        patch.object(
            ConditionCountAggregation,
            "compute",
            wraps=builder.aggregations[1].compute,
        ) as conditions,
        patch.object(
            RecentReadingsAggregation,
            "compute",
            wraps=builder.aggregations[2].compute,
        ) as recent,
    ):
        summary = builder.build()
    daily.assert_called_once_with(sample_records)
    conditions.assert_called_once_with(sample_records)
    recent.assert_called_once_with(sample_records)
    assert summary["records_processed"] == 3
