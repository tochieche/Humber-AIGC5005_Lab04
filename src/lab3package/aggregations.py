
"""Provide aggregation strategies for hourly weather observations."""

from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from typing import TypeAlias

AggregationResult: TypeAlias = (
    dict[str, dict[str, float | int]]
    | dict[str, int]
    | list[dict[str, str | float]]
)


class Aggregation(ABC):
    """Define the common interface for weather aggregations.

    Subclasses implement the compute method to perform
    a specific calculation on hourly weather records.
    """

    @abstractmethod
    def compute(self, records) -> Any:
        """Compute statistics from hourly weather records.

        Args:
            records: Collection of HourlyRecord objects.

        Returns:
            Any: Aggregation results determined by
                the implementing subclass.
        """
        pass


class DailyTemperatureAggregation(Aggregation):
    """Calculate daily temperature and precipitation statistics.

    Groups hourly observations by calendar date and
    calculates daily minimum, maximum, and average
    temperature, total precipitation, and record count.
    """

     @abstractmethod
    def compute(
        self,
        records: list[HourlyRecord],
    ) -> AggregationResult:
        """Return the calculated weather aggregation."""
        """Aggregate hourly observations into daily statistics.

        Args:
            records: Collection of HourlyRecord objects.

        Returns:
            dict: Mapping of dates to daily statistics,
                including temperature, precipitation,
                and number of readings.
        """
        grouped = defaultdict(list)

        for rec in records:
            date_str = rec.timestamp.split("T")[0]
            grouped[date_str].append(rec)

        return {
            date: {
                "min_temp_c": round(
                    min(r.temperature for r in day_recs), 1
                ),
                "max_temp_c": round(
                    max(r.temperature for r in day_recs), 1
                ),
                "avg_temp_c": round(
                    sum(r.temperature for r in day_recs)
                    / len(day_recs), 1
                ),
                "total_precip_mm": round(
                    sum(r.precipitation for r in day_recs), 1
                ),
                "readings": len(day_recs),
            }
            for date, day_recs in grouped.items()
        }


class ConditionCountAggregation(Aggregation):
    """Classify and count weather conditions.

    Categorizes hourly records as Precipitation,
    Freezing Dry, Cool Dry, or Warm Dry according
    to precipitation and temperature measurements.
    """

    def compute(self, records) -> dict[str, int]:
        """Count observations in each weather category.

        Args:
            records: Collection of HourlyRecord objects.

        Returns:
            dict[str, int]: Weather category names mapped
                to their observation counts.
        """
        conditions = []

        for rec in records:
            if rec.precipitation > 0.0:
                conditions.append("Precipitation")
            elif rec.temperature < 0.0:
                conditions.append("Freezing Dry")
            elif rec.temperature < 15.0:
                conditions.append("Cool Dry")
            else:
                conditions.append("Warm Dry")

        return dict(Counter(conditions))


class RecentReadingsAggregation(Aggregation):
    """Retrieve the most recent hourly weather observations.

    Limits the returned observations to a configurable
    number and formats each record as a dictionary.
    """

    def __init__(self, count=5):
        """Initialize the recent observation limit.

        Args:
            count (int): Number of recent observations
                to include. Defaults to five.
        """
        self.count = count

    def compute(self, records) -> list[dict[str, Any]]:
        """Return the most recent weather observations.

        Args:
            records: Chronologically ordered collection
                of HourlyRecord objects.

        Returns:
            list[dict]: Recent observations containing
                timestamp, temperature, and precipitation.
        """
        recent = (
            records[-self.count:]
            if len(records) >= self.count
            else records
        )

        return [
            {
                "timestamp": r.timestamp,
                "temperature_c": r.temperature,
                "precipitation_mm": r.precipitation,
            }
            for r in recent
        ]
