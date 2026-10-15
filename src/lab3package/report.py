
"""Build and export JSON weather reports using polymorphic aggregations."""

import json

from .config import SOURCE_URL, OUTPUT_PATH
from .aggregations import (
    Aggregation,
    DailyTemperatureAggregation,
    ConditionCountAggregation,
    RecentReadingsAggregation,
)
import logging

logger = logging.getLogger(__name__)

class ReportBuilder:
    """Generate weather reports using a collection of aggregations.

    Each aggregation inherits from Aggregation and implements
    the compute() method. ReportBuilder executes all aggregation
    objects polymorphically through the shared interface.
    """

    def __init__(self, records):
        """Initialize the report builder and its aggregations.

        Args:
            records: Validated HourlyRecord objects to summarize.
        """
        self.records = records

        self.aggregations: list[Aggregation] = [
            DailyTemperatureAggregation(),
            ConditionCountAggregation(),
            RecentReadingsAggregation(count=5),
        ]

    def build(self):
        """Execute each aggregation and construct the report.

        Iterates through the list of Aggregation objects and
        calls compute() on each, allowing Python to dispatch
        the call to the appropriate subclass implementation.

        Returns:
            dict: Weather summary containing daily statistics,
                condition counts, and recent observations.

        Raises:
            ValueError: If no daily weather statistics exist.
        """
        results = {}

        for aggregation in self.aggregations:
            results[type(aggregation).__name__] = (
                aggregation.compute(self.records)
            )

        daily_stats = results["DailyTemperatureAggregation"]
        condition_counts = results["ConditionCountAggregation"]
        recent_readings = results["RecentReadingsAggregation"]

        if not daily_stats:
            raise ValueError(
                "Cannot build a weather report without valid daily data."
            )

        hottest_day = max(
            daily_stats,
            key=lambda d: daily_stats[d]["max_temp_c"]
        )
        logger.info("Starting report generation")
        logger.debug("Processed %s records", len(self.records))
        return {
            "source_url": SOURCE_URL,
            "records_processed": len(self.records),
            "hottest_day": hottest_day,
            "hottest_day_max_temp_c": daily_stats[
                hottest_day
            ]["max_temp_c"],
            "daily_breakdown": daily_stats,
            "condition_counts": condition_counts,
            "recent_readings": recent_readings,
        }

    def write(self, path=OUTPUT_PATH):
        """Write the generated weather summary to a JSON file.

        Args:
            path: Destination Path for the JSON report.

        Returns:
            dict: The generated report summary.

        Raises:
            OSError: If the report cannot be written.
        """
        summary = self.build()

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return summary
