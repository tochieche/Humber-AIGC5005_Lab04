
"""Test polymorphic aggregation execution in ReportBuilder."""

import unittest
from unittest.mock import patch

from lab3package.aggregations import (
    Aggregation,
    DailyTemperatureAggregation,
    ConditionCountAggregation,
    RecentReadingsAggregation,
)
from lab3package.models import HourlyRecord
from lab3package.report import ReportBuilder


class TestPolymorphism(unittest.TestCase):
    """Verify that ReportBuilder uses polymorphism correctly."""

    def setUp(self):
        """Create sample weather observations for testing."""
        self.records = [
            HourlyRecord("2026-10-14T10:00", 18.5, 0.0),
            HourlyRecord("2026-10-14T11:00", 20.0, 1.2),
        ]

    def test_aggregation_list(self):
        """Verify all configured objects inherit from Aggregation."""
        builder = ReportBuilder(self.records)

        self.assertEqual(len(builder.aggregations), 3)

        for aggregation in builder.aggregations:
            self.assertIsInstance(aggregation, Aggregation)

    def test_all_compute_methods_called(self):
        """Verify each aggregation executes through the shared interface."""
        builder = ReportBuilder(self.records)

        daily_result = {
            "2026-10-14": {"max_temp_c": 20.0}
        }

        condition_result = {
            "Warm Dry": 1,
            "Precipitation": 1,
        }

        recent_result = [
            {"timestamp": "2026-10-14T11:00"}
        ]

        with (
            patch.object(
                DailyTemperatureAggregation,
                "compute",
                return_value=daily_result,
            ) as daily_mock,
            patch.object(
                ConditionCountAggregation,
                "compute",
                return_value=condition_result,
            ) as condition_mock,
            patch.object(
                RecentReadingsAggregation,
                "compute",
                return_value=recent_result,
            ) as recent_mock,
        ):
            summary = builder.build()

        daily_mock.assert_called_once_with(self.records)
        condition_mock.assert_called_once_with(self.records)
        recent_mock.assert_called_once_with(self.records)

        self.assertEqual(
            summary["hottest_day"],
            "2026-10-14",
        )

        self.assertEqual(
            summary["hottest_day_max_temp_c"],
            20.0,
        )

        self.assertEqual(
            summary["condition_counts"],
            condition_result,
        )

        self.assertEqual(
            summary["recent_readings"],
            recent_result,
        )


if __name__ == "__main__":
    unittest.main()
